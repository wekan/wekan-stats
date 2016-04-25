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
    
    def order_dic_per_cards_nb(self, board, branch) :
        """Method to order dic with cards_live values - new dic self.data[ board ][ branch_sort ] will be created"""
    
        self.logger.info('Will order for a board %s class dic branch %s', board, branch)
        # Create dic for order
        self.data[ board ][ branch + '_sort' ] = dict()
        # Parse branch
        for key, value in self.data[ board ][ branch ].items() :
            self.data[ board ][ branch + '_sort' ][ len(value['cards_live'])*1000+random.randrange(1,999) ] = key
    
    def get_data_from_json(self, board, url_json) :
        """Method to export JSON Wekan URL to a dictionary : """
        
        self.logger.info('Will export below JSON Wekan URL for board %s to a class dic : %s', board, url_json)
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
            # Populate list
            if ca['archived'] == False :
                self.data[ board ]['lists'][ ca['listId'] ]['cards_live'].append(ca['_id'])
            else :
                self.data[ board ]['lists'][ ca['listId'] ]['cards_arch'].append(ca['_id'])
    
            # Populate labels
            for lab in ca['labelIds'] :
                if ca['archived'] == False :
                    self.data[ board ]['labels'][ lab ]['cards_live'].append(ca['_id'])
                else :
                    self.data[ board ]['labels'][ lab ]['cards_arch'].append(ca['_id'])
            # Populate users
            for mem in ca['members'] :
                if ca['archived'] == False :
                    self.data[ board ]['users'][ mem ]['cards_live'].append(ca['_id'])
                else :
                    self.data[ board ]['users'][ mem ]['cards_arch'].append(ca['_id'])
        
        # Order
        self.order_dic_per_cards_nb(board,'labels')
        self.order_dic_per_cards_nb(board,'users')
        
        # Close file
        file.close()