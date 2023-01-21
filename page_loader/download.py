import os
import requests
import logging
from page_loader import url
from page_loader.html import get_resources
from progress.bar import ChargingBar


logging.basicConfig(level=logging.INFO)


def download_link(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logging.error(error)
        logging.info(f'Failed.Check your internet connection or url:{url}')
        raise Exception(error)
    return response


def save_content(file_path, content):
    try:
        if isinstance(content, bytes):
            with open(file_path, 'wb+') as downloaded_file:
                downloaded_file.write(content)
        else:
            with open(file_path, 'w') as downloaded_file:
                downloaded_file.write(content)
    except PermissionError as error1:
        logging.error(error1)
        logging.info(f'Denied access to the file {file_path}')
        raise Exception(error1)
    except OSError as error2:
        logging.error(error2)
        logging.info(f'Unable to save to the file {file_path}')
        raise Exception(error2)


def download(link, actual_path=os.getcwd()):
    logging.info(f'Requested url: {link}')
    logging.info(f'Output path: {actual_path}')
    file_name = url.make_filename(link)
    file_path = os.path.join(actual_path, file_name)
    dir_name = url.make_dirname(link)
    dir_path = os.path.join(actual_path, dir_name)
    response = download_link(link)
    resources, new_html = get_resources(response, link, dir_name)
    save_content(file_path, new_html)
    if len(resources) != 0:
        logging.info(f'Write HTML file: {file_path}')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        download_content(resources, dir_path)
        logging.info(f'Page was downloaded as "{file_name}"')
    return file_path


def download_content(resources, path):
    len_ = len(resources)
    with ChargingBar('Downloading:', max=len_, suffix='%(percent)d%%') as bar:
        for resource in resources:
            bar.next()
            try:
                content_response = download_link(resource)
            except requests.exceptions.RequestException as error:
                logging.error(error)
                continue
            path_content = os.path.join(path, url.make_filename(resource))
            save_content(path_content, content_response.content)
