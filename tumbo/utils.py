import os
import sys

from jinja2 import Template


def compile_string(template: str, variables={}):
    return Template(template).render(**variables)


def buffer_to_string(buffer) -> str:
    return buffer.decode(sys.getdefaultencoding()).strip()


def resolve_path(base: str, path: str) -> str:
    if not os.path.isabs(path):
        # If the path is not absolute take the relative path from the base directory
        path = os.path.join(base, path)
    return os.path.abspath(path)  # Normalise
