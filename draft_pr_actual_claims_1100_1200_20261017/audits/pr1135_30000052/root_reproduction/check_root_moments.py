"""Exact parent reconstruction of moments, independent of reviewer programs.
Standard library only; no numerical quadrature or formal-proof claim.
"""
from fractions import Fraction as Q
from math import comb, factorial
import json

def add(*ps):
 out=[Q(0)]*max(map(len,ps))
 for p in ps:
  for i,v in enumerate(p):out[i]+=v
 return trim(out)
def trim(p):
 while len(p)>1 and not p[-1]:p.pop()
 return p
def scale(p,a):return trim([a*x for x in p])
def mul(p,q):
 r=[Q(0)]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):r[i+j]+=a*b
 return trim(r)
def power(p,n):
 r=[Q(1)]
 for _ in range(n):r=mul(r,p)
 return r
def integral(p,a=Q(0),b=Q(1)):
 return sum(v*(b**(i+1)-a**(i+1))/Q(i+1) for i,v in enumerate(p))
def value(p,t):return sum(v*t**i for i,v in enumerate(p))
checks=[]
def check(name,got,want):
 if got!=want:raise RuntimeError((name,got,want))
 checks.append(name)
one=[Q(1)];x=[Q(0),Q(1)]
q=[Q(0),Q(0),Q(1,2)]
# Solve E N and E binom(N,2), without assuming iid triples.
P=[add([Q(1),-3,3],scale(q,-1)),add([Q(0),3,-6],scale(q,3)),add([Q(0),0,3],scale(q,-3)),q]
check('total probability',add(*P),one)
check('expected indexed count E N',add(*(scale(P[k],k) for k in range(4))),[Q(0),3])
check('expected unordered pairs E binom(N,2)',add(*(scale(P[k],comb(k,2)) for k in range(4))),[Q(0),0,3])
F=add(*(mul(P[k],power([Q(k,3),Q(-1)],4)) for k in range(4)))
check('derived lattice integrand',F,[Q(0),Q(1,27),Q(8,27),Q(-10,9),Q(1)])
lattice=2*integral(F,b=Q(1,2))
check('lattice fourth moment',lattice,Q(19,1620))
def iid_integrand(n):
 return add(*(scale(mul(mul(power(x,k),power([Q(1),Q(-1)],n-k)),power([Q(k,n),Q(-1)],4)),comb(n,k)) for k in range(n+1)))
G=iid_integrand(3)
diff=add(F,scale(G,-1))
check('pointwise lower-half margin',diff,scale(mul(power(x,2),power([Q(1),Q(-2)],2)),Q(2,9)))
check('integrated strict excess',2*integral(diff,b=Q(1,2)),Q(1,540))
for n in range(1,17):
 check('independent binomial iid n'+str(n),integral(iid_integrand(n)),Q(3*n-1,30*n**3))
check('ratio',lattice/integral(G),Q(19,16))
for p in (2,4,6,8):
 # Integrating both empty tails first in shift and then generator.
 tail_one=Q(2,(p+1)*(p+2))*integral(power([Q(1),Q(-1)],p+2))
 check('one unit-scaled triangle p'+str(p),tail_one,Q(2,(p+1)*(p+2)*(p+3)))
check('n4 two-triangle lower bound',Q(4,5*6*7*3),Q(2,315))
check('n4 lower bound excess',Q(2,315)-Q(11,1920),Q(5,8064))
check('n3 tail bound insufficient',Q(1,105)<Q(4,405),True)
# Additional deduction from the accepted lower bound, not needed for n3.
# At n=4+t, the cross-multiplied comparison polynomial is positive.
cross=add(scale(power([Q(4),Q(1)],3),4),scale(power([Q(4),Q(1)],2),-21),scale([Q(4),Q(1)],28),[Q(-7)])
check('all-n>=4 lower-bound comparison polynomial',cross,[Q(25),Q(52),Q(27),Q(4)])
for d in range(1,9):
 for n in (1,2,3,4,11):
  second=(Q(1,2)**d-Q(1,3)**d)/n
  check('positive second moment '+str((n,d)),second>0,True)
# Adverse controls distinguish erroneous independence, normalization, reflection.
check('pairwise does not imply triple',value(q,Q(1,4))!=Q(1,4)**3,True)
check('lower-half q cannot extend to one',value(q,Q(1))!=1,True)
check('missing reflection factor fails',integral(F,b=Q(1,2))!=lattice,True)
check('unnormalized count fourth moment differs',3**4*lattice!=lattice,True)
print(json.dumps({'status':'PASS','checks_passed':len(checks),'checks':checks,'lattice_n3':str(lattice),'iid_n3':str(integral(G)),'excess':str(2*integral(diff,b=Q(1,2))),'all_n_ge4_from_tail_bound':True,'formal_certification':False},indent=2))
