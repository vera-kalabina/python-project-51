import os
import re
from urllib.parse import urlparse, urlunparse


def get_new_name_and_extension(url):
    url_parts = list(urlparse(url))
    url_parts[0] = ''
    path, extension = os.path.splitext(url_parts[2])
    url_parts[2] = path
    url_without_scheme = urlunparse(url_parts)
    new_name = re.sub('[^a-z0-9A-Z]', '-', url_without_scheme)
    new_name = new_name.strip('-')
    return new_name, extension


def make_filename(url):
    new_name, extension = get_new_name_and_extension(url)
    if extension:
        format = extension
    else:
        format = '.html'
    return f'{new_name}{format}'


def make_dirname(url):
    new_name, extension = get_new_name_and_extension(url)
    new_extension = '_files'
    return f'{new_name}{new_extension}'
