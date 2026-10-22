#!/usr/bin/env python3
"""Audit-only independent controls; not a new attempt or a proof search."""
import hashlib, itertools, json, subprocess, sys
from collections import Counter
from pathlib import Path
from sympy import Matrix, QQ, GF, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.matrices.normalforms import smith_normal_form
ROOT=Path(__file__).resolve().parents[1]
MAN=json.loads((ROOT/'AUTHOR_MANIFEST.json').read_text())
assert len(MAN['files'])==10
hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h for f,h in MAN['files'].items()}
assert all(hashes.values())
rerun=json.loads(subprocess.check_output([sys.executable,str(ROOT/'verify_partial_results.py')],text=True))
assert rerun==json.loads((ROOT/'verification.json').read_text())

def closure(facets):
    return {tuple(c) for f in facets for k in range(1,len(f)+1) for c in itertools.combinations(sorted(f),k)}

def boundary_data(facets):
    fs=closure(facets);d=max(map(len,fs))-1
    bases=[[()]]+[[f for f in sorted(fs) if len(f)==k+1] for k in range(d+1)]
    matrices=[]
    for k in range(d+1):
        idx={f:i for i,f in enumerate(bases[k])}
        m=Matrix.zeros(len(bases[k]),len(bases[k+1]))
        for col,s in enumerate(bases[k+1]):
            for j in range(len(s)):
                m[idx[s[:j]+s[j+1:]],col]=(-1)**j
        matrices.append(m)
    for k in range(1,len(matrices)):
        assert matrices[k-1]*matrices[k]==Matrix.zeros(matrices[k-1].rows,matrices[k].cols)
    return bases,matrices

rp=[(0,1,2),(0,1,3),(0,2,4),(0,3,5),(0,4,5),(1,2,5),(1,3,4),(1,4,5),(2,3,4),(2,3,5)]
original=sorted(closure(rp),key=lambda s:(len(s),s)); idx={f:i for i,f in enumerate(original)}
# Every complete chain vertex < edge < triangle, independently of permutation enumeration.
sd=[tuple(sorted((idx[v],idx[e],idx[t]))) for v in original if len(v)==1 for e in original if len(e)==2 and set(v)<set(e) for t in original if len(t)==3 and set(e)<set(t)]
examples={'point':[(0,)],'edge':[(0,1)],'path_three_edges':[(0,1),(1,2),(2,3)],'triangle_simplex':[(0,1,2)],'square_cycle':[(0,1),(1,2),(2,3),(0,3)],'barycentric_six_vertex_complex':sd}
ind={}
for name,facets in examples.items():
    bases,matrices=boundary_data(facets);f=[len(b) for b in bases[1:]];results={}
    for p in (0,2,3,5):
        domain=QQ if p==0 else GF(p)
        ranks=[DomainMatrix.from_Matrix(m).convert_to(domain).rank() for m in matrices]+[0]
        reduced=[f[i]-ranks[i]-ranks[i+1] for i in range(len(f))]
        assert reduced==rerun['bestvina_brady'][name]['fields'][str(p)]['reduced_link_betti']
        results[str(p)]={'boundary_ranks':ranks[:-1],'reduced_betti':reduced}
    assert f==rerun['bestvina_brady'][name]['f_vector']
    ind[name]={'f_vector':f,'fields':results,'boundary_squared_zero':True}
# Explicit flag check through possible missing triangles; no 4-clique can exist
# in a comparability graph with strict chain lengths confined to 1,2,3.
sdfs=closure(sd);edges={frozenset(x) for x in sdfs if len(x)==2};triangles={frozenset(x) for x in sdfs if len(x)==3}
cliques=[frozenset(x) for x in itertools.combinations(range(31),3) if all(frozenset(e) in edges for e in itertools.combinations(x,2))]
assert set(cliques)==triangles
assert not any(all(frozenset(e) in edges for e in itertools.combinations(x,2)) for x in itertools.combinations(range(31),4))
_,rp_boundary=boundary_data(rp)
snf=smith_normal_form(rp_boundary[2],domain=ZZ)
snf_abs=[abs(int(snf[i,i])) for i in range(min(snf.shape)) if snf[i,i]]
assert snf_abs==[1]*9+[2]
# An independent count is the squared l2 norm of the Euler-value histogram.
vectors=list(itertools.product(range(4),repeat=4))
euler=lambda a:sum(a[::2])-sum(a[1::2])
hist=Counter(map(euler,vectors));pair_count=sum(n*n for n in hist.values());assert pair_count==8092
# Verify the cumulative alternating-prefix formula rather than the author's recurrence.
for a in vectors:
 for b in vectors:
    if euler(a)!=euler(b):continue
    delta=[x-y for x,y in zip(a,b)]
    s=[sum((-1)**(i-j)*delta[j] for j in range(i+1)) for i in range(4)]
    assert s[3]==0
    aa=list(a);bb=list(b)
    for i in range(3):
        for j in (i,i+1):
            aa[j]+=max(-s[i],0);bb[j]+=max(s[i],0)
    assert aa==bb
# BS controls use divisibility/exponent-sum formula rather than matrix elimination.
for item in rerun['baumslag_solitar']:
    m,p=item['m'],item['characteristic'];bad=(p!=0 and (m-1)%p==0)
    assert item['betti']==([1,2,1] if bad else [1,1,0])
assert len(rerun['baumslag_solitar'])==35
out={'author_hashes_match':hashes,'author_output_exactly_reproduced':True,'independent_simplicial_checks':ind,'original_d2_smith_nonzero_invariants':snf_abs,'barycentric_flag_check':True,'rank_synchronization_pairs':pair_count,'bs_cases':35,'status':'PASS; audit controls only; problem remains unsolved'}
print(json.dumps(out,indent=2))
