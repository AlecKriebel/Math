"""One exact finite cancellation example, not certification of a general theorem."""
from fractions import Fraction as F
import json

def require(ok, message):
    if not ok:
        raise ValueError(message)

def mat(rows):
    return [[F(x) for x in row] for row in rows]

def mul(a,b):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]

def sub(a,b):
    return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def ident(n):
    return mat([[int(i==j) for j in range(n)] for i in range(n)])

def run():
    d=mat([[1,2,0],[3,7,1],[0,1,2]])
    reduced=mat([[1,1],[1,2]])
    i1=mat([[-2,0],[1,0],[0,1]])
    i0=mat([[0,0],[1,0],[0,1]])
    p1=mat([[0,1,0],[0,0,1]])
    p0=mat([[-3,1,0],[0,0,1]])
    h=mat([[1,0,0],[0,0,0],[0,0,0]])
    require(mul(d,i1)==mul(i0,reduced),'inclusion chain identity')
    require(mul(p0,d)==mul(reduced,p1),'projection chain identity')
    require(mul(p1,i1)==ident(2) and mul(p0,i0)==ident(2),'retraction identity')
    require(mul(i1,p1)==sub(ident(3),mul(h,d)),'degree one homotopy identity')
    require(mul(i0,p0)==sub(ident(3),mul(d,h)),'degree zero homotopy identity')
    return {'example':'one matched pivot in a finite two-term rational complex',
            'input_matrix':[[str(x) for x in row] for row in d],
            'reduced_matrix':[[str(x) for x in row] for row in reduced],
            'checks':['inclusion chain identity','projection chain identity','retraction identity','degree one homotopy identity','degree zero homotopy identity'],
            'general_proof_computationally_certified':False}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
