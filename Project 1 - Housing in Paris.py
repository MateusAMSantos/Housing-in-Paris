#!/usr/bin/env python
# coding: utf-8

# # Importing libraries

# In[6]:


import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup as BS
import requests
from time import sleep
from selenium import webdriver
import unicodedata


# # Creating the urls

# In[32]:


base_url = 'https://www.bienici.com/recherche/location/paris-75000/appartement?prix-min=300&prix-max=1000&page='
page_url_num = '1'
add_url = '&mode=liste'
# https://www.bienici.com/recherche/location/paris-75000/appartement?prix-min=300&prix-max=1000&mode=liste
# https://www.bienici.com/recherche/location/paris-75000/appartement?prix-min=300&prix-max=1000&page=2&mode=liste


# In[33]:


url1 = base_url + page_url_num + add_url
print(url1)


# # Extracting the pages information with BeautifulSoup

# In[35]:


options = webdriver.EdgeOptions()
# options.headless = True   # just set it to the headless mode

browser1 = webdriver.Edge(options=options)
browser1.get(url1)

page1 = browser1.page_source

sleep(5)

soup1 = BS(page1, 'html.parser')
soup1.prettify()


# In[36]:


base_url = 'https://www.bienici.com/recherche/location/paris-75000/appartement?prix-min=300&prix-max=1000&page='
page_url_num = '2'
add_url = '&mode=liste'
url2 = base_url + page_url_num + add_url
print(url2)


# In[37]:


base_url = 'https://www.bienici.com/recherche/location/paris-75000/appartement?prix-min=300&prix-max=1000&page='
page_url_num = '3'
add_url = '&mode=liste'
url3 = base_url + page_url_num + add_url
print(url3)


# In[38]:


base_url = 'https://www.bienici.com/recherche/location/paris-75000/appartement?prix-min=300&prix-max=1000&page='
page_url_num = '4'
add_url = '&mode=liste'
url4 = base_url + page_url_num + add_url
print(url4)


# In[45]:


options = webdriver.EdgeOptions()
# options.headless = True   # just set it to the headless mode

browser2 = webdriver.Edge(options=options)
browser2.get(url2)

page2 = browser2.page_source

sleep(40)

soup2 = BS(page2, 'html.parser')
soup2.prettify()


# In[46]:


browser3 = webdriver.Edge(options=options)
browser3.get(url3)

page3 = browser3.page_source

sleep(10)

soup3 = BS(page3, 'html.parser')
soup3.prettify()


# In[47]:


browser4 = webdriver.Edge(options=options)
browser4.get(url4)

page4 = browser4.page_source

sleep(19)

soup4 = BS(page4, 'html.parser')
soup4.prettify()


# In[ ]:





# In[ ]:





# In[ ]:





# # Housing and Surface

# ##### Extracting the type of housing and the surface for all the pages on the BienIci website

# In[48]:


v1 = soup1.find_all('span', attrs={"class":"ad-overview-details__ad-title"})
v1 = [unicodedata.normalize("NFKC", x.get_text(strip=True)) for x in v1]
v1


# In[50]:


v2 = soup2.find_all('span', attrs={"class":"ad-overview-details__ad-title"})
v2 = [unicodedata.normalize("NFKC", x.get_text(strip=True)) for x in v2]
v2


# In[51]:


v3 = soup3.find_all('span', attrs={"class":"ad-overview-details__ad-title"})
v3 = [unicodedata.normalize("NFKC", x.get_text(strip=True)) for x in v3]
v3


# In[52]:


v4 = soup4.find_all('span', attrs={"class":"ad-overview-details__ad-title"})
v4 = [unicodedata.normalize("NFKC", x.get_text(strip=True)) for x in v4]
v4


# ##### Storing the information on a list

# In[61]:


housing = []
housing.extend(v1)
housing.extend(v2)
housing.extend(v3)
housing.extend(v4)
len(housing)


# ##### Separating the surface of the apartment from the housing type

# In[62]:


surface = []

for i in range(0,len(housing)):
    var = [int(j) for j in housing[i].split() if j.isdigit()]
    if int(var[-1]) >= 9:
        var = var[-1]
        surface.append(int(var))
    # print(i, var, surface[i])
    
len(surface)


# In[65]:


var3 = []
for i in range(0,len(housing)):
    var2 = [j for j in housing[i].split() if j.isdigit()==False]# and int(v2[i].split()[-2]) >= 9]
    #var2 = [var2[i].replace(['pièce','pièces','m2'],'').strip() for x in var2[i]]
    var3.append(var2)
    # print(i, v3)#, surface[i])
    
len(var3)


# ###### Using a DataFrame to eliminate undesired names

# In[66]:


columns = ['name1','name2','unused1','unused2']
df1 = pd.DataFrame(var3, columns = columns)
df1


# In[68]:


df2 = df1
df2 = df2.drop(['unused1','unused2'], axis=1)
df2


# ###### Replacing the values in the column 'name2' for 'None'

# In[69]:


var4 = list(df2['name2'])


# In[70]:


var5 = [] # var for eliminating 'pièce' and 'm2'
#v5 = v5.extend([x.replace('pièce','').split() for x in v4])
#v5

var6 = [] # var5 after replacing 'pièce' and 'm2' for 'None'


for i in range(0,len(var4)):
    var5 = var4[i].replace('pièce','None').replace('m2','None').split()
    var6.extend(var5)
    # print(var5,var6)


# ###### Manipulating the names

# In[79]:


