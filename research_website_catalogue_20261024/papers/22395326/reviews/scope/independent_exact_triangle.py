"""Own exact differentiation of the printed literal sunlet map; no source imports."""
from fractions import Fraction as Q
from itertools import permutations
import json

def rank(A):
 A=[list(r) for r in A];i=0
 for j in range(len(A[0])):
  k=next((k for k in range(i,len(A)) if A[k][j]),None)
  if k is None:continue
  A[i],A[k]=A[k],A[i];a=A[i][j];A[i]=[x/a for x in A[i]]
  for k in range(len(A)):
   if k!=i:
    a=A[k][j];A[k]=[x-a*y for x,y in zip(A[k],A[i])]
  i+=1
  if i==len(A):break
 return i

def determinant(A):
 A=[list(r) for r in A];d=Q(1)
 for j in range(len(A)):
  k=next((k for k in range(j,len(A)) if A[k][j]),None)
  if k is None:return Q(0)
  if k!=j:A[j],A[k]=A[k],A[j];d=-d
  pivot=A[j][j];d*=pivot
  for k in range(j+1,len(A)):
   a=A[k][j]/pivot;A[k]=[x-a*y for x,y in zip(A[k],A[j])]
 return d
coords=[(x,y,x^y) for x in range(4) for y in range(4) if (x,y)!=(0,0)]
edges={k:[Q(1)]+[Q(1,3) if k=='f' else Q(1,2)]*3 for k in 'abcdef'};lam=Q(1,2)
rows=[];values=[]
for x,y,z in coords:
 a,b,c,d,e,f=[edges[k] for k in 'abcdef'];p=a[x]*b[y]*c[z];u=lam*f[y]*d[z];v=(1-lam)*f[x]*e[z];value=p*(u+v);values.append(value)
 row=[]
 for edge in 'abcdef':
  for h in range(1,4):
   derivative={'a':value*(x==h),'b':value*(y==h),'c':value*(z==h),'d':p*u*(z==h),'e':p*v*(z==h),'f':p*(u*(y==h)+v*(x==h))}[edge]
   row.append(derivative/value)
 row.append(p*(f[y]*d[z]-f[x]*e[z])/value);rows.append(row)
results=[]
for blocks in [[[1,2,3]],[[1,3],[2]],[[1],[2],[3]]]:
 A=[[sum(row[3*i+h-1] for h in block) for i in range(6) for block in blocks]+[row[-1]] for row in rows]
 results.append({'r':len(blocks),'parameter_dimension':6*len(blocks)+1,'rank_at_printed_strict_point':rank(A),'kernel_dimension':len(A[0])-rank(A)})
# Trivial directions scale every nonzero character of an edge equally.
idx=lambda c:coords.index(tuple(c));directions=[[sum(row[3*i:3*i+3]) for i in [0,1,2,5]] for row in rows]
J0=[directions[idx(c)] for c in [(1,1,0),(1,0,1),(0,1,1),(2,1,3)]]
# A distinguished G anisotropy changes only that character; contrasts kill invariant parts.
contrast_pairs=[((2,2,0),(1,1,0)),((2,0,2),(1,0,1)),((0,2,2),(0,1,1)),((1,2,3),(2,1,3)),((1,3,2),(2,1,3))]
Jp=[[rows[idx(a)][3*i+1]-rows[idx(b)][3*i+1] for i in [0,1,2,3,5]] for a,b in contrast_pairs]
assert determinant(J0)==Q(-1,2) and determinant(Jp)==Q(-1,4)
# Exhaustive finite orbit arithmetic is universal for the stated finite state set.
orbits=[]
for perms in [list(permutations([1,2,3])),[(1,2,3),(3,2,1)],[(1,2,3)]]:
 unseen={(x,y,x^y) for x in range(4) for y in range(4)};groups=[]
 while unseen:
  c=next(iter(unseen));orb={tuple(([0]+list(p))[h] for h in c) for p in perms};unseen-=orb;groups.append(sorted(orb))
 orbits.append({'group_order':len(perms),'coordinate_orbits':len(groups),'normalized_ambient':len(groups)-1,'orbits':groups})
print(json.dumps({'method':'own exact rational derivative of literal printed q_xyz, logarithmic edge/output coordinates; no bundled mathematical program imported','point':{'a_through_e':'1/2','f':'1/3','lambda':'1/2'},'results':results,'J0':[[str(x) for x in row] for row in J0],'det_J0':str(determinant(J0)),'J_anisotropy':[[str(x) for x in row] for row in Jp],'det_J_anisotropy':str(determinant(Jp)),'finite_state_orbits':orbits,'boundary':'At-point rank is an exact lower bound for generic rank. Global K3P upper bound/common orientation physical germs/H14 irreducibility and all-network classification remain separate proof/import obligations.'},indent=2))
