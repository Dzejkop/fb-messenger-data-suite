from itertools import groupby
from datetime import date
from functools import reduce

def subparser(subparsers):
    parser = subparsers.add_parser('message-count', description='Message count by grouping')

    parser.add_argument('--group-by', choices=['day', 'week', 'month'], help='grouping of data if applicable, default is month', default='month')

    parser.set_defaults(func=message_count)
    return parser

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

    conversations = messages_by_person.conversations()

    timestamps_by_person = {convo.person(): [msg.timestamp() for msg in convo.messages()] for convo in conversations}
    timestamps_by_person = {person: sorted(timestamps) for person, timestamps in timestamps_by_person.items()}

    grouped_messages_by_person = {person: groupby(timestamps, lambda ts: to_month(ts))
        for person, timestamps in timestamps_by_person.items()}

    messages_count_by_person_by_month = {person: {month: len(list(messages)) for month, messages in by_month} 
        for person, by_month in grouped_messages_by_person.items()}

    return messages_count_by_person_by_month

def message_count(messages_by_person, args):
    raw = message_count_raw(messages_by_person, args.group_by, args.verbose)
    all_dates = sorted(reduce(lambda x,y :x + y, ([date for date, count in entries.items()] for p, entries in raw.items())))

    oldest_date = min(all_dates)
    newest_date = max(all_dates)

    date_range = month_range(oldest_date, newest_date)

    data = {person: [msg_counts[time] if time in msg_counts else 0 for time in date_range] for person, msg_counts in raw.items()}
    header = [''] + [str(d) for d in date_range]

    ret = [header] + [[person] + msg_counts for person, msg_counts in data.items()]
    return ret