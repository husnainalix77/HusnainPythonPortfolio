## FLAMES Game

def removeSameChar(name1, name2):
    'Removes same characters which are in both names'
    name1_list = list(name1)
    name2_list = list(name2)
    
    for ch in name1_list[:]: ## Shallow copy is needed while iterating with removing elements
        if ch in name2_list:
            name1_list.remove(ch)
            name2_list.remove(ch)
            
    return len(name1_list+name2_list)

if __name__ =='__main__':
    name1 = input('Enter player 1 name: ').replace(' ','').lower()
    name2 = input('Enter player 2 name: ').replace(' ','').lower()
    
    total_len = removeSameChar(name1, name2)
    flames = ['F', 'L', 'A', 'M', 'E', 'S']
    
    while len(flames) > 1:
        cut = (total_len%len(flames)) -1
        
        if cut>=0:
            flames = flames[cut+1:] + flames[:cut]
        else:
            flames = flames[:len(flames)-1]
            
    # Mapping result
    mapping = {
    'F': 'Friend',
    'L': 'Love',
    'A': 'Affection',
    'M': 'Marriage',
    'E': 'Enemy',
    'S': 'Siblings'
    }

    print("Relationship is:", mapping[flames[0]])        