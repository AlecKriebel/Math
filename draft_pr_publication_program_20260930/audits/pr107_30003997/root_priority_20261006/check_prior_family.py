from pathlib import Path
import datetime, hashlib, itertools, json, os, random

A = Path(__file__).resolve().parent
def require(condition, message):
    if not condition: raise RuntimeError(message)

def check(edges, exhaustive, seed):
    h = len(edges)
    vertices = sorted(set().union(*map(set, edges)))
    require(len(vertices)==h, 'balanced RXC3 input')
    require(all(len(e)==3 for e in edges), '3-uniform')
    require(all(sum(v in e for e in edges)==3 for v in vertices), '3-regular')
    overlap = [(i,j) for i in range(h) for j in range(i+1,h) if set(edges[i]) & set(edges[j])]
    selectors = [('t',i) for i in range(h)] + [('f',i) for i in range(h)]
    u = [('u',i) for i in range(h)]
    elements = [('v',v) for v in vertices]
    w = [('w',i,j) for i,j in overlap]
    nonroot = selectors+u+elements+w
    incoming = {q:['s'] for q in selectors}
    incoming.update({q:[('t',i),('f',i)] for i,q in enumerate(u)})
    incoming.update({('v',v):[('u',i) for i,e in enumerate(edges) if v in e] for v in vertices})
    incoming.update({('w',i,j):[('u',i),('u',j)] for i,j in overlap})
    arcs = [(p,q) for q in nonroot for p in incoming[q]]
    cost = {(v,e):int((v[0]=='v' and e[0]=='s' and e[1][0]=='f') or
                     (v[0]=='w' and e[0]=='s' and e[1][0]=='t')) for v in nonroot for e in arcs}
    require(max(map(len,incoming.values()))<=3,'degree bound')
    path_offset = 4*h+3*(h+len(w))
    choose = u+elements+w
    choices = [incoming[q] for q in choose]
    rng = random.Random(seed)
    selections = itertools.product(*choices) if exhaustive else ([rng.choice(cs) for cs in choices] for _ in range(1500))
    counts = {'trees':0,'zero_cost_trees':0,'positive_cost_trees':0,'zero_cost_exact_cover_failures':0}
    for selected in selections:
        parent = {q:'s' for q in selectors}
        parent.update(zip(choose,selected))
        total = shifted = 0
        for dest in nonroot:
            q = dest; seen = set()
            while q!='s':
                require(q not in seen,'cycle')
                seen.add(q); e=(parent[q],q)
                total += cost[dest,e]
                shifted += cost[dest,e]+1
                q=parent[q]
        black = {i for i in range(h) if parent[('u',i)][0]=='t'}
        monochromatic = all(parent[('v',v)][1] in black for v in vertices) and all(parent[q][1] not in black for q in w)
        require((total==0)==monochromatic,'prior/cost equivalence')
        require(shifted-total==path_offset,'universal positive offset')
        exact = all(sum(v in edges[i] for i in black)==1 for v in vertices)
        if total==0: require(exact,'zero-cost implication to exact cover')
        counts['trees']+=1
        counts['zero_cost_trees' if total==0 else 'positive_cost_trees']+=1
    # The independent exact-cover search certifies the existential negative control;
    # random sampled trees alone are not used to infer absence.
    covers=[]
    for bits in itertools.product((0,1),repeat=h):
        ids=[i for i,b in enumerate(bits) if b]
        if all(sum(v in edges[i] for i in ids)==1 for v in vertices): covers.append(ids)
    if exhaustive: require(bool(counts['zero_cost_trees'])==bool(covers),'existential exact-cover equivalence')
    constructed_cover_costs=[]
    for ids in covers:
        parent={q:'s' for q in selectors}
        parent.update({('u',i):('t' if i in ids else 'f',i) for i in range(h)})
        parent.update({('v',v):('u',next(i for i in ids if v in edges[i])) for v in vertices})
        parent.update({('w',i,j):('u',i if i not in ids else j) for i,j in overlap})
        require(all(parent[('v',v)][1] in ids for v in vertices),'forward cover membership')
        require(all(parent[q][1] not in ids for q in w),'forward overlap membership')
        total=shifted=0
        for dest in nonroot:
            q=dest
            while q!='s':
                e=(parent[q],q)
                total+=cost[dest,e]; shifted+=cost[dest,e]+1; q=parent[q]
        require(total==0 and shifted==path_offset,'dense-table evaluation of constructed positive cover')
        constructed_cover_costs.append({'selected_hyperedges':ids,'binary_cost':total,'positive_cost':shifted})
    return {'h':h,'overlaps':len(w),'vertices':len(nonroot)+1,'arcs':len(arcs),'positive_threshold':path_offset,'exhaustive':exhaustive,'exact_cover_count':len(covers),'constructed_cover_costs':constructed_cover_costs,**counts}

cases=[check(list(itertools.combinations(range(4),3)),True,1),check([tuple((i+j)%6 for j in range(3)) for i in range(6)],False,2)]
out={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'cases':cases,'verdict':'PASS','limits':'Finite checks complement the arbitrary-size proof comparison; the six-vertex graph is sampled with all exact covers searched, not an exhaustive tree claim.'}
(A/'ROOT_PRIOR_FINITE_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
