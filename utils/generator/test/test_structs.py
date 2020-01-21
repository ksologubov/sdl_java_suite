from collections import namedtuple
import unittest

from transformers.structs_producer import StructsProducer
from model.param import Param
from model.struct import Struct


class TestStructsProducer(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        Paths = namedtuple('Prop', 'enums_package structs_package struct_class')
        paths = Paths(enums_package='com.smartdevicelink.proxy.rpc.enums',
                      structs_package='com.smartdevicelink.proxy.rpc',
                      struct_class='com.smartdevicelink.proxy.RPCStruct')
        self.producer = StructsProducer(paths, (), ('Image',))

    def test_SoftButton(self):
        item = Struct(name='SoftButton', members={
            'image': Param(name='image', param_type=Struct(name='Image'), description=['Optional image']),
        })
        result = self.producer.transform(item)
        expected = {
            'package_name': 'com.smartdevicelink.proxy.rpc',
            'imports': ['android.support.annotation.NonNull', '', 'com.smartdevicelink.proxy.RPCStruct', '',
                        'java.util.Hashtable'],
            'class_name': 'SoftButton',
            'extends_class': 'RPCStruct',
            'since': None,
            'deprecated': None,
            'params': (self.producer.params(deprecated=None, description=['Optional image'], key='KEY_IMAGE',
                       last='image', mandatory=True, origin='image', return_type='Image',
                       since=None, title='Image'),)
        }
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
    # unittest.defaultTestLoader.loadTestsFromName(__name__).debug()  # enable debugging
