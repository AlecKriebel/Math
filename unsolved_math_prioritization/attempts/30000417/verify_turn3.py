#!/usr/bin/env python3
"""Exhaustive finite-state certificate: every length, d=2, six-list union <=8.
Only Python 3 standard library. No state cap and no random sampling.
"""
from itertools import combinations, product
from collections import Counter
from hashlib import sha256
import json


def automaton(M):
    K=6;d=2;rowmask=(1<<M)-1
    lists=sorted(sum(1<<j for j in js) for js in combinations(range(M),K))
    far=[sum(1<<j for j in range(M) if abs(i-j)>=d) for i in range(M)]
    lmasks={L:sum(rowmask<<(M*j) for j in range(M) if L>>j&1) for L in lists}
    states=[];index={};depth=[];parent=[];incoming=[];first=[]
    for A in lists:
        for B in lists:
            state=sum((A&far[b])<<(M*b) for b in range(M) if B>>b&1)
            assert state
            if state not in index:
                index[state]=len(states);states.append(state);depth.append(2)
                parent.append(-1);incoming.append(B);first.append(A)
    initial=len(states);head=0;transitions=0;minrob=M;minrob_index=0
    while head<len(states):
        state=states[head]
        rows=[(state>>(M*b))&rowmask for b in range(M)]
        rob=sum(bool(x) and x.bit_length()-1-((x&-x).bit_length()-1)>=3 for x in rows)
        if rob<minrob:minrob=rob;minrob_index=head
        full=0
        for c in range(M):
            nextrow=0
            for b in range(M):
                if (far[c]>>b&1) and (rows[b]&far[c]):nextrow|=1<<b
            full|=nextrow<<(M*c)
        for L in lists:
            nxt=full&lmasks[L];transitions+=1
            assert nxt, ('empty state',M,head,L)
            if nxt not in index:
                index[nxt]=len(states);states.append(nxt);depth.append(depth[head]+1)
                parent.append(head);incoming.append(L);first.append(-1)
        head+=1
    assert head==len(states)
    witness=[];cur=minrob_index
    while parent[cur]>=0:
        witness.append(incoming[cur]);cur=parent[cur]
    witness.extend([incoming[cur],first[cur]]);witness.reverse()
    witness=[[j+1 for j in range(M) if L>>j&1] for L in witness]
    h=sha256();width=(M*M+7)//8
    for state in sorted(states):h.update(state.to_bytes(width,'little'))
    hist={str(k):v for k,v in sorted(Counter(depth).items())}
    return dict(palette_size=M,list_size=K,separation=d,initial_states=initial,
                closed_states=len(states),checked_transitions=transitions,
                empty_state_reached=False,max_shortest_prefix_length=max(depth),
                depth_histogram=hist,state_encoding=f'{M} rows of {M} bits; each state in {width} little-endian bytes; numeric ascending order',
                state_set_sha256=h.hexdigest(),minimum_robust_rows=minrob,
                minimum_robust_witness_lists=witness)


def pair_layers(L,d):
    R={(a,b) for a in L[0] for b in L[1] if abs(a-b)>=d};layers=[sorted(R)]
    for C in L[2:]:
        R={(b,c) for a,b in R for c in C if abs(a-c)>=d and abs(b-c)>=d}
        layers.append(sorted(R))
    return layers

results=[automaton(M) for M in [6,7,8]]
expected={6:(2,2),7:(2221,15547),8:(227952,6382656)}
for result in results:
    M=result['palette_size']
    assert (result['closed_states'],result['checked_transitions'])==expected[M]
    layers=pair_layers(result['minimum_robust_witness_lists'],2)
    assert layers[-1]
    rob=0
    for b in set(x[1] for x in layers[-1]):
        A=[a for a,y in layers[-1] if y==b]
        rob+=max(A)-min(A)>=3
    assert rob==result['minimum_robust_rows']

# Explicit five-list obstruction on P6, one below its proposed value six.
lower=[[1,2,5,6,7],[2,3,4,5,6],[1,2,3,5,6],
       [2,3,4,5,6],[1,2,3,5,6],[2,3,4,5,6]]
layers=pair_layers(lower,2)
assert not layers[-1]
assert all(len(set(L))==5 for L in lower)
assert (3*2*(6-1))//6+1==6
valid_tuples=sum(all(abs(x[i]-x[j])>=2 for i in range(6) for j in range(i+1,min(i+3,6))) for x in product(*lower))
assert valid_tuples==0
print(json.dumps(dict(problem_id=30000417,turn=3,status='exhaustive finite-state closure passed',
    theorem='For every n>=1, arbitrary six-element lists using at most eight distinct integer labels admit a (2,2)-labeling of P_n.',
    automata=results,lower_obstruction={'n':6,'d':2,'list_size':5,'lists':lower,'reachable_pair_layers':layers,'independent_full_tuples_checked':5**6,'valid_tuples':valid_tuples},
    boundary='For n>=6 the six-list bound agrees with the original floor target. Larger unions and other d remain unresolved.',
    dependencies='Python 3 standard library'),indent=2))
