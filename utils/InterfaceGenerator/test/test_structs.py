from collections import namedtuple
from unittest import TestCase

from StructsProducer import StructsProducer
from parsers.Model import Struct, Param


class TestStructsProducer(TestCase):
    def setUp(self):
        self.maxDiff = None
        Prop = namedtuple('Prop', 'STRUCTS_DIR_NAME ENUMS_DIR_NAME PATH_TO_STRUCT_CLASS')
        paths = Prop(ENUMS_DIR_NAME='../enums',
                     STRUCTS_DIR_NAME='../structs',
                     PATH_TO_STRUCT_CLASS='../RpcStruct.js')

        self.producer = StructsProducer(paths, (), ('Image'))

    def test_SoftButton(self):
        item = Struct(name='SoftButton', members={
            'image': Param(name='image', param_type=Struct(name='Image'), description=['Optional image']),
        })
        expected = {
            'name': 'SoftButton',
            'imports': [self.producer.imports(what='Image', wherefrom='./Image.js'),
                        self.producer.imports(what='RpcStruct', wherefrom='../RpcStruct.js')],
            'methods': [self.producer.methods(description=['Optional image'], external='Image',
                                              key='KEY_IMAGE', method_title='Image',
                                              origin='image', param_name='image', type='Image')],
            'params': [self.producer.params(key='KEY_IMAGE', value="'image'")],
            'extend': 'RpcStruct'
        }
        result = self.producer.transform(item)
        self.assertEqual(expected, result)
