# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:09:57 2020

@author: pedro
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import alcohol as alcohol
import crime as crime
import metereology as meteorology
import suicide_rate as suicide
import numpy as np
#from heatmap import heatmap, corrplot
import altair as alt
import matplotlib as mpl



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
europe_country['index']=europe_country.index




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
                                      'Freedom':'Freedom to make life choices','Trust (Government Corruption)':'Government trust', \
                                        'Family':'Family_Social_Support'  },inplace=True)

happiness_report2016.rename(columns={'Economy (GDP per Capita)':'GDP per capita', 'Health (Life Expectancy)':'Healthy life expectancy', \
                                      'Freedom':'Freedom to make life choices','Trust (Government Corruption)':'Government trust', \
                                         'Family':'Family_Social_Support'      },inplace=True)
    
happiness_report2017.rename(columns={'Happiness.Score':'Happiness Score','Social support':'Family_Social_Support',\
                                     'Economy..GDP.per.Capita.':'GDP per capita',   'Family':'Family_Social_Support'  , \
                                      'Health..Life.Expectancy.': 'Healthy life expectancy', 'Freedom':'Freedom to make life choices', \
                                       'Trust..Government.Corruption.': 'Government trust'     },inplace=True)


happiness_report2018.rename(columns={'Score':'Happiness Score','Social support':'Family_Social_Support','Perceptions of corruption':'Government trust'},inplace=True)
happiness_report2019.rename(columns={'Score':'Happiness Score','Social support':'Family_Social_Support','Perceptions of corruption':'Government trust'},inplace=True)



happiness_report2015.rename(columns={'Region_x':'Region'},inplace=True)
happiness_report2015.drop(columns='Region_y',inplace=True)


happiness_report2016.rename(columns={'Region_x':'Region'},inplace=True)
happiness_report2016.drop(columns='Region_y',inplace=True)





# Bring data from 5 years to only one dataframe
# If don't want to use a dataframe with every report, we can also use report of each year

main_data_report = happiness_report2015.append(happiness_report2016)
main_data_report = main_data_report.append(happiness_report2017)
main_data_report = main_data_report.append(happiness_report2018)
main_data_report = main_data_report.append(happiness_report2019)

## main_data_report columns

#['Country', 'Region',            'Happiness Score',            'GDP per capita',
#  'Family_Social_Support',          'Healthy life expectancy',
#   'Freedom to make life choices',      'Perceptions of corruption',
#       'Generosity',                         'year',                        'ranking']





## Here we have all dataframes done for each metric

alcohol_table = alcohol.get_alcohol_table()
crime_table = crime.get_crime_table()
meteorology_table = meteorology.get_meteorology_table()
suicide_table = suicide.get_suicide_rate()

alcohol_table.query('Alcohol_type == "All types"',inplace=True)
alcohol_table.drop(columns=['Alcohol_type','Region'],inplace=True)




#Dataframes with one value per country
alcohol_table['Alcohol Consumption (in litres)'] = alcohol_table['Alcohol Consumption (in litres)'].astype(float)
alcohol_table_mean = pd.DataFrame(alcohol_table.groupby(by='Country',as_index=False)['Alcohol Consumption (in litres)'].mean())

crime_table['Crime_Value'] = crime_table['Crime_Value'].astype(float)
crime_table_mean = pd.DataFrame(crime_table.groupby(by='Country',as_index=False)['Crime_Value'].mean())

suicide_table['Suicide_Value'] = suicide_table['Suicide_Value'].astype(float)
suicide_table_mean = pd.DataFrame(suicide_table.groupby(by='Country',as_index=False)['Suicide_Value'].mean())




main_data_report_mean = main_data_report.merge(alcohol_table_mean, on='Country', how='inner')
main_data_report_mean = main_data_report_mean.merge(crime_table_mean, on='Country', how='inner')
main_data_report_mean = main_data_report_mean.merge(suicide_table_mean, on='Country', how='inner')

main_data_report_mean = main_data_report_mean.merge(meteorology_table, on='Country', how='inner')
main_data_report_mean.rename(columns={'index_x':'index'},inplace=True)
main_data_report_mean.drop(columns='index_y',inplace=True)





'''

main_data_report = main_data_report.merge(alcohol_table, on='Country', how='inner')

main_data_report = main_data_report.merge(crime_table, on='Country', how='inner')

main_data_report = main_data_report.merge(meteorology_table, on='Country', how='inner')
main_data_report.rename(columns={'index_x':'index'},inplace=True)
main_data_report.drop(columns='index_y',inplace=True)

main_data_report = main_data_report.merge(suicide_table, on='Country', how='inner')

'''



