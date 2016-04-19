#! /usr/bin/python

import json
from pprint import pprint
from terminaltables import AsciiTable

json_file='input.json'

json_data=open(json_file)
data = json.load(json_data)
#pprint(data)
json_data.close()

tmp = dict()
# Loop on users
tmp['users'] = dict()
for us in data['users'] :
    tmp['users'][ us['_id'] ] = dict()
    tmp['users'][ us['_id'] ]['username'] = us['username']
    tmp['users'][ us['_id'] ]['cards_live'] = list()
    tmp['users'][ us['_id'] ]['cards_arch'] = list()

# Loop on lists
tmp['lists'] = dict()
tmp['lists_sort'] = dict()
for li in data['lists'] :
    tmp['lists_sort'][ li['sort'] ] = li['_id']
    tmp['lists'][ li['_id'] ] = dict()
    tmp['lists'][ li['_id'] ]['name'] = li['title']
    tmp['lists'][ li['_id'] ]['sort'] = li['sort']
    tmp['lists'][ li['_id'] ]['cards_live'] = list()
    tmp['lists'][ li['_id'] ]['cards_arch'] = list()
sorted(tmp['lists'], key=lambda student: student[2])


# Loop on labels
tmp['labels'] = dict()
for la in data['labels'] :
    tmp['labels'][ la['_id'] ] = dict()
    tmp['labels'][ la['_id'] ]['name'] = la['name']
    tmp['labels'][ la['_id'] ]['cards_live'] = list()
    tmp['labels'][ la['_id'] ]['cards_arch'] = list()

# Loop on cards
tmp['cards'] = dict()
for ca in data['cards'] :
    # Get data
    tmp['cards'][ ca['_id'] ] = dict()
    tmp['cards'][ ca['_id'] ]['title'] = ca['title']
    # Populate list
    if ca['archived'] == False :
        tmp['lists'][ ca['listId'] ]['cards_live'].append(ca['_id'])
    else :
        tmp['lists'][ ca['listId'] ]['cards_arch'].append(ca['_id'])
    # Populate labels
    for lab in ca['labelIds'] :
        if ca['archived'] == False :
            tmp['labels'][ lab ]['cards_live'].append(ca['_id'])
        else :
            tmp['labels'][ lab ]['cards_arch'].append(ca['_id'])
    # Populate users
    for mem in ca['members'] :
        if ca['archived'] == False :
            tmp['users'][ mem ]['cards_live'].append(ca['_id'])
        else :
            tmp['users'][ mem ]['cards_arch'].append(ca['_id'])
# Sum-up
print "####### Stats for Wekan board : '" + data['title'] + "' #######"
print "#### LISTS STATS ####"
for li in tmp['lists_sort'].values() : 
    print "- Number of cards in list '" + tmp['lists'][ li ]['name'] + "' : live => " + str(len(tmp['lists'][ li ]['cards_live'])) + " archive => " + str(len(tmp['lists'][ li ]['cards_arch']))
print "#### LABEL STATS ####"
for la in tmp['labels'].values() :
    print "- Number of active cards in label '" + la['name'] + "' : live => " + str(len(la['cards_live'])) + " archive => " + str(len(la['cards_arch']))
print "#### USER STATS ####"
for us in tmp['users'].values() :
    print "- Number of active cards for user'" + us['username'] + "' : live => " + str(len(us['cards_live'])) + " archive => " + str(len(us['cards_arch']))

#pprint(tmp)
#print "Dimension: ", data['cubes'][cube]['dim']
#print "Measures:  ", data['cubes'][cube]['meas']