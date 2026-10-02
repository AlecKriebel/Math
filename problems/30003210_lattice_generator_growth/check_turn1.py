import itertools,json
from fractions import Fraction
checks=0
def test(c):
 global checks
 assert c
 checks+=1
def mul(A,B):return tuple(sum(A[2*i+k]*B[2*k+j] for k in range(2)) for i in range(2) for j in range(2))
def power(A,n):
 R=(1,0,0,1)
 while n:
  if n%2:R=mul(R,A)
  A=mul(A,A);n//=2
 return R
def v3(n):
 if not n:return 100000
 s=0
 while n%3==0:n//=3;s+=1
 return s
for B in itertools.product(range(-2,3),repeat=4):
 if not any(B):continue
 for k in range(1,4):
  A=tuple((1 if i in (0,3) else 0)+3**k*B[i] for i in range(4))
  s=min(v3(3**k*b) for b in B)
  for ell in (2,3,5,7):
   P=power(A,ell);z=min(v3(P[i]-(1 if i in (0,3) else 0)) for i in range(4))
   test(z==s+(ell==3))
for den in range(1,20):
 for num in range(den,den*5):
  s=Fraction(num,den);test(1+2*s>1+s);test(3*s>1+s)
for m in range(1,1000):
 test(2**(m.bit_length()-1)<=m<2**m.bit_length())
for N in range(1,8):
 for D in range(1,12):test((3**D)**(N*N)==3**(D*N*N))
print(json.dumps({'assertions':checks,'scope':'finite exact controls for the written valuation and index proofs; no finite test proves the source conjecture'},indent=2))
