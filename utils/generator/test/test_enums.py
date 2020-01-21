from collections import namedtuple
import unittest

from transformers.enums_producer import EnumsProducer
from model.enum import Enum
from model.enum_element import EnumElement


class TestEnumsProducer(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        Paths = namedtuple('Prop', 'enums_package')
        paths = Paths(enums_package='com.smartdevicelink.proxy.rpc.enums')
        self.producer = EnumsProducer(paths)

    def test_FunctionID(self):
        item = Enum(name='FunctionID', elements={
            'RESERVED': EnumElement(name='RESERVED', hexvalue=0),
            'RegisterAppInterfaceID': EnumElement(name='RegisterAppInterfaceID', hexvalue=1),
            'PerformAudioPassThruID': EnumElement(name='PerformAudioPassThruID', hexvalue=10)
        })
        result = self.producer.transform(item)
        expected = {
            'kind': 'simple',
            'return_type': 'int',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'FunctionID',
            'params': (self.producer.params(name='RESERVED', origin='RESERVED'),
                       self.producer.params(name='RegisterAppInterfaceID', origin='RegisterAppInterfaceID'),
                       self.producer.params(name='PerformAudioPassThruID', origin='PerformAudioPassThruID')),
            'since': None,
            'deprecated': None
        }
        self.assertEqual(expected, result)

    def test_Result(self):
        item = Enum(name='Result', elements={
            'SUCCESS': EnumElement(name='SUCCESS')
        })
        result = self.producer.transform(item)
        expected = {
            'kind': 'simple',
            'return_type': 'String',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'Result',
            'params': (self.producer.params(name='SUCCESS', origin='SUCCESS'),),
            'since': None,
            'deprecated': None
        }
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
    # unittest.defaultTestLoader.loadTestsFromName(__name__).debug()  # enable debugging