###### Visualizations


'''
main_data_report.drop(columns=['year','index','ranking'],inplace=True)

main_data_corr = main_data_report.corr()
mask = np.triu(np.ones_like(main_data_corr,dtype=bool))

corrplot(main_data_corr)
'''


#### Correlation between metrics

'''
plt.clf()
plt.rcdefaults()
sns.reset_defaults()
mpl.rc_file_defaults()

mpl.style.use('classic')

mpl.rcParams.update(mpl.rcParamsOrig)
mpl.rcParams.update(mpl.rcParamsDefault)
'''
'''
main_data_report_mean.drop(columns=['year','index','ranking'],inplace=True)

main_data_corr = main_data_report_mean.corr()
mask = np.triu(np.ones_like(main_data_corr,dtype=bool))
f , ax = plt.subplots(figsize=(20,15))

cmap  = sns.diverging_palette(20,230,as_cmap=True)

fig = sns.heatmap(main_data_corr, mask=mask,cmap=cmap,annot=True,vmax=1,vmin=-1 \
            ,center=0,square=True,linewidths=1)
plt.title('Correlation between metrics')
fig.set_xticklabels(fig.get_xticklabels(),rotation=45,horizontalalignment='right')
a = fig.get_figure()
a.savefig('Correlation between metrics')
'''



##### Distribution of GDP per capita across Countries trough the years

#fig = sns.catplot(x="GDP per capita", y="year",hue='Country',s=14,height=10,kind="swarm",palette=sns.color_palette(), orient="h",data=main_data_report)
#fig.set(ylabel="Year")
#fig.savefig("Distribution of GDP per capita across Countries trough the years.png")




###### correlation between Happiness Score and Freedom to make choices
#plt.scatter(main_data_report['Happiness Score'],main_data_report['Freedom to make life choices'],c = 'green')





###### correlation between Happiness Score and Generosity

#sns.lmplot('Happiness Score', 'Generosity',col='year', data=main_data_report, hue='Country', fit_reg=False)






##### Distribution of Happiness Score across Countries trough the years
#sns.catplot(x="Happiness Score", y="year",hue='Country',kind="swarm",palette=sns.color_palette(), orient="h",data=main_data_report)





##### Distribution of Happiness across Countries through the years ( Heatmap )
'''
main_data_report = main_data_report.pivot("Country", "year", "Happiness Score")
main_data_report.sort_values(main_data_report.max().idxmax(), ascending=False,inplace=True)
plt.figure(figsize=(20,20))

fig = sns.heatmap(main_data_report, cmap="YlGnBu",annot=True,fmt=".3f")
fig.set(xlabel="Year")
plt.title('Happiness Score')
#a.savefig("output.png")

a = fig.get_figure()
a.savefig('Happiness Score through years by Country')
'''




### Alcohol vs Hapiness Score

'''
alcohol_table_2015 = alcohol_table.query('Alcohol_year == 2015')
alcohol_table_2016 = alcohol_table.query('Alcohol_year == 2016')
alcohol_table_2017 = alcohol_table.query('Alcohol_year == 2017')
alcohol_table_2018 = alcohol_table.query('Alcohol_year == 2018')


happiness_report2018_countries = happiness_report2018.query('ranking <= 15')
countries_to_plot = list(happiness_report2018_countries['Country'])

happiness_report2015_countries = happiness_report2015[happiness_report2015['Country'].isin(countries_to_plot)]
happiness_report2016_countries = happiness_report2016[happiness_report2017['Country'].isin(countries_to_plot)]
happiness_report2017_countries = happiness_report2017[happiness_report2017['Country'].isin(countries_to_plot)]
happiness_report2018_countries = happiness_report2018[happiness_report2018['Country'].isin(countries_to_plot)]




happiness_report2015_alcohol =  happiness_report2015.merge(alcohol_table_2015,on='Country',how='left')
happiness_report2015_alcohol.drop(columns='Alcohol_year',inplace=True)

happiness_report2016_alcohol =  happiness_report2016.merge(alcohol_table_2016,on='Country',how='left')
happiness_report2016_alcohol.drop(columns='Alcohol_year',inplace=True)

happiness_report2017_alcohol =  happiness_report2017.merge(alcohol_table_2017,on='Country',how='left')
happiness_report2017_alcohol.drop(columns='Alcohol_year',inplace=True)

happiness_report2018_alcohol =  happiness_report2018.merge(alcohol_table_2018,on='Country',how='left')
happiness_report2018_alcohol.drop(columns='Alcohol_year',inplace=True)

data_happiness_alcohol= happiness_report2015_alcohol.append(happiness_report2016_alcohol)
data_happiness_alcohol= data_happiness_alcohol.append(happiness_report2017_alcohol)
data_happiness_alcohol= data_happiness_alcohol.append(happiness_report2018_alcohol)


data_happiness_alcohol = data_happiness_alcohol[['Country','Happiness Score','year','Alcohol Consumption (in litres)']]
'''

