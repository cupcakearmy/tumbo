import argparse
import os

from termcolor import cprint
from yaml import load, Loader

from tumbo import runner
from tumbo.utils import resolve_path


def cli():
    parser = argparse.ArgumentParser(
        description='Build and push docker matrix build')
    parser.add_argument(
        'config',
        default='./spec.yml', nargs='?', type=str,
        help='Config file for the build', metavar='file',
    )

    args = vars(parser.parse_args())

    config_file = os.path.abspath(args['config'])
    config_context = os.path.dirname(config_file)
    if not os.path.isfile(os.path.abspath(config_file)):
        cprint(f'Config file "{args["config"]}" does not exist', 'red')
        return

    with open(config_file, 'r') as f:
        config = load(f, Loader=Loader)
    context = config.get('context', config_context)
    context = resolve_path(config_context, context)

    if not os.path.isdir(context):
        cprint(f'Context is not a valid directory. {context}', 'red')

    config['context'] = context

    try:
        runner(**config)
    except FileNotFoundError as e:
        cprint(e, 'red')
