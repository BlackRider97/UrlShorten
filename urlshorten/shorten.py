#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import logging

BASE = 62
UPPERCASE_OFFSET = 55
LOWERCASE_OFFSET = 61
DIGIT_OFFSET = 48

class UrlShortener:
    
    def __init__(self,dbconnections):
        self.dbconnections = dbconnections
  
    def get_digit_from_char(self, char):
        if char.isdigit():
            return ord(char) - DIGIT_OFFSET
        elif 'A' <= char <= 'Z':
            return ord(char) - UPPERCASE_OFFSET
        elif 'a' <= char <= 'z':
            return ord(char) - LOWERCASE_OFFSET
        
    def get_char_from_digit(self, digit):
        if digit < 10:
            return chr(digit + DIGIT_OFFSET)
        elif 10 <= digit <= 35:
            return chr(digit + UPPERCASE_OFFSET)
        elif 36 <= digit < 62:
            return chr(digit + LOWERCASE_OFFSET)

    def get_index_from_key(self, key):
        int_sum = 0
        reversed_key = key[::-1]
        for idx, char in enumerate(reversed_key):
            int_sum += self.get_digit_from_char(char) * int(math.pow(BASE, idx))
        return int_sum

    def get_key_from_index(self, index):
        # we shouldn't return a number 
        if index == 0:
            return '0'
        string = ""
        while index > 0:
            remainder = index % BASE
            string = self.get_char_from_digit(remainder) + string
            index /= BASE
        return string
                
    def get_short_url(self, long_url):
        """
        store long_url and corresponding short_url in db and also maintain a cache to avoid hotspoting problem
        and finally return short_url
        
        """
        integer_value  = self.dbconnections.dbhandler.insert_data_in_mysql(long_url)
        short_url = self.get_key_from_index(integer_value)
        if short_url:
            self.dbconnections.dbhandler.set_data_in_redis(short_url, long_url)
            return short_url
        return None

    def get_long_url(self, short_url):
        """
        first check key in cache if found then return value from cache other wise return value from presistent storage 
        
        """
        long_url = self.dbconnections.dbhandler.get_data_from_redis(short_url)
        if long_url:
            # found in cache
            return long_url
        integer_value = self.get_index_from_key(short_url)
        #query from mysql
        long_url = self.dbconnections.dbhandler.get_data_from_mysql(integer_value)
        if not long_url:
            return None
        # update cache
        self.dbconnections.dbhandler.set_data_in_redis(short_url, long_url)
        return long_url