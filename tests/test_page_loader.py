import pytest

from page_loader.download import download
from page_loader import url


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
def test_to_filename(link, expected):

    actual = url.convert_name(link)
    assert actual == expected