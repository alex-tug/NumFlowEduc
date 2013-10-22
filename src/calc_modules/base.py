''' 
calculation/ base module
    prepare stuff for the calculations
    
## TO BE REMOVED! ##
'''

import numpy as np

def replaceBadValues(vec):   
    BIG_NUMBER = 1e20
    BIG_NUMBER_NEG = -1 * 1e20
    
    sel_nan = [np.isnan(vec)]
    vec[sel_nan] = 0
    
    #sel_inf = [vec==np.inf]
    sel_inf = [vec>BIG_NUMBER]
    vec[sel_inf] = BIG_NUMBER
    
    #sel_neg_inf = [vec==-np.inf]
    sel_neg_inf = [vec<BIG_NUMBER_NEG]
    vec[sel_neg_inf] = BIG_NUMBER_NEG
        
    return vec
    
 
        
        
        
    
    
    
    