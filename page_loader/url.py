import os
import re
from urllib.parse import urlparse, urlunparse


def convert_name(url):
    url_parts = list(urlparse(url))
    url_parts[0] = ''
    path, extension = os.path.splitext(url_parts[2])
    url_parts[2] = path
    if extension:
        format = extension
    else:
        format = '.html'
    url_without_scheme = urlunparse(url_parts)
    new_name = replace_chars(url_without_scheme)
    new_name = new_name.strip('-')
    return f'{new_name}{format}'


def replace_chars(string):
    result = re.sub('[^a-z0-9A-Z]', '-', string)
    return result
