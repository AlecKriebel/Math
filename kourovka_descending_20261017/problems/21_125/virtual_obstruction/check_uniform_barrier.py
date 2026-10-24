#!/usr/bin/env python3
"""Exact finite sanity checks; the note supplies the unbounded proof."""
from pathlib import Path
from datetime import datetime,timezone
import json
import check_index_obstruction as perm

def delta(v): return tuple(v[j]^v[(j+1)%len(v)] for j in range(len(v)))
def b(v):return tuple(2*j+(bit^v[j]) for j in range(len(v)) for bit in (0,1))
def reduce_word(w):
    out=[]
    for x in w:
        if out and out[-1]==-x:out.pop()
        else:out.append(x)
    return out

def inv_word(w):return [-x for x in reversed(w)]
def theta_q(w,q):
    out=[]
    for x in w:
        image=[2]+[1]*q if abs(x)==2 else [1]
        out.extend(image if x>0 else inv_word(image))
    return reduce_word(out)

results=[]
for m in range(2,66):
    n=1
    while n<m-1:n*=2
    v=(1,)+(0,)*(n-1)
    for _ in range(n-(m-1)):v=delta(v)
    top=v;vectors={m:v}
    for i in range(m-1,0,-1):v=delta(v);vectors[i]=v
    t=tuple(2*((j+1)%n)+bit for j in range(n) for bit in (0,1));ti=perm.inverse(t)
    identity=tuple(range(2*n)); images={i:b(v) for i,v in vectors.items()}
    assert images[1]==identity
    assert images[2]==tuple(x^1 for x in range(2*n))
    for i in range(2,m+1):assert perm.conjugator_step(images[i],t,ti)==images[i-1]
    assert perm.conjugator_step(images[1],t,ti)==identity
    power=identity
    for j in range(n):
        assert perm.derangement(perm.compose(images[2],power));power=perm.compose(power,t)
    assert power==identity
    reached={0};frontier=[0]
    generators=[t,ti,images[m]]
    while frontier:
        x=frontier.pop()
        for g in generators:
            y=g[x]
            if y not in reached:reached.add(y);frontier.append(y)
    assert len(reached)==2*n
    results.append({'rank':m,'N':n,'degree':2*n,'top_flip_vector':list(top),'exact_relators':True,'transitive':True,'entire_centralizer_coset_filter_passes_by_symbolic_lemma':True})

powers=[]
for p in range(1,13):
    for q in range(1,13):
        x=[2]*p;c=reduce_word(inv_word(x)+theta_q(x,q))
        second=reduce_word(inv_word(c)+theta_q(c,q))
        assert bool(second)==(p>=2)
        powers.append({'power_a2':p,'power_t':q,'commutator_length':len(c),'second_engel_length':len(second)})

Path(__file__).with_name('uniform_barrier_checks.json').write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Finite exact sanity checks only; the note proves uniformity for all ranks. Positive powers show why the Engel relation does not survive arbitrary finite-index power replacement.','wreath_models':results,'power_checks':powers},indent=2)+'\n')
print('PASS: 64 transitive models, all displayed relators and full-coset sanity conditions; 144 signed-free-word power checks.')
