"""Search finite-group vertices whose continuous interpolation is not extreme.
Random objectives are deterministic. Every reported candidate is rechecked exactly.
Run: python checks/find_grid_counterexample.py
"""
from fractions import Fraction as F
import json, random
import numpy as np
from scipy.optimize import linprog
from sympy import Matrix

def row(q,i,j):
    a=[0]*q;a[i]+=1;a[j]+=1;a[(i+j)%q]-=1
    return a

def rank_at(values,factor=1,f_index=None):
    q=len(values);N=q*factor
    v=[]
    for k in range(N):
        i,t=divmod(k,factor)
        v.append(((factor-t)*values[i]+t*values[(i+1)%q])/factor)
    f_index = values.index(F(1)) if f_index is None else f_index
    A=[[int(i==0) for i in range(N)],[int(i==f_index*factor) for i in range(N)]]
    A += [row(N,i,j) for i in range(N) for j in range(i,N) if v[i]+v[j]==v[(i+j)%N]]
    return int(Matrix(A).rank()),N,A,v

def search():
    rng=random.Random(1827)
    for q in range(3,16):
        for f in range(1,q):
            a=[row(q,i,j) for i in range(q) for j in range(i,q)]
            eq=[[int(i==0) for i in range(q)],[int(i==f) for i in range(q)]]; b=[0,1]
            for i in range(q):
                r=[0]*q;r[i]+=1;r[(f-i)%q]+=1;eq.append(r);b.append(1)
            for z in range(25):
                c=[rng.uniform(-1,1) for _ in range(q)]
                res=linprog(c,A_ub=-np.array(a),b_ub=np.zeros(len(a)),A_eq=eq,b_eq=b,bounds=(0,1),method='highs')
                if not res.success:continue
                v=[F(float(x)).limit_denominator(10**6) for x in res.x]
                if v[0]!=0 or v[f]!=1 or any(v[i]+v[(f-i)%q]!=1 for i in range(q)):continue
                if any(sum(x*y for x,y in zip(r,v))<0 for r in a):continue
                r,N,A,_=rank_at(v)
                if r!=q:continue
                rr,NN,AA,vv=rank_at(v,3)
                if rr<NN:
                    null=Matrix(AA).nullspace()[0]
                    out={'q':q,'f_index':f,'values':list(map(str,v)),'coarse_rank':r,'refinement_factor':3,'refined_rank':rr,'refined_dimension':NN,'kernel':[str(x) for x in null]}
                    print(json.dumps(out,indent=2));return out
    raise RuntimeError('No counterexample found')
if __name__=='__main__':
    out=search()
    from pathlib import Path
    Path(__file__).with_name('grid_counterexample.json').write_text(json.dumps(out,indent=2)+'\n')
