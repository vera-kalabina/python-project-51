from page_loader import download
from page_loader import cli


def main():
    args = cli.parse()

    download(args.url, args.output)


if __name__ == '__main__':
    main()
