"""Exact arithmetic checks of the rational constants in the analytic proof.
These checks supplement, not replace, the analytic monotonicity proof.
"""
from fractions import Fraction as F
import json

def check(q=F(5,7), factor=F(14,5)):
    exp_lower=1+q+q*q/2+q*q*q/6
    if not exp_lower>2: raise ValueError('Exponential lower polynomial does not exceed 2')
    if not factor*q<=2: raise ValueError('Union-logarithm constant exceeds 2')
    if not factor==1+F(9,5): raise ValueError('Incorrect r(5) envelope')
    if not 5*5<2**5: raise ValueError('log2(5) < 5/2 fails')
    if not 2*5+3<2**5: raise ValueError('Threshold endpoint fails')
    return {'exp_lower':str(exp_lower),'ln2_upper':str(q),'envelope':str(factor),'product':str(factor*q),'passed':True}
if __name__=='__main__':print(json.dumps(check(),sort_keys=True))
