#!/usr/bin/env python3
"""Exact finite controls for the authored partial results; requires SymPy.

No network, input corpus, source PDF, floating-point solver, or private file is used.
This is not a formal proof-assistant verification of the universal arguments.
"""
import hashlib
import itertools
import json
from pathlib import Path
import sympy as S

ROOT=Path(__file__).resolve().parent
count=0
sections={}
def check(condition, label):
    global count
    if not bool(condition):
        raise AssertionError(label)
    count += 1

def zero(poly, label):
    check(S.expand(poly)==0,label)

def finish(name, start):
    sections[name]=count-start

t,eps,c=S.symbols('t eps c')
x=S.symbols('x0:5')
E=[S.Integer(1)]+[sum(S.prod(z) for z in itertools.combinations(x,k)) for k in range(1,6)]
p=4500*E[5]-220*E[1]*E[4]+7*E[1]**2*E[3]
e=[1]*5
w=[6,1,1,1,1]
def D(q,v): return sum(v[i]*S.diff(q,x[i]) for i in range(5))
def delta(f,d): return S.expand(t*S.diff(f,t)-(d-1)*f)

start=count
G=S.expand((t-1)**2*(t-2)**2*(t+6))
F=t**5+23*t**3-33*t**2+S.Rational(68,3)*t-6
H=F/t**4
zero(delta(F+c*t**4,5)-G,'all inverse symbols')
zero(S.diff(H,t)-G/t**5,'critical-value derivative')
check(H.subs(t,1)==S.Rational(23,3),'critical value one')
check(H.subs(t,2)==S.Rational(185,24),'critical value two')
check(H.subs(t,2)-H.subs(t,1)==S.Rational(1,24),'nonzero obstruction gap')
for n in range(2,11):
    zero(delta((t-1)**n,n)-(t-1)**(n-1)*(t+n-1),f'delta g0 n={n}')
    for k in range(n+1):
        zero(delta(t**(n-k),n)-(1-k)*t**(n-k),f'diagonal delta n={n}, k={k}')
# Independent direct computation of the operator sign from its definition.
zero(p.subs(dict(zip(x,[1-t,1-t,1-t,1-t,-4-t])))+750*G,'associated-symbol sign')
finish('inverse_symbol',start)

start=count
W=S.expand(D(p,e)*D(p,w)-p*D(D(p,e),w))
zero(p.subs({x[i]:w[i]+t for i in range(5)})-750*t**2*(t+1)**2*(t+8),'cone boundary line')
a,b,z=S.symbols('a b c')
certs=json.loads((ROOT/'SLICE_GRAM_CERTIFICATES.json').read_text())
specs={
 'symmetric':({x[0]:0,x[1]:a,x[2]:b,x[3]:z,x[4]:0},49*(a+b+z)**2),
 's4slice':({x[0]:a,x[1]:b,x[2]:z,x[3]:z,x[4]:z},9*(a+b-7*z)**2)
}
for name,(sub,fac) in specs.items():
    cert=certs[name]
    mons=S.Matrix([S.sympify(v,locals={'a':a,'b':b,'c':z}) for v in cert['monomials']])
    Q=S.Matrix([[S.Rational(v) for v in row] for row in cert['matrix']])
    check(Q==Q.T,name+' symmetry')
    zero(W.subs(sub)-fac*(mons.T*Q*mons)[0],name+' exact polynomial identity')
    J=cert['positive_principal_indices']
    for i in range(1,len(J)+1):
        v=Q.extract(J[:i],J[:i]).det()
        check(v==S.Rational(cert['leading_principal_minors'][i-1]),name+' saved exact minor')
        check(v>0,name+' positive leading minor')
    check(Q.rank()==cert['rank']==len(J),name+' full-rank positive block')
    # Exact Schur factorization, a second route to PSD.
    P=Q.extract(J,J)
    B=Q[:,J]
    zero_matrix=Q-B*P.inv()*B.T
    check(zero_matrix==S.zeros(Q.rows),name+' exact PSD congruence identity')
finish('quintic_sos_restrictions',start)

