import logging
import textwrap
from collections import namedtuple

from generator.InterfaceProducerCommon import InterfaceProducerCommon
from InterfaceParser.parsers.Model import EnumElement, Enum


class EnumsProducer(InterfaceProducerCommon):
    def __init__(self, paths, mapping=None):
        super(EnumsProducer, self).__init__(
            container_name='elements',
            directory=paths.ENUMS_DIR_NAME,
            enums_dir_name=paths.ENUMS_DIR_NAME,
            structs_dir_name=paths.STRUCTS_DIR_NAME,
            mapping=mapping['enums'] if mapping and 'enums' in mapping else {})
        self.logger = logging.getLogger('Generator.EnumsProducer')
        self.enum_class = paths.PATH_TO_ENUM_CLASS

    @property
    def methods(self):
        """
        Override
        :return: namedtuple methods(origin='', method_title='', description='', type='')
        """
        return namedtuple('Methods', 'origin method_title description type')

    def transform(self, item: Enum) -> dict:
        """
        Override
        :param item: particular element from initial Model
        :return: dictionary to be applied to jinja2 template
        """
        tmp = super(EnumsProducer, self).transform(item)
        what_where = self.extract_imports(self.enum_class)
        tmp.update({'extend': what_where.what})
        tmp['imports'].append(what_where)
        return tmp

    def common_flow(self, param: EnumElement, item_type=None):
        """
        Override
        Main transformation flow, for Enum
        :param param: sub-element (EnumElement) of element from initial Model
        :param item_type: not used
        :return: tuple with 3 element, which going to be applied to jinja2 template
        """
        (n, d) = self.extract_name_description(param)
        t = self.extract_type(param)
        d = textwrap.wrap(d, 118 - len(t))
        n = self.ending_cutter(n)

        methods = self.methods(origin=param.name, method_title=n, description=d, type=t)
        params = self.extract_param(param)

        imports = None
        return imports, methods, params

    def extract_param(self, param: EnumElement) -> namedtuple:
        """
        Evaluate and extract params
        :param param: sub-element (EnumElement) of element from initial Model
        :return: self.params
        """
        if hasattr(param, 'hexvalue') and param.hexvalue is not None:
            if len(str(param.hexvalue)) > 1:
                value = '0x{}'.format(param.hexvalue)
            else:
                value = '0x0{}'.format(param.hexvalue)
        elif hasattr(param, 'value') and param.value is not None:
            value = param.value
        else:
            value = "'{}'".format(param.name)
        return self.params(key=self.ending_cutter(param.primary_name), value=value)

    @staticmethod
    def extract_type(param: EnumElement) -> str:
        """
        Override
        Evaluate and extract type
        :param param: sub-element (EnumElement) of element from initial Model
        :return: string with sub-element type
        """
        if hasattr(param, 'hexvalue') and param.hexvalue is not None or \
                        hasattr(param, 'value') and param.value is not None:
            return 'Number'
        else:
            return 'String'