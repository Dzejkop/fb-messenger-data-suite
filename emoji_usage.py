import argparse
from emoji import UNICODE_EMOJI

def subparser(subparsers):
    parser = subparsers.add_parser('emoji-usage')

    parser.add_argument('person', type=str, help='Name of person')
    parser.add_argument('--split-by-person', action='store_true')

    parser.set_defaults(func=analyze_emoji_usage)
    return parser

def find_emoji(s):
    all_emojis = UNICODE_EMOJI
    return {emoji: s.count(emoji) if emoji in s else 0 for emoji in all_emojis}

def merge_emoji_usage(list_of_usages):
    usages = {}

    for entry in list_of_usages:
        for k in entry.keys():
            if k in usages:
                usages[k] += entry[k]
            else:
                usages[k] = entry[k]
    
    return usages

def find_convo_with_person(messages_by_person, person, verbose):
    if verbose:
        print ('Analyzing emoji usage for {}'.format(person))

    if not person in messages_by_person:
        print ('Failed to find {} in {}'.format(person, messages_by_person.keys()))

    return messages_by_person[person]

def analyze_emoji_usage(messages_by_person, args):
    convo = find_convo_with_person(messages_by_person, args.person, args.verbose)

    people = list(set(map(lambda msg: msg['sender_name'], convo)))

    messages_by_sender = { person: list(filter(lambda msg: msg['sender_name'] == person, convo)) for person in people }

    message_contents_by_sender = { person: list(map(lambda msg: msg['content'], messages)) for person, messages in messages_by_sender.items() }

    emoji_usages_by_sender = { person: merge_emoji_usage(map(lambda msg: find_emoji(msg), messages)) for person, messages in message_contents_by_sender.items() }

    total_emoji_usage = merge_emoji_usage(emoji_usages_by_sender.values())

    total_emoji_usage = {k: v for k, v in total_emoji_usage.items() if v > 0}

    for_each_emoji = {emoji: [total_emoji_usage[emoji]] + [individual_usage[emoji] for individual_usage in emoji_usages_by_sender.values()] for emoji in total_emoji_usage.keys()}

    header = ['Emoji', 'Total'] + people
    rows = [[emoji] + usage for emoji, usage in for_each_emoji.items()]

    return [header] + rows
