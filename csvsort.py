#!/usr/bin/env python
'''
  filter on column names
'''

import argparse
import collections
import csv
import logging
import sys

def safe_float(v, default):
  if v in ('nan', 'inf'):
    return default

  try:
    return float(v)
  except:
    return default

def process(reader, col, numeric, descending, delimiter):
    '''
        read in csv file, look at the header of each
        apply rule to each field (in order)
    '''
    logging.info('reading from stdin...')

    lines = []
    for row in reader:
      lines.append(row)

    out = csv.DictWriter(sys.stdout, delimiter=delimiter, fieldnames=reader.fieldnames)
    out.writeheader()

    if numeric:
      sorted_lines = sorted(lines, key=lambda k: safe_float(k[col], -1e100))
    else:
      sorted_lines = sorted(lines, key=lambda k: k[col])

    if descending:
      sorted_lines = sorted_lines[::-1]

    for row in sorted_lines:
      out.writerow(row)

    logging.info('done')

def main():
    '''
        parse command line arguments
    '''
    parser = argparse.ArgumentParser(description='Update CSV column values')
    parser.add_argument('--col', required=True, help='column to sort on')
    parser.add_argument('--delimiter', default=',', help='file delimiter')
    parser.add_argument('--numeric', action='store_true', help='numeric sort')
    parser.add_argument('--desc', action='store_true', help='descending')
    parser.add_argument('--verbose', action='store_true', help='more logging')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    process(csv.DictReader(sys.stdin, delimiter=args.delimiter), args.col, args.numeric, args.desc, args.delimiter)

if __name__ == '__main__':
    main()