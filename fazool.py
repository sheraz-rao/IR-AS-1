from collections import OrderedDict
import pickle

def get_positions(data):
    t = {}
    for d in data:
        c = d.split('\t')
        t[c[0], c[1]] = c[2:]
    
    return t

def indexer():
    f = open('temp_pos.txt')
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
    
    out = open('term_index.txt', 'w', encoding="utf-8")
    
    for key in sorted_keys:
        sub_arr = term_index[str(key)]
        
        t_id = sorted_keys[index] #tells us termID of word
        index += 1
        out.write(str(t_id) + ' ')
        ind = 0
        
        whole_dict = {}
        elements=[]
        inner_arr=[]      
        
        for e in sub_arr:
            e1 = list(e)[0]
            #print(e1)
            whole_dict[e1] = e[e1]
        
        for item in sub_arr:
            temp = list(item)[0]
            elements.append(temp)    
            
        #print("whole dict: \n", whole_dict)
        print("\n")    
        
        #print("elements: \n", elements)  
        #print("\n")
        
        sub_keys = sorted(map(int, elements))
        #print("sub_keys: \n", sub_keys) #tells a list of docs in which the word appear
        
        total_doc_count = len(sub_keys) #tells us total docs in which word appear
        doc_id = elements[ind] #gives doc_id
        ind += 1
        
        temp = {}
        temp[doc_id] = sub_keys

        count = 0
        z = 0
        for sub_key in sub_keys:
            sub_values = whole_dict[str(sub_key)]
            #print("sub_values: \n")
            #print(sub_values)
            
            #print("sub_values_int: \n")
            
            i = sorted(map(int, sub_values))
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
            
        out.write(str(count) + ' ' + str(total_doc_count) + ' ')
        #counter = 0
        #for counter in range(0, total_doc_count):
        #l = {}
        #l = ((final_index[key]))
        #print(l)
        
            #out.write(' ' + str(l) + ' ')
        out.write(str(temp))
        out.write('\n')
        #print("final index: \n", final_index, "\n")    
    
    out.close()
    
       
    lines_length = []
    '''
    length_index = 0
    with open('term_index.txt', 'w', encoding="utf-8") as output_file:
        for key, value in final_index.items():
            
            output_file.write(str(key)+'\t')
            lines_length.append(len(str(key)+'\t'))
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
                        doc_id = current_doc_id - last_doc_id
                        first_time = False
                
                    line = str(doc_id)
                    line +=':'
                    line += str(abs(current_position - last_position))
                    line += str('\t')
                    
                    output_file.write(line)
                    lines_length[length_index] += len(line)
                    last_position = current_position 
                
            output_file.write('\n')
            lines_length[length_index] += len('\n')
            lines_length[length_index] += 1
            length_index += 1
    output_file.close()    
    '''
    offset = 1
    first_line = True
    length_index=0
    with open('term_info.txt', 'w', encoding="utf-8") as output_file:
        for key in final_index.keys():
            output_file.write(str(key)+'\t')        
            sub_list = final_index[key]
            
            if first_line == False:
                if length_index == 0:
                    output_file.write(str(lines_length[length_index])+'\t')
                else:
                    lines_length[length_index]+=lines_length[length_index-1]
                    output_file.write(str(lines_length[length_index])+'\t')
                length_index+=1
            
            else:
                output_file.write('0'+'\t')
                first_line = False            
            
            corpus_count = 0        
            for doc_dict in sub_list:
                temp = list(doc_dict)[0]
                corpus_count += len(doc_dict[temp])
            
            output_file.write(str(corpus_count)+'\t')
            document_occurences = len(sub_list)
            output_file.write(str(document_occurences)+'\n')
        
    output_file.close()

        
indexer()