import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk import PorterStemmer
import re
import codecs
import json
from gensim.corpora import Dictionary

path = r'C:\\Users\\pakistan\\Desktop\\IR\\Assignment-1\\corpus\\corpus\\corpus'
subpath = r'C:\\Users\\pakistan\\Desktop\\IR\\Assignment-1'
index = 0

#r = root, d = directory, f = files
def process_files(filenames):
    file_to_terms = {}
    for file in filenames:
        stopwords = open('stoplist.txt', 'r')
        #ids = open('termids.txt', 'w', encoding="utf-8")
        sp = stopwords.readlines()
        pattern = re.compile('[\W_]+')
        
        with codecs.open(filenames, encoding="utf-8", errors = 'ignore') as query:
            soup = BeautifulSoup(query.read(), 'lxml').find('html')

            #kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
        
            #get text
            text = soup.get_text()
                
            file_to_terms[file] = text.lower();
            file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
            re.sub(r'[\W_]+','', file_to_terms[file])
            #file_to_terms[file] = file_to_terms[file].split()
            file_to_terms[file] = word_tokenize(file_to_terms[file])
                       
            file_to_terms[file] = [w for w in file_to_terms[file] if w not in sp]
            
            print("stemming...\n")                
            file_to_terms[file] = [PorterStemmer().stem(w) for w in file_to_terms[file]]
            
            print("File pre processed.... returning:\n")
            print(file_to_terms[file]) 
            '''
            print("copying to file")
            temp = [data.split() for data in file_to_terms[file]]    
            dct = Dictionary(temp)  # initialize a Dictionary
            for k, v in dct.token2id.items():
                ids.write(str(v) + '\t')
                ids.write(k)
                ids.write('\n')
                
            ids.close()
            '''                                
            return file_to_terms

#input = [word1, word2, ...]
#output = {word1: [pos1, pos2], word2: [pos2, pos434], ...}
def index_one_file(termlist):
    fileIndex = {}
    for index, word in enumerate(termlist):
        if word in fileIndex.keys():
            fileIndex[word].append(index)
        else:
            fileIndex[word] = [index]
    return fileIndex

#input = {filename: [word1, word2, ...], ...}
#res = {filename: {word: [pos1, pos2, ...]}, ...}
def make_indices(termlists):
    total = {}
    for filename in termlists.keys():
        total[filename] = index_one_file(termlists[filename])
    return total

def fullIndex(regdex):
    total_index = {}
    for filename in regdex.keys():
        for word in regdex[filename].keys():
            if word in total_index.keys():
                if filename in total_index[word].keys():
                   total_index[word][filename].extend(regdex[filename][word][:])
                else:
                   total_index[word][filename] = regdex[filename][word]
            else:
               total_index[word] = {filename: regdex[filename][word]}
    return total_index

temp = []
#r = root, d = directory, f = files
for r, d, f in os.walk(path):
    for file in f:
        file_name = os.path.join(r, file)
        name = os.path.basename(file_name)
        print(name)
        temp.append(name)
        file_to_term = process_files(file_name)
        index += 1
        #print(index)
        
        print("File to Term func output:\n")
        print(file_to_term)
        total = make_indices(file_to_term)
        
        print("Make indices Output: \n")
        print(total)
        
        print("Final index: \n")
        finalIndex = fullIndex(total)
        print(finalIndex)

'''
temp1 = [t.split() for t in temp]
docs = open('docids.txt', 'w')
name_to_int = Dictionary(temp1) 
for k, v in name_to_int.token2id.items():
        docs.write(str(v)+'\t')
        docs.write(k)
        docs.write('\n')
       
docs.close()
'''        