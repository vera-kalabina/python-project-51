install:
		poetry install

build:
		poetry build

package-install:
		python3 -m pip install --user --force-reinstall dist/*.whl

lint:
		poetry run flake8 page_loader

test:
		poetry run pytest

test-cov:
		poetry run pytest --cov=page_loader --cov-report xml
