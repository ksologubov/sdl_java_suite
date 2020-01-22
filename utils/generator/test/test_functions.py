from collections import namedtuple
import unittest

from transformers.functions_producer import FunctionsProducer
from model.array import Array
from model.boolean import Boolean
from model.enum import Enum
from model.enum_element import EnumElement
from model.function import Function
from model.integer import Integer
from model.param import Param
from model.string import String
from model.struct import Struct


class TestFunctionsProducer(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        Paths = namedtuple('Prop', 'enums_package structs_package functions_package request_class response_class notification_class')
        paths = Paths(enums_package='com.smartdevicelink.proxy.rpc.enums',
                     structs_package='com.smartdevicelink.proxy.rpc',
                     functions_package='com.smartdevicelink.proxy.rpc',
                     request_class='com.smartdevicelink.proxy.RPCRequest',
                     response_class='com.smartdevicelink.proxy.RPCResponse',
                     notification_class='com.smartdevicelink.proxy.RPCNotification')

        mapping = ()
        enum_names = ('FileType', 'Language')
        struct_names = ('SyncMsgVersion', 'TemplateColorScheme', 'TTSChunk', 'Choice')
        self.producer = FunctionsProducer(paths, enum_names, struct_names, mapping)

    def test_PutFileRequest(self):
        item = Function(name='PutFile', function_id=None, description=['\n            Used to'],
                        message_type=EnumElement(name='request'), params=
                        {
                            'fileType': Param(name='fileType', param_type=
                            Enum(name='FileType', description=['Enumeration listing'], elements={
                                'AUDIO_MP3': EnumElement(name='AUDIO_MP3')
                            }), description=['Selected file type.'])
                        })
        result = self.producer.transform(item)
        expected = {'kind': 'request', 'package_name': 'com.smartdevicelink.proxy.rpc',
                    'imports': ['android.support.annotation.NonNull', '',
                                'com.smartdevicelink.protocol.enums.FunctionID', 'com.smartdevicelink.proxy.RPCRequest',
                                'com.smartdevicelink.proxy.rpc.enums.FileType', '', 'java.util.Hashtable'],
                    'function_id': 'PUT_FILE', 'class_name': 'PutFile', 'extends_class': 'RPCRequest', 'since': None,
                    'deprecated': None, 'description': ['Used to'], 'params': (
                    self.producer.params(deprecated=None, description=['Selected file type.'], key='KEY_FILE_TYPE',
                                         last='fileType', mandatory=True, origin='fileType',
                                         return_type='FileType', since=None, title='FileType'),)}
        self.assertEqual(expected, result)

    def test_OnEncodedSyncPDataNotification(self):
        item = Function(name='OnEncodedSyncPData', function_id=None, description=['\n           Callback including \n'],
                        message_type=EnumElement(name='notification'), params=
                        {
                            'URL': Param(name='URL', param_type=String(), description=['\n                If '])
                        })
        result = self.producer.transform(item)
        expected = {'kind': 'notification', 'package_name': 'com.smartdevicelink.proxy.rpc',
                    'imports': ['android.support.annotation.NonNull', '',
                                'com.smartdevicelink.protocol.enums.FunctionID',
                                'com.smartdevicelink.proxy.RPCNotification', '', 'java.util.Hashtable'],
                    'function_id': 'ON_ENCODED_SYNC_PDATA', 'class_name': 'OnEncodedSyncPData',
                    'extends_class': 'RPCNotification', 'since': None, 'deprecated': None,
                    'description': ['Callback including'], 'params': (
                    self.producer.params(deprecated=None, description=['If'], key='KEY_URL', last='URL',
                                         mandatory=True, origin='URL', return_type='String', since=None, title='URL'),)}
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()

