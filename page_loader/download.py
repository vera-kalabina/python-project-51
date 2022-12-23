import os
import requests
import logging
from page_loader import url
from page_loader.html import get_resources
from progress.bar import ChargingBar


def download_link(url):
    response = requests.get(url)
    return response


def save_content(file_path, content):
    if isinstance(content, bytes):
        with open(file_path, 'wb+') as downloaded_file:
            downloaded_file.write(content)
    else:
        with open(file_path, 'w') as downloaded_file:
            downloaded_file.write(content)


def download(link, actual_path=os.getcwd()):
    file_name = url.make_file_name(link)
    file_path = os.path.join(actual_path, file_name)
    dir_name = url.make_dir_name(link)
    dir_path = os.path.join(actual_path, dir_name)
    response = download_link(link)
    resources, new_html = get_resources(response, link, dir_name)
    save_content(file_path, new_html)
    if len(resources) != 0:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        download_content(resources, dir_path)
    return file_path


def download_content(resources, path):
    bar_len = len(resources)
    with ChargingBar('Downloading', max=bar_len, suffix='%(percent)d%%') as bar:
        for resource in resources:
            bar.next()
            content_response = download_link(resource)
            path_content = os.path.join(path, url.make_file_name(resource))
            save_content(path_content, content_response.content)