from datetime import datetime
import time
from itertools import groupby

def subparser(subparsers):
    parser = subparsers.add_parser('message-analysis')

    parser.add_argument('person', type=str, help='Name of person')
    parser.add_argument('grouping', choices=['hour-of-day', 'day-of-the-week'])

    parser.set_defaults(func=analysis)

    return parser

class Grouping:
    def __init__(self, mode):
        if mode == 'hour-of-day':
            self.func = self.group_by_hour_of_day
            self.keys = self.hours_of_day
        elif mode == 'day-of-the-week':
            self.func = self.group_by_day_of_the_week
            self.keys = self.days_of_the_week
        else:
            raise Exception('Unsupported grouping type')

    def group_by_hour_of_day(self, dt):
        return dt.hour

    def group_by_day_of_the_week(self, dt):
        return dt.weekday()

    def days_of_the_week(self):
        return [x for x in range(7)]

    def hours_of_day(self):
        return [x for x in range(24)]

    def over_datetime(self, dt):
        return self.func(dt)

    def over_timestamp(self, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        return self.over_datetime(dt)

def analysis(messages, args):
    convo = messages.conversation(args.person)
    grouping = Grouping(args.grouping)
    people = convo.people()

    timestamps_by_person = {person: [msg.timestamp() for msg in convo.messages_of(person)] for person in people}
    grouping_values = {person: [grouping.over_timestamp(ts) for ts in timestamps] for person, timestamps in timestamps_by_person.items()}
    grouping_values = {k: sorted(v) for k, v in grouping_values.items()}

    grouped = {person: groupby(v) for person, v in grouping_values.items()}

    unpacked = {person: {k: len(list(values)) for k, values in gp} for person, gp in grouped.items()}

    rows = [[k] + [x[k] if k in x else 0 for x in unpacked.values()] for k in grouping.keys()]

    header = ['Time of day'] + list(people)

    return [header] + rows