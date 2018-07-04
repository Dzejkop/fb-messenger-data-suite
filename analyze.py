#!/usr/bin/env python3
import argparse
import json
import csv

from analyze_commands import message_count
from analyze_commands import emoji_usage
from analyze_commands import message_analysis

from common import Messages

def filter_data_by_people(data, people):
    return {key: value for key, value in data.items() if key in people}

def save_results(data, verbose, csv_delimiter, output_filepath = None):
    out_file = output_filepath if output_filepath else 'out.csv'

    if verbose:
        print('Saving data to {}'.format(out_file))

    with open(out_file, 'w', encoding='utf-8') as output_file:
        csv_writer = csv.writer(output_file, delimiter=csv_delimiter)
        for row in data:
            csv_writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(epilog='~~ From Dzejkop with Love <3 ~~')

    parser.add_argument('data_source', metavar='SOURCE', type=str, help='data source file.')
    parser.add_argument('--output', type=str, help='output file path, by default is equal to "out.csv" with extension matching the format')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--filter', metavar='PERSON', type=str, nargs='*', help='parse only select people')
    parser.add_argument('--csv-delimiter', default=',', help='"," by default')

    subparsers = parser.add_subparsers(help='Available commands')
    message_count.subparser(subparsers)
    emoji_usage.subparser(subparsers)
    message_analysis.subparser(subparsers)

    args = parser.parse_args()

    if args.verbose:
        print ('Running with args {}'.format(args))

    if args.verbose:
        print ('Reading data from {}'.format(args.data_source))

    data = {}
    with open(args.data_source, encoding='utf-8') as source_file:
        data = json.load(source_file)

    if args.filter:
        if args.verbose:
            print('Filtering by people {}'.format(args.filter))
        data = filter_data_by_people(data, args.filter)

    data = Messages(data)

    result = args.func(data, args)
    
    save_results(result, args.verbose, args.csv_delimiter, args.output)

if __name__ == '__main__':
    main()