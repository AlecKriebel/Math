#!/usr/bin/env python3
"""Independent exact checks for pass 3; analytic arguments remain in the audit."""
import hashlib,json
from pathlib import Path
import sympy as S
root=Path(__file__).resolve().parents[1]
checks=[]
def check(name,expr):
 assert expr,name
 checks.append({'name':name,'passed':True})
m,b,c=S.symbols('m b c',real=True)
s=m+b+c; gamma=s-3; eta=2*(3*m+b+2*c-6)
check('tied minimum forces positive eta',S.expand(eta.subs(b,m)-4*(s.subs(b,m)-3))==0)
check('eta rewriting',S.expand(eta-2*(s+2*m+c-6))==0)
base=5*m-6
check('gradient correction gap',S.expand(3*m+2*b-6-base-2*(b-m))==0)
check('cofactor correction gap',S.expand(2*m+3*b-6-base-3*(b-m))==0)
check('determinant square gap',S.expand(gamma+b+c-3-base-(2*s-6*m))==0)
check('barrier correction gap',S.expand(b+c-3-3*gamma-base-2*(6-s-3*m))==0)
check('spherical scalar coefficient',S.expand(m*(2+5*(m-1))-m*(5*m-3))==0)
check('critical scalar exponent',S.solve(5*m-3,m)==[S.Rational(3,5)])
check('admissible residual exponent example',eta.subs({m:S.Rational(3,5),b:S.Rational(5,4),c:S.Rational(5,4)})==-S.Rational(9,10))
check('residual example sum',s.subs({m:S.Rational(3,5),b:S.Rational(5,4),c:S.Rational(5,4)})==S.Rational(31,10))
for H in [S.diag(2,3,4),S.Matrix([[1,1,0],[0,2,1],[1,0,3]]),S.Matrix([[2,1,-1],[1,3,0],[0,2,2]])]:
 K=H.det(); F=H.inv(); C=H.cofactor_matrix()
 check('inverse weak-derivative matrix identity '+str(K),C.T/K==F)
 check('transported cofactor matrix identity '+str(K),C/K==F.T)
 check('inverse determinant identity '+str(K),F.det()==1/K)
check('inverse gradient coercivity powers',3*S.Rational(3,5)==S.Rational(9,5) and -2*S.Rational(3,5)+3*S.Rational(2,5)==0)
check('inverse cofactor coercivity powers',6*S.Rational(3,8)==S.Rational(9,4) and -5*S.Rational(3,8)+3*S.Rational(5,8)==0)
metadata=json.loads((root/'counterexample/SOURCE_METADATA.json').read_text())
data=(root/'counterexample/private_sources/uhlenbeck1977.pdf').read_bytes()
check('Uhlenbeck primary PDF bytes and hash',len(data)==metadata['bytes'] and hashlib.sha256(data).hexdigest()==metadata['sha256'])

u,v=S.symbols('u v',positive=True)
check('barrier midpoint coercivity remainder', S.factor(u**-2+v**-2-8/(u+v)**2-(1/u-1/v)**2-2*(u-v)**2/(u*v*(u+v)**2))==0)
check('relative barrier exact identity', S.factor(u**-2-v**-2+2*v**-3*(u-v)-(u-v)**2*(2*u+v)/(v**3*u**2))==0)
r=S.symbols('r',positive=True)
check('ordinary primal conjugate threshold',S.simplify(5/(6*r+3)+3/(2*r+1)-1-(11-6*r)/(3*(2*r+1)))==0)
check('ordinary inverse duality threshold',S.Rational(6,7)+S.Rational(1,7)==1)
x,y,z=S.symbols('x y z',positive=True)
a,bcoef,c,d=S.symbols('a bcoef c d',positive=True)
Sum=x+y+z; Pair=x*y+x*z+y*z
Ui=6*a*Sum**2*x+3*bcoef*S.sqrt(Pair)*x*(Sum-x)+2*c*x*y*z
Uj=6*a*Sum**2*y+3*bcoef*S.sqrt(Pair)*y*(Sum-y)+2*c*x*y*z
check('principal constitutive stress gap',S.simplify(Ui-Uj-(x-y)*(6*a*Sum**2+3*bcoef*S.sqrt(Pair)*z))==0)
t,e,rx,ry=S.symbols('t e rx ry',real=True,positive=True)
R=S.Matrix([[rx,ry,0],[0,0,0],[0,0,0]])
F=t*S.eye(3)+e*R
C=F.cofactor_matrix(); J=F.det()
W=a*sum(q*q for q in F)**3+bcoef*sum(q*q for q in C)**S.Rational(3,2)+c*J**2+d/J**2
stiff=S.diff(W,e,2).subs(e,0)
expected=(54*a+3*S.sqrt(3)*bcoef)*t**4*(rx**2+ry**2)+((72*a+7*S.sqrt(3)*bcoef+2*c)*t**4+6*d*t**-8)*rx**2
check('general rank-one stiffness at tI',S.simplify(stiff-expected)==0)
metadata2=json.loads((root/'literature/SOURCE_INSPECTION_MANIFEST.json').read_text())['sources'][2]
data2=(root/'literature/private_sources/barchiesi_henao_mora_rodiac2024v2.pdf').read_bytes()
check('area formula primary PDF bytes and hash',len(data2)==metadata2['bytes'] and hashlib.sha256(data2).hexdigest()==metadata2['sha256'])

result={'purpose':'Exact algebra and primary-source metadata checks supporting the independent written audit.', 'checks':checks,'total_checks':len(checks),'benchmark_proved':False,'benchmark_counterexample':False}
p=Path(__file__).with_name('AUDIT_CHECKS.json');p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'total_checks':len(checks)},indent=2))
