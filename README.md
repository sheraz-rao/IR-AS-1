# IR-AS-1

there are few temporary text files in repository; you can ignore those files
i made these files to test my code on very small data set(courpus1), contains just 4 files from corpus.
there are 3 code files

1) tokenizer
  it initial step for data pre processing
  
2) inverted_index
   it is file containing code for inverted index using dictionary and it also checks the user input(word to search).
   just enter the word after reading files at the end of phase. program will fetch the word listings for you.
   
3) inverted_index with sorting
    this file uses a txt file containing forward index...I used it to make the required "term_index.txt" format.
    inverted index is stored in a dictionary named final_index.
    Also this file makes inverted index file and term_offset.txt
    
second file uses term_offset.txt for listing of the word you want to search.    

so order of the files to run should be 1 -> 3 -> 2
