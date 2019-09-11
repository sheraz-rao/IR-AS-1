import numpy as np
import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk import PorterStemmer
import re
import codecs
import sys

#path = r'F:\IR\IR-AS-1\corpus1\corpus\corpus'

mapping = {} #this will have {fname: [word,...],...}
posting = {}
docs = []

def remove_headers(file_name):
    with codecs.open(file_name, encoding="utf-8", errors = 'ignore') as f: 
        data = f.read().splitlines()
    
    head = True
    i = 0
    for line in data:
        if ('<html' in line.lower() or\
            '<!doctype html' in line.lower()) \
            and 'content-type:' not in line.lower():
            
            head = False
            file_data = ' '.join(data)
            return file_data
        
        if head == True:
            data[i] = ''
        
        i += 1
        
    file_data = ' '.join(data)
    return file_data

def process_files(path):
    file_names = os.listdir(path)
    doc_id = 1
    term_id = 1
    terms = []
    
    doc_term_positions = []
    term_map = {} #map tokens/words to integer
    
    for file in file_names:
        print(file + ' ' + str(doc_id))
        stopwords = open('stoplist.txt', 'r')
        #ids = open('termids.txt', 'w', encoding="utf-8")
        sp = stopwords.readlines()
        pattern = re.compile('[\W_]+')
            
        #remove header
        data = remove_headers(path + '\\' + file)
        soup = BeautifulSoup(data, "lxml")

        #kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract() 
    
        #get text
        text = soup.get_text()     
        text1 = text.lower();
        text2 = pattern.sub(' ',text1)
        re.sub(r'[\W_]+','', text2)
        
        tokens = word_tokenize(text2)
                    
        print("stop wording...\n")           
        stop = [w for w in tokens if w not in sp]
        stopwords.close()
        
        print("stemming...\n")                
        stemm = [PorterStemmer().stem(s) for s in stop]
        
        mapping[file] = stemm
          
        pos = 1
        for token in stemm:
            if  token not in term_map:
                term_map[token] = term_id
                terms.append(str(term_id) + '\t' + token) #it will be write to the file
                term_id += 1
            doc_term_positions.append((doc_id, term_map[token], pos))
            pos += 1
         
        #get file name from path and this info  will be written to the .txt file
        docs.append((str(doc_id) + '\t' + file))
        doc_id += 1

    for p in doc_term_positions:
        if posting.__contains__((p[0], p[1])) == False:
            posting[(p[0], p[1])] = [p[2]]
        else:
            posting[(p[0], p[1])].append(p[2])
                   
    #term_file.write(terms)
    #np.savetxt('temp_termids.txt', terms, encoding="utf-8", fmt='%s')
    #np.savetxt('temp_docids.txt', docs, encoding="utf-8", fmt='%s')
    
    print("File pre processed.... returning:\n")
    #term_file.close()                               
    return mapping, term_map

#input = [word1, word2, ...]
#output = {word1: [pos1, pos2], word2: [pos2, pos3], ...}
def make_word_pos_dict(parameter):
    word_positions = {}
    for index, word in enumerate(parameter):
        if word in word_positions.keys():
            word_positions[word].append(index)
           
        else:
            word_positions[word] = [index]
           
    return word_positions

#input = {fname: [word1, word2, ...], ...}
#res = {fname: {word: [pos1, pos2, ...]}, ...}
def make_hashmap_of_hashmap(parameter):
    file_word_pos_dict = {}
    for fname in parameter.keys():
        file_word_pos_dict[fname] = make_word_pos_dict(parameter[fname])
    return file_word_pos_dict

#input = {fname: {word: [pos1, pos2, ...], ... }}
#res = {word: {fname: [pos1, pos2]}, ...}, ...}
def final_indexing(parameter):
    final_index = {}
    
    for fname in parameter.keys():
        
        #iterate through every word in the parameter hash
        for word in parameter[fname].keys():
            #check if that word is present as a key in the final_index. 
            #If it isn’t, then we add it, setting as its value another hashtable
            #that maps the document, in this case by the variable fname, to the list of positions of that word.
            if word in final_index.keys():
                
                #If it is a key, then check: if the current document is in each 
                #word’s hashtable; the one that maps filenames to word positions(fname).
                #If yes, we extend the current positions list with this list of positions
                if fname in final_index[word].keys():
                   final_index[word][fname].extend(parameter[fname][word][:])
                
                #set the positions equal to the positions list for this filename.
                else:
                   final_index[word][fname] = parameter[fname][word]
            else:
                final_index[word] = {fname: parameter[fname][word]}
    return final_index

import linecache

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("How to use? Write according to this:\n python file_name.py directory_name/path")
        
    else:
        print(sys.argv[1])
        res, term_map = process_files(sys.argv[1])
        hashmap = make_hashmap_of_hashmap(res)
        index = final_indexing(hashmap)
    
        #print(term_map)
        query = input("\nEnter Word to Search: ")
        #print(query)
        
        query1 = PorterStemmer().stem(query)
        res = (term_map.get(query1, "Not Found!"))
        #print(res)
        
        file = "term_info.txt"
        
        f =  linecache.getline(file, res)
        print("TermID, offset, pos, docs_count")
        print((f))