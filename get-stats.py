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
import pprint
import argparse
import datetime
import operator
import logging
import ConfigParser
from terminaltables import AsciiTable
from lib.wsmotor import WsMotor

def main() :
    
    # Parameters
    time_start = datetime.datetime.now()
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
    parser.add_argument('--action', action='store', dest='action', choices=['list-stats', 'label-stats', 'user-stats'])
    args = parser.parse_args()
    
    # WsMotor object instance
    try :
        inst_wsmotor = WsMotor(Config.get('GLOBAL','application'))  
    except Exception as e :
        logger.error('RunTimeError during instance creation : %s', str(e))
        raise RuntimeError('Exception during instance creation : ' + str(e))
    
    # Parse JSON Wekan URLs and populate dict - 
    dic_wekan = dict()
    for board, url in Config.items('WEKAN_JSON') :
        # Populate dic
        dic_wekan = inst_wsmotor.export_from_json_to_dic(board,url)
    
    # Stats on lists
    if args.action == 'list-stats' :
        # Ascii table for List
        myAsciiTableList = [['List name','NB of live card(s)','NB of archived card(s)','Total card(s)']]
        cards_live_total = 0
        cards_arch_total = 0
        cards_total = 0
        for li in dic_wekan['lists_sort'].values() :
            cards_live_total = cards_live_total + len(dic_wekan['lists'][ li ]['cards_live'])
            cards_arch_total = cards_arch_total + len(dic_wekan['lists'][ li ]['cards_arch'])
            cards_total = cards_total + len(dic_wekan['lists'][ li ]['cards_live']) + len(dic_wekan['lists'][ li ]['cards_arch'])
            tmpdata = list()
            tmpdata.append(dic_wekan['lists'][ li ]['name']) # ListName
            tmpdata.append(str(len(dic_wekan['lists'][ li ]['cards_live']))) # Live cards    
            tmpdata.append(str(len(dic_wekan['lists'][ li ]['cards_arch']))) # Archive cards
            tmpdata.append(str(len(dic_wekan['lists'][ li ]['cards_arch'])+len(dic_wekan['lists'][ li ]['cards_live']))) # Total cards    
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
    
    # Stats on labels
    if args.action == 'label-stats' :
        # Ascii table for Label
        myAsciiTableLabel = [['Label name','NB of live card(s)','NB of archived card(s)','Total card(s)']]
        cards_live_total = 0
        cards_arch_total = 0
        cards_total = 0
        for la in dic_wekan['labels'].values() :
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
    
    # Stats on users
    if args.action == 'user-stats' :
        # Ascii table for User
        myAsciiTableUser = [['Username','NB of live card(s)','NB of archived card(s)','Total card(s)']]
        cards_live_total = 0
        cards_arch_total = 0
        cards_total = 0
        for us in dic_wekan['users'].values() :
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

if __name__ == "__main__" :
    main()