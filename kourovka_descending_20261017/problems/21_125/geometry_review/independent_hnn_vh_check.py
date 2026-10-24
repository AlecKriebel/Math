#!/usr/bin/env python3
"""Independent exact link and recursive Britton checks for the HNN/VH delta.

No author modules or earlier audit checkers imported. Symbols are 1=s,
2=alpha_1,...; rank m is the iterated HNN group G_m, with G_1=Z^2.
The infinite statements rest on the independent proof in the audit.
"""
from collections import deque
from functools import lru_cache
from pathlib import Path
import hashlib
import json


def inverse(word):
    return tuple(-x for x in reversed(word))


def power(letter,n):
    return (letter if n>=0 else -letter,)*abs(n)


def exponents(rank,word):
    # H_1(G_rank;Z) has basis s and alpha_rank. All lower alpha_i map to s.
    return (sum((1 if x>0 else -1) for x in word if abs(x)!=rank+1),
            sum((1 if x>0 else -1) for x in word if abs(x)==rank+1))


@lru_cache(maxsize=None)
def cyclic_exponent(rank,word,which):
    a,b=exponents(rank,word)
    if which=='s':
        if b:return None
        exponent,letter=a,1
    else:
        if a:return None
        exponent,letter=b,rank+1
    return exponent if trivial(rank,word+power(letter,-exponent)) else None


@lru_cache(maxsize=None)
def reduced_top_length(rank,word):
    if rank==1:
        return 0
    top=rank+1
    blocks=[[]]
    stable=[]
    for x in word:
        if abs(x)==top:
            stable.append(1 if x>0 else -1)
            blocks.append([])
        else:
            blocks[-1].append(x)
    while True:
        for j in range(len(stable)-1):
            if stable[j]!=-stable[j+1]:
                continue
            # z^-1 <s> z and z <alpha_(m-1)> z^-1 are the only pinches.
            which='s' if stable[j]<0 else 'top'
            exponent=cyclic_exponent(rank-1,tuple(blocks[j+1]),which)
            if exponent is None:
                continue
            replacement=power(rank if which=='s' else 1,exponent)
            blocks[j:j+3]=[blocks[j]+list(replacement)+blocks[j+2]]
            stable[j:j+2]=[]
            break
        else:
            return len(stable)


@lru_cache(maxsize=None)
def trivial(rank,word):
    if rank==1:
        return exponents(1,word)==(0,0)
    top=rank+1
    blocks=[[]]
    stable=[]
    for x in word:
        if abs(x)==top:
            stable.append(1 if x>0 else -1)
            blocks.append([])
        else:
            blocks[-1].append(x)
    while stable:
        for j in range(len(stable)-1):
            if stable[j]!=-stable[j+1]:continue
            which='s' if stable[j]<0 else 'top'
            exponent=cyclic_exponent(rank-1,tuple(blocks[j+1]),which)
            if exponent is None:continue
            replacement=power(rank if which=='s' else 1,exponent)
            blocks[j:j+3]=[blocks[j]+list(replacement)+blocks[j+2]]
            stable[j:j+2]=[]
            break
        else:
            return False
    return trivial(rank-1,tuple(blocks[0]))


def subgroup_words(rank,length):
    yield ()
    layer=[()]
    for _ in range(length):
        nxt=[]
        for w in layer:
            for i in range(1,rank+1):
                for x in (i,-i):
                    if not w or x!=-w[-1]:nxt.append(w+(x,))
        yield from nxt
        layer=nxt


def image(word):
    result=[]
    for x in word:
        i=abs(x)
        w=(2,) if i==1 else (i+1,1,-(i+1))
        result.extend(w if x>0 else inverse(w))
    return tuple(result)


def link(rank):
    adjacency={x:set() for i in range(1,rank+2) for x in (i,-i)}
    corner_sources={}
    for i in range(1,rank+1):
        alpha=i+1
        prev=1 if i==1 else i
        boundary=(1,alpha,-prev,-alpha)
        for j,x in enumerate(boundary):
            a,b=-boundary[(j-1)%4],x
            assert b not in adjacency[a],('duplicate corner',rank,a,b)
            adjacency[a].add(b);adjacency[b].add(a)
            corner_sources[frozenset((a,b))]=(i,j)
    return adjacency,corner_sources


def bipartite(adjacency):
    colors={}
    for start in adjacency:
        if start in colors:continue
        colors[start]=0;todo=[start]
        for a in todo:
            for b in adjacency[a]:
                if b in colors:
                    if colors[b]==colors[a]:return False
                else:colors[b]=1-colors[a];todo.append(b)
    return True


def main():
    cycle=(3,1,2,-3,-4) # alpha_2+,s+,alpha_1+,alpha_2-,alpha_3-
    links=[]
    for rank in range(1,51):
        adjacency,sources=link(rank)
        if rank>=3:
            assert len(set(cycle))==5
            assert all(cycle[(j+1)%5] in adjacency[a] for j,a in enumerate(cycle))
            assert not bipartite(adjacency)
        else:assert bipartite(adjacency)
        links.append({'rank':rank,'bipartite':bipartite(adjacency)})
    word_cases,base_intersection_cases,s_cyclic_cases=0,0,0
    for rank in range(1,7):
        for w in subgroup_words(rank,4):
            v=image(w)
            assert trivial(rank,v)==(not w)
            word_cases+=1
            assert (cyclic_exponent(rank,v,'s') is not None)==(not w)
            s_cyclic_cases+=1
            if rank>=2:
                assert (reduced_top_length(rank,v)>0)==any(abs(x)==rank for x in w)
                base_intersection_cases+=1
        # Check all original defining relators and both pinch directions.
        assert trivial(rank,(-2,-1,2,1))
        for i in range(2,rank+1):
            assert trivial(rank,(-(i+1),1,i+1,-i))
    out={'status':'PASS','scope':'bounded exact implementation checks, not a replacement for the unbounded proofs',
         'links':links,'link_cycle_symbols':list(cycle),
         'rank3_cycle_corner_sources':[list(link(3)[1][frozenset((a,cycle[(j+1)%5]))]) for j,a in enumerate(cycle)],
         'free_product_word_cases':word_cases,'base_intersection_word_cases':base_intersection_cases,
         'intersection_with_s_word_cases':s_cyclic_cases}
    Path(__file__).with_name('HNN_VH_INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='links'}))


if __name__=='__main__':main()
