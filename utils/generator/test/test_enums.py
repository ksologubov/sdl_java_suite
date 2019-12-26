from collections import namedtuple
from unittest import TestCase

from transformers.enums_producer import EnumsProducer
from model.enum import Enum
from model.enum_element import EnumElement


class TestEnumsProducer(TestCase):
    def setUp(self):
        self.maxDiff = None
        Prop = namedtuple('Prop', 'ENUMS_DIR_NAME STRUCTS_DIR_NAME PATH_TO_ENUM_CLASS')
        paths = Prop(ENUMS_DIR_NAME='../enums',
                     STRUCTS_DIR_NAME='../structs',
                     PATH_TO_ENUM_CLASS='../../util/Enum.js')
        self.producer = EnumsProducer(paths)

    def test_FunctionID(self):
        item = Enum(name='FunctionID', elements={
            'RESERVED': EnumElement(name='RESERVED', value=0),
            'RegisterAppInterfaceID': EnumElement(name='RegisterAppInterfaceID', hexvalue=1),
            'PerformAudioPassThruID': EnumElement(name='PerformAudioPassThruID', hexvalue=10)
        })
        expected = {
            'name': 'FunctionID',
            'imports': [self.producer.imports(what='Enum', wherefrom='../../util/Enum.js')],
            'methods': [self.producer.methods(origin='RESERVED',
                                              method_title='RESERVED',
                                              description=[], type='Number'),
                        self.producer.methods(origin='RegisterAppInterfaceID',
                                              method_title='RegisterAppInterface',
                                              description=[], type='Number'),
                        self.producer.methods(origin='PerformAudioPassThruID',
                                              method_title='PerformAudioPassThru',
                                              description=[], type='Number')],
            'params': [self.producer.params(key='RESERVED', value=0),
                       self.producer.params(key='RegisterAppInterface', value='0x01'),
                       self.producer.params(key='PerformAudioPassThru', value='0x10')],
            'extend': 'Enum'
        }
        result = self.producer.transform(item)
        self.assertEqual(expected, result)

    def test_Result(self):
        item = Enum(name='Result', elements={
            'SUCCESS': EnumElement(name='SUCCESS')
        })
        expected = {
            'name': 'Result',
            'imports': [self.producer.imports(what='Enum', wherefrom='../../util/Enum.js')],
            'methods': [self.producer.methods(origin='SUCCESS',
                                              method_title='SUCCESS',
                                              description=[], type='String')],
            'params': [self.producer.params(key='SUCCESS', value="'SUCCESS'")],
            'extend': 'Enum'
        }
        result = self.producer.transform(item)
        self.assertEqual(expected, result)

# if __name__ == '__main__':
#     testLoad = TestLoader()
#     suites: TestSuite = testLoad.loadTestsFromTestCase(TestEnumsProducer)
#
#     runner = TextTestRunner(verbosity=2)
#     testResult = runner.run(suites)
