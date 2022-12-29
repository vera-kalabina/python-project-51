import os
import requests
from page_loader import url
from page_loader.html import get_resources
from progress.bar import ChargingBar
from page_loader.logger import log_info, log_error


def download_link(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def save_content(file_path, content):
    if isinstance(content, bytes):
        with open(file_path, 'wb+') as downloaded_file:
            downloaded_file.write(content)
    else:
        with open(file_path, 'w') as downloaded_file:
            downloaded_file.write(content)


def download(link, actual_path=os.getcwd()):
    log_info.info(f'Requested url: {link}')
    log_info.info(f'Output path: {actual_path}')
    file_name = url.make_filename(link)
    file_path = os.path.join(actual_path, file_name)
    dir_name = url.make_dirname(link)
    dir_path = os.path.join(actual_path, dir_name)
    response = download_link(link)
    resources, new_html = get_resources(response, link, dir_name)
    save_content(file_path, new_html)
    if len(resources) != 0:
        log_info.info(f'Write HTML file: {file_path}')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        download_content(resources, dir_path)
        log_info.info(f'Page was downloaded as "{file_name}"')
    return file_path


def download_content(resources, path):
    len_ = len(resources)
    with ChargingBar('Downloading:', max=len_, suffix='%(percent)d%%') as bar:
        for resource in resources:
            bar.next()
            try:
                content_response = download_link(resource)
            except requests.exceptions.RequestException as error:
                log_error.error(error)
                continue
            path_content = os.path.join(path, url.make_filename(resource))
            save_content(path_content, content_response.content)
