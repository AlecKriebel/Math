#!/usr/bin/env python3
"""Independent finite checks of even move soundness certificates.
Every even scheme is expanded to elementary ordinary Markov edges and checked,
then repadded. This is distinct from an oracle for link equivalence.
Run: python independent_checks.py > independent_results.json
"""
from dataclasses import dataclass
from collections import Counter
import json

checks=Counter(); coverage=Counter(); ordinary_coverage=Counter()
def test(ok,label):
    assert bool(ok),label
    checks[label]+=1
def c(i): return (('c',i),)
def v(i): return (('v',i),)
def invert(w):
    return tuple((kind,-i if kind=='c' else i) for kind,i in reversed(w))
def shift(w):
    return tuple((kind,(abs(i)+1)*(1 if i>0 else -1)) for kind,i in w)
def in_alphabet(w,k,virtual):
    return all(1<=abs(i)<=k and (kind=='c' or (virtual and kind=='v' and i>0))
               for kind,i in w)
@dataclass(frozen=True)
class State:
    n:int
    word:tuple
def valid(x,virtual):
    return x.n>=1 and in_alphabet(x.word,x.n-1,virtual)
def pad(x):
    return x if x.n%2==0 else State(x.n+1,x.word+c(x.n))
def collapse(seq):
    out=[]
    for x in seq:
        if not out or out[-1]!=x: out.append(x)
    return out

# Count connected components by a layered wiring graph, not by permutation cycles.
def components(x):
    n=x.n; layers=len(x.word)+1; parent=list(range(n*layers))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    def join(i,j):
        a,b=find(i),find(j)
        if a!=b:parent[a]=b
    for level,(_,letter) in enumerate(x.word):
        i=abs(letter)-1
        for j in range(n):
            target=i+1 if j==i else i if j==i+1 else j
            join(level*n+j,(level+1)*n+target)
    for j in range(n): join(j,(layers-1)*n+j)
    return len({find(j) for j in range(n)})

def exchange_words(n,a,b,left):
    aa,bb=(shift(a),shift(b)) if left else (a,b)
    i=1 if left else n-1
    return aa+c(-i)+bb+c(i),aa+v(i)+bb+v(i)

# Verify an ordinary edge, allowing either direction.
def ordinary_edge(x,y,kind,data,virtual):
    test(valid(x,virtual) and valid(y,virtual),'ordinary_endpoints_well_typed')
    if kind=='stab':
        small,big=(x,y) if x.n<y.n else (y,x)
        ok=(big.n==small.n+1 and len(big.word)==len(small.word)+1
            and big.word[:-1]==small.word and abs(big.word[-1][1])==small.n)
        test(ok,'ordinary_stabilization_pattern')
        origin=small.n
    elif kind=='conj':
        a=data
        test(x.n==y.n and in_alphabet(a,x.n-1,virtual),'ordinary_conjugator_support')
        test(y.word==a+x.word+invert(a) or x.word==a+y.word+invert(a)
             or y.word==invert(a)+x.word+a or x.word==invert(a)+y.word+a,
             'ordinary_conjugation_pattern')
        origin=x.n
    else:
        a,b,left=data
        test(x.n==y.n and in_alphabet(a,x.n-2,True) and in_alphabet(b,x.n-2,True),
             'ordinary_exchange_block_support')
        p,q=exchange_words(x.n,a,b,left)
        test((x.word,y.word) in [(p,q),(q,p)],'ordinary_exchange_pattern')
        origin=x.n
    test(components(x)==components(y),'ordinary_edge_wiring_components')
    ordinary_coverage[(kind,'odd' if origin%2 else 'even')]+=1

def samples(k,virtual):
    if k==0:return [()]
    return [(),c(k),c(-1)+(v(k) if virtual else c(k))+c(1)]
