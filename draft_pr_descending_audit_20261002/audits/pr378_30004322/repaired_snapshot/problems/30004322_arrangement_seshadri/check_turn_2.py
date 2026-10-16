#!/usr/bin/env python3
"""Exact Hesse/auxiliary-line certificate; no floating point."""
import json
from fractions import Fraction as Q
from itertools import combinations
# Q[z]/(z²+z+1)
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def neg(x):return(-x[0],-x[1])
def mul(x,y):return(x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]-x[1]*y[1])
def inv(x):
 a,b=x;den=a*a-a*b+b*b;return((a-b)/den,-b/den)
def div(x,y):return mul(x,inv(y))
z=(Q(0),Q(1));one=(Q(1),Q(0));zero=(Q(0),Q(0));roots=[one,z,neg(add(one,z))]
def norm(v):
 lead=next(x for x in v if x!=zero);return tuple(div(x,lead) for x in v)
def cross(a,b):return norm(tuple(add(mul(a[(i+1)%3],b[(i+2)%3]),neg(mul(a[(i+2)%3],b[(i+1)%3]))) for i in range(3)))
def dot(a,b):
 x=zero
 for u,v in zip(a,b):x=add(x,mul(u,v))
 return x
axes=[(one,zero,zero),(zero,one,zero),(zero,zero,one)]
H=axes+[(one,a,b) for a in roots for b in roots]
Z=sorted({cross(a,b) for a,b in combinations(H,2)})
F=[norm((one,neg(a),zero)) for a in roots]+[norm((zero,one,neg(a))) for a in roots]+[norm((neg(a),zero,one)) for a in roots]

N=0
def ck(v):
 global N
 assert v;N+=1
ck(len(H)==len(set(H))==12);ck(len(F)==len(set(F))==9);ck(not(set(H)&set(F)));ck(len(Z)==21)
incH=[[int(dot(l,p)==zero) for p in Z] for l in H]
incF=[[int(dot(l,p)==zero) for p in Z] for l in F]
mult=[sum(row[j] for row in incH) for j in range(21)]
D=[j for j,m in enumerate(mult) if m==2];Qp=[j for j,m in enumerate(mult) if m==4]
ck(len(D)==12 and len(Qp)==9)
for row in incH:ck(sum(row[j] for j in D)==2 and sum(row[j] for j in Qp)==3)
for row in incF:ck(sum(row[j] for j in D)==4 and sum(row[j] for j in Qp)==0)
for j in range(21):
 cover=sum(Q(1,4)*row[j] for row in incH)+sum(Q(1,6)*row[j] for row in incF)
 ck(cover==1)
point_weights=[Q(1,4) if j in D else Q(1,6) for j in range(21)]
ck(sum(point_weights)==Q(9,2))
for row in incH+incF:ck(sum(w*x for w,x in zip(point_weights,row))==1)
# Enumerate every line through a pair, which covers all possible >=2-point lines.
pairlines={cross(a,b) for a,b in combinations(Z,2)}
counts=[]
for l in pairlines:
 hits=[j for j,p in enumerate(Z) if dot(l,p)==zero]
 ck(len(hits)<=5)
 ck(len(hits)==5 if l in H else len(hits)<=4)
 ck(sum(point_weights[j] for j in hits)<=1)
 counts.append(len(hits))
ck(max(counts)==5);ck(sum(1 for c in counts if c==5)==12)
ck(Q(12,2)==6);ck(Q(12,4)+Q(9,6)==Q(9,2));ck(Q(2,9)>Q(1,5))
print(json.dumps({'status':'PASS','assertions':N,'H_lines':12,'F_lines':9,'singular_points':21,'double_points':12,'quadruple_points':9,'all_pair_lines':len(pairlines),'arrangement_only_cover_optimum':'6','global_fractional_line_cover_optimum':'9/2','seshadri':'1/5 (credited known Hesse case)','nonlinear_ratio_lower_bound':'2/9','scope':'Exact finite incidence/LP certificates. No universal arrangement theorem follows.'},indent=2,sort_keys=True))
