"""Exact auxiliary identity in F_2[e]/(e^3); no approximation or proof substitute."""
import json

def add(a,b):
    return a^b

def mul(a,b):
    c=0
    for i in range(3):
        if (b>>i)&1:
            c^=a<<i
    return c&7

def mm(a,b):
    return [[add(mul(a[i][0],b[0][j]),mul(a[i][1],b[1][j])) for j in range(2)] for i in range(2)]

def scale(c,a):
    return [[mul(c,x) for x in r] for r in a]

one,e,e2=1,2,4
M=[[one,e],[one,one]]
Mprime=[[one,e^e2],[one,one]]
C=[[one^e,e],[0,one]]
if mm(Mprime,C)!=scale(one^e,mm(C,M)):
    raise RuntimeError("Projective conjugacy identity failed")
if mm(M,M)!=[[one^e,0],[0,one^e]]:
    raise RuntimeError("Involution identity failed")
print(json.dumps({"ring":"F_2[e]/(e^3)","encoding":"bit i is the coefficient of e^i", "conjugacy_identity":"M_(e+e^2) C = (1+e) C M_e", "conjugacy_verified":True, "involution_verified":True, "both_conjugacy_sides":mm(Mprime,C)},indent=2))
