import logging

from InterfaceProducerCommon import InterfaceProducerCommon
from InterfaceParser.parsers.Model import Struct


class StructsProducer(InterfaceProducerCommon):
    def __init__(self, paths, enum_names, struct_names, mapping=None):
        super(StructsProducer, self).__init__(
            container_name='members',
            directory=paths.STRUCTS_DIR_NAME,
            enums_dir_name=paths.ENUMS_DIR_NAME,
            structs_dir_name=paths.STRUCTS_DIR_NAME,
            enum_names=enum_names,
            struct_names=struct_names,
            mapping=mapping['structs'] if mapping and 'structs' in mapping else {})
        self.logger = logging.getLogger('Generator.StructsProducer')
        self.struct_class = paths.PATH_TO_STRUCT_CLASS

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