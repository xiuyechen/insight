# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 11:58:40 2018

@author: xiuye
"""

from googlesearch.googlesearch import GoogleSearch
response = GoogleSearch().search("walnut")
for result in response.results:
    print("Title: " + result.title)
    print("Content: " + result.getText())