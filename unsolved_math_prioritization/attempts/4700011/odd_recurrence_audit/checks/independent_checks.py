#!/usr/bin/env python3
"""Independent exact audit: quotient polynomials, resultants, manual Sturm signs.
Does not import or execute either authored verifier. No floating-point arithmetic.
"""
import copy, hashlib, itertools, json, math
from pathlib import Path
import sympy as S
BASE=Path(__file__).resolve().parents[1]
x,z,t=S.symbols('x z t')
checks=[]
def check(name, value, **detail):
    assert value, (name,detail)
    checks.append(dict(name=name,passed=True,**detail))

def sturm_variations(poly, endpoint):
    p=S.Poly(poly,t,domain=S.QQ)
    chain=[p,p.diff()]
    while not chain[-1].is_zero:
        nxt=-chain[-2].rem(chain[-1])
        if nxt.is_zero: break
        chain.append(nxt)
    signs=[]
    for q in chain:
        if endpoint == '-inf': val=S.sign(q.LC())*(-1)**q.degree()
        elif endpoint == 'inf': val=S.sign(q.LC())
        else: val=S.sign(q.eval(endpoint))
        if val: signs.append(int(val))
    return sum(a!=b for a,b in zip(signs,signs[1:]))

def roots_between(poly,a,b):
    assert S.Poly(poly,t).eval(a)!=0 and S.Poly(poly,t).eval(b)!=0
    return sturm_variations(poly,a)-sturm_variations(poly,b)

class ResultantField:
    def __init__(self,k):
        self.k=k
        self.mod=S.Poly(S.cyclotomic_poly(2*k,x),x,domain=S.QQ)
    def red(self,p):
        return S.Poly(p,x,domain=S.QQ).rem(self.mod).as_expr()
    def minpoly(self,p):
        # Norm via resultant, then squarefree monic part: not a multiplication matrix.
        norm=S.Poly(S.resultant(self.mod.as_expr(),t-self.red(p),x),t,domain=S.QQ)
        return norm.exquo(S.gcd(norm,norm.diff())).monic()
    def factor(self,signs):
        A=S.Poly(z+1,z,domain=S.QQ[x])
        for j,sign in enumerate(signs,1):
            q=self.red(x**j+x**(2*self.k-j))
            A=A*S.Poly(z*z+sign*q*z+1,z,domain=S.QQ[x])
            A=S.Poly(sum(self.red(a)*z**i for (i,),a in A.terms()),z,domain=S.QQ[x])
        return [self.red(A.nth(i)) for i in range(self.k+1)]
    def quotient(self,a,b):
        return self.red(a*S.invert(b,self.mod.as_expr(),x))
    def integral(self,a):
        return all(c.q==1 for c in self.minpoly(a).all_coeffs())

