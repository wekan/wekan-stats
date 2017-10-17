#!/usr/bin/env python
#
# get-cards.py
#
# Simple wrapper that giving cards list specific Wekan dashboard
#
# Author: Florent MONTHEL (fmonthel@flox-arts.net)
#

#! /usr/bin/python

import os
import argparse
import datetime
import logging
import ConfigParser
from terminaltables import AsciiTable
from lib.wsmotor import WsMotor

def main() :

    # Parameters
    file_config = os.path.join(os.path.dirname(__file__), 'conf/config.ini')
    Config = ConfigParser.ConfigParser()
    Config.read(file_config)
    # Logging setup
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(Config.get('GLOBAL','application'))
    handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), 'log/'+Config.get('GLOBAL','application')+'.log'))
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Options
    parser = argparse.ArgumentParser(description='Get cards list of Wekan Dashboard')
    parser.add_argument('--board', action='store', dest='board', help='Board name indicated in ini file - Example : my-board', required=True)
    parser.add_argument('--card-type', action='store', dest='card_type', choices=['live', 'archived', 'all'], help='Kind of cards to get')
    parser.add_argument('--username', action='store', dest='username')
    parser.add_argument('--list', action='store', dest='list')

    args = parser.parse_args()
    
    # WsMotor object instance
    try :
        
        inst_wsmotor = WsMotor(Config.get('GLOBAL','application'))
       
        # Parse JSON Wekan URLs and populate dict
        dic_wekan = dict()
        for board, url in Config.items('WEKAN_JSON') :
            # Is it board that we want ?
            if board != args.board :
                continue
            # Populate dic
            inst_wsmotor.get_data_from_json(board, url)
            # Get boad data
            dic_wekan = inst_wsmotor.data[ args.board ]
        
        # Board not found
        if len(dic_wekan) == 0 :
            raise RuntimeError('Board "' + args.board + '" not found in ini file :(')
        
    except Exception as e :
        logger.error('RunTimeError during instance creation : %s', str(e))
        raise RuntimeError('Exception during instance creation : ' + str(e))


    # Ok get cards info
    myAsciiTableCard = [['Card title','List','Archived','Member(s)','Labek(s)','Created Date','NB of event(s)']]
    events_total = 0
    for (k,v) in sorted(dic_wekan['cards_sort'].items(),reverse=False) :
        if args.card_type == 'live' and dic_wekan['cards'][ v ]['archived'] == True :
            continue
        if args.card_type == 'archived' and dic_wekan['cards'][ v ]['archived'] == False :
            continue
        if args.username :
            username_found = False
            for mem in dic_wekan['cards'][ v ]['members'] :
                if dic_wekan['users'][ mem ]['username'] == args.username :
                     username_found = True
            if username_found == False :
                continue
        if args.list and dic_wekan['lists'][ dic_wekan['cards'][ v ]['list'] ]['name'] != args.list :
            continue
        events_total = events_total + len(dic_wekan['cards'][ v ]['events']['all'])
        tmpdata = list()
        tmpdata.append(str(dic_wekan['cards'][ v ]['title'][0:80].encode('utf8'))) # Card name
        # List
        tmpdata.append(str(dic_wekan['lists'][ dic_wekan['cards'][ v ]['list'] ]['name']))
        # Archived or Live
        if dic_wekan['cards'][ v ]['archived'] == False :
            tmpdata.append('No') # Live cards
        else :
            tmpdata.append('Yes') # Archived cards
        # Members
        members = ''
        for mem in dic_wekan['cards'][ v ]['members'] :
            if members == '' :
                members = dic_wekan['users'][ mem ]['username']
            else :
                members = members + "\n" + dic_wekan['users'][ mem ]['username']
        tmpdata.append(str(members))
        # Labels
        labels = ''
        for lab in dic_wekan['cards'][ v ]['labels'] :
            if labels == '' :
				labels = dic_wekan['labels'][ lab ]['name']
            else :
                labels = labels + " - " + dic_wekan['labels'][ lab ]['name']
        tmpdata.append(str(labels))
        tmpdata.append(str(dic_wekan['cards'][ v ]['created'][0:10])) # Date of creation
        tmpdata.append(str(len(dic_wekan['cards'][ v ]['events']['all']))) # Events nb
        myAsciiTableCard.append(tmpdata)
    # Total for Card
    tmpdata = list()
    tmpdata.append("Total : " + str(len(myAsciiTableCard) - 1) + " card(s)")
    tmpdata.append("")
    tmpdata.append("")
    tmpdata.append("")
    tmpdata.append("")
    tmpdata.append("")
    tmpdata.append(str(events_total))
    myAsciiTableCard.append(tmpdata)
    # Create AsciiTable for Card
    myTable = AsciiTable(myAsciiTableCard)
    myTable.inner_footing_row_border = True
    myTable.justify_columns[1] = myTable.justify_columns[2] = myTable.justify_columns[3] = myTable.justify_columns[4] = 'right'
    myTable.justify_columns[5] = myTable.justify_columns[6] = 'right'
    # Output data
    print myTable.table
    
    
if __name__ == "__main__" :
    main()