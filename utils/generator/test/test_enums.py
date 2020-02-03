import unittest
from collections import namedtuple

from model.enum import Enum
from model.enum_element import EnumElement
from transformers.enums_producer import EnumsProducer


class TestEnumsProducer(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        Paths = namedtuple('Prop', 'enums_package')
        paths = Paths(enums_package='com.smartdevicelink.proxy.rpc.enums')
        self.producer = EnumsProducer(paths, self.mapping)
        self.params = namedtuple('params', 'origin name internal description since value deprecated')

    def comparison(self, expected, actual):
        if 'valueForString' in actual:
            content = self.producer.get_file_content(self.mapping['enums'][actual['class_name']]['valueForString'])
            self.assertSequenceEqual(content, actual['valueForString'])
        expected_params = dict(zip((k.name for k in expected['params']), expected['params']))
        for param in actual['params']:
            for field in param._fields:
                self.assertEqual(getattr(expected_params[param.name], field), getattr(param, field, None))

        expected_filtred = dict(filter(lambda e: e != 'params', expected.items()))
        actual_filtred = dict(filter(lambda e: e not in ('params', 'valueForString'), expected.items()))

        self.assertEqual(expected_filtred, actual_filtred)

    @property
    def mapping(self):
        return {'enums': {
            'TestDeprecated': {
                'kind': 'custom'
            },
            'DisplayType': {
                'kind': 'custom',
                'valueForString': 'templates/scripts/DisplayType_valueForString.groovy',
                '-imports': [
                    'java.util.EnumSet'''
                ]
            },
            'SpeechCapabilities': {
                'kind': 'simple'
            },
            "VrCapabilities": {
                "valueForString": "templates/scripts/VrCapabilities_valueForString.groovy",
                "kind": "simple",
                "params": {
                    "Text": {
                        "deprecated": "any",
                        "since": "1.0"
                    }
                }
            },
            'MessageType': {
                'package_name': 'com.smartdevicelink.protocol.enums',
                'kind': 'simple',
                '-params': [
                    'notification',
                    'request',
                    'response'
                ],
                'params': {
                    'UNDEFINED': {},
                    'BULK': {},
                    'RPC': {}
                }
            }
        }}

    def test_deprecated(self):
        item = Enum(name='TestDeprecated', deprecated=True, elements={
            'PRIMARY_WIDGET': EnumElement(name='PRIMARY_WIDGET', internal_name='PRIMARY_WIDGET', value=1,
                                          deprecated=True)
        })
        expected = {
            'kind': 'custom',
            'return_type': 'int',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'TestDeprecated',
            'imports': {'java.util.EnumSet'},
            'params': (
                self.params(name='PRIMARY_WIDGET', origin='PRIMARY_WIDGET', deprecated=True,
                            internal=1, description=None, since=None, value=1),),
            'since': None,
            'deprecated': True
        }
        actual = self.producer.transform(item)

        self.comparison(expected, actual)

    def test_FunctionID(self):
        item = Enum(name='FunctionID', elements={
            'RESERVED': EnumElement(name='RESERVED', hex_value=0),
            'RegisterAppInterfaceID': EnumElement(name='RegisterAppInterfaceID', hex_value=1),
            'PerformAudioPassThruID': EnumElement(name='PerformAudioPassThruID', hex_value=10)
        }, description=[
            'Enumeration linking function names with function IDs in SmartDeviceLink protocol. Assumes enumeration '
            'starts at value 0.'])
        expected = {
            'kind': 'simple',
            'return_type': 'int',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'FunctionID',
            'description': [
                'Enumeration linking function names with function IDs in SmartDeviceLink protocol. Assumes '
                'enumeration starts at',
                'value 0.'],
            'params': (
                self.params(name='RESERVED', origin='RESERVED', internal=None, description=None, since=None,
                            value=None, deprecated=None),
                self.params(name='RegisterAppInterfaceID', origin='RegisterAppInterfaceID', internal=None,
                            description=None, since=None, value=None, deprecated=None),
                self.params(name='PerformAudioPassThruID', origin='PerformAudioPassThruID', internal=None,
                            description=None, since=None, value=None, deprecated=None)),
            'since': None,
            'deprecated': None
        }
        actual = self.producer.transform(item)

        self.comparison(expected, actual)

    def test_Language(self):
        item = Enum(name='Language', elements={
            'EN-US': EnumElement(name='EN-US', internal_name='EN-US')
        })
        expected = {
            'kind': 'custom',
            'return_type': 'String',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'Language',
            'imports': {'java.util.EnumSet'},
            'params': (
                self.params(name='EN-US', origin='EN-US', internal='"EN-US"', description=None, since=None,
                            value=None, deprecated=None),),
            'since': None,
            'deprecated': None
        }
        actual = self.producer.transform(item)

        self.comparison(expected, actual)

    def test_PredefinedWindows(self):
        item = Enum(name='PredefinedWindows', elements={
            'DEFAULT_WINDOW': EnumElement(name='DEFAULT_WINDOW', value=0),
            'PRIMARY_WIDGET': EnumElement(name='PRIMARY_WIDGET', value=1)
        })
        expected = {
            'kind': 'complex',
            'return_type': 'int',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'PredefinedWindows',
            'imports': {'java.util.HashMap', 'java.util.Map.Entry', 'java.util.EnumSet', 'java.util.Iterator'},
            'params': (self.params(name='DEFAULT_WINDOW', origin='DEFAULT_WINDOW',
                                   internal='"DEFAULT_WINDOW"', description=None, since=None, value=0,
                                   deprecated=None),
                       self.params(name='PRIMARY_WIDGET', origin='PRIMARY_WIDGET',
                                   internal='"PRIMARY_WIDGET"', description=None, since=None, value=1,
                                   deprecated=None)),
            'since': None,
            'deprecated': None
        }
        actual = self.producer.transform(item)

        self.comparison(expected, actual)

    def test_SamplingRate(self):
        item = Enum(name='SamplingRate', elements={
            '8KHZ': EnumElement(name='8KHZ', internal_name='SamplingRate_8KHZ')
        })
        expected = {
            'kind': 'custom',
            'return_type': 'String',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'SamplingRate',
            'imports': {'java.util.EnumSet'},
            'params': (
                self.params(name='_8KHZ', origin='8KHZ', internal='"8KHZ"', description=None, since=None,
                            value=None,
                            deprecated=None),),
            'since': None,
            'deprecated': None
        }
        actual = self.producer.transform(item)

        self.comparison(expected, actual)

    def test_Result(self):
        item = Enum(name='Result', elements={
            'SUCCESS': EnumElement(name='SUCCESS', description=['The request succeeded']),
            'VEHICLE_DATA_NOT_AVAILABLE': EnumElement(name='VEHICLE_DATA_NOT_AVAILABLE', since='2.0.0')
        })
        expected = {
            'kind': 'simple',
            'return_type': 'String',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'Result',
            'params': (
                self.params(name='SUCCESS', origin='SUCCESS', internal=None, description=['The request succeeded'],
                            since=None, value=None, deprecated=None),
                self.params(name='VEHICLE_DATA_NOT_AVAILABLE', origin='VEHICLE_DATA_NOT_AVAILABLE',
                            internal=None, description=None, since='2.0.0', value=None, deprecated=None)),
            'since': None,
            'deprecated': None
        }
        actual = self.producer.transform(item)

        self.comparison(expected, actual)

    def test_DisplayType(self):
        item = Enum(name='DisplayType', deprecated=True, since='5.0.0', elements={
            'CID': EnumElement(name='CID', since='3.0.0')
        })
        expected = {
            'kind': 'custom',
            'return_type': 'String',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'DisplayType',
            'imports': {'java.util.EnumSet'},
            'params': (
                self.params(name='CID', origin='CID', internal='"CID"', description=None,
                            since='3.0.0', value=None, deprecated=None),),
            'since': '5.0.0',
            'deprecated': True
        }
        actual = self.producer.transform(item)

        self.comparison(expected, actual)

    def test_SpeechCapabilities(self):
        item = Enum(name='SpeechCapabilities', since='1.0.0', elements={
            'TEXT': EnumElement(name='TEXT', internal_name='SC_TEXT')
        })
        expected = {
            'kind': 'simple',
            'return_type': 'String',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'SpeechCapabilities',
            'imports': set(),
            'params': (
                self.params(name='TEXT', origin='TEXT', description=None,
                            since=None, value=None, deprecated=None, internal=None),),
            'since': '1.0.0',
            'deprecated': None
        }
        actual = self.producer.transform(item)

        self.comparison(expected, actual)

    def test_VrCapabilities(self):
        item = Enum(name='VrCapabilities', elements={
            'TEXT': EnumElement(name='TEXT', internal_name='VR_TEXT')
        })
        expected = {
            'kind': 'simple',
            'return_type': 'String',
            'package_name': 'com.smartdevicelink.proxy.rpc.enums',
            'class_name': 'VrCapabilities',
            'imports': set(),
            'params': (
                self.params(name='TEXT', origin='TEXT', description=None,
                            since=None, value=None, deprecated=None, internal=None),
                self.params(name='Text', origin='TEXT', description=None,
                            since='1.0', value=None, deprecated='any', internal=None)),
            'since': None,
            'deprecated': None
        }
        actual = self.producer.transform(item)

        self.comparison(expected, actual)

    def test_VrCapabilities(self):
        item = Enum(name='MessageType', elements={
            'NOTIFICATION': EnumElement(name='notification', internal_name='NOTIFICATION', value=2)
        })
        expected = {
            'kind': 'simple',
            'return_type': 'int',
            'package_name': 'com.smartdevicelink.protocol.enums',
            'class_name': 'MessageType',
            'imports': set(),
            'params': (
                self.params(name='notification', origin='notification', description=None,
                            since=None, value=None, deprecated=None, internal=None),
                self.params(name='UNDEFINED', origin=None, description=None,
                            since=None, value=None, deprecated=None, internal=None),
                self.params(name='RPC', origin=None, description=None,
                            since=None, value=None, deprecated=None, internal=None),
                self.params(name='BULK', origin=None, description=None,
                            since=None, value=None, deprecated=None, internal=None)),
            'since': None,
            'deprecated': None
        }
        actual = self.producer.transform(item)

        self.comparison(expected, actual)
