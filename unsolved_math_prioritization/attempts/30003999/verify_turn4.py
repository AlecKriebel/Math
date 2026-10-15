"""Exact controls for the positive-root and gap bounds; no approximate roots."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json
import sympy as s
count=0
assert F(3,4)*F(17,16)==F(51,64)<1;count+=1
assert F(9,8)*F(15,16)==F(135,128)>1;count+=1
assert F(15,16)/F(3,4)==F(5,4);count+=1
for r in range(1,501):
 assert r*F(3,4)**(r-1)<=F(27,16);count+=1
 if r>=3:assert r*F(1,2)**(r-1)<=F(3,4);count+=1
# Universal algebra in n for the Rouche disk.
n=s.symbols('n',positive=True,integer=True);radius=1/(1024*n)
assert s.simplify(512*n*radius**2-radius/2)==0;count+=1
assert F(1,2)<F(4,3);count+=1
assert F(2)/(1-F(7,8))**3==1024;count+=1
# Endpoint and derivative interval implications on finite exact input instances.
near=0
for size in range(2,7):
 for rs in combinations_with_replacement(range(1,13),size):
  val=sum((F(2,3)**r for r in rs),F(0))-1
  assert val!=0;count+=1
  if abs(val)<=F(1,16):
   assert sum((F(1,2)**r for r in rs),F(0))<1;count+=1
   assert sum((F(3,4)**r for r in rs),F(0))>1;count+=1
   near+=1
# Tail margin constants and exponent-cap integrality.
for N in range(2,101):
 k=(N-1).bit_length();M=3*k*(3**N-1)//2
 assert 2*M==3*k*(3**N-1);count+=1
 assert N*F(8,27)**k<=F(16,27);count+=1
 assert 1-F(16,27)==F(11,27);count+=1
# Good conditioning does not imply a large value at a rational comparison point.
for N in range(3,101):
 assert 2*F(1,2)+F(1,2)**N-1==F(1,2)**N;count+=1
 assert 3*F(2,3)+F(2,3)**N-2==F(2,3)**N;count+=1
print(json.dumps({'status':'PASS','exact_assertions':count,'near_threshold_positive_instances':near,'positive_root_local_radius':'1/(1024*n)','gap_bound':'(11/27)*3^(-M_n), M_n=(3*ceil(log2 n)/2)*(3^n-1), n>=2','limitations':'Exact algebra and finite controls of analytic estimates, not a polynomial rational-separation bound or a sign-complexity lower bound.'},indent=2))
