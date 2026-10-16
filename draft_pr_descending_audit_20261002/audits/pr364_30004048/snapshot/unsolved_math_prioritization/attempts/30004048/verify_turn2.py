#!/usr/bin/env python3
"""Exact fixed-pattern primal/dual and ordinary blow-up checks; no global asymmetry claim."""
from fractions import Fraction as F
from pathlib import Path
import json
checks=0
def ok(x):
 global checks
 assert x
 checks+=1
def tr(M):return list(map(list,zip(*M)))
def mv(M,v):return [sum(F(a)*b for a,b in zip(row,v)) for row in M]
pth=Path(__file__).with_name('TURN_2_CERTIFICATE.json');d=json.loads(pth.read_text())
P,Q,R=d['P'],d['Q'],d['R'];PT,QT,RT=tr(P),tr(Q),tr(R)
ok(R==[[int(any(P[i][j]*Q[j][k] for j in range(4))) for k in range(3)] for i in range(2)])
p=list(map(F,d['A_weights']));b=list(map(F,d['B_weights']));x=F(1,2)
ys=sorted({F(a,n) for n in range(1,151) for a in range(1,n+1) if F(1,4)<F(a,n)<=F(1,3)})
for y in ys:
 q=[y,y,1-2*y]
 for w in [p,b,q]:ok(sum(w)==1);ok(min(w)>0)
 ok(min(mv(P,b))>=x);ok(min(mv(PT,p))>=x)
 ok(min(mv(Q,q))>=y);ok(min(mv(QT,b))>=y)
 ok(max(mv(RT,p))==F(1,2));ok(max(mv(R,q))==2*y);ok(2*y>F(1,2))
 fd=d['forward_dual'];rd=d['reverse_dual']
 ok(mv(R,list(map(F,fd['u_C'])))==mv(P,list(map(F,fd['v_B']))))
 ok(mv(RT,list(map(F,rd['u_A'])))==mv(QT,list(map(F,rd['v_B']))))
 ok(x*sum(fd['v_B'])==F(1,2));ok(y*sum(rd['v_B'])==2*y)
 # After deleting b1,b2 the vanished constraints no longer apply.
 bp=[F(1,2),F(1,2)];qp=[F(1,4),F(1,4),F(1,2)]
 PP=[[1,0],[0,1]];QQ=[[1,1,0],[0,0,1]]
 ok(min(mv(PP,bp))>=x);ok(min(mv(tr(PP),p))>=x)
 ok(min(mv(QQ,qp))>=y);ok(min(mv(tr(QQ),bp))>=y)
 ok(max(mv(R,qp))==F(1,2))
# Actual 40+40+40 ordinary graph, retaining all positive middle types.
def types(sizes):return [j for j,n in enumerate(sizes) for _ in range(n)]
AA,BB,CC=map(types,[d['blowup_A'],d['blowup_B'],d['blowup_C']])
PP=[[P[i][j] for j in BB] for i in AA];QQ=[[Q[j][k] for k in CC] for j in BB]
ok(len(AA)==len(BB)==len(CC)==40)
for row in PP:ok(sum(row)>=20)
for row in tr(PP):ok(sum(row)>=20)
for row in QQ:ok(sum(row)>=12)
for row in tr(QQ):ok(sum(row)>=12)
RR=[[any(PP[i][j] and QQ[j][k] for j in range(40)) for k in range(40)] for i in range(40)]
ok(max(map(sum,tr(RR)))==20);ok(max(map(sum,RR))==24)
ok(not d['is_original_counterexample'])
print(json.dumps({'status':'PASS','assertions':checks,'family_parameters':len(ys),'blowup_vertices':120,'scope':'Exact template and blow-up certificates; lower bounds apply to the retained template, not to all graphs'},indent=2,sort_keys=True))
