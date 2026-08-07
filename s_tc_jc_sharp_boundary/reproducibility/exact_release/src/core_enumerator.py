from collections import Counter, defaultdict, deque
from itertools import permutations, product

def multiset_permutations(items): return sorted(set(permutations(items)))
def weak_compositions(total, parts):
    if parts==1: yield (total,); return
    for first in range(total+1):
        for rest in weak_compositions(total-first,parts-1): yield (first,)+rest

def path_sequence_triples(event_types):
    triples=set()
    for word in multiset_permutations(event_types):
        for lengths in weak_compositions(len(word),3):
            paths=[]; off=0
            for length in lengths:
                paths.append(tuple(word[off:off+length])); off+=length
            triples.add(tuple(paths))
    return sorted(triples)
def reversed_template(branches,paths): return (branches[::-1],tuple(tuple(reversed(p)) for p in paths))
def canonical_template(branches,paths):
    c=[]
    for cb,cp in ((branches,paths),reversed_template(branches,paths)):
        for perm in permutations(range(3)): c.append((cb,tuple(cp[i] for i in perm)))
    return min(c)
def event_segment_signs(path):
    if not path: return (None,)
    signs=[-1 if path[0]=='S' else +1]
    for l,r in zip(path,path[1:]):
        a=+1 if l=='S' else -1; b=-1 if r=='S' else +1
        if a!=b: return None
        signs.append(a)
    signs.append(+1 if path[-1]=='S' else -1)
    return tuple(signs)
def instantiate(branches,paths,empty_signs):
    vertices={'U':branches[0],'V':branches[1]}; edges=[]; ei=0; xi=0
    for pi,path in enumerate(paths):
        names=['U']
        for ev in path:
            name='S' if ev=='S' else f'X{xi}'; xi += ev=='X'; vertices[name]=ev; names.append(name)
        names.append('V'); signs=event_segment_signs(path)
        if signs is None: return None
        if not path: signs=(empty_signs[ei],); ei+=1
        for si,(l,r,s) in enumerate(zip(names,names[1:],signs)):
            t,h=(l,r) if s==1 else (r,l)
            edges.append({'tail':t,'head':h,'path':pi,'segment':si})
    return vertices,edges
def degrees(vertices,edges):
    ind=Counter(); out=Counter()
    for e in edges: out[e['tail']]+=1; ind[e['head']]+=1
    return {v:(ind[v],out[v]) for v in vertices}
def is_acyclic_reachable(vertices,edges):
    out=defaultdict(list); ind=Counter()
    for e in edges: out[e['tail']].append(e['head']); ind[e['head']]+=1
    q=deque(v for v in vertices if ind[v]==0); order=[]
    while q:
        v=q.popleft(); order.append(v)
        for w in out[v]:
            ind[w]-=1
            if ind[w]==0:q.append(w)
    if len(order)!=len(vertices): return False
    seen={'S'}; q=deque(['S'])
    while q:
        v=q.popleft()
        for w in out[v]:
            if w not in seen: seen.add(w); q.append(w)
    return seen==set(vertices)
def degree_constraints_hold(vertices,edges):
    req={'S':(0,2),'X':(2,0),'T':(1,2),'R':(2,1)}; act=degrees(vertices,edges)
    return all(act[v]==req[c] for v,c in vertices.items())
def minimal_strong_repairs(vertices,edges):
    out=defaultdict(list)
    for i,e in enumerate(edges): out[e['tail']].append((i,e['head']))
    obl=[]
    for v,c in vertices.items():
        children=out[v]
        if c in {'T','S'}:
            if not any(vertices[w] in {'T','S'} for _,w in children): obl.append(tuple(i for i,_ in children))
        elif c=='R':
            assert len(children)==1
            i,w=children[0]
            if vertices[w] in {'R','X'}: obl.append((i,))
    if not obl:return ((),)
    reps=[]
    for mask in range(1<<len(edges)):
        ch=tuple(i for i in range(len(edges)) if mask>>i&1)
        if all(any(i in ch for i in o) for o in obl): reps.append(ch)
    m=min(map(len,reps)); return tuple(r for r in reps if len(r)==m)
def enumerate_cores():
    accepted={}; raw=0
    for br in (0,1):
        branches=('T','T') if br==0 else ('T','R'); events=('S',)+('X',)*(2-br)
        for paths in path_sequence_triples(events):
            fs=[event_segment_signs(p) for p in paths]
            if any(s is None for s in fs): continue
            ec=sum(not p for p in paths)
            for es in product((-1,1),repeat=ec):
                inst=instantiate(branches,paths,es)
                if not inst: continue
                v,e=inst
                if not degree_constraints_hold(v,e) or not is_acyclic_reachable(v,e): continue
                raw+=1; can=canonical_template(branches,paths)
                if can in accepted: continue
                accepted[can]={'vertex_types':v,'directed_segments':e,'branches':branches,'paths':paths,'repairs':minimal_strong_repairs(v,e)}
    return raw,list(accepted.values())
if __name__=='__main__':
    import pprint
    raw,cores=enumerate_cores(); print('raw',raw,'cores',len(cores))
    for i,c in enumerate(cores):
        print('\nCORE',i,'branches',c['branches'],'paths',c['paths'],'repairs',c['repairs'])
        print('vertices',c['vertex_types']); print('segments')
        for j,e in enumerate(c['directed_segments']): print(j,e)
