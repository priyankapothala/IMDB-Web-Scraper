import requests
import csv
from bs4 import BeautifulSoup
import re

years = [i for i in range(2000,2020)]
pages = [0,1]

with open("imdb_data.csv", 'w', encoding="utf8", newline='') as output_file: 
    writer = csv.writer(output_file)
    writer.writerow(['imdb_id','name','imdb_rating','year','meta_score','votes','genres','runtime','certificate','revenue'])
    for year in years:
        for page in pages:
            request_url = 'http://www.imdb.com/search/title?release_date='+str(year)+'&sort=num_votes,desc&count=250&start='+str((page*250)+1)
            response = requests.get(request_url)            
            movies = BeautifulSoup(response.text, 'html.parser')
            elements = movies.find_all('div', class_ = 'lister-item mode-advanced')
            for elem in elements:
                nodes = elem.find_all('span', attrs = {'name':'nv'})
                metascore = elem.find('div', class_ = 'ratings-metascore')
                if len(nodes) == 2 and metascore is not None:
                    imdb_id = elem.find('span',class_='userRatingValue')['data-tconst']
                    name = elem.h3.a.text
                    year = int(re.sub("[^0-9]", "", elem.h3.find('span', class_ = 'lister-item-year').text).strip())
                    runtime = int(elem.find('span', class_ = 'runtime').text.replace('min',''))
                    genres = elem.find('span', class_ = 'genre').text.strip()
                    cert = elem.find('span', class_ = 'certificate')
                    metascore = elem.find('div', class_ = 'ratings-metascore').span.text
                    if cert:
                        certificate = elem.find('span', class_ = 'certificate').text
                    else:
                        certificate = 'Not Rated'
                    imdb_rating = float(elem.strong.text)
                    votes = int(nodes[0]['data-value'])
                    revenue = int(nodes[1]['data-value'].replace(',',''))
                    writer.writerow([imdb_id,name,imdb_rating,year,metascore,votes,genres,runtime,certificate,revenue])
