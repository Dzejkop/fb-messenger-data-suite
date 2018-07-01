#!/usr/bin/env python3
from pathlib import Path
from copy import copy
import json
import argparse
from itertools import islice

def find_message_files(working_dir, fname, verbose):
    if verbose:
        print('Looking for {} files in {}'.format(fname, working_dir))

    pathlist = Path(working_dir).glob('**/{}'.format(fname))
    return [str(path) for path in pathlist]

def read_messages_file(path, verbose):
    if (verbose):
        print('Reading data from {}'.format(path))
    
    with open(path) as f:
        return json.load(f)

def merge_conversations(conversations, is_including_groups, is_ignoring_abandoned, verbose):
    if verbose:
        print ('Merging conversations')
    
    return { convo['participants'][0]: convo['messages'] for convo in conversations}

def filter_conversations(conversations, is_including_groups, is_ignoring_abandoned, verbose):
    convos = copy(conversations)
    if is_ignoring_abandoned:
        if verbose:
            print('Filtering out abandoned conversations')
        convos = filter(lambda convo: convo['is_still_participant'], convos)

    if not is_including_groups:
        if verbose:
            print('Filtering out group conversations')
        convos = filter(lambda convo: 'participants' in convo and len(convo['participants']) == 1, convos)

    if verbose:
        print('Filtering out invaild conversations')
        
    convos = filter(lambda convo: convo['participants'][0], convos)

    return convos

def main():
    parser = argparse.ArgumentParser(epilog='~~ From Dzejkop with Love <3 ~~')

    parser.add_argument('dir', metavar='DIR', type=str, help='Directory too look for messages.json files')
    parser.add_argument('-o', '--output', type=str, help='Output file name, default is merged.json', default='merged.json')
    parser.add_argument('--fname', type=str, help='Name of the messages file to look for, default is message.json', default='message.json')
    parser.add_argument('--include-groups', action='store_true', help='Ignore group conversations')
    parser.add_argument('--parse-abandoned', action='store_true', help='Parse the conversations that you left')
    parser.add_argument('--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('--pretty', action='store_true', help='Pretty format the output file')

    args = parser.parse_args()
    if args.verbose:
        print('Running with args {}'.format(args))

    if args.include_groups:
        raise Exception('Group conversations are currenlty not supported.')

    message_files = find_message_files(args.dir, args.fname, args.verbose)
    conversations = [read_messages_file(path, args.verbose) for path in message_files]
    conversations = filter_conversations(conversations, args.include_groups, not args.parse_abandoned, args.verbose)
    merged = merge_conversations(conversations, args.include_groups, not args.parse_abandoned, args.verbose)

    if args.verbose:
        print ('Saving merged conversations to {}'.format(args.output))
    
    with open(args.output, 'w') as output_file:
        json.dump(merged, output_file, indent=args.pretty)

if __name__ == '__main__':
    main()