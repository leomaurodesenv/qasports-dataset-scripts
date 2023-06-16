from datetime import datetime
import json
from bs4 import BeautifulSoup
import os

count = 0
for filename in os.listdir('./soccer_html/'):
    count+=1

    print(count, end=", ")
    print(filename)
    pathHTML = './soccer_html/' + filename
    f = open(pathHTML, 'r') 
    data = json.load(f)
    f.close()

    soup = BeautifulSoup(data['html'], 'html.parser')

    conteudo = soup.find(class_="mw-parser-output")
    
    if(conteudo != None):
        tabela = conteudo.find(class_="infobox")
        if(tabela != None):
            tabela = tabela.extract().get_text()

            tabela = tabela.replace("\\\\\\n", " ")
            tabela = tabela.replace("\\\\n", " ")
            tabela = tabela.replace("\\n", " ")
            tabela = tabela.replace("\n", " ")
            tabela = tabela.replace("\\", "")
            tabela = tabela.replace("    "," ")
            tabela = tabela.replace("   "," ")
            tabela = tabela.replace("  "," ")
            tabela = tabela.replace("\u00a0\u2022\u00a0", " ")
            tabela = tabela.replace("\u2013", "-")
            tabela = tabela.replace("\u2212", " ")
            tabela = tabela.replace("\u00a0", " ")
            tabela = tabela.replace("xe2x80x93", "-")
            tabela = tabela.replace("\u00bd", ".5 ")
            tabela = tabela.replace("\xa0", " ")
            tabela = tabela.replace("\u2022", " ")

            if(tabela.startswith(" NOTE: This")):
                tabela = ""
        else:
            tabela = ""


        data['infobox'] = tabela


        if(conteudo.find(id="toc")!= None):
            toc = conteudo.find(id="toc").extract()

        tabela = conteudo.get_text()

        tabela = tabela.replace("\\\\\\n", " ")
        tabela = tabela.replace("\\\\n", " ")
        tabela = tabela.replace("\\n", " ")
        tabela = tabela.replace("\n", " ")
        tabela = tabela.replace("\\", " ")
        tabela = tabela.replace("      "," ")
        tabela = tabela.replace("     "," ")
        tabela = tabela.replace("    "," ")
        tabela = tabela.replace("   "," ")
        tabela = tabela.replace("  "," ")
        tabela = tabela.replace("\u00a0\u2022\u00a0", " ")
        tabela = tabela.replace("\u2013", "-")
        tabela = tabela.replace("\u2212", " ")
        tabela = tabela.replace("\u00a0", " ")
        tabela = tabela.replace("xe2x80x93", "-")
        tabela = tabela.replace("\u00bd", ".5 ")
        tabela = tabela.replace("\xa0", " ")
        tabela = tabela.replace("\u2022", " ")

        tabela = tabela.split("See also")[0]
        tabela = tabela.split("External links")[0]
        tabela = tabela.split("References")[0]
        
        data['text'] = tabela
        data.pop('html')


        pathFINAL = './soccer/' + filename
        f = open(pathFINAL, 'w')
        f.write(json.dumps(data))
        f.close()



