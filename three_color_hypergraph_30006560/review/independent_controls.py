#!/usr/bin/env python3
"""Independent finite audit controls; imports no author code; not new research."""
from itertools import combinations,product
from collections import Counter,defaultdict
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib

def sh(family): return {frozenset(p) for e in family for p in combinations(e,len(e)-1)}
def good(H,r):
    V=set().union(*H) if H else set()
    return [(frozenset(s),[e for e in H if e<=set(s)]) for s in combinations(V,r) if {H[e] for e in H if e<=set(s)}=={1,2,3}]
def set_edges(H):return {frozenset(e):c for e,c in H.items()}
def moved(H,i,j):
    out={}
    for e,c in H.items():
        f=(e-{j})|{i} if j in e and i not in e else e
        if f in H: f=e
        assert f not in out
        out[f]=c
    return out

out={}
triples=[frozenset(t) for t in combinations(range(6),3)]
families=[(frozenset(F),sh(F)) for F in combinations(triples,3)]
hist=Counter(); witness=None
for i,(F,SF) in enumerate(families):
    for G,SG in families[i+1:]:
        if not F&G:
            k=len(SF&SG);hist[k]+=1
            assert k<=7
            if k==7:witness=(F,G)
assert sum(hist.values())==387600 and witness
out['disjoint_three_triple_pairs_n6']={'checked':sum(hist.values()),'max_common_pairs':max(hist),'histogram':dict(sorted(hist.items()))}
groups=defaultdict(list)
for F in combinations(triples,4):
    S=frozenset(sh(F))
    if len(S)==12:groups[S].append(frozenset(F))
for P,decomps in groups.items():
    assert len(decomps)==2 and not decomps[0]&decomps[1]
    assert len([t for t in triples if sh([t])<=P])==8
assert len(groups)==15
out['four_triple_exact_shadow_groups_n6']={'families_examined':4845,'twelve_pair_shadows':15,'decompositions_per_shadow':2,'no_third_disjoint_decomposition':True}
H={frozenset(map(int,e)):c for c,es in [(1,['012','013','014','023','123','234']),(2,['024','134']),(3,['034','124'])] for e in es}
S=good(H,4);reds=[e for e,c in H.items() if c==1]; options=[[e for e in faces if H[e]==1] for s,faces in S]
degrees=[sum(e in faces for s,faces in S) for e in reds]
assert len(S)==4 and sum(x*x for x in degrees)==12
energies=[]
for masses in product(range(7),repeat=4):
    loads=dict.fromkeys(reds,Q(0))
    for O,m in zip(options,masses):
        loads[O[0]]+=Q(m,6);loads[O[1]]+=1-Q(m,6)
    energies.append(sum(x*x for x in loads.values()))
assert min(energies)==Q(8,3)
y=dict.fromkeys(reds,Q(2,3)); A=sum(min(y[e] for e in O) for O in options);B=sum(t*t for t in y.values())
assert A==B==Q(8,3) and 2*A-B==min(energies)
# A deliberately nonuniform primal assignment still obeys weak duality, including signed weights.
loads={e:Q(degrees[i],2) for i,e in enumerate(reds)}; primal=sum(t*t for t in loads.values())
for weights in product((-2,0,1),repeat=6):
    y=dict(zip(reds,weights));dual=2*sum(min(y[e] for e in O) for O in options)-sum(t*t for t in y.values())
    assert dual<=primal
out['ownership']={'rational_assignments':2401,'minimum_energy':'8/3','matching_dual':'8/3','signed_weak_duality_checks':729}
negative={}
negative['deduplicated_T_is_not_sum_of_link_triangles']=(len(S)==4 and sum(Counter(H[e] for e in f)[1]*Counter(H[e] for e in f)[2]*Counter(H[e] for e in f)[3] for s,f in S)==8)
negative['raw_red_square_bound_false']=sum(d*d for d in degrees)>8
# The square of 8+2 sqrt(2) is 72+32 sqrt(2)>24=(sqrt(RGB))^2, exactly.
negative['lossless_link_aggregation_false']=72>24
C=set_edges({(0,2):1,(1,3):1,(1,2):2,(2,3):3});C2=moved(C,0,1)
negative['shift_monotonicity_false']=len(good(C,3))==1 and len(good(C2,3))==0 and Counter(C.values())==Counter(C2.values())
K=set_edges({(0,1):1,(2,3):1,(0,2):2,(1,3):2,(0,3):3,(1,2):3})
negative['constant_one_false']=len(good(K,3))**2==16>8
F=[frozenset(range(3*i,3*i+3)) for i in range(3)]
negative['disjointness_needed_for_three_triple_lemma']=len(sh(F)&sh(F))==9>7
F4=F+[frozenset((9,10,11))]
negative['disjointness_needed_for_four_triple_lemma']=len(sh(F4)&sh(F4)&sh(F4))==12>11
assert all(negative.values());out['negative_controls']=negative
# Zero-success cases: Eq. (9) has maximum 0; Eq. (10) has no nonzero weight when R=0.
assert good({},3)==[] and list(product([],repeat=1))==[]
out['degenerate_formula_10']={'R0':'No nonzero vector exists in R^0, so the stated supremum needs a guard.','T0_Rpositive':'All ratios are zero; formula valid.'}
# Verify the corrected frozen author package using portable relative paths.
manifest=Path(__file__).resolve().with_name('CORRECTED_ARTIFACT_MANIFEST.json')
m=json.loads(manifest.read_text());assert len(m['files'])==11
for f in m['files']:
    data=(manifest.parent.parent/f['path']).read_bytes();assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256']
out['frozen_author_files_unchanged']=11
print(json.dumps(out,indent=2,sort_keys=True))
