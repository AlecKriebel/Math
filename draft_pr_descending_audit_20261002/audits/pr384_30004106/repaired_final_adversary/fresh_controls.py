#!/usr/bin/env python3
"""Fresh exact controls from actual actions, not imported audit code."""
from itertools import product
from fractions import Fraction as F
from collections import Counter
import json
checks=0
def ck(v):
 global checks
 assert v
 checks+=1

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(A,B,p):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*B)] for r in A]
def add(A,B,p):return [[(x+y)%p for x,y in zip(a,b)] for a,b in zip(A,B)]
def scale(A,x,p):return [[x*y%p for y in r] for r in A]
def powm(A,n,p):
 B=eye(len(A))
 for _ in range(n):B=mm(B,A,p)
 return B

def rank(A,p):
 A=[r[:] for r in A];r=0
 for c in range(len(A[0]) if A else 0):
  t=next((t for t in range(r,len(A)) if A[t][c]%p),None)
  if t is None:continue
  A[t],A[r]=A[r],A[t];a=pow(A[r][c],-1,p);A[r]=[x*a%p for x in A[r]]
  for t in range(r+1,len(A)):
   a=A[t][c]%p
   if a:A[t]=[(x-a*y)%p for x,y in zip(A[t],A[r])]
  r+=1
 return r

def kron(A,B):return [[x*y for x in ar for y in br] for ar in A for br in B]
actual=[]
for p,j in [(2,1),(3,2),(5,4)]:
 n=j*p; X=[[int(c==r+1) for c in range(j)] for r in range(j)]
 Y=[[int(c==r+1) for c in range(p)] for r in range(p)]
 x=kron(X,eye(p));y=kron(eye(j),Y)
 A=add(eye(n),x,p); B=add(eye(n),y,p)
 ck(mm(A,B,p)==mm(B,A,p));ck(powm(A,p,p)==eye(n));ck(powm(B,p,p)==eye(n))
 mons=[mm(powm(x,a,p),powm(y,b,p),p) for a in range(j) for b in range(p)]
 ck(rank([[M[r][c] for r in range(n) for c in range(n)] for M in mons],p)==j*p)
 # These actual commuting matrices realize the local tensor endomorphism ring.
 # Its augmentation ideal is nilpotent with nilpotence bound j+p-1.
 for M in mons[1:]:ck(powm(M,j+p-1,p)==[[0]*n for _ in range(n)])
 def jord(g):
  z=add(g,scale(eye(n),-1,p),p)
  null=[0]+[n-rank(powm(z,k,p),p) for k in range(1,p+1)]
  ck(null[-1]==n)
  return [null[k]-null[k-1] for k in range(1,p+1)]
 restrictions=[]
 for a,b in [(1,0)]+[(a,1) for a in range(p)]:
  r=jord(mm(powm(A,a,p),powm(B,b,p),p))
  ck(r==([p]*j+[0]*(p-j) if b==0 else [j]*p))
  restrictions.append({'line':[a,b],'jordan_blocks_at_least_k':r,'free':b!=0})
 if p<=3:
  # Solve centralizer constraints for actual matrices, independently of the tensor formula.
  equations=[]
  for C in [A,B]:
   for r,c in product(range(n),repeat=2):
    eq=[0]*(n*n)
    for k in range(n):
     eq[r*n+k]=(eq[r*n+k]+C[k][c])%p
     eq[k*n+c]=(eq[k*n+c]-C[r][k])%p
    equations.append(eq)
  ck(n*n-rank(equations,p)==j*p)
  idempotents=0
  for coeffs in product(range(p),repeat=j*p):
   Q=[[0]*n for _ in range(n)]
   for M,c in zip(mons,coeffs):Q=add(Q,scale(M,c,p),p)
   if mm(Q,Q,p)==Q:idempotents+=1;ck(Q==eye(n) or not any(map(any,Q)))
  ck(idempotents==2)
 actual.append({'p':p,'core_j':j,'induced_dimension':n,'actual_monomial_basis_dimension':j*p,'cyclic_restrictions':restrictions,'enumerated_centralizer_idempotents':2 if p<=3 else None})

# Actual diagonal coset G-set tensor decomposition for all subgroups of C_p^2.
lattices=[]
for p in [2,3,5]:
 G=list(product(range(p),repeat=2));zero=(0,0)
 plus=lambda a,b:tuple((x+y)%p for x,y in zip(a,b))
 lines=[frozenset((c%p,0) for c in range(p))]+[frozenset((a*c%p,c%p) for c in range(p)) for a in range(p)]
 S=[frozenset([zero])]+lines+[frozenset(G)]
 def cosets(H):
  todo=set(G);out=[]
  while todo:
   a=min(todo);C=frozenset(plus(a,h) for h in H);out.append(C);todo-=C
  return out
 C=[cosets(H) for H in S]
 actions=[]
 for cs in C:actions.append({g:[cs.index(frozenset(plus(g,x) for x in c)) for c in cs] for g in G})
 for i,j in product(range(len(S)),repeat=2):
  todo=set(product(range(len(C[i])),range(len(C[j]))));stabs=[]
  while todo:
   a,b=min(todo);orbit={(actions[i][g][a],actions[j][g][b]) for g in G};todo-=orbit
   stab=frozenset(g for g in G if actions[i][g][a]==a and actions[j][g][b]==b);stabs.append(stab)
  intersection=S[i]&S[j];summ=frozenset(plus(a,b) for a in S[i] for b in S[j])
  ck(all(H==intersection for H in stabs));ck(len(stabs)==len(G)//len(summ))
 # Full dimension weighted basis and exact Mobius/mark transform including projective q_0.
 mu={}
 for j,H in enumerate(S):
  for i,V in enumerate(S):
   if V<=H:mu[i,j]=1 if i==j else -sum(mu[i,k] for k,K in enumerate(S[:j]) if V<=K<=H)
 E=[{i:mu[i,j] for i in range(len(S)) if (i,j) in mu and mu[i,j]} for j in range(len(S))]
 def times(a,b):
  out=Counter()
  for i,c in a.items():
   for j,d in b.items():out[S.index(S[i]&S[j])]+=c*d
  return {i:x for i,x in out.items() if x}
 for i,j in product(range(len(S)),repeat=2):ck(times(E[i],E[j])==(E[i] if i==j else {}))
 ck({i:sum(e.get(i,0) for e in E) for i in range(len(S)) if sum(e.get(i,0) for e in E)}=={len(S)-1:1})
 norms=[sum(abs(x) for x in e.values()) for e in E]
 ck(norms==[1]+[2]*(p+1)+[2*p+2])
 # Norms of q_H are one in actual dimension weights; all factors are C. Exact bound for sum norm.
 forward=max(norms);inverse=max(sum(int(S[j]<=S[i]) for j in range(len(S))) for i in range(len(S)))
 for coeffs in product([-1,0,1],repeat=len(S)):
  # Keep p5 enumeration under 7000 inputs.
  f=[sum(coeffs[i]*int(S[j]<=S[i]) for i in range(len(S))) for j in range(len(S))]
  g=[sum(f[j]*E[j].get(i,0) for j in range(len(S))) for i in range(len(S))]
  ck(g==list(coeffs));ck(sum(map(abs,g))<=forward*sum(map(abs,f)));ck(sum(map(abs,f))<=inverse*sum(map(abs,coeffs)))
 lattices.append({'p':p,'subgroups':len(S),'actual_tensor_pair_orbits_checked':len(S)**2,'idempotent_weighted_norms':norms,'forward_sum_norm':forward,'inverse_sum_norm':inverse})

# Independent inseparable witness: companion s satisfies s^2=t; base change t=a^2 makes s+a nilpotent.
# Polynomial matrices over F2[a] represented by coefficient bit masks.
def pm(a,b):
 z=0
 while b:
  if b&1:z^=a
  a<<=1;b>>=1
 return z

def pmm(A,B):return [[pm(A[r][0],B[0][c])^pm(A[r][1],B[1][c]) for c in range(2)] for r in range(2)]
Smat=[[0,4],[1,0]];aI=[[2,0],[0,2]];eps=[[Smat[i][j]^aI[i][j] for j in range(2)] for i in range(2)]
ck(pmm(Smat,Smat)==[[4,0],[0,4]]);ck(any(map(any,eps)));ck(pmm(eps,eps)==[[0,0],[0,0]])
# Two distinct factors retain disjoint central idempotents even though EACH division factor base-changes to dual numbers.
ck(pmm([[1,0],[0,0]],[[0,0],[0,1]])==[[0,0],[0,0]])

# Q8 signed actual finite algebra: basis k,Omega,Omega2,Omega3,P, using verified minimal dimensions.
dims=[1,7,9,7,8]
def qmul(a,b):
 out=[F(0)]*5
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i==4 or j==4:out[4]+=x*y*dims[j if i==4 else i]
   else:
    k=(i+j)%4;m=F(dims[i]*dims[j]-dims[k],8);ck(m.denominator==1 and m>=0)
    out[k]+=x*y;out[4]+=x*y*m
 return out
unit=[F(1),F(0),F(0),F(0),F(0)];x=[F(-2),F(1),F(0),F(1),F(-3,2)]
def sadd(a,b):return [x+y for x,y in zip(a,b)]
def sscale(a,c):return [x*c for x in a]
ck(sum(a*d for a,d in zip(x,dims))==0)
x2=qmul(x,x);x3=qmul(x2,x);ck(sadd(sadd(x3,sscale(x2,6)),sscale(x,8))==[0]*5)
# Nonzero algebraic spectral idempotents force ambient roots; no species extension assumed.
idempotents=[]
for lam in [0,-2,-4]:
 Q=unit[:]
 for oth in [v for v in [0,-2,-4] if v!=lam]:Q=sscale(qmul(Q,sadd(x,sscale(unit,-oth))),F(1,lam-oth))
 ck(any(Q));ck(qmul(Q,Q)==Q);ck(qmul(sadd(x,sscale(unit,-lam)),Q)==[0]*5)
 idempotents.append([str(a) for a in Q])
ck(sadd(sadd(*[[F(a) for a in Q] for Q in idempotents[:2]]),[F(a) for a in idempotents[2]])==unit)
# Restriction to C2: k->k,Omega->k+3P2,Omega2->k+4P2,Omega3->k+3P2,P->4P2.
ck(sum(x[:4])==0);ck(sum(a*d for a,d in zip(x,[0,3,4,3,4]))==0)

result={'exact_assertions':checks,'actual_induction_controls':actual,'actual_coset_and_full_mobius_controls':lattices,'inseparable_radical_equality_countercontrol':True,'Q8_actual_full_signed_element':[str(a) for a in x],'Q8_ambient_spectrum':[0,-2,-4],'Q8_nonzero_polynomial_spectral_idempotents':idempotents,'universal_question_answered':False,'fresh_code_imports_no_candidate_or_previous_audit_code':True}
print(json.dumps(result,indent=2))
