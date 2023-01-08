from bs4 import BeautifulSoup
import os
from page_loader.logger import log_error


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
            log_error.error('Content not found')
            continue
        if content.startswith('http'):
            if urlparse(link).netloc == urlparse(content).netloc:
                content_link = content
            else:
                log_error.error("Content wasn't downloaded "
                                "as it's on a different host")
                continue
        else:
            if not content.startswith('/'):
                content = '/' + content
            content_link = urljoin(link, content)
        resources.append(content_link)
        teg[attribute] = os.path.join(dir_name, url.make_filename(content_link))
    return resources, data.prettify()
