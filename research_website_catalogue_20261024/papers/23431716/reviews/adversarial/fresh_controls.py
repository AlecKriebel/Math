"""Fresh controls from the paper only, before reading submitted helper code.

Uses full reachable-state graphs for small arbitrary schedules; finite tests
supplement, and do not replace, the proof of the reduction.
"""
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations, product
from collections import deque
from math import lcm, prod
import json

ROOT=Path(__file__).resolve().parent
def counts(q,A):
    return [1+int((-a-1)%q in A)-int((-a)%q in A) for a in range(q)]
def storage(q,A,k):
    return sum(c*((a+k)%q) for a,c in enumerate(counts(q,A)))
def graph(banks,oriented):
    Q=sum(q for q,A in banks);P=max(q for q,A in banks)
    offsets=[(q,a) for q,A in banks for a,c in enumerate(counts(q,A)) for _ in range(c)]
    assert len(offsets)==Q
    returns=P if oriented else P-1
    adj=[[] for _ in range(1+Q+returns)]
    adj[0]=list(range(1,Q+1))
    for v,(q,a) in enumerate(offsets,1):
        adj[v]=list(range(Q+1,Q+1+q)) if oriented else [0]+list(range(Q+1,Q+q))
    for v in range(Q+1,len(adj)):adj[v]=[0]
    B=sum(q*(q+1)//2-len(A) for q,A in banks)
    C=Q+B-1
    initial=[C-sum(a for q,a in offsets)]+[a for q,a in offsets]+[0]*returns
    assert min(initial)>=0 and sum(initial)==C
    assert len(adj)==Q+P+int(oriented)
    assert sum(map(len,adj))==Q+sum(q*q for q,A in banks)+P-1+int(oriented)
    arcs={(u,v) for u in range(len(adj)) for v in adj[u]}
    assert len(arcs)==sum(map(len,adj)) and all(u!=v for u,v in arcs)
    if oriented:assert all((v,u) not in arcs for u,v in arcs)
    assert all(not(any(w!=0 for w in adj[v])) for u,v in arcs if u!=0 and v!=0)
    for start in range(len(adj)):
        seen={start};todo=[start]
        while todo:
            for v in adj[todo.pop()]:
                if v not in seen:seen.add(v);todo.append(v)
        assert len(seen)==len(adj)
    return adj,tuple(initial),offsets
def fire(adj,state,v):
    assert state[v]>=len(adj[v])>0
    x=list(state);x[v]-=len(adj[v])
    for w in adj[v]:x[w]+=1
    assert min(x)>=0 and sum(x)==sum(state)
    return tuple(x)
def stable(adj,x):return all(x[v]<len(adj[v]) for v in range(len(adj)))
def exhaustive(adj,initial):
    states=[initial];index={initial:0};edges=[]
    for x in states:
        row=[]
        for v in range(len(adj)):
            if x[v]>=len(adj[v]):
                y=fire(adj,x,v)
                if y not in index:index[y]=len(states);states.append(y)
                row.append(index[y])
        edges.append(row)
    indeg=[0]*len(states)
    for row in edges:
        for j in row:indeg[j]+=1
    todo=deque(i for i,d in enumerate(indeg) if d==0);removed=0
    while todo:
        i=todo.popleft();removed+=1
        for j in edges[i]:
            indeg[j]-=1
            if indeg[j]==0:todo.append(j)
    halts=any(not row for row in edges);cycle=removed<len(states)
    assert halts!=cycle  # Every maximal schedule agrees in these complete finite models.
    return {'states':len(states),'transitions':sum(map(len,edges)),'stable_reachable':halts,'reachable_cycle':cycle}
def canonical(banks,oriented):
    adj,x,offsets=graph(banks,oriented)
    Q=len(offsets);period=lcm(*(q for q,A in banks));C=sum(x);rootfires=0;steps=0
    for k in range(period+1):
        assert x[0]==C-sum(storage(q,A,k) for q,A in banks)
        assert x[1:Q+1]==tuple((a+k)%q for q,a in offsets)
        assert all(v==0 for v in x[Q+1:])
        accepts=all(k%q in A for q,A in banks)
        assert stable(adj,x)==accepts
        if accepts:return {'halt':True,'root_firings':rootfires,'individual_firings':steps}
        if k==period:break
        x=fire(adj,x,0);steps+=1;rootfires+=1
        for v in range(1,Q+1):
            if x[v]>=len(adj[v]):x=fire(adj,x,v);steps+=1
        for v in range(Q+1,len(adj)):
            while x[v]>=len(adj[v]):x=fire(adj,x,v);steps+=1
    return {'halt':False,'root_firings':rootfires,'individual_firings':steps,'checkpoint_period_repeated':True}

start=datetime.now(timezone.utc).isoformat()
bank_tests=0;damaged_failures=0
for q in range(2,9):
    for mask in range(1,1<<q):
        A={i for i in range(q) if mask>>i&1};c=counts(q,A)
        assert sum(c)==q and set(c)<=set((0,1,2))
        for k in range(-q,2*q):
            assert storage(q,A,k)==q*(q-1)//2-len(A)+q*int(k%q in A)
        assert max(storage(q,A,k) for k in range(q))==q*(q+1)//2-len(A)
        # Drop the initial priming of counters: the claimed A no longer labels maxima.
        unprimed=[q*(k%q) for k in range(q)]
        if [k for k in range(q) if unprimed[k]==max(unprimed)]!=sorted(A):damaged_failures+=1
        bank_tests+=1
small=[]
families=[[(q,{i for i in range(q) if mask>>i&1})] for q in (2,3) for mask in range(1,1<<q)]
families += [[(2,{i for i in range(2) if a>>i&1}),(2,{i for i in range(2) if b>>i&1})] for a in range(1,4) for b in range(1,4)]
for banks in families:
    expected=any(all(k%q in A for q,A in banks) for k in range(lcm(*(q for q,A in banks))))
    for oriented in (False,True):
        adj,x,offsets=graph(banks,oriented);r=exhaustive(adj,x)
        assert r['stable_reachable']==expected
        assert canonical(banks,oriented)['halt']==expected
        small.append({'banks':[(q,sorted(A)) for q,A in banks],'oriented':oriented,**r})
print('banks and exhaustive small graphs complete',flush=True)

# Independent two-variable SAT predicate generation: list all one/two-literal clauses.
primes=[3,5]
clauses=[(a,) for a in (-1,1,-2,2)]+list(product((-1,1),(-2,2)))
formulas=[[]]+[[c] for c in clauses]+[[c,d] for c in clauses for d in clauses]
sat=[]
for formula in formulas:
    truth=lambda assignment:all(any(assignment[abs(lit)-1]==(lit>0) for lit in clause) for clause in formula)
    expected=any(truth(a) for a in product((False,True),repeat=2))
    banks=[(p,{0,1}) for p in primes]
    for clause in formula:
        I=sorted({abs(l)-1 for l in clause});q=prod(primes[i] for i in I)
        A={k for k in range(q) if all(k%primes[i] in (0,1) for i in I) and any((k%primes[abs(l)-1]==1)==(l>0) for l in clause)}
        assert len(A)==(1<<len(I))-1
        banks.append((q,A))
    residuals=[k for k in range(prod(primes)) if all(k%q in A for q,A in banks)]
    assert bool(residuals)==expected
    for oriented in (False,True):
        result=canonical(banks,oriented)
        assert result['halt']==expected
        sat.append({'formula':formula,'oriented':oriented,'satisfiable':expected,**result})

# Negative control: changing root mass by one can destroy the intended test.
banks=[(3,{0,1})];adj,x,_=graph(banks,False)
wrong=tuple(v+int(i==0) for i,v in enumerate(x))
bad=exhaustive(adj,wrong)
assert canonical(banks,False)['halt'] and not bad['stable_reachable']

out={'started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_FRESH_CONTROLS','bank_subsets_checked':bank_tests,'unprimed_variants_detected':damaged_failures,'complete_reachable_graph_checks':small,'SAT_canonical_checks':sat,'extra_root_chip_negative_control':bad,'limits':'Finite controls only; general correctness assessed by direct proof. No submitted helpers read or imported.'}
(ROOT/'fresh-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'banks':bank_tests,'all_schedule_cases':len(small),'reachable_states_total':sum(i['states'] for i in small),'SAT_cases':len(sat),'largest_graph_state_count':max(i['states'] for i in small)}))
