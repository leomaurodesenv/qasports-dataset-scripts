import requests
from datetime import datetime
import json
from bs4 import BeautifulSoup
import csv

def FetchHtml(url):
    
    try:
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        FileName = "./basketball/" + soup.title.contents[0].split("|")[0][0:-1].replace(" ","_").replace("/", "_").replace(":", "_") + '.json'

        f = open(FileName, 'w')

        instancia = {}

        instancia['url'] = url
        instancia['title'] = soup.title.contents

        #CATEGORIAS
        cat = soup.find(class_="page-header__categories")
        

        if(cat != None):
            cat = cat.get_text().split('\n')
            if("\t" in cat[-1]):
                todas = cat[2:-1][0]
            else:
                todas = cat[2:][0]
        else:
            todas = " "
        

        cat = soup.find(class_="page-header__categories-dropdown-content")
        if(cat != None):
            cat = cat.get_text().split('\n')
            for i in range(0, len(cat)):
                if(i != ''):
                    todas = todas + "," + cat[i]
            todas = todas.split(",")
        else:
            if(todas != " "):
                todas=todas.split(',')
        
        categorias = []
        if(todas != " "):
            for i in todas:
                if(i != ',' and i != 'and' and i != '' and i != ' \t\t\t'):
                    categorias.append(i)

        #print(categorias)
        instancia['categories'] = categorias

        #DATA DE COLETA
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        instancia['date'] = dt_string


        instancia['html'] =  str(response.content, encoding='UTF-8')
        #print(instancia)

        f.write(json.dumps(instancia))

        f.close()
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("erro")
        FetchHtml(url)



with open('url_bask_clean.txt', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if(row != []):
                    url = row[1]
                    line_count+=1
                    print(line_count)
                    FetchHtml(url)
            else:
                line_count+=1
