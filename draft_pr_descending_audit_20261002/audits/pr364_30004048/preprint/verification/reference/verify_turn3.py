#!/usr/bin/env python3
"""Exact source-matrix, finite-graph and boundary-extraction certificates."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
checks=0;low_graphs=0;full_graphs=0;templates=0
def ok(x):
 global checks
 assert x
 checks+=1
def tr(M):return list(map(list,zip(*M)))
def mv(M,v):return [sum(F(a)*b for a,b in zip(row,v)) for row in M]
def types(sizes):return [i for i,n in enumerate(sizes) for _ in range(n)]
def boolean(P,Q):return [[int(any(a*b for a,b in zip(row,col))) for col in tr(Q)] for row in P]
d=json.loads(Path(__file__).with_name('TURN_3_CERTIFICATE.json').read_text())
M=d['M'];bs=d['B_type_sizes'];cs=d['C_type_sizes'];b=[F(i,27) for i in bs];q=[F(i,27) for i in cs]
for num,N in [(13,M),(14,[[1-a for a in row] for row in M])]:
 theta=F(num,27);ok(mv(N,q)==[theta]*7);ok(mv(tr(N),b)==[theta]*7)
 ok(len(set(map(tuple,tr(N))))==7);ok(max(map(sum,N))==4)
 # Positive equal weighted column sizes imply the explicit incomparability.
 for i,j in product(range(7),repeat=2):
  if i!=j:ok(any(N[k][i] and not N[k][j] for k in range(7)))
 cert=d['theta'+str(num)];AA=types(cert['A_type_sizes']);BB=types(bs);CC=types(cs)
 P=[[1 if i==7 else 1-N[j][i] for j in BB] for i in AA]
 Q=[[N[j][k] for k in CC] for j in BB]
 R=boolean(P,Q)
 mins=[min(map(sum,P)),min(map(sum,tr(P))),min(map(sum,Q)),min(map(sum,tr(Q)))]
 ok(mins==cert['minimum_directed_degrees']);ok(set(map(sum,tr(R)))=={cert['reached_A_count']})
 ok(F(cert['reached_A_count'],len(AA))==F(cert['upper_bound']))
 ok(len(AA)+len(BB)+len(CC)==162)
 for v in mv(P,[F(1,len(BB))]*len(BB)):ok(v>=1-theta)
 for v in mv(tr(P),[F(1,len(AA))]*len(AA)):ok(v>=1-theta)
 for v in mv(Q,[F(1,len(CC))]*len(CC)):ok(v>=theta)
 for v in mv(tr(Q),[F(1,len(BB))]*len(BB)):ok(v>=theta)
# All possible invariant values permitted by the source certificate are separated.
gaps=[]
for dd,ee in product(range(1,5),repeat=2):
 gap=abs(F(13,27*dd)-F(14,27*ee));gaps.append(gap)
 ok(13*ee!=14*dd);ok(gap>=F(1,108))
ok(min(gaps)==F(1,108))
# Cyclic templates: nonempty class, integer minimum bound, and delta=0 case.
for r in range(2,17):
 for p in range(1,r):
  N=[[int((i-j)%r<p) for j in range(r)] for i in range(r)]
  w=[F(1,r)]*r;theta=F(p,r);degree=p;t=theta/degree;delta=1-r*t
  ok(mv(N,w)==[theta]*r);ok(mv(tr(N),w)==[theta]*r)
  ok(len(set(map(tuple,tr(N))))==r);ok(delta==0);ok(t==F(1,r));templates+=1
# Universal-lower-bound extraction on every eligible labeled3+3+3 graph
# at the two nontrivial rational boundary parameters of denominator3.
matrices=[[[int((mask>>(3*i+j))&1) for j in range(3)] for i in range(3)] for mask in range(512)]
for numerator in (1,2):
 theta=F(numerator,3);x=1-theta
 Ps=[P for P in matrices if min(map(sum,P))>=3*x and min(map(sum,tr(P)))>=3*x]
 Qs=[Q for Q in matrices if min(map(sum,Q))>=3*theta and min(map(sum,tr(Q)))>=3*theta]
 for P,Q in product(Ps,Qs):
  R=boolean(P,Q);Fval=F(max(map(sum,tr(R))),3)
  if Fval==1:full_graphs+=1;continue
  low_graphs+=1
  ok(set(map(sum,tr(Q)))=={3*theta});ok(set(map(sum,Q))=={3*theta})
  columns=list(map(tuple,tr(Q)));distinct=sorted(set(columns));counts=[columns.count(c) for c in distinct]
  N=tr(distinct);qw=[F(c,3) for c in counts];bw=[F(1,3)]*3
  ok(mv(N,qw)==[theta]*3);ok(mv(tr(N),bw)==[theta]*len(distinct))
  masses=[F(sum(tuple(row)==tuple(1-z for z in col) for row in P),3) for col in distinct]
  ok(min(masses)>0);t=min(masses);D=max(map(sum,N));ok(Fval==1-t);ok(t*D<=theta)
  for row in N:ok(sum(a*w for a,w in zip(row,masses))<=theta)
print(json.dumps({'status':'PASS','assertions':checks,'explicit_graph_orders':[162,162],'cyclic_templates':templates,'nonfull_boundary_graphs_checked':low_graphs,'full_reach_graphs_checked':full_graphs,'scope':'Exact finite controls; the universal invariant formula, minimum attainment and rationalization are proved analytically'},indent=2,sort_keys=True))
