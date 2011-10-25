#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import requests
import re
import json

def imdb_rating(title):
    url = 'http://www.imdbapi.com/?t=%s' % title
    imdb = requests.get(url)
    return json.loads(imdb.content)

def decode_title(title):
    m = re.match('([\w\.]+).(\d{4}).*', title)
    if m != None:
        return {'title': m.group(1),
                'year': m.group(2)}
    return None

def pretty_print(movie):
    print '|%s|%s|%s|%s|' % (
        movie['Title'].encode('ascii', 'ignore'),
        movie['Genre'].encode('ascii', 'ignore'),
        movie['Plot'].encode('ascii', 'ignore'),
        movie['Rating'].encode('ascii', 'ignore'))

r = requests.get('http://users.telenet.be/alenkin/')
soup = BeautifulSoup(r.content)


items = []
for item in soup.findAll('a', target = '_blank'):
    name = item.string
    if name != None:
        movie = decode_title(name)
        if movie != None:
            items.append(imdb_rating(movie['title'].replace('.', '%20')))

byrating = sorted(items, key=lambda i: i['Rating'])
print '|title|genre|plot|score|'
map(pretty_print, byrating)
