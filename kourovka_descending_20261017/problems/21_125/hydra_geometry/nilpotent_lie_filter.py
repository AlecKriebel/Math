#!/usr/bin/env python3
"""Exact finite-field truncated-associative calculation of canonical H subgroup Lie images.
Lazard application is recorded separately; this script is only exact linear algebra.
"""
from pathlib import Path
import json
P=101

def add(a,b,scale=1):
    d=dict(a)
    for w,c in b.items():
        d[w]=(d.get(w,0)+scale*c)%P
        if not d[w]:del d[w]
    return d

def scalar(a,c):return {w:c*v%P for w,v in a.items() if c*v%P}
def prod(a,b,k):
    d={}
    for u,c in a.items():
        for v,e in b.items():
            if len(u)+len(v)<=k:
                w=u+v;d[w]=(d.get(w,0)+c*e)%P
    return {w:c for w,c in d.items() if c}
def exp(a,k):
    out={'':1};power={'':1};den=1
    for i in range(1,k+1):
        power=prod(power,a,k);den=den*i%P
        out=add(out,scalar(power,pow(den,-1,P)))
    return out

def log(a,k):
    z=add(a,{'':1},-1);power={'':1};out={}
    for i in range(1,k+1):
        power=prod(power,z,k)
        out=add(out,scalar(power,((-1)**(i+1))*pow(i,-1,P)))
    return out

def inverse(a,k):
    z=add(a,{'':1},-1);power={'':1};out={'':1}
    for i in range(1,k+1):
        power=prod(power,z,k);out=add(out,power,(-1)**i)
    return out

def bracket(a,b,k):return add(prod(a,b,k),prod(b,a,k),-1)
class Span:
    def __init__(self):self.rows={}
    def reduce(self,a):
        a=dict(a)
        for p,r in sorted(self.rows.items(),key=lambda x:(len(x[0]),x[0])):
            if p in a:a=add(a,r,-a[p])
        return a
    def insert(self,a):
        a=self.reduce(a)
        if not a:return None
        pivot=min(a,key=lambda w:(len(w),w));a=scalar(a,pow(a[pivot],-1,P));self.rows[pivot]=a
        return a

def run(m):
    s=exp({'x':1},m);t=exp({'y':1},m)
    aa=[s]+[None]*m;aa[m]=t
    for i in range(m,1,-1):aa[i-1]=prod(prod(inverse(aa[i],m),s,m),aa[i],m)
    # Relation [s,alpha1]=1 is exact in the class-m truncation.
    assert prod(s,aa[1],m)==prod(aa[1],s,m)
    gens=[log(aa[1],m)]
    gens += [log(prod(prod(aa[i],s,m),inverse(aa[i],m),m),m) for i in range(2,m+1)]
    basis=Span();queue=[]
    for g in gens:
        b=basis.insert(g)
        if b:queue.append(b)
    for b in queue:
        for g in gens:
            c=basis.insert(bracket(g,b,m))
            if c:queue.append(c)
    outcomes=[]
    for i in range(m+1):
        remainder=basis.reduce(log(aa[i],m))
        outcomes.append({'label':'s' if i==0 else 'alpha_'+str(i),'in_L_lie_span':not remainder,'remainder':remainder})
    return {'rank':m,'prime':P,'class':m,'Lie_L_dimension':len(basis.rows),'generator_count':len(gens),'membership':outcomes,'basis':[{ 'pivot':w,'row':r} for w,r in sorted(basis.rows.items(),key=lambda x:(len(x[0]),x[0]))]}
if __name__=='__main__':
    rows=[]
    for m in range(2,10):
        r=run(m);rows.append(r);print(m,r['Lie_L_dimension'],[(x['label'],x['in_L_lie_span']) for x in r['membership']],flush=True)
    Path(__file__).with_name('nilpotent_lie_filter_results.json').write_text(json.dumps({'warning':'exact F101 arithmetic and class<=9; interpretation needs Lazard theory and is not a specialness criterion','rows':rows},indent=2)+'\n')
