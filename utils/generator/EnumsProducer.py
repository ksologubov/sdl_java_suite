import logging
import textwrap
from collections import namedtuple

from InterfaceProducerCommon import InterfaceProducerCommon
from rpc_spec.InterfaceParser.parsers.Model import Interface, Enum


class EnumsProducer(InterfaceProducerCommon):
    def __init__(self, interface: Interface, prop):
        super(EnumsProducer, self).__init__(prop)
        self.logger = logging.getLogger('Generator.EnumsProducer')
        self.enums = list(interface.enums.values())
        self.enum_class = prop.PATH_TO_ENUM_CLASS

    @property
    def items(self) -> list:
        return self.enums

    @property
    def directory(self) -> str:
        return self.enums_dir

    @property
    def container_name(self) -> str:
        return 'elements'

    @property
    def methods(self):
        return namedtuple('Methods', 'name description type')

    def transform(self, item: Enum) -> dict:
        methods = []
        for param in getattr(item, self.container_name).values():
            (n, d) = self.extract_name_description(param)
            if item.name == 'AudioType':
                print('AudioType')
            t = 'Number' if getattr(param, 'hexvalue', None) else 'String'
            d = textwrap.wrap(d, 118 - len(t))
            n = self.ending_cutter(n)
            methods.append(self.methods(name=n, description=d, type=t))
        what_where = self.extract_imports(self.enum_class)
        tmp = {'name': item.name,
               'imports': [what_where],
               'extend': what_where.what,
               'params': self.form_map(item),
               'methods': methods}
        if getattr(item, 'description', None):
            tmp.update({'description': self.extract_description(item.description)})
        return tmp

    def form_map(self, item: Enum) -> str:
        tmp = []
        for param in getattr(item, self.container_name).values():
            if getattr(param, 'hexvalue', None):
                if len(param.hexvalue) > 1:
                    value = '0x{}'.format(param.hexvalue)
                else:
                    value = '0x0{}'.format(param.hexvalue)
            else:
                value = "'{}'".format(param.name)
            tmp.append("'{}': {},\n".format(self.ending_cutter(param.primary_name), value))
        return ''.join(tmp)
