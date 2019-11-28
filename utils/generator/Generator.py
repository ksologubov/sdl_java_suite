import argparse
import logging
import re
from collections import namedtuple
from pathlib import Path


def class_pass_imports() -> str:
    import sys
    path = Path(__file__)

    sys.path.append(path.parents[1].joinpath('utils/generator/rpc_spec/InterfaceParser').as_posix())
    return path.parents[0]


root = class_pass_imports()

try:
    from rpc_spec.InterfaceParser import Parser
    from rpc_spec.InterfaceParser.parsers.Model import Interface
except ModuleNotFoundError as e:
    print('{}. probably you did not initialize submodule'.format(e.msg))
    exit(1)

logger = logging.getLogger('Generator')


def _create_parser():
    """Create parser for parsing command-line arguments.
    Returns an instance of argparse.ArgumentParser
    """
    Paths = namedtuple('Paths', 'name path')
    #xml = Paths('source_xml', root.parents[0].joinpath('lib/rpc_spec/MOBILE_API.xml'))
    xml = Paths('source_xml', root.parents[0].joinpath('generator/rpc_spec/MOBILE_API.xml'))
    required_source = False if xml.path.exists() else True

    #out = Paths('output_directory', root.parents[0].joinpath('lib/js/src/rpc'))
    out = Paths('output_directory', root.parents[0].joinpath('generator/rpc_spec/java/src/rpc'))
    output_required = False if out.path.exists() else True

    parser = argparse.ArgumentParser(description='SmartSchema interface parser')
    parser.add_argument('-xml', '--source-xml', '--input-file', required=required_source,
                        help='should point to MOBILE_API.xml')
    parser.add_argument('-xsd', '--source-xsd', required=False)
    parser.add_argument('-d', '--output-directory', required=output_required,
                        help='define the place where the generated output should be placed')
    parser.add_argument('-r', '--regex-pattern', required=False, type=str,
                        help='only elements matched with defined regex pattern will be parsed and generated, '
                             'if present')
    parser.add_argument('-v', '--version', required=False, default='1.0')
    parser.add_argument('--verbose', action='store_true', help='display additional details like logs etc')
    parser.add_argument('-e', '--enums', required=False, action='store_true',
                        help='only specified elements will be generated, if present')
    parser.add_argument('-s', '--structs', required=False, action='store_true',
                        help='only specified elements will be generated, if present')
    parser.add_argument('-m', '-f', '--functions', required=False, action='store_true',
                        help='only specified elements will be generated, if present')
    parser.add_argument('-y', '--overwrite', action='store_true',
                        help='force overwriting of existing files in output directory, ignore confirmation message')
    parser.add_argument('-n', '--skip', action='store_true',
                        help='skip overwriting of existing files in output directory, ignore confirmation message')
    parser.add_argument('-t', '--templates-directory', nargs='?', default=root.joinpath('templates').as_posix(),
                        help='path to directory with templates', type=str)

    args, unknown = parser.parse_known_args()

    for n in (xml, out):
        if not getattr(args, n.name) and n.path.exists():
            while True:
                confirm = input('Confirm default path {} for {} Y/Enter = yes, N = no\n'.format(n.path, n.name))
                if confirm.lower() == 'y' or not confirm:
                    setattr(args, n.name, n.path.as_posix())
                    logger.warning('{} set to {}, you can overwrite it using argument'.format(n.name, n.path))
                    break

    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)

    if not args.enums and not args.structs and not args.functions:
        args.enums = True
        args.structs = True
        args.functions = True

    logger.debug(args)

    return args


def get_paths(file_name=root.joinpath('paths.ini').as_posix()):
    fields = ('PATH_TO_ENUM_CLASS', 'PATH_TO_STRUCT_CLASS', 'PATH_TO_REQUEST_CLASS', 'PATH_TO_RESPONSE_CLASS',
              'PATH_TO_NOTIFICATION_CLASS', 'ENUMS_DIR_NAME', 'STRUCTS_DIR_NAME', 'FUNCTIONS_DIR_NAME')
    d = {}
    with open(file_name, 'r') as f:
        for line in f:
            if line.startswith('#'):
                logger.debug('commented property {}, which will be skipped'.format(line.strip()))
                continue
            if re.match(r'^(\w+)\s?=\s?(.+)', line):
                if len(line.split('=')) > 2:
                    logger.critical('can not evaluate value, too many separators {}'.format(str(line)))
                    exit(1)
                name, var = line.partition('=')[::2]
                if name.strip() in d:
                    logger.critical('duplicate key {}'.format(name))
                    exit(1)
                d[name.strip()] = var.strip()

    for line in fields:
        if line not in d:
            logger.critical('in {} missed fields: {} '.format(file_name, str(line)))
            exit(1)

    return d


if __name__ == '__main__':
    from EnumsProducer import EnumsProducer
    from FunctionsProducer import FunctionsProducer
    from StructsProducer import StructsProducer

    arg = _create_parser()

    for na, va in get_paths().items():
        setattr(arg, na, va)

    i = Parser.main(source_xml=arg.source_xml, source_xsd=arg.source_xsd)
    logger.debug(vars(i))

    if arg.enums:
        EnumsProducer(i, arg).process()
    if arg.structs:
        StructsProducer(i, arg).process()
    if arg.functions:
        FunctionsProducer(i, arg).process()