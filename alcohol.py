# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:45:15 2020

@author: pedro
"""

import pandas as pd
import requests

response = requests.get('http://apps.who.int/gho/athena/api/GHO/SA_0000001400.json?profile=simple')

#Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol)
alcohol = pd.json_normalize(response.json()['fact'])

alcohol.rename(columns={'dim.YEAR':'year'},inplace=True)

alcohol['year'] = alcohol['year'].astype(int)
alcohol = alcohol[alcohol['year']>2014]

alcohol.drop(columns=['dim.PUBLISHSTATE','dim.DATASOURCE','dim.GHO',],inplace=True)

#print(alcohol.columns)
cols_alcohol = ['Value','Region','Alcohol_type','Country','year']

alcohol.columns=cols_alcohol

alcohol.query('Region == "Europe"',inplace=True)

alcohol.reset_index(inplace=True)
alcohol.drop(columns='index',inplace=True)

alcohol.sort_values(by='Country',inplace=True)


#a = alcohol['Country'].unique()

alcohol["Country"].replace({"Russian Federation": "Russia"}, inplace=True)
alcohol["Country"].replace({"United Kingdom of Great Britain and Northern Ireland": "United Kingdom"}, inplace=True)
alcohol["Country"].replace({"Czechia": "Czech Republic"}, inplace=True)




countries_to_drop = ['Albania', 'Andorra', 'Armenia', 'Azerbaijan', 'Belarus', 'Bosnia and Herzegovina', \
                     'Georgia','Kazakhstan', 'Kyrgyzstan', 'North Macedonia', 'Republic of Moldova',  'Tajikistan', 'Turkey', \
                         'Turkmenistan','Russia','Ukraine', 'Uzbekistan','Israel']
    
alcohol = alcohol[~alcohol['Country'].isin(countries_to_drop)]






alcohol.rename(columns={'Value':'Alcohol Consumption (in litres)'},inplace=True)
alcohol.rename(columns={'year':'Alcohol_year'},inplace=True)


alcohol.reset_index(inplace=True)
alcohol.drop(columns='index',inplace=True)




def get_alcohol_table():
    return alcohol


