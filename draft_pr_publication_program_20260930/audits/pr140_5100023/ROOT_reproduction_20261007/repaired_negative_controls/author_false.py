#!/usr/bin/env python3
"""Exact chord identities; no numerical billiard orbits are used as proof."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from math import gcd
import json
checks=0; chords=0; rotation_cases=0

def ck(p):
 global checks
 if not p:raise RuntimeError("Exact verification check failed")
 checks+=1

def dot(x,y):return sum(a*b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def q(A,B,M):
 r=sub(A,M);s=sub(B,M)
 # q is in absolute coordinates: (Q-M).r=|r|².
 det=r[0]*s[1]-r[1]*s[0]
 ck(det!=0)
 z=((dot(r,r)*s[1]-dot(s,s)*r[1])/det,(r[0]*dot(s,s)-s[0]*dot(r,r))/det)
 Q=tuple(z[j]+M[j] for j in range(2))
 ck(dot(sub(Q,M),r)==dot(r,r));ck(dot(sub(Q,M),s)==dot(s,s))
 return Q

def unit(t):return ((1-t*t)/(1+t*t),2*t/(1+t*t))
ck(False)
print("FALSE CHECK ACCEPTED")
