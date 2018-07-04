class Messages:
    def __init__(self, data):
        self.data = data

    def raw_data(self):
        print ('WARNING: Using raw data')
        return self.data

    def conversation(self, person):
        if not person in self.data:
            raise Exception('Cannot resolve {} in data.'.format(person))

        return Conversation(person, self.data[person])

    def conversations(self):
        return (Conversation(person, self.data[person]) for person in self.data.keys())

class Conversation:
    def __init__(self, person, data):
        self._person = person
        self.data = data

    def raw_data(self):
        print ('WARNING: Using raw data')
        return self.data

    def messages(self):
        return (Message(msg) for msg in self.data)

    def person(self):
        return self._person

    def people(self):
        return set(msg.sender() for msg in self.messages())

    def messages_of(self, sender):
        return (msg for msg in self.messages() if msg.sender() == sender)

class Message(object):
    SENDER_NAME = 'sender_name'
    CONTENT = 'content'
    TIMESTAMP = 'timestamp'

    def __init__(self, data):
        self.data = data

    def sender(self):
        return self.data[self.SENDER_NAME]

    def content(self):
        return self.data[self.CONTENT]

    def timestamp(self):
        return self.data[self.TIMESTAMP]