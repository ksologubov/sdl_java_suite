import logging
import re
import textwrap
from abc import ABC
from collections import namedtuple, OrderedDict
from pathlib import Path

from model.Array import Array
from model.Enum import Enum
from model.Function import Function
from model.Struct import Struct


class InterfaceProducerCommon(ABC):
    def __init__(self, container_name, enums_package, structs_package, package_name,
                 enum_names=(), struct_names=(), mapping=OrderedDict()):
        self.logger = logging.getLogger('Generator.InterfaceProducerCommon')
        self.container_name = container_name
        self.enum_names = enum_names
        self.struct_names = struct_names
        self.enums_package = enums_package
        self.structs_package = structs_package
        self.mapping = mapping
        self.package_name = package_name

    @property
    def imports(self):
        """
        :return: namedtuple imports(what='', wherefrom='')
        """
        return namedtuple('Imports', 'what wherefrom')

    @property
    def methods(self):
        """
        :return: namedtuple methods(
                            origin='', key='', method_title='', external='', description='', param_name='', type='',)
        """
        return namedtuple('Methods', 'origin key method_title external description param_name type')

    @property
    def params(self):
        """
        :return: namedtuple params(key='', value='')
        """
        return namedtuple('Params', 'key value')

    def transform(self, item) -> dict:
        """
        :param item: particular element from initial Model
        :return: dictionary to be applied to jinja2 template
        """
        if not getattr(item, self.container_name, None):
            self.logger.info('{} of type {} has no attribute "{}"'.format(item.name, type(item).__name__,
                                                                          self.container_name))
            return {'name': item.name, 'imports': []}
        imports = {}
        methods = []
        params = []
        scripts = []

        if isinstance(item, Function):
            mapping_name = item.name + item.message_type.name.capitalize()
        else:
            mapping_name = item.name

        if mapping_name in self.mapping:
            if 'params_additional' in self.mapping[mapping_name]:
                params.append(self.params(**self.mapping[mapping_name]['params_additional']))
            if 'script_additional' in self.mapping[mapping_name]:
                script = self.get_file_content(self.mapping[mapping_name]['script_additional'])
                if script:
                    scripts.append(script)

        for param in getattr(item, self.container_name).values():
            if isinstance(item, Function) and item.message_type.name == 'response' and \
                            param.name in ('success', 'resultCode', 'info'):
                self.logger.warning('{} of type {}/{} - skip parameter "{}"'
                                    .format(item.name, type(item).__name__, item.message_type.name, param.name))
                continue

            (i, m, p) = self.common_flow(param, type(item))

            if mapping_name in self.mapping and param.name in self.mapping[mapping_name]:
                mapping = self.mapping[mapping_name][param.name]
                if 'imports' in mapping:
                    i = {mapping['imports']['what']: mapping['imports']['wherefrom']}
                if 'methods' in mapping:
                    d = m._asdict()
                    d.update(mapping['methods'])
                    m = self.methods(**d)
                if 'params' in mapping:
                    d = p._asdict()
                    d.update(mapping['params'])
                    p = self.params(**d)
                if 'script' in mapping:
                    script = self.get_file_content(mapping['script'])
                    if script:
                        self.logger.warning('the getter/setter for parameter {} will be replaced by manually provided '
                                            'from {}'.format(param.name, mapping['script']))
                        scripts.append(script)
                        m = None
            if i:
                imports.update(i)
            if m:
                methods.append(m)
            params.append(p)

        tmp = {'name': item.name,
               'imports': [self.imports(what=k, wherefrom=v) for k, v in imports.items()],
               'methods': methods,
               'params': params}
        if getattr(item, 'description', None):
            tmp.update({'description': self.extract_description(item.description)})
        if scripts:
            tmp.update({'scripts': scripts})
        return tmp

    def common_flow(self, param, item_type):
        """
        Main transformation flow, for Struct and Function
        :param param: sub-element (Param, FunctionParam) of element from initial Model
        :param item_type: type of parent element from initial Model
        :return: tuple with 3 element, which going to be applied to jinja2 template
        """
        (n, d) = self.extract_name_description(param)
        t = self.extract_type(param)
        imports = None
        if n:
            if n in self.enum_names:
                imports = {n: '{}/{}.js'.format(self.enums_dir, n)}
            elif n in self.struct_names:
                if item_type is Struct:
                    import_path = '.'
                else:
                    import_path = self.structs_dir
                imports = {n: '{}/{}.js'.format(import_path, n)}

        key = self.key(param.name)
        l = re.sub(r'^\w*([A-Z][a-z]\w*|[A-Z]{3,})$', r'\1', param.name).lower()
        d = textwrap.wrap(d, 102 - len(t) - len(l))
        title = param.name[:1].upper() + param.name[1:]

        methods = self.methods(origin=param.name, key=key, method_title=title, external=n, description=d,
                               param_name=l, type=t)
        params = self.params(key=key, value="'{}'".format(param.name))
        return imports, methods, params

    def extract_imports(self, extend):
        """
        Extract imports from property PATH_TO_(STRUCT|REQUEST|RESPONSE|NOTIFICATION)_CLASS
        :param extend: property to be evaluated and converted to self.imports
        :return: self.imports
        """
        tmp = re.match(r'.+/(.+).js', extend)
        if tmp:
            return self.imports(what=tmp.group(1), wherefrom=extend)

    @staticmethod
    def last(name):
        return re.sub(r'^\w*([A-Z][a-z]\w*|[A-Z]{2,})$', r'\1', name).lower()

    @staticmethod
    def key(param: str):
        """
        Convert param string to uppercase and inserting underscores
        :param param: camel case string
        :return: string in uppercase with underscores
        """
        if re.match(r'^[A-Z_\d]+$', param):
            return param
        else:
            return re.sub(r'([a-z]|[A-Z]{2,})([A-Z]|\d$)', r'\1_\2', param).upper()

    @staticmethod
    def ending_cutter(n: str):
        """
        If string not contains only uppercase letters and end with 'ID' deleting 'ID' from end of string
        :param n: string to evaluate and deleting 'ID' from end of string
        :return: if match cut string else original string
        """
        if re.match('^\w+[a-z]+([A-Z]{2,})?ID$', n):
            return n[:-2]
        else:
            return n

    @staticmethod
    def extract_description(d):
        """
        Evaluate, align and delete @TODO
        :param d: list with description
        :return: evaluated string
        """
        return re.sub(r'(\s{2,}|\n|\[@TODO.+)', ' ', ''.join(d)).strip() if d else ''

    @staticmethod
    def extract_name_description(param):
        """
        Extracting and evaluating name, description from appropriate place
        :param param: sub-element (Param, FunctionParam) of element from initial Model
        :return: tuple with 2 element (name, description)
        """
        n = None
        d = None
        if getattr(param, 'description', None):
            d = param.description

        if getattr(param, 'primary_name', None):
            n = param.primary_name
        elif getattr(param, 'param_type', None):
            if getattr(param.param_type, 'name', None):
                n = param.param_type.name
                if not d and getattr(param.param_type, 'description', None):
                    d = param.param_type.description
            elif getattr(param.param_type, 'element_type', None) and \
                    getattr(param.param_type.element_type, 'name', None):
                n = param.param_type.element_type.name
                if not d and getattr(param.param_type.element_type, 'description', None):
                    d = param.param_type.element_type.description

        return n, InterfaceProducerCommon.extract_description(d)

    @staticmethod
    def extract_type(param):
        """
        Evaluate and extract type
        :param param: sub-element (Param, FunctionParam) of element from initial Model
        :return: string with sub-element type
        """

        def evaluate(t1):
            if isinstance(t1, Struct) or isinstance(t1, Enum):
                return t1.name
            # elif isinstance(t1, Integer) or isinstance(t1, Double):
            #     return 'Number'
            else:
                return type(t1).__name__

        if isinstance(param.param_type, Array):
            return 'List<{}>'.format(evaluate(param.param_type.element_type))
        else:
            return evaluate(param.param_type)

    def get_file_content(self, file: str):
        """
        Used for getting content of custom scripts used in custom mapping
        :param file: relational path custom scripts
        :return: string with content of custom scripts
        """
        file = Path(__file__).absolute().parents[0].joinpath(file)
        try:
            with file.open('r') as f:
                s = f.readlines()
            return ''.join(s)
        except FileNotFoundError as e:
            self.logger.error(e)
            return ''

    def custom_mapping(self, render):
        """
        To be moved into parent class
        :param render: dictionary with moder ready for jinja template
        :return: None
        """
        custom = self.mapping[render['class_name']]

        for name in ('description', 'see', 'since', 'package_name'):
            if name in custom:
                render[name] = custom[name]
        if 'imports' in custom:
            if 'imports' in render:
                render['imports'].update(custom['imports'])
            else:
                render['imports'] = {custom['imports']}
        if '-imports' in custom:
            for i in custom['-imports']:
                if 'imports' in render:
                    render['imports'].remove(i)
        if '-params' in custom:
            for name in custom['-params']:
                if name in render['params']:
                    self.logger.warning('deleting parameter {}'.format(render['params'][name]))
                    del render['params'][name]
        if 'params_rename' in custom:
            for name, new_name in custom['params_rename'].items():
                if name in render['params']:
                    render['params'][new_name] = render['params'][name]._replace(name=new_name)
                    del render['params'][name]
        if 'script' in custom:
            script = self.get_file_content(custom['script'])
            if script:
                render.update({'scripts': [script]})
        if 'description_file' in custom:
            render['description'] = self.get_file_content(custom['description_file']).split('\n')

        if 'params' in custom:
            for name, value in custom['params'].items():
                if name in render['params']:
                    for k, v in value.items():
                        if isinstance(v, bool):
                            render['return_type'] = 'bool'
                            value.update({k: str(v).lower()})
                    d = render['params'][name]._asdict()
                    if 'description' in value:
                        d.update({'description': textwrap.wrap(value['description'], 113)})
                        del value['description']
                    if 'description_file' in value:
                        d.update({'description': self.get_file_content(value['description_file']).split('\n')})
                        del value['description_file']
                    if 'param_doc_file' in value:
                        d.update({'param_doc': self.get_file_content(value['param_doc_file']).split('\n')})
                        del value['param_doc_file']
                    if 'param_doc' in value:
                        d.update({'param_doc': textwrap.wrap(value['param_doc'], 100)})  # len(d['last'])
                        del value['param_doc']
                    if '-SuppressWarnings' in value:
                        del d['SuppressWarnings']
                        del value['-SuppressWarnings']
                    d.update(value)
                    Params = namedtuple('Params', sorted(d))
                    render['params'].update({name: Params(**d)})
                else:
                    for k, v in value.items():
                        if isinstance(v, bool):
                            value.update({k: str(v).lower()})
                    value.update({'name': name})
                    # if 'title' not in value:
                    #     value.update({'title': name[:1].upper() + name[1:]})
                    if 'description' in value:
                        value.update({'description': textwrap.wrap(value['description'], 113)})
                    if 'description_file' in value:
                        value.update({'description': self.get_file_content(custom['description_file']).split('\n')})
                        del value['description_file']
                    Params = namedtuple('Params', sorted(value))
                    render['params'].update({name: Params(**value)})
