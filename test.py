import numpy as np
import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk import PorterStemmer
import re
import codecs
from gensim.corpora import Dictionary
import sys

#path = r'F:\IR\IR-AS-1\corpus1\corpus\corpus'

mapping = {} #this will have {fname: [word,...],...}
posting = {}
docs = []

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
        
        mapping[file] = (stemm)
          
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
    return mapping, term_map

#input = [word1, word2, ...]
#output = {word1: [pos1, pos2], word2: [pos2, pos434], ...}
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
        for word in parameter[fname].keys():
            if word in final_index.keys():
                if fname in final_index[word].keys():
                   final_index[word][fname].extend(parameter[fname][word][:])
                
                else:
                   final_index[word][fname] = parameter[fname][word]
            else:
                final_index[word] = {fname: parameter[fname][word]}
    return final_index

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("How to use? Write according to this:\n python file_name.py directory_name/path")
        
    else:
        print(sys.argv[1])
        res, term_map = process_files(sys.argv[1])
        hashmap = make_hashmap_of_hashmap(res)
        index = final_indexing(hashmap)
        #print(index)
        #print((index.keys()))
        #print((index.values()))
        #print(term_map)
        #sorted_keys = sorted(map(int, list(str(index))[0]))
        #print(sorted_keys)
        #file = open('index.txt', 'w', encoding="utf-8")
        #np.savetxt('index.txt', list(index), encoding="utf-8", fmt='%s')
        #file.close()
        #ind = 0
        #f = open('temp_docids.txt', 'r')
        #fmap = list(index.values())
        #print(fmap, docs)
        '''
        for word in (index.keys()):
            e = list(term_map.values())[ind]
            file.write(str(e) + ' ' + str(fmap))
            file.write('\n')
            ind += 1
        file.close()
        '''
        docs = []  #total docs in which a word appear
        pos = []   #frequency of docs
        for word in index.keys():
            d = list(index[word].keys())
            docs.append(d)

            i = 0
            for item in index.values():
                last = list(index.values())[i]
                #print(last)
                last1 = list(last.keys())[-5:]
                pos.append(last1)
                i += 1
            
            print(pos)
            sub_keys = sorted(map(int, (pos)))
            
            count = 0
            z = 0
            temp = []
            
            whole_dict = {}
            for e in index:
                e1 = list(e)[0]
                whole_dict[e1] = e[e1]
            
            for sub_key in sub_keys:
                sub_values = whole_dict[str(sub_key)]
                
                i = sorted(map(int, sub_values))
                temp.append(i)
                count = count + len(i)  #total positions in a file
                #print(count)
        #print(docs)
            print(count)        