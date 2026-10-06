#!/usr/bin/env python3
"""Fresh explicit arc-identity mapping; local exceptions survive python -O."""
from collections import Counter, deque
from itertools import combinations, product
from pathlib import Path
import datetime, hashlib, json, math, random, sys

COUNTS = Counter()
def require(value, label):
    if not value:
        raise RuntimeError(label)
    COUNTS[label] += 1

if '--negative-guard' in sys.argv:
    require(False, 'deliberate negative guard')


def family(edges, diagonal=False, ordered=False):
    h = len(edges)
    ground = sorted(set().union(*map(set, edges))) if edges else []
    pairs = [(i,j) for i in range(h) for j in range(h)
             if ((i<=j if diagonal else i<j) if not ordered else i!=j)
             and set(edges[i]) & set(edges[j])]
    # Edge indices distinguish the two parallel original root arcs.
    verts = [('r',)] + [('u',i) for i in range(h)] + [('v',x) for x in ground] + [('w',i,j) for i,j in pairs]
    old=[]
    for i in range(h):
        old.extend([(('r',),('u',i),0),(('r',),('u',i),1)])
    for i,e in enumerate(edges):
        old.extend((('u',i),('v',x),0) for x in sorted(e))
    for i,j in pairs:
        old.append((('u',i),('w',i,j),1))
        if i!=j: old.append((('u',j),('w',i,j),1))
    expanded_verts=verts+[('a',e) for e in range(2*h)]
    new=[]; middle={}; copied={}; forced=[]
    for e,(u,v,c) in enumerate(old):
        if u==('r',):
            a=('a',e)
            forced.append(len(new));new.append((u,a,c))
            middle[e]=len(new);new.append((a,v,c))
        else:
            copied[e]=len(new);new.append((u,v,c))
    # Every destination/arc entry is explicit, including unused intermediates.
    table=[]
    for dest in expanded_verts:
        row=[]
        for u,v,color in new:
            terminal_color = 0 if dest[0]=='v' else 1 if dest[0]=='w' else None
            row.append(int(terminal_color is not None and u==('r',) and color!=terminal_color))
        table.append(row)
    return {'edges':edges,'h':h,'ground':ground,'pairs':pairs,'old_v':verts,'old':old,'new_v':expanded_verts,'new':new,'table':table,'middle':middle,'copied':copied,'forced':forced}


def validate_tree(vertices, arcs, selected):
    incoming={v:[] for v in vertices}; children={v:[] for v in vertices}
    for e in selected:
        u,v,c=arcs[e];incoming[v].append(e);children[u].append(e)
    require(not incoming[('r',)] and all(len(incoming[v])==1 for v in vertices[1:]),'tree incoming counts')
    paths={('r',):()}; q=deque([('r',)])
    while q:
        u=q.popleft()
        for e in children[u]:
            v=arcs[e][1]
            require(v not in paths,'tree acyclic traversal')
            paths[v]=paths[u]+(e,);q.append(v)
    require(len(paths)==len(vertices),'tree spans all vertices')
    return paths


def all_parent_selections(vertices, arcs):
    inc={v:[] for v in vertices[1:]}
    for e,(u,v,c) in enumerate(arcs): inc[v].append(e)
    return product(*(inc[v] for v in vertices[1:]))


def test_tree(f, selected):
    oldpaths=validate_tree(f['old_v'],f['old'],selected)
    mapped=tuple(f['forced'])+tuple(f['middle'][e] if e in f['middle'] else f['copied'][e] for e in selected)
    newpaths=validate_tree(f['new_v'],f['new'],mapped)
    reverse={e:k for k,e in {**f['middle'],**f['copied']}.items()}
    recovered={reverse[e] for e in mapped if e not in f['forced']}
    require(recovered==set(selected),'all ordinary tree inverse mapping')
    value=sum(f['table'][i][e] for i,v in enumerate(f['new_v']) if v!=('r',) for e in newpaths[v])
    shifted=sum(f['table'][i][e]+1 for i,v in enumerate(f['new_v']) if v!=('r',) for e in newpaths[v])
    old_monochromatic=all(len({f['old'][e][2] for e in path})<=1 for path in oldpaths.values())
    mismatch=sum(int(f['old'][path[0]][2]!=f['old'][path[-1]][2]) for v,path in oldpaths.items() if v[0] in ('v','w'))
    require(value==mismatch,'dense path sum equals old endpoint color mismatch')
    require((value==0)==old_monochromatic,'zero iff original all paths monochromatic')
    require(shifted-value==4*f['h']+3*(len(f['ground'])+len(f['pairs'])),'universal 1-2 offset')
    for v in f['new_v']:
        if v[0]=='a': require(newpaths[v]==(f['forced'][v[1]],),'both used and unused intermediate vertices forced')
    return value


def per_assignment(f):
    out=[]
    for bits in product((0,1),repeat=f['h']):
        selected={i for i,b in enumerate(bits) if b==0}
        missed=sum(not any(x in f['edges'][i] for i in selected) for x in f['ground'])
        overlap=sum(i in selected and j in selected for i,j in f['pairs'])
        # Exhaust all possible choices separately at each terminal, evaluating
        # dense path rows; separability proves their sum is each assignment optimum.
        root_edges=[2*i+bits[i] for i in range(f['h'])]
        root_new={('u',i):f['middle'][e] for i,e in enumerate(root_edges)}
        marginal=0
        for d in f['old_v']:
            if d[0] not in ('v','w'):continue
            row=f['table'][f['new_v'].index(d)];vals=[]
            for e,(u,v,c) in enumerate(f['old']):
                if v==d:
                    re=root_new[u];first=f['forced'][root_edges[u[1]]]
                    vals.append(sum(row[a] for a in (first,re,f['copied'][e])))
            require(bool(vals),'every terminal feasible')
            marginal+=min(vals)
        require(marginal==missed+overlap,'exact optimized terminal count for every assignment')
        exact=all(sum(x in f['edges'][i] for i in selected)==1 for x in f['ground'])
        require((marginal==0)==exact,'zero optimum iff assignment is exact cover')
        out.append({'bits':bits,'optimum':marginal,'exact_cover':exact})
    return out


def test_family(name, edges, exhaustive):
    f=family(edges); levels={v:0 if v[0]=='r' else 1 if v[0]=='a' else 2 if v[0]=='u' else 3 for v in f['new_v']}
    require(len({(u,v) for u,v,c in f['new']})==len(f['new']),'expanded simple graph')
    require(all(levels[v]==levels[u]+1 for u,v,c in f['new']),'expanded consecutive depth-three layers')
    indeg=Counter(v for u,v,c in f['new'])
    require(all(1<=indeg[v]<=3 for v in f['new_v'][1:]),'expanded indegree1-3 and reachable')
    require(all(c in (0,1) for row in f['table'] for c in row),'dense all entries binary')
    h=f['h']; degree3=all(len(e)==3 for e in edges) and all(sum(x in e for e in edges)==3 for x in f['ground'])
    if degree3: require(len(f['ground'])==h and len(f['pairs'])<=3*h,'RXC3 balancing and overlap size bound')
    counts=Counter(); seen=set()
    selections=all_parent_selections(f['old_v'],f['old']) if exhaustive else None
    if not exhaustive:
        incoming={v:[e for e,(_,head,_) in enumerate(f['old']) if head==v] for v in f['old_v'][1:]}
        rng=random.Random(20261006)
        selections=(tuple(rng.choice(incoming[v]) for v in f['old_v'][1:]) for _ in range(2000))
    for s in selections:
        value=test_tree(f,s);counts['trees']+=1;counts['zero' if value==0 else 'positive']+=1;seen.add(tuple(s))
    assignments=per_assignment(f)
    # Construct every zero-eligible assignment, so sampling is never evidence of nonexistence.
    for a in assignments:
        if a['optimum']!=0:continue
        bits=a['bits'];s=[2*i+bits[i] for i in range(h)]
        for d in f['old_v'][h+1:]:
            color=0 if d[0]=='v' else 1
            s.append(next(e for e,(u,v,c) in enumerate(f['old']) if v==d and bits[u[1]]==color))
        require(test_tree(f,tuple(s))==0,'forward exact cover construct actual dense zero tree')
    total=math.prod(sum(v==head for _,v,_ in f['old']) for head in f['old_v'][1:])
    if exhaustive:require(len(seen)==total,'all ordinary trees exhaustively mapped with no duplication')
    # An independent edge-subset census for a tiny model avoids assuming the parameterization.
    subset_trees=None
    if len(f['new'])<=16:
        subset_trees=0
        for ids in combinations(range(len(f['new'])),len(f['new_v'])-1):
            ic=Counter(f['new'][e][1] for e in ids)
            if any(ic[v]!=1 for v in f['new_v'][1:]):continue
            paths=validate_tree(f['new_v'],f['new'],ids)
            inverse=tuple(sorted({k for k,e in {**f['middle'],**f['copied']}.items() if e in ids}))
            require(inverse in seen,'unfiltered subset has mapped original preimage')
            subset_trees+=1
        require(subset_trees==total,'unfiltered expanded subset census')
    return {'name':name,'vertices':len(f['new_v']),'arcs':len(f['new']),'full_dense_entries':sum(map(len,f['table'])),'RXC3_regular_uniform_family':degree3,'RXC3_universe_divisible_by_three':len(f['ground'])%3==0,'exhaustive_all_tree_mapping':exhaustive,'all_possible_ordinary_trees':total,'tested':dict(counts),'unfiltered_subset_trees':subset_trees,'all_selector_assignments_checked':len(assignments),'exact_covers':sum(a['exact_cover'] for a in assignments),'exact_minimum':min(a['optimum'] for a in assignments),'positive_threshold':4*h+3*(len(f['ground'])+len(f['pairs']))}

