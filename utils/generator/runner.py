import logging
import re
import sys
from collections import namedtuple
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

root = Path(__file__).absolute().parents[0]

sys.path.append(root.joinpath('rpc_spec/InterfaceParser').as_posix())

try:
    from parsers.SDLRPCV2 import Parser
    from parsers.RPCBase import ParseError
    from model.Interface import Interface
    from model.Function import Function
except ModuleNotFoundError as e:
    print('{}. probably you did not initialize submodule'.format(e.msg))
    exit(1)


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
        self._env = None

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, value):
        self._env = Environment(loader=FileSystemLoader(value))

    def get_parser(self):
        """
        Parsing command-line arguments, or evaluating required Paths interactively.
        :return: an instance of argparse.ArgumentParser
        """
        if len(sys.argv) == 2 and sys.argv[1] in ('-v', '--version'):
            self.logger.warning('1.0')
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

        if args.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.ERROR)

        if unknown:
            self.logger.critical('found unknown arguments: ' + ' '.join(unknown))
            parser.print_help(sys.stderr)
            exit(1)

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
                            exit(1)
                    except KeyboardInterrupt:
                        self.logger.critical('\nThe user interrupted the execution of the program')
                        exit(1)

        p = Path(args.output_directory).absolute().resolve()
        p = p if p != out.path else out.path
        if not p.exists():
            self.logger.warning('Directory not found: {}, trying to create it'.format(p))
            try:
                p.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                self.logger.critical(e)
                exit(1)
        setattr(args, 'output_directory', p)

        if not Path(args.source_xml).exists():
            self.logger.critical('File not found: {}'.format(args.source_xml))
            exit(1)
        if args.source_xsd and not Path(args.source_xsd).exists():
            self.logger.critical('File not found: {}'.format(args.source_xsd))
            exit(1)
        elif not args.source_xsd and not Path(args.source_xml.replace('.xml', '.xsd')).exists():
            self.logger.critical('File not found: {}'.format(args.source_xml.replace('.xml', '.xsd')))
            exit(1)
        else:
            setattr(args, 'source_xsd', args.source_xml.replace('.xml', '.xsd'))

        if not args.enums and not args.structs and not args.functions:
            args.enums = True
            args.structs = True
            args.functions = True

        self.env = args.templates_directory

        self.logger.info(vars(args))
        return args

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

    def write_file(self, t, f, d):
        """
        Calling producer/transformer instance to transform initial Model to dict used in jinja2 templates.
        Applying transformed dict to jinja2 templates and writing to appropriate file
        :param t:
        :param f:
        :param d:
        :return: None
        """
        f.parents[0].mkdir(parents=True, exist_ok=True)
        with f.open('w', encoding='utf-8') as f:
            f.write(self.env.get_template(t + '_template.java').render(d))

    def process(self, args, items, transformer):
        """
        Process each item from initial Model. According to provided arguments skipping, overriding or asking what to to.
        :param args: parsed command-line arguments
        :param items: elements initial Model
        :param transformer: producer/transformer instance
        :return: None
        """
        for item in items:
            if args.regex_pattern and not re.match(args.regex_pattern, item.name):
                # self.logger.debug('{}/{} not match with {}'.format(args.output_directory.joinpath(
                #     transformer.package_name.replace('.', '/')), item.name, args.regex_pattern))
                continue
            name_type = type(item).__name__.lower()
            file = item.name + '.java'
            if isinstance(item, Function) and item.message_type.name == 'response':
                file = item.name + item.message_type.name.capitalize() + '.java'
            data = transformer.transform(item)
            file = args.output_directory.joinpath(data['package_name'].replace('.', '/')).joinpath(file)
            if file.is_file():
                if args.skip:
                    self.logger.info('Skipping {}'.format(file))
                    continue
                elif args.overwrite:
                    self.logger.info('Overriding {}'.format(file))
                    self.write_file(name_type, file, data)
                else:
                    while True:
                        confirm = input('File already exists {}. Overwrite? Y/Enter = yes, N = no\n'.format(file))
                        if confirm.lower() == 'y' or not confirm:
                            self.logger.info('Overriding {}'.format(file))
                            self.write_file(name_type, file, data)
                            break
                        if confirm.lower() == 'n':
                            self.logger.info('Skipping {}'.format(file))
                            break
            else:
                self.logger.info('Writing new {}'.format(file))
                self.write_file(name_type, file, data)

    def parser(self, xml, xsd):
        """
        Validate xml to match with xsd. Calling parsers to get Model from xml. If provided pattern, filtering Model.
        :param xml: path to MOBILE_API.xml
        :param xsd: path to MOBILE_API.xsd
        :param pattern: regex-pattern from command-line arguments to filter element from initial Model
        :return: initial Model
        """
        self.logger.info('''
        Validating XML and generating model with following parameters:
            Source xml      : {0}
            Source xsd      : {1}
        '''.format(xml, xsd))

        import xmlschema
        xs = xmlschema.XMLSchema(xsd)
        if not xs.is_valid(xml):
            self.logger.error(xs.validate(xml))
            exit(1)

        try:
            interface = Parser().parse(xml)
        except ParseError as e:
            self.logger.critical(e)
            exit(1)

        self.logger.info(vars(interface))
        return interface

    def get_paths(self, file=root.joinpath('paths.ini')):
        """
        :param file: path to file with Paths
        :return: namedtuple with Paths to key elements
        """
        fields = ('STRUCT_CLASS', 'REQUEST_CLASS', 'RESPONSE_CLASS',
                  'NOTIFICATION_CLASS', 'ENUMS_PACKAGE', 'STRUCTS_PACKAGE', 'FUNCTIONS_PACKAGE')
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
                            exit(1)
                        name, var = line.partition('=')[::2]
                        if name.strip() in d:
                            self.logger.critical('duplicate key {}'.format(name))
                            exit(1)
                        d[name.strip()] = var.strip()
        except FileNotFoundError as e1:
            self.logger.critical(e1)
            exit(1)

        for line in fields:
            if line not in d:
                self.logger.critical('in {} missed fields: {} '.format(file, str(line)))
                exit(1)

        Paths = namedtuple('Paths', ' '.join(fields))
        return Paths(**d)

    def main(self):
        """
        Entry point for parser and generator
        :return: None
        """
        args = self.get_parser()
        paths = self.get_paths()

        interface = self.parser(xml=args.source_xml, xsd=args.source_xsd)

        enum_names = tuple(interface.enums.keys())
        struct_names = tuple(interface.structs.keys())

        mappings = self.get_mappings()

        if args.enums and interface.enums:
            from EnumsProducer import EnumsProducer
            self.process(args, interface.enums.values(),
                         EnumsProducer(paths.ENUMS_PACKAGE, mappings))
        if args.structs and interface.structs:
            from StructsProducer import StructsProducer
            self.process(args, interface.structs.values(),
                         StructsProducer(paths, enum_names, struct_names, mappings))
        if args.functions and interface.functions:
            from FunctionsProducer import FunctionsProducer
            self.process(args, interface.functions.values(),
                         FunctionsProducer(paths, enum_names, struct_names, mappings))


if __name__ == '__main__':
    Generator().main()
