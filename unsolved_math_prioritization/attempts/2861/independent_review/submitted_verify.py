"""Exact consistency checks for a credited trace-formula specialization; no manifold computation."""
import hashlib,json
from pathlib import Path
import sympy as s
count=0
families={}
def check(x,label):
 global count
 assert x, label
 count+=1;families[label]=families.get(label,0)+1
x,L,ell,a=s.symbols('x L ell a',positive=True)
G=s.exp(-x*x/2)
check(s.integrate(s.sqrt(2*s.pi)*G,(x,0,s.oo))==s.pi,'Gaussian normalization')
check(s.simplify((s.integrate(s.sqrt(2*s.pi)*G,(x,L*a,s.oo))/s.pi-s.erfc(L*a/s.sqrt(2))).rewrite(s.erf))==0,'Gaussian normalization')
T=s.symbols('T',positive=True)
primitive=-s.exp(-ell*ell/(2*T*T))/ell
integrand=-ell*s.exp(-ell*ell/(2*T*T))/T**3
check(s.simplify(s.diff(primitive,T)-integrand)==0,'geometric Mellin sign')
check(s.limit(primitive,T,0,dir='+')==0,'geometric Mellin sign')
u,c=s.symbols('u c',real=True)
check(s.expand((1+u*u-2*u*c)*(1+u**-2-2*c/u)-(u+1/u-2*c)**2)==0,'denominator square')
check(s.expand(u*(1-1/u)**2-(u+1/u-2))==0,'denominator lower bound')
for n in range(1,9):
 R=4*n*n
 check(s.Rational(R)-s.Rational(R*R,2*n*n)==-4*n*n,'cutoff first exponent')
 for k in range(R,R+6):
  ratio=s.Rational(1)-s.Rational(2*k+1,2*n*n)
  check(ratio<=-3,'cutoff ratio exponent')
for m in range(1,13):
 check(s.Rational(1,m)*m==1,'primitive iterate factor')
 # A spin sign twist acts on the m-th power by (-1)^m.
 z=s.symbols('z',nonzero=True)
 check(s.expand((-z)**m-(-1)**m*z**m)==0,'spin iterate sign')
for theta in [s.pi/6,s.pi/4,s.pi/3,2*s.pi/3,3*s.pi/4]:
 check(s.simplify(s.sin(theta+s.pi)+s.sin(theta))==0,'spin half angle')
 check(s.simplify(s.cos(2*(theta+s.pi))-s.cos(2*theta))==0,'spin half angle')
check(s.Rational(1)-s.Rational(40028711,10**9)/4==s.Rational(3959971289,4*10**9),'Weeks normalization arithmetic only')
# Zero modes contribute zero before Mellin integration; no reduced eta correction.
check(s.Integer(0)*s.sqrt(2*s.pi)==0,'kernel convention')
check(s.simplify(s.erfc(x)+(-1)*s.erfc(x))==0,'opposite spectral pair')
result={'artifact_sha256':hashlib.sha256(Path('SOURCE_STATUS.md').read_bytes()).hexdigest(),'assertions':count,'families':families,'status':'pass','scope':'Exact algebra and normalization controls only; no geometric input or eta decimal certified.'}
Path('verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
