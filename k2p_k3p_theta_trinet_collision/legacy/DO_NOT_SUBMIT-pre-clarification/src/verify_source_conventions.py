#!/usr/bin/env python3
from fractions import Fraction as F
NAME='ACGT';ADD=[[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]
def k2p(c,g):return [F(1),c,g,c]
def sun(a,b,c,d,e,f,delta,x,y,z):return a[x]*b[y]*c[z]*(delta*d[z]*f[y]+(1-delta)*e[z]*f[ADD[y][z]])
a,b,c,d,e,f=[k2p(F(1,3),F(2,5)),k2p(F(2,7),F(3,7)),k2p(F(1,4),F(5,9)),k2p(F(3,8),F(4,9)),k2p(F(2,9),F(1,2)),k2p(F(5,11),F(3,10))];q=F(2,5)
checks={(0,2,2):b[2]*c[2]*(q*d[2]*f[2]+(1-q)*e[2]),(1,1,0):a[1]*b[1]*f[1],(2,0,2):a[2]*c[2]*(q*d[2]+(1-q)*e[2]*f[2]),(2,2,0):a[2]*b[2]*f[2],(3,1,2):a[1]*b[1]*c[2]*f[1]*(q*d[2]+(1-q)*e[2])}
for t,w in checks.items():assert sun(a,b,c,d,e,f,q,*t)==w
# Reproduce favorable-order Q factorization numerically exactly by identity.
coords={(x,y,z):sun(a,b,c,d,e,f,q,x,y,z) if x^y^z==0 else F(0) for x in range(4) for y in range(4) for z in range(4)}
Q=coords[0,2,2]*coords[2,0,2]*coords[1,1,0]**2-coords[0,0,0]*coords[2,2,0]*coords[3,1,2]**2
positive=(a[2]*b[2]*c[2]**2*d[2]*e[2]*a[1]**2*b[1]**2*f[1]**2*q*(1-q)*(1-f[2])**2)
assert Q==positive and Q>0
print('[source conventions] PASS  A,C,G,T order; C+G=T; K2P a_C=a_T')
print('[source conventions] PASS  five explicit Lemma 4.1 coordinates and favorable-order Q factorization')
