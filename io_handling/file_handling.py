'''
input output handling/ file handling 
    define makeSurePathExists(path)
'''

import os
import errno

# from: http://stackoverflow.com/questions/273192/python-best-way-to-create-directory-if-it-doesnt-exist-for-file-write
def makeSurePathExists(path):
    try:
        os.makedirs(path)
        print "created ", path
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise