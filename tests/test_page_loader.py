import pytest
import os
import requests_mock
import stat
from tempfile import TemporaryDirectory
from requests.exceptions import Timeout, ConnectionError, HTTPError


from page_loader.download import download, download_link
from page_loader import url
from page_loader.html import get_resources

URL = 'https://ru.hexlet.io'
URL_IMG = 'https://ru.hexlet.io/professions/python.png'
URL_CSS = 'https://ru.hexlet.io/assets/application.css'
URL_JS = 'https://ru.hexlet.io/packs/js/runtime.js'


RAW = 'tests/fixtures/raw.html'
IMG = 'tests/fixtures/image.png'
HTML = 'tests/fixtures/expected.html'
CSS = 'tests/fixtures/styles.css'
JS = 'tests/fixtures/script.js'


DIRECTORY = 'ru-hexlet-io_files'
EXPECTED_HTML = 'ru-hexlet-io.html'
EXPECTED_IMG = os.path.join(DIRECTORY, 'ru-hexlet-io-professions-python.png')
EXPECTED_CSS = os.path.join(DIRECTORY, 'ru-hexlet-io-assets-application.css')
EXPECTED_JS = os.path.join(DIRECTORY, 'ru-hexlet-io-packs-js-runtime.js')


def read(file, binary=False):
    if not binary:
        with open(file, 'r') as f:
            return f.read()
    with open(file, 'rb') as file:
        return file.read()


@pytest.mark.parametrize('link, expected', [
    (
        'https://ru.hexlet.io',
        'ru-hexlet-io.html'
    ),
    (
        'https://hexlet.io',
        'hexlet-io.html'
    ),
    (
        'https://ru.hexlet.io/professions/python.js',
        'ru-hexlet-io-professions-python.js'
    )
])
def test_make_filename(link, expected):
    actual = url.make_filename(link)
    assert actual == expected


@pytest.mark.parametrize('link, expected', [
    (
        'https://ru.hexlet.io',
        'ru-hexlet-io_files'
    ),
    (
        'https://hexlet.io',
        'hexlet-io_files'
    ),
    (
        'https://ru.hexlet.io/professions/python.js',
        'ru-hexlet-io-professions-python_files'
    )
])
def test_make_dirname(link, expected):
    actual = url.make_dirname(link)
    assert actual == expected


def test_downloads():
    html_raw = read(RAW)
    html_expected = read(HTML)
    image = read(IMG, binary=True)
    css = read(CSS, binary=True)
    js = read(JS, binary=True)
    with requests_mock.Mocker() as m, TemporaryDirectory() as tmpdir:
        m.get(URL, text=html_raw)
        m.get(URL_IMG, content=image)
        m.get(URL_CSS, content=css)
        m.get(URL_JS, content=js)
        download(URL, tmpdir)

        html_path = os.path.join(tmpdir, EXPECTED_HTML)
        img_path = os.path.join(tmpdir, EXPECTED_IMG)
        css_path = os.path.join(tmpdir, EXPECTED_CSS)
        js_path = os.path.join(tmpdir, EXPECTED_JS)

        actual_html = read(html_path)
        assert actual_html == html_expected

        actual_img = read(img_path, binary=True)
        assert actual_img == image

        actual_css = read(css_path, binary=True)
        assert actual_css == css

        actual_js = read(js_path, binary=True)
        assert actual_js == js

        actual_path = os.path.join(tmpdir, DIRECTORY)
        assert len(os.listdir(actual_path)) == 3


def test_get_resources():
    html_raw = read(RAW)
    html_expected = read(HTML)

    with requests_mock.Mocker() as m:
        m.get(URL, text=html_raw)
        response = download_link(URL)
        resources, processed_html = get_resources(response, URL, DIRECTORY)
        assert processed_html == html_expected
        expected_resources = ['https://ru.hexlet.io/assets/application.css',
                              'https://ru.hexlet.io/professions/python.png',
                              'https://ru.hexlet.io/packs/js/runtime.js']

        assert resources == expected_resources


@pytest.mark.parametrize('errors', [
    Timeout, ConnectionError, HTTPError])
def test_requests(errors):
    with requests_mock.Mocker() as m, TemporaryDirectory() as tmpdir:
        m.get(URL, exc=errors)
        with pytest.raises(Exception):
            assert download(URL, tmpdir)


def test_permissions_and_file_not_found(requests_mock, tmpdir):
    requests_mock.get(URL)
    os.chmod(tmpdir, stat.S_IRUSR)
    with pytest.raises(Exception) as permission_error:
        assert download(URL, tmpdir) == permission_error
    with pytest.raises(Exception) as file_not_found:
        assert download(URL, 'not_file') == file_not_found
