import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk import PorterStemmer
#from collections import defaultdict
import re

path = r'C:\Users\pakistan\Desktop\IR\Assignment-1\corpus\corpus\corpus'

def process_files(filenames):
    file_to_terms = {}
    for file in filenames:
        #stopwords = open('stoplist.txt', 'r')
        #sp = stopwords.readlines()
        pattern = re.compile('[\W_]+')
        with open(filenames) as temp:
            soup = BeautifulSoup(temp.read(), 'lxml')
               
        #kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract() # rip it out
        
        #get text
        text = soup.get_text()
        
        #break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        
        #break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        print(text)
            
        file_to_terms[file] = text.lower();
        file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
        re.sub(r'[\W_]+','', file_to_terms[file])
        file_to_terms[file] = file_to_terms[file].split()
        print("File processed.... returning:\n")
        #file_to_terms[file] = [w for w in file_to_terms[file] if w not in sp]
        #file_to_terms[file] = [PorterStemmer().stem(w) for w in file_to_terms[file]]
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

#r = root, d = directory, f = files
for r, d, f in os.walk(path):
    for file in f:
        file_name = os.path.join(r, file)
        name = os.path.basename(file_name)
        print(name)
        file_to_term = process_files(file_name)
        print("File to Term func output:\n")
        print(file_to_term)
        total = make_indices(file_to_term)
        print("Make indices Output: \n")
        print(total)