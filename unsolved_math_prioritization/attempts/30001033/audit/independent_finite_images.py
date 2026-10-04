#!/usr/bin/env python3
"""Dense truncated unitriangular implementation independent of package code."""
import json, pathlib
P=pathlib.Path(__file__).resolve().parents[1]/'package'
M=json.loads((P/'matrices.json').read_text())['matrices']
records=[]
for m in range(1,6):
 n=3*(m+3);E=tuple(1<<i for i in range(n))
 masks=tuple((1<<min(n,3*(i//3+m+1)))-1 for i in range(n))
 def multiply(A,B):
  C=[]
  for i,row in enumerate(A):
   c=0
   while row:
    low=row&-row;c^=B[low.bit_length()-1];row^=low
   C.append(c&masks[i])
  return tuple(C)
 def inverse(A):
  B=list(E)
  for i in reversed(range(n)):
   row=A[i]^(1<<i)
   while row:
    low=row&-row;B[i]^=B[low.bit_length()-1];row^=low
   B[i]&=masks[i]
  return tuple(B)
 def generator(letter):
  poly=[M[letter+'0'],M[letter+'1']];A=list(E)
  for block in range(m+3):
   phase=block%3
   for d in range(1,m+1):
    if block+d>=m+3:break
    q,c=divmod(phase+d,3)
    if q>=2:continue
    for i in range(3):
     for j in range(3):
      A[3*block+i]^=poly[q][3*phase+i][3*c+j]<<(3*(block+d)+j)
  return tuple(A)
 def subgroup(gs):
  gs=set(gs)-{E};S={E};todo=[E]
  while todo:
   a=todo.pop()
   for g in gs:
    b=multiply(a,g)
    if b not in S:S.add(b);todo.append(b)
   assert len(S)<=65536
  return S
 x,y=generator('A'),generator('B');gens=[x,y];inverses=[inverse(g) for g in gens]
 assert all(multiply(g,h)==E and multiply(h,g)==E for g,h in zip(gens,inverses))
 K=subgroup(gens);orders=[len(K)];normality=[]
 for depth in range(m+1):
  candidates=set()
  for k in K:
   ki=inverse(k)
   for g,gi in zip(gens,inverses):
    candidates.add(multiply(multiply(multiply(ki,gi),k),g))
  J=subgroup(candidates);assert J<=K
  # Explicit normality, including both signs, rather than assuming the claim.
  for h in J:
   for g,gi in zip(gens,inverses):
    assert multiply(multiply(gi,h),g) in J
    assert multiply(multiply(g,h),gi) in J
  normality.append(True);orders.append(len(J))
  if J=={E}:break
  assert len(J)<len(K);K=J
 assert orders[-1]==1
 records.append({'cutoff':m,'orders':orders,'indices':[a//b for a,b in zip(orders,orders[1:])],'normality_checked_each_term':normality})
expected=json.loads((P/'controls-output.json').read_text())['finite_images']
assert all(r['orders']==s['lower_central_orders'] for r,s in zip(records,expected))
print(json.dumps({'algorithm':'band-truncated dense upper unitriangular matrices over F2','matches_frozen_results':True,'finite_images':records},indent=2))
