"""All-dimension contraction by polynomial division in the chain index.

No project verifier is imported. The 4x4 second-harmonic boundary system is
solved symbolically, then each interior contraction is divided into a polynomial
in i and a single reciprocal term. This gives a separate derivation of the
formal harmonic-sum bridge, including the rescaled mass gauge.
"""
from pathlib import Path
import datetime,json,hashlib
import sympy as s
R=s.Rational
m,i,h,L,u=s.symbols('m i h L u')
nu=m-2
K=lambda j:91*m-181-j
sig=1/(126*nu)
r1=s.Integer(1); r2=-K(2)/(63*nu); rl=-K(m-1)/(63*nu); rm=-R(2,9); rz=R(5,14)
e1=-R(266,815); e2=78260*nu/(163*K(1)); em=R(18368,7335)
scale=78260*nu/163
tests=[]
def zero(name,expr):
    assert s.cancel(expr)==0,(name,s.factor(expr))
    tests.append(name)
def Bboundary(w1,w2,wl,wm,wz):
    return s.Matrix([-(wl+rl*w1)+2*rz*wz-(wm+rm*w1),-(w2+r2*w1)+2*rm*wm,2*(wl+rl*w1)-4*rm*wm+2*rz*wz-(wm+rm*w1),-4*rz*wz+2*(wm+rm*w1)])
b=-Bboundary(1,r2,rl,rm,rz)/4
w01=(182448*m-373417)/(31752*(8*m-17))
w02=(1008*m*m-20459*m+37138)/(31752*nu*(8*m-17))
w0i=w02-(i-2)*sig; w0l=w0i.subs(i,m-1); w0m=-R(1,81); w0z=(16861*m-34044)/(7938*(8*m-17))
B0=s.Matrix([[-2,-1,-1,2],[-1,-1,2,0],[1,2,-5,2],[2,0,2,-4]])
for k,val in enumerate(B0*s.Matrix([w01,w0l,w0m,w0z])-s.Matrix([b[0],b[1]+w02-w0l,b[2],b[3]])):
    zero('zero harmonic boundary '+str(k),val)
zero('zero harmonic physical mass',4*s.summation(w0i,(i,2,m-1))+2*w0m+w0z)
zero('zero harmonic interior',w0i.subs(i,i-1)-w0i-sig)
T=lambda j:s.prod(K(j-k) for k in range(4))/s.prod(K(k) for k in range(-1,3))
tl=s.factor(T(m-1));delta=sig*(tl*K(2)-K(m-1))/3
M=s.Matrix([[-R(218,63),-tl,-1,2],[-1,-(1+4/K(2)),2,0],[1,2*tl,-R(39,7),2],[2,0,2,-R(244,45)]])
rhs=b+s.Matrix([delta,0,-2*delta,0])
print('solving generic boundary system',flush=True)
W=M.inv(method='DM')*rhs
W=[s.cancel(v) for v in W]; w21,w22,w2m,w2z=W
for k,val in enumerate(M*s.Matrix(W)-rhs):zero('second harmonic boundary '+str(k),val)
w2i=T(i)*(w22+sig*K(2)/3)-sig*K(i)/3
zero('second harmonic first index',w2i.subs(i,2)-w22)
zero('second harmonic recurrence',w2i.subs(i,i-1)-(1+4/K(i))*w2i-sig)
Q=589180301*m**3-3500015940*m**2+6930529579*m-4574434500
zero('boundary determinant',M.det()-64*Q/(6615*(91*m-183)*(91*m-181)*(91*m-180)))

def chain_sum(wi,w1):
    integrand=s.cancel(scale*(wi.subs(i,i-1)-wi-w1/(63*nu))/K(i-1))
    numerator,denominator=s.fraction(integrand)
    quotient,remainder=s.div(numerator,denominator,i)
    coefficient=s.cancel(remainder*K(i-1)/denominator)
    assert i not in coefficient.free_symbols
    zero('index polynomial division',integrand-quotient-coefficient/K(i-1))
    # i=3..m-1 corresponds precisely to reciprocal K_2..K_(m-2).
    return s.factor(s.summation(quotient,(i,3,m-1))+coefficient*(h-1/K(1)))

def contraction(w1,wsecond,wi,wm,wz):
    bb=Bboundary(w1,wsecond,wi.subs(i,m-1),wm,wz)
    return s.factor(e1*bb[0]+e2*bb[1]+em*bb[2]+bb[3]+chain_sum(wi,w1))
print('reducing rational interior sums',flush=True)
N=s.factor(contraction(w01,w02,w0i,w0m,w0z)+contraction(w21,w22,w2i,w2m,w2z)/2)
PR=68605040480814208768*m**4-550882186169626030957*m**3+1658612632937449670852*m**2-2219226476204103501323*m+1113379274975809565700
PC=652054120726848*m**4-5151971981328467*m**3+15265080924982572*m**2-20102347725659113*m+9927281930180400
Rt=PR/(286118780220*(8*m-17)*Q);Ct=-215*PC/(11645046*(8*m-17)*Q)
zero('all-dimension cubic numerator R+C*h',N-Rt-Ct*h)
S=contraction(s.Integer(2),s.Integer(-2),s.Integer(-2),s.Integer(0),s.Integer(1))
zero('gauge contraction',S+4*(1760850*h-10253)/462105)
for name,p in [('Q',Q),('PR',PR),('PC',PC)]:
    assert all(c>0 for c in s.Poly(s.expand(p.subs(m,u+3)),u).all_coeffs());tests.append('positive shifted '+name)
Hup=(m-2)/(90*m-179)
for name,expr in [('N positive',Rt+Ct*Hup),('N margin >1/100',Rt+Ct*Hup-R(1,100))]:
    p,q=s.fraction(s.cancel(expr));
    assert all(c>0 for c in s.Poly(s.expand(p.subs(m,u+3)),u).all_coeffs())
    assert all(c>0 for c in s.Poly(s.expand(q.subs(m,u+3)),u).all_coeffs());tests.append(name)

# Obtain the weighted zero-mode mass from the reciprocal-index sum directly.
weighted=s.cancel(L*K(i-1)/K(i)*w0i)
num,den=s.fraction(weighted);qt,rem=s.div(num,den,i)
coeff=s.cancel(rem*K(i)/den);assert i not in coeff.free_symbols
Hshift=h-1/K(1)+1/K(m-1)
mass=s.factor(4*(s.summation(qt,(i,2,m-1))+coeff*Hshift)+2*w0m+w0z)
massrho=1-8*L*(nu+Hshift)
tau=s.factor(-mass/massrho)
At=1494249120*h*L*nu**2-69786990*h*L*nu+108738630*L*nu**2+1214388*L*nu-8521*L-125249670*nu**2+1031940*nu
Bt=32760*h*L*nu+32760*L*nu**2+4*L-4095*nu
zero('mass gauge closed formula',tau+At/(15876*(8*nu-1)*Bt))
zero('tau derivative in h',s.diff(tau,h)+4225*L*nu**2*(182448*L*nu+1008*L-7513)/(2*Bt**2))
zero('tau derivative in L',s.diff(tau,L)+65*nu*(-61531470*h*nu+125249670*nu**2+1031940*nu-7513)/(252*Bt**2))
here=Path(__file__).resolve().parent
result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks_passed':len(tests),'checks':tests,'all_dimension_route':'Polynomial division of the chain-index rational contraction; symbolic boundary solve; formal harmonic sum then exact sign bounds.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(here/'generic-cubic-division.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS generic division',len(tests),flush=True)
