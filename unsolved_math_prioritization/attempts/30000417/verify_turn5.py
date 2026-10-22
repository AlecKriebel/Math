#!/usr/bin/env python3
"""Exact all-length nine-palette closure, with transition lookup precomputation.
Python 3 standard library only; no cap, search heuristic or random choice.
"""
from itertools import combinations
from hashlib import sha256
import json

M=9;K=6;d=2;rowmask=(1<<M)-1
lists=sorted(sum(1<<a for a in A) for A in combinations(range(M),K))
far=[sum(1<<a for a in range(M) if abs(a-b)>=d) for b in range(M)]
masks=[sum(rowmask<<(M*b) for b in range(M) if L>>b&1) for L in lists]
# Contribution of one old row b to the unrestricted next relation.
table=[]
for b in range(M):
    contribution=[]
    for row in range(1<<M):
        contribution.append(sum(1<<(M*c+b) for c in range(M)
                                if (far[c]>>b&1) and (row&far[c])))
    table.append(contribution)
seen={sum((A&far[b])<<(M*b) for b in range(M) if B>>b&1)
      for A in lists for B in lists}
assert 0 not in seen
initial=len(seen);queue=list(seen);head=0
while head<len(queue):
    state=queue[head];full=0
    for b in range(M):full|=table[b][(state>>(M*b))&rowmask]
    successors={full&mask for mask in masks}
    assert 0 not in successors
    new=successors-seen
    seen.update(new);queue.extend(new);head+=1
assert head==len(seen)==4087257
assert initial==7056 and len(lists)==84
h=sha256()
for state in sorted(seen):h.update(state.to_bytes(11,'little'))
closure=dict(palette_size=M,list_size=K,separation=d,initial_states=initial,
             closed_states=len(seen),checked_input_transitions=len(lists)*len(seen),
             empty_state_reached=False,state_set_sha256=h.hexdigest(),
             encoding='9 rows of 9 bits; numeric ascending states, each in 11 little-endian bytes')

# Independent straightforward set-pair recurrence and witness recovery.
def layers_and_witness(L,d):
    layers=[{(a,b):None for a in L[0] for b in L[1] if abs(a-b)>=d}]
    for C in L[2:]:
        nxt={}
        for a,b in sorted(layers[-1]):
            for c in C:
                if abs(a-c)>=d and abs(b-c)>=d:nxt.setdefault((b,c),(a,b))
        layers.append(nxt)
    if not layers[-1]:return [sorted(x) for x in layers],None
    pair=min(layers[-1]);rev=[pair[1],pair[0]]
    for i in range(len(layers)-1,0,-1):pair=layers[i][pair];rev.append(pair[0])
    return [sorted(x) for x in layers],rev[::-1]

L10=[sorted({(i+j)%10+1 for j in range(6)}) for i in range(10)]
cooccurrence=all(any(a in A and b in A for A in L10) for a,b in combinations(range(1,11),2))
assert cooccurrence
_,color10=layers_and_witness(L10,2)
assert color10 and all(color10[i] in L10[i] for i in range(10))
assert all(abs(color10[i]-color10[j])>=2 for i in range(10) for j in range(i+1,min(i+3,10)))
assert 3*2*9//10+1==6

L3=[[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[1,2,3,4,6,7,8,9],
    [2,3,4,5,6,7,8,9],[2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8],
    [1,2,3,4,6,7,8,9],[1,2,3,4,5,6,7,8],[2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,8],[1,2,3,4,6,7,8,9],[1,2,3,4,5,6,7,8],
    [2,3,4,5,6,7,8,9]]
R3,color3=layers_and_witness(L3,3)
assert color3 is None and not R3[-1]
assert all(len(set(A))==8 for A in L3)
assert 3*3*12//13+1==9
print(json.dumps(dict(problem_id=30000417,turn=5,status='all exact controls passed',
    closure=closure,
    recoding_barrier=dict(n=10,d=2,list_size=6,lists=L10,every_label_pair_cooccurs=cooccurrence,
                         explicit_valid_labeling=color10,
                         conclusion='Any single global label map preserving six distinct labels in every list is injective, so cannot reduce this ten-label union to nine.'),
    other_parameter_control=dict(n=13,d=3,list_size=8,lists=L3,reachable_pair_layers=R3,
                                 source_conjectured_size=9,meaning='One-below-target obstruction, not a counterexample to the source conjecture.'),
    final_status='Original unrestricted-palette, all-d floor conjecture remains unresolved after five genuine author turns.',
    dependencies='Python 3 standard library'),indent=2))
