from collections import OrderedDict
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
    term_index = {}
    
    for key in t:
        if term_index.__contains__(key[1]) == False:
            term_index[key[1]]=[{key[0]:t[(key[0],key[1])]}]    
        else:
            term_index[key[1]].append({key[0]:t[(key[0],key[1])]})
    
    sorted_keys = sorted(map(int, list(term_index.keys())))
    final_index = OrderedDict()
    i=0
    for key in sorted_keys:
        sub_arr = term_index[str(key)]
        whole_dict = {}
        
        for e in sub_arr:
            whole_dict[e.keys()[0]]=e[e.keys()[0]]
        
        elements=[]
        inner_arr=[]
        for item in sub_arr:
            elements.append(item.keys()[0])
        
        sub_keys = sorted(map(int, elements))
        
indexer()