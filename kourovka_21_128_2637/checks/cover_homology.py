"""Exact rational H_1 of two explicitly specified finite covers.
Uses presentation-complex cellular boundaries; no asphericity claim needed for H_1.
"""
from itertools import combinations
from math import gcd
from pathlib import Path
import json
from sympy import Matrix, SparseMatrix
from sympy.polys.matrices import DomainMatrix

def relators(labels, central_power):
    out=[]
    for i,j in combinations(range(4),2):
        m=labels.get((i,j),2)
        left=[(i if k%2==0 else j)+1 for k in range(m)]
        right=[(j if k%2==0 else i)+1 for k in range(m)]
        out.append(left+[-a for a in right[::-1]])
    out.append([1,2,3,4]*central_power)
    return out

def boundaries(n, weights, rels):
    entries={}
    for r,word in enumerate(rels):
        assert sum((1 if x>0 else -1)*weights[abs(x)-1] for x in word)%n==0
        for start in range(n):
            pos=start
            for x in word:
                g=abs(x)-1
                if x>0:
                    row=4*pos+g;value=1;pos=(pos+weights[g])%n
                else:
                    pos=(pos-weights[g])%n;row=4*pos+g;value=-1
                key=(row,r*n+start);entries[key]=entries.get(key,0)+value
            assert pos==start
    d2=SparseMatrix(4*n,len(rels)*n,{k:v for k,v in entries.items() if v})
    d1=SparseMatrix(n,4*n,{})
    for pos in range(n):
        for g,w in enumerate(weights):
            d1[(pos+w)%n,4*pos+g]+=1
            d1[pos,4*pos+g]-=1
    assert d1*d2==SparseMatrix(n,len(rels)*n,{})
    return d1,d2

def run():
    results={}
    for name,n,weights,labels,k in [('F4',12,[1,1,0,0],{(0,1):3,(1,2):4,(2,3):3},6),('H4',60,[1,1,1,1],{(0,1):5,(1,2):3,(2,3):3},15)]:
        d1,d2=boundaries(n,weights,relators(labels,k))
        r1=len(DomainMatrix.from_Matrix(d1).convert_to(__import__('sympy').QQ).rref()[1])
        r2=len(DomainMatrix.from_Matrix(d2).convert_to(__import__('sympy').QQ).rref()[1])
        results[name]={'index':n,'weights':weights,'c0':n,'c1':4*n,'c2':len(relators(labels,k))*n,'rank_d1_Q':r1,'rank_d2_Q':r2,'b1_Q':4*n-r1-r2,'d1_d2_zero':True}
        print(name,results[name],flush=True)
    return results
if __name__=='__main__':
    data=run();(Path(__file__).with_name('cover_homology_results.json')).write_text(json.dumps(data,indent=2)+'\n')
