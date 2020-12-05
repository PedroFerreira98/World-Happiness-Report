# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:09:57 2020

@author: pedro
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



#Load every report and create a collum for each dataframe a collumn year
happiness_report2015 = pd.read_csv(r'2015.csv')
happiness_report2015['year'] = 2015

happiness_report2016 = pd.read_csv(r'2016.csv')
happiness_report2016['year']=2016

happiness_report2017 = pd.read_csv(r'2017.csv')
happiness_report2017['year']=2017

happiness_report2018 = pd.read_csv(r'2018.csv')
happiness_report2018['year']=2018

happiness_report2019 = pd.read_csv(r'2019.csv')
happiness_report2019['year']=2019



#Reports from 2018 and 2019 only had a collum with Country or Region, so i'll create a Country table in order to match those tables countries with
# their respective Region. Only on years 2015 and 2016 we had collumns Country and Region, so I've used them both in order to make
# a Country table ( Country/region database)
country2015 = [happiness_report2015['Country'],happiness_report2015['Region']]
country_table2015 = pd.concat(country2015, axis=1, keys=['Country','Region'])

country2016 = [happiness_report2016['Country'],happiness_report2016['Region']]
country_table2016 = pd.concat(country2016, axis=1, keys=['Country','Region'])

country_table = country_table2015.merge(country_table2016, on='Country', how='outer')
country_table['Region_x'].fillna(country_table['Region_y'],inplace=True)
country_table.drop(columns=['Region_y'],inplace=True)
country_table.rename(columns={'Region_x':'Region'},inplace=True)
#country_table['country_id'] = country_table.index



europe_country = country_table.query('Region == "Central and Eastern Europe"')
europe_country = europe_country.append(country_table.query('Region == "Western Europe" ' ))
europe_country.sort_values(by='Country',inplace=True)
europe_country.reset_index(inplace=True)
europe_country.drop(columns='index',inplace=True)
europe_country['country_id']=europe_country.index


countries_to_drop = ['Azerbaijan', 'Albania', 'Armenia', 'Belarus', 'Bosnia and Herzegovina', 'Georgia, Kazakhstan', 'Kosovo', 'Kyrgyzstan', 'Macedonia', \
               'Georgia', 'Moldova', 'North Cyprus', 'Tajikistan','Russia','Ukraine', 'Turkemenistan','Turkmenistan','Kazakhstan', 'Uzbekistan']
    
europe_country = europe_country[~europe_country['Country'].isin(countries_to_drop)]
europe_country.reset_index(inplace=True)
europe_country.drop(columns=['index','country_id'],inplace=True)
europe_country['country_id']=europe_country.index




happiness_report2018.rename(columns={'Country or region':'Country'},inplace=True)
happiness_report2019.rename(columns={'Country or region':'Country'},inplace=True)



### In here I made some changes to Country names, where they changed acrossed the years, so I normalized them
#Fix Trinidad and Tobago / Trinidad & Tobago
happiness_report2018["Country"].replace({"Trinidad & Tobago": "Trinidad and Tobago"}, inplace=True)
happiness_report2019["Country"].replace({"Trinidad & Tobago": "Trinidad and Tobago"}, inplace=True)


#Fix Northern Cyprus / North Cyprus
happiness_report2018["Country"].replace({"Northern Cyprus": "North Cyprus"}, inplace=True)
happiness_report2019["Country"].replace({"Northern Cyprus": "North Cyprus"}, inplace=True)




# There's different collumns across all reports, I have eliminated columns like Confidence Intervas, Dystopia Residual , Overal Rank etc
# I've done this so I have the same collumns on every report
cols_2015 = [2,4,11]
happiness_report2015.drop(happiness_report2015.columns[cols_2015],axis=1,inplace=True)

cols_2016 = [2,4,5,12]
happiness_report2016.drop(happiness_report2016.columns[cols_2016],axis=1,inplace=True)

cols_2017 = [1,3,4,11]
happiness_report2017.drop(happiness_report2017.columns[cols_2017],axis=1,inplace=True)

