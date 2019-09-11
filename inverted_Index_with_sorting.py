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
    term_index = {} #it will have {word: [{fname: [pos1, pos2, pos3...]},...],...}
    
    for key in t:
        if term_index.__contains__(key[1]) == False:
            term_index[key[1]]=[{key[0]:t[(key[0],key[1])]}]    
        else:
            term_index[key[1]].append({key[0]:t[(key[0],key[1])]})
    
    sorted_keys = sorted(map(int, list(term_index.keys())))
    
    final_index = OrderedDict()
    address = []    
    index = 0
    
    #sorted_keys has sorted list[1,2,3,4,.....]
    for key in sorted_keys:
        #it will have [fname: [pos1, pos2, pos3...],...]
        sub_arr = term_index[str(key)]
        
        helper_dict = {}
        doc_ids = []   
        
        for e in sub_arr:
            e1 = list(e)[0]
            helper_dict[e1] = e[e1]
            doc_ids.append(e1)    
            
        sorted_ids = sorted(map(int, doc_ids))
        #print("sorted_ids: \n", sorted_ids) #tells a list of docs in which the word appear
        
        total_doc_count = len(sorted_ids) #tells us total docs in which word appear
        
        count = 0
        z = 0
        for sub_key in sorted_ids:
            pos_of_words = helper_dict[str(sub_key)]
            
            i = sorted(map(int, pos_of_words))
            count = count + len(i)  #total positions in a file
    
            internal_dict = {}
            #store positions against each word
            internal_dict[sub_key] = sorted(map(int, pos_of_words))
           
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
            
            #contains [{fname: [positions of word]}]
            fname_Wpos = final_index[key]
            
            #loop for storing corpus_count(occurences) and doc_count(total docs in which word appear),         
            occurences = 0
            for doc_dict in fname_Wpos:
                k = list(doc_dict)[0]  #k contains key which is fname
                occurences += len(doc_dict[k])  #doc_dict[k] contains list of positions 
            
            out.write(str(occurences) + ' ')
            doc_occur = len(fname_Wpos) #count of docs a word occured in
            out.write(str(doc_occur) + ' ')
            
            #loop for delta encoding....
            curr_doc_id = 0
            for doc_dict1 in fname_Wpos:
                last_doc_id = curr_doc_id
                k1 = list(doc_dict1)[0]    #k1 contains fname       
                curr_doc_id = k1  
                
                last_pos = 0
                #first time use actual doc_id and store data accordingly
                #next time use '0' for same doc_id
                first_time = True            
                for curr_pos in doc_dict1[curr_doc_id]:
                    if first_time == True:
                        doc_id = abs(curr_doc_id - last_doc_id)
                        first_time = False    
                    
                    else:
                        doc_id = 0

                    #for offset calc add up values and take length
                    docid_pos = str(doc_id)
                    docid_pos +=','
                    docid_pos += str(abs(curr_pos - last_pos))
                    docid_pos += str('\t')
                    
                    out.write(docid_pos)
                    #address has offsets stored in it...
                    address[index] += len(docid_pos)
                    last_pos = curr_pos 
                
            out.write('\n')
            address[index] += len('\n')
            address[index] += 1
            index += 1
    
    out.close()
    
    first_line = True
    index = 0
    with open('term_info.txt', 'w', encoding="utf-8") as out:
        for key in final_index.keys():
            out.write(str(key) + '\t')        
            fname_Wpos = final_index[key]
            
            if first_line == True:
                #offset for first is set to zero.....
                out.write('0' + '\t')
                first_line = False   
            
            else: #will be skipped for first time...
                if index == 0:
                    out.write(str(address[index]) + '\t')
                
                else:
                    #address will be calc by adding value at address[index] + previous value
                    address[index] += address[index-1]
                    out.write(str(address[index]) + '\t')
                
                index += 1           
            
            occurences = 0        
            for doc_dict in fname_Wpos:
                k = list(doc_dict)[0]
                occurences += len(doc_dict[k])
            
            out.write(str(occurences) + '\t')
            doc_occur = len(fname_Wpos)
            out.write(str(doc_occur) + '\n')
        
    out.close()
         
indexer()