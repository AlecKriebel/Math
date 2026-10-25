#!/usr/bin/env python3
"""Fresh literal-graph reconstruction; no submitted checker imported or read."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
from itertools import product
from datetime import datetime,timezone
import json,hashlib,time
start=time.time();checks=[];details={}
def ck(ok,label):
    if not ok:raise AssertionError(label)
    checks.append(label)
def denominator(weights):
    d=1
    for x in weights:d=d*x.denominator//gcd(d,x.denominator)
    return d
def build(M,b,q,theta,a_multiplier=1):
    n=len(q);d=max(map(sum,M));t=theta/d;res=1-n*t
    ck(res>=0,'nonnegative residual')
    a=[t]*n+([res] if res else [])
    copies=lambda w:[i for i,x in enumerate(w) for _ in range(int(x*denominator(w)))]
    aa,bb,cc=map(copies,(a,b,q));aa=[i for i in aa for _ in range(a_multiplier)];AB=[];CB=[]
    for i in aa:AB.append(sum(1<<v for v,row in enumerate(bb) if i==n or not M[row][i]))
    for i in cc:CB.append(sum(1<<v for v,row in enumerate(bb) if M[row][i]))
    return aa,bb,cc,AB,CB,t
def stats(na,nb,nc,AB,CB):
    reach=[sum(bool(x&y) for x in AB) for y in CB]
    da=min(F(x.bit_count(),nb) for x in AB)
    db=min(F(sum(x>>v&1 for x in AB),na) for v in range(nb))
    dc=min(F(y.bit_count(),nb) for y in CB)
    dd=min(F(sum(y>>v&1 for y in CB),nc) for v in range(nb))
    return [da,db,dd,dc],reach
def template(M,b,q,theta,label,a_multiplier=1):
    ck(all(x>0 for x in b+q) and sum(b)==sum(q)==1,label+' strictly positive probabilities')
    ck(all(sum(q[i]*r[i] for i in range(len(q)))==theta for r in M),label+' row regularity')
    cols=[tuple(r[i] for r in M) for i in range(len(q))]
    ck(len(set(cols))==len(cols),label+' distinct columns')
    ck(all(sum(b[v]*c[v] for v in range(len(b)))==theta for c in cols),label+' column regularity')
    ck(all(any(x and not y for x,y in zip(c,e)) for c in cols for e in cols if c!=e),label+' incomparable supports')
    aa,bb,cc,AB,CB,t=build(M,b,q,theta,a_multiplier);ds,reach=stats(len(aa),len(bb),len(cc),AB,CB)
    ck(ds[0]>=1-theta and ds[1]>=1-theta and ds[2]==ds[3]==theta,label+' four literal graph constraints')
    ck(all(F(z,len(aa))==1-t for z in reach),label+' literal distinct-vertex reachability')
    return {'parts':list(map(len,(aa,bb,cc))),'minimum_degrees':list(map(str,ds)),'reach_counts':sorted(set(reach)),'theta':str(theta),'degree':max(map(sum,M)),'F':str(1-t)}
M=[[1,0,1,1,1,0,0],[0,1,1,1,1,0,0],[0,0,1,0,0,1,1],[0,0,0,1,0,1,1],[0,0,0,0,1,1,1],[1,1,0,0,0,1,0],[1,1,0,0,0,0,1]]
b=[F(x,27) for x in [5,5,3,3,3,4,4]];q=[F(x,27) for x in [4,4,3,3,3,5,5]]
details['fixture']=template(M,b,q,F(13,27),'credited seven-type fixture')
details['complement']=template([[1-x for x in r] for r in M],b,q,F(14,27),'complement fixture',2)
ck(details['fixture']['parts']==[108,27,27] and details['fixture']['reach_counts']==[95],'first explicit count')
ck(details['complement']['parts']==[108,27,27] and details['complement']['reach_counts']==[94],'complement explicit count')
# Separate denominators, repeated rows, and asymmetric rational splitting.
MM=[M[0],M[0]]+M[1:];bb=[b[0]/3,2*b[0]/3]+b[1:]
details['split_row']=template(MM,bb,q,F(13,27),'split middle row')
cyclic=[]
for r in range(2,10):
 for p in range(1,r):
    if gcd(p,r)!=1:continue
    T=[[int((v-i)%r<p) for i in range(r)] for v in range(r)]
    z=template(T,[F(1,r)]*r,[F(1,r)]*r,F(p,r),f'cyclic {p}/{r}')
    ck(z['F']==str(F(r-1,r)),f'cyclic residual-zero {p}/{r}')
    cyclic.append(z)
details['cyclic']=cyclic
gaps={(d,e):abs(F(13,27*d)-F(14,27*e)) for d in range(1,5) for e in range(1,5)}
ck(min(gaps.values())==F(1,108),'all16 integer cases exact minimum')
ck([list(x) for x,z in gaps.items() if z==F(1,108)]==[[4,4]],'equality only d=e=4')
details['gaps']=[{'d':d,'e':e,'gap':str(z)} for (d,e),z in gaps.items()]

# Exhaust all literal graphs in several small part sizes. Check lower-bound
# extraction against every qualifying graph; no optimization/extremizer assumed.
exhaust=[]
for na,nb,nc in [(2,2,2),(3,2,2),(3,2,3),(2,3,2),(3,3,3),(4,3,2)]:
 for theta in [F(1,3),F(1,2),F(2,3)]:
    left=[x for x in product(range(1<<nb),repeat=na) if all(F(a.bit_count(),nb)>=1-theta for a in x) and all(F(sum(a>>v&1 for a in x),na)>=1-theta for v in range(nb))]
    right=[y for y in product(range(1<<nb),repeat=nc) if all(F(c.bit_count(),nb)>=theta for c in y) and all(F(sum(c>>v&1 for c in y),nc)>=theta for v in range(nb))]
    total=proper=extras=0
    for AB in left:
     for CB in right:
      total+=1;ds,reach=stats(na,nb,nc,AB,CB);bound=F(max(reach),na)
      if bound==1:continue
      proper+=1;Ts=sorted(set(CB));full=(1<<nb)-1
      ck(all(F(T.bit_count(),nb)==theta for T in Ts),'exhaust exact C degree')
      ck(all(F(sum(c>>v&1 for c in CB),nc)==theta for v in range(nb)),'exhaust exact B-to-C degree')
      sizes=[sum(a==full^T for a in AB) for T in Ts]
      ck(min(sizes)>0,'exhaust all complement classes nonempty')
      ck(sum(sizes)<=na,'exhaust disjoint complement classes')
      if sum(sizes)<na:extras+=1
      tt=F(min(sizes),na);Delta=max(sum(T>>v&1 for T in Ts) for v in range(nb))
      ck(bound==1-tt,'exhaust exact missing-class formula')
      ck(all(sum(F(z,na) for z,T in zip(sizes,Ts) if T>>v&1)<=theta for v in range(nb)),'exhaust row budget with extras retained')
      ck(tt*Delta<=theta and bound>=1-theta/Delta,'exhaust integer-degree lower bound')
    exhaust.append({'parts':[na,nb,nc],'theta':str(theta),'admissible_graphs':total,'F_less_than_1':proper,'extra_A_cases':extras})
details['exhaustive']=exhaust
ck(sum(x['F_less_than_1'] for x in exhaust)>0,'nonvacuous exhaustive lower-bound cases')
ck(sum(x['extra_A_cases'] for x in exhaust)>0,'nonvacuous extra A cases')

# A deliberately weakened positivity hypothesis demonstrates why all middle
# types must survive: nested distinct supports become indistinguishable.
Z=[[1,1,0,0],[0,0,1,1],[1,0,1,0]];zb=[F(1,2),F(1,2),F(0)];zq=[F(1,4)]*4
ck(all(sum(zq[i]*row[i] for i in range(4))==F(1,2) for row in Z),'zero-weight control still row regular')
ck(all(sum(zb[v]*Z[v][i] for v in range(3))==F(1,2) for i in range(4)),'zero-weight control still column regular')
aa,bb,cc,AB,CB,t=build(Z,zb,zq,F(1,2));ds,reach=stats(len(aa),len(bb),len(cc),AB,CB)
ck(set(reach)=={2} and len(aa)==4 and 1-t==F(3,4),'zero-middle-weight control breaks claimed exact reachability')
details['negative_control']={'zero_middle_weight':list(map(str,zb)),'actual_reach_fraction':str(F(reach[0],len(aa))),'invalid_predicted_fraction':str(1-t)}
res={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','checks':len(checks),'details':details,'seconds':time.time()-start,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Fresh ordinary-vertex adjacency, exact boundary-template construction, exhaustive literal small graphs and invalid-positive-boundary control. No submitted code imported or inspected before construction.'}
Path(__file__).with_name('fresh_graph_results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'literal_admissible_graphs':sum(x['admissible_graphs'] for x in exhaust),'proper_cases':sum(x['F_less_than_1'] for x in exhaust),'seconds':time.time()-start}))
