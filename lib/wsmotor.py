#!/usr/bin/python

import logging
import urllib
import json


class WsMotor :
    """Class to manage Wekan Stats """
    
    def __init__(self, app_name) :
        
        # Class name
        self.class_name = self.__get_class_name()
        # Logger
        self.logger = logging.getLogger(app_name+'.'+self.class_name)
        self.logger.info('Creating an instance of %s', self.class_name)

    def __get_class_name(self) :
        """Method to have instance name of class (str)"""

        return self.__class__.__name__
    
    def export_from_json_to_dic(self, board, url_json) :
        """Method to export JSON Wekan URL to a dictionary : dic[ year ][ month ][ day ] = busy"""
        
        self.logger.info('Will export below JSON Wekan URL for board %s to a dic : %s', board, url_json)
        # Get data from JSON URL
        file = urllib.urlopen(url_json)
        data = json.load(file)
        tmpDic = dict()
        
        # Parsing of JSON users
        tmpDic['users'] = dict()
        for us in data['users'] :
            self.logger.debug('Board %s - Add "%s" user with id %s into dict', board, us['username'], us['_id'])
            tmpDic['users'][ us['_id'] ] = dict()
            tmpDic['users'][ us['_id'] ]['username'] = us['username']
            tmpDic['users'][ us['_id'] ]['cards_live'] = list()
            tmpDic['users'][ us['_id'] ]['cards_arch'] = list()

        # Parsing of JSON lists
        tmpDic['lists'] = dict()
        tmpDic['lists_sort'] = dict()
        for li in data['lists'] :
            self.logger.debug('Board %s - Add "%s" list with id %s into dict', board, li['title'], li['_id'])
            tmpDic['lists_sort'][ li['sort'] ] = li['_id']
            tmpDic['lists'][ li['_id'] ] = dict()
            tmpDic['lists'][ li['_id'] ]['name'] = li['title']
            tmpDic['lists'][ li['_id'] ]['sort'] = li['sort']
            tmpDic['lists'][ li['_id'] ]['cards_live'] = list()
            tmpDic['lists'][ li['_id'] ]['cards_arch'] = list()

        # Parsing of JSON labels
        tmpDic['labels'] = dict()
        for la in data['labels'] :
            self.logger.debug('Board %s - Add "%s" label with id %s into dict', board, la['name'], la['_id'])
            tmpDic['labels'][ la['_id'] ] = dict()
            tmpDic['labels'][ la['_id'] ]['name'] = la['name']
            tmpDic['labels'][ la['_id'] ]['cards_live'] = list()
            tmpDic['labels'][ la['_id'] ]['cards_arch'] = list()


        # Parsing of JSON cards
        tmpDic['cards'] = dict()
        for ca in data['cards'] :
            self.logger.debug('Board %s - Add "%s" card with id %s into dict', board, ca['title'], ca['_id'])
            tmpDic['cards'][ ca['_id'] ] = dict()
            tmpDic['cards'][ ca['_id'] ]['title'] = ca['title']
            # Populate list
            if ca['archived'] == False :
                tmpDic['lists'][ ca['listId'] ]['cards_live'].append(ca['_id'])
            else :
                tmpDic['lists'][ ca['listId'] ]['cards_arch'].append(ca['_id'])
    
            # Populate labels
            for lab in ca['labelIds'] :
                if ca['archived'] == False :
                    tmpDic['labels'][ lab ]['cards_live'].append(ca['_id'])
                else :
                    tmpDic['labels'][ lab ]['cards_arch'].append(ca['_id'])
            # Populate users
            for mem in ca['members'] :
                if ca['archived'] == False :
                    tmpDic['users'][ mem ]['cards_live'].append(ca['_id'])
                else :
                    tmpDic['users'][ mem ]['cards_arch'].append(ca['_id'])

        # Close file and return dictionnary
        file.close()  
        return tmpDic