# IR-AS-1

There are few temporary text files in repository; you can ignore those files
I made these files to test my code on very small data set(courpus1), contains just 4 files from corpus.

There are 3 code files

1) tokenizer.py
  it initial step for data pre processing
  
  How to run it? Enter in terminal in this format: 
  python inverted_index.py <directory/path>
  
2) inverted_index.py
   it is file containing code for inverted index using dictionary and it also checks the user input(word to search).
   just enter the word after program has made indexes. program will fetch the word listings for you.
   
   How to run it? Enter in terminal in this format: 
   python inverted_index.py <directory/path>
   After files have been processed you will be asked to enter the word to search. Enter the word and program will show you related data to    that word i.e. termID, total docs it appeared in and total positions it occured in.
   
3) inverted_index_with_sorting.py
    this file uses a txt file containing forward index...I used it to make the required "term_index.txt" format.
    inverted index is stored in a dictionary named final_index.
    Also this file makes inverted index file and term_offset.txt
    
    How to run it? Just hit ctrl + f5 :)
    

Second file uses term_offset.txt for listing of the word you want to search.    
So order of the files to run should be 1 -> 3 -> 2
