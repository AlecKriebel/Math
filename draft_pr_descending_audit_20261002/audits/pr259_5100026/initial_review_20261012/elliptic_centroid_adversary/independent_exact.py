"""Exact controls built before first submitted-proof read. Python 3; SymPy 1.14."""
import json, sys, platform
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0, str(Path(__file__).resolve().parent/'vendor'))
import sympy as z

checks={}
X,Y,Z,W,f=z.symbols('X Y Z W f')
H=X*X+Z*Z+Y*Y+W*W-f*X
J=2*X*Z+2*Y*W-f*Z
d0=X*W-Y*Z
ux=(H*W-Y*J)/(d0-f*W)
paired=z.factor(ux-ux.subs(f,-f))
checks['general_Cramer_antipodal_x_identity']=z.factor(paired-2*f*(W*W-Y*Y)*(Z*Z+W*W)/(d0*d0-f*f*W*W))==0
s,p,m=z.symbols('s p m')
Q=1-m*p*s*s;D2=1-m*p;C2=1-p
checks['paired_numerator_factor']=z.expand(p*D2*s*s*(1-m*s*s)-C2*(1-s*s)-Q*(D2*s*s-C2))==0
q,c,d,F=z.symbols('q c d F')
r0=z.Matrix([s,c]);r1=z.Matrix([c/d,-q*s/d]);M=z.Matrix([F,0]);V=r0+r1;Wv=r1-r0
pair=lambda v,h:2*F*(1-F**2)*v[0]*v/(h*h-F*F*v[0]*v[0])-2*M
four=pair(V,1+r0.dot(r1))+pair(Wv,1-r0.dot(r1))
n4=[]
for e in four:
 n,den=z.together(e).as_numer_denom()
 for x,val in [(c,1-s*s),(d,1-(1-q*q)*s*s),(F,(1-q)/(1+q))]:
  n=z.rem(z.Poly(n,x),z.Poly(x*x-val,x)).as_expr()
 n4.append(z.factor(n)==0)
checks['N4_vector_polynomial_remainders']=n4
zh=(25-10*z.sqrt(5))/3;mh=z.Rational(9,25);qh=z.Rational(4,5)
a2=(1-mh*zh)/(1-mh);f2=a2-1
checks['exact_8_3_a2']=z.simplify(a2-(-25+15*z.sqrt(5))/8)==0
checks['exact_8_3_focus2']=z.simplify(f2-(-33+15*z.sqrt(5))/8)==0
checks['exact_8_3_modulus_relation']=z.simplify((a2-1)/(a2-zh)-mh)==0
checks['exact_8_3_duplication']=z.simplify(4*zh*(1-zh)*(1-mh*zh)/(1-mh*zh*zh)**2-z.Rational(5,9))==0
checks['exact_8_3_strict_domain']=bool(a2>1 and zh>0 and zh<1)
C2h=1-zh;D2h=1-mh*zh;h=z.Rational(5,9)
ratio=z.radsimp(z.simplify((-C2h+2*(D2h*h-C2h)/(1-mh*zh*h)+(D2h-C2h)/D2h)/(4*C2h)))
checks['exact_8_3_centroid_ratio']=z.simplify(ratio-(11+5*z.sqrt(5))/8)==0
checks['exact_8_3_outside_chosen_focus']=bool(ratio>1)
checks['N4_paired_x_zero']=z.factor((q*s*s-q/(1+q))/(1-(1-q)*s*s)+(q*(1-s*s)/(1-(1-q*q)*s*s)-q/(1+q))/(1-(1-q)*(1-s*s)/(1-(1-q*q)*s*s)))==0
payload={'UTC':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'sympy':z.__version__,'checks':checks,'centroid_ratio_exact':str(ratio),'all_pass':all(all(v) if isinstance(v,list) else v for v in checks.values())}
print(json.dumps(payload,indent=2))
if not payload['all_pass']:raise SystemExit(1)
