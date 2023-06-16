import os
import json
import pandas as pd


arquivo = pd.DataFrame(columns=['url', 'title', 'categories', 'date of collection', 'passage'])

w = open("basket2.csv", 'w', encoding="utf-8")
w.write("url;title;date of collection;categories;passage\n")

for filename in os.listdir(os.getcwd()):
   print(filename)
   if(filename != "CreateCSV.py" and filename != 'basket.csv' and filename != 'basket2.csv' and filename != 'Dataset_Question_Generation.ipynb'):
      with open(os.path.join(os.getcwd(), filename), 'r') as f:
         data = json.load(f)
         texto = data['text'].replace(";", ",").split(".")

         passagem = ""

         indice =0 
         while(indice < len(texto)):

            passagem = texto[indice] + "."
            indice+=1
            while(len(passagem) < 255 and indice < len(texto)):
                  passagem = passagem + texto[indice] + "."
                  indice+=1

            
            
            if((len(passagem) >= 256 and "http" not in passagem and not passagem.startswith("Expression error:")) or indice == len(texto) - 1):
                  categorias = ""
                  for i in data['categories']:
                      categorias = categorias + "," + i 

                  linha = data['url'] + ";" + data['title'][0] + ";" + data['date'] + ";" + categorias[1:] + ";\"" + passagem + "\""
                  w.write(linha)
                  w.write("\n")
                  
                  


      
