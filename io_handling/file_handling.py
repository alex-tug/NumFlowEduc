'''
Created on 22.12.2012

@author: Alex
'''

import os
import errno



# http://stackoverflow.com/questions/273192/python-best-way-to-create-directory-if-it-doesnt-exist-for-file-write
def makeSurePathExists(path):
    try:
        os.makedirs(path)
        print "created ", path
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise