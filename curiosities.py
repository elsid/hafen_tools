#!/usr/bin/env python3

from argparse import ArgumentParser, FileType
from common import parse_html, create_database_table
from sys import stdin


def main():
    args = parse_args()
    columns, rows = parse_html(args.html.read(), key_rename, 'table:first')
    create_database_table('curiosities', columns, rows)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('html', type=FileType(), nargs='?', default=stdin)
    return parser.parse_args()


def key_rename(value):
    return (value
            .replace(' smwtype_num', '')
            .replace(' smwtype_txt', '')
            .replace(' smwtype_wpg', '')
            .replace('-(Real-Hours)', '')
            .replace('%', '')
            .replace('-', '_')
            .replace('/', '_per_')
            .lower())


if __name__ == '__main__':
    main()
