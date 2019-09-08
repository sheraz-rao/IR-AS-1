import numpy as np
import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk import PorterStemmer
import re
import codecs
from gensim.corpora import Dictionary
import sys

#path = r'C:\\Users\\pakistan\\Desktop\\IR\\Assignment-1\\IR-AS-1\\corpus1\\corpus\\corpus'
#subpath = r'C:\\Users\\pakistan\\Desktop\\IR\\Assignment-1'
#term_file = open('termids.txt', 'w')
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
def process_files(path):
    file_names = os.listdir(path)
    doc_id = 1
    term_id = 1
    terms = []
    docs = []
    doc_term_positions = []
    term_map = {}
    
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
            script.extract()    # rip it out
    
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
          
        pos = 1
        for token in stemm:
            if  token not in term_map:
                term_map[token] = term_id
                terms.append(str(term_id) + '\t' + token) #it will be write to the file
                term_id += 1
            doc_term_positions.append((doc_id, term_map[token], pos))
            pos += 1
        print("i am here....1\n") 
        #get file name from path and this info  will be written to the .txt file
        #name = os.path.basename(filenames)
        docs.append((str(doc_id) + '\t' + file))
        doc_id += 1
    
    print("i am here....2\n")
    posting = {}
    for p in doc_term_positions:
        if posting.__contains__((p[0], p[1])) == False:
            posting[(p[0], p[1])] = [p[2]]
        else:
            posting[(p[0], p[1])].append(p[2])
                   
    #term_file.write(terms)
    #np.savetxt('temp_termids.txt', terms, encoding="utf-8", fmt='%s')
    #np.savetxt('docids.txt', docs, encoding="utf-8", fmt='%s')
    
    '''
    #Forward index containing position of each term in each file
    with open('temp_pos.txt', mode='w', encoding="utf-8", errors='ignore') as pos_in_file:
        for key in posting:
            pos_in_file.write(str(key[0]) + '\t' + str(key[1]))
            for value in posting[key]:
                pos_in_file.write('\t' + str(value))
            pos_in_file.write('\n')
    pos_in_file.close()
    '''
    print("File pre processed.... returning:\n")
    #term_file.close()                               
    return

def get_positions(data):
    t = {}
    for d in data:
        c = d.split('\t')
        t[c[0], c[1]] = c[2:]
    
    return t

def indexer():
    f = open('pos_of_each_term_in_each_file.txt')
    data = f.readlines()

    #collect positions of words saved in the file
    t = get_positions(data)

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

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("usage: python tokenize <directory_name>")
        
    else:
        print(sys.argv[1])
        process_files(sys.argv[1])