# To Do
1. [x] Basic parsing, number of messages by month
2. [ ] Support for group conversations
3. [ ] Multiple grouping options: month, day, week, etc.
4. [ ] Multiple modes: average number of messages, cumulative number of messages, etc.
5. [ ] Analyzing individual conversations

# merge.py
Use it to parse Facebook's raw conversation json data and merge it into a single file suitable for `process.py`.

## Example usage:
After downloading Facebook's archive, unarchive to some location, we'll call it `ARCHIVE_LOCATION`

Then use the script to merge the multiple files in the archive into a single json file, like so:
```bash
$ ./merge.py ARCHIVE_LOCATION
```

The script should produce a `merged.json` file.

For more options use the `-h` flag.

# process.py
Used to process the data into data sersies suitable for visualization.

## Expected format:
```json
{
    "John Doe": [ 
        {
            "timestamp": 1526397926
        },
        {
            "timestamp": 1526397752
        },
        ...
    ]
}
```

## Example usage:
```bash
$ ./process.py merged.json message-count
```

By default the above command will produce `out.csv` file.

Which would look something like this:
```csv
,2011-08-01,2011-09-01,2011-10-01
John Doe,20,30,40
Jane Doe,40,30,20
```