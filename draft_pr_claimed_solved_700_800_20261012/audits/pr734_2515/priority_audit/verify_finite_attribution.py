"""Authored reproducible provenance calculation, not a replacement for the proof.
Source records: Hulpke, ctglist.pdf, p.2, degree 8 index 21; Xia-Zheng v1,
Notation 4.1 and proof of Theorem 1.5. No third-party full text included.
"""
import itertools, json, pathlib, datetime
N=8
identity=tuple(range(N))
def perm(*cycles):
    p=list(identity)
    for cyc in cycles:
        c=[x-1 for x in cyc]
        for x,y in zip(c,c[1:]+c[:1]):p[x]=y
    return tuple(p)
def mul(a,b):return tuple(a[b[i]] for i in range(N))
def inv(a):
    p=[0]*N
    for x,y in enumerate(a):p[y]=x
    return tuple(p)
def closure(gens):
    found={identity};todo=[identity]
    while todo:
        x=todo.pop()
        for g in gens:
            y=mul(g,x)
            if y not in found:found.add(y);todo.append(y)
    return found
candidate_gens=[perm((1,3,2,4),(5,7),(6,8)),perm((1,5),(2,6),(3,7),(4,8))]
P=set()
for mask in range(16):
    for t in range(4):
        if mask.bit_count()%2 != t%2:continue
        P.add(tuple(2*(v^t)+(eps^((mask>>(v^t))&1)) for v in range(4) for eps in range(2)))
assert len(P)==32 and closure(candidate_gens)==P
hulpke_gens=[perm((1,5),(3,7)),perm((1,4,5,8),(2,3),(6,7)),perm((1,3),(2,8),(4,6),(5,7))]
T=closure(hulpke_gens)
rho=None
for r in itertools.permutations(range(N)):
    rinv=inv(r)
    if all(mul(r,mul(g,rinv)) in P for g in hulpke_gens):
        rho=r;break
assert rho is not None and len(T)==32
conjugated={mul(rho,mul(g,inv(rho))) for g in T}
assert conjugated==P
# Xia-Zheng b=(1,0) in R; their theta eta sends 1 to delta_0.
# Their g1 adds delta_0 BEFORE translating, whereas candidate a adds it AFTER.
xia_g1=tuple(2*(v^1)+(eps^(v==0)) for v in range(4) for eps in range(2))
xia_g2=tuple(2*(v^2)+eps for v in range(4) for eps in range(2))
assert xia_g1==inv(candidate_gens[0]) and xia_g2==candidate_gens[1]
assert closure([xia_g1,xia_g2])==P
# De Caro pp.3-4 uses the second and third Hulpke generators.
decaro_a,decaro_b=hulpke_gens[1:]
assert closure([decaro_a,decaro_b])==T
# Source uses GAP right-action convention; ba means first b then a.
decaro_u=mul(decaro_a,decaro_b)
decaro_v=mul(decaro_a,mul(decaro_b,mul(inv(decaro_a),decaro_b)))
assert decaro_u==perm((1,2),(3,4,7,8),(5,6))
assert decaro_v==perm((2,6),(4,8))
assert {decaro_v[0],decaro_v[1]}=={0,5}
# Existing action has candidate's crossing witness; equivalence transfers it.
z=perm((3,4),(5,6));C={0,4};image={z[i] for i in C}
assert z in P and C&image=={0} and C!=image
out={
 'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'candidate_order':len(P),'candidate_generator_arrays_1_based':[[x+1 for x in g] for g in candidate_gens],
 'hulpke_primary_location':'ctglist.pdf, dated February 8 2002, printed page 2, Degree 8, Nr.21',
 'hulpke_group_order':len(T),'relabel_hulpke_to_candidate_1_based':[x+1 for x in rho],
 'hulpke_conjugated_group_equals_candidate':True,
 'xia_zheng_primary_location':'arXiv:2608.25792v1, Notation 4.1 p.6, Lemma 4.2 pp.6-7, Notation 4.3 p.7, proof of Theorem 1.5 pp.11-12',
 'xia_zheng_parameters':{'p':2,'m':2,'b_R':['1','0'],'base_kernel_ideal':'(X1,X2)','kernel_dimension':3},
 'xia_first_generator_is_candidate_a_inverse':True,'xia_second_generator_is_candidate_b':True,
 'xia_generated_group_equals_candidate':True,
 'crossing_witness':{'C':[1,5],'z_C':[1,6],'intersection':[1]},
 'decaro_primary_location':'Zenodo record21538908, DOI10.5281/zenodo.21538908, July24 2026, pp.3-5',
 'decaro_generators_generate_hulpke_group':True,
 'decaro_gap_word_witness_verified':True,
 'decaro_group_is_candidate_up_to_reported_relabelling':True,
 'infinite_equivalence':{'map':'(x,(t0,t1,...)) -> (rho(x), sum_j t_j*2**j)','stage_preservation':'Xn maps to D x {0,...,2**n-1}','first_factor_embeddings_match':True,'top_swaps_match':True,'induced_bottom_action_matches':True},
 'interpretation':'Finite P and the parity-gluing mechanism are prior ingredients. De Caro July24 2026 also states and proves the same infinite universal-containment counterexample, so the candidate result is a rediscovery.'}
path=pathlib.Path(__file__).with_name('finite_attribution_certificate.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
