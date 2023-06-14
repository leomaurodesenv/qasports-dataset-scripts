import os
import json
import pandas as pd

maior_sentenca = 0
maior_passagem = 0
arquivo = pd.DataFrame(columns=['url', 'title', 'categories', 'date of collection', 'passage'])

w = open("football2.csv", 'w', encoding="utf-8")
w.write("url;title;date of collection;categories;passage\n")

for filename in os.listdir(os.getcwd()):
   print(filename)
   if(filename != "CreateCSV.py" and filename != 'football.csv' and filename != 'football2.csv' and filename != 'Dataset_Question_Generation.ipynb'):
      with open(os.path.join(os.getcwd(), filename), 'r') as f:
         data = json.load(f)
         texto = data['text'].split(".")

         passagem = ""

         indice =0 
         while(indice < len(texto)):

            passagem = texto[indice] + "."
            indice+=1
            while(len(passagem) < 255 and indice < len(texto)):
                  passagem = passagem + texto[indice] + "."
                  indice+=1

            
            if(len(passagem) > maior_passagem): maior_passagem = len(passagem)
            
            if((len(passagem) >= 256 and "http" not in passagem and not passagem.startswith("Expression error:")) or indice == len(texto) - 1):
                  categorias = ""
                  for i in data['categories']:
                      categorias = categorias + "," + i 

                  linha = data['url'] + ";" + data['title'][0] + ";" + data['date'] + ";" + categorias[1:] + ";\"" + passagem + "\""
                  w.write(linha)
                  w.write("\n")
                  
                  #arquivo = pd.concat([pd.DataFrame([data['url'], data['title'], data['categories'], data['date'], passagem]), arquivo], ignore_index=True)
                  
                  #arquivo = arquivo.append(dict(zip(arquivo.columns, [data['url'], data['title'], data['categories'], data['date'], passagem])), ignore_index=True)



print(maior_passagem)

      