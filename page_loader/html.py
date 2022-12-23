import requests
from bs4 import BeautifulSoup
import os

from urllib.parse import urljoin, urlparse
from page_loader import url

def get_resources(response, link, dir_name):
    TAGS_AND_ATTRIBUTES = {
        'img': 'src',
        'script': 'src',
        'link': 'href',
    }
    resources = []
    data = BeautifulSoup(response.text, 'html.parser')
    for teg in data.find_all(TAGS_AND_ATTRIBUTES.keys()):
        attribute = TAGS_AND_ATTRIBUTES.get(teg.name)
        content = teg.get(attribute)
        if content is None:
            continue
        if content.startswith('http'):
            if urlparse(link).netloc == urlparse(content).netloc:
                content_link = content
        else:
            if not content.startswith('/'):
                content = '/' + content
            content_link = urljoin(link, content)
        resources.append(content_link)
        teg[attribute] = os.path.join(dir_name, url.make_file_name(content_link))
    return resources, data.prettify()