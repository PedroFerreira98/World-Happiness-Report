# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 12:01:54 2020

@author: joana
"""

#!pip install eurostat
import eurostat      
import pandas as pd


toc = eurostat.get_toc()
df = eurostat.get_toc_df()

crime = eurostat.subset_toc_df(df, "crime")
#code: [ilc_mddw03]


crime = eurostat.get_data_df('ilc_mddw03', flags=False)
#'PC': 'Percentage'
#'hhtyp'(TYPE OF HOUSEHOLD): TOTAL
#'incgrp'(INCOME SITUATION) : TOTAL

pd.set_option("display.max_rows", 2193)


#Filtrar por TOTAL em TYPE OF HOUSEHOLD e INCOME SITUATION
crimedf= crime[(crime['hhtyp']=='TOTAL') & (crime['incgrp']=='TOTAL')]

crimedf= crimedf.drop(['hhtyp', 'incgrp', 'unit'], axis=1)
#crimedf = crimedf.reset_index(drop=True)

#Criar coluna country com os dados da coluna geo/time
crimedf['Country'] =crimedf.iloc[:,0]

#Drop coluna geo/time
crimedf.drop(crimedf.columns[0], axis=1, inplace=True)

# get a list of columns
cols = list(crimedf)
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('Country')))
cols
# use ix to reorder
crimedf= crimedf.loc[:, cols]

crimedf.sort_values(by=['Country'])


#DROP ROW WIHT COUNTRY AS EA18
indexNames = crimedf[ crimedf['Country'] == 'EA18' ].index
crimedf.drop(indexNames , inplace=True)


#DROP ROW WIHT COUNTRY AS EA19
indexNames = crimedf[ crimedf['Country'] == 'EA19' ].index
crimedf.drop(indexNames , inplace=True)


#DROP ROW WIHT COUNTRY AS EU27_2007
indexNames = crimedf[ crimedf['Country'] == 'EU27_2007' ].index
crimedf.drop(indexNames , inplace=True)

#DROP ROW WIHT COUNTRY AS EU27_2020
indexNames = crimedf[ crimedf['Country'] == 'EU27_2020' ].index
crimedf.drop(indexNames , inplace=True)

#DROP ROW WIHT COUNTRY AS EU28
indexNames = crimedf[ crimedf['Country'] == 'EU28' ].index
crimedf.drop(indexNames , inplace=True)


#DROP ROW WIHT COUNTRY AS EA
indexNames = crimedf[ crimedf['Country'] == 'EA' ].index
crimedf.drop(indexNames , inplace=True)

#DROP ROW WIHT COUNTRY AS EU
indexNames = crimedf[ crimedf['Country'] == 'EU' ].index
crimedf.drop(indexNames , inplace=True)


crimedf['Country'] = crimedf['Country'].map({'AT': 'Austria', \
                                             'BE':'Belgium', \
                                             'BG': 'Bulgaria',\
                                             'CH':'Switzerland',\
                                             'CY':'Cyprus',\
                                             'CZ':'Czechia',\
                                             'DE':'Germany',\
                                             'DK':'Denmark',\
                                             'EE':'Estonia',\
                                             'EL':'Greece',\
                                             'ES':'Spain',\
                                             'FI':'Finland',\
                                             'FR':'France',\
                                             'HR':'Croatia',\
                                             'HU':'Hungary',\
                                             'IE':'Ireland',\
                                             'IS':'Iceland',\
                                             'IT':'Italy',\
                                             'LT':'Lithuania',\
                                             'LU':'Luxembourg',\
                                             'LV':'Latvia',\
                                             'ME':'Montenegro',\
                                             'MK':'North Macedonia',\
                                             'MT':'Malta',\
                                             'NL':'Netherlands',\
                                             'NO':'Norway',\
                                             'PL':'Poland',\
                                             'PT':'Portugal',\
                                             'RO':'Romania',\
                                             'RS':'Serbia',\
                                             'SE':'Sweden',\
                                             'SI':'Slovenia',\
                                             'SK':'Slovakia',\
                                             'TR':'Turkey',\
                                             'UK':'United Kingdom',\
                                             'XK':'Kosovo'})

    
crimedf