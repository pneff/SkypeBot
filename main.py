#!/usr/bin/env python
import Skype4Py

def main():
    skype = Skype4Py.Skype()
    skype.OnMessageStatus = on_message
    skype.Attach()
    # Wait until user exits
    cmd = '';
    while not cmd == 'exit':
        cmd = raw_input('');

def on_message(message, status):
    if status == 'RECEIVED' or status == 'SENT':
        process_message(message)


class DebugComponent(object):
    def handle(self, msg):
        """Print the message."""
        for key in dir(msg):
            if not key.startswith('_'):
                try:
                    print "{0:>20}: {1}".format(key, getattr(msg, key))
                except:
                    pass
        print '*' * 80


class NagiosNotificationComponent(object):
    def __init__(self):
        self.subscribers = {}

    def handle(self, msg):
        """Print the message."""
        body = msg.Body.strip()
        if not body.lower().startswith('nagios '):
            return
        body = body[6:].strip()
        print body
        if body.lower().startswith('sub'):
            self.subscribe(msg.FromHandle)
            msg.Chat.SendMessage("You've been subscribed to receive Nagios alerts.")
        elif body.lower().startswith('unsub'):
            self.unsubscribe(msg.FromHandle)
            msg.Chat.SendMessage("You've been unsubscribed from receiving Nagios alerts.")
        else:
            msg.Chat.SendMessage("Unknown command for Nagios.\nKnown commands:\n  - sub: Subscribe to nagios alerts\n  - unsub: Unsubscribe from nagios alerts")
        return True

    def subscribe(self, handle):
        self.subscribers[handle] = True

    def unsubscribe(self, handle):
        del self.subscribers[handle]


components = [
    NagiosNotificationComponent(),
    DebugComponent(),
]

def process_message(msg):
    for component in components:
        if component.handle(msg) is True:
            return


if __name__ == '__main__':
    main()
