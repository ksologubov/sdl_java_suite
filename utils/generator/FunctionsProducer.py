import logging

from InterfaceProducerCommon import InterfaceProducerCommon
from parsers.Model import Function


class FunctionsProducer(InterfaceProducerCommon):
    def __init__(self, paths, enum_names, struct_names, mapping=None):
        super(FunctionsProducer, self).__init__(
            container_name='params',
            enums_package=paths.ENUMS_PACKAGE,
            structs_package=paths.STRUCTS_PACKAGE,
            enum_names=enum_names,
            struct_names=struct_names,
            package_name=paths.FUNCTIONS_PACKAGE,
            mapping=mapping['functions'] if mapping and 'functions' in mapping else {})
        self.logger = logging.getLogger('Generator.FunctionsProducer')
        self.request_class = paths.REQUEST_CLASS
        self.response_class = paths.RESPONSE_CLASS
        self.notification_class = paths.NOTIFICATION_CLASS

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
