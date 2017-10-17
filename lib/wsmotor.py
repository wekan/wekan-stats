#!/usr/bin/python

import logging
import urllib
import json
import random


class WsMotor :
    """Class to manage Wekan Stats """

    def __init__(self, app_name) :
        
        # Class name
        self.class_name = self.__get_class_name()
        # Logger
        self.logger = logging.getLogger(app_name+'.'+self.class_name)
        self.logger.info('Creating an instance of %s', self.class_name)
        # Data of Wekan
        self.data = dict()

    def __get_class_name(self) :
        """Method to have instance name of class (str)"""

        return self.__class__.__name__
    
    def add_card_into_user_dic(self, board, card) :
        """Method that will add card into user dict"""
        
        # Populate users
        for user in card['members'] :
            if card['archived'] == False :
                self.data[ board ]['users'][ user ]['cards_live'].append(card['_id'])
            else :
                self.data[ board ]['users'][ user ]['cards_arch'].append(card['_id'])

    def add_card_into_label_dic(self, board, card) :
        """Method that will add card into label dict"""
        
        # Populate labels
        for label in card['labelIds'] :
            if card['archived'] == False :
                self.data[ board ]['labels'][ label ]['cards_live'].append(card['_id'])
            else :
                self.data[ board ]['labels'][ label ]['cards_arch'].append(card['_id'])

    def add_card_into_list_dic(self, board, card) :
        """Method that will add card into list dict"""
        
        # Populate list
        if card['archived'] == False :
            self.data[ board ]['lists'][ card['listId'] ]['cards_live'].append(card['_id'])
        else :
            self.data[ board ]['lists'][ card['listId'] ]['cards_arch'].append(card['_id'])

    def add_event_into_user_dic(self, board, event) :
        """Method that will add event into user dict"""
        
        # Populate user dict
        if not event['activityType'] in self.data[ board ]['users'][ event['userId'] ]['events']['type'].keys() :
            self.data[ board ]['users'][ event['userId'] ]['events']['type'][ event['activityType'] ] = list()
        self.data[ board ]['users'][ event['userId'] ]['events']['type'][ event['activityType'] ].append(event['_id'])
        self.data[ board ]['users'][ event['userId'] ]['events']['all'].append(event['_id'])
    
    def add_event_into_list_dic(self, board, event) :
        """Method that will add event into list dict"""
        
        # Populate list dict
        if not event['activityType'] in self.data[ board ]['lists'][ event['listId'] ]['events']['type'].keys() :
            self.data[ board ]['lists'][ event['listId'] ]['events']['type'][ event['activityType'] ] = list()
        self.data[ board ]['lists'][ event['listId'] ]['events']['type'][ event['activityType'] ].append(event['_id'])
        self.data[ board ]['lists'][ event['listId'] ]['events']['all'].append(event['_id'])

    def add_event_into_card_dic(self, board, event) :
        """Method that will add event into card dict"""
        
        # Populate list dict
        if not event['activityType'] in self.data[ board ]['cards'][ event['cardId'] ]['events']['type'].keys() :
            self.data[ board ]['cards'][ event['cardId'] ]['events']['type'][ event['activityType'] ] = list()
        self.data[ board ]['cards'][ event['cardId'] ]['events']['type'][ event['activityType'] ].append(event['_id'])
        self.data[ board ]['cards'][ event['cardId'] ]['events']['all'].append(event['_id'])

    def order_dic_per_cards_nb(self, board, branch) :
        """Method to order dic with cards_live values - new dic self.data[ board ][ branch_sort ] will be created"""
    
        self.logger.info('Ordering dictionnary "%s" for board "%s"', branch,  board)
        # Create dic for order
        self.data[ board ][ branch + '_sort' ] = dict()
        # Parse branch
        for key, value in self.data[ board ][ branch ].items() :
            self.data[ board ][ branch + '_sort' ][ len(value['cards_live'])*1000+random.randrange(1,999) ] = key
    
    def order_dic_cards(self, board) :
        """Method to order dic cards - new dic self.data[ board ][ cards_sort ] will be created"""
    
        self.logger.info('Ordering dictionnary "cards" for board "%s"',  board)
        # Create dic for order
        self.data[ board ]['cards_sort' ] = dict()
        # Parse branch
        for key, value in self.data[ board ]['cards'].items() :
            self.data[ board ]['cards_sort' ][ value['sort']*1000+random.randrange(1,999) ] = key
    
    def get_data_from_json(self, board, url_json) :
        """Method to export JSON Wekan URL to a dictionary : """
        
        self.logger.info('Exporting JSON Wekan URL for board "%s" to a class dic : %s', board, url_json)
        # Get data from JSON URL
        file = urllib.urlopen(url_json)
        data_json = json.load(file)
        # Dic for the board
        self.data[ board ] = dict()
        
        # Parsing of JSON users
        self.data[ board ]['users'] = dict()
        for us in data_json['users'] :
            self.logger.debug('Board %s - Add "%s" user with id %s into dict', board, us['username'], us['_id'])
            self.data[ board ]['users'][ us['_id'] ] = dict()
            self.data[ board ]['users'][ us['_id'] ]['username'] = us['username']
            self.data[ board ]['users'][ us['_id'] ]['cards_live'] = list()
            self.data[ board ]['users'][ us['_id'] ]['cards_arch'] = list()
            self.data[ board ]['users'][ us['_id'] ]['events'] = dict()
            self.data[ board ]['users'][ us['_id'] ]['events']['all'] = list()
            self.data[ board ]['users'][ us['_id'] ]['events']['type'] = dict()

        # Parsing of JSON lists
        self.data[ board ]['lists'] = dict()
        self.data[ board ]['lists_sort'] = dict()
        for li in data_json['lists'] :
            self.logger.debug('Board %s - Add "%s" list with id %s into dict', board, li['title'], li['_id'])
            self.data[ board ]['lists_sort'][ li['sort'] ] = li['_id']
            self.data[ board ]['lists'][ li['_id'] ] = dict()
            self.data[ board ]['lists'][ li['_id'] ]['name'] = li['title']
            self.data[ board ]['lists'][ li['_id'] ]['cards_live'] = list()
            self.data[ board ]['lists'][ li['_id'] ]['cards_arch'] = list()
            self.data[ board ]['lists'][ li['_id'] ]['events'] = dict()
            self.data[ board ]['lists'][ li['_id'] ]['events']['all'] = list()
            self.data[ board ]['lists'][ li['_id'] ]['events']['type'] = dict()

        # Parsing of JSON labels
        self.data[ board ]['labels'] = dict()
        self.data[ board ]['labels_sort'] = dict()
        for la in data_json['labels'] :
            self.logger.debug('Board %s - Add "%s" label with id %s into dict', board, la['name'], la['_id'])
            self.data[ board ]['labels'][ la['_id'] ] = dict()
            self.data[ board ]['labels'][ la['_id'] ]['name'] = la['name']
            self.data[ board ]['labels'][ la['_id'] ]['cards_live'] = list()
            self.data[ board ]['labels'][ la['_id'] ]['cards_arch'] = list()


        # Parsing of JSON cards
        self.data[ board ]['cards'] = dict()
        for ca in data_json['cards'] :
            self.logger.debug('Board %s - Add "%s" card with id %s into dict', board, ca['title'], ca['_id'])
            self.data[ board ]['cards'][ ca['_id'] ] = dict()
            self.data[ board ]['cards'][ ca['_id'] ]['title'] = ca['title']
            self.data[ board ]['cards'][ ca['_id'] ]['archived'] = ca['archived']
            self.data[ board ]['cards'][ ca['_id'] ]['sort'] = ca['sort']
            self.data[ board ]['cards'][ ca['_id'] ]['members'] = ca['members']
            self.data[ board ]['cards'][ ca['_id'] ]['labels'] = ca['labelIds']
            self.data[ board ]['cards'][ ca['_id'] ]['list'] = ca['listId']
            self.data[ board ]['cards'][ ca['_id'] ]['created'] = ca['createdAt']
            self.data[ board ]['cards'][ ca['_id'] ]['lastupdate'] = ca['dateLastActivity']
            self.data[ board ]['cards'][ ca['_id'] ]['events'] = dict()
            self.data[ board ]['cards'][ ca['_id'] ]['events']['all'] = list()
            self.data[ board ]['cards'][ ca['_id'] ]['events']['type'] = dict()
            # Populate list
            self.add_card_into_list_dic(board,ca)
            # Populate labels
            self.add_card_into_label_dic(board,ca)
            # Populate users
            self.add_card_into_user_dic(board,ca)
        
        # Parsing of JSON events
        self.data[ board ]['events'] = {'all': dict(),'type': dict()}
        for ev in data_json['activities'] :
            # Populate dict all
            self.logger.debug('Board %s - Add event type "%s" with id %s into events dict', board, ev['activityType'], ev['_id'])
            self.data[ board ]['events']['all'][ ev['_id'] ] = dict()
            self.data[ board ]['events']['all'][ ev['_id'] ]['type'] = ev['activityType']
            self.data[ board ]['events']['all'][ ev['_id'] ]['created'] = ev['createdAt']
            # Populate dict type
            if not ev['activityType'] in self.data[ board ]['events']['type'].keys() :
                self.data[ board ]['events']['type'][ ev['activityType'] ] = list()
            self.data[ board ]['events']['type'][ ev['activityType'] ].append(ev['_id'])
            # Populate user
            self.add_event_into_user_dic(board,ev)
            # Populate list if needed
            if 'listId' in ev.keys() :
                self.add_event_into_list_dic(board,ev)
            # Populate card if needed
            if 'cardId' in ev.keys() :
                self.add_event_into_card_dic(board,ev)
        
        # Order
        self.order_dic_per_cards_nb(board,'labels')
        self.order_dic_per_cards_nb(board,'users')
        self.order_dic_cards(board)
        
        # Close file
        file.close()