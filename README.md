# To Do
1. [x] Basic parsing, number of messages by month
2. [ ] Support for group conversations
3. [ ] Multiple grouping options: month, day, week, etc.
4. [ ] Multiple modes: average number of messages, cumulative number of messages, etc.
5. [ ] Analyzing individual conversations

# merge.py
Use it to parse Facebook's raw conversation json data and merge it into a single file suitable for `process.py`.

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