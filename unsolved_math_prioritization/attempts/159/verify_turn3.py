"""Exact controls of the inward step, Boolean products, and failed padding."""
from itertools import product
import json
from fractions import Fraction as F
N=0
def ck(b):
 global N
 N+=1
 assert b
def conv(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def polys(m):return [(1,)+q+(1,) for q in product((0,1),repeat=m-1)]
def rem(a,b):
 a=list(map(F,a));b=list(map(F,b))
 while len(a)>=len(b):
  v=a[-1]/b[-1];k=len(a)-len(b)
  for i,x in enumerate(b):a[k+i]-=v*x
  while a and not a[-1]:a.pop()
 return a
def main():
 steps=admissible=windows=nonpal=0
 for a,b,c,d in product(range(5),repeat=4):
  if a+b==c+d and a+b in (0,4) and a*d==c*b==0:
   steps+=1;ck(a==c and b==d);ck(all(x in (0,4) for x in (a,b,c,d)))
 for m in range(1,8):
  for n in range(m,9):
   for a,b in product(polys(m),polys(n)):
    c=conv(a,b)
    if max(c)>1:continue
    admissible+=1
    if all(c[k]==c[-1-k] for k in range(m//2+1)):
     windows+=1;ck(a==a[::-1]);ck(all(x in (0,1) for x in b))
     if c!=c[::-1]:nonpal+=1
 a=(1,0,1);b=tuple(int(i in (0,5,11)) for i in range(12));c=conv(a,b)
 ck(max(c)==1 and c[1]==c[-2]);ck(c!=c[::-1] and b!=b[::-1])
 A=(1,1,0,1);Ar=A[::-1]
 for L in range(4,51):
  D=list(A)+[0]*L
  for i,x in enumerate(Ar):D[L+i]+=x
  ck(D==D[::-1]);ck(max(D)==1);ck(bool(rem(D,A)))
  P=conv(A,Ar);ck(P[len(A)-1]==sum(A)>1)
 print(json.dumps({'problem_id':159,'turn':3,'status':'PASS','exact_assertions':N,'local_inward_step_cases':steps,'Boolean_factor_pairs':admissible,'outer_window_cases':windows,'nonpalindromic_window_cases':nonpal,'padding_lengths_checked':47,'scope':'Finite algebraic controls. All-degree reflection criterion and failures of generic symmetrization follow from the written proofs.'},indent=2))
if __name__=='__main__':main()
