import json
checks=0
def ck(x):
 global checks
 checks+=1
 assert x
def red(w):
 s=[]
 for x in w:
  if s and s[-1]==-x:s.pop()
  else:s.append(x)
 return tuple(s)
def inv(w):return tuple(-x for x in reversed(w))
def apply(A,w):
 out=()
 for x in w:out=red(out+(A[x-1] if x>0 else inv(A[-x-1])))
 return out
def comp(A,B):return tuple(apply(A,w) for w in B)
def gen(n,i,sign):
 A=[(j+1,) for j in range(n)]
 if sign==1:A[i-1]=(i,i+1,-i);A[i]=(i,)
 else:A[i-1]=(i+1,);A[i]=(-(i+1),i,i+1)
 return tuple(A)
def aut(n,w):
 A=tuple((j+1,) for j in range(n))
 for i in w:A=comp(A,gen(n,abs(i),1 if i>0 else -1))
 return A
examples=[]
for K in range(2,17):
 N=K+2;delta=tuple(range(1,N));d_inv=inv(delta)
 one=aut(N,());a=(1,);a1=delta+a+d_inv
 ck(aut(N,a+a1+a)==aut(N,a1+a+a1))
 for j in range(1,K+1):
  aj=delta*j+a+d_inv*j;ck(aut(N,aj)==aut(N,(j+1,)))
  if j>=2:ck(aut(N,a+aj+inv(a)+inv(aj))==one)
 for i in range(1,N-1):ck(aut(N,delta+(i,)+d_inv)==aut(N,(i+1,)))
 w=(-1,)*4+a1+(1,1)+a1;alpha=(-1,)*4+(2,1,1,2)
 ck(aut(N,w)==aut(N,alpha));ck(sum(1 if x>0 else -1 for x in alpha)==0)
 # The commuting Jucys-Murphy factors used in the cited signature calculation.
 eta2=(1,1);eta3=(2,1,1,2)
 ck(aut(N,eta2+eta3)==aut(N,eta3+eta2))
 ck(aut(N,inv(eta2)*2+eta3)==aut(N,alpha))
 examples.append({'K':K,'target_strands':N})
for m in range(1,101):
 for i in range(m+1):
  for j in range(i+1,m+1):
   ck(min(abs(x-y) for x in (3*i,3*i+1) for y in (3*j,3*j+1))>=2)
print(json.dumps({'assertions':checks,'finite_presentations_checked':len(examples),'K_range':[2,16],'displacement_pattern_max_m':100,'scope':'Exact free-group Artin actions and integer separation; signature and displacement bounds are credited primary inputs'},indent=2,sort_keys=True))
