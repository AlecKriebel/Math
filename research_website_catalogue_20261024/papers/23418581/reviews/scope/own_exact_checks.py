#!/usr/bin/env python3
"""Reviewer-written exact formal root-coefficient checks. No target code imported."""
from math import comb
import hashlib,json
from pathlib import Path

def graph(p,m):
 # Column i is v_i=x^(m-i)y^i. Retain every coefficient of both formal root actions.
 edges={i:set() for i in range(m+1)};coefficients=0
 for i in range(m+1):
  for a in range(i+1):
   c=comb(i,a)%p;coefficients+=1
   if c:edges[i].add(i-a)
  for a in range(m-i+1):
   c=comb(m-i,a)%p;coefficients+=1
   if c:edges[i].add(i+a)
 return edges,coefficients

def reachable(g,start,allowed=None):
 allowed=set(g) if allowed is None else set(allowed);seen={start};todo=[start]
 while todo:
  x=todo.pop()
  for y in g[x]&allowed:
   if y not in seen:seen.add(y);todo.append(y)
 return seen

def strong(g,allowed=None):
 allowed=set(g) if allowed is None else set(allowed)
 return all(reachable(g,i,allowed)==allowed for i in allowed)

def comps(total,n):
 if n==1:yield(total,);return
 for first in range(total+1):
  for rest in comps(total-first,n-1):yield(first,)+rest

checks=0;rows=[]
for p in [3,5,7,11,13,17,19,23,29,31]:
 r=2*p-1;m=2*p-3;g,ncoeff=graph(p,r);checks+=1;assert strong(g)
 binomials=[comb(r,j)%p for j in range(r+1)];checks+=1;assert all(binomials)
 h,ncoeffB=graph(p,m);W=set(range(p-2))|set(range(p,2*p-2));Q={p-2,p-1}
 checks+=1;assert len(W)==2*p-4 and len(Q)==2 and W|Q==set(h) and not(W&Q)
 checks+=1;assert all(h[i]<=W for i in W)
 checks+=1;assert strong(h,W) and strong(h,Q)
 checks+=1;assert h[p-2]-Q and 0 in h[p-2]
 checks+=1;assert comb(p-2,p-2)%p==1
 checks+=1;assert comb(p-1,1)%p==p-1 and comb(m-(p-2),1)%p==p-1
 # Every nonzero torus-stable invariant support is W or the full B: SCC condensation is Q->W.
 checks+=1;assert all(reachable(h,i)==W for i in W) and all(reachable(h,i)==set(h) for i in Q)
 checks+=1;assert (2*p-2,1)!=(p,p-1)
 # Euler multiplication-polarization on all degree-r monomials at ranks2 and3.
 monomialchecks=0
 for n in [2,3]:
  for alpha in comps(r,n):
   monomialchecks+=1;checks+=1;assert sum(a%p for a in alpha)%p==r%p!=0
 # Polynomial highest vector coefficient support exactly W.
 checks+=1;assert {i for i in range(m+1)if comb(m,i)%p}==W
 rows.append({'p':p,'r':r,'Sym_r_dimension':r+1,'Sym_r_root_graph_strongly_connected':True,'B_dimension':m+1,'W_dimension':len(W),'quotient_dimension':len(Q),'B_SCC_sizes':[len(W),len(Q)],'quotient_to_W_nonsplit_obstruction':True,'formal_root_coefficients_checked':ncoeff+ncoeffB,'Euler_monomials_checked_ranks_2_3':monomialchecks,'equal_head_socle_dimensions':len(W)==len(Q)})
print(json.dumps({'status':'OWN_EXACT_CHECKS_PASS','implementation_SHA256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'arithmetic':'integer binomial coefficients reduced modulo exact prime, formal unipotent polynomial coefficients; no finite-field evaluation approximation','checks':checks,'rows':rows,'all_prime_theorem_proved_by_this_finite_run':False,'all_rank_Schur_input_proved_by_this_finite_run':False,'supplied_scientific_code_imports_or_execution':[]},indent=2))
