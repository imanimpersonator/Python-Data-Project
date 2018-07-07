import sqlite3
import time
import urllib
import zlib
import string
import re

conn = sqlite3.connect('index.sqlite')
conn.text_factory = str
cur = conn.cursor()

cur.execute('''SELECT subject_id,subject FROM Messages
    JOIN Subjects ON Messages.subject_id = Subjects.id''')
stop = ['and', 'but', 'sakai', 'they', 'they', 'it', 'she', 'he', 'under', 're:', '2.1.1', '1.5.1', 'from', '2.1.x',
        'with', 'email', 'sakai:', 'sakai_session', 'this', 'sakai_event,', '2.1:', '2.2?', '2.1.2', '2.2.0', 'what'
        , 'sakai?']
counts = dict()
for message_row in cur:
    text = message_row[1]
    text = text.strip()
    text = text.lower()
    text = text.replace("'", " ")
    words = text.split(" ")

    for word in words:
        if len(word) < 4:
            continue
        else:
            if word in stop:
                continue
        counts[word] = counts.get(word, 0) + 1

# Find the top 100 words
words = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for w in words[:100]:
    if highest is None or highest < counts[w] :
        highest = counts[w]
    if lowest is None or lowest > counts[w] :
        lowest = counts[w]
print('Range of counts:',highest,lowest)

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('gword.js','w')
fhand.write("gword = [")
first = True
for k in words[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")

print("Output written to gword.js")
print("Open gword.htm in a browser to view")