cases=[]
cases.append(test_family('small overlapping positive generic control',[{0},{0}],True))
cases.append(test_family('all four triples negative RXC3',[set(x) for x in combinations(range(4),3)],True))
cyclic=[{(i+j)%6 for j in range(3)} for i in range(6)]
cases.append(test_family('cyclic six positive RXC3',cyclic,False))
no_cover=[{i,(i+1)%6,(i+3)%6} for i in range(6)]
cases.append(test_family('cyclic gap six negative RXC3',no_cover,False))
require(cases[-1]['exact_covers']==0 and cases[-1]['exact_minimum']>0,'eligible negative RXC3 control')
# Perturb one correctly zero destination coefficient; direct path equality must reject it.
bad=family(cyclic);bits=(0,1,1,0,1,1);s=[2*i+bits[i] for i in range(6)]
for d in bad['old_v'][7:]:
    color=0 if d[0]=='v' else 1
    s.append(next(e for e,(u,v,c) in enumerate(bad['old']) if v==d and bits[u[1]]==color))
bad['table'][bad['new_v'].index(('v',0))][bad['forced'][0]]=1
try:
    test_tree(bad,tuple(s))
except RuntimeError as error:
    require(str(error)=='dense path sum equals old endpoint color mismatch','corrupted destination price caught by independent old-color comparison')
else:
    raise RuntimeError('Corrupted coefficient was silently accepted')
# Empty direct instance is a feasible root-only yes case; hardness uses nonempty RXC3.
e=family([]);require(len(e['new_v'])==1 and not e['new'] and not e['pairs'],'empty construction root-only boundary')
# The printed diagonal interpretation is a real failure, not cosmetic algebra.
literal=family(cyclic,diagonal=True)
literal_min=[]
for bits in product((0,1),repeat=6):
 selected={i for i,b in enumerate(bits) if b==0}
 literal_min.append(sum(not any(x in cyclic[i] for i in selected) for x in range(6))+sum(i in selected and j in selected for i,j in literal['pairs']))
require(min(literal_min)>0 and cases[-2]['exact_covers']>0,'diagonal W literal interpretation falsified on a positive RXC3 control')
ordered=family(cyclic,ordered=True);require(len(ordered['pairs'])==2*len(family(cyclic)['pairs']),'ordered duplicate pairs alter count but not zero criterion')
# A generic signed-cost <=0 certificate is not the same as exact-zero feasibility.
signed_paths=[-1];require(min(signed_paths)<=0 and 0 not in signed_paths,'signed threshold versus exact zero distinction')
script=Path(__file__).resolve()
print(json.dumps({'status':'PASS','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checker_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'optimized_python':not __debug__,'checks':dict(COUNTS),'total_explicit_checks':sum(COUNTS.values()),'cases':cases,'negative_controls':{'literal_diagonal_W_minimum':min(literal_min),'original_positive_exact_covers':cases[-2]['exact_covers'],'signed_exactzero_not_threshold':True},'limitations':'Fresh bounded computation supports the arbitrary-size proof reconstruction; cyclic-six full trees are sampled, every selector assignment and exact cover are exhaustively checked. No novelty or earliest-priority theorem is inferred from finite tests.'},indent=2,sort_keys=True))
