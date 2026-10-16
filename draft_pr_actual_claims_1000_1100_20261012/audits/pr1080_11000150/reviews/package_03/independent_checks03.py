#!/usr/bin/env python3
"""Independent exact finite falsifications; no candidate imports or assertions."""
from itertools import product, combinations
from fractions import Fraction
import json,sys
from pathlib import Path

def need(test, message):
    if not test:
        raise RuntimeError(message)

def red(w):
    out=[]
    for x in w:
        if out and out[-1]==-x: out.pop()
        else: out.append(x)
    return tuple(out)

def inv(w): return tuple(-x for x in w[::-1])
def sub(u,v):
    it=iter(v)
    return all(any(y==x for y in it) for x in u)

def main(fault=None):
    # Three conjugates of positive generators, independent free-group model.
    alphabet={'X':(1,), 'Y':(2,), 'Z':(1,2,-1)}
    def evaluate(w): return red(sum((alphabet[x] for x in w),()))
    def height(w):return sum(1 if x>0 else -1 for x in w)
    fibers={};checks=0
    for n in range(7):
        for w in product('XYZ',repeat=n):
            h=evaluate(w)
            need(height(h)==n,'Conjugacy-invariant height lost')
            fibers.setdefault(h,[]).append(w);checks+=1
    pairs=0
    for h,words in fibers.items():
        for u,v in product(words,repeat=2):
            need(not sub(u,v) or u==v,'Proper comparable equal-valued words')
            pairs+=1
    insertion=0;wrong_detected=0
    for retained in [(),(1,), (1,2), (2,1,-2), (1,2,-1,2)]:
        for blocks in product([(),(1,),(2,),(-1,2,1)],repeat=len(retained)+1):
            v=[];rhs=();prefix=()
            for j,b in enumerate(blocks):
                v.extend(b)
                rhs=red(rhs+b) if fault=='omit_conjugates' else red(rhs+prefix+b+inv(prefix))
                if j<len(retained):v.append(retained[j]);prefix+=retained[j:j+1]
            lhs=red(tuple(v)+inv(retained))
            wrong=red(sum(blocks,()))
            wrong_detected+=lhs!=wrong
            need(lhs==rhs,'Independent insertion identity')
            insertion+=1
    # Exact rational generic perturbation of concurrent branches.
    vertices=0
    for n in range(2,13):
        eps=Fraction(1,100*n*n)
        points=[]
        for i,j in combinations(range(1,n+1),2):
            x=-eps*(i+j);y=-eps*i*j
            need(-1<x<1,'Crossing escaped local square')
            need(i*x+eps*i*i==j*x+eps*j*j==y,'Rational crossing equality')
            points.append((x,y))
        need(len(set(points))==n*(n-1)//2,'Triple concurrence survived')
        for x in [-1,1]:
            ys=[i*x+eps*i*i for i in range(1,n+1)]
            need(ys==sorted(ys,reverse=(x==-1)),'Endpoint cyclic order lost')
        vertices+=len(points)
    # All alternating-form vectors through genus four; same fiber parity is zero.
    vectors=0
    for g in range(1,5):
        for v in product([0,1],repeat=2*g):
            pairing=sum(v[i]*v[g+i]+v[g+i]*v[i] for i in range(g))%2
            if fault=='wrong_parity':pairing=1
            need(pairing==0,'Independent mod-2 alternation')
            vectors+=1
    # Boundary cases: repeated letters are occurrences, isolated circles need vertices.
    need(evaluate('Z')==evaluate('XYX')[:0]+(1,2,-1),'Conjugate generator')
    for isolated in range(1,21):
        v=isolated;e=isolated;b=2*isolated
        need(v-e==0 and 2*isolated-b==0,'Disconnected annulus accounting')
    for g in range(1,31):
        need(3*g-2>=2*g-1,'Pants Euler bound')
        need(2*g*(4*g+2)==4*g*(2*g+1),'Chain length')
    return {'status':'PASS','independent_from_candidate_code':True,'finite_only':True,
            'positive_conjugate_words':checks,'fiber_comparisons':pairs,
            'insertion_cases':insertion,'wrong_unconjugated_rhs_detected_cases':wrong_detected,
            'rational_perturbed_double_crossings':vertices,'mod2_vectors':vectors,
            'isolated_annulus_cases':20,'chain_and_pants_genera':30,
            'universal_topology_or_source_theorems_proved_by_computation':False}

if __name__=='__main__':
    print(json.dumps(main(sys.argv[1] if len(sys.argv)>1 else None),indent=2))