def instance(name,N,a,b,g,virtual):
    # Explicit even endpoints, then a separate short ordinary soundness witness.
    if name=='C':
        x=State(N,b);y=State(N,a+b+invert(a))
        route=[x,y];edge=[('conj',a)]
    elif name=='BC':
        x=State(N,b+c(N-1));y=State(N,a+b+invert(a)+c(N-1))
        route=[x,State(N-1,b),State(N-1,a+b+invert(a)),y]
        edge=[('stab',None),('conj',a),('stab',None)]
    elif name=='T':
        x=State(N,b+c(N-1));y=State(N,b+g)
        route=[x,State(N-1,b),y];edge=[('stab',None)]*2
    elif name=='D':
        x=State(N,b);y=State(N+2,b+g+c(N+1))
        route=[x,State(N+1,b+g),y];edge=[('stab',None)]*2
    else:
        buffered=name.startswith('B')
        left=name.endswith('L')
        m=N-1 if buffered else N
        p,q=exchange_words(m,a,b,left)
        if buffered:
            x=State(N,p+c(N-1));y=State(N,q+c(N-1))
            route=[x,State(m,p),State(m,q),y]
            edge=[('stab',None),('left' if left else 'right',(a,b,left)),('stab',None)]
        else:
            x=State(N,p);y=State(N,q)
            route=[x,y];edge=[('left' if left else 'right',(a,b,left))]
    test(x.n%2==y.n%2==0,'even_scheme_endpoints')
    test(valid(x,virtual) and valid(y,virtual),'even_scheme_index_ranges')
    test(components(x)==components(y),'even_scheme_wiring_components')
    for j,(kind,data) in enumerate(edge):
        ordinary_edge(route[j],route[j+1],kind,data,virtual)
        ordinary_edge(route[j+1],route[j],kind,data,virtual)
    padded=[pad(t) for t in route]
    test(all(t.n%2==0 and valid(t,virtual) for t in padded),'padded_witness_all_even')
    test(collapse(padded)==collapse([x,y]),'padded_witness_collapses_to_exact_scheme')
    test(max(t.n for t in padded)==2*((max(t.n for t in route)+1)//2),
         'exact_height_rounding')
    coverage[('virtual_' if virtual else 'classical_')+name]+=1

for virtual in [False,True]:
    for N in [2,4,6,8]:
        names=['C','BC','T','D']+(['R','L']+(['BR','BL'] if N>=4 else []) if virtual else [])
        for name in names:
            k={'C':N-1,'BC':N-2,'T':N-2,'D':N-1,'R':N-2,'L':N-2,'BR':N-3,'BL':N-3}[name]
            if name in ['T','D']:
                i=N-1 if name=='T' else N
                for b in samples(k,virtual):
                    for g in [c(i),c(-i)]+([v(i)] if virtual else []):
                        instance(name,N,(),b,g,virtual)
            else:
                for a in samples(k,virtual):
                    for b in samples(k,virtual):
                        instance(name,N,a,b,(),virtual)

# A missing terminal-tail or incorrect support cutoff must be rejected.
test(not in_alphabet(c(1)+c(1),0,False),'reject_crossing_change_prefix_at_two_strands')
test(not in_alphabet(c(3),2,True),'reject_terminal_generator_inside_BC_block')
test(not in_alphabet(v(2),1,True),'reject_overwide_buffered_exchange_block')
test(not valid(State(4,c(4)),True),'reject_out_of_range_terminal_index')
test(pad(State(1,()))==State(2,c(1)),'one_strand_unknot_padding')
test(components(State(2,()))==2 and components(State(4,()))==4,'empty_words_need_strand_tags')
test(components(State(2,c(1)*3))==components(State(2,c(1)))==1,
     'component_count_does_not_distinguish_two_strand_knots')
test(set(coverage)=={'classical_'+x for x in ['C','BC','T','D']} |
                   {'virtual_'+x for x in ['C','BC','T','D','R','L','BR','BL']},
     'all_twelve_context_families_checked')
test(set(ordinary_coverage)=={(x,y) for x in ['stab','conj','right','left'] for y in ['odd','even']},
     'all_ordinary_edge_types_and_parities_checked')

print(json.dumps({
 'status':'PASS','exact_assertions':sum(checks.values()),
 'even_scheme_instances':sum(coverage.values()),'checks':dict(checks),
 'scheme_coverage':dict(sorted(coverage.items())),
 'ordinary_edge_coverage':{kind+'_'+parity:n for (kind,parity),n in sorted(ordinary_coverage.items())},
 'scope':'Short ordinary soundness certificates for every even pattern, repadding to the exact endpoints, '
         'both directions, parity, tag and support controls. These are finite diagnostics, not link-equivalence '
         'or braid-word-problem oracles. General soundness and completeness are audited in REVIEW.md.'
},indent=2))
