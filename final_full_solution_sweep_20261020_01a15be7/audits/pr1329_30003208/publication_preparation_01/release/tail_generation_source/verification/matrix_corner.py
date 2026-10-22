# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Alec Kriebel
"""Exact finite control of the nonselfadjoint 2x2 corner device.
The universal norm argument is in the written proof, not inferred from this case.
"""
from fractions import Fraction as F
import json
checks=0
def need(p,label):
 global checks
 checks+=1
 if not p:raise ValueError(label)
def mul(a,b):return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def tr(a):return [list(x) for x in zip(*a)]
T=[[F(0),F(1)],[F(0),F(0)]]
Y=[[F(0) for j in range(4)] for i in range(4)]
for i in range(2):
 for j in range(2):Y[i][j+2]=T[i][j];Y[i+2][j]=T[j][i]
need(T!=tr(T),'target is nonselfadjoint')
need(Y==tr(Y),'block is selfadjoint')
TT=mul(T,tr(T));TtT=mul(tr(T),T);Y2=mul(Y,Y)
need([r[:2] for r in Y2[:2]]==TT,'upper block TT*')
need([r[2:] for r in Y2[2:]]==TtT,'lower block T*T')
need(mul(Y2,Y)==Y and Y!=[[F(0)]*4 for _ in range(4)],'selfadjoint nonzero Y^3=Y implies norm1')
need(TtT==[[F(0),F(0)],[F(0),F(1)]],'T norm1')
need([r[2:] for r in Y[:2]]==T,'upper-right corner recovers exact target')
rejected=0
for bad,label in [([r[:2] for r in Y[:2]],'wrong corner'),([[x/2 for x in r] for r in T],'wrong half-radius target')]:
 try:need(bad==T,label)
 except ValueError:rejected+=1
 else:raise ValueError('false control accepted')
print(json.dumps({'schema':'tail-generation-matrix-corner-control/v1','checks':checks,'negative_rejections':rejected,'universal_proof_from_finite_controls':False},sort_keys=True,separators=(',',':')))
