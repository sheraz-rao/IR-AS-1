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
    f = open('temp_pos.txt') #this file has forward index table
    data = f.readlines()

    #collect positions of words saved in the file
    t = get_positions(data)
    term_index = {}
    
    index = 0
    
    for key in t:
        if term_index.__contains__(key[1]) == False:
            term_index[key[1]]=[{key[0]:t[(key[0],key[1])]}]    
        else:
            term_index[key[1]].append({key[0]:t[(key[0],key[1])]})
    
    sorted_keys = sorted(map(int, list(term_index.keys())))
    #print("\nSorted keys: \n", sorted_keys ,"\n")
    
    final_index = OrderedDict()
    
    #doc_id = 1
    
    #out = open('temp_term_index.txt', 'w', encoding="utf-8")
    
    for key in sorted_keys:
        sub_arr = term_index[str(key)]
        
        t_id = sorted_keys[index] #tells us termID of word
        index += 1
        #out.write(str(t_id) + ' ')
        ind = 0
        
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
        doc_id = elements[ind] #gives doc_id
        
        count = 0
        z = 0
        temp = []
        for sub_key in sub_keys:
            sub_values = whole_dict[str(sub_key)]
            
            #print("sub_values_int: \n")
            
            i = sorted(map(int, sub_values))
            temp.append(i)
            #print(temp)
            count = count + len(i)  #total positions in a file
            #print(i, "\n")
            
            internal_dict = {}
            internal_dict[sub_key] = sorted(map(int, sub_values))
            #print("internal_dict: \n")
            #print(internal_dict)
            
            if final_index.__contains__(key) == False:
                final_index[key] = [internal_dict]
            else:
                final_index[key].append(internal_dict)
            
            z+=1
            
        #out.write(str(count) + ' ' + str(total_doc_count) + ' ')
        #for i in range(0, total_doc_count):
            #out.write(str(elements[i]) + ',' + str(temp[i]) + ' ')
        #out.write('\n')
        ind += 1
        #print("final index: \n", final_index, "\n")    
    
    #out.close()
       
        
indexer()