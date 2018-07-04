# Facebook Messenger Data Analysis Suite
The aim of this project is to provide a data visualization/analysis suite for conversations from facebook's messenger.

I'm trying to create a system separated into 3 modules:
## Data preparation
Takes the raw archive data and processes it to a format more suitable for analysis and visualization.

Default method is to use the `prepare.py` script:
```
usage: prepare.py [-h] [-o OUTPUT] [--fname FNAME] [--include-groups]
                  [--parse-abandoned] [--verbose] [--pretty]
                  [--encode-decode ENC] [--skip-strip]
                  DIR

positional arguments:
  DIR                   Directory too look for messages.json files

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name, default is merged.json
  --fname FNAME         Name of the messages file to look for, default is
                        message.json
  --include-groups      Ignore group conversations
  --parse-abandoned     Parse the conversations that you left
  --verbose             Verbose mode
  --pretty              Pretty format the output file
  --encode-decode ENC   Perform the .encode(ENC).decode(utf-8) step for
                        content of all messages.
  --skip-strip          Skip stripping of unrelevant data.
```

However any method is applicable as long as the end result is a json file of the following format:
```json
{
    "John Doe": [ 
        {
            "sender_name": "John Doe",
            "content": "Lorem ipsum...",
            "timestamp": 1526397926
        },
        {
            "sender_name": "Jane doe",
            "content": "...dolor sit amet...",
            "timestamp": 1526397752
        },
        ...
    ],
    ...
}
```

## Data analysis
WIP
```
usage: analyze.py [-h] [--output OUTPUT] [--verbose]
                  [--filter [PERSON [PERSON ...]]]
                  [--csv-delimiter CSV_DELIMITER]
                  SOURCE {message-count,emoji-usage,message-analysis} ...

positional arguments:
  SOURCE                data source file.
  {message-count,emoji-usage,message-analysis}
                        Available commands

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT       output file path, by default is equal to "out.csv"
                        with extension matching the format
  --verbose
  --filter [PERSON [PERSON ...]]
                        parse only select people
  --csv-delimiter CSV_DELIMITER
                        "," by default
```

## Data visualization
WIP

### [Examples - visualized using Google Sheets](./example)
