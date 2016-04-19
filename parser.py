#! /usr/bin/python

import json
import argparse
import urllib
from pprint import pprint
from terminaltables import AsciiTable
import operator


# PARAMS
wekan_export_url_json ='http://monwekan/export.json'

# Options
parser = argparse.ArgumentParser(description='Get some stats on Wekan Dashboard')
parser.add_argument('--action', action='store', dest='action', choices=['list-stats', 'label-stats', 'user-stats'])
args = parser.parse_args()

# Load JSON
file = urllib.urlopen(wekan_export_url_json)
data = json.load(file.read())
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

if args.action == 'list-stats' :

    # Ascii table for List
    myAsciiTableList = [['List name','NB of live card(s)','NB of archived card(s)','Total card(s)']]
    cards_live_total = 0
    cards_arch_total = 0
    cards_total = 0
    for li in tmp['lists_sort'].values() :
        cards_live_total = cards_live_total + len(tmp['lists'][ li ]['cards_live'])
        cards_arch_total = cards_arch_total + len(tmp['lists'][ li ]['cards_arch'])
        cards_total = cards_total + len(tmp['lists'][ li ]['cards_live']) + len(tmp['lists'][ li ]['cards_arch'])
        tmpdata = list()
        tmpdata.append(tmp['lists'][ li ]['name']) # ListName
        tmpdata.append(str(len(tmp['lists'][ li ]['cards_live']))) # Live cards    
        tmpdata.append(str(len(tmp['lists'][ li ]['cards_arch']))) # Archive cards
        tmpdata.append(str(len(tmp['lists'][ li ]['cards_arch'])+len(tmp['lists'][ li ]['cards_live']))) # Total cards    
        myAsciiTableList.append(tmpdata)
    # Total for List
    tmpdata = list()
    tmpdata.append("Total : " + str(len(myAsciiTableList) - 1) + " list(s)")
    tmpdata.append(str(cards_live_total))
    tmpdata.append(str(cards_arch_total))
    tmpdata.append(str(cards_total))
    myAsciiTableList.append(tmpdata)
    # Create AsciiTable for List
    myTable = AsciiTable(myAsciiTableList)
    myTable.inner_footing_row_border = True
    myTable.justify_columns[1] = myTable.justify_columns[2] = myTable.justify_columns[3] = 'right'
    # Output data
    print myTable.table

if args.action == 'label-stats' :

    # Ascii table for Label
    myAsciiTableLabel = [['Label name','NB of live card(s)','NB of archived card(s)','Total card(s)']]
    cards_live_total = 0
    cards_arch_total = 0
    cards_total = 0
    for la in tmp['labels'].values() :
        cards_live_total = cards_live_total + len(la['cards_live'])
        cards_arch_total = cards_arch_total + len(la['cards_arch'])
        cards_total = cards_total + len(la['cards_live']) + len(la['cards_arch'])
        tmpdata = list()
        tmpdata.append(la['name']) # ListName
        tmpdata.append(str(len(la['cards_live']))) # Live cards    
        tmpdata.append(str(len(la['cards_arch']))) # Archive cards
        tmpdata.append(str(len(la['cards_arch'])+len(la['cards_live']))) # Total cards    
        myAsciiTableLabel.append(tmpdata)
    # Total for Label
    tmpdata = list()
    tmpdata.append("Total : " + str(len(myAsciiTableLabel) - 1) + " label(s)")
    tmpdata.append(str(cards_live_total))
    tmpdata.append(str(cards_arch_total))
    tmpdata.append(str(cards_total))
    myAsciiTableLabel.append(tmpdata)
    # Create AsciiTable for Label
    myTable = AsciiTable(myAsciiTableLabel)
    myTable.inner_footing_row_border = True
    myTable.justify_columns[1] = myTable.justify_columns[2] = myTable.justify_columns[3] = 'right'
    # Output data
    print myTable.table

if args.action == 'user-stats' :
    
    # Ascii table for User
    myAsciiTableUser = [['Username','NB of live card(s)','NB of archived card(s)','Total card(s)']]
    cards_live_total = 0
    cards_arch_total = 0
    cards_total = 0
    for us in tmp['users'].values() :
        cards_live_total = cards_live_total + len(us['cards_live'])
        cards_arch_total = cards_arch_total + len(us['cards_arch'])
        cards_total = cards_total + len(us['cards_live']) + len(us['cards_arch'])
        tmpdata = list()
        tmpdata.append(us['username']) # UserName
        tmpdata.append(str(len(us['cards_live']))) # Live cards    
        tmpdata.append(str(len(us['cards_arch']))) # Archive cards
        tmpdata.append(str(len(us['cards_arch'])+len(us['cards_live']))) # Total cards    
        myAsciiTableUser.append(tmpdata)
    # Total for User
    tmpdata = list()
    tmpdata.append("Total : " + str(len(myAsciiTableUser) - 1) + " User(s)")
    tmpdata.append(str(cards_live_total))
    tmpdata.append(str(cards_arch_total))
    tmpdata.append(str(cards_total))
    myAsciiTableUser.append(tmpdata)
    # Create AsciiTable for Label
    myTable = AsciiTable(myAsciiTableUser)
    myTable.inner_footing_row_border = True
    myTable.justify_columns[1] = myTable.justify_columns[2] = myTable.justify_columns[3] = 'right'
    # Output data
    print myTable.table