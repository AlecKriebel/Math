"""Independent exact audit controls; no author code is imported.

Moment derivation uses the algebraic R-transform inversion for a projection and
S-transform series rather than the author's colored noncrossing recursion.
Finite matrices are controls on deterministic identities, never free inputs.
"""
import sympy as s
from itertools import combinations
from collections import Counter
import json
C=Counter()
def ck(name,ok):
    if not ok:raise AssertionError(name)
    C[name]+=1
p,v,t=s.symbols('p v t',real=True)
# R_P(w)=[w-1+sqrt(1+(4p-2)w+w²)]/(2w).
# Free difference R_P(w)-R_P(-w) yields M_D(v)^2=
# [1-(2p-1)^2 v²]/(1-v²), with the branch M_D(0)=1.
M=s.sqrt((1-(2*p-1)**2*v*v)/(1-v*v)).series(v,0,7).removeO().expand()
y=[s.Integer(1),2*t,2*t-2*t*t,2*t-4*t*t+4*t**3]
for k in range(1,4):ck('projection_difference_algebraic_series',s.expand(M.coeff(v,2*k)-y[k].subs(t,p*(1-p)))==0)
for k in (1,3,5):ck('projection_difference_odd_moments',M.coeff(v,k)==0)
for pv in (0,s.Rational(1,2),1):
    expect=1/s.sqrt(1-v*v) if pv==s.Rational(1,2) else s.Integer(1)
    ck('boundary_generating_function',s.expand(M.subs(p,pv)-expect.series(v,0,7).removeO())==0)

def S_series(a1,a2,a3):
    inv1=1/a1;inv2=-a2/a1**3;inv3=2*a2*a2/a1**5-a3/a1**4
    return [inv1,inv1+inv2,inv2+inv3]
def multiply_moments(aa,bb):
    A=S_series(*aa);B=S_series(*bb)
    coeff=[s.expand(sum(A[j]*B[k-j] for j in range(k+1))) for k in range(3)]
    m1=s.cancel(1/coeff[0]);m2=s.cancel(m1**3*(1/m1-coeff[1]));m3=s.cancel(m1**4*(2*m2*m2/m1**5-m2/m1**3-coeff[2]))
    return [m1,m2,m3]
b1,b2,b3,r,ss=s.symbols('b1 b2 b3 r ss')
yraw=multiply_moments([s.Integer(2),s.Integer(6),s.Integer(20)],[b1,b2,b3])
for got,want in zip(yraw,[2*b1,4*b2+2*b1*b1,8*b3+12*b1*b2]):ck('arcsine_product_from_S',s.expand(got-want)==0)
ygen=multiply_moments([s.Integer(1),r,ss],[b1,b2,b3])
for got,want in zip(ygen,[b1,b2+(r-1)*b1*b1,b3+3*(r-1)*b1*b2+(ss-3*r+2)*b1**3]):ck('general_product_from_S',s.expand(got-want)==0)
sol={}
for b,got,want in zip([b1,b2,b3],ygen,y[1:]):sol[b]=s.expand(s.solve(s.Eq(got.subs(sol),want),b)[0])
det=s.expand(sol[b1]*sol[b3]-sol[b2]**2)
ck('universal_factor_determinant',s.expand(det-t**3*(-8*(r-1)+(32*r*r-8*r-16*ss-4)*t))==0)
ck('arcsine_normalization',s.expand(det.subs({r:s.Rational(3,2),ss:s.Rational(5,2)})-16*t**3*(t-s.Rational(1,4)))==0)
u=s.symbols('u',positive=True);z=-s.I*u
G=(1-p)/(z+p)+p/(z-(1-p))
ck('two_point_imaginary_sign',s.factor(s.im(s.simplify(z*G))-u*p*(1-p)*(2*p-1)/((u*u+p*p)*(u*u+(1-p)**2)))==0)
for denom in (7,11,19):
 for k in range(1,denom):
    pv=s.Rational(k,denom);tv=pv*(1-pv)
    ck('strict_arcsine_obstruction',tv**3*(tv-s.Rational(1,4))<0)

def block(rows):return s.BlockMatrix(rows).as_explicit()
def zero(M):return all(s.cancel(x)==0 for x in M)
def psd(M):
    for k in range(1,M.rows+1):
      for inds in combinations(range(M.rows),k):
        ck('exact_PSD_principal_minor',s.simplify(M.extract(inds,inds).det())>=0)
