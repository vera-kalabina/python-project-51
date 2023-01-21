from bs4 import BeautifulSoup
import os
import logging


from urllib.parse import urljoin, urlparse
from page_loader import url


TAGS_AND_ATTRIBUTES = {
    'img': 'src',
    'script': 'src',
    'link': 'href',
}


def get_resources(response, link, dir_name):
    resources = []
    data = BeautifulSoup(response.text, 'html.parser')
    for tag in data.find_all(TAGS_AND_ATTRIBUTES.keys()):
        attribute = TAGS_AND_ATTRIBUTES.get(tag.name)
        attr_value = tag.get(attribute)
        if attr_value is None:
            logging.info('Content not found')
            continue
        if attr_value.startswith('http'):
            if urlparse(link).netloc == urlparse(attr_value).netloc:
                content_link = attr_value
            else:
                logging.debug(f"Content {attr_value} wasn't downloaded "
                              "as it's on a different host")
                continue
        else:
            if not attr_value.startswith('/'):
                attr_value = '/' + attr_value
            content_link = urljoin(link, attr_value)
        resources.append(content_link)
        tag[attribute] = os.path.join(dir_name, url.make_filename(content_link))
    return resources, data.prettify()
