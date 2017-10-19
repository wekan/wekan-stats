#!/usr/bin/env python
#
# get-stats.py
#
# Simple wrapper that giving some stats on specific Wekan dashboard
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
    parser = argparse.ArgumentParser(description='Get some stats on Wekan Dashboard')
    parser.add_argument('--board', action='store', dest='board', help='Board name indicated in ini file - Example : my-board', required=True)
    parser.add_argument('--action', action='store', dest='action', choices=['list-stats', 'label-stats', 'user-stats', 'event-stats'], required=True)
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
    
    # Stats on lists
    if args.action == 'list-stats' :
        # Ascii table for List
        myAsciiTableList = [['List name','Event(s) generated','NB of live card(s)','NB of archived card(s)','Total card(s)']]
        events_total = 0
        cards_live_total = 0
        cards_arch_total = 0
        cards_total = 0
        for (k,v) in sorted(dic_wekan['lists_sort'].items()) :
            events_total = events_total + len(dic_wekan['lists'][ v ]['events']['all'])
            cards_live_total = cards_live_total + len(dic_wekan['lists'][ v ]['cards_live'])
            cards_arch_total = cards_arch_total + len(dic_wekan['lists'][ v ]['cards_arch'])
            cards_total = cards_total + len(dic_wekan['lists'][ v ]['cards_live']) + len(dic_wekan['lists'][ v ]['cards_arch'])
            tmpdata = list()
            tmpdata.append(dic_wekan['lists'][ v ]['name']) # ListName
            tmpdata.append(str(len(dic_wekan['lists'][ v ]['events']['all']))) # Total events
            tmpdata.append(str(len(dic_wekan['lists'][ v ]['cards_live']))) # Live cards
            tmpdata.append(str(len(dic_wekan['lists'][ v ]['cards_arch']))) # Archive cards
            tmpdata.append(str(len(dic_wekan['lists'][ v ]['cards_arch'])+len(dic_wekan['lists'][ v ]['cards_live']))) # Total cards
            myAsciiTableList.append(tmpdata)
        # Total for List
        tmpdata = list()
        tmpdata.append("Total : " + str(len(myAsciiTableList) - 1) + " list(s)")
        tmpdata.append(str(events_total))
        tmpdata.append(str(cards_live_total))
        tmpdata.append(str(cards_arch_total))
        tmpdata.append(str(cards_total))
        myAsciiTableList.append(tmpdata)
        # Create AsciiTable for List
        myTable = AsciiTable(myAsciiTableList)
        myTable.inner_footing_row_border = True
        myTable.justify_columns[1] = myTable.justify_columns[2] = myTable.justify_columns[3] = myTable.justify_columns[4] = 'right'
        # Output data
        print myTable.table
    
    # Stats on labels
    if args.action == 'label-stats' :
        # Ascii table for Label
        myAsciiTableLabel = [['Label name','NB of live card(s)','NB of archived card(s)','Total card(s)']]
        cards_live_total = 0
        cards_arch_total = 0
        cards_total = 0
        for (k,v) in sorted(dic_wekan['labels_sort'].items(),reverse=True) :
            cards_live_total = cards_live_total + len(dic_wekan['labels'][ v ]['cards_live'])
            cards_arch_total = cards_arch_total + len(dic_wekan['labels'][ v ]['cards_arch'])
            cards_total = cards_total + len(dic_wekan['labels'][ v ]['cards_live']) + len(dic_wekan['labels'][ v ]['cards_arch'])
            tmpdata = list()
            tmpdata.append(dic_wekan['labels'][ v ]['name']) # ListName
            tmpdata.append(str(len(dic_wekan['labels'][ v ]['cards_live']))) # Live cards
            tmpdata.append(str(len(dic_wekan['labels'][ v ]['cards_arch']))) # Archive cards
            tmpdata.append(str(len(dic_wekan['labels'][ v ]['cards_arch'])+len(dic_wekan['labels'][ v ]['cards_live']))) # Total cards
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
    
    # Stats on users
    if args.action == 'user-stats' :
        # Ascii table for User
        myAsciiTableUser = [['Username','Event(s) generated','NB of live card(s)','NB of archived card(s)','Total card(s)']]
        events_total = 0
        cards_live_total = 0
        cards_arch_total = 0
        cards_total = 0
        for (k,v) in sorted(dic_wekan['users_sort'].items(),reverse=True) :
            if len(dic_wekan['users'][ v ]['cards_live']) + len(dic_wekan['users'][ v ]['cards_arch']) == 0 :
                continue
            events_total = events_total + len(dic_wekan['users'][ v ]['events']['all'])
            cards_live_total = cards_live_total + len(dic_wekan['users'][ v ]['cards_live'])
            cards_arch_total = cards_arch_total + len(dic_wekan['users'][ v ]['cards_arch'])
            cards_total = cards_total + len(dic_wekan['users'][ v ]['cards_live']) + len(dic_wekan['users'][ v ]['cards_arch'])
            tmpdata = list()
            tmpdata.append(dic_wekan['users'][ v ]['username']) # Username
            tmpdata.append(str(len(dic_wekan['users'][ v ]['events']['all']))) # Total events
            tmpdata.append(str(len(dic_wekan['users'][ v ]['cards_live']))) # Live cards
            tmpdata.append(str(len(dic_wekan['users'][ v ]['cards_arch']))) # Archive cards
            tmpdata.append(str(len(dic_wekan['users'][ v ]['cards_arch'])+len(dic_wekan['users'][ v ]['cards_live']))) # Total cards
            
            myAsciiTableUser.append(tmpdata)
        # Total for users
        tmpdata = list()
        tmpdata.append("Total : " + str(len(myAsciiTableUser) - 1) + " User(s)")
        tmpdata.append(str(events_total))
        tmpdata.append(str(cards_live_total))
        tmpdata.append(str(cards_arch_total))
        tmpdata.append(str(cards_total))
        myAsciiTableUser.append(tmpdata)
        # Create AsciiTable for User
        myTable = AsciiTable(myAsciiTableUser)
        myTable.inner_footing_row_border = True
        myTable.justify_columns[1] = myTable.justify_columns[2] = myTable.justify_columns[3] = myTable.justify_columns[4] = 'right'
        # Output data
        print myTable.table
    
    # Stats on events
    if args.action == 'event-stats' :
        # Ascii table for Label
        myAsciiEventLabel = [['Event name','NB of event(s)']]
        events_total = 0
        for (k,v) in dic_wekan['events']['type'].items() :
            events_total = events_total + len(dic_wekan['events']['type'][ k ])
            tmpdata = list()
            tmpdata.append(k) # Event name
            tmpdata.append(str(len(dic_wekan['events']['type'][ k ]))) # Events count
            myAsciiEventLabel.append(tmpdata)
        # Total for Events
        tmpdata = list()
        tmpdata.append("Total : " + str(len(myAsciiEventLabel) - 1) + " Event(s)")
        tmpdata.append(str(events_total))
        myAsciiEventLabel.append(tmpdata)
        # Create AsciiTable for Label
        myTable = AsciiTable(myAsciiEventLabel)
        myTable.inner_footing_row_border = True
        myTable.justify_columns[1] = myTable.justify_columns[2] = 'right'
        # Output data
        print myTable.table

if __name__ == "__main__" :
    main()
