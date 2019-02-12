import numpy as np
import math
def unique_occurances(array):
    """
    Returns a dictionary of distinct values as
    keys and number of their occurances as values
    __total_num_of_elements__ is off limits!!!!
    Expects array like: [yes,yes,no,no,no,...]
    """
    elements = {"__total_num_of_elements__":0}
    for a in array:
        if a not in elements:
            elements[a] = 1
        else:
            elements[a] += 1
        elements["__total_num_of_elements__"] += 1    
    return elements

def unique_attr_occurances(array, class_array):
    """
    Finds unique occurances of elements of array
    and links them with the class array.
    Expects input like:
    array => [one, two, three, two, one, one,...]
    class_array => [yes, no, yes, yes, no, yes,...]
    Returns a dictionary looking something like this:
    {   
        __total_num_of_elements:x, 
        one:{__total_num_of_elements:11, yes:4, no:7},
        two:{...},...
    }
    """
    elements = {"__total_num_of_elements__":0}
    class_unique = unique_occurances(class_array)
    del class_unique["__total_num_of_elements__"]
    for attr_element, class_element in zip(array, class_array):
        if attr_element not in elements:
            elements[attr_element] = {}
            elements[attr_element]["__total_num_of_elements__"] = 0
            for cu in class_unique:
                elements[attr_element][cu] = 0
        elements[attr_element][class_element] += 1
        elements[attr_element]["__total_num_of_elements__"] += 1
        elements["__total_num_of_elements__"] += 1
    return elements

def entropy(class_ellements):
    """ 
    Entropija skupa S se racuna po formuli 
    H(S) = sum(i=1..k) (-p(Ci)*log(base k)(p(Ci)))
    gde je p(Ci) procenat elemenata skupa S koji 
    pripadaju klasi.
    Kao parametar se ocekuje cela kolona iz matrice
    Vrednost entropije je 0 kada svi elementi skupa
    pripadaju jednoj istoj klasi (Skup je perfektno klasifikovan)
    Vrednost entropije je 1 kada svakoj klasi pripada
    podjednak broj elemenata (Skup je potpuno stohasticki)
    """
    # First get unique elements and number
    # of their occurances
    elements = unique_occurances(class_ellements)
    total_num = elements["__total_num_of_elements__"]
    total_sum = 0
    # - 1 because __total_num_of_elements__
    elements_length = len(elements)-1
    if elements_length == 1:
        return 0
    else:
        for value in list(elements.values())[1:]:
            p_Ci = float(value/total_num)
            # -1 because of __total_num_of_elements__
            total_sum += -p_Ci*math.log(p_Ci, elements_length)
        return total_sum

def attr_entropy(attr_dict):
    """
    Expects input like:
    {__total_num_of_elements__:6, yes:4, no:2}
    Returns the entropy of that attributes case
    """
    total_sum = 0
    total_num = 0
    log_k = len(attr_dict)-1
    if log_k == 1:
        return 0
    for key, val in list(attr_dict.items()):
        if key == "__total_num_of_elements__":
            total_num = val
        elif val is not None:
            p_Ci = val/total_num
            if p_Ci == 0:
                return 0
            else:
                total_sum += -p_Ci*math.log(p_Ci,log_k)
    return total_sum

def attribute_gain(entropy, data):
    """
    Expects input like:
    entropy => number between 0 and 1
    data => 
        {'__total_num_of_elements__': 14, 
        'suncano': 
            {
                '__total_num_of_elements__': 5,
                'nepogodno': 1, 'pogodno': 4
            },
        'oblacno': 
            {
                '__total_num_of_elements__': 4,
                'nepogodno': 1,
                'pogodno': 3
            },
        'kisa': 
            {
                '__total_num_of_elements__': 5,
                'nepogodno': 5,
                'pogodno': 0
            }
        }
    Calculates attribute gain by formula:
    G(S, A) = H(S) -Σi=1..m( |SAi|/|S| * H(SAi) )
    """
    G = entropy
    total_num = data["__total_num_of_elements__"]
    for key, val in list(data.items())[1:]:
        G += -val["__total_num_of_elements__"]/total_num*attr_entropy(val)
    return G

def max_gain(data):
    """
    Returns the collumn that has the highest
    gain value
    """
    H = entropy(data[:,len(data[0])-1])
    max_collumn = -1
    max_gain = -9999999
    for column in range(len(data.T)-1):
        gain = attribute_gain(H, unique_attr_occurances(data[:,column],data[:,len(data[0])-1]))
        if max_gain < gain:
            max_collumn = column
            max_gain = gain
    return max_collumn
    
data = np.array([
        #izgled vremena, temperatura, vlaznost, vetar, klasa
        ["suncano","toplo","visoka","slab","nepogodno"],
        ["suncano","toplo","visoka","jak","pogodno"],
        ["oblacno","toplo","visoka","slab","pogodno"],
        ["kisa","prijatno","visoka","slab","nepogodno"],
        ["kisa","hladno","normalna","slab","nepogodno"],
        ["kisa","hladno","normalna","jak","nepogodno"],
        ["oblacno","hladno","normalna","jak","nepogodno"],
        ["suncano","prijatno","visoka","slab","pogodno"],
        ["suncano","hladno","normalna","slab","pogodno"],
        ["kisa","prijatno","normalna","slab","nepogodno"],
        ["suncano","prijatno","normalna","jak","pogodno"],
        ["oblacno","prijatno","visoka","jak","pogodno"],
        ["oblacno","toplo","normalna","slab","pogodno"],
        ["kisa","prijatno","visoka","jak","nepogodno"],
    ])
# H = entropy(data[:,len(data[0])-1])
# func_Return = unique_attr_occurances(data[:,3],data[:,len(data[0])-1])
# print(attribute_gain(H, func_Return))
# print(func_Return)
print("class entropy: {}".format(entropy(data[:,len(data[0])-1])))
for column in range(len(data.T)-1):
    print("gain for collumn {}: {}".format(column,attribute_gain(entropy(data[:,len(data[0])-1]), unique_attr_occurances(data[:,column],data[:,len(data[0])-1]))))
print("collumn with best gain: {}".format(max_gain(data)))