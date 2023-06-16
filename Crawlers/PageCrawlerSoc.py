import requests 
from bs4 import BeautifulSoup 
import csv
from datetime import datetime
 
# Lista para armazenar as URLs 
linha_csv = [] 
wiki_url = []
other_url = []
broken_url = []

controle = []


NLinks = 0


def Request(url, url_wiki):
    
    NLinks = len(url_wiki)
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser") 
        soup =  soup.body.contents[7].contents[5].contents[3]

        links = soup.find_all("a")
        urls_and_titles = [(link.get("href")) for link in links]

        
        #print(urls_and_titles)

        alternador = 1
        proxima = -1

        for i in urls_and_titles:
            print(i)
            if(i not in url_wiki):
                if i is not None and "/wiki" in i: 
                    if i.startswith("https://football.fandom.com"):
                        NLinks += 1

                        linha_csv.append([i])
                        wiki_url.append(i)
                    else: 
                        i = 'https://football.fandom.com' + i # adiciona o prefixo da URL 
                        NLinks+=1

                        linha_csv.append([i])
                        wiki_url.append(i)
        

            elif i == "/Blog:Recent_posts": 
                i = 'https://football.fandom.com' + i
                NLinks+=1
                
                linha_csv.append([i])
                wiki_url.append(i)
            else: 
                other_url.append((i)) 

            if(i.startswith('https://football.fandom.com/wiki/Special:AllPages')) : 
                if(alternador == -1 or NLinks < 376):
                    #print(i)
                    if i not in controle:
                        controle.append(i)
                        proxima = i
                    
                    alternador = alternador *-2
                else:
                    alternador = alternador*-1
            
        if(proxima != -1):
            Request(proxima, url_wiki)
    

        return
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("erro")
        broken_url.append(url)
        return
    
Request('https://football.fandom.com/wiki/Special:AllPages', wiki_url)

#print(linha_csv)
print("---------------------------------------------------------------")
#print(wiki_url)

with open('url_socc.txt', 'w') as file: 
            
    writer = csv.writer(file)
    header = ['id', 'url']
    writer.writerow(header)

    cont = 0
    for i in linha_csv: 
        cont+=1
        if(i[0] != None):
            writer.writerow([i,cont])
        
    
with open('wrong_links.txt', 'w') as file:
    
    lista = []
    for url in other_url: 
        if(url != None):
            #cont+=1
            #linha = str(cont) + ', ' + title +", " + url
            #file.wri(url)
            url = url + '\n'
            lista.append(url)

    print(len(broken_url))
    
    file.writelines(lista)

