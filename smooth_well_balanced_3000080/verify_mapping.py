import itertools,json
checks=0
for n in range(1,5):
 pairs=list(itertools.combinations(range(n),2))
 for mask in range(1<<len(pairs)):
  edges=[e for i,e in enumerate(pairs) if mask>>i&1]
  deg=[sum(v in e for e in edges) for v in range(n)]
  odd=[v for v in range(n) if deg[v]%2]
  cuts=[s for s in range(1,(1<<n)-1)]
  ug={s:sum(bool(s>>a&1)!=bool(s>>b&1) for a,b in edges) for s in cuts}
  for bits in range(1<<len(edges)):
   arcs=[(b,a) if bits>>i&1 else (a,b) for i,(a,b) in enumerate(edges)]
   out=[sum(a==v for a,b in arcs) for v in range(n)]
   inn=[deg[v]-out[v] for v in range(n)]
   smooth=all(abs(out[v]-inn[v])<=1 for v in range(n))
   dc={s:sum((s>>a&1) and not(s>>b&1) for a,b in arcs) for s in cuts}
   rev={s:sum((s>>b&1) and not(s>>a&1) for a,b in arcs) for s in cuts}
   def wb(d):
    return all(min(d[s] for s in cuts if (s>>u&1) and not(s>>v&1)) >= min(ug[s] for s in cuts if (s>>u&1) and not(s>>v&1))//2 for u in range(n) for v in range(n) if u!=v)
   if wb(dc)!=wb(rev): raise RuntimeError('reversal')
   for tm in range(1<<len(odd)):
    T=[v for i,v in enumerate(odd) if tm>>i&1]
    # Upper-outdegree version before reversal equals EGRES requirement afterwards.
    a=smooth and wb(dc) and all(out[v]<=deg[v]//2 for v in T)
    b=smooth and wb(rev) and all(out[v]<inn[v] for v in T)
    if a!=b: raise RuntimeError('mapping')
    checks+=1
print(json.dumps({'checks':checks,'result':'pass','scope':'all simple graphs through 4 vertices, all orientations and odd-vertex subsets; not a full NP-hardness certificate'}))
