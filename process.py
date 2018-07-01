#!/usr/bin/env python3
import argparse
import json
import csv
from datetime import date
from itertools import groupby
from functools import reduce

def to_month(ts):
    d = date.fromtimestamp(ts)
    return date(d.year, d.month, 1)

def month_range(start_month, end_month):
    date_range = [start_month]

    for year in range(start_month.year, end_month.year + 1):
        for month in range(1, 13):
            new_date = date(year, month, 1)
            if new_date > start_month and new_date <= end_month:
                date_range.append(new_date)
    
    return date_range

def message_count_raw(messages_by_person, grouping, verbose):
    if grouping != 'month':
        raise Exception('Only month grouping is supported now')

    sorted_messages_by_person = {person: sorted(messages, key=lambda msg: msg['timestamp']) 
        for person, messages in messages_by_person.items()}

    grouped_messages_by_person = {person: groupby(messages, lambda msg: to_month(msg['timestamp']))
        for person, messages in sorted_messages_by_person.items()}

    messages_count_by_person_by_month = {person: {month: len(list(messages)) for month, messages in by_month} 
        for person, by_month in grouped_messages_by_person.items()}

    return messages_count_by_person_by_month

def message_count(messages_by_person, grouping, verbose, out_format='csv'):
    raw = message_count_raw(messages_by_person, grouping, verbose)
    all_dates = sorted(reduce(lambda x,y :x + y, ([date for date, count in entries.items()] for p, entries in raw.items())))

    oldest_date = min(all_dates)
    newest_date = max(all_dates)

    date_range = month_range(oldest_date, newest_date)

    data = {person: [msg_counts[time] if time in msg_counts else 0 for time in date_range] for person, msg_counts in raw.items()}
    header = ['Person'] + [str(d) for d in date_range]

    ret = [header] + [[person] + msg_counts for person, msg_counts in data.items()]
    return ret

def filter_data_by_people(data, people):
    return {key: value for key, value in data.items() if key in people}

def save_results(data, out_format, verbose, output_filepath = None):
    out_file = output_filepath
    if not out_file:
        if out_format in ['json', 'pretty-json']:
            out_file = 'out.json'
        elif out_format in ['csv']:
            out_file = 'out.csv'
        else:
            raise Exception('Unsupported output format')

    if verbose:
        print('Saving data to {}'.format(args.output))
    with open(out_file, 'w') as output_file:
        if out_format == 'json':
            json.dump(result, output_file)
        elif out_format == 'pretty-json':
            json.dump(result, output_file, indent=True)
        elif out_format == 'csv':
            csv_writer = csv.writer(output_file, delimiter=args.csv_delimiter)
            for row in result:
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

if __name__ == '__main__':
    main()