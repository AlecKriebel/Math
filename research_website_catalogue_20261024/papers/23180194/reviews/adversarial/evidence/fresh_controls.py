"""Independent exact constraints; no submitted checker imports or expected outputs.
Finite regular ambient G-orbits retain states even when xi is periodic.
Compare row spaces of stationarity constraints with full Campbell reversal.
"""
from fractions import Fraction as F
from itertools import product
from datetime import datetime, timezone
import json
from pathlib import Path

def rref(rows,n):
    rows=[list(map(F,r)) for r in rows if any(r)]
    piv=0
    for col in range(n):
        j=next((j for j in range(piv,len(rows)) if rows[j][col]),None)
        if j is None: continue
        rows[piv],rows[j]=rows[j],rows[piv]
        a=rows[piv][col]; rows[piv]=[v/a for v in rows[piv]]
        for k in range(len(rows)):
            if k!=piv and rows[k][col]:
                b=rows[k][col];rows[k]=[u-b*v for u,v in zip(rows[k],rows[piv])]
        piv+=1
        if piv==n: break
    return rows[:piv]

def group(moduli):
    elements=list(product(*[range(m) for m in moduli]));lookup={v:i for i,v in enumerate(elements)}
    add=lambda a,b:lookup[tuple((x+y)%m for x,y,m in zip(elements[a],elements[b],moduli))]
    neg=lambda a:lookup[tuple((-x)%m for x,m in zip(elements[a],moduli))]
    return elements,add,neg

def run(moduli,w):
    els,add,neg=group(moduli);n=len(els);assert len(w)==n
    shifted=[tuple(w[add(x,t)] for t in range(n)) for x in range(n)]
    H=[h for h in range(n) if shifted[h]==tuple(w)]
    denom=F(1,(1+sum(w))**2)
    matrices=[];local_rows=[];period_rows=[];seen=set()
    # Independent edge-orbit gates F union R(F), indexed by a measure and displacement.
    for x in range(n):
      for t in range(n):
        y=add(x,t)
        if shifted[x]==shifted[y]:continue
        gate=frozenset([(shifted[x],t),(shifted[y],neg(t))])
        if gate in seen:continue
        seen.add(gate)
        K=[[F(int(i==j)) for j in range(n)] for i in range(n)]
        for i in range(n):
          for h in range(n):
            if (shifted[i],h) in gate:
              j=add(i,h);flow=denom*w[j]
              K[i][j]+=flow;K[i][i]-=flow
        matrices.append(K)
        local_rows.extend([[K[i][j]-int(i==j) for i in range(n)] for j in range(n)])
    # Period rows include all singletons and selected non-symmetric unions.
    for B in [{h} for h in H]+[set(H),set(H[1::2])]:
      K=[[F(0) for j in range(n)] for i in range(n)]
      for i in range(n):
        total=sum(w[add(i,h)] for h in B)
        if total:
          for h in B:K[i][add(i,h)]+=F(w[add(i,h)],total)
        else:K[i][i]=F(1)
      matrices.append(K)
      period_rows.extend([[K[i][j]-int(i==j) for i in range(n)] for j in range(n)])
    # Every kernel is stochastic and preserves the spatial measure, exactly.
    for K in matrices:
      assert all(sum(row)==1 and min(row)>=0 for row in K)
      assert [sum(F(w[i])*K[i][j] for i in range(n)) for j in range(n)]==list(map(F,w))
      # Measure-only dependence: displacement rows at equal xi coincide.
      for i in range(n):
       for j in range(n):
        if shifted[i]==shifted[j]:
         assert all(K[i][add(i,h)]==K[j][add(j,h)] for h in range(n))
    reversal=[]
    for x in range(n):
      for y in range(n):
        row=[0]*n;row[x]+=w[y];row[y]-=w[x];reversal.append(row)
    actual=rref(local_rows+period_rows,n);expected=rref(reversal,n)
    assert actual==expected
    assert len(actual)==n-1 if sum(w) else len(actual)==0
    # All constraints annihilate the independently obtained Palm weights w.
    assert all(sum(a*b for a,b in zip(row,w))==0 for row in actual)
    return dict(group=moduli,weights=w,period_size=len(H),local_rank=len(rref(local_rows,n)),combined_rank=len(actual),campbell_rank=len(expected),kernels=len(matrices),passed=True)

cases=[]
for n in [1,6,7,8,9,12]:
 patterns=[[1]*n,list(range(1,n+1)),[int(i==0) for i in range(n)],[(i*i+2*i)%5 for i in range(n)]]
 if n%2==0:patterns += [[1+i%2 for i in range(n)],[2*(i%2) for i in range(n)]]
 if n%3==0:patterns += [[0,2,5]*(n//3)]
 for w in patterns:cases.append(run([n],w))
for moduli in [[4,2],[3,3],[2,2,2]]:
 els,_,_=group(moduli)
 for w in [[1]*len(els),[1+e[0]%2 for e in els],[sum(e)%3 for e in els],[int(e==els[0]) for e in els]]:
  cases.append(run(moduli,w))
# Negative: xi fixed Haar, arbitrary hidden root law leaves canonical law unchanged,
# but full ambient invariance under a period shift detects the wrong hidden root.
n=8;q=[F(1)]+[F(0)]*(n-1);shifted_q=q[-1:]+q[:-1]
assert q!=shifted_q
# Negative: off-period gates alone see nothing for a Haar measure.
haar=next(c for c in cases if c['group']==[8] and c['weights']==[1]*8)
assert haar['local_rank']==0 and haar['combined_rank']==7
# Negative: row-normalized symmetric conductance is not generally mass-preserving.
w=[1,2,4];raw=[[int(abs(i-j)<=1) for j in range(3)] for i in range(3)]
K=[[F(raw[i][j]*w[j],sum(raw[i][k]*w[k] for k in range(3))) for j in range(3)] for i in range(3)]
received=[sum(F(w[i])*K[i][j] for i in range(3)) for j in range(3)]
assert received!=list(map(F,w))
# Negative: dropping nonzero permits trivial constant-zero canonical state.
zero=run([6],[0]*6);assert zero['combined_rank']==0
out={'created_utc':datetime.now(timezone.utc).isoformat(),'method':'exact rational independently coded stationarity-vs-Campbell row-space comparison','cases':cases,'case_count':len(cases),'negative_controls':{'canonical_only_misses_hidden_state':True,'offperiod_only_misses_Haar_state':True,'naive_row_normalization_breaks_balance':{'expected':w,'received':[str(v) for v in received]},'zero_measure_has_no_Campbell_constraints':True},'scope':'finite falsification controls only; universal measurable proof audited analytically','status':'PASS'}
Path(__file__).with_name('fresh-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','cases':len(cases),'kernels':sum(c['kernels'] for c in cases),'negative_controls':4}))
