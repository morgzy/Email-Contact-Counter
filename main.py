"""
A script for rapid parsing of large email dumps to analyse senders and receivers,
useful for finding anomalies and frequent contacts

By Morgan Hopkins
2022
"""

import os
import re

# Assign path to folder and return list of all emails within
path = './email-dump/'  # NAME OF DIRECTORY HERE
listing = os.listdir(path)


def getRecipient(email):
    """
    Registry expression to find recipient
    """
    recipient = re.findall(f'Delivered-To: ([a-zA-Z0-9._%+-]+[@][a-zA-Z0-9._%+-]+)', email)
    return recipient


def getSender(email):
    """
    Registry expression to find sender
    """
    sender = re.findall(f'Return-Path: <([a-zA-Z0-9._%+-]+[@][a-zA-Z0-9._%+-]+)>', email)
    return sender


fails = []  # List of emails script failed to read
connections = {}  # Dictionary containing all found connections

i = 0
for file in listing:
    """
    Read through each email
    """
    get = open(path + file)
    try:
        current = get.read()
    except:
        fails.append(file)
        continue
    recipients = getRecipient(current)
    send = getSender(current)
    for sender in send:
        if sender not in connections:
            connections[sender] = {}
            connections[sender]['files'] = []
        for recipient in recipients:
            if recipient not in connections[sender]:
                connections[sender][recipient] = 1
                connections[sender]['files'].append(file)
            else:
                connections[sender][recipient] += 1
                connections[sender]['files'].append(file)

with open("./connections.txt", "w") as f:
    for key, nested in sorted(connections.items()):
        for subkey, value in sorted(nested.items()):
            print(key, '\n   {}: {}'.format(subkey, value), file=f)
        print(file=f)
