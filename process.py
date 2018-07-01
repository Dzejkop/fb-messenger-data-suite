#!/usr/bin/env python3
import argparse
import json
import csv

from message_count import message_count

def filter_data_by_people(data, people):
    return {key: value for key, value in data.items() if key in people}

def save_results(data, out_format, verbose, csv_delimiter, output_filepath = None):
    out_file = output_filepath
    if not out_file:
        if out_format in ['json', 'pretty-json']:
            out_file = 'out.json'
        elif out_format in ['csv']:
            out_file = 'out.csv'
        else:
            raise Exception('Unsupported output format')

    if verbose:
        print('Saving data to {}'.format(out_file))

    with open(out_file, 'w') as output_file:
        if out_format == 'json':
            json.dump(data, output_file)
        elif out_format == 'pretty-json':
            json.dump(data, output_file, indent=True)
        elif out_format == 'csv':
            csv_writer = csv.writer(output_file, delimiter=csv_delimiter)
            for row in data:
                csv_writer.writerow(row)
        else:
            raise Exception('Unsupported output format')

def main():
    parser = argparse.ArgumentParser(epilog='~~ From Dzejkop with Love <3 ~~')

    parser.add_argument('data_source', metavar='SOURCE', type=str, help='data source file.')
    parser.add_argument('mode', choices=['message-count'], help='mode of operation')
    parser.add_argument('--output', type=str, help='output file path, by default is equal to "out" with extension matching the format')
    parser.add_argument('--group_by', choices=['day', 'week', 'month'], help='grouping of data if applicable, default is month', default='month')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--filter', metavar='PERSON', type=str, nargs='*', help='parse only select people')
    parser.add_argument('--output-format', choices=['pretty-json', 'json', 'csv'], default='csv')
    parser.add_argument('--csv-delimiter', default=',', help='"," by default')
    
    args = parser.parse_args()

    if args.verbose:
        print ('Running with args {}'.format(args))

    if args.verbose:
        print ('Reading data from {}'.format(args.data_source))

    data = {}
    with open(args.data_source, 'r') as source_file:
        data = json.load(source_file)

    if args.filter:
        if args.verbose:
            print('Filtering by people {}'.format(args.filter))
        data = filter_data_by_people(data, args.filter)

    result = None
    if args.mode == 'message-count':
        result = message_count(data, args.group_by, args.verbose)
    
    save_results(result, args.output_format, args.verbose, args.csv_delimiter, args.output)

if __name__ == '__main__':
    main()