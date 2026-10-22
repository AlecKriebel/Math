"""Parent exact checks for the new audit Fourier proof using classical tools.
Written independently of reviewer programs. The analytic inequalities are
proved in ROOT_FOURIER_PRIORITY_BRIDGE.md, not certified by these finite checks.
"""
from collections import Counter
from fractions import Fraction as Q
import json

checks=[]
def require(name,condition):
 if not condition:raise RuntimeError(name)
 checks.append(name)
for n in range(1,65):
 sums=Counter(a+b for a in range(n) for b in range(n))
 differences=Counter(a-b for a in range(n) for b in range(n))
 energy=sum(x*x for x in sums.values())
 require('pair-sum energy n'+str(n),energy==Q(2*n**3+n,3))
 require('Laurent constant term n'+str(n),sum(differences[k]*differences[-k] for k in differences)==energy)
 require('triangular multiplicities n'+str(n),all(sums[s]==min(s+1,2*n-1-s) for s in range(2*n-1)))
 if n<=9:
  direct=sum(a+b==c+d for a in range(n) for b in range(n) for c in range(n) for d in range(n))
  require('independent four-index expansion n'+str(n),direct==energy)
# Identity proving pi<22/7: numerator/(1+x^2)=quotient-4/(1+x^2).
num=[0,0,0,0,1,-4,6,-4,1]
quotient=[4,0,-4,0,5,-4,1]
product=[0]*9
for i,a in enumerate(quotient):product[i]+=a;product[i+2]+=a
product[0]-=4
require('positive-integral pi upper-bound division',product==num)
require('polynomial integral is22/7',sum(Q(a,i+1) for i,a in enumerate(quotient))==Q(22,7))
pi4upper=Q(22,7)**4
n=234
gap=60*n*n+30-48*pi4upper*(3*n-1)
require('certified strict fourth-moment lower-bound gap at234',gap==Q(5975502,2401) and gap>0)
require('all larger n positivity: constant',gap>0)
require('all larger n positivity: linear',120*n-144*pi4upper>0)
require('all larger n positivity: quadratic',60>0)
require('coarse pi<4 witness n1000',Q(2*1000**2+1,48*4**4)>Q(3*1000-1,30))
# Controls against losing the coherent off-diagonal terms or normalization.
require('energy is not iid-pair energy n3',Q(2*3**3+3,3)!=2*3**2-3)
require('coherent fourth energy grows cubically',Q(2*8**3+8,3)>8**2)
require('normalized fourth moment needs n4 denominator',Q(2*234**3+234,3*234**4)!=Q(2*234**3+234,3*234**2))
require('bound does not prove n3 reversal',Q(2*3**2+1,48*pi4upper*3**3)<Q(4,405))
require('fixed zero generator does not equal generator average',4**4!=Q(2*4**3+4,3))
print(json.dumps({'status':'PASS','checks_passed':len(checks),'checks':checks,'n234_crossmultiplied_gap_lower':str(gap),'witness_n1000_with_pi_lt4':True,'formal_certification':False},indent=2))
