import logging
import re
import sys
from collections import namedtuple
from pprint import pformat

from jinja2 import Environment, FileSystemLoader
from pathlib2 import Path

root = Path(__file__).absolute().parents[0]

sys.path.append(root.joinpath('rpc_spec/InterfaceParser').as_posix())

try:
    from parsers.sdl_rpc_v2 import Parser
    from parsers.parse_error import ParseError
    from model.interface import Interface
    from model.function import Function
except ModuleNotFoundError as e:
    print('{}.\nprobably you did not initialize submodule'.format(e))
    sys.exit(1)

from transformers.common_producer import InterfaceProducerCommon
from transformers.enums_producer import EnumsProducer
from transformers.functions_producer import FunctionsProducer
from transformers.structs_producer import StructsProducer


class Generator(object):
    """
    This class contains only technical features, as follow:
    - parsing command-line arguments, or evaluating required Paths interactively;
    - calling parsers to get Model from xml;
    - calling producers to transform initial Model to dict used in jinja2 templates
    Not required to be covered by unit tests cause contains only technical features.
    """

    def __init__(self):
        self.logger = logging.getLogger('Generator')
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%m-%d %H:%M')
        self._env = None

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, value):
        if not Path(value).exists():
            self.logger.critical('Directory with templates not found {}'.format(value))
            sys.exit(1)
        else:
            self._env = Environment(loader=FileSystemLoader(value))

    @property
    def get_version(self):
        return InterfaceProducerCommon.version

    def get_parser(self):
        """
        Parsing command-line arguments, or evaluating required Paths interactively.
        :return: an instance of argparse.ArgumentParser
        """
        if len(sys.argv) == 2 and sys.argv[1] in ('-v', '--version'):
            print(self.get_version)
            exit(0)

        from argparse import ArgumentParser

        Paths = namedtuple('Paths', 'name path')
        xml = Paths('source_xml', root.joinpath('rpc_spec/MOBILE_API.xml'))
        required_source = False if xml.path.exists() else True

        out = Paths('output_directory', root.parents[1].joinpath('base/src/main/java/'))
        output_required = False if out.path.exists() else True

        parser = ArgumentParser(description='Proxy Library RPC Generator')
        parser.add_argument('-v', '--version', action='store_true', help='print the version and exit')
        parser.add_argument('-xml', '--source-xml', '--input-file', required=required_source,
                            help='should point to MOBILE_API.xml')
        parser.add_argument('-xsd', '--source-xsd', required=False)
        parser.add_argument('-d', '--output-directory', required=output_required,
                            help='define the place where the generated output should be placed')
        parser.add_argument('-t', '--templates-directory', nargs='?', default=root.joinpath('templates').as_posix(),
                            help='path to directory with templates')
        parser.add_argument('-r', '--regex-pattern', required=False,
                            help='only elements matched with defined regex pattern will be parsed and generated')
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

        args, unknown = parser.parse_known_args()

        if unknown:
            self.logger.critical('found unknown arguments: ' + ' '.join(unknown))
            parser.print_help(sys.stderr)
            sys.exit(1)

        if args.skip and args.overwrite:
            self.logger.critical('please select only one option skip or overwrite')
            sys.exit(1)

        if not args.enums and not args.structs and not args.functions:
            args.enums = args.structs = args.functions = True

        for n in (xml, out):
            if not getattr(args, n.name) and n.path.exists():
                while True:
                    try:
                        confirm = input('Confirm default path {} for {} Y/Enter = yes, N = no\n'.format(n.path, n.name))
                        if confirm.lower() == 'y' or not confirm:
                            self.logger.warning('{} set to {}'.format(n.name, n.path))
                            setattr(args, n.name, n.path.as_posix())
                            break
                        if confirm.lower() == 'n':
                            self.logger.warning('provide argument {}'.format(n.name))
                            sys.exit(1)
                    except KeyboardInterrupt:
                        print('\nThe user interrupted the execution of the program')
                        sys.exit(1)

        if not Path(args.source_xml).exists():
            self.logger.critical('File not found: {}'.format(args.source_xml))
            sys.exit(1)
        if args.source_xsd and not Path(args.source_xsd).exists():
            self.logger.critical('File not found: {}'.format(args.source_xsd))
            sys.exit(1)
        elif not args.source_xsd and not Path(args.source_xml.replace('.xml', '.xsd')).exists():
            self.logger.critical('File not found: {}'.format(args.source_xml.replace('.xml', '.xsd')))
            sys.exit(1)
        else:
            setattr(args, 'source_xsd', args.source_xml.replace('.xml', '.xsd'))

        if args.output_directory.startswith('/'):
            p = Path(args.output_directory).absolute().resolve()
        else:
            p = root.joinpath(args.output_directory).resolve()
        if not p.exists():
            self.logger.warning('Directory not found: {}, trying to create it'.format(p))
            try:
                p.mkdir(parents=True, exist_ok=True)
            except OSError as e1:
                self.logger.critical('Failed to create directory {}, {}'.format(p.as_posix(), e1))
                sys.exit(1)
        setattr(args, 'output_directory', p)

        self.env = args.templates_directory

        if args.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.ERROR)

        self.logger.info(pformat(vars(args)))
        return args

    def versions_compatibility_validating(self):
        """version of generator script requires the same or lesser version of parser script.
        if the parser script needs to fix a bug (and becomes, e.g. 1.0.1) and the generator script stays at 1.0.0.
        As long as the generator script is the same or greater major version, it should be parsable.
        This requires some level of backward compatibility. E.g. they have to be the same major version.

        """
        from re import findall
        from inspect import getfile
        from os.path import basename

        regex = '(\d+\.\d+).(\d)'

        parser_origin = Parser().get_version
        generator_origin = self.get_version
        parser_split = findall(regex, parser_origin).pop()
        generator_split = findall(regex, generator_origin).pop()

        parser_major = float(parser_split[0])
        generator_major = float(generator_split[0])

        if parser_major > generator_major:
            self.logger.critical('Generator ({}) requires the same or lesser version of Parser ({})'
                                 .format(generator_origin, parser_origin))
            sys.exit(1)

        self.logger.info('Parser type: {}, version {}.\tGenerator type: {}, version {}'
                         .format(basename(getfile(Parser().__class__)), parser_origin,
                                 basename(getfile(InterfaceProducerCommon.__class__)), generator_origin))

    def get_paths(self, file=root.joinpath('paths.ini')):
        """
        :param file: path to file with Paths
        :return: namedtuple with Paths to key elements
        """
        fields = ('struct_class', 'request_class', 'response_class',
                  'notification_class', 'enums_package', 'structs_package', 'functions_package')
        d = {}
        try:
            with file.open('r') as f:
                for line in f:
                    if line.startswith('#'):
                        self.logger.info('commented property {}, which will be skipped'.format(line.strip()))
                        continue
                    if re.match(r'^(\w+)\s?=\s?(.+)', line):
                        if len(line.split('=')) > 2:
                            self.logger.critical('can not evaluate value, too many separators {}'.format(str(line)))
                            sys.exit(1)
                        name, var = line.partition('=')[::2]
                        if name.strip() in d:
                            self.logger.critical('duplicate key {}'.format(name))
                            sys.exit(1)
                        d[name.strip().lower()] = var.strip()
        except FileNotFoundError as e1:
            self.logger.critical(e1)
            sys.exit(1)

        for line in fields:
            if line not in d:
                self.logger.critical('in {} missed fields: {} '.format(file, str(line)))
                sys.exit(1)

        Paths = namedtuple('Paths', ' '.join(fields))
        return Paths(**d)

    def get_mappings(self, file=root.joinpath('mapping.json')):
        """
        The key name in *.json is equal to property named in jinja2 templates
        :param file: path to file with manual mappings
        :return: dictionary with custom manual mappings
        """
        import json
        from json import JSONDecodeError
        try:
            with file.open('r') as f:
                s = f.readlines()
            return json.loads(''.join(s))
        except (FileNotFoundError, JSONDecodeError) as e1:
            self.logger.error(e1)
            return {}

    def write_file(self, file, data, template):
        """
        Calling producer/transformer instance to transform initial Model to dict used in jinja2 templates.
        Applying transformed dict to jinja2 templates and writing to appropriate file
        :param file:
        :param data:
        :param template:
        """
        file.parents[0].mkdir(parents=True, exist_ok=True)
        with file.open('w', encoding='utf-8') as f:
            f.write(self.env.get_template(template).render(data))

    def process(self, directory, skip, overwrite, items, transformer):
        """
        Process each item from initial Model. According to provided arguments skipping, overriding or asking what to to.
        :param directory: output directory for writing output files
        :param skip: if file exist skip it
        :param overwrite: if file exist overwrite it
        :param items: elements initial Model
        :param transformer: producer/transformer instance
        """
        template = type(next(iter(items))).__name__.lower() + '_template.java'
        for item in items:
            file = item.name + '.java'
            if isinstance(item, Function) and item.message_type.name == 'response':
                suffix = item.message_type.name.capitalize()
                if item.name != "GenericResponse":
                    file = item.name + suffix + '.java'
            data = transformer.transform(item)
            file = directory.joinpath(data['package_name'].replace('.', '/')).joinpath(file)
            if file.is_file():
                if skip:
                    self.logger.info('Skipping {}'.format(file))
                    continue
                elif overwrite:
                    self.logger.info('Overriding {}'.format(file))
                    self.write_file(file, data, template)
                else:
                    while True:
                        confirm = input('File already exists {}. Overwrite? Y/Enter = yes, N = no\n'.format(file))
                        if confirm.lower() == 'y' or not confirm:
                            self.logger.info('Overriding {}'.format(file))
                            self.write_file(file, data, template)
                            break
                        if confirm.lower() == 'n':
                            self.logger.info('Skipping {}'.format(file))
                            break
            else:
                self.logger.info('Writing new {}'.format(file))
                self.write_file(file, data, template)

    def parser(self, xml, xsd, pattern=None):
        """
        Validate xml to match with xsd. Calling parsers to get Model from xml. If provided pattern, filtering Model.
        :param xml: path to MOBILE_API.xml
        :param xsd: path to MOBILE_API.xsd
        :param pattern: regex-pattern from command-line arguments to filter element from initial Model
        :return: initial Model
        """
        self.logger.info('''Validating XML and generating model with following parameters:
            Source xml      : {0}
            Source xsd      : {1}'''.format(xml, xsd))

        from xmlschema import XMLSchema
        from parsers.parse_error import ParseError as InterfaceError
        from xml.etree.ElementTree import ParseError as XMLSchemaError

        interface = Interface()
        try:
            xs = XMLSchema(xsd)
            if not xs.is_valid(xml):
                raise XMLSchemaError(xs.validate(xml))
            interface = Parser().parse(xml)
        except (InterfaceError, XMLSchemaError, TypeError) as e1:
            self.logger.critical('Invalid XML file content: {}, {}'.format(xml, e1))
            sys.exit(1)

        enum_names = tuple(interface.enums.keys())
        struct_names = tuple(interface.structs.keys())

        if pattern:
            match = {}
            match.update({'params': interface.params})
            for k, v in vars(interface).items():
                if k == 'params':
                    continue
                for k1, item in v.items():
                    if re.match(pattern, item.name):
                        self.logger.info('{}/{} match with {}'.format(k, item.name, pattern))
                        if k in match:
                            match[k].update({k1: item})
                        else:
                            match.update({k: {k1: item}})
            interface = Interface(**match)

        match = {'enums': tuple(interface.enums.keys()),
                 'structs': tuple(interface.structs.keys()),
                 'functions': tuple(map(lambda i: i.function_id.name, interface.functions.values())),
                 'params': interface.params}
        self.logger.debug(pformat(match))
        return enum_names, struct_names, interface

    def main(self):
        """
        Entry point for parser and generator
        :return: None
        """
        args = self.get_parser()

        self.versions_compatibility_validating()

        enum_names, struct_names, interface = self.parser(xml=args.source_xml, xsd=args.source_xsd,
                                                          pattern=args.regex_pattern)

        paths = self.get_paths()
        mappings = self.get_mappings()

        if args.enums and interface.enums:
            self.process(args.output_directory, args.skip, args.overwrite, tuple(interface.enums.values()),
                         EnumsProducer(paths.enums_package, mappings))
        if args.structs and interface.structs:
            self.process(args.output_directory, args.skip, args.overwrite, tuple(interface.structs.values()),
                         StructsProducer(paths, enum_names, struct_names, mappings))
        if args.functions and interface.functions:
            self.process(args.output_directory, args.skip, args.overwrite, tuple(interface.functions.values()),
                         FunctionsProducer(paths, enum_names, struct_names, mappings))


if __name__ == '__main__':
    Generator().main()