var7 = list(df2['name1']) # the first housing name
name = [] # the result

for i in range(0,len(var7)):
    if var6[i] != 'None':
        var = var7[i] + ' ' + var6[i]
    else:
        var = var7[i]
    name.append(var)
    # print(i, name)


# ###### Storing the data into a temporary DataFrame

# In[83]:


t1 = pd.DataFrame([name,surface], index=['Housing','Surface'])
t1 = t1.transpose()
t1


# In[ ]:





# # Price

# ##### Extracting the prices of all the advertisements

# In[84]:


price1 = soup1.find_all('span', {"class":"ad-price__the-price"})
price1 = [unicodedata.normalize("NFKC", x.get_text()) for x in price1]
price1 = [x.strip(' €') for x in price1]


# In[85]:


price2 = soup2.find_all('span', {"class":"ad-price__the-price"})
price2 = [unicodedata.normalize("NFKC", x.get_text()) for x in price2]
price2 = [x.strip(' €') for x in price2]


# In[86]:


price3 = soup3.find_all('span', {"class":"ad-price__the-price"})
price3 = [unicodedata.normalize("NFKC", x.get_text()) for x in price3]
price3 = [x.strip(' €') for x in price3]


# In[87]:


price4 = soup4.find_all('span', {"class":"ad-price__the-price"})
price4 = [unicodedata.normalize("NFKC", x.get_text()) for x in price4]
price4 = [x.strip(' €') for x in price4]


# In[88]:


len(price1)+len(price2)+len(price3)+len(price4)


# ##### Storing everything under the same list

# In[89]:


price = []
price.extend(price1)
price.extend(price2)
price.extend(price3)
price.extend(price4)
len(price)


# ##### Adding it to the temp. dataframe

# In[90]:


t1['Price'] = price
t1


# In[ ]:





# In[ ]:





# # Address

# ##### Extracting the address of all the advertisements

# In[91]:


address1 = soup1.find_all('span', attrs={"class":"ad-overview-details__address-title"})
address1 = [unicodedata.normalize("NFKC", x.get_text()) for x in address1]
address1


# In[92]:


address2 = soup2.find_all('span', attrs={"class":"ad-overview-details__address-title"})
address2 = [unicodedata.normalize("NFKC", x.get_text()) for x in address2]


# In[93]:


address3 = soup3.find_all('span', attrs={"class":"ad-overview-details__address-title"})
address3 = [unicodedata.normalize("NFKC", x.get_text()) for x in address3]


# In[94]:


address4 = soup4.find_all('span', attrs={"class":"ad-overview-details__address-title"})
address4 = [unicodedata.normalize("NFKC", x.get_text()) for x in address4]


# ##### Storing everything under the same variable

# In[95]:


address = []
address.extend(address1)
address.extend(address2)
address.extend(address3)
address.extend(address4)
len(address)


# ##### Separating the complement from the address

# In[121]:


test1 = [x.split('(') for x in address]
test1


# In[ ]:





# In[ ]:





# In[132]:


var1 = [x.split('(') for x in address]
PCQ = [] # Storing the adress into Postal Code, City and Quartier
compl = [] # Alocating the address complement to another variable

for i in range(0,len(var1)):
    a = var1[i] # temp. variable
    if len(a) > 1:
        b = a[0].strip() # temp. var. to store the first string containing postal code, city and quartier
        c = a[1].strip() # temp. var. to store the address complement
    else:
        b = a[0].strip()
        c = 'None'
        
    PCQ.append(b)
    compl.append(c)


# In[135]:


# Removing the ')'
compl = [x.strip(')') for x in compl]


# In[137]:


# Splitting PCQ into a list
PCQ = [x.split() for x in PCQ]
PCQ


# In[147]:


# Storing into another temp. DataFrame
t2 = pd.DataFrame(PCQ, columns= ['Postal Code','City','Quartier'])
t2


# In[148]:


t2['Address'] = compl
t2


# In[149]:


# Adding everything to the final DataFrame
table = pd.concat([t1,t2],axis=1)
table


# In[ ]:





# # Apartment Link

# In[154]:


ap_link1 = soup1.find_all(['div','a'], {"class":"detailsContent adOverview"}) # tag
ap_link1 = [x.find('a').attrs['href'] for x in ap_link1] # text


# In[155]:


ap_link2 = soup2.find_all(['div','a'], {"class":"detailsContent adOverview"})
ap_link2 = [x.find('a').attrs['href'] for x in ap_link2]


# In[156]:


ap_link3 = soup3.find_all(['div','a'], {"class":"detailsContent adOverview"})
ap_link3 = [x.find('a').attrs['href'] for x in ap_link3]


# In[157]:


ap_link4 = soup4.find_all(['div','a'], {"class":"detailsContent adOverview"})
ap_link4 = [x.find('a').attrs['href'] for x in ap_link4]


# In[158]:


ap_link = []
ap_link.extend(ap_link1)
ap_link.extend(ap_link2)
ap_link.extend(ap_link3)
ap_link.extend(ap_link4)
len(ap_link)


# In[160]:


# Completing the link
link = []
for i in range(0,len(ap_link)):
    new = 'https://www.bienici.com' + ap_link[i]
    link.append(new)
    # print(link,'\n')


# # FINAL TABLE

# In[161]:


table['Link'] = link
table


# In[162]:


table.to_csv(r'C:\Users\Mateus de Alencar\Downloads\PortfolioProjects\Housing_Paris.csv', index = False, sep=';')


# In[ ]:




