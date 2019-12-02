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
    from parsers.Model import Interface, Function
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

    def get_parser(self, output_dir):
        """
        Parsing command-line arguments, or evaluating required Paths interactively.
        :return: an instance of argparse.ArgumentParser
        """
        from argparse import ArgumentParser

        Paths = namedtuple('Paths', 'name path')
        xml = Paths('source_xml', root.joinpath('rpc_spec/MOBILE_API.xml'))
        required_source = False if xml.path.exists() else True

        out = Paths('output_directory', root.parents[1].joinpath(output_dir))
        output_required = False if out.path.exists() else True

        parser = ArgumentParser(description='SmartSchema interface parser')
        parser.add_argument('-xml', '--source-xml', '--input-file', required=required_source,
                            help='should point to MOBILE_API.xml')
        parser.add_argument('-xsd', '--source-xsd', required=False)
        parser.add_argument('-d', '--output-directory', required=output_required,
                            help='define the place where the generated output should be placed')
        parser.add_argument('-t', '--templates-directory', nargs='?', default=root.joinpath('templates').as_posix(),
                            help='path to directory with templates', type=str)
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

        args, unknown = parser.parse_known_args()

        if unknown:
            self.logger.warning('found unknown arguments' + ''.join(unknown))

        for n in (xml, out):
            if not getattr(args, n.name) and n.path.exists():
                while True:
                    confirm = input('Confirm default path {} for {} Y/Enter = yes, N = no\n'.format(n.path, n.name))
                    if confirm.lower() == 'y' or not confirm:
                        setattr(args, n.name, n.path.as_posix())
                        self.logger.warning('{} set to {}, you can overwrite it using argument'.format(n.name, n.path))
                        break
                    if confirm.lower() == 'n':
                        self.logger.warning('provide argument {}'.format(n.name))
                        exit(1)

        if args.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.ERROR)

        if not args.enums and not args.structs and not args.functions:
            args.enums = True
            args.structs = True
            args.functions = True

        if args.source_xsd is None:
            setattr(args, 'source_xsd', args.source_xml.replace('.xml', '.xsd'))
        if not Path(args.source_xsd).exists():
            self.logger.critical(FileNotFoundError('not found', args.source_xsd))
            exit(1)

        self.logger.info(vars(args))

        setattr(args, 'output_directory', Path(args.output_directory))
        setattr(args, 'templates_directory', Environment(loader=FileSystemLoader(args.templates_directory)))

        return args

    @staticmethod
    def get_mappings(file=root.joinpath('mapping.json')):
        """
        The key name in *.json is equal to property named in jinja2 templates
        :param file: path to file with manual mappings
        :return: dictionary with custom manual mappings
        """
        import json
        with file.open('r') as f:
            s = f.readlines()
        return json.loads(''.join(s))

    @staticmethod
    def make_directory(output_directory: Path, directory) -> Path:
        """
        :param output_directory: target Path output_directory in which should be create directory
        :param directory: property from producer/transformer (ENUMS|STRUCTS|FUNCTIONS)_DIR_NAME
        :return: Path to output_directory + directory
        """
        p = re.search(r'^([../]*)(.+)', directory)
        if p:
            p = output_directory.joinpath(p.group(2))
        p.mkdir(parents=True, exist_ok=True)
        return p

    def process(self, args, items, transformer):
        """
        Process each item from initial Model. According to provided arguments skipping, overriding or asking what to to.
        :param args: parsed command-line arguments
        :param items: elements initial Model
        :param transformer: producer/transformer instance
        :return: None
        """

        def write_file(it):
            """
            Calling producer/transformer instance to transform initial Model to dict used in jinja2 templates.
            Applying transformed dict to jinja2 templates and writing to appropriate file
            :param it: one particular element from initial Model
            :return: None
            """
            data = transformer.transform(it)

            template_suffix = '_template.java'
            if name_type.lower() == 'enum':
                if data['methods'][0].method_title == data['methods'][0].origin:
                    template_suffix = '_template_simple.java'
                else:
                    template_suffix = '_template_custom.java'
            else:
                return  # stub till other types implemented

            with file.open('w', encoding='utf-8') as f:
                f.write(args.templates_directory.get_template(name_type.lower() + template_suffix).render(data))

        path = self.make_directory(args.output_directory, transformer.directory)
        for item in items:
            name_type = type(item).__name__
            file = path.joinpath(item.name + '.java')
            if isinstance(item, Function) and item.message_type.name == 'response':
                file = path.joinpath(item.name + item.message_type.name.capitalize() + '.java')
            if file.is_file():
                if args.skip:
                    self.logger.info('Skipping {}'.format(file))
                    continue
                elif args.overwrite:
                    self.logger.info('Overriding {}'.format(file))
                    write_file(item)
                else:
                    while True:
                        confirm = input('File already exists {}. Overwrite? Y/Enter = yes, N = no\n'.format(file))
                        if confirm.lower() == 'y' or not confirm:
                            self.logger.info('Overriding {}'.format(file))
                            write_file(item)
                            break
                        if confirm.lower() == 'n':
                            self.logger.info('Skipping {}'.format(file))
                            break
            else:
                self.logger.info('Writing new {}'.format(file))
                write_file(item)

    def parser(self, xml, xsd, pattern=None):
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

        self.logger.info(vars(interface))
        return interface

    def get_paths(self, file=root.joinpath('paths.ini')):
        """
        :param file: path to file with Paths
        :return: namedtuple with Paths to key elements
        """
        fields = ('PATH_TO_STRUCT_CLASS', 'PATH_TO_REQUEST_CLASS', 'PATH_TO_RESPONSE_CLASS',
                  'PATH_TO_NOTIFICATION_CLASS', 'OUTPUT_DIR_NAME', 'ENUMS_DIR_NAME', 'STRUCTS_DIR_NAME',
                  'FUNCTIONS_DIR_NAME')
        d = {}
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
        paths = self.get_paths()
        args = self.get_parser(paths.OUTPUT_DIR_NAME)

        interface = self.parser(xml=args.source_xml, xsd=args.source_xsd, pattern=args.regex_pattern)

        enum_names = tuple(interface.enums.keys())
        struct_names = tuple(interface.structs.keys())

        mappings = self.get_mappings()

        if args.enums and interface.enums:
            from EnumsProducer import EnumsProducer
            self.process(args, interface.enums.values(), EnumsProducer(paths, mappings))
        if args.structs and interface.structs:
            from StructsProducer import StructsProducer
            self.process(args, interface.structs.values(), StructsProducer(paths, enum_names, struct_names, mappings))
        if args.functions and interface.functions:
            from FunctionsProducer import FunctionsProducer
            self.process(args, interface.functions.values(),
                         FunctionsProducer(paths, enum_names, struct_names, mappings))


if __name__ == '__main__':
    Generator().main()
