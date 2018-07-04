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

def merge_conversations(conversations, is_ignoring_abandoned, verbose):
    if verbose:
        print ('Merging conversations')
    
    return { ', '.join(convo['participants']): convo['messages'] for convo in conversations}

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

    return [c for c in convos if 'participants' in c]

def strip_message(msg, verbose):
    if verbose:
        print ('Stripping {}'.format(msg))

    if not ('sender_name' in msg and 'timestamp' in msg and 'content' in msg):
        return None

    return {'sender_name': msg['sender_name'], 'timestamp': msg['timestamp'], 'content': msg['content']}

def strip_conversation(conversation, verbose):
    if verbose:
        print ('Stripping conversation with {}'.format(conversation['participants']))

    strip = lambda msg: strip_message(msg, verbose)

    convo = copy(conversation)

    convo['messages'] = list(filter(lambda msg: msg != None, map(strip, convo['messages'])))

    return convo

def strip_conversations(conversations, verbose):
    if verbose:
        print ('Stripping conversations')

    strip = lambda convo: strip_conversation(convo, verbose)

    return list(map(strip, conversations))

def encode_decode_conversations(conversations, enc, verbose):
    convos = copy(conversations)
    if verbose:
        print ('Performing .encode({}).decode(utf-8) for all contents and names'.format(enc))
    
    enc_dec = lambda content: content.encode(enc).decode('utf-8')

    for convo in convos:
        if 'participants' in convo:
            convo['participants'] = [enc_dec(p) for p in convo['participants']]
            
        for msg in convo['messages']:
            if not msg:
                continue

            if 'sender_name' in msg:
                sname = msg['sender_name']
                msg['sender_name'] = enc_dec(sname)

                if verbose:
                    print ('{} -> {}'.format(sname, msg['sender_name']))

            if 'content' in msg:
                content = msg['content']
                msg['content'] = enc_dec(content)

                if verbose:
                    print ('{} -> {}'.format(content, msg['content']))
    
    return convos

def main():
    parser = argparse.ArgumentParser(epilog='~~ From Dzejkop with Love <3 ~~')

    parser.add_argument('dir', metavar='DIR', type=str, help='Directory too look for messages.json files')
    parser.add_argument('-o', '--output', type=str, help='Output file name, default is merged.json', default='merged.json')
    parser.add_argument('--fname', type=str, help='Name of the messages file to look for, default is message.json', default='message.json')
    parser.add_argument('--include-groups', action='store_true', help='Ignore group conversations. Groups will be parsed as separate conversations where the conversation name is the concatenation of participant names.')
    parser.add_argument('--parse-abandoned', action='store_true', help='Parse the conversations that you left')
    parser.add_argument('--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('--pretty', action='store_true', help='Pretty format the output file')
    parser.add_argument('--encode-decode', metavar='ENC', help='Perform the .encode(ENC).decode(utf-8) step for content of all messages.')
    parser.add_argument('--skip-strip', action='store_true', help='Skip stripping of unrelevant data.')

    args = parser.parse_args()
    if args.verbose:
        print('Running with args {}'.format(args))

    message_files = find_message_files(args.dir, args.fname, args.verbose)
    conversations = [read_messages_file(path, args.verbose) for path in message_files]

    conversations = filter_conversations(conversations, args.include_groups, not args.parse_abandoned, args.verbose)

    if not args.skip_strip:
        conversations = strip_conversations(conversations, args.verbose)

    if args.encode_decode:
        conversations = encode_decode_conversations(conversations, args.encode_decode, args.verbose)

    merged = merge_conversations(conversations, not args.parse_abandoned, args.verbose)

    if args.verbose:
        print ('Saving merged conversations to {}'.format(args.output))
    
    with open(args.output, 'w', encoding='utf-8') as output_file:
        json.dump(merged, output_file, indent=args.pretty, ensure_ascii=False)

if __name__ == '__main__':
    main()