#!/usr/bin/env python3
"""Independent pre-candidate controls; exact rational weighted cotrees."""
from fractions import Fraction as Q
from itertools import product
import json, random

class Leaf:
    def __init__(self, loop): self.loop = loop
class Node:
    def __init__(self, join, children, weights):
        self.join, self.children, self.weights = join, children, weights
        assert sum(weights) == 1 and min(weights) >= 0

def rec(t):
    if isinstance(t, Leaf): return Q(t.loop), Q(0)
    children = [rec(s) for s in t.children]
    e = sum(w*w*x[0] for w,x in zip(t.weights,children))
    c = sum(w**4*x[1] for w,x in zip(t.weights,children))
    for i in range(len(children)):
        for j in range(i):
            if t.join:
                a,b=t.weights[i],t.weights[j]
                e += 2*a*b
                c += 6*a*a*b*b*(1-children[i][0])*(1-children[j][0])
    return e,c

def flatten(t, mass=Q(1)):
    if isinstance(t,Leaf): return [(mass,t.loop)], [[t.loop]]
    leaves=[]; blocks=[]
    for w,child in zip(t.weights,t.children):
        ll,mm=flatten(child,mass*w); leaves += ll; blocks.append(mm)
    m=[[t.join]*len(leaves) for _ in leaves]
    offset=0
    for block in blocks:
        for i,row in enumerate(block):
            for j,x in enumerate(row): m[offset+i][offset+j]=x
        offset += len(block)
    return leaves,m

def brute(t):
    leaves,m=flatten(t)
    e=sum(leaves[i][0]*leaves[j][0]*m[i][j] for i,j in product(range(len(leaves)),repeat=2))
    c=Q(0)
    for v in product(range(len(leaves)),repeat=4):
        if all(sum(m[v[i]][v[j]] for j in range(4) if j!=i)==2 for i in range(4)):
            c += product_mass([leaves[x][0] for x in v])
    return e,c

def product_mass(vals):
    p=Q(1)
    for x in vals:p*=x
    return p

def random_tree(rng,n):
    if n==1:return Leaf(rng.randrange(2))
    left=rng.randrange(1,n)
    weights=[Q(rng.randrange(0,13),12)]
    weights.append(1-weights[0])
    return Node(rng.randrange(2),[random_tree(rng,left),random_tree(rng,n-left)],weights)

def main():
    rng=random.Random(37430005116)
    checks=0
    for n in range(1,8):
        for _ in range(30):
            tree=random_tree(rng,n)
            assert rec(tree)==brute(tree), (n,rec(tree),brute(tree))
            checks += 1
    endpoints=[]
    for k in range(2,13):
        t=Node(True,[Leaf(0) for _ in range(k)],[Q(1,k)]*k)
        e,c=rec(t)
        assert e==1-Q(1,k) and c==Q(3*(k-1),k**3)
        endpoints.append({'k':k,'edge':str(e),'induced_C4':str(c)})
    sparse=[]
    for a in (Q(0),Q(1,7),Q(1,3),Q(1,2),Q(1)):
        e,c=rec(Node(True,[Leaf(0),Leaf(0)],[a,1-a]))
        assert c==Q(3,2)*e*e
        sparse.append({'a':str(a),'edge':str(e),'induced_C4':str(c)})
    print(json.dumps({'status':'PASS','seed':37430005116,'rational_tuple_formula_checks':checks,'maximum_leaves':7,'zero_weights_and_both_leaf_types':True,'balanced_endpoints':endpoints,'bipartite_equalities':sparse},indent=2))
if __name__=='__main__':main()
