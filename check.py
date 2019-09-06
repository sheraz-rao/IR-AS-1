import numpy as np
import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk import PorterStemmer
import re
import codecs
from gensim.corpora import Dictionary
import sys

path = r'C:\\Users\\pakistan\\Desktop\\IR\\Assignment-1\\corpus\\corpus\\corpus'
subpath = r'C:\\Users\\pakistan\\Desktop\\IR\\Assignment-1'
index = 0
doc_id = 1
term_id = 1
terms = []
docs = []
doc_term_positions = []
term_map = {}

def remove_headers(file_name):
    with codecs.open(file_name, encoding="utf-8", errors = 'ignore') as f: 
        data = f.read().splitlines()
    
    found_header = True
    i = 0
    for line in data:
        if ('<html' in line.lower() or\
        '<!doctype html' in line.lower()) \
        and 'content-type:' not in line.lower():
            found_header = False
            file_data = ' '.join(data)
            return file_data
        if found_header == True:
            data[i] = ''
        i += 1
        
    file_data = ' '.join(data)
    return file_data

#r = root, d = directory, f = files
def process_files(filenames):
    file_to_terms = {}
    for file in filenames:
        print(file + '\n')
        stopwords = open('stoplist.txt', 'r')
        ids = open('termids.txt', 'w', encoding="utf-8")
        sp = stopwords.readlines()
        pattern = re.compile('[\W_]+')
            
        #remove header
        data = remove_headers(filenames)
        
        soup = BeautifulSoup(data, "lxml")

        #kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
    
        #get text
        text = soup.get_text()
            
        file_to_terms[filenames] = text.lower();
        file_to_terms[filenames] = pattern.sub(' ',file_to_terms[filenames])
        re.sub(r'[\W_]+','', file_to_terms[filenames])
        
        file_to_terms[filenames] = word_tokenize(file_to_terms[filenames])
                    
        print("stemming...\n")           
        file_to_terms[filenames] = [w for w in file_to_terms[filenames] if w not in sp]
                        
        file_to_terms[filenames] = [PorterStemmer().stem(w) for w in file_to_terms[filenames]]
        
        print("File pre processed.... returning:\n")
         
        '''
        print("copying to file")
        temp = [data.split() for data in file_to_terms[filenames]]    
        dct = Dictionary(temp)  # initialize a Dictionary
        for k, v in dct.token2id.items():
            ids.write(str(v) + '\t')
            ids.write(k)
            ids.write('\n')
            
        ids.close()
        '''
        
        pos = 1
        for token in file_to_terms[filenames]:
            if term_map.has_key(token) == False:
                term_map[token] = term_id
                terms.append(str(term_id) + '\t' + token) #it will be write to the file
                term_id += 1
            doc_term_positions.append((doc_id, term_map[token], pos))
            pos += 1

        #get file name from path and this info  will be written to the .txt file
        name = os.path.basename(filenames)
        docs.append((str(doc_id) + '\t' + name))
        doc_id += 1
                                       
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

'''
from collections import defaultdict
def doc_count(my_list):
    revDict = {v : sum(1 for l in my_list.values() if v in l)  
        for v in set(x for y in my_list.values() for x in y) }
    return revDict
'''

#temp = []
#r = root, d = directory, f = files
for r, d, f in os.walk(path):
    for file in f:
        file_name = os.path.join(r, file)
        
        #print(name)
        #temp.append(name)
        file_to_term = process_files(file_name)
        index += 1
        print(index)
        
        #print("File to Term func output:\n")
        #print(file_to_term)
        
        #total = make_indices(file_to_term)
        
        #print("Make indices Output: \n")
        #print(counter, total)
        
        #print("Final index: \n")
        #finalIndex = fullIndex(total)
        #print(finalIndex)

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