import logging
import textwrap
from collections import namedtuple

from InterfaceProducerCommon import InterfaceProducerCommon
from model.Enum import Enum
from model.EnumElement import EnumElement


class EnumsProducer(InterfaceProducerCommon):
    def __init__(self, enums_package, mapping=None):
        super(EnumsProducer, self).__init__(
            container_name='elements',
            enums_package=None,
            structs_package=None,
            package_name=enums_package,
            mapping=mapping['enums'] if mapping and 'enums' in mapping else {})
        self.logger = logging.getLogger('Generator.EnumsProducer')

    def transform(self, item: Enum) -> dict:
        """
        Override
        :param item: particular element from initial Model
        :return: dictionary to be applied to jinja2 template
        """
        imports = set()
        params = {}
        kind = 'simple'
        return_type = 'String'

        for param in getattr(item, self.container_name).values():
            (t, p) = self.extract_param(param, item.name)
            if t == 'complex':
                kind = t
            elif t == 'custom' and kind != 'complex':
                kind = t
            return_type = self.extract_type(param)

            params.update({p.name: p})
            imports.update(self.extract_imports(param))

        render = {'kind': kind,
                  'return_type': return_type,
                  'package_name': self.package_name,
                  'class_name': item.name[:1].upper() + item.name[1:],
                  'params': params,
                  'since': item.since}

        description = self.extract_description(item.description)
        if description:
            render.update({'description': description})
        if imports:
            render.update({'imports': imports})

        self.custom_mapping(render)
        render.update({'params': tuple(render['params'].values())})
        if 'description' in render and isinstance(render['description'], str):
            render['description'] = textwrap.wrap(render['description'], 113)

        return render

    def extract_param(self, param: EnumElement, item_name):
        d = {'origin': param.name}
        kind = 'simple'
        if getattr(param, 'value', None) is not None:
            n = self.ending_cutter(param.name)
            d.update({'name': self.key(n)})
            d.update({'value': param.value})
            d.update({'internal': '"{}"'.format(n)})
            kind = 'complex'
        elif getattr(param, 'internal_name', None) is not None:
            if param.internal_name.startswith(item_name):
                n = param.internal_name[len(item_name):]
            else:
                n = param.internal_name
            d.update({'name': n})
            d.update({'internal': '"{}"'.format(param.name)})
            kind = 'custom'
        else:
            d.update({'name': param.name})

        if getattr(param, 'since', None):
            d.update({'since': param.since})
        if getattr(param, 'description', None):
            d.update({'description': textwrap.wrap(self.extract_description(param.description), 113)})
        Params = namedtuple('Params', sorted(d))
        return kind, Params(**d)

    @staticmethod
    def extract_imports(param):
        imports = []
        if getattr(param, 'value', None):
            imports.extend(['java.util.EnumSet', 'java.util.HashMap', 'java.util.Iterator', 'java.util.Map.Entry'])
        elif getattr(param, 'internal_name', None):
            imports.append('java.util.EnumSet')
        return imports

    @staticmethod
    def extract_type(param: EnumElement) -> str:
        """
        Override
        Evaluate and extract type
        :param param: sub-element (EnumElement) of element from initial Model
        :return: string with sub-element type
        """
        if getattr(param, 'hexvalue') is not None or getattr(param, 'value') is not None:
            return 'int'
        else:
            return 'String'

    def custom_mapping(self, render):
        if not render['class_name'] in self.mapping:
            return
        super(EnumsProducer, self).custom_mapping(render)
        custom = self.mapping[render['class_name']]
        if 'kind' in custom:
            if custom['kind'] == 'simple':
                self.logger.warning('for {} changing kind to {}'.format(render['class_name'], custom['kind']))
                params = {}
                for name, value in render['params'].items():
                    d = value._asdict()
                    if 'origin' in d:
                        d['name'] = d['origin']
                    else:
                        d['name'] = name
                    if 'internal' in d:
                        del d['internal']
                    if 'value' in d:
                        del d['value']
                    Params = namedtuple('Params', sorted(d))
                    d = Params(**d)
                    params.update({d.name: d})
                render['kind'] = custom['kind']
                render['params'] = params
                render['imports'].clear()
            if custom['kind'] == 'custom':
                self.logger.warning('for {} changing kind to {}'.format(render['class_name'], custom['kind']))
                params = {}
                for name, value in render['params'].items():
                    d = value._asdict()
                    if 'value' in d:
                        d['internal'] = d['value']
                    elif 'internal' not in d:
                        d['internal'] = '"{}"'.format(d['name'])
                    d['name'] = self.key(d['name'])
                    Params = namedtuple('Params', sorted(d))
                    d = Params(**d)
                    params.update({d.name: d})
                render['kind'] = custom['kind']
                render['params'] = params
                render['imports'] = set()
                if render['return_type'] != 'bool':
                    render['imports'].add('java.util.EnumSet')

        if 'valueForString' in custom:
            script = self.get_file_content(custom['valueForString'])
            if script:
                render['valueForString'] = script
