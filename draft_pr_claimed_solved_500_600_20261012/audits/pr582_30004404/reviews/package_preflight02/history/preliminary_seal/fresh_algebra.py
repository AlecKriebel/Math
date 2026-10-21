#!/usr/bin/env python3
"""New finite controls: UT3(F5), free-normal-form and an SL2(Z) falsifier."""
from itertools import product
from fractions import Fraction
import json

def reduce(w):
 out=[]
 for x in w:
  if out and out[-1]==-x:out.pop()
  else:out.append(x)
 return tuple(out)
def inverse(w):return tuple(-x for x in w[::-1])
def bracket(u,v):return u+v+inverse(u)+inverse(v)
c=bracket((1,),(2,));d=(1,)+c+(-1,);w=reduce(bracket(c,d))
assert ''.join({1:'x',2:'y',-1:'X',-2:'Y'}[x] for x in w)=='xyXYxxyXYXyxxYXX'
assert len(w)==16 and reduce(w+inverse(w))==()
# Nilpotent nonabelian UT3(F5): triples encode entries (1,2),(2,3),(1,3).
p=5;one=(0,0,0)
def mul(x,y):a,b,c=x;d,e,f=y;return ((a+d)%p,(b+e)%p,(c+f+a*e)%p)
def inv(x):a,b,c=x;return (-a%p,-b%p,(a*b-c)%p)
def comm(x,y):return mul(mul(mul(x,y),inv(x)),inv(y))
def evaluate(word,x,y):
 im={1:x,2:y,-1:inv(x),-2:inv(y)};out=one
 for l in word:out=mul(out,im[l])
 return out
els=list(product(range(p),repeat=3));noncomm=0;paircount=0
for x,y in product(els,repeat=2):
 assert mul(x,inv(x))==mul(inv(x),x)==one
 z=comm(x,y);assert z[:2]==(0,0)
 assert evaluate(w,x,y)==one
 noncomm+=z!=one;paircount+=1
assert noncomm>0 and paircount==15625
# The genuine non-metabelian matrix evaluation may not be hardcoded to identity.
def mm(x,y):return tuple(sum(x[i*2+k]*y[k*2+j] for k in range(2)) for i in range(2) for j in range(2))
def mi(x):a,b,c,d=x;assert a*d-b*c==1;return(d,-b,-c,a)
x=(1,2,0,1);y=(1,0,2,1);im={1:x,2:y,-1:mi(x),-2:mi(y)};z=(1,0,0,1)
for l in w:z=mm(z,im[l])
assert z!=(1,0,0,1)
chi=[sum((Fraction(1,k) for k in a),Fraction(-1)) for a in [(2,3,7),(2,4,5),(3,3,4),(2,3,6),(2,3,5)]]
assert chi==[Fraction(-1,42),Fraction(-1,20),Fraction(-1,12),Fraction(0),Fraction(1,30)]
print(json.dumps({'status':'PASS','witness':list(w),'length':len(w),'UT3_F5':{'order':125,'ordered_pairs':paircount,'witness_identity_pairs':paircount,'noncommuting_pairs':noncomm},'SL2Z_nonidentity_witness':list(z),'orbifold_characteristics_and_boundaries':list(map(str,chi)),'limits':'Exact finite checks supplement the universal proof; they do not classify fillings, exhaust free subgroups or establish historical priority.'},indent=2,sort_keys=True))
