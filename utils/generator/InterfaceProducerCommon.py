import logging
import re
import textwrap
from abc import ABC, abstractmethod
from collections import namedtuple
from pathlib import Path

import Generator
from jinja2 import Environment, FileSystemLoader

Generator.class_pass_imports()
try:
    import rpc_spec.InterfaceParser.Parser
    from rpc_spec.InterfaceParser.parsers.Model import Interface, Struct, Enum, Array, FunctionParam, EnumElement, Function, EnumSubset, \
        Integer, Double
except ModuleNotFoundError as e:
    print('{}. probably you did not initialize submodule'.format(e.msg))
    exit(1)


class InterfaceProducerCommon(ABC):
    def __init__(self, prop, enum_names=None, struct_names=None):
        self.logger = logging.getLogger('Generator.InterfaceProducerCommon')
        self.enum_names = enum_names
        self.struct_names = struct_names
        self.output = Path(prop.output_directory)
        self.skip = prop.skip
        self.overwrite = prop.overwrite
        self.enums_dir = prop.ENUMS_DIR_NAME
        self.structs_dir = prop.STRUCTS_DIR_NAME
        self.env = Environment(loader=FileSystemLoader(prop.templates_directory))

    @property
    def imports(self):
        return namedtuple('Imports', 'what wherefrom')

    @property
    def methods(self):
        return namedtuple('Methods', 'key upper last foreign description type')

    @staticmethod
    def underscore(param):
        if re.match(r'^[A-Z_]+$', param):
            return param
        else:
            return re.sub(r'([a-z]|[A-Z]{3,})([A-Z])', r'\1_\2', param).upper()

    @property
    @abstractmethod
    def items(self) -> list:
        pass

    @property
    @abstractmethod
    def directory(self) -> str:
        pass

    @property
    @abstractmethod
    def container_name(self) -> str:
        pass

    def make_directory(self) -> Path:
        path = re.search(r'^([../]*)(.+)', self.directory)
        if path:
            path = self.output.joinpath(path.group(2))
        else:
            path = self.output.joinpath('temp')
            self.logger.warning('can not evaluate {}, will use "{}"'.format(self.directory, path))
        path.mkdir(parents=True, exist_ok=True)
        return path

    def process(self):
        path = self.make_directory()

        def write_file():
            data = self.transform(item)
            with file.open('w', encoding='utf-8') as f:
                f.write(self.env.get_template(name_type.lower() + '_template.js').render(data))

        for item in self.items:
            name_type = type(item).__name__
            file = path.joinpath(item.name + '.js')
            if isinstance(item, Function) and item.message_type.name == 'response':
                file = path.joinpath(item.name + item.message_type.name.capitalize() + '.js')
            if file.is_file():
                if self.skip:
                    self.logger.debug('Skipping {}'.format(file))
                    continue
                elif self.overwrite:
                    self.logger.debug('Overriding {}'.format(file))
                    write_file()
                else:
                    while True:
                        confirm = input('File already exists {}. Overwrite? Y/Enter = yes, N = no\n'.format(file))
                        if confirm.lower() == 'y' or not confirm:
                            self.logger.debug('Overriding {}'.format(file))
                            write_file()
                            break
            else:
                self.logger.debug('Writing new {}'.format(file))
                write_file()

    def transform(self, item) -> dict:
        if not getattr(item, self.container_name, None):
            self.logger.debug('{} of type {} has no attribute "{}"'.format(item.name, type(item).__name__,
                                                                           self.container_name))
            return {'name': item.name, 'imports': []}
        Params = namedtuple('Params', 'key value')

        imports = {}
        params = []
        methods = []

        for param in getattr(item, self.container_name).values():
            if isinstance(param, FunctionParam) and item.message_type.name == 'response' \
                    and param.name in ('success', 'resultCode', 'info'):
                self.logger.debug('{} of type {}/{} - skip parameter "{}"'.format(item.name, type(item).__name__,
                                                                                  item.message_type.name, param.name))
                continue
            (n, d) = self.extract_name_description(param)
            if n:
                if n in self.enum_names:
                    imports.update({n: '{}/{}.js'.format(self.enums_dir, n)})
                elif n in self.struct_names:
                    imports.update({n: '{}/{}.js'.format(self.structs_dir, n)})
            key = self.underscore(param.name)
            params.append(Params(key=key, value=param.name))
            t = self.extract_type(param)
            l = re.sub(r'.+([A-Z][a-z].+|[A-Z]{2,})$', r'\1', param.name).lower()
            d = textwrap.wrap(d, 102 - len(t) - len(l))
            methods.append(self.methods(key=key, foreign=n, description=d, type=t, last=l,
                                        upper=''.join([param.name[:1].upper(), param.name[1:]])))
        tmp = {'name': item.name,
               'imports': [self.imports(what=k, wherefrom=v) for k, v in imports.items()],
               'params': params,
               'methods': methods}
        if getattr(item, 'description', None):
            tmp.update({'description': InterfaceProducerCommon.extract_description(item.description)})
        return tmp

    @staticmethod
    def ending_cutter(n: str):
        if n.endswith('ID') and not re.match(r'[A-Z]{3,}', n):
            return n[:-2]
        else:
            return n

    @staticmethod
    def extract_description(d):
        return re.sub(r'(\s{2,}|\n|\[@TODO.+)', ' ', ''.join(d)).strip() if d else ''

    @staticmethod
    def extract_name_description(param):
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
    def extract_type(param) -> str:
        def evaluate(t1):
            if isinstance(t1, Struct) or isinstance(t1, Enum):
                return t1.name
            elif isinstance(t1, Integer) or isinstance(t1, Double):
                return 'Number'
            else:
                return type(t1).__name__

        if isinstance(param.param_type, Array):
            t = 'Array<{}>'.format(evaluate(param.param_type.element_type))
        else:
            t = evaluate(param.param_type)
        return t

    def extract_imports(self, extend) -> imports:
        tmp = re.findall(r'.+/(.+).js', extend)
        if tmp:
            return self.imports(what=tmp.pop(), wherefrom=extend)
        else:
            self.logger.error('can not extract {}'.format(extend))