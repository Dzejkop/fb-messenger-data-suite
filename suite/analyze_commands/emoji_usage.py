import argparse
from emoji import UNICODE_EMOJI
from copy import copy

DESC = """
Emoji usage by person in conversation.

Returns 3 rows of data: Emoji, person A usage of given emoji, person B usage of given emoji.
"""

def subparser(subparsers):
    parser = subparsers.add_parser('emoji-usage', description=DESC)

    parser.add_argument('person', type=str, help='Name of person')

    parser.set_defaults(func=analyze_emoji_usage)
    return parser

def find_emoji_in_str(s):
    all_emojis = UNICODE_EMOJI
    return {emoji: s.count(emoji) for emoji in all_emojis if emoji in s}

def emoji_set_from_str(s):
    return EmojiSet(find_emoji_in_str(s))

class EmojiSet:
    def __init__(self, data):
        self.data = data

    def add(self, other):
        usages = copy(self.data)

        for k, v in other.data.items():
            if k in usages:
                usages[k] += v
            else:
                usages[k] = v
        
        return EmojiSet(usages)

    def val(self, emoji):
        return self.data[emoji] if emoji in self.data else 0

class EmojiUsage(object):
    def __init__(self, contents):
        emoji_usages = map(emoji_set_from_str, contents)
        self.usage = EmojiSet({})

        for usage in emoji_usages:
            self.usage = self.usage.add(usage)

    def of_emoji(self, emoji):
        return self.usage.val(emoji)

    def emojis(self):
        return self.usage.data.keys()

def analyze_emoji_usage(messages, args):
    convo = messages.conversation(args.person)

    people = convo.people()

    messages_by_sender = { person: [msg.content() for msg in convo.messages_of(person)] for person in people }

    emoji_usages_by_sender = { person: EmojiUsage(messages) for person, messages in messages_by_sender.items() }

    all_emojis_used_by_senders = []
    for emoij_set in emoji_usages_by_sender.values():
        all_emojis_used_by_senders += list(emoij_set.emojis())

    all_emojis_used_by_senders = set(all_emojis_used_by_senders)

    for_each_emoji = {emoji: [individual_usage.of_emoji(emoji) for individual_usage in emoji_usages_by_sender.values()] for emoji in all_emojis_used_by_senders}

    header = ['Emoji'] + list(people)
    rows = [[emoji] + usage for emoji, usage in for_each_emoji.items()]

    return [header] + rows
