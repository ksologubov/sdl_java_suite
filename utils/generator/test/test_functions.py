from collections import namedtuple
from unittest import TestCase

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


class TestFunctionsProducer(TestCase):
    def setUp(self):
        self.maxDiff = None
        Prop = namedtuple('Prop',
                          'FUNCTIONS_DIR_NAME ENUMS_DIR_NAME STRUCTS_DIR_NAME PATH_TO_REQUEST_CLASS '
                          'PATH_TO_RESPONSE_CLASS PATH_TO_NOTIFICATION_CLASS')
        paths = Prop(FUNCTIONS_DIR_NAME='../messages',
                     ENUMS_DIR_NAME='../enums',
                     STRUCTS_DIR_NAME='../structs',
                     PATH_TO_REQUEST_CLASS='../RpcRequest.js',
                     PATH_TO_RESPONSE_CLASS='../RpcResponse.js',
                     PATH_TO_NOTIFICATION_CLASS='../RpcNotification.js')

        mapping = {"functions": {
            "RegisterAppInterfaceRequest": {
                "syncMsgVersion": {
                    "imports": {
                        "what": "SdlMsgVersion",
                        "wherefrom": "../structs/SdlMsgVersion.js"
                    },
                    "methods": {
                        "method_title": "SdlMsgVersion",
                        "external": "SdlMsgVersion",
                        "key": "KEY_SDL_MSG_VERSION",
                        "type": "SdlMsgVersion"
                    },
                    "params": {
                        "key": "KEY_SDL_MSG_VERSION"
                    }
                },
                "fullAppID": {
                    "script": "templates/scripts/fullAppID.js"
                },
                "params_additional": {
                    "key": "APP_ID_MAX_LENGTH",
                    "value": 10
                }
            },
            "RegisterAppInterfaceResponse": {
                "script_additional": "templates/scripts/notExist.js"
            },
            "PutFileRequest": {
                "script_additional": "templates/scripts/PutFileRequest.js"
            }}}

        enum_names = ('FileType', 'Language')
        struct_names = ('SyncMsgVersion', 'TemplateColorScheme', 'TTSChunk', 'Choice')
        self.producer = FunctionsProducer(paths, enum_names, struct_names, mapping)

    def test_RegisterAppInterfaceRequest(self):
        item = Function(name='RegisterAppInterface', function_id=None,
                        message_type=EnumElement(name='request'), params=
                        {
                            'syncMsgVersion': Param(name='syncMsgVersion', param_type=
                            Struct(name='SyncMsgVersion', description=['Specifies the'], members={
                                'majorVersion': Param(name='majorVersion', param_type=Integer())
                            }), description=['See SyncMsgVersion']),
                            'fullAppID': Param(name='fullAppID', description=['ID used'], param_type=String()),
                            'dayColorScheme': Param(name='dayColorScheme', param_type=
                            Struct(name='TemplateColorScheme', description=
                            ['\n            A color scheme for all display layout templates.\n        '])),
                            'ttsName': Param(name='ttsName', description=['\n      TTS string for'], param_type=
                            Array(element_type=Struct(name='TTSChunk', description=['A TTS chunk'])))
                        })
        expected = {
            'name': 'RegisterAppInterface',
            'imports': [self.producer.imports(what='SdlMsgVersion', wherefrom='../structs/SdlMsgVersion.js'),
                        self.producer.imports(what='TemplateColorScheme',
                                              wherefrom='../structs/TemplateColorScheme.js'),
                        self.producer.imports(what='TTSChunk', wherefrom='../structs/TTSChunk.js'),
                        self.producer.imports(what='RpcRequest', wherefrom='../RpcRequest.js'),
                        self.producer.imports(what='FunctionID', wherefrom='../enums/FunctionID.js')],
            'methods': [self.producer.methods(origin='syncMsgVersion', key='KEY_SDL_MSG_VERSION',
                                              method_title='SdlMsgVersion', external='SdlMsgVersion',
                                              description=['See SyncMsgVersion'], param_name='version',
                                              type='SdlMsgVersion'),
                        self.producer.methods(origin='dayColorScheme', key='KEY_DAY_COLOR_SCHEME', param_name='scheme',
                                              method_title='DayColorScheme', external='TemplateColorScheme',
                                              description=['A color scheme for all display layout templates.'],
                                              type='TemplateColorScheme'),
                        self.producer.methods(origin='ttsName', key='KEY_TTS_NAME', param_name='name',
                                              method_title='TtsName', external='TTSChunk',
                                              description=['TTS string for'], type='Array<TTSChunk>')],
            'params': [self.producer.params(key='APP_ID_MAX_LENGTH', value=10),
                       self.producer.params(key='KEY_SDL_MSG_VERSION', value="'syncMsgVersion'"),
                       self.producer.params(key='KEY_FULL_APP_ID', value="'fullAppID'"),
                       self.producer.params(key='KEY_DAY_COLOR_SCHEME', value="'dayColorScheme'"),
                       self.producer.params(key='KEY_TTS_NAME', value="'ttsName'")],
            'scripts': [self.producer.get_file_content('templates/scripts/fullAppID.js')],
            'func': 'RegisterAppInterface',
            'extend': 'RpcRequest'
        }
        result = self.producer.transform(item)
        self.assertEqual(expected, result)

    def test_RegisterAppInterfaceResponse(self):
        item = Function(name='RegisterAppInterface', function_id=None, description=['The response '],
                        message_type=EnumElement(name='response'), params=
                        {
                            'success': Param(name='success', param_type=Boolean(), description=[' true if ']),
                            'language': Param(name='language', param_type=
                            Enum(name='Language', elements={
                                'EN-US': EnumElement(name='EN-US', description=['English - US'])
                            }), description=['The currently']),
                            'supportedDiagModes': Param(name='supportedDiagModes', param_type=
                            Array(element_type=Integer()), description=['\n                Specifies the'], )
                        })
        expected = {
            'name': 'RegisterAppInterfaceResponse',
            'imports': [self.producer.imports(what='Language', wherefrom='../enums/Language.js'),
                        self.producer.imports(what='RpcResponse', wherefrom='../RpcResponse.js'),
                        self.producer.imports(what='FunctionID', wherefrom='../enums/FunctionID.js')],
            'methods': [self.producer.methods(origin='language', key='KEY_LANGUAGE',
                                              method_title='Language', external='Language',
                                              description=['The currently'], param_name='language',
                                              type='Language'),
                        self.producer.methods(origin='supportedDiagModes', key='KEY_SUPPORTED_DIAG_MODES',
                                              method_title='SupportedDiagModes', external=None,
                                              description=['Specifies the'], param_name='modes',
                                              type='Array<Number>')],
            'params': [self.producer.params(key='KEY_LANGUAGE', value="'language'"),
                       self.producer.params(key='KEY_SUPPORTED_DIAG_MODES', value="'supportedDiagModes'")],
            'description': 'The response',
            'func': 'RegisterAppInterface',
            'extend': 'RpcResponse'
        }
        result = self.producer.transform(item)
        self.assertEqual(expected, result)

    def test_UnregisterAppInterfaceRequest(self):
        item = Function(name='UnregisterAppInterface', function_id=None,
                        message_type=EnumElement(name='request'), params={})
        expected = {
            'name': 'UnregisterAppInterface',
            'imports': [self.producer.imports(what='RpcRequest', wherefrom='../RpcRequest.js'),
                        self.producer.imports(what='FunctionID', wherefrom='../enums/FunctionID.js')],
            'func': 'UnregisterAppInterface',
            'extend': 'RpcRequest'
        }
        result = self.producer.transform(item)
        self.assertEqual(expected, result)

    def test_PutFileRequest(self):
        item = Function(name='PutFile', function_id=None, description=['\n            Used to'],
                        message_type=EnumElement(name='request'), params=
                        {
                            'fileType': Param(name='fileType', param_type=
                            Enum(name='FileType', description=['Enumeration listing'], elements={
                                'AUDIO_MP3': EnumElement(name='AUDIO_MP3')
                            }), description=['Selected file type.'])
                        })
        expected = {
            'name': 'PutFile',
            'imports': [self.producer.imports(what='FileType', wherefrom='../enums/FileType.js'),
                        self.producer.imports(what='RpcRequest', wherefrom='../RpcRequest.js'),
                        self.producer.imports(what='FunctionID', wherefrom='../enums/FunctionID.js')],
            'methods': [self.producer.methods(origin='fileType', key='KEY_FILE_TYPE',
                                              method_title='FileType', external='FileType',
                                              description=['Selected file type.'], param_name='type',
                                              type='FileType')],
            'params': [self.producer.params(key='KEY_FILE_TYPE', value="'fileType'")],
            'description': 'Used to',
            'scripts': [self.producer.get_file_content('templates/scripts/PutFileRequest.js')],
            'func': 'PutFile',
            'extend': 'RpcRequest'
        }
        result = self.producer.transform(item)
        self.assertEqual(expected, result)

    def test_OnEncodedSyncPDataNotification(self):
        item = Function(name='OnEncodedSyncPData', function_id=None, description=['\n           Callback including \n'],
                        message_type=EnumElement(name='notification'), params=
                        {
                            'URL': Param(name='URL', param_type=String(), description=['\n                If '])
                        })
        expected = {
            'name': 'OnEncodedSyncPData',
            'imports': [self.producer.imports(what='RpcNotification', wherefrom='../RpcNotification.js'),
                        self.producer.imports(what='FunctionID', wherefrom='../enums/FunctionID.js')],
            'methods': [self.producer.methods(origin='URL', key='KEY_URL',
                                              method_title='URL', external=None,
                                              description=['If'], param_name='url',
                                              type='String')],
            'params': [self.producer.params(key='KEY_URL', value="'URL'")],
            'description': 'Callback including',
            'func': 'OnEncodedSyncPData',
            'extend': 'RpcNotification'
        }
        result = self.producer.transform(item)
        self.assertEqual(expected, result)

    def test_CreateInteractionChoiceSetRequest(self):
        item = Function(name='CreateInteractionChoiceSet', function_id=None, description=['creates interaction'],
                        message_type=EnumElement(name='request'), params=
                        {
                            'choiceSet': Param(name='choiceSet', param_type=
                            Array(element_type=Struct(name='Choice', description=['A choice is an option given to '])))
                        })
        expected = {
            'name': 'CreateInteractionChoiceSet',
            'imports': [self.producer.imports(what='Choice', wherefrom='../structs/Choice.js'),
                        self.producer.imports(what='RpcRequest', wherefrom='../RpcRequest.js'),
                        self.producer.imports(what='FunctionID', wherefrom='../enums/FunctionID.js')],
            'methods': [self.producer.methods(origin='choiceSet', key='KEY_CHOICE_SET',
                                              method_title='ChoiceSet', external='Choice',
                                              description=['A choice is an option given to'], param_name='set',
                                              type='Array<Choice>')],
            'params': [self.producer.params(key='KEY_CHOICE_SET', value="'choiceSet'")],
            'description': 'creates interaction',
            'func': 'CreateInteractionChoiceSet',
            'extend': 'RpcRequest'
        }
        result = self.producer.transform(item)
        self.assertEqual(expected, result)
