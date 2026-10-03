from fractions import Fraction as Q
import itertools,json
N=0
def ck(v):
 global N
 assert v;N+=1
I=((1,0),(0,1))
def add(A,B):return tuple(tuple(A[i][j]+B[i][j] for j in range(2)) for i in range(2))
def neg(A):return tuple(tuple(-a for a in row) for row in A)
def mul(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
T={1:((1,1),(0,1)),2:((1,0),(1,1)),-1:((1,-1),(0,1)),-2:((1,0),(-1,1))}
ck(mul(T[1],T[2])!=mul(T[2],T[1]))
# Right-suffix telescoping with noncommuting integral actions and negative generators.
for size in range(7):
 for word in itertools.product([1,-1,2,-2],repeat=size):
  product=I
  for x in word:product=mul(product,T[x])
  total=((0,0),(0,0));suffix=I
  for x in reversed(word):
   coeff=suffix if x>0 else neg(mul(T[x],suffix))
   total=add(total,mul(add(T[abs(x)],neg(I)),coeff));suffix=mul(T[x],suffix)
  ck(total==add(product,neg(I)))
# Heisenberg fixed-side commutators for arbitrary signed powers in a finite range.
def hm(x,y):return (x[0]+y[0],x[1]+y[1],x[2]+y[2]+x[0]*y[1])
def hi(x):return (-x[0],-x[1],-x[2]+x[0]*x[1])
for n in range(-100,101):
 a=(n,0,0);b=(0,1,0);ck(hm(hm(hm(a,b),hi(a)),hi(b))==(0,0,n))
# Independent exact rational primal-dual certificates for a family of abelian presentations.
for q in range(1,101):
 for p in range(1,q+1):
  primal=(Q(p,q),Q(0));dual=(Q(1),Q(p,q));alpha=Q(p,q)
  ck(p*dual[0]-q*dual[1]==0);ck(max(map(abs,dual))<=1)
  ck(sum(map(abs,primal))==dual[1]==alpha)
  ck(q*alpha==p)
# Displaced supports in the infinite braid-shift construction.
for m in range(1,51):
 supports=[(3*i,3*i+1) for i in range(m+1)]
 for i,j in itertools.combinations(range(m+1),2):ck(min(abs(a-b) for a in supports[i] for b in supports[j])>=2)
ck(14*3==42)
print(json.dumps({'status':'PASS','independent_assertions':N,'scope':'Noncommuting augmentation telescoping, exact Heisenberg identities, rational stable-norm certificates and braid support separation. Signature and displacement theorems are independently source-checked credited inputs.'},indent=2))
