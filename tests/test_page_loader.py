import pytest

from page_loader.download import download
from page_loader import url

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
def test_make_file_name(link, expected):

    actual = url.make_file_name(link)
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
def test_make_dir_name(link, expected):

    actual = url.make_dir_name(link)
    assert actual == expected