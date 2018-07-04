#!/usr/bin/env python3
import argparse
import json
import csv
import sys

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

    parser.add_argument('--from-file', metavar='SOURCE', type=str, help='data source file.')
    parser.add_argument('--from-std-in', action='store_true', help='Read data from stdin instead of source file.')
    parser.add_argument('--output', type=str, help='output file path, by default is equal to "out.csv" with extension matching the format')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--filter', metavar='PERSON', type=str, nargs='*', help='parse only select people')
    parser.add_argument('--csv-delimiter', default=',', help='"," by default')
    parser.add_argument('--to-std-out', action='store_true', help='Send output into stdout instead of saving to file.')

    subparsers = parser.add_subparsers(help='Available commands')
    message_count.subparser(subparsers)
    emoji_usage.subparser(subparsers)
    message_analysis.subparser(subparsers)

    args = parser.parse_args()

    if args.verbose:
        print ('Running with args {}'.format(args))

    data = {}
    if args.from_std_in:
        if args.verbose:
            print ('Reading data from std in')
        data = json.load(sys.stdin)
    elif args.from_file:
        if args.verbose:
            print ('Reading data from {} file'.format(args.from_file))
        with open(args.from_file, encoding='utf-8') as source_file:
           data = json.load(source_file)
    else:
        raise Exception('No data source specified. Use either "--from-std-in" or "--data FILENAME"')

    if args.filter:
        if args.verbose:
            print('Filtering by people {}'.format(args.filter))
        data = filter_data_by_people(data, args.filter)

    data = Messages(data)

    result = args.func(data, args)
    
    if args.to_std_out:
        for row in result:
            print (str(args.csv_delimiter).join(map(lambda x: str(x), row)))
    else:
        save_results(result, args.verbose, args.csv_delimiter, args.output)

if __name__ == '__main__':
    main()