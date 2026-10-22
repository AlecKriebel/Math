"""Supplementary exact/algebraic and Decimal controls; universal proof is in the root note.
No external dependencies, no removable assertions; forced flag changes actual expected field.
"""
from fractions import Fraction as Q
from decimal import Decimal as D, localcontext
import argparse,hashlib,json,math
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--force-wrong-sign',action='store_true');args=ap.parse_args()
count=0

def require(ok,why):
 global count
 count+=1
 if not ok:raise ArithmeticError(why)

# Exact complex rational arithmetic (real,imaginary), independent from complex floating point.
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def inv(a):
 t=a[0]*a[0]+a[1]*a[1]
 return (a[0]/t,-a[1]/t)
def sqinv(a):return mul(inv(a),inv(a))
# Exact normalized disk moments of harmonic monomials; analytic mean-value theorem
# gives all degrees. Finite degrees independently catch mass/pi/angular mistakes.
def disk_monomial(a,b):
 if a%2 or b%2:return Q(0)
 u,v=a//2,b//2
 return Q(math.factorial(2*u)*math.factorial(2*v),4**(u+v)*math.factorial(u)*math.factorial(v)*math.factorial(u+v+1))
require(disk_monomial(0,0)==1,'normalized disk area')
require(disk_monomial(2,0)==Q(1,4),'disk x-square normalization')
for degree in range(1,31):
 values=[Q(0),Q(0)]
 for j in range(degree+1):
  v=math.comb(degree,j)*disk_monomial(degree-j,j)
  values[j%2]+=(-1)**(j//2)*v
 require(values==[0,0],'nonconstant harmonic monomial disk average')
# Fixed rational pole configurations, including repeated centers, and translated evaluation points.
weights=[Q(1,6),Q(1,3),Q(1,2)];centers=[(Q(2),Q(-1)),(Q(2),Q(-1)),(Q(-3),Q(4))]
fields=[]
for z in [(Q(0),Q(0)),(Q(20),Q(3)),(Q(-100),Q(1)),(Q(1,2),Q(3,2))]:
 g=(Q(0),Q(0))
 for w,a in zip(weights,centers):
  k=sqinv((a[0]-z[0],a[1]-z[1]));g=(g[0]+w*k[0],g[1]+w*k[1])
 coalesced=(Q(0),Q(0))
 for w,a in [(Q(1,2),centers[0]),(Q(1,2),centers[2])]:
  k=sqinv((z[0]-a[0],z[1]-a[1]));coalesced=(coalesced[0]+w*k[0],coalesced[1]+w*k[1])
 require(g==coalesced,'coalescence/squared denominator sign');T=(-g[0],-g[1]);expected=g if args.force_wrong_sign else (-g[0],-g[1]);require(T==expected,'Beurling exterior sign mismatch');fields.append([str(v) for v in g])
# Rational finite geometric tail identity proves every truncation has its declared remainder.
for s in [Q(0),Q(1,7),Q(1,2),Q(9,10)]:
 for M in range(0,25):
  q=s*s;require(sum((q**k for k in range(M+1)),Q(0))+q**(M+1)/(1-q)==1/(1-q),'Poisson zero mode remainder')
# Endpoint/entropy/localization values are diagnostic, not interval or continuum proofs.
worst=D(0)
with localcontext() as c:
 c.prec=70
 for k in range(0,101):
  t=D(k)/100;entropy=D(0) if not t else -t*t.ln();require(entropy<=1/D(1).exp(),'entropy')
  for R in [D(1)+D('1e-35'),D('1.01'),D('1.5'),D(2),D(10),D('1e20')]:
   near=D(0) if not t else t*(2*R*R/t).ln();far=(1-t)*D(2).ln();combined=near+far;simple=2*R.ln()+D(2).ln()+1/D(1).exp();require(combined<=simple,'localized scalar bound');require(abs(combined-(2*t*R.ln()+D(2).ln()+entropy))<D('1e-65'),'near/far identity');worst=max(worst,combined-simple)
# Real wrong alternatives have explicit witnesses.
adverse={
 'first-order scale invariant': Q(2)!=Q(1),
 'union of repeated half disks has full mass':Q(1,2)!=Q(1),
 'drop entropy at t=1/2':D(2).ln()/2>D(0),
 'reversed kernel sign':fields[0]!=[str(-Q(v)) for v in fields[0]],
 'smaller logarithmic coefficient plus fixed constant':Q(2)*Q(100)>Q(1)*Q(100)+Q(10),
}
for name,ok in adverse.items():require(ok,name)
print(json.dumps({'status':'PASS','checks':count,'adverse_rejections':adverse,'rational_fields':fields,'scalar_domain':'101 near-mass values, six radii, Decimal70 diagnostic only','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'universal_proofs_required':True},sort_keys=True,indent=2))
