import logging

from generator.InterfaceProducerCommon import InterfaceProducerCommon
from InterfaceParser.parsers.Model import Function


class FunctionsProducer(InterfaceProducerCommon):
    def __init__(self, paths, enum_names, struct_names, mapping=None):
        super(FunctionsProducer, self).__init__(
            container_name='params',
            directory=paths.FUNCTIONS_DIR_NAME,
            enums_dir_name=paths.ENUMS_DIR_NAME,
            structs_dir_name=paths.STRUCTS_DIR_NAME,
            enum_names=enum_names,
            struct_names=struct_names,
            mapping=mapping['functions'] if mapping and 'functions' in mapping else {})
        self.logger = logging.getLogger('Generator.FunctionsProducer')
        self.request_class = paths.PATH_TO_REQUEST_CLASS
        self.response_class = paths.PATH_TO_RESPONSE_CLASS
        self.notification_class = paths.PATH_TO_NOTIFICATION_CLASS

    def transform(self, item: Function) -> dict:
        """
        Override
        :param item: particular element from initial Model
        :return: dictionary to be applied to jinja2 template
        """
        tmp = super(FunctionsProducer, self).transform(item)
        tmp.update({'func': self.ending_cutter(tmp['name'])})
        name = None
        if item.message_type.name == 'request':
            name = self.request_class
        elif item.message_type.name == 'response':
            name = self.response_class
            tmp['name'] = tmp['name'] + 'Response'
        elif item.message_type.name == 'notification':
            name = self.notification_class
        if name:
            what_where = self.extract_imports(name)
            tmp.update({'extend': what_where.what})
            tmp['imports'].append(what_where)
        tmp['imports'].append(self.imports(what='FunctionID', wherefrom='{}/FunctionID.js'.format(self.enums_dir)))
        return tmp