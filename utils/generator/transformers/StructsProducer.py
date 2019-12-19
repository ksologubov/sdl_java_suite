import logging
import textwrap
from collections import namedtuple

from model.Struct import Struct
from transformers.InterfaceProducerCommon import InterfaceProducerCommon


class StructsProducer(InterfaceProducerCommon):
    def __init__(self, paths, enum_names, struct_names, mapping=None):
        super(StructsProducer, self).__init__(
            container_name='members',
            enums_package=paths.enums_package,
            structs_package=paths.structs_package,
            enum_names=enum_names,
            struct_names=struct_names,
            package_name=paths.structs_package,
            mapping=mapping['structs'] if mapping and 'structs' in mapping else {})
        self.logger = logging.getLogger('StructsProducer')
        self.struct_class = paths.struct_class

    def transform(self, item: Struct) -> dict:
        """
        Override
        :param item: particular element from initial Model
        :return: dictionary to be applied to jinja2 template
        """
        class_name = item.name[:1].upper() + item.name[1:]

        imports = {'java.util.Hashtable'}
        extends_class = self.struct_class

        imports.add(extends_class)
        extends_class = extends_class.rpartition('.')[-1]

        params = {}

        for param in getattr(item, self.container_name).values():
            i, p = self.extract_param(param)
            imports.update(i)
            params.update({param.name: p})

        for n1, v1 in params.items():
            for n2, v2, in params.items():
                if n1 != n2 and v1.last == v2.last:
                    d = v2._replace(last=v2.origin)
                    params.update({n2: d})

        render = {'package_name': self.package_name,
                  'imports': imports,
                  'class_name': class_name,
                  'extends_class': extends_class,
                  'since': item.since,
                  'deprecated': item.deprecated}

        description = self.extract_description(item.description)
        if description:
            render.update({'description': description})
        if imports:
            render.update({'imports': imports})
        if params:
            render.update({'params': params})

        self.custom_mapping(render)
        if 'imports' in render:
            render.update({'imports': self.sort_imports(render['imports'])})
        if params:
            render.update({'params': tuple(render['params'].values())})
        if 'description' in render and isinstance(render['description'], str):
            render['description'] = textwrap.wrap(render['description'], 113)

        return render

    def sort_imports(self, imports: set):
        sorted_imports = []
        if 'android.support.annotation.NonNull' in imports:
            sorted_imports.append('android.support.annotation.NonNull')
            imports.remove('android.support.annotation.NonNull')
            # sorted_imports.append('')
        tmp = []
        for i in imports:
            if i.rpartition('.')[0] != self.package_name and not i.startswith('java'):
                tmp.append(i)
        if tmp:
            tmp.sort()
            sorted_imports.extend(tmp)
        if 'java.util.Hashtable' in imports or 'java.util.List' in imports:
            sorted_imports.append('')
        for i in ('java.util.Hashtable', 'java.util.List', 'java.util.ArrayList'):
            if i in imports:
                sorted_imports.append(i)
        return sorted_imports

    def extract_param(self, param: Struct):
        imports = set()
        p = {'title': param.name[:1].upper() + param.name[1:]}
        p.update({'key': 'KEY_' + self.key(param.name)})
        p.update({'mandatory': param.is_mandatory})
        p.update({'last': param.name})
        p.update({'since': param.since})
        p.update({'deprecated': param.deprecated})
        p.update({'origin': param.name})
        d = self.extract_description(param.description)
        if d:
            p.update({'description': textwrap.wrap(d, 113)})
        t = self.extract_type(param)
        tr = t
        if t.startswith('List'):
            imports.add('java.util.List')
            p.update({'SuppressWarnings': 'unchecked'})
            tr = t.replace('List<', '').rstrip('>')
        p.update({'return_type': t})

        if tr in self.enum_names:
            imports.add('{}.{}'.format(self.enums_package, tr))
        if tr in self.struct_names:
            imports.add('{}.{}'.format(self.structs_package, tr))
        if param.is_mandatory:
            imports.add('android.support.annotation.NonNull')

        Params = namedtuple('Params', sorted(p))
        return imports, Params(**p)

    def custom_mapping(self, render):
        if not render['class_name'] in self.mapping:
            return
        super(StructsProducer, self).custom_mapping(render)
        #     custom = self.mapping[render['class_name']]