I=s.I;E=s.eye(3);O=s.zeros(3)
U=s.diag(1,I,-1)
q=s.Matrix([1,2,-1]);Q=E-2*q*q.T/(q.T*q)[0]
A=s.diag(s.Rational(-3,2),s.Rational(1,3),2)
B=U*Q*s.diag(-1,s.Rational(2,3),3)*Q.T*U.H
c=I*(A*B-B*A);D=A*A+B*B
ck('complex_Hermitian_inputs',A.H==A and B.H==B and c.H==c)
L=block([[O,A,B],[A,O,-I*E],[B,I*E,O]])
Qlower=block([[O,-I*E],[I*E,O]])
V=A.row_join(B)
for z in (s.Rational(2,3)+I*s.Rational(4,5),-1+2*I):
 eta=s.im(z);R0=(z*E-c).inv()
 for eps in (s.Rational(1,7),s.Rational(3,5)):
    low=(I*eps*s.eye(6)-Qlower)
    Linv=(-I*eps*s.eye(6)-Qlower)/(1+eps**2)
    ck('lower_inverse',zero(low*Linv-s.eye(6)))
    Schur=z*E-c/(1+eps**2)+I*eps*D/(1+eps**2)
    RR=Schur.inv()
    # Independent full block inverse multiplication checks its top-left block.
    inv=block([[RR,RR*V*Linv],[Linv*V.H*RR,Linv+Linv*V.H*RR*V*Linv]])
    Lambda=block([[z*E,O,O],[O,I*eps*E,O],[O,O,I*eps*E]])
    ck('full_block_inverse',zero((Lambda-L)*inv-s.eye(9)))
    ck('coercive_sign',zero((Schur-Schur.H)/(2*I)-eta*E-eps*D/(1+eps**2)))
    Diff=(RR-R0).applyfunc(s.cancel)
    ck('regularization_resolvent_identity',zero(Diff-RR*(-eps**2*c-I*eps*D)/(1+eps**2)*R0))
    bound=(2*eps**2*2*3+eps*(4+9))/((1+eps**2)*eta**2)
    psd((bound**2*E-Diff.H*Diff).applyfunc(s.cancel))
# New five-dimensional outlier family with nontrivial rank fraction <1.
E=s.eye(5);q=s.Matrix([1,2,3,1,-1]);Q=E-2*q*q.T/(q.T*q)[0]
av=[s.Rational(-1,2),0,s.Rational(1,3),1,20];bv=[-1,s.Rational(-1,2),0,s.Rational(1,2),1]
A=s.diag(*av);B=Q*s.diag(*bv)*Q.T;c=I*(A*B-B*A)
rank_cases=[]
for T in (s.Integer(1),s.Integer(2),s.Integer(30)):
 clip=lambda x:max(-T,min(x,T))
 AT=s.diag(*map(clip,av));BT=Q*s.diag(*map(clip,bv))*Q.T;ct=I*(AT*BT-BT*AT)
 qa=s.Rational(sum(int(bool(abs(x)>T)) for x in av),5);qb=s.Rational(sum(int(bool(abs(x)>T)) for x in bv),5);delta=min(1,2*(qa+qb))
 rank=s.Rational((c-ct).rank(),5);rank_cases.append({'T':int(T),'delta':str(delta),'actual_rank':str(rank)})
 ck('strict_clipping_support',s.Rational((A-AT).rank(),5)==qa and s.Rational((B-BT).rank(),5)==qb)
 ck('commutator_rank',rank<=delta)
 ck('decomposition',zero(c-ct-I*((A-AT)*B-B*(A-AT)+AT*(B-BT)-(B-BT)*AT)))
 for z in (I,s.Rational(3,2)+s.Rational(2,3)*I):
    eta=s.im(z);R=(z*E-c).inv();RT=(z*E-ct).inv();V=(R-RT).applyfunc(s.cancel)
    ck('affiliated_identity_finite_control',zero(V-R*(c-ct)*RT))
    ck('resolvent_rank_control',s.Rational(V.rank(),5)<=rank)
    trace=s.cancel(s.trace(V)/5)
    ck('tail_Cauchy_bound',s.simplify(trace*s.conjugate(trace))<=(2*delta/eta)**2)
ck('nontrivial_rank_family',any(s.Rational(x['delta'])>0 and s.Rational(x['delta'])<1 for x in rank_cases))
print(json.dumps({'status':'PASS_INDEPENDENT_EXACT_CONTROLS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'rank_cases':rank_cases,'scope':'Analytic R/S-transform series and different rational Hermitian matrices; no author imports, no claim of finite-matrix freeness or formal infinite-dimensional proof.'},indent=2,sort_keys=True))
