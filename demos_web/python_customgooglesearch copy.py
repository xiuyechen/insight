# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 12:16:17 2018

@author: xiuye
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.

Command-line application that does a search.
"""

__author__ = 'jcgregorio@google.com (Joe Gregorio)'

import pprint

from googleapiclient.discovery import build

# load sensitive info
from dotenv import load_dotenv
import os
load_dotenv()
my_developerKey = os.getenv('GOOGLE_DEVELOPER_KEY')
customsearch_cx = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_CX')


GOOGLE_DEVELOPER_KEY
GOOGLE_CUSTOM_SEARCH_ENGINE_CX

def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey=my_developerKey)

  res = service.cse().list(
      q='cake',
      cx=customsearch_cx,
    ).execute()
  return res 
  
def parse_return():
    gs = main()
    # gs.keys() = ['kind', 'items', 'queries', 'searchInformation', 'context', 'url']
    items = gs['items']    

if __name__ == '__main__':
  main()