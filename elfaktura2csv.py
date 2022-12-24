#! /usr/local/bin/python3.11

import os
import re
import sys
from tika import parser


DELIMITER = ';'
HEADER = ['Anläggnings ID', 'År', 'Månad', 'Förbrukning (kWh)', 'Pris ex. moms (öre/kWh)', 'Rabatt (öre/kWh)']


def write_csv(vals):
    print(DELIMITER.join(vals))


def parse_groups(regex, text):
    m = re.search(regex, text)
    if m:
        return m.groups()
    return None


def parse_fortum(content):
    groups = parse_groups(r'[Anläggnings|Anl] id:? ([\d\s]+)\n', content)
    anlaggnings_id = groups[0]

    groups = parse_groups(r'[Ff]ör perioden \d (\w+) ([\d]+)', content)
    month, year = groups[0], groups[1]

    regexes = [
        r'(\n[\w]+) \d\d\d\d\-\d\d\-\d\d \- \d\d\d\d\-\d\d\-\d\d ([\d\s]+) kWh ([\d,-]+) öre\/kWh',  # new style
        r'(\n[\w]+) ([\d\s]+) kWh ([\d,-]+) öre\/kWh',  # old style
        r'(\n[\w]+) \d+ \w+\-\d+ ([\d\s]+) kWh ([\d,-]+) öre\/kWh'  # different style
    ]
    parsed = {}
    for regex in regexes:
        res = re.findall(regex, content)
        if res:  #[('\nEl', '986', '230,36'), ('\nRabatt', '986', '-4,00')]
            for r in res:
                item, kwh, cost = r[0].strip(), r[1], r[2]
                parsed[item] = (kwh, cost)

    kwh, cost = parsed['El']
    discount = parsed.get('Rabatt', ('', ''))[1]

    row = [anlaggnings_id, year, month, kwh, cost, discount]
    write_csv(map(str.strip, row))


def parse_pdf(fpath):
    if not os.path.splitext(fpath)[1] == '.pdf':
        print(f'Error. File "{fpath}" is not a PDF file')
        return

    try:
        raw = parser.from_file(fpath, 'http://127.0.0.1:9998/tik', xmlContent=True)

        # Figure out what company this PDF is from
        if 'Fortum Markets AB' in raw['content']:
            parse_fortum(raw['content'])
        else:
            print(f'PDF {os.path.basename(fpath)} is not a supported vendor/company.')
    except Exception as e:
        print(f'Failed to parse PDF file "{fpath}"')
        print(e)


def parse_dir(dirpath):
    for fname in os.listdir(dirpath):
        parse_pdf(os.path.join(fpath, fname))


if __name__ == '__main__':
    try:
        fpath = sys.argv[1]
    except:
        sys.exit(f'Usage: {sys.argv[0]} <PDF file or path to directory with PDFs>')

    write_csv(HEADER)

    if os.path.isdir(fpath):
        parse_dir(fpath)
    elif os.path.isfile(fpath):
        parse_pdf(fpath)
    else:
        sys.exit('Must provide path to file or directory')