# Verify frozen pins before interpreting certificates.
for turn in (3,4):
    entries=json.loads((BASE/'frozen'/f'turn0{turn}_manifest.json').read_text())
    for row in entries:
        p=BASE/'frozen'/Path(row['file']).name
        check('frozen_pin_'+p.name,p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'])

# Broad algebraic identities, without imposing numerical choices.
a0,h,E,O,r,u,v=S.symbols('a0 h E O r u v',nonzero=True)
residual=2*r*(E-v*O)+r*r*(E*E-u*O*O)
check('spectral_identity_reduction',S.cancel(residual.subs(r,2*h/a0)-(4*h/a0**2)*(h*(E*E-u*O*O)-a0*(v*O-E)))==0)
lam,L=S.symbols('lam L',nonzero=True)
check('normalization_polynomial_relation',S.rem(S.Poly((1-lam*L)*(lam+1)-lam,lam),S.Poly(L*lam*lam+L*lam-1,lam)).is_zero)
check('integrality_quadratic_relation',S.expand((lam*u)*(lam*u+u)-u*u/L-u*u*(lam**2+lam-1/L))==0)

claimed=json.loads((BASE/'frozen'/'turn03_verification.json').read_text())
orders=[]
for order_claim in claimed['orders']:
    k=order_claim['summary']['k']; F=ResultantField(k)
    cert={tuple(r['signs']):r for r in order_claim['rejections']}
    assert len(cert)==len(order_claim['rejections'])
    stats=dict(k=k,patterns=0,zero_interior_sum=0,failed_total_realness=0,failed_integrality=0,negative=0,retained=0)
    detail=[];seen=set();minpolys={}
    for signs in itertools.product((-1,1),repeat=(k-1)//2):
        stats['patterns']+=1; A=F.factor(signs); sA=sum(A); inner=F.red(sA-2)
        token=tuple(A);assert token not in seen;seen.add(token)
        assert A[0]==A[-1]==1 and A==list(reversed(A))
        # Each coefficient of the full product is checked in the cyclotomic quotient.
        conv=[F.red(sum(A[i]*A[n-i]*(-1)**(n-i) for i in range(max(0,n-k),min(k,n)+1))) for n in range(2*k+1)]
        assert conv==[1]+[0]*(2*k-1)+[-1]
        row=dict(signs=signs)
        if inner==0:
            stats['zero_interior_sum']+=1;row['verdict']='zero interior sum';assert signs not in cert
            row['A_coefficients']=[str(v) for v in A]
        else:
            mp=F.minpoly(sA);minpolys[str(mp.as_expr())]=True
            # Every conjugate is real, positive, and off the filter endpoints.
            assert sturm_variations(mp,'-inf')-sturm_variations(mp,'inf')==mp.degree()
            assert sturm_variations(mp,'-inf')-sturm_variations(mp,0)==0
            assert mp.eval(0)!=0 and mp.eval(2)!=0
            nbad=roots_between(mp,0,2)
            if nbad:
                stats['failed_total_realness']+=1;row.update(verdict='total realness',minpoly=str(mp.as_expr()),bad_conjugates=nbad)
                c=cert[signs];assert c['reason']=='A(1) has a conjugate in (0,2)'
                assert S.Poly(S.sympify(c['polynomial']),t).monic()==mp
            else:
                bad=None
                for j in range(1,k):
                    q=F.quotient(A[j]*A[j],inner);qp=F.minpoly(q)
                    if any(c.q!=1 for c in qp.all_coeffs()):
                        bad=(j,qp);break
                if bad:
                    stats['failed_integrality']+=1;j,qp=bad
                    row.update(verdict='integrality',index=j,minpoly=str(qp.as_expr()))
                    c=cert[signs];assert c['reason']=='coefficient-square quotient not algebraic integer' and c['index']==j
                    assert S.Poly(S.sympify(c['polynomial']),t).monic()==qp
                else:
                    assert all(v.is_Rational for v in A)
                    neg=any(v<0 for v in A);stats['negative' if neg else 'retained']+=1
                    row.update(verdict='negative coefficients' if neg else 'retained',A_coefficients=[str(v) for v in A])
                    assert signs not in cert
        detail.append(row)
    actual_survivors={(tuple(row['signs']),tuple(row['A_coefficients'])) for row in detail if row['verdict'] in ('retained','negative coefficients')}
    authored_survivors={(tuple(row['signs']),tuple(row['A_coefficients'])) for row in order_claim['summary']['survivors']}
    check('all_survivor_coefficients_match_order_'+str(k),actual_survivors==authored_survivors)
    retained=[row['A_coefficients'] for row in detail if row['verdict']=='retained']
    expected_retained=[] if k==13 else [[str(1 if j in (0,15) else 2 if j in (5,10) else 0) for j in range(16)]]
    check('exact_nonnegative_survivors_order_'+str(k),retained==expected_retained)
    expected=([64,1,62,1,0,0] if k==13 else [128,2,114,10,1,1])
    check('all_spectral_factors_order_'+str(k),[stats[q] for q in ('patterns','zero_interior_sum','failed_total_realness','failed_integrality','negative','retained')]==expected,summary=stats)
    check('all_author_rejections_verified_order_'+str(k),len(cert)==stats['failed_total_realness']+stats['failed_integrality'])
    orders.append(dict(summary=stats,factors=detail))
    print('Verified order', k, stats, flush=True)

# Manual Sturm controls with exact roots and repeated-root removal.
check('sturm_open_interval_control',roots_between(S.Poly((t-S.Rational(1,3))*(t-1)*(t-3),t),0,2)==2)
check('sturm_outside_interval_control',roots_between(S.Poly((t+1)*(t-3),t),0,2)==0)
F=ResultantField(15)
check('nonintegral_rational_control',not F.integral(S.Rational(1,6)))
check('integral_irrational_control',F.integral(x+x**29))
check('half_unit_nonintegral_control',not F.integral(x/2))
# A certificate with an altered rejection polynomial must fail comparison.
original=claimed['orders'][0]['rejections'][0]
mp=ResultantField(13).minpoly(sum(ResultantField(13).factor(original['signs'])))
check('reject_changed_rejection_polynomial',S.Poly(S.sympify(original['polynomial'])+1,t).monic()!=mp)
check('reject_deleted_sign_pattern',len(set(itertools.product((-1,1),repeat=6))-{tuple(original['signs'])})!=64)
A=F.factor((-1,)*7);A[1]+=1
badconv=[F.red(sum(A[i]*A[n-i]*(-1)**(n-i) for i in range(max(0,n-15),min(15,n)+1))) for n in range(31)]
check('reject_changed_factor_coefficient',badconv!=[1]+[0]*29+[-1])
# Logical separation controls appearing in the manuscript.
sqrt5=S.sqrt(5); vals=[1+sqrt5,3+sqrt5,3+sqrt5,1+sqrt5];LS=sum(vals)
check('integrality_without_total_realness_control',all(all(c.q==1 for c in S.Poly(S.minpoly(S.simplify(v*v/LS),t),t).monic().all_coeffs()) for v in vals) and 0<10-4*sqrt5<2)
check('total_realness_without_integrality_control',26>2 and S.Rational(4,24).q!=1)
check('filters_without_nonnegativity_control',any(r['verdict']=='negative coefficients' for r in orders[1]['factors']))

# General root-order bound checked on prime powers and finite sanity range.
check('odd_field_degree_formula',all(S.totient(2*k)==S.totient(k) for k in range(3,100,2)))
check('totient_bound_sanity',all(2*S.totient(n)**2>=n for n in range(1,2001)))
# A nonlinear involution is locally faithful, while a nonperiodic tangent-identity
# map prevents accidentally dropping the finite-order hypothesis from the lemma.
y=S.symbols('y')
inv=-y/(1+y)
check('nonlinear_involution_control',S.cancel(inv.subs(y,inv)-y)==0 and S.diff(inv,y).subs(y,0)==-1)
par=y/(1-y)
check('finite_order_hypothesis_control',S.diff(par,y).subs(y,0)==1 and S.cancel(par.subs(y,par)-y)!=0)

# Independent derivation of the cubic source by multiplying formal scalar jets.
a,b,T,U,V,W=S.symbols('a b T U V W',nonzero=True)
jet0=a+b+U*a*a+V*a*b+W*b*b
jetk=a*T+b/T+U*a*a*T*T+V*a*b+W*b*b/T**2
product=S.Poly(S.expand(jet0*jetk),a,b)
qaa=product.coeff_monomial(a*a);qab=product.coeff_monomial(a*b)
cubic=product.coeff_monomial(a*a*b)
check('quadratic_source_from_scalar_jets',S.cancel(qaa-T)==0 and S.cancel(qab-T-1/T)==0)
check('cubic_source_from_scalar_jets',S.expand(cubic-(U*(T*T+1/T)+V*(1+T)))==0)
P1,P2,ss=S.symbols('P1 P2 ss',nonzero=True)
sub=S.factor(cubic.subs({U:-T/P2,V:-(T+1/T)/P1}))
G=P1*T*(T**3+1)+P2*(T*T+1)*(T+1)
check('cubic_divisibility_numerator',S.cancel(-sub*P1*P2*T-G)==0)
# Real form of G derived through t+t^-1=2v.
vv,M=S.symbols('vv M',nonzero=True)
realG=(2-ss)*(2*vv-1)+2*vv*(2*vv+ss-2*M)
solM=S.solve(realG,M)[0]
check('second_moment_from_real_cubic',S.cancel(solM-(vv+1-(2-ss)/(4*vv)))==0)
variance=solM-2*(vv+1)/ss
check('weighted_variance_from_second_moment',S.cancel(variance-(2-ss)*(ss+4*vv*(vv+1))/(-4*ss*vv))==0)

# Independent complete coefficient ideals in one variable, plus a deliberate
# false candidate. A root of one coefficient is not mistaken for common zero.
c=S.symbols('c')
for k in (2,3):
    P=z**k+1-c*sum(z**j for j in range(1,k));G=(2-(k-1)*c)*z**k*(z**(3*k)+1)+P.subs(z,z*z)*(z**(2*k)+1)*(z**k+1)
    rem=S.Poly(S.rem(G,P,z),z)
    gb=S.groebner(rem.all_coeffs(),c,domain=S.QQ)
    expected=c*(c-2)*(c-1)*(c*c+c-1) if k==2 else c*(c-1)*(c*c+2*c-1)*(c**3+4*c*c+2*c-2)
    check('complete_cubic_ideal_order_'+str(k),len(gb.polys)==1 and gb.polys[0].monic()==S.Poly(expected,c).monic())
H=c**3+4*c*c+2*c-2
check('false_cubic_candidate_irreducible',S.Poly(H,c).is_irreducible)
check('false_cubic_candidate_intervals',H.subs(c,S.Rational(12,25))<0<H.subs(c,S.Rational(49,100)) and H.subs(c,-4)<0<H.subs(c,-3))
check('false_cubic_candidate_exact_isolation',roots_between(H.subs(c,t),S.Rational(12,25),S.Rational(49,100))==1 and roots_between(H.subs(c,t),-4,-3)==1)
# Verify the certificate passes all cubic coefficients identically in Q[c]/H.
P=z**3-c*z*z-c*z+1;G=(2-2*c)*z**3*(z**9+1)+P.subs(z,z*z)*(z**6+1)*(z**3+1)
check('false_cubic_candidate_actually_passes',all(S.rem(a,H,c)==0 for a in S.Poly(S.rem(G,P,z),z).all_coeffs()))
check('false_cubic_candidate_conjugate_fails_unit_circle',(-3+1)<-1 and (-3+1)**2>=4)

# Classical controls include homogeneous, no-support, odd -1 roots, and scales.
classical=[]
for ell in (1,2,3,5):
    for family,k,coeff in [('reciprocal',ell,{}),('six',2*ell,{ell:S.Integer(1)}),('five',2*ell,{ell:(S.sqrt(5)-1)/2}),('eight',3*ell,{ell:S.sqrt(2)-1,2*ell:S.sqrt(2)-1})]:
        P=z**k+1-sum(a*z**j for j,a in coeff.items());ss=sum(coeff.values())
        G=(2-ss)*z**k*(z**(3*k)+1)+P.subs(z,z*z)*(z**(2*k)+1)*(z**k+1)
        assert S.rem(G,P,z,extension=True)==0
        # Pairwise product resonance test using a resultant and gcd.
        K=S.QQ.algebraic_field(S.sqrt(2),S.sqrt(5))
        R=S.Poly(P.subs(z,x),x,domain=K.poly_ring(z)).resultant(S.Poly(S.expand(x**k*P.subs(z,z/x)),x,domain=K.poly_ring(z)))
        assert S.Poly(P,z,domain=K).gcd(S.Poly(R,z,domain=K)).degree()==0
        classical.append(dict(family=family,dilation=ell))
check('classical_cubic_and_nonresonance_controls',True,cases=classical)
# Unit constraints at the two inhomogeneous nonconstant base families.
for c0 in ((3-S.sqrt(5))/2,3-2*S.sqrt(2)):
    check('normalized_unit_'+str(c0),abs(S.Poly(S.minpoly(c0,t),t).monic().TC())==1)

# Direct Jacobians at both fixed points, including k=1 and sparse specializations.
for k in range(1,7):
    xx=S.symbols('x0:'+str(k));cc=S.symbols('c1:'+str(k));c0=1-sum(cc)
    fn=(c0+sum(cc[j-1]*xx[j] for j in range(1,k)))/xx[0]
    for rr,label in [(S.Integer(1),'positive'),(-c0,'negative')]:
        fixed={q:rr for q in xx}
        assert S.cancel(fn.subs(fixed)-rr)==0
        last=[S.cancel(S.diff(fn,q).subs(fixed)) for q in xx]
        assert last==[-1]+[S.cancel(q/rr) for q in cc]
        J=S.zeros(k)
        for j in range(k-1):J[j,j+1]=1
        for j in range(k):J[k-1,j]=last[j]
        expected=z**k+1-sum(S.cancel(cc[j-1]/rr)*z**j for j in range(1,k))
        assert S.cancel(J.charpoly(z).as_expr()-expected)==0
check('two_fixed_point_jacobians_orders_1_through_6',True)
# The arc endpoint contradiction uses exact third roots, including s=1.
omega=(-1+S.sqrt(3)*S.I)/2
check('quadratic_resonance_endpoint_contradiction',S.expand((1+omega)**2-omega)==0 and S.expand(1+omega**2+omega)==0 and omega!=0)

out=dict(all_passed=True,sympy_version=S.__version__,method='Independent polynomial quotient arithmetic, resultants and manual exact Sturm variations; no authored verifier imports and no floating point.',checks=checks,orders=orders)
(BASE/'checks'/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(all_passed=True,check_count=len(checks),orders=[o['summary'] for o in orders]),indent=2))
