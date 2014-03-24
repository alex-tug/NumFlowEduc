''' 
calculation/ base module
    prepare stuff for the calculations
    
## TO BE REMOVED! ##
'''

import numpy as np

def replaceBadValues(vec):   
    BIG_NUMBER = 1e10
    BIG_NUMBER_NEG = -1 * 1e10
    
    sel_nan = [np.isnan(vec)]
    vec[sel_nan] = 0
    
    #sel_inf = [vec==np.inf]
    sel_inf = [vec>BIG_NUMBER]
    vec[sel_inf] = BIG_NUMBER
    
    #sel_neg_inf = [vec==-np.inf]
    sel_neg_inf = [vec<BIG_NUMBER_NEG]
    vec[sel_neg_inf] = BIG_NUMBER_NEG
        
    return vec
    
 
def cut_too_big_values(vec):   
    """ used to avoid troubles in matplotlib"""
    
    vec = replaceBadValues(vec)
    
    max_value = 1000
    min_value = -1000
    
    sel_inf = [vec>max_value]
    vec[sel_inf] = max_value
    
    sel_neg_inf = [vec<min_value]
    vec[sel_neg_inf] = min_value
    
    return vec
        
        
        
    
    
    
    