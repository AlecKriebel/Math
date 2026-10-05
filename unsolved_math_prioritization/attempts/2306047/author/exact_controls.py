#!/usr/bin/env python3
"""Authored algebraic controls, not a formal proof of univalence or extremality.
Requires SymPy. No downloads, private inputs, or source files are used.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import sympy as s

checks = []
def check(name, condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)

z,w,a,x,c = s.symbols('z w a x c', nonzero=True)
a2,a3,a4 = s.symbols('a2 a3 a4')
k = lambda t:t/(1-t)**2
check('Koebe collision factorization', s.simplify(k(z)-k(w)-(z-w)*(1-z*w)/((1-z)**2*(1-w)**2)) == 0)
p = z+2*a*(1/(1-z)+s.log(1-z)-1)
check('primitive derivative', s.simplify(s.diff(p,z)-1-2*a*k(z)) == 0)
for n in range(2,9):
    check('primitive coefficient n='+str(n), s.expand(s.series(p,z,0,9).removeO()).coeff(z,n)==2*a*(n-1)/n)
num = z*z+s.Rational(8,5)*z+1
for sign in [-1,1]:
    root=-s.Rational(4,5)+sign*3*s.I/5
    check('boundary zero '+str(sign), s.simplify(num.subs(z,root))==0 and s.simplify(root*s.conjugate(root))==1)

f = z+a2*z*z+a3*z**3+a4*z**4
inv = s.series(z/f,z,0,4).removeO()
check('area theorem first coefficient', s.expand(inv).coeff(z,2)==a2*a2-a3)
check('derivative normalized second coefficient', s.expand((s.diff(f,z)-1)/(2*a2)).coeff(z,2)==3*a3/(2*a2))
C=(2+s.sqrt(13))/3
check('quadratic constant exact', s.simplify(C*C-4*C/3-1)==0)
check('C greater than 9/5', C>s.Rational(9,5))

G=-z/3-s.Rational(4,3)*s.log(1-z)
check('convex model derivative', s.simplify(s.diff(G,z)-(1+z/3)/(1-z))==0)
check('convex model criterion', s.simplify(1+z*s.diff(G,z,2)/s.diff(G,z)-(1+z/(1-z)+z/(3+z)))==0)
for n in range(2,9):
    bn=s.expand(s.series(G,z,0,9).removeO()).coeff(z,n)
    check('convex model coefficient n='+str(n),bn==s.Rational(4,3*n))
    check('reject printed sharpness value n='+str(n),bn!=s.Rational(4*n,3))

Q=sum(2*x*(-1)**j*z**(2*j+1)/s.Integer(2*j+1)**2 for j in range(4))
H=s.series(s.exp(Q),z,0,7).removeO()
FP=s.expand(s.series((1+z)/(1-z)**2,z,0,7).removeO()*H)
known={2:s.Rational(3,2)+x,3:s.Rational(5,3)+2*x+2*x*x/3,
       4:s.Rational(7,4)+22*x/9+3*x*x/2+x**3/3}
for n,v in known.items():check('candidate coefficient n='+str(n),s.expand(FP.coeff(z,n-1)/n-v)==0)

E=z-(s.exp(2*s.I*z)-1-2*s.I*z)/40
TE=z+(1-s.cos(2*z))/40
check('entire example normalization',E.subs(z,0)==0 and s.diff(E,z).subs(z,0)==1)
check('entire example second derivative',s.simplify(s.diff(E,z,2)-s.exp(2*s.I*z)/10)==0)
check('entire example positive real a2',s.diff(E,z,2).subs(z,0)/2==s.Rational(1,20))
check('entire example a3 nonreal',s.diff(E,z,3).subs(z,0)/6==s.I/30)
reflected=z-(s.exp(-2*s.I*z)-1+2*s.I*z)/40
check('conjugate averaging formula',s.simplify(s.expand_trig((E+reflected)/2-TE).rewrite(s.exp))==0)
check('averaging preserves a2',s.diff(TE,z,2).subs(z,0)/2==s.Rational(1,20))
check('average derivative has interior critical point',s.diff(TE,z,2).subs(z,s.pi/4)==0)

# For 0<=t<=1, an alternating atan series lies between consecutive partial sums.
def atan_interval(t,terms=24):
    total=sum(((-1)**j*t**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
    next_total=total+(-1)**terms*t**(2*terms+1)/F(2*terms+1)
    return min(total,next_total),max(total,next_total)
lo5,hi5=atan_interval(F(1,5));lo239,hi239=atan_interval(F(1,239))
pi_lo,pi_hi=16*lo5-4*hi239,16*hi5-4*lo239
check('pi lower bound for collision threshold',pi_lo>F(28,9))
check('pi between 3 and 4 for periodicity and interior zero',3<pi_lo and pi_hi<4)

def J_interval(r):
    lo,hi=atan_interval((1-r)/(1+r))
    atan_lo,atan_hi=pi_lo/4-hi,pi_hi/4-lo
    center=r+F(18,5)*r/(1+r*r)
    return center-F(18,5)*atan_hi,center-F(18,5)*atan_lo
jl=J_interval(F(19,20));jr=J_interval(F(49,50))
check('collision function positive at 19/20',jl[0]>0)
check('collision function negative at 49/50',jr[1]<0)
# e^2: positive series and a geometric bound on the tail after k=10.
term=F(1);total=term
for j in range(1,11):term*=F(2,j);total+=term
next_term=term*F(2,11)
e2_upper=total+next_term/(1-F(2,12))
check('exact e squared bound',e2_upper<8)
check('positive-real-part margin', (e2_upper+1)/20<F(9,20)<1)
check('reject non-normalized derivative using A2',s.diff((s.diff(f,z)-1)/(2*C),z).subs(z,0).subs(a2,1)!=1)

output={
    'status':'passed', 'checks_passed':len(checks),'checks':checks,
    'sympy_version':s.__version__,
    'exact_interval_controls':{
      'pi_lower':str(pi_lo),'pi_upper':str(pi_hi),
      'J_19_over_20_lower':str(jl[0]),'J_49_over_50_upper':str(jr[1]),
      'e_squared_upper':str(e2_upper)},
    'proof_limits':'Algebra and rational interval controls only. Analytic injectivity arguments are in PROOF_PARTIALS.md. No sharp coefficient maximum is certified.'}
path=Path(__file__).with_name('EXACT_RESULTS.json')
path.write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'status':output['status'],'checks_passed':len(checks),'sympy_version':s.__version__}))
