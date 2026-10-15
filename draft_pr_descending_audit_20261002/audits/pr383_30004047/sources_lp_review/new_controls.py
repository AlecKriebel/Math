#!/usr/bin/env python3
"""Independent exact controls. No candidate module is imported or executed here."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, lcm
from pathlib import Path
import hashlib
import json
import random
import subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SNAP = AUDIT / 'snapshot'
HEAD = '967e8e489aa4599f712d5ddcde62e591827f7e38'
counts = dict(exact_lp_instances=0, actual_lp_blowups=0,
              uniform_boundary_instances=0, actual_uniform_graphs=0,
              weighted_rank_two_graphs=0, exact_cover_dual_controls=0)

def lin_solve(rows, rhs):
    n = len(rows)
    a = [[Q(z) for z in row] + [Q(v)] for row, v in zip(rows, rhs)]
    for col in range(n):
        pivot = next((i for i in range(col,n) if a[i][col]), None)
        if pivot is None:
            return None
        a[col],a[pivot] = a[pivot],a[col]
        d = a[col][col]
        a[col] = [z/d for z in a[col]]
        for i in range(n):
            if i != col:
                d = a[i][col]
                a[i] = [u-d*v for u,v in zip(a[i],a[col])]
    return tuple(row[-1] for row in a)

def dot(a,b):
    return sum((u*v for u,v in zip(a,b)),Q(0))

def simplex_extremum(payoffs, minimize=True):
    """Enumerate exact LP vertices, with a simplex and one payoff bound variable.

    minimize: min distribution max rows; otherwise max distribution min rows.
    All equalities and inequality checks use Fraction, not numerical tolerances.
    """
    d = len(payoffs[0])
    eq = [Q(1)]*d + [Q(0)]
    constraints = []
    for j in range(d):
        constraints.append(tuple(Q(-int(i==j)) for i in range(d))+(Q(0),))
    for row in payoffs:
        constraints.append(tuple(Q(v) if minimize else -Q(v) for v in row)
                           +(Q(-1) if minimize else Q(1),))
    best = None
    for inds in combinations(range(len(constraints)),d):
        point = lin_solve([eq]+[constraints[i] for i in inds], [1]+[0]*d)
        if point is None or any(dot(r,point)>0 for r in constraints):
            continue
        if best is None or (point[-1]<best[-1] if minimize else point[-1]>best[-1]):
            best = point
    assert best is not None
    return best

def game(rows):
    primal = simplex_extremum(rows,True)
    transpose = list(map(list,zip(*rows)))
    dual = simplex_extremum(transpose,False)
    assert primal[-1] == dual[-1]
    assert sum(primal[:-1]) == sum(dual[:-1]) == 1
    for j in range(len(primal)-1):
        v = sum(dual[i]*rows[i][j] for i in range(len(rows)))
        assert v>=primal[-1]
        if primal[j]>0:
            assert v==primal[-1]
    for i in range(len(rows)):
        v = dot(rows[i],primal[:-1])
        assert v<=primal[-1]
        if dual[i]>0:
            assert v==primal[-1]
    return primal,dual

def duplicates(weights):
    den = lcm(*(w.denominator for w in weights))
    return [i for i,w in enumerate(weights) for _ in range(int(den*w))]

def actual_weighted_graph(S, T, alpha, beta, gamma, x, y):
    """Construct every vertex clone and every relevant edge as integer indices."""
    aa,bb,cc = map(duplicates,(alpha,beta,gamma))
    assert aa and bb and cc
    AB = [{j for j,b in enumerate(bb) if b in S[a]} for a in aa]
    BC = [{k for k,c in enumerate(cc) if b in T[c]} for b in bb]
    assert all(Q(len(n),len(bb))>=x for n in AB)
    assert all(Q(len(n),len(cc))>=y for n in BC)
    reaches = [{i for i,n in enumerate(AB)
                if any(k in BC[j] for j in n)} for k in range(len(cc))]
    fraction = max(Q(len(n),len(aa)) for n in reaches)
    weighted = max(sum((alpha[a] for a,s in enumerate(S) if s&t),Q(0)) for t in T)
    assert fraction == weighted
    return dict(parts=[len(aa),len(bb),len(cc)], maximum_reach=str(fraction),
                x=str(x), y=str(y))

# Input identity is independently checked against bytes, SHA and Git objects.
manifest = json.loads((AUDIT/'snapshot_manifest.json').read_text())
assert manifest['head']==HEAD and len(manifest['files'])==49
repo = subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=AUDIT,text=True).strip()
identity = []
for row in manifest['files']:
    blob = (SNAP/row['path']).read_bytes()
    git_blob = subprocess.check_output(['git','show',HEAD+':'+row['path']],cwd=repo)
    assert blob==git_blob
    assert len(blob)==row['bytes'] and hashlib.sha256(blob).hexdigest()==row['sha256']
    identity.append(dict(path=row['path'],bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest(),git_byte_exact=True))
actual_names={str(p.relative_to(SNAP)) for p in SNAP.rglob('*') if p.is_file()}
assert actual_names=={r['path'] for r in manifest['files']}
assert sum('/attempts/30004047/' in r['path'] for r in manifest['files'])==48

# A distinct exact LP control uses unequal B weights and explicit ordinary blowups.
# Every 2-by-3 nonempty B-row template, and 24 seeded 3-by-3 templates, are tested.
template_results=[]
cases=[]
for b_rows in product(range(1,8),repeat=2):
    cases.append((tuple(Q(v,3) for v in (1,2)),b_rows,(Q(1,3),Q(1,2),Q(2,3))))
rng=random.Random(202610030223)
seen=set()
while len(seen)<24:
    seen.add(tuple(rng.randrange(1,8) for _ in range(3)))
for b_rows in sorted(seen):
    cases.append((tuple(Q(v,7) for v in (1,2,4)),b_rows,(Q(2,7),Q(1,2),Q(5,7))))
for beta,b_rows,xs in cases:
    T=[{b for b,m in enumerate(b_rows) if m>>c&1} for c in range(3)]
    gamma=[Q(1,3)]*3
    y=min(Q(m.bit_count(),3) for m in b_rows)
    for x in xs:
        S=[{b for b in range(len(beta)) if m>>b&1}
           for m in range(1,1<<len(beta))
           if sum((beta[b] for b in range(len(beta)) if m>>b&1),Q(0))>=x]
        rows=[[int(bool(s&t)) for s in S] for t in T]
        p,q=game(rows)
        graph=actual_weighted_graph(S,T,list(p[:-1]),list(beta),gamma,x,y)
        assert Q(graph['maximum_reach'])==p[-1]
        counts['exact_lp_instances']+=1
        counts['actual_lp_blowups']+=1
        template_results.append(dict(B_weights=list(map(str,beta)),B_C_masks=list(b_rows),
                                     alpha=list(map(str,p[:-1])),dual_q=list(map(str,q[:-1])),
                                     rho=str(p[-1]),ordinary_graph=graph))

# Threshold endpoints and actual graphs use x immediately below, at, and above each
# binomial jump. This includes r=1, k=1, x=1 and strict versus weak boundary cases.
uniform_results=[]
for n in range(1,10):
    for r in range(1,n+1):
        m=comb(n,r)
        jumps=sorted({Q(comb(h,r),m) for h in range(r,n+1)})
        xs=set(jumps)
        for j,v in enumerate(jumps):
            below=jumps[j-1] if j else Q(0)
            xs.add((below+v)/2)
            if v<1:
                xs.add((v+jumps[j+1])/2)
        B=[set(c) for c in combinations(range(n),r)]
        T=[{b for b,s in enumerate(B) if c in s} for c in range(n)]
        for x in sorted(xs):
            need=(x*m).__ceil__()
            h=next(t for t in range(r,n+1) if comb(t,r)>=need)
            A=[set(c) for c in combinations(range(n),h)]
            S=[{b for b,s in enumerate(B) if s<=a} for a in A]
            graph=actual_weighted_graph(S,T,[Q(1,len(A))]*len(A),[Q(1,m)]*m,
                                        [Q(1,n)]*n,x,Q(r,n))
            assert Q(graph['maximum_reach'])==Q(h,n)
            if n<=5:
                for sub in range(1,1<<m):
                    if sub.bit_count()<need:
                        continue
                    u=set().union(*(B[b] for b in range(m) if sub>>b&1))
                    assert len(u)>=h
            for k in range(1,12):
                for y in {Q(r,n),Q(r,2*n)}:
                    if x+k*y>1 and k*x+y>=1:
                        assert Q(h,n)>=Q(1,k)
            counts['uniform_boundary_instances']+=1
            counts['actual_uniform_graphs']+=1
            uniform_results.append(dict(n=n,r=r,x=str(x),h=h,reach=str(Q(h,n))))

# Distinct cover cost / dual certificates are computed over exact rational vertices.
# They include strict cost <3, the equality barrier 3, and several non-witness supports.
cover_results=[]
E=list(combinations(range(5),2))
supports=[[],[(0,1)],[(0,1),(0,2),(0,3),(0,4)],
          [(0,1),(1,2),(2,0),(3,4)],
          [(0,1),(1,2),(2,3),(3,4),(4,0)],
          [(0,1),(1,2),(2,3),(3,4)],E]
for edges in supports:
    types=[{i} for i in range(5)]+[set(e) for e in edges]
    # x*=max_beta min_i d_beta(i)=min_alpha max_S alpha(S).
    rows=[[int(i in s) for i in range(5)] for s in types]
    p,q=game(rows)
    cost=1/p[-1]
    dual_u=[v/p[-1] for v in p[:-1]]
    assert sum(dual_u)==cost and all(sum(dual_u[i] for i in s)<=1 for s in types)
    cover=[v/p[-1] for v in q[:-1]]
    assert sum(cover)==cost
    assert all(sum(cover[j] for j,s in enumerate(types) if i in s)>=1 for i in range(5))
    counts['exact_cover_dual_controls']+=1
    cover_results.append(dict(edges=edges,cost=str(cost),dual_u=list(map(str,dual_u)),
                              primal_cover=list(map(str,cover))))
assert cover_results[3]['cost']==cover_results[4]['cost']=='5/2'
assert cover_results[5]['cost']=='3'

# Weighted examples were not used by the author controls: construct actual clone
# graphs and compute all distinct reaches, rather than checking only formulas.
rank_results=[]
for a,types,b,g in [
    ([Q(v,20) for v in (3,4,5,3,5)], [{0,1},{1,2},{2,0},{3,4}],
     [Q(1,5),Q(1,5),Q(1,5),Q(2,5)], [Q(1,4)]*4),
    ([Q(v,15) for v in (2,3,3,7)], [{0,1},{1,2},{2,0},{3}],
     [Q(1,5),Q(1,5),Q(1,5),Q(2,5)], [Q(1,4)]*4),
    ([Q(v,15) for v in (2,3,4,3,3)], [{0,1},{1,2},{2,3},{3,4},{4,0}],
     [Q(1,5)]*5, [Q(1,5)]*5)]:
    S=[{j for j,s in enumerate(types) if i in s} for i in range(len(a))]
    T=[{j} for j in range(len(types))]
    x=min(sum((b[j] for j in s),Q(0)) for s in S)
    y=min(g)
    graph=actual_weighted_graph(S,T,a,b,g,x,y)
    assert Q(graph['maximum_reach'])<Q(1,2) and x==Q(2,5)
    unions=[[str(sum((a[i] for i in u|v),Q(0))) for v in types] for u in types]
    assert all(Q(unions[i][j])>=Q(1,2) for i in range(len(types)) for j in range(i))
    counts['weighted_rank_two_graphs']+=1
    rank_results.append(dict(A_weights=list(map(str,a)),B_A_types=[sorted(s) for s in types],
                             B_weights=list(map(str,b)),pair_union_weights=unions,
                             ordinary_graph=graph))

out=dict(status='PASS',counts=counts,identity=dict(head=HEAD,files=49,target_files=48,queue_files=1,
                                                  byte_git_sha_verified=identity),
         lp_instances=template_results,uniform_boundary_instances=uniform_results,
         exact_cover_dual_controls=cover_results,weighted_rank_two_graphs=rank_results,
         scope='New exact finite controls and actual finite graphs. No author imports, no universal theorem inferred from finite enumeration.')
(HERE/'NEW_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status='PASS',counts=counts,input_files_verified=49,scope=out['scope']),indent=2))
