import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk import PorterStemmer

path = 'C:\\Users\\pakistan\\Desktop\\IR\\corpus\\corpus\\corpus'
doc_files = open('docids.txt', 'a')
stop = []
tok = []

#r = root, d = directory, f = files
for r, d, f in os.walk(path):
    for file in f:
        file_name = os.path.join(r, file)
        #name = os.path.basename(file_name)
        #doc_files.write(name + "\n")
        with open(file_name) as query:
            
            file = open('stoplist.txt', 'r')
            #print("reading file\n")
            stopL = file.readlines()
            for stops in stopL:
                stop.append(str(stops[:-1]))
    
            try:
                #print("Reading file\n")
                soup = BeautifulSoup(query.read(), 'lxml')
               
                #kill all script and style elements
                for script in soup(["script", "style"]):
                    script.extract()    # rip it out
                
                #get text
                text = soup.get_text()
                #print(text)
                
                #break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
                
                #break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                
                # drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)
                
                #print(text)
                
                #make tokens of the text
                tokens = word_tokenize(text)
                temp = []
                
                for token in tokens:
                    temp.append(str(token).lower())
                
                #print(temp)
                
                for s in stop:
                    if s in temp:
                        temp.remove(s)
                
                for t in temp:
                    tok.append(str(PorterStemmer().stem(t)))
                #print(tok)
         
            except:
                   pass
doc_files.close()               