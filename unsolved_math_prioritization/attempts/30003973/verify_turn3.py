#!/usr/bin/env python3
"""Exact finite certificate; independent of the discovery optimizer."""
from pathlib import Path
import json,itertools
c=json.loads((Path(__file__).parent/'TURN_3_CERTIFICATE.json').read_text())
m=c['ground_set_size'];U=(1<<m)-1;count={}
def ck(x,k):
    assert x,k
    count[k]=count.get(k,0)+1

def fam(facets):return {s for s in range(1<<m) if any(s&t==s for t in facets)}
def product(F,G):return {a|b for a in F for b in G}
def facets(F):return sorted(s for s in F if not any(s!=t and s&t==s for t in F))
def nonfaces(F):return [s for s in range(1<<m) if s not in F and all((s^(1<<i)) in F for i in range(m) if s>>i&1)]
A=fam(c['A_facets']);B=fam(c['B_facets']);D=fam(c['common_square_facets'])
for F,fs in [(A,c['A_facets']),(B,c['B_facets']),(D,c['common_square_facets'])]:
    ck(facets(F)==fs,'facet_lists_exact')
    for s in F:
        for t in range(1<<m):
            if s&t==t:ck(t in F,'downward_closure')
for F in [A,B]:
    for i in range(m):ck(1<<i in F,'all_singletons')
for fs in [c['A_facets'],c['B_facets']]:
    for a in fs:
        for b in fs:ck(a|b in D,'square_upper_bound_pair')
for r in c['facet_witnesses']:
    for key,fs in [('A_pair',c['A_facets']),('B_pair',c['B_facets'])]:
        a,b=r[key];ck(a in fs and b in fs and a|b==r['square_facet'],'square_lower_bound_witness')
ck(product(A,A)==D,'direct_A_square')
ck(product(B,B)==D,'direct_B_square')
for a in A:
    for b in A:
        for d in A:ck(a|b|d in product(A,D),'A_triple_consistency')
for a in c['B_facets']:
    for b in c['B_facets']:
        for d in c['B_facets']:ck((a|b|d)!=U,'B_no_three_cover')
Ac=product(A,D);Bc=product(B,D)
ck(Ac==set(range(1<<m)),'A_cube_full')
ck(Bc==set(range(U)),'B_cube_all_proper_sets')
ck(facets(Bc)==c['B_cube_facets'],'B_cube_facets')
ck(set(c['A_three_cover'])<=A and c['A_three_cover'][0]|c['A_three_cover'][1]|c['A_three_cover'][2]==U,'A_cover_witness')
r=0
for s in c['B_four_cover']:ck(s in B,'B_four_cover_member');r|=s
ck(r==U,'B_four_cover_union')
ck(nonfaces(A)==c['A_minimal_nonfaces'],'A_minimal_nonfaces')
ck(nonfaces(B)==c['B_minimal_nonfaces'],'B_minimal_nonfaces')
for F,pair,triple in [(A,17,11),(B,9,7)]:
    ck(pair in nonfaces(F) and pair.bit_count()==2,'forbidden_pair')
    ck(triple in nonfaces(F) and triple.bit_count()==3,'forbidden_triple')
# Direct combinatorial explanation of the obstruction for B.
ck([s for s in c['B_facets'] if s.bit_count()==3]==[14,69],'only_two_B_triples')
ck((U^(14|69))==48 and 48 not in B,'two_triples_leave_forbidden_pair')
for triple,isolated in [(14,5),(69,4)]:
    comp=U^triple
    for other in range(m):
        if other!=isolated and comp>>other&1:ck((1<<other)|(1<<isolated) not in B,'complementary_isolated_point')
print(json.dumps({'problem_id':30003973,'status':'PASS','assertions':sum(count.values()),'counts':count,'family_sizes':{'A':len(A),'B':len(B),'square':len(D),'A_cube':len(Ac),'B_cube':len(Bc)},'covering_numbers':{'A':3,'B':4},'cube_difference':[U],'arithmetic':'Exact integers and sets; no optimization dependency','scope':'An abstract downward-family counterexample only. Mixed-size minimal nonfaces exclude direct single-graph avoidance realization. No answer to the original universal Ramsey-equivalence question.'},indent=2,sort_keys=True))
