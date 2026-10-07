#!/usr/bin/env python3
"""Independent model: abstract D8 pairs plus SymPy ambient group generation.
Never imports or executes the author's fusion-check implementation.
"""
from itertools import product
from pathlib import Path
import json
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup
import sympy

def need(ok, message):
    if not ok: raise RuntimeError(message)

P=Path(__file__).resolve().parent.parent/'packet'
labels=[(a,b) for b in range(2) for a in range(4)]
def mult(x,y):
    a,b=labels[x]; c,d=labels[y]
    return labels.index(((a+(-1)**b*c)%4,(b+d)%2))
def pw(x,n):
    a=0
    for _ in range(n): a=mult(a,x)
    return a
def generated(gens):
    out={0}; todo=[0]
    while todo:
        x=todo.pop()
        for g in gens:
            y=mult(x,g)
            if y not in out:out.add(y);todo.append(y)
    return frozenset(out)
subgroups={frozenset({0})}
while True:
    bigger=subgroups|{generated(set(A)|{g}) for A in subgroups for g in range(8)}
    if bigger==subgroups:break
    subgroups=bigger
subs=sorted(map(lambda x:tuple(sorted(x)),subgroups),key=lambda x:(len(x),x))
need(len(subs)==10,'subgroup inventory')
r=Permutation([1,2,3,0,5,4]);s=Permutation([2,1,0,3,5,4])
# SymPy multiplies permutations left to right, hence s^b*r^a.
embedded=[s**b*r**a for a,b in labels]
need(all(embedded[mult(i,j)]==embedded[j]*embedded[i] for i,j in product(range(8),repeat=2)),'abstract embedding')

def parity_embed(g):
    return Permutation([g(i) for i in range(4)]+([4,5] if g.is_even else [5,4]))
groups={
    'D8':list(PermutationGroup(r,s).generate_schreier_sims()),
    'S4':[parity_embed(g) for g in SymmetricGroup(4).generate_schreier_sims()],
    'A6':list(AlternatingGroup(6).generate_schreier_sims()),
}
need([len(groups[k]) for k in groups]==[8,24,360],'group orders')
need(all(embedded[i] in groups[g] for g in groups for i in range(8)),'Sylow inclusions')
embedding_index={x:i for i,x in enumerate(embedded)}
# Partial conjugation functions, then fully enumerated subgroup morphisms.
conj={g:[tuple(embedding_index.get(h**-1*x*h,-1) for x in embedded) for h in ambient] for g,ambient in groups.items()}
morph={g:{A:{tuple(c[x] for x in A) for c in conj[g] if all(c[x]>=0 for x in A)} for A in subs} for g in groups}
# A homomorphism is determined by generators; all 64 assignments are tested by
# all 64 multiplication equations, without presentation-relation filtering.
homs=[]
for u,v in product(range(8),repeat=2):
    f=tuple(mult(pw(u,a),pw(v,b)) for a,b in labels)
    if all(f[mult(i,j)]==mult(f[i],f[j]) for i,j in product(range(8),repeat=2)):homs.append(f)
need(len(homs)==len(set(homs))==36,'endomorphism inventory')

def preserves(f,source,target):
    for A in subs:
        B=tuple(sorted({f[x] for x in A}))
        for alpha in morph[source][A]:
            values={}
            for x,y in zip(A,alpha):
                if f[x] in values and values[f[x]]!=f[y]:return False
                values[f[x]]=f[y]
            induced=tuple(values[y] for y in B)
            if induced not in morph[target][B]:return False
    return True
passing={a+'->'+b:[f for f in homs if preserves(f,a,b)] for a,b in product(groups,repeat=2)}
frozen=json.loads((P/'FUSION_CHECKS.json').read_text())
for k,fs in passing.items():need(sorted(fs)==sorted(map(tuple,frozen['fusion_preserving'][k]['maps'])),'complete map list '+k)
for g in groups:
    counts={','.join(map(str,A)):len(morph[g][A]) for A in subs}
    need(counts==frozen['fusion_map_counts'][g],'morphism table counts '+g)
    strong=[list(A) for A in subs if all(set(alpha)<=set(A) for Q in subs if set(Q)<=set(A) for alpha in morph[g][Q])]
    need(strong==frozen['strongly_closed'][g],'strong closure '+g)
    gens=[]
    for A in subs:
        for alpha in morph[g][A]:
            if set(alpha)!=set(A):continue
            perm=Permutation([A.index(y) for y in alpha])
            if perm.order()%2==1:
                for x,y in zip(A,alpha):
                    inverse=next(z for z in range(8) if mult(x,z)==0)
                    gens.append(mult(inverse,y))
    need(sorted(generated(gens))==frozen['hyperfocal'][g],'hyperfocal '+g)
need([len(passing[a+'->'+b]) for a,b in product(groups,repeat=2)]==[36,36,36,6,10,14,1,1,9],'nine expected counts')
result={
 'status':'PASS','implementation':'abstract semidirect-product D8; SymPy Schreier-Sims ambient groups; induced subgroup-map lookup',
 'sympy_version':sympy.__version__,
 'all_author_map_lists_match':True,'all_author_morphism_counts_match':True,
 'all_author_strongly_closed_inventories_match':True,'all_author_hyperfocal_subgroups_match':True,
 'group_orders':{g:len(groups[g]) for g in groups},
 'fusion_preserving_counts':{k:len(v) for k,v in passing.items()},
 'all_fusion_morphisms':{g:{','.join(map(str,A)):[list(m) for m in sorted(morph[g][A])] for A in subs} for g in groups},
 'passing_maps':{k:[list(f) for f in v] for k,v in passing.items()},
}
print(json.dumps(result,indent=2,sort_keys=True))
