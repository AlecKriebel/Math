#!/usr/bin/env python3
"""Independent word, nontriviality and metabelian finite controls (not proof)."""
from itertools import permutations, product
from fractions import Fraction
import json

def inv(w): return tuple(-x for x in reversed(w))
def red(w):
    state=[]
    for x in w:
        if state and state[-1]==-x: state.pop()
        else: state.append(x)
    return tuple(state)
def bracket(a,b): return red(a+b+inv(a)+inv(b))
x,y=(1,),(2,)
c=bracket(x,y);d=red(x+c+inv(x));w=bracket(c,d)
letters={1:'x',2:'y',-1:'X',-2:'Y'}
assert ''.join(letters[k] for k in w)=='xyXYxxyXYXyxxYXX'
assert len(w)==16 and all(w[i]!=-w[i+1] for i in range(15))
assert red(w+inv(w))==()

def eval_word(word,x,y,mul,inverse,identity):
    table={1:x,2:y,-1:inverse(x),-2:inverse(y)}
    out=identity
    for k in word:out=mul(out,table[k])
    return out
# Unitriangular 3x3 matrices over F3, represented by (a,b,c):
# [1 a c;0 1 b;0 0 1]. Commutators are central; the group is metabelian.
def hm(g,h):
    a,b,c=g;d,e,f=h
    return ((a+d)%3,(b+e)%3,(c+f+a*e)%3)
def hi(g):
    a,b,c=g;return (-a%3,-b%3,(-c+a*b)%3)
H=list(product(range(3),repeat=3));ids=(0,0,0)
assert all(hm(g,hi(g))==ids==hm(hi(g),g) for g in H)
assert all(eval_word(w,g,h,hm,hi,ids)==ids for g,h in product(H,repeat=2))
noncommuting=sum(hm(g,h)!=hm(h,g) for g,h in product(H,repeat=2))
assert noncommuting>0
# S4 rejects the hypothesis that the evaluator makes every word vanish.
def pm(g,h):return tuple(g[h[i]] for i in range(4))
def pi(g):return tuple(g.index(i) for i in range(4))
S=list(permutations(range(4)));Sidentity=(0,1,2,3)
nonidentity=[(g,h,eval_word(w,g,h,pm,pi,Sidentity)) for g,h in product(S,repeat=2) if eval_word(w,g,h,pm,pi,Sidentity)!=Sidentity]
assert len(nonidentity)==168
triples=((2,3,7),(2,4,5),(3,3,4),(2,3,6),(2,3,5))
chi=[-1+sum((Fraction(1,k) for k in t),Fraction()) for t in triples]
assert chi==[Fraction(-1,42),Fraction(-1,20),Fraction(-1,12),Fraction(),Fraction(1,30)]
print(json.dumps({'status':'PASS','word':' '.join(letters[k] for k in w),'word_length':len(w),'UT3_F3_elements':len(H),'UT3_F3_ordered_pairs':len(H)**2,'UT3_F3_noncommuting_pairs':noncommuting,'UT3_F3_witness_killed':len(H)**2,'S4_ordered_pairs':len(S)**2,'S4_nonidentity_witnesses':len(nonidentity),'S4_first_nonidentity':nonidentity[0],'orbifold_euler_characteristics':list(map(str,chi)),'limits':'Finite controls supplement a free-normal-form and derived-subgroup proof; no topology or priority claim.'},indent=2))
