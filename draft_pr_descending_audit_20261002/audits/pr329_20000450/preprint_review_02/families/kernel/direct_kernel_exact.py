"""Independent kernel audit from line intersection; no package imports or data inputs."""
import datetime, json
import sympy as S

x,A,B,C,b = S.symbols('x A B C beta')
f=x**3+A*x*x+B*x+C
fp=S.diff(f,x)
# Vieta for the tangent line: x2=fp^2/(4f)-A-2x.
# Write D=x2-x. Then the secant through P and 2P has squared slope
# fp^2/(4f)+2fp/D+4f/D^2, and x2-x3=D-2fp/D-4f/D^2.
Q3=S.expand(4*f*(3*x+A)-fp**2)
H6=S.expand(2*fp*Q3-16*f**2)
Q5=S.expand(16*f**2*H6-Q3**3)
checks=[]
def ck(name,a,z=0):
    d=S.cancel(a-z)
    if d != 0: raise AssertionError(name+': '+str(d))
    checks.append(name)

D=-Q3/(4*f)
ck('Vieta tangent difference',D,fp**2/(4*f)-A-3*x)
ck('Secant equality numerator identity',4*f*Q3**2*(D-2*fp/D-4*f/D**2),Q5)
b2,b4,b6,b8=4*A,2*B,4*C,4*A*C-B**2
ck('Generic psi3 expansion',Q3,3*x**4+b2*x**3+3*b4*x*x+3*b6*x+b8)
ck('Generic H6 expansion',H6,2*x**6+b2*x**5+5*b4*x**4+10*b6*x**3+10*b8*x*x+(b2*b8-b4*b6)*x+b4*b8-b6**2)
special={A:(b*b-6*b+1)/4,B:(b*b-b)/2,C:b*b/4}
T=S.expand(4*f.subs(special))
p3=S.expand(Q3.subs(special)); h=S.expand(H6.subs(special)); p5=S.expand(Q5.subs(special))
quot,rem=S.div(p5,x*(x-b),x)
ck('Marked abscissas divide fifth kernel',rem)
rows={10:5,9:5*(b*b-5*b+1),8:b**4-7*b**3+44*b*b-38*b+1,
7:b*(b**4+3*b**3-26*b*b+127*b-9),6:b*b*(b**4+3*b**3+19*b*b-248*b+36),
5:b**3*(b**4+3*b**3-71*b*b+322*b-84),4:b**4*(b**4-12*b**3+94*b*b-293*b+126),
3:5*b**5*(b**3-10*b*b+36*b-25),2:5*b**6*(2*b*b-13*b+16),1:10*b**7*(b-3),0:5*b**8}
R=sum(co*x**j for j,co in rows.items())
for j in range(11): ck('Residual coefficient x^'+str(j),S.Poly(quot,x).coeff_monomial(x**j),rows[j])
Delta=b**5*(b*b-11*b-1)
resT=S.factor(S.resultant(p5,T,x)); ck('Exact resultant with ordinate branch',resT,Delta**6)
res3=S.factor(S.resultant(p5,p3,x)); ck('Exact resultant with tripling denominator',res3,Delta**8)
ck('R(0)',R.subs(x,0),5*b**8); ck('R(beta)',R.subs(x,b),5*b**12)
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'base identities and resultants done','checks':checks},indent=2),flush=True)
# Direct resultant proves squarefreeness and the 12-abscissa count independently
# of importing a division-polynomial theorem or checking a single test curve.
disc5=S.factor(S.discriminant(p5,x))
ck('Exact universal Tate fifth-kernel discriminant',disc5,5**11*Delta**22)
assert S.degree(p5,x)==12 and S.Poly(p5,x).LC()==5
print(json.dumps({'status':'EXACT_PASS','sympy_version':S.__version__,'checks':checks,
 'mechanism':'Vieta tangent/secant equation; Q3=4f(3x+A)-fp^2; H6=2fpQ3-16f^2; Q5 from x2-x3',
 'generic_psi3':str(Q3),'generic_H6':str(H6),
 'generic_Q5_coefficients':[str(S.factor(a)) for a in S.Poly(Q5,x).all_coeffs()],
 'Tate_psi3':str(p3),'Tate_H6':str(h),
 'resultant_Q5_T':str(resT),'resultant_Q5_Q3':str(res3),
 'disc_Q5':str(disc5),'residual_coefficients':{str(j):str(S.factor(rows[j])) for j in range(11)},
 'proof_scope':'Universal exact identities over Q(beta). With the direct chord iff argument recorded in report, nonzero Delta implies 12 distinct abscissas, 24 finite points, and O; no sampled-degree inference.'},indent=2))
