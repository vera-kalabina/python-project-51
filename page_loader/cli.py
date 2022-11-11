import argparse
import os


def parse():
    parser = argparse.ArgumentParser(
        description='Downloads web-page to the specified exist directory',
        prog='page-loader'
    )
    parser.add_argument('-o', '--output', type=str, default=os.getcwd())
    parser.add_argument('url', type=str)
    return parser.parse_args()
