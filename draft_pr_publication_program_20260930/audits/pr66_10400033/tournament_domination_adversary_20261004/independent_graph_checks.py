#!/usr/bin/env python3
"""Independent endpoint-word and bitset implementation; no author-code import."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
import hashlib, json, pathlib

HERE=pathlib.Path(__file__).resolve().parent
checks=Counter()
def require(value, category, context=None):
    if not value:
        raise AssertionError((category,context))
    checks[category]+=1

def matching_words(n):
    # First occurrences receive labels in order, so each perfect matching occurs once.
    def walk(prefix, opened, introduced):
        if len(prefix)==2*n:
            yield prefix
            return
        if introduced<n:
            yield from walk(prefix+(introduced,),opened+(introduced,),introduced+1)
        for label in opened:
            yield from walk(prefix+(label,),tuple(x for x in opened if x!=label),introduced)
    yield from walk((),(),0)

def events(word, bits):
    seen=set(); ans=[]
    for label in word:
        first=label not in seen
        tail=first != bool((bits>>label)&1)
        ans.append((label,tail))
        seen.add(label)
    return tuple(ans)

def necklace(sequence):
    # Rotation-normalized event strings with letters renamed by first appearance.
    variants=[]
    for shift in range(len(sequence)):
        rotated=sequence[shift:]+sequence[:shift]
        names={}; encoded=[]
        for letter,tail in rotated:
            if letter not in names:names[letter]=len(names)
            encoded.append(2*names[letter]+int(tail))
        variants.append(tuple(encoded))
    return min(variants)

P_events=((0,False),(1,False),(2,True),(0,True),(2,False),(1,True))
T_events=((0,False),(1,True),(2,False),(0,True),(1,False),(2,True))
P=necklace(P_events); T=necklace(T_events)

def oriented_edges(sequence,n):
    out=[0]*n
    for i,j in combinations(range(n),2):
        pair=[event for event in sequence if event[0] in (i,j)]
        k=pair.index((i,True))
        pair=pair[k:]+pair[:k]
        if pair[2]!=(i,False):continue
        if pair[1]==(j,True):out[i]|=1<<j
        else:out[j]|=1<<i
    return out

def cycle(out,triple):
    a,b,c=triple
    return ((out[a]>>b)&1 and (out[b]>>c)&1 and (out[c]>>a)&1) or \
           ((out[a]>>c)&1 and (out[c]>>b)&1 and (out[b]>>a)&1)

def local_cyclic_fraction(out,triple):
    missing=[(i,j) for i,j in combinations(triple,2)
             if not (((out[i]>>j)&1) or ((out[j]>>i)&1))]
    cyclic=0
    for mask in range(1<<len(missing)):
        completion=out.copy()
        for k,(i,j) in enumerate(missing):
            if (mask>>k)&1:completion[i]|=1<<j
            else:completion[j]|=1<<i
        cyclic+=bool(cycle(completion,triple))
    return Fraction(cyclic,1<<len(missing))

def maximum(n):
    return Fraction(n*(n*n-1),24) if n%2 else Fraction(n*(n*n-4),24)

diagrams=Counter(); local_types=Counter(); sign_assignments=Counter()
for n in range(6):
    triples=list(combinations(range(n),3))
    pairs=list(combinations(range(n),2))
    for word in matching_words(n):
        base=oriented_edges(events(word,0),n)
        for bits in range(1<<n):
            seq=events(word,bits); out=oriented_edges(seq,n)
            # A single arrow reversal switches exactly its incident directed edges.
            switched=[0]*n
            for i,j in pairs:
                if not (((base[i]>>j)&1) or ((base[j]>>i)&1)):continue
                i_to_j=bool((base[i]>>j)&1) != bool(((bits>>i)^(bits>>j))&1)
                if i_to_j:switched[i]|=1<<j
                else:switched[j]|=1<<i
            require(switched==out,'four_endpoint_orientation_and_switching')
            if n and n<=4:
                require(oriented_edges(seq[1:]+seq[:1],n)==out,'rotation_invariance')
                backwards=oriented_edges(tuple(reversed(seq)),n)
                require(all(backwards[i]==sum(1<<j for j in range(n) if (out[j]>>i)&1)
                            for i in range(n)),'circle_reversal_reverses_edges')
            coefficients=[]; unsigned=Fraction(0); expected=Fraction(0)
            for triple in triples:
                selected=tuple(e for e in seq if e[0] in triple)
                kind=necklace(selected)
                coefficient=Fraction(1,2) if kind==P else Fraction(1) if kind==T else Fraction(0)
                probability=local_cyclic_fraction(out,triple)
                require(coefficient<=probability,'per_subset_domination')
                if kind==P:require(probability==Fraction(1,2),'P_exact_probability')
                if kind==T:require(probability==1,'T_exact_probability')
                coefficients.append((triple,coefficient))
                unsigned+=coefficient;expected+=probability
                if n==3:
                    edge_count=sum((out[i]>>j)&1 for i in triple for j in triple)
                    local_types[(edge_count,str(coefficient),str(probability))]+=1
            require(unsigned<=expected<=maximum(n),'unsigned_expectation_and_extremal_bound')
            for signs in range(1<<n):
                signed=sum(((-1)**sum((signs>>j)&1 for j in triple))*coefficient
                           for triple,coefficient in coefficients)
                require(abs(signed)<=unsigned,'every_sign_assignment')
                sign_assignments[n]+=1
            diagrams[n]+=1

tournaments=Counter(); extrema={};degree_sequences={}
for n in range(7):
    pairs=list(combinations(range(n),2)); triples=list(combinations(range(n),3))
    highest=-1;degree_sequences[n]=set()
    for bits in range(1<<len(pairs)):
        out=[0]*n
        for k,(i,j) in enumerate(pairs):
            if (bits>>k)&1:out[i]|=1<<j
            else:out[j]|=1<<i
        C=sum(bool(cycle(out,t)) for t in triples)
        degree=[x.bit_count() for x in out]
        transitive=sum(d*(d-1)//2 for d in degree)
        require(C==n*(n-1)*(n-2)//6-transitive,'unique_source_identity')
        mean=Fraction(n-1,2)
        variance=sum((d-mean)**2 for d in degree)
        require(Fraction(C)==Fraction(n*(n*n-1),24)-variance/2,'exact_variance_identity')
        require(C<=maximum(n),'integer_tournament_bound')
        highest=max(highest,C)
        if C==maximum(n):degree_sequences[n].add(tuple(sorted(degree)))
        tournaments[n]+=1
    extrema[n]=highest
    require(highest==maximum(n),'finite_extremum_attained')

# Explicit all-n attainment mechanism: regular cyclic tournament, delete vertex for even n.
attainments=[]
for n in range(101):
    odd=n if n%2 else n+1
    half=(odd-1)//2
    out=[sum(1<<j for j in range(n) if i!=j and 0<(j-i)%odd<=half) for i in range(n)]
    degrees=[x.bit_count() for x in out]
    C=n*(n-1)*(n-2)//6-sum(d*(d-1)//2 for d in degrees)
    require(C==maximum(n),'regular_or_vertex_deleted_construction')
    attainments.append({'n':n,'cycles':C,'degree_counts':dict(Counter(degrees))})

result={'status':'PASS','implementation':'endpoint-event necklaces and adjacency bitsets; no author import',
        'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        'patterns':{'P':P,'T':T},'oriented_diagrams_by_n':dict(diagrams),
        'sign_assignments_by_n':dict(sign_assignments),'tournaments_by_n':dict(tournaments),
        'finite_extrema':extrema,'extremal_degree_sequences':{k:sorted(v) for k,v in degree_sequences.items()},
        'three_arrow_local_histogram':[{'edges':k[0],'coefficient':k[1],'probability':k[2],'count':v}
                                       for k,v in sorted(local_types.items())],
        'construction_checks_0_through_100':attainments,'assertions':dict(checks),
        'total_assertions':sum(checks.values()),
        'limitation':'Exact finite diagnostics do not prove the imported v3 identity or replace the universal graph argument.'}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='construction_checks_0_through_100'},indent=2))