###### Alcohol values thourgh years
'''
alcohol_chart = alt.Chart(data_happiness_alcohol).mark_bar().encode(
    x='Country',
    y='Alcohol Consumption (in litres)',
    column='year',
    color='Country'
).properties(
    width=450,
    height=750
)

alcohol_chart.save('Alcohol_year.html')


'''


##### Alcohol vs Happiness Score through years
## Top 15 from 2018

'''
Select_Year = alt.selection_single(
    name='Select', fields=['year'], init={'year': 2015},
    bind=alt.binding_range(min=2015, max=2018, step=1)
)

data_happiness_alcohol['Alcohol Consumption (in litres)']=data_happiness_alcohol['Alcohol Consumption (in litres)'].astype(float)

alcohol_year = alt.Chart(data_happiness_alcohol).mark_point(filled=True).encode(
    alt.X('Alcohol Consumption (in litres)',scale=alt.Scale(domain=(4, 18))),
    alt.Y('Happiness Score',scale=alt.Scale(domain=(4, 9))),
    alt.Color('Country'),
    alt.OpacityValue(0.7),
    tooltip = [alt.Tooltip('Country:N'),
               alt.Tooltip('Alcohol Consumption (in litres):Q'),
               alt.Tooltip('Happiness Score:Q'),
               #alt.Tooltip('US_Gross:Q')
              ]
)

a = alcohol_year + alcohol_year.transform_regression('Alcohol Consumption (in litres)','Happiness Score').mark_line()

b = alt.layer(alcohol_year, a).properties(
    width=1600, height=800
).add_selection(Select_Year).transform_filter(Select_Year).configure_point(
    size=500
).configure_axis(
    labelFontSize=15,
    titleFontSize=15).configure_legend(
    labelFontSize=20
) 

b.save('Alcohol_Year_Happiness.html')

'''
##### Crime vs Happiness Score through years
## Top 15 from 2019

'''
crime_table_2015 = crime_table.query('Crime_year == 2015')
crime_table_2016 = crime_table.query('Crime_year == 2016')
crime_table_2017 = crime_table.query('Crime_year == 2017')
crime_table_2018 = crime_table.query('Crime_year == 2018')
crime_table_2019 = crime_table.query('Crime_year == 2019')



happiness_report2019_countries = happiness_report2019.query('ranking <= 15')
countries_to_plot = list(happiness_report2019_countries['Country'])

happiness_report2015_countries = happiness_report2015[happiness_report2015['Country'].isin(countries_to_plot)]
happiness_report2016_countries = happiness_report2016[happiness_report2017['Country'].isin(countries_to_plot)]
happiness_report2017_countries = happiness_report2017[happiness_report2017['Country'].isin(countries_to_plot)]
happiness_report2018_countries = happiness_report2018[happiness_report2018['Country'].isin(countries_to_plot)]




happiness_report2015_crime =  happiness_report2015.merge(crime_table_2015,on='Country',how='left')
happiness_report2015_crime.drop(columns='Crime_year',inplace=True)

happiness_report2016_crime =  happiness_report2016.merge(crime_table_2016,on='Country',how='left')
happiness_report2016_crime.drop(columns='Crime_year',inplace=True)

happiness_report2017_crime =  happiness_report2017.merge(crime_table_2017,on='Country',how='left')
happiness_report2017_crime.drop(columns='Crime_year',inplace=True)

happiness_report2018_crime =  happiness_report2018.merge(crime_table_2018,on='Country',how='left')
happiness_report2018_crime.drop(columns='Crime_year',inplace=True)

happiness_report2019_crime =  happiness_report2019.merge(crime_table_2019,on='Country',how='left')
happiness_report2019_crime.drop(columns='Crime_year',inplace=True)

data_happiness_crime= happiness_report2015_crime.append(happiness_report2016_crime)
data_happiness_crime= data_happiness_crime.append(happiness_report2017_crime)
data_happiness_crime= data_happiness_crime.append(happiness_report2018_crime)
data_happiness_crime= data_happiness_crime.append(happiness_report2019_crime)

data_happiness_crime = data_happiness_crime[['Country','Happiness Score','year','Crime_Value']]


Select_Year = alt.selection_single(
    name='Select', fields=['year'], init={'year': 2015},
    bind=alt.binding_range(min=2015, max=2019, step=1)
)


crime_year = alt.Chart(data_happiness_crime).mark_point(filled=True).encode(
    alt.X('Crime_Value',scale=alt.Scale(domain=(0, 27))),
    alt.Y('Happiness Score',scale=alt.Scale(domain=(4, 9))),
    alt.Color('Country'),
    alt.OpacityValue(0.7),
    tooltip = [alt.Tooltip('Country:N'),
               alt.Tooltip('Crime_Value:Q'),
               alt.Tooltip('Happiness Score:Q'),
               #alt.Tooltip('US_Gross:Q')
              ]
)


#alcohol_year.save('Crime_Year_Happiness.html')


a = crime_year + crime_year.transform_regression('Crime_Value','Happiness Score').mark_line()

b = alt.layer(crime_year, a).properties(
    width=1600, height=800
).add_selection(Select_Year).transform_filter(Select_Year).configure_point(
    size=500
).configure_axis(
    labelFontSize=15,
    titleFontSize=15).configure_legend(
    labelFontSize=20
) 

b.save('Crime_Happiness.html')
'''

##### Suicide vs Happiness Score through years
## Top 15 from 2016


suicide_table['Suicide_year']=suicide_table['Suicide_year'].astype(int)

suicide_table_2015 = suicide_table.query('Suicide_year == 2015')
suicide_table_2016 = suicide_table.query('Suicide_year == 2016')

alcohol_table_2015 = alcohol_table.query('Alcohol_year == 2015')
alcohol_table_2016 = alcohol_table.query('Alcohol_year == 2016')


happiness_report2016_countries = happiness_report2016.query('ranking <= 15')
countries_to_plot = list(happiness_report2016_countries['Country'])

happiness_report2015_countries = happiness_report2015[happiness_report2015['Country'].isin(countries_to_plot)]
happiness_report2016_countries = happiness_report2016[happiness_report2017['Country'].isin(countries_to_plot)]



happiness_report2015_suicide =  happiness_report2015.merge(suicide_table_2015,on='Country',how='left')
happiness_report2015_suicide.drop(columns='Suicide_year',inplace=True)
happiness_report2015_suicide =  happiness_report2015_suicide.merge(alcohol_table_2015,on='Country',how='left')
happiness_report2015_suicide.drop(columns='Alcohol_year',inplace=True)



happiness_report2016_suicide =  happiness_report2016.merge(suicide_table_2016,on='Country',how='left')
happiness_report2016_suicide.drop(columns='Suicide_year',inplace=True)
happiness_report2016_suicide =  happiness_report2016_suicide.merge(alcohol_table_2016,on='Country',how='left')
happiness_report2016_suicide.drop(columns='Alcohol_year',inplace=True)



data_happiness_suicide= happiness_report2015_suicide.append(happiness_report2016_suicide)


data_happiness_suicide = data_happiness_suicide[['Country','Happiness Score','year','Suicide_Value','Alcohol Consumption (in litres)']]

'''

Select_Year = alt.selection_single(
    name='Select', fields=['year'], init={'year': 2015},
    bind=alt.binding_range(min=2015, max=2016, step=1)
)


suicide_year = alt.Chart(data_happiness_suicide).mark_point(filled=True).encode(
    alt.X('Suicide_Value',scale=alt.Scale(domain=(3, 36))),
    alt.Y('Happiness Score',scale=alt.Scale(domain=(4, 9))),
    alt.Color('Country'),
    alt.OpacityValue(0.7),
    tooltip = [alt.Tooltip('Country:N'),
               alt.Tooltip('Suicide_Value:Q'),
               alt.Tooltip('Happiness Score:Q'),
               #alt.Tooltip('US_Gross:Q')
              ]
)




a = suicide_year + suicide_year.transform_regression('Suicide_Value','Happiness Score').mark_line()

b = alt.layer(suicide_year, a).properties(
    width=1600, height=800
).add_selection(Select_Year).transform_filter(Select_Year).configure_point(
    size=500
).configure_axis(
    labelFontSize=15,
    titleFontSize=15).configure_legend(
    labelFontSize=20
) 


b.save('Suicide_Year_Happiness.html')
'''

##### Mereology vs Happiness Score

happiness_report2015_countries = happiness_report2015.query('ranking <= 15')
happiness_report2016_countries = happiness_report2016.query('ranking <= 15')
happiness_report2017_countries = happiness_report2017.query('ranking <= 15')
happiness_report2018_countries = happiness_report2018.query('ranking <= 15')
happiness_report2019_countries = happiness_report2019.query('ranking <= 15')

meteo_happiness_data = happiness_report2015.append(happiness_report2016)
meteo_happiness_data = meteo_happiness_data.append(happiness_report2017)
meteo_happiness_data = meteo_happiness_data.append(happiness_report2018)
meteo_happiness_data = meteo_happiness_data.append(happiness_report2019)



meteorlogy_happiness_data = meteo_happiness_data.merge(meteorology_table, on='Country',how='left')
meteorlogy_happiness_data = meteorlogy_happiness_data[['Country','Happiness Score','Hours of Sun','year']]

'''
fig = alt.Chart(meteorlogy_happiness_data).mark_bar().encode(
    x=('Hours of Sun:Q'),
    y=('Happiness Score:Q'),
    color=('Country:N'),
    row=('year:N')
)
fig.save('Meteorology_Year_Happiness.html')
'''
'''
meteorlogy_happiness_data['Happiness Score']=meteorlogy_happiness_data['Happiness Score'].astype(float)


fig = alt.Chart(meteorlogy_happiness_data).mark_bar().encode(
    column='year',
    x='Happiness Score:Q',
    y=alt.Y('Country', sort=alt.SortField(field="Happiness Score", order='ascending')),
    color='Hours of Sun'
).properties(width=220)

fig.save('Meteorology_Year_Happiness.html')


Select_Year = alt.selection_single(
    name='Select', fields=['year'], init={'year': 2015},
    bind=alt.binding_range(min=2015, max=2016, step=1)
)


meteo_year = alt.Chart(meteorlogy_happiness_data).mark_point(filled=True).encode(
    alt.X('Hours of Sun',scale=alt.Scale(domain=(3, 36))),
    alt.Y('Happiness Score',scale=alt.Scale(domain=(4, 9))),
    alt.Color('Country'),
    alt.OpacityValue(0.7),
    tooltip = [alt.Tooltip('Country:N'),
               alt.Tooltip('Hours of Sun:Q'),
               alt.Tooltip('Happiness Score:Q'),
               #alt.Tooltip('US_Gross:Q')
              ]
)




a = meteo_year + meteo_year.transform_regression('Hours of Sun','Happiness Score').mark_line()

b = alt.layer(meteo_year, a).properties(
    width=1600, height=800
).add_selection(Select_Year).transform_filter(Select_Year).configure_point(
    size=500
).configure_axis(
    labelFontSize=15,
    titleFontSize=15).configure_legend(
    labelFontSize=20
) 


b.save('HoursSun_Year_Happiness.html')
'''



data_happiness_suicide = data_happiness_suicide[['Country','Happiness Score','year','Suicide_Value','Alcohol Consumption (in litres)']]
data_happiness_suicide = data_happiness_suicide.query('year == 2016')



suicide_alcohol = alt.Chart(data_happiness_suicide).mark_point().encode(
    x=alt.X('Suicide_Value',scale=alt.Scale(domain=(2, 29))),
    y=alt.Y('Alcohol Consumption (in litres)',scale=alt.Scale(domain=(5, 17))),
    color='Country'
)

a = suicide_alcohol + suicide_alcohol.transform_regression('Suicide_Value', 'Alcohol Consumption (in litres)').mark_line()
b = alt.layer(suicide_alcohol, a).properties(
    width=800, height=600
)


b.save('Alcohol_suicide.html')


data_happiness_suicide = data_happiness_suicide.merge(meteorology_table, on='Country',how='left')
#data_happiness_suicide = data_happiness_suicide.query('year == 2019')


suicide_sun = alt.Chart(data_happiness_suicide).mark_point().encode(
    x=alt.X('Suicide_Value',scale=alt.Scale(domain=(2, 29))),
    y=alt.Y('Hours of Sun',scale=alt.Scale(domain=(1100, 3400))),
    color='Country'
)

a = suicide_sun + suicide_sun.transform_regression('Suicide_Value', 'Hours of Sun').mark_line()
b = alt.layer(suicide_sun, a).properties(
    width=800, height=600
)


b.save('Sun_suicide.html')
