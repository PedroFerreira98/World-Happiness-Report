from bs4 import BeautifulSoup
import requests
import pandas as pd

##Use the url to get the html code
url = "https://en.wikipedia.org/wiki/List_of_cities_by_sunshine_duration"
response = requests.get(url)

#Turn it into soup
soup = BeautifulSoup(response.content, features = "lxml")
print(soup.prettify())

#Store the table I want in a variable
tables = soup.find_all('table', attrs= {'class' : "wikitable plainrowheaders sortable"})
table = tables[2]

#Get the columns of the table, and then get the content of each column
header = [th.text.rstrip() for th in table.find_all('th')]
c1 =  []
c2 = []
c3 = []
c4 = []
c5 = []
c6 = []
c7 = []
c8 = []
c9 = []
c10 = []
c11 = []
c12 = []
c13 = []
c14 = []
c15 = []
c16 = []


for col in table.find_all('tr'):
    cells = col.find_all('td')
    if len(cells) > 0:
        c1.append(cells[0].find(text=True))
        c2.append(cells[1].find(text=True))
        c3.append(cells[2].find(text=True))
        c4.append(cells[3].find(text=True))
        c5.append(cells[4].find(text=True))
        c6.append(cells[5].find(text=True))
        c7.append(cells[6].find(text=True))
        c8.append(cells[7].find(text=True))
        c9.append(cells[8].find(text=True))
        c10.append(cells[9].find(text=True))
        c11.append(cells[10].find(text=True))
        c12.append(cells[11].find(text=True))
        c13.append(cells[12].find(text=True))
        c14.append(cells[13].find(text=True))
        c15.append(cells[14].find(text=True))
        c16.append(cells[15].find(text=True))
    
#Create the dict to store the data
d = dict([x,0] for x in header)

#Populate the dict
d['Country'] = c1
d['City'] = c2
d['Jan'] = c3
d['Feb'] = c4
d['Mar'] = c5
d['Apr'] = c6
d['May'] = c7
d['Jun'] = c8
d['Jul'] = c9
d['Aug'] = c10
d['Sep'] = c11
d['Oct'] = c12
d['Nov'] = c13
d['Dec'] = c14
d['Year'] = c15
d['Ref.'] = c16

#Turn the dict into a data frame
hours_of_sun = pd.DataFrame(d)

#Clean the 'Year' column
year_cleaned = []

for a in list(hours_of_sun['Year']):
    x = a.replace('\n', '')               #We need to take the '\n' with the replace method
    x = float(x.replace(',', '.')[:5])    #Since the ',' don't allow us to convert directly to float we need to replace the 
                                          #',' with '.'  and select only the first 5 characters so we don't end up with
                                          #numbers like 2.393.3 what aren't convertable to float
    x = x*1000                            #Since the numbers are now intepreted as 1000 times smaller we need to multiply by 1000
    year_cleaned.append(x)                

year_cleaned[15] = year_cleaned[15]/1000                #We divide the element in the 15th position of the list by 1000, because since he dind't have any commas
                                                        #he didn't suffered any changes but we still multipied him by 1000

#Create a new dataframe with a slice of the original dataframe and add the new cleaned 'Year' column
hours_of_sun_year = hours_of_sun[['Country', 'City']]
hours_of_sun_year['Metereology_year'] = year_cleaned
hours_of_sun_year.columns = ['Country', 'City', 'Hours of Sun']

#Groupby country
hours_of_sun_year_by_country = hours_of_sun_year.groupby('Country', as_index = False).agg('mean')

#Drop columns that we don't need
cols_to_drop = ['Armenia', 'Albania', 'Belarus', 'Bosnia and Herzegovina', 'Georgia', 'Faroe Islands', 'Moldova', 'Monaco', 'North Macedonia', 'Russia', 'Turkey', 'Ukraine']
hours_of_sun_year_by_country = hours_of_sun_year_by_country[~hours_of_sun_year_by_country['Country'].isin(cols_to_drop)]

#Create ordered index
hours_of_sun_year_by_country.reset_index(inplace=True)
hours_of_sun_year_by_country.drop(columns='index', inplace = True)
hours_of_sun_year_by_country['index']=hours_of_sun_year_by_country.index

#Print final table
print(hours_of_sun_year_by_country)

def get_meteorology_table():
    return hours_of_sun_year_by_country

