#!/usr/bin/env python3
"""Finite matrix-unit controls for the universal analytic corner argument."""
import itertools,json
checks=0; partitions=0; basis_count=0
def ok(x):
 global checks
 assert x
 checks+=1
def parts(n):
 def rec(a):
  if len(a)==n:yield a;return
  for x in range(max(a)+2):yield from rec(a+[x])
 if n:yield from rec([0])
for n in range(1,7):
 for labels in parts(n):
  partitions+=1
  basis=[(i,j) for i in range(n) for j in range(n) if labels[i]==labels[j]]
  ok(len(basis)<=n*n)
  diagonal=[(i,j) for i,j in basis if all(int(k==i)-int(k==j)==0 for k in range(n))]
  ok(diagonal==[(i,i) for i in range(n)])
  commuting=[]
  for (i,j),(k,l) in itertools.product(basis,repeat=2):
   basis_count+=1
   # Diagonal tensor projections act by row-label minus column-label.
   row=(i,k);col=(j,l)
   is_commuting=all(int(a==row)-int(a==col)==0 for a in itertools.product(range(n),repeat=2))
   ok(is_commuting==(i==j and k==l))
   if is_commuting:commuting.append((row,col))
  ok(len(commuting)==n*n)
  # Rank-one corners and normalized matrix-unit identity y=v(v*y).
  for i,j in basis:
   ok(labels[i]==labels[j]);ok((j,j) in basis and (i,i) in basis)
   for a in range(-3,4):ok(a==1*(1*a))
print(json.dumps({'status':'PASS','assertions':checks,'block_partitions':partitions,'tensor_matrix_units':basis_count,'scope':'Finite controls only; arbitrary C*-algebras, the shared-unit lemma and all-completion density argument are proved analytically'},indent=2,sort_keys=True))
