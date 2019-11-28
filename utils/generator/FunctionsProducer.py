import logging

from InterfaceProducerCommon import InterfaceProducerCommon
from rpc_spec.InterfaceParser.parsers.Model import Interface, Function


class FunctionsProducer(InterfaceProducerCommon):
    def __init__(self, interface: Interface, prop):
        super(FunctionsProducer, self).__init__(prop, tuple(interface.enums.keys()), tuple(interface.structs.keys()))
        self.logger = logging.getLogger('Generator.FunctionsProducer')
        self.functions = list(interface.functions.values())
        self.functions_dir = prop.FUNCTIONS_DIR_NAME
        self.request_class = prop.PATH_TO_REQUEST_CLASS
        self.response_class = prop.PATH_TO_RESPONSE_CLASS
        self.notification_class = prop.PATH_TO_NOTIFICATION_CLASS

    @property
    def directory(self) -> str:
        return self.functions_dir

    @property
    def items(self) -> list:
        return self.functions

    @property
    def container_name(self) -> str:
        return 'params'

    def transform(self, item: Function) -> dict:
        tmp = super(FunctionsProducer, self).transform(item)
        tmp.update({'func': self.ending_cutter(tmp['name'])})
        if item.message_type.name == 'request':
            name = self.request_class
        elif item.message_type.name == 'response':
            name = self.response_class
            tmp['name'] = tmp['name'] + 'Response'
        elif item.message_type.name == 'notification':
            name = self.notification_class
        else:
            name = None
        if name:
            what_where = self.extract_imports(name)
            tmp.update({'extend': what_where.what})
            tmp['imports'].append(what_where)
        tmp['imports'].append(self.imports(what='FunctionID', wherefrom='{}/FunctionID.js'.format(self.enums_dir)))
        return tmp