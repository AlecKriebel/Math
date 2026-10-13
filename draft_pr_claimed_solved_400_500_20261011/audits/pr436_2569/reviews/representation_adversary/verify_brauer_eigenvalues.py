#!/usr/bin/env python3
"""Close the explicit eigenvalue receipt for the natural F4 module over F2."""
from itertools import product, permutations
from collections import Counter
import json

def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def fmul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return r
def mm(a,b):return tuple(fmul(a[2*i],b[j])^fmul(a[2*i+1],b[2+j]) for i in range(2) for j in range(2))
def pmul(a,b):
    r=0
    while b:
        if b&1:r^=a
        a<<=1;b>>=1
    return r

def characteristic(columns):
    det=0
    for p in permutations(range(4)):
        term=1
        for i in range(4):term=pmul(term,((columns[p[i]]>>i)&1)^(2 if i==p[i] else 0))
        det^=term
    return det
H=[a for a in product(range(4),repeat=4) if fmul(a[0],a[3])^fmul(a[1],a[2])==1]
counts=Counter()
for a in H:
    v=a;o=1
    while v!=(1,0,0,1):v=mm(v,a);o+=1
    columns=[]
    for j in range(4):
        v=[0,0];v[j//2]=1<<(j%2)
        columns.append((fmul(a[0],v[0])^fmul(a[1],v[1]))|((fmul(a[2],v[0])^fmul(a[3],v[1]))<<2))
    counts[(o,characteristic(columns))]+=1
check(counts==Counter({(1,17):1,(2,17):15,(3,21):20,(5,31):24}),'actual characteristic polynomial mismatch')
print(json.dumps({'status':'PASS','matrices_checked':60,'charpoly_bit_encoding':'bit i is coefficient of X^i',
 'order_charpoly_counts':[{'order':o,'charpoly':p,'count':n} for (o,p),n in sorted(counts.items())],
 'odd_order_Brauer_values':{'1':4,'3':-2,'5':-1},
 'derivation':'order3 charpoly=(X^2+X+1)^2 gives each primitive third root twice; order5 charpoly=Phi5 gives all four primitive fifth roots once'},indent=2))
