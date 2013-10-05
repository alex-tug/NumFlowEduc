''' 
interpolations
    define various methods for interpolation
'''

def linearInterpol(xa, xb, fa, fb, x):
    fx = fa + (fb-fa) * (x-xa)/(xb-xa)
    return fx