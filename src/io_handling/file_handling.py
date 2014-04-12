"""
input output handling/ file handling
    define makeSurePathExists(path)
"""

import os, sys
import errno
import csv


# from: http://stackoverflow.com/questions/273192/python-best-way-to-create-directory-if-it-doesnt-exist-for-file-write
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
        print "created ", path
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def create_png(path, filename, fig):
    try:
        make_sure_path_exists(path)
        fig.savefig(os.path.join(path, filename + '.png'), dpi=300)
    except:
        print "Error in create_png:", sys.exc_info()[0]
        raise


def export_stability_check_results(path, signature, check_vec):
    for method, data in check_vec.iteritems():
        filename = signature + method
        print "\ncheck_vec ", method
        labels = ["CFL", "NE", "PE", "is_positive", "is_not_null", "is_stable", method]
        write_csv(path, filename, labels, data)


def create_csv(path, filename, pd):

    x = pd.x
    data = []
    data.append(x.reshape(x.size))
    
    labels = ['x']
    
    for m in pd.methods.itervalues():
        data.append(m.u_final)
        labels.append(['y_' + m.name])

    write_csv(path, filename, labels, data, transpose_flag=True)


def write_csv(path, filename, labels, data, transpose_flag=False):
    """
        write labels and data into a csv-file
    """

    try:
        make_sure_path_exists(path)

        with open(os.path.join(path, filename+'.csv'), 'wb') as f:
            cw = csv.writer(f,
                            delimiter=' ',
                            quotechar='|',
                            quoting=csv.QUOTE_MINIMAL)
            cw.writerow(labels)

            if transpose_flag:
                # zip(*data) ... transpose structure of list "data"
                cw.writerows(zip(*data))
            else:
                cw.writerows(data)
    except:
        print "Error in write_csv:", sys.exc_info()[0]
        raise

