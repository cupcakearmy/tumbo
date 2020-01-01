import os
import random
import subprocess
from itertools import product
from multiprocessing import Pool, cpu_count
from typing import Optional

from termcolor import colored

from tumbo.utils import buffer_to_string, resolve_path, compile_string


def exec(command, *args, **kwargs):
    output = subprocess.run(command, *args, capture_output=True, **kwargs)

    if output.returncode is not 0:
        raise Exception(buffer_to_string(output.stderr))

    return buffer_to_string(output.stdout)


def exec_multiple(commands, *args, show=True, **kwargs):
    try:
        for command in commands:
            print(colored(' '.join(command), 'blue', attrs=['bold']))
            result = exec(command, *args, **kwargs)
            if show:
                print(result + '\n')
    except Exception as e:
        print(colored(e, 'red'))


def build_push_run(rendered, name, context, push, run, show=False):
    try:

        # Create a tmp dockerfile to work with
        hash = resolve_path(context, str(random.getrandbits(128)))

        if not os.access('.', os.W_OK):
            print(colored('Cannot write to directory', 'red'))
            return

        if os.path.isfile(hash):
            print(colored(f'File {hash} already exitsts.', 'red'))
            return

        with open(hash, 'w') as f:
            f.write(rendered)

        commands = [['docker', 'build', '-f', hash, '-t', name, '.']]
        if (push):
            commands.append(['docker', 'push', name])
        if (run):
            commands.append(['docker', 'run', '--rm', name])

        exec_multiple(commands, cwd=context, show=show)

    finally:
        # Delete the tmp file
        if os.path.exists(hash):
            os.remove(hash)


def process_queue(queue, context, parallel, push, run):
    queue = [
        (rendered, tag, context, push, run, True)
        for rendered, tag in queue
    ]

    if parallel:
        thread_count = parallel if type(parallel) is int else cpu_count()
        with Pool(thread_count) as pool:
            pool.starmap(build_push_run, queue)
    else:
        for item in queue:
            build_push_run(*item)


def compile_templates(variables, recipe, tag, context, show=True):
    queue = []
    for item in product(*variables.values()):
        zipped_variables = dict(zip(variables.keys(), item))
        path = compile_string(recipe, zipped_variables)
        if tag:
            name = compile_string(tag, zipped_variables)
        else:
            # If no tag is provided construct one from all variables to avoid any duplicated tags
            all_values_as_strings = map(str, zipped_variables.values())
            name = '-'.join(all_values_as_strings)
            name = name.lower()  # Docker tags must be lower case

        with open(resolve_path(context, path), 'r') as f:
            rendered = compile_string(f.read(), zipped_variables)

        queue.append((rendered, name))

        if show:
            print(
                '\n' +
                colored('Variation:', 'green') + f'\t{str(zipped_variables)}\n' +
                colored('Recipe:', 'green') + f'\t\t{path}\n' +
                colored('Tag:', 'green') + f'\t\t{name}\n'
            )

    return queue


def login_if_required(registry) -> Optional[str]:
    if registry:
        host = registry.get('host')
        username = registry.get('username')
        password = registry.get('password')

        if not host:
            raise Exception(colored('No host set for registry', 'red'))

        cmd = ['docker', 'login']
        if username or password:
            if not username or not password:
                raise Exception(colored('Username or password not set', 'red'))
            # TODO: use stdin
            cmd += ['-u', username, '-p', password]

        try:
            out = exec(cmd + [host])
            print(colored(out + '\n', 'green'))
            return host
        except Exception as e:
            print(colored('Could not log in, check your username', 'red'))
            return None

    return None
