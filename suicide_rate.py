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

fully_flat = fully_flat.dropna(axis=0, subset=['dim.COUNTRY'])

fully_flat = fully_flat[fully_flat['dim.SEX']=='Both sexes']

fully_flat = fully_flat[fully_flat['dim.REGION']=='Europe']
fully_flat= fully_flat.drop(['Comments', 'dim.PUBLISHSTATE', 'dim.SEX','dim.GHO','dim.UNREGION','dim.REGION','dim.WORLDBANKINCOMEGROUP','dim.AGEGROUP'], axis=1)


fully_flat.sort_values(by=['dim.COUNTRY'])

fully_flat = fully_flat[(fully_flat['dim.YEAR']=='2015') | (fully_flat['dim.YEAR']=='2016')]

fully_flat = fully_flat[['dim.COUNTRY','dim.YEAR', 'Value', ]]

fully_flat = fully_flat.rename(columns={"dim.COUNTRY": "Country", "dim.YEAR": "Suicide_year"})

rows_to_drop = ['Albania', 'Azerbaijan', 'Armenia', 'Bosnia and Herzegovina','Georgia', 'Israel', 'Kazakhstan', 'Kyrgyzstan','North Macedonia','Republic of Moldova', 'Belarus','Turkey', 'Tajikistan','Turkmenistan'
]
europe_country = fully_flat [~fully_flat ['Country'].isin(rows_to_drop)]

europe_country["Country"]=europe_country["Country"].replace({"Czechia": "Czech Republic","Russian Federation": "Russia","United Kingdom of Great Britain and Northern Ireland": "United Kingdom"})

europe_country["Value"] = pd.to_numeric(europe_country["Value"])

suicide_rate = pd.DataFrame(europe_country.groupby(['Country','Suicide_year'], as_index=False )['Value'].mean())

rows_to_drop = ['Uzbekistan', 'Ukraine', 'Russia']
suicide_rate = suicide_rate [~suicide_rate ['Country'].isin(rows_to_drop)]

suicide_rate['Country'].nunique()

suicide_rate= suicide_rate.rename(columns={"Value": "Suicide_Value"})

suicide_rate

def get_suicide_rate():
    return suicide_rate