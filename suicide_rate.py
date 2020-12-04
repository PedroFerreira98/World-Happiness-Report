# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:21:09 2020

@author: joana
"""

import pandas as pd
import requests

response = requests.get('http://apps.who.int/gho/athena/api/GHO/SDGSUICIDE.json?profile=simple')

new_df = pd.DataFrame(response.json()['fact'])
fully_flat = pd.json_normalize(response.json()['fact'])
fully_flat

#FILTER BY BOTH SEXES
fully_flat = fully_flat[fully_flat['dim.SEX']=='Both sexes']
fully_flat.head(15)

#DROP COLUMNS
fully_flat= fully_flat.drop(['Comments', 'dim.PUBLISHSTATE', 'dim.SEX',	'dim.GHO','dim.WORLDBANKINCOMEGROUP','dim.AGEGROUP'], axis=1)

#CHANGE ORDER COLUMNS
fully_flat = fully_flat[['dim.COUNTRY', 'dim.REGION', 'dim.UNREGION', 'dim.YEAR', 'Value', ]]

#DROP ROW WITH COUNTRY NAN- VALUES OF WORLD
fully_flat = fully_flat.dropna(axis=0, subset=['dim.COUNTRY'])

fully_flat