import numpy as np, sympy as sp, itertools
from fractions import Fraction as Fr
G = sp.Matrix([
[5127,-24,1,7,-9,-19,-1810,-1809,-1788,1788,-23,30],
[-24,1670,1,-2,-1190,-1191,8,-8,20,-13,-3,-3],
[1,1,1718,11,-1212,1212,-20,13,-39,-39,2,-2],
[7,-2,11,27,-22,30,3,3,-2,2,-5,6],
[-9,-1190,-1212,-22,1712,-18,3,-2,26,17,3,0],
[-19,-1191,1212,30,-18,1723,2,21,-17,-27,0,5],
[-1810,8,-20,3,3,2,1283,644,628,0,18,0],
[-1809,-8,13,3,-2,21,644,1277,0,-629,0,-16],
[-1788,20,-39,-2,26,-17,628,0,1273,-625,-8,0],
[1788,-13,-39,2,17,-27,0,-629,-625,1269,0,-3],
[-23,-3,2,-5,3,0,18,0,-8,0,25,-1],
[30,-3,-2,6,0,5,0,-16,0,-3,-1,26]])
print("symmetric:", G == G.T, "trace", G.trace(), sp.Rational(G.trace(),600), sp.Rational(289,10)-sp.Rational(7,20))
# leading principal minors
D=[sp.Integer(1)]
for k in range(1,13):
    D.append(G[:k,:k].det())
print("all minors positive:", all(d>0 for d in D))
fl=[sp.floor(sp.Rational(10*D[k],D[k-1])) for k in range(1,13)]
print("floors:", fl)
print("claimed: [51270,16698,17179,269,8,10,4199,5263,242,252,5,11]")
ev = np.linalg.eigvalsh(np.array(G.tolist(),dtype=float))
print("eigs:", ev)

# symbolic word check: words are (alice word tuple, bob word tuple) with reduction of adjacent equal letters
def red(w):
    out=[]
    for c in w:
        if out and out[-1]==c: out.pop()
        else: out.append(c)
    return tuple(out)
words=[((),()),(('a0',),()),(('a1',),()),(('a2',),()),((),('b0',)),((),('b1',)),
       (('a0',),('b0',)),(('a0',),('b1',)),(('a1',),('b0',)),(('a1',),('b1',)),(('a2',),('b0',)),(('a2',),('b1',))]
def dag(w): return (tuple(reversed(w[0])),tuple(reversed(w[1])))
def mul(w1,w2): return (red(w1[0]+w2[0]),red(w1[1]+w2[1]))
poly={}
for i in range(12):
    for j in range(12):
        w=mul(dag(words[i]),words[j])
        poly[w]=poly.get(w,0)+sp.Rational(G[i,j],600)
# target: 289/10 - B02
tgt={}
def add(w,c): tgt[w]=tgt.get(w,0)+c
add(((),()),sp.Rational(289,10)-sp.Rational(7,20))
for (a,b,s) in [('a0','b0',1),('a0','b1',1),('a1','b0',1),('a1','b1',-1)]:
    add(((a,),(b,)),-10*s)
add(((),('b0',)),-sp.Rational(3,20)); add(((),('b1',)),-sp.Rational(1,5)); add((('a2',),()),sp.Rational(1,20))
add((('a2',),('b0',)),-sp.Rational(3,20)); add((('a2',),('b1',)),sp.Rational(1,5))
keys=set(poly)|set(tgt)
bad={k:(poly.get(k,0),tgt.get(k,0)) for k in keys if sp.simplify(poly.get(k,0)-tgt.get(k,0))!=0}
print("mismatching words:", bad)
print("number of distinct words:", len(keys))
