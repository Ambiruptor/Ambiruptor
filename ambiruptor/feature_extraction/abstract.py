#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Abstract :
    """Abstract class for feature extraction"""
    
    def __init__(self, word) :
        """Init the feature extractor with the ambiguous word"""
        pass
    
    def extract(self, window, pos) :
        """
        Extract a features vector.
        @param(window) : string
        @param(pos) : integer (position of the word in the sentence)
        @return : vector of features
        """
        pass
