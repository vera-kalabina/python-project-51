from page_loader import download
from page_loader import cli

import sys


def main():
    args = cli.parse()

    try:
        download(args.url, args.output)
    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    main()
