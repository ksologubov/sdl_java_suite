import logging

from InterfaceProducerCommon import InterfaceProducerCommon
from rpc_spec.InterfaceParser.parsers.Model import Interface, Struct


class StructsProducer(InterfaceProducerCommon):
    def __init__(self, interface: Interface, prop):
        super(StructsProducer, self).__init__(prop, tuple(interface.enums.keys()), tuple(interface.structs.keys()))
        self.logger = logging.getLogger('Generator.StructsProducer')
        self.structs = list(interface.structs.values())
        self.struct_class = prop.PATH_TO_STRUCT_CLASS

    @property
    def directory(self) -> str:
        return self.structs_dir

    @property
    def items(self) -> list:
        return self.structs

    @property
    def container_name(self) -> str:
        return 'members'

    def transform(self, item: Struct) -> dict:
        tmp = super(StructsProducer, self).transform(item)
        what_where = self.extract_imports(self.struct_class)
        tmp.update({'extend': what_where.what})
        tmp['imports'].append(what_where)
        return tmp