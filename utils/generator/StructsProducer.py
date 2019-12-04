import logging

from InterfaceProducerCommon import InterfaceProducerCommon
from parsers.Model import Struct


class StructsProducer(InterfaceProducerCommon):
    def __init__(self, paths, enum_names, struct_names, mapping=None):
        super(StructsProducer, self).__init__(
            container_name='members',
            enums_package=paths.ENUMS_PACKAGE,
            # structs_package=paths.STRUCTS_PACKAGE,
            enum_names=enum_names,
            struct_names=struct_names,
            package_name=paths.STRUCTS_PACKAGE,
            mapping=mapping['structs'] if mapping and 'structs' in mapping else {})
        self.logger = logging.getLogger('Generator.StructsProducer')
        self.struct_class = paths.STRUCT_CLASS

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