start=count
Ge=S.expand(G+eps*t*S.diff(G,t))
Fe=S.expand(F+eps*t*S.diff(F,t))
C=(1+5*eps)*t**3+(3+15*eps)*t**2-(16+34*eps)*t+12
zero(Ge-(t-1)*(t-2)*C,'deformed symbol factorization')
zero(delta(Fe+c*t**4,5)-Ge,'deformed full inverse-symbol family')
check(C.subs(t,0)==12,'cubic at zero')
zero(C.subs(t,1)+14*eps,'cubic at one')
zero(C.subs(t,2)-32*eps,'cubic at two')
He=Fe/t**4
zero(He-(1+4*eps)*H-eps*t*S.diff(H,t),'deformed critical function')
zero(He.subs(t,1)-(1+4*eps)*S.Rational(23,3),'deformed first minimum')
zero(He.subs(t,2)-(1+4*eps)*S.Rational(185,24),'deformed second minimum')
c2=-(1+4*eps)*S.Rational(185,24)
Qe=((24+120*eps)*t**3-(89+260*eps)*t**2+(100+136*eps)*t-36)/24
zero(Fe+c2*t**4-(t-2)**2*Qe,'endpoint inverse factorization')
Dep=167620*eps**3-8871*eps**2+2820*eps-752
zero(S.discriminant(Qe,t)-(4*eps+1)*Dep/5184,'exact threshold discriminant')
check(S.discriminant(S.diff(Dep,eps),eps)==-5357482236,'strict monotonicity discriminant')
check(Dep.subs(eps,0)<0,'negative starting threshold polynomial')
check(Dep.subs(eps,S.Rational(1467,10000))<0,'rational threshold lower isolator')
check(Dep.subs(eps,S.Rational(1468,10000))>0,'rational threshold upper isolator')
check(Dep.subs(eps,S.Rational(1,7))<0,'one seventh nonextendable control')
check(Dep.subs(eps,S.Rational(1,6))>0,'one sixth extendable control')
zero(((t-1)**5+eps*t*S.diff((t-1)**5,t))-(t-1)**4*((1+5*eps)*t-1),'Euler preserver symbol')
pe=p+eps*E[1]*D(p,e)/5
pe_hook=4500*E[5]+(-220+680*eps)*E[1]*E[4]+(7-74*eps)*E[1]**2*E[3]+S.Rational(21,5)*eps*E[1]**3*E[2]
zero(pe-pe_hook,'deformation remains hook-shaped')
zero(pe.subs(dict.fromkeys(x,1))-750*(1+5*eps),'nonzero value at e')
zero(pe.subs(dict(zip(x,[1-t,1-t,1-t,1-t,-4-t])))+750*Ge,'deformed operator computed from p')
finish('exact_extension_threshold',start)

start=count
# Lorentz null-pair SOS identity, with c^2+s^2=1 reduced algebraically.
z0,z1,z2,z3,cc,ss=S.symbols('z0 z1 z2 z3 cc ss')
quad=z0**2-z1**2-z2**2-z3**2
expr=4*(z0-cc*z1-ss*z2)*(z0-cc*z1+ss*z2)-4*ss**2*quad
claimed=4*((cc*z0-z1)**2+ss**2*z3**2)
check(S.rem(S.Poly(S.expand(expr-claimed),cc),S.Poly(cc**2+ss**2-1,cc)).as_expr()==0,'Lorentz SOS identity')
# Exact polynomial product rule on nontrivial sample forms, directions and powers.
for i in range(1,5):
    f=(x[0]+2*x[1]+x[2])**i
    q=x[0]**2-x[1]**2-2*x[2]**2
    u=[i,1,2,0,0];v=[i+1,2,-1,0,0]
    Wf=D(f,u)*D(f,v)-f*D(D(f,u),v)
    Wq=D(q,u)*D(q,v)-q*D(D(q,u),v)
    Wprod=D(f*q,u)*D(f*q,v)-f*q*D(D(f*q,u),v)
    zero(Wprod-q*q*Wf-f*f*Wq,f'product identity degree={i}')
for n in range(2,9):
    for aa in [1,2,5]:
        for bb in [0,1,3]:
            rr=S.sqrt(S.Rational(bb*n*(n-1),aa))
            zero(delta(aa*(t-rr)**2,2)-(aa*t*t-bb*n*(n-1)),f'quadratic extension n={n},a={aa},b={bb}')
finish('quadratic_and_product_controls',start)

start=count
# Use the rational basis [e_i-e_n] for e-perp. Its determinant identity is e_{n-1},
# since orthonormalization changes determinant by det(B^T B)=n.
for n in range(2,7):
    ys=S.symbols('y:'+str(n))
    Br=S.zeros(n,n-1)
    for i in range(n-1):Br[i,i]=1;Br[n-1,i]=-1
    Ar=Br.T*S.diag(*ys)*Br
    enm1=sum(S.prod(a)for a in itertools.combinations(ys,n-1))
    zero(Ar.det(method='domain-ge')-enm1,f'penultimate determinant n={n}')
    check((Br.T*Br).det()==n,f'basis normalization n={n}')
# An exact noncommuting-pencil adjugate/trace check with PSD direction matrices.
r,s0,h=S.symbols('r s h')
A=S.Matrix([[r,s0],[s0,h]])
U=S.Matrix([[2,1],[1,1]]);V=S.Matrix([[1,-1],[-1,3]])
P=A.det();coords=[r,s0,h]
def dir2(q,M):return sum(v*S.diff(q,z)for v,z in zip([M[0,0],M[0,1],M[1,1]],coords))
WW=dir2(P,U)*dir2(P,V)-P*dir2(dir2(P,U),V)
zero(WW-S.trace(A.adjugate()*U*A.adjugate()*V),'noncommuting determinant Wronskian')
finish('determinantal_controls',start)

result={'status':'PASS','exact_assertions':count,'sections':sections,
        'dependencies':{'sympy':S.__version__},
        'interpretation':'Finite exact identity and certificate checks support the written partial proofs; they do not solve the full conjecture.',
        'threshold_isolating_interval':['1467/10000','1468/10000'],
        'slice_certificate_sha256':hashlib.sha256((ROOT/'SLICE_GRAM_CERTIFICATES.json').read_bytes()).hexdigest()}
print(json.dumps(result,indent=2))
