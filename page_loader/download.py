import os
from page_loader import url


def download(link, actual_path=os.getcwd()):
    html_path = os.path.join(actual_path, url.convert_name(link))
    print(html_path)
