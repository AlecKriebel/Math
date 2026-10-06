"""Intentional independent private scalar-type mutation: fail, not a production test."""
def equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
if not equal({'count':True},{'count':1}): raise ValueError('EXPECTED_PRIVATE_NEGATIVE: boolean attempt count is not integer1')
