'''
input output handling/ file handling 
    define makeSurePathExists(path)
'''

import os, sys
import errno
import csv

# from: http://stackoverflow.com/questions/273192/python-best-way-to-create-directory-if-it-doesnt-exist-for-file-write
def makeSurePathExists(path):
    try:
        os.makedirs(path)
        print "created ", path
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        
def createPNG(path, filename, fig):
    try:
        makeSurePathExists(path)        
        fig.savefig(os.path.join(path, filename +'.png'))
    except:
        print "Error in createPNG:", sys.exc_info()[0]
        raise
        
     
def createCSV(path, filename, method, x, y):     

    try:
        makeSurePathExists(path)
        
        with open(os.path.join(path, filename+'.csv'), 'wb') as f:
            cw = csv.writer(f, delimiter=' ',\
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            cw.writerow(['x'] + ['y_'+method])
            # reshape self.x from x.shape=(size,1) to (size,)
            cw.writerows(zip(x.reshape(x.size), y))
    except:
        print "Error in createCSV:", sys.exc_info()[0]
        raise