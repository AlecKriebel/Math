"""Exhaustive exact checks of the finite automaton escape/block-count lemma."""
from itertools import product
import json
count=0; automata=0;certified=0
for m in range(1,4):
  sink=m
  for raw in product(range(m+1), repeat=2*m):
    trans=[raw[2*s:2*s+2] for s in range(m)]+[(sink,sink)]
    reach={0};todo=[0]
    while todo:
      s=todo.pop()
      for t in trans[s]:
        if t!=sink and t not in reach:reach.add(t);todo.append(t)
    dist={sink:0}
    for _ in range(m):
      for s in range(m):
        ds=[dist[t]+1 for t in trans[s] if t in dist]
        if ds:dist[s]=min(ds+[dist.get(s,m+1)])
    def run(s,w):
      for a in w:s=trans[s][a]
      return s
    for s in reach:
      brute=any(run(s,w)==sink for w in product((0,1),repeat=m))
      assert brute==(s in dist)
      count+=1
      if s in dist:
        d=dist[s]
        assert 1<=d<=m
        assert any(run(s,w)==sink for w in product((0,1),repeat=d))
        assert not any(run(s,w)==sink for w in product((0,1),repeat=d-1))
        count+=3
    if all(s in dist for s in reach):
      certified+=1;N=max(dist[s] for s in reach)
      for s in reach:
        surv=sum(run(s,w)!=sink for w in product((0,1),repeat=N))
        assert surv<=2**N-1;count+=1
      # exact dynamic counts to three blocks plus one remainder
      v={0:1}
      for length in range(1,3*N+2):
        nv={}
        for s,num in v.items():
          for t in trans[s]:
            if t!=sink:nv[t]=nv.get(t,0)+num
        v=nv;k,r=divmod(length,N)
        assert sum(v.values())<=(2**N-1)**k*2**r;count+=1
    automata+=1
print(json.dumps({'automata':automata,'certified':certified,'assertions':count,'scope':'all binary total automata with one through three safe states; graph lemma controls only'},sort_keys=True))