cols_2018 = [0]
happiness_report2018.drop(happiness_report2018.columns[cols_2018],axis=1,inplace=True)

cols_2019 = [0]
happiness_report2019.drop(happiness_report2019.columns[cols_2019],axis=1,inplace=True)



# This 3 years only had Country collumn, didn't have Region collumn, by doing this I added the region collumn to this tables by merging 
# with the country table, which has for every country their respective region
happiness_report2015 = happiness_report2015.merge(europe_country, left_on='Country', right_on='Country',how='right')
happiness_report2016 = happiness_report2016.merge(europe_country, left_on='Country', right_on='Country',how='right')
happiness_report2017 = happiness_report2017.merge(europe_country, left_on='Country', right_on='Country',how='right')
happiness_report2018 = happiness_report2018.merge(europe_country, left_on='Country', right_on='Country',how='right')
happiness_report2019 = happiness_report2019.merge(europe_country, left_on='Country', right_on='Country',how='right')



#Create ranking for each year, now we can know for each year the ranking of the happiness score of all the countries for that year
happiness_report2015['ranking']=happiness_report2015.index+1
happiness_report2016['ranking']=happiness_report2016.index+1
happiness_report2017['ranking']=happiness_report2017.index+1
happiness_report2018['ranking']=happiness_report2018.index+1
happiness_report2019['ranking']=happiness_report2019.index+1




# Changing collumns names in order to normalize every collumn across all data tables
happiness_report2015.rename(columns={'Economy (GDP per Capita)':'GDP per capita','Health (Life Expectancy)':'Healthy life expectancy', \
                                      'Freedom':'Freedom to make life choices','Trust (Government Corruption)':'Perceptions of corruption', \
                                        'Family':'Family_Social_Support'  },inplace=True)

happiness_report2016.rename(columns={'Economy (GDP per Capita)':'GDP per capita', 'Health (Life Expectancy)':'Healthy life expectancy', \
                                      'Freedom':'Freedom to make life choices','Trust (Government Corruption)':'Perceptions of corruption', \
                                         'Family':'Family_Social_Support'      },inplace=True)
    
happiness_report2017.rename(columns={'Happiness.Score':'Happiness Score','Social support':'Family_Social_Support',\
                                     'Economy..GDP.per.Capita.':'GDP per capita',   'Family':'Family_Social_Support'  , \
                                      'Health..Life.Expectancy.': 'Healthy life expectancy', 'Freedom':'Freedom to make life choices', \
                                       'Trust..Government.Corruption.': 'Perceptions of corruption'     },inplace=True)


happiness_report2018.rename(columns={'Score':'Happiness Score','Social support':'Family_Social_Support'},inplace=True)
happiness_report2019.rename(columns={'Score':'Happiness Score','Social support':'Family_Social_Support'},inplace=True)



happiness_report2015.rename(columns={'Region_x':'Region'},inplace=True)
happiness_report2015.drop(columns='Region_y',inplace=True)


happiness_report2016.rename(columns={'Region_x':'Region'},inplace=True)
happiness_report2016.drop(columns='Region_y',inplace=True)


# Bring data from 5 years to only one dataframe

main_data_report = happiness_report2015.append(happiness_report2016)
main_data_report = main_data_report.append(happiness_report2017)
main_data_report = main_data_report.append(happiness_report2018)
main_data_report = main_data_report.append(happiness_report2019)

## main_data_report columns

#['Country', 'Region',            'Happiness Score',            'GDP per capita',
#  'Family_Social_Support',          'Healthy life expectancy',
#   'Freedom to make life choices',      'Perceptions of corruption',
#       'Generosity',                         'year',                        'ranking']






sns.distplot(happiness_report2016['GDP per capita'],bins=40,axlabel='GDP per capita 2016')


#avg_gdp=pd.DataFrame(main_data_report.groupby(by=['year'])['GDP per capita','Happiness Score','Freedom to make life choices'].mean())


#plt.plot(avg_gdp.index, avg_gdp['GDP per capita'],avg_gdp['Freedom to make life choices'])
#plt.xlim(2014,2020) 


