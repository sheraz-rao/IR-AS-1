from collections import OrderedDict
import pickle

def get_positions(data):
    t = {}
    for d in data:
        c = d.split('\t')
        t[c[0], c[1]] = c[2:]
    
    return t

def indexer():
    #pos_of_each_term_in_each_file.txt
    f = open('pos_of_each_term_in_each_file.txt') #this file has forward index table
    data = f.readlines()

    #collect positions of words saved in the file
    t = get_positions(data)
    term_index = {}
    
    for key in t:
        if term_index.__contains__(key[1]) == False:
            term_index[key[1]]=[{key[0]:t[(key[0],key[1])]}]    
        else:
            term_index[key[1]].append({key[0]:t[(key[0],key[1])]})
    
    #print("\nterm index: \n", term_index ,"\n")
    sorted_keys = sorted(map(int, list(term_index.keys())))
    
    final_index = OrderedDict()
    address = []    
    index = 0
    
    for key in sorted_keys:
        sub_arr = term_index[str(key)]
        
        whole_dict = {}
        elements=[]
        inner_arr=[]      
        
        for e in sub_arr:
            e1 = list(e)[0]
            whole_dict[e1] = e[e1]
        
        for item in sub_arr:
            temp = list(item)[0]
            elements.append(temp)    
            
        sub_keys = sorted(map(int, elements))
        #print("sub_keys: \n", sub_keys) #tells a list of docs in which the word appear
        
        total_doc_count = len(sub_keys) #tells us total docs in which word appear
        
        count = 0
        z = 0
        for sub_key in sub_keys:
            sub_values = whole_dict[str(sub_key)]
            
            i = sorted(map(int, sub_values))
            count = count + len(i)  #total positions in a file
    
            internal_dict = {}
            internal_dict[sub_key] = sorted(map(int, sub_values))
           
            if final_index.__contains__(key) == False:
                final_index[key] = [internal_dict]
            else:
                final_index[key].append(internal_dict)
            
            z+=1 
    
    #final index has been made.... 
    #below code is for term_index file format...
    #wordID, totalCount, total docs, docId:position_of_word....
    
    with open('term_index.txt', 'w', encoding="utf-8") as out:
        for key, value in final_index.items():
            out.write(str(key) +' ')
            address.append(len(str(key) + '\t'))
            
            sub_list = final_index[key]
            
            #loop for storing corpus_count(total occurences) and doc_count(total docs in which word appear),         
            corpus_count = 0
            for doc_dict in sub_list:
                temp = list(doc_dict)[0]
                corpus_count += len(doc_dict[temp])
            
            out.write(str(corpus_count) + ' ')
            document_occurences = len(sub_list)
            out.write(str(document_occurences) + ' ')
            
            
            #loop for delta encoding....
            current_doc_id = 0
            for doc_dict in value:
                last_doc_id = current_doc_id
                temp =  list(doc_dict)[0]           
                current_doc_id = temp  
                
                last_position = 0
                first_time = True            
                for current_position in doc_dict[current_doc_id]:
                    if first_time == False:
                        doc_id = 0    
                    
                    else:
                        doc_id = abs(current_doc_id - last_doc_id)
                        first_time = False

                    #for offset calc add up values and take length
                    docid_pos = str(doc_id)
                    docid_pos +=','
                    docid_pos += str(abs(current_position - last_position))
                    docid_pos += str('\t')
                    
                    out.write(docid_pos)
                    address[index] += len(docid_pos)
                    last_position = current_position 
                
            out.write('\n')
            address[index] += len('\n')
            address[index] += 1
            index += 1
    
    out.close()
    
    print(address)
        
    offset = 1
    first_line = True
    index = 0
    with open('term_info.txt', 'w', encoding="utf-8") as output_file:
        for key in final_index.keys():
            output_file.write(str(key) + '\t')        
            sub_list = final_index[key]
            
            if first_line == True:
                #offset for first is set to zero.....
                output_file.write('0' + '\t')
                first_line = False   
            
            else: #will be skipped for first time...
                if index == 0:
                    output_file.write(str(address[index]) + '\t')
                
                else:
                    #address will be calc by adding value at address[index] + previous value
                    address[index] += address[index-1]
                    output_file.write(str(address[index]) + '\t')
                
                index += 1           
            
            corpus_count = 0        
            for doc_dict in sub_list:
                temp = list(doc_dict)[0]
                corpus_count += len(doc_dict[temp])
            
            output_file.write(str(corpus_count) + '\t')
            document_occurences = len(sub_list)
            output_file.write(str(document_occurences) + '\n')
        
    output_file.close()
             
indexer()