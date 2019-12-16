import sys
from pathlib import Path
from unittest import TestLoader, TestSuite, TextTestRunner

path = Path(__file__).absolute()

sys.path.append(path.parents[2].joinpath('lib/rpc_spec/InterfaceParser').as_posix())
sys.path.append(path.parents[1].as_posix())

try:
    from test_enums import TestEnumsProducer
    from test_functions import TestFunctionsProducer
    from test_structs import TestStructsProducer
    from EnumsProducer import EnumsProducer
    from parsers.Model import Interface
except ModuleNotFoundError as e:
    print('{}. probably you did not initialize submodule'.format(e.msg))
    exit(1)

if __name__ == '__main__':
    suite = TestSuite()

    suite.addTests(TestLoader().loadTestsFromTestCase(TestFunctionsProducer))
    suite.addTests(TestLoader().loadTestsFromTestCase(TestEnumsProducer))
    suite.addTests(TestLoader().loadTestsFromTestCase(TestStructsProducer))

    runner = TextTestRunner(verbosity=2)
    testResult = runner.run(suite)
