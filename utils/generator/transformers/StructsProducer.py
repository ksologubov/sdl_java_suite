import logging

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
        tmp = super(StructsProducer, self).transform(item)
        what_where = self.extract_imports(self.struct_class)
        tmp.update({'extend': what_where.what})
        tmp['imports'].append(what_where)
        return tmp
