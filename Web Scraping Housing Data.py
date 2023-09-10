from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import requests

from lxml import etree


last_updated = []
project_name = []
min_price = []
max_price = []
b_y = []
location = []
sizes_type = []
avg_price = []
min_sizes = []
max_sizes = []
project_area = []
project_size = []
launch_date = []
possession_starts = []
configurations = []
rera_id = []
about_project = []
amenities = []
neighbourhood = []
builder_name = []
established_in = []
total_projects = []
about_builder = []
project_page_link = []


driver=webdriver.Chrome()
driver.get('https://housing.com/in/buy/searches/AE0P38f9yfbk7p3m2h1f')

content = driver.page_source

soup = BeautifulSoup(content, features='html.parser')

boxes=[]

for box in soup.find_all('div',{'class' : 'css-2rx1iy'}):
    
    boxes.append(box.find('a')['href'])


for box in boxes:
    print(box)
    response = requests.get('https://housing.com/'+box)
    soup2 = BeautifulSoup(response.content, features='html.parser')
    
    #last_updated
    outerdiv = soup2.find('div', {'class':'css-1iv3lhr'})
    last_updated.append(outerdiv.find('div').text.replace('Last updated: ',''))
    
    #project_name
    outerdiv2 = soup2.find('div', {'class':'css-js5v7e'})
    project_name.append(outerdiv2.find('h1').text)
    
    #min_price
    if ' - ' in soup2.find('div', {'class':'css-1hidc9c'}).text:
        outerdiv3 = soup2.find('div', {'class':'css-1hidc9c'})
        min_price.append(outerdiv3.find('span',{'class' : 'css-19rl1ms'}).text.split(' - ')[0])
        
        #max_price
        outerdiv4 = soup2.find('div', {'class':'css-1hidc9c'})
        max_price.append(outerdiv4.find('span',{'class' : 'css-19rl1ms'}).text.split(' - ')[1])
    
    else:
        outerdiv3 = soup2.find('div', {'class':'css-1hidc9c'})
        min_price.append(outerdiv3.find('span',{'class' : 'css-19rl1ms'}).text)
        max_price.append('empty')
    
    #b_y
    outerdiv5 = soup2.find('div', {'class':'css-1bcji2n'})
    b_y.append(outerdiv5.find('a').find('span').text.strip())
    
    #location
    location.append(soup2.find('div', {'class':'css-1ty5xzi'}).text)
    
    #sizes_type
    sizes_type.append(soup2.find('div', {'class':'css-w788ou'}).text.replace('(','').replace(')',''))
    
    #project area, sizes,project size, launch date, avg. price, possession starts, configurations, rera id
    outertable = soup2.find('div', {'class':'css-fq1k4c'}).find('table',{'class':'css-13o7eu2'})
    headers = outertable.find_all('th',{'class':'css-2fe3eo'})

    title=[]
    for head in headers:
        title.append(head.text)

    empty=['Project Area','Sizes','Project Size','Launch Date','Avg. Price','Possession Starts','Configuration','Rera Id']

    for row in outertable.find_all('tr'):
        
        if row.find('th').text == 'Project Area':
            project_area.append(row.find('td').text)
            empty.remove('Project Area')
        
        if row.find('th').text == 'Sizes':
            min_sizes.append(row.find('td').text.split(' - ')[0])
            max_sizes.append(row.find('td').text.split(' - ')[1])
            empty.remove('Sizes')
        
        if row.find('th').text == 'Project Size':
            project_size.append(row.find('td').text)
            empty.remove('Project Size')
            
        if row.find('th').text == 'Launch Date':
            launch_date.append(row.find('td').text)
            empty.remove('Launch Date')
        
        if row.find('th').text == 'Avg. Price':
            avg_price.append(row.find('td').text)
            empty.remove('Avg. Price')
            
        if row.find('th').text == 'Possession Starts':
            possession_starts.append(row.find('td').text)
            empty.remove('Possession Starts')
        
        if row.find('th').text == 'Configuration' or row.find('th').text == 'Configurations':
            configurations.append(row.find('td').text)
            empty.remove('Configuration')
            
        if row.find('th').text == 'Rera Id':
            rera_id.append(row.find('td').text)
            empty.remove('Rera Id')
            
    for item in empty:
        
        if len(empty)==0:
            break
        
        if item == 'Project Area':
            project_area.append('empty')
        
        if item == 'Sizes':
            min_sizes.append('empty')
            max_sizes.append('empty')
        
        if item == 'Project Size':
            project_size.append('empty')
        
        if item == 'Launch Date':
            launch_date.append('empty')
        
        if item == 'Avg. Price':
            avg_price.append('empty')
        
        if item == 'Possession Starts':
            possession_starts.append('empty')
        
        if item == 'Configuration':
            configurations.append('empty')
        
        if item == 'Rera Id':
            rera_id.append('empty')
     
        
    
    #about_project
    if soup2.find('div', {'class':'css-9sd731'}):
        if 'About' in soup2.find('div', {'class':'css-9sd731'}).find('h2').text:
            about_project.append(soup2.find('div', {'class':'css-9sd731'}).find_all('div')[0].text)
    else:
        about_project.append('no information')
    
    #amenities
    outerdiv9a = soup2.find('div', {'class':'css-a9s06j'})
    outersection9b = outerdiv9a.find('section')
    outerdiv9c = outersection9b.find('div')
    boxes = outerdiv9c.find_all('div')
    facility=set()
    for box in boxes:
        for item in box:
            facility.add(item.text)  
    facility.remove('')
    amenities.append(facility)
    
    # @ neighbourhood @
    outerdiv10a = soup2.find('div', {'class':'section-border'})
    outerdiv10b = outerdiv10a.find('div')
    outerdiv10c = outerdiv10b.find('div')
    outerdiv10d = outerdiv10c.find_all('div')
    neighbourhood.append(outerdiv10d[-1].text)
    
    #builder_name, established_in, total_projects, about_builder, project_page_link
    if soup2.find('section', {'id':'aboutDeveloper'}):
        outerdiv11 = soup2.find('div', {'class':'css-7q4j2k'}).find('div').find('div')
        builder_name.append(outerdiv11.find('h3').find('a').text)
            
        
        outerdiv12a = soup2.find('div', {'class':'css-7q4j2k'}).find('div').find('div')
        outerdiv12b = outerdiv12a.find('h3').find('div')
        outerdiv12c = outerdiv12b.find_all('div',{'class':'css-fpceup'})
        
        if 'Established In' in outerdiv12a.text:
            
            if 'Total Projects' in outerdiv12a.text:
                established_in.append(outerdiv12c[0].find('div',{'class':'css-bu7ujg'}).text)
                total_projects.append(outerdiv12c[1].find('div',{'class':'css-bu7ujg'}).text)
            
        elif 'Established In' in outerdiv12a.text:
            
            established_in.append(outerdiv12c[0].find('div',{'class':'css-bu7ujg'}).text)
            total_projects.append('empty')
        
        elif 'Total Projects' in outerdiv12a.text:
            established_in.append('empty')
            total_projects.append(outerdiv12c[0].find('div',{'class':'css-bu7ujg'}).text)
        
        else:
            established_in.append('empty')
            total_projects.append('empty')
            
        outerdiv14a = soup2.find('div', {'class':'css-7q4j2k'})
        about_builder.append(outerdiv14a.find('div').find('div',{'data-q':'desc'}).text)
    
    
        outerdiv15 = soup2.find('div', {'class':'css-7q4j2k'}).find('div').find('div')
        project_page_link.append('https://housing.com/'+outerdiv15.find('h3').find('a')['href'])    
        
    else:
        builder_name.append('empty')
        established_in.append('empty')
        total_projects.append('empty')
        about_builder.append('empty')
        project_page_link.append('empty')
        


driver.quit()


import pandas as pd

df = pd.DataFrame({'Last updated':last_updated,
                   'Project Name':project_name,
                   'Min Price':min_price,
                   'Max Price':max_price,
                   'By':b_y,
                   'Location':location,
                   'Sizes Type':sizes_type,
                   'Avg. Price':avg_price,
                   'Min Size':min_sizes,
                   'Max Size':max_sizes,
                   'Project Area':project_area,
                   'Project Size':project_size,
                   'Launch Date':launch_date,
                   'Possession Starts':possession_starts,
                   'Configuration':configurations,
                   'Rera Id':rera_id,
                   'About Project':about_project,
                   'Amenities':amenities,
                   'Neighbourhood':neighbourhood,
                   'Builder Name':builder_name,
                   'Established In':established_in,
                   'Total Projects':total_projects,
                   'About Builder':about_builder,
                   'Project Page Link':project_page_link})

df.to_csv('listings.csv', index=False, encoding='utf-8')

