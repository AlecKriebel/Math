#!/usr/bin/env python3
"""Read-only stdlib verification of explicit finite Lie spaces and dual separation.
The abstract exp/log-to-finite-group justification is in NILPOTENT_QUOTIENT_PARTIAL.md.
This is not an independent mathematical review or an inter-osculation verifier.
"""
import json,hashlib,itertools,time
from pathlib import Path
p=Path(__file__).with_name('rank5_lie_certificate.json');raw=p.read_bytes();C=json.loads(raw);prime=C['prime'];cap=C['class_bound'];one={'':1}
def plus(a,b,k=1):
    out=dict(a)
    for w,v in b.items():
        out[w]=(out.get(w,0)+k*v)%prime
        if not out[w]:out.pop(w)
    return out
def times(a,b):
    out={}
    for x,u in a.items():
        for y,v in b.items():
            if len(x)+len(y)<=cap:out[x+y]=(out.get(x+y,0)+u*v)%prime
    return {w:v for w,v in out.items() if v}
def scaled(a,k):return {w:v*k%prime for w,v in a.items() if v*k%prime}
def exponential(a):
    out=dict(one);t=dict(one);f=1
    for i in range(1,cap+1):
        t=times(t,a);f=f*i%prime;out=plus(out,scaled(t,pow(f,-1,prime)))
    return out
def logarithm(a):
    u=plus(a,one,-1);t=dict(one);out={}
    for i in range(1,cap+1):t=times(t,u);out=plus(out,scaled(t,(-1)**(i+1)*pow(i,-1,prime)))
    return out
def inverse(a):
    u=plus(a,one,-1);t=dict(one);out=dict(one)
    for i in range(1,cap+1):t=times(t,u);out=plus(out,t,(-1)**i)
    return out
def bkt(a,b):return plus(times(a,b),times(b,a),-1)
def ordering(w):return (len(w),w)
class Space:
    def __init__(self,rows):
        self.echelon={}
        for r in rows:
            rem=self.reduce(r);assert rem,'dependent certificate basis'
            pivot=min(rem,key=ordering);self.echelon[pivot]=scaled(rem,pow(rem[pivot],-1,prime))
        self.rows=list(self.echelon.values())
    def reduce(self,r):
        out=dict(r)
        for pivot,row in sorted(self.echelon.items(),key=lambda z:ordering(z[0])):
            if pivot in out:out=plus(out,row,-out[pivot])
        return out
    def contains(self,r):return not self.reduce(r)
def minimum_degree(a):return min(map(len,a),default=cap+1)
def check_products(left,right,target,symmetric=False):
    count=0;nonzero=0
    for i,a in enumerate(left):
        for j,b in enumerate(right):
            if symmetric and j<=i:continue
            if minimum_degree(a)+minimum_degree(b)>cap:continue
            v=bkt(a,b);assert target.contains(v),(i,j,'bracket fails')
            count+=1;nonzero+=bool(v)
    return {'checked':count,'nonzero_brackets':nonzero}
start=time.time()
assert prime>cap and all(prime%d for d in range(2,int(prime**0.5)+1))
for key in ('R_basis','ideal_basis','W_basis'):
    for row in C[key]:
        assert row
        for word,value in row.items():assert word and len(word)<=cap and set(word)<=set('xy') and type(value)==int and 0<value<prime
R=Space(C['R_basis']);I=Space(C['ideal_basis']);W=Space(C['W_basis'])
assert len(R.rows)==C['ambient_lie_dimension']==226
assert len(I.rows)==C['relation_ideal_dimension']==31
assert len(W.rows)==C['W_dimension']==88
assert C['quotient_dimension']==len(R.rows)-len(I.rows)==195
assert R.contains({'x':1}) and R.contains({'y':1})
assert all(R.contains(v) for v in I.rows+W.rows)
assert all(W.contains(v) for v in I.rows)
checks={}
checks['R_Lie_closed']=check_products(R.rows,R.rows,R,True)
checks['I_is_ideal_in_R']=check_products(R.rows,I.rows,I)
checks['W_Lie_closed']=check_products(W.rows,W.rows,W,True)
s=exponential({'x':1});top=exponential({'y':1});aa=[s]+[None]*C['rank'];aa[-1]=top
for i in range(C['rank'],1,-1):aa[i-1]=times(times(inverse(aa[i]),s),aa[i])
logs=[logarithm(v) for v in aa]
assert logs[1:]==C['alpha_logs']
assert all(R.contains(v) for v in logs)
rel=logarithm(times(times(times(inverse(s),inverse(aa[1])),s),aa[1]))
assert rel==C['relator_log'] and I.contains(rel)
gs=[logs[1]]+[logarithm(times(times(a,s),inverse(a))) for a in aa[2:]]
assert gs==C['L_generator_logs'] and all(W.contains(g) for g in gs)
values=[]
for dual in C['dual_separation_certificates']:
    f=dual['functional'];j=dual['alpha_index']
    assert 2<=j<=C['rank']
    apply=lambda row:sum(v*f.get(w,0) for w,v in row.items())%prime
    assert all(apply(b)==0 for b in W.rows)
    value=apply(logs[j]);assert value==dual['nonzero_value'] and value
    assert not W.contains(logs[j]);values.append({'alpha_index':j,'value':value,'functional_support_size':len(f)})
assert sorted(d['alpha_index'] for d in values)==list(range(2,C['rank']+1))
out={'status':'PASS','certificate_sha256':hashlib.sha256(raw).hexdigest(),'elapsed_seconds':time.time()-start,'dimensions':{'R':226,'I':31,'R_over_I':195,'W':88},'finite_group_order':'101^195','checks':checks,'dual_values':values,'scope':'finite quotient cover has no hyperplane self-intersections only; all other specialness conditions unproved; independent review pending'}
Path(__file__).with_name('rank5_lie_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
