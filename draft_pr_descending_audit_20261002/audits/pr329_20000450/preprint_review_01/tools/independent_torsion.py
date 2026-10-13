#!/usr/bin/env python3
"""Own chord-derived psi5 and disjoint finite-field controls; no package imports."""
import json
import sympy as S

x, a2, a4, a6, beta = S.symbols("x a2 a4 a6 beta")
f = x**3 + a2*x*x + a4*x + a6
checks = []
def same(label, left, right=0):
    value = S.cancel(left-right)
    if value != 0:
        raise AssertionError((label, value))
    checks.append(label)

# Express the tangent and subsequent secant through their ratios to v, where
# v^2=f. This produces the fifth-kernel equation without division recursion.
dx = S.diff(f, x)
doubled_x = S.cancel(dx*dx/(4*f)-a2-2*x)
doubled_v_ratio = S.cancel(-1 + dx*(x-doubled_x)/(2*f))
secant_ratio = S.cancel((doubled_v_ratio-1)/(doubled_x-x))
tripled_x = S.cancel(f*secant_ratio**2-a2-x-doubled_x)
p3 = S.cancel(4*f*(x-doubled_x))
p4_over_2v = S.cancel(16*f*f*doubled_v_ratio)
p5 = S.Poly(S.cancel(4*f*p3*p3*(doubled_x-tripled_x)), x).as_expr()
same("doubling remains on curve", f.subs(x,doubled_x), f*doubled_v_ratio**2)
same("generic fifth equation is polynomial", p5, 16*f*f*p4_over_2v-p3**3)
assert S.Poly(p5,x).degree()==12 and S.Poly(p5,x).LC()==5
specialization={a2:(beta**2-6*beta+1)/4, a4:(beta**2-beta)/2, a6:beta**2/4}
psi=S.Poly(S.expand(p5.subs(specialization)),x)
R,rem=S.div(psi,S.Poly(x*(x-beta),x))
assert rem.is_zero
claimed=[5,5*(beta**2-5*beta+1),beta**4-7*beta**3+44*beta**2-38*beta+1,
 beta*(beta**4+3*beta**3-26*beta**2+127*beta-9),
 beta**2*(beta**4+3*beta**3+19*beta**2-248*beta+36),
 beta**3*(beta**4+3*beta**3-71*beta**2+322*beta-84),
 beta**4*(beta**4-12*beta**3+94*beta**2-293*beta+126),
 5*beta**5*(beta**3-10*beta**2+36*beta-25),
 5*beta**6*(2*beta**2-13*beta+16),10*beta**7*(beta-3),5*beta**8]
for j,(derived,table) in enumerate(zip(R.all_coeffs(),claimed)):
    same("residual coefficient x^"+str(10-j),derived,table)
T=S.expand(4*f.subs(specialization))
D=beta**5*(beta**2-11*beta-1)
same("branch collision resultant",S.resultant(psi.as_expr(),T,x),D**6)
same("tripling denominator resultant",S.resultant(psi.as_expr(),p3.subs(specialization),x),D**8)
same("marked abscissa zero excluded",R.eval(0),5*beta**8)
same("marked abscissa beta excluded",R.eval(beta),5*beta**12)
same("universal discriminant constant",S.discriminant(p5.subs({a2:0,a4:0,a6:1}),x),5**11*(-432)**22)
assert S.Poly(psi.as_expr().subs(beta,0),x).gcd(S.Poly(S.diff(psi.as_expr(),x).subs(beta,0),x)).degree()>0
assert S.Poly(psi.as_expr().subs(beta,1),x,modulus=5).degree()<12

def prime(n):
    return n>=2 and all(n%d for d in range(2,int(n**.5)+1))
def finite_curve(p,c2,c1,c0):
    squares={}
    for y in range(p):squares.setdefault(y*y%p,[]).append(y)
    points=[(xx,y) for xx in range(p) for y in squares.get((xx**3+c2*xx*xx+c1*xx+c0)%p,[])]
    def add(P,Q):
        if P is None:return Q
        if Q is None:return P
        xx,y=P;zz,w=Q
        if xx==zz and (y+w)%p==0:return None
        numerator=(3*xx*xx+2*c2*xx+c1) if P==Q else w-y
        denominator=2*y if P==Q else zz-xx
        slope=numerator*pow(denominator%p,-1,p)%p
        h=(slope*slope-c2-xx-zz)%p
        answer=(h,(slope*(xx-h)-y)%p)
        assert (answer[1]**2-answer[0]**3-c2*answer[0]**2-c1*answer[0]-c0)%p==0
        return answer
    def times5(P):
        double=add(P,P)
        return add(add(double,double),P)
    return points,times5,squares

# Ordinary grid differs from the shipped direct-finite checker; p=31 is an
# additional explicit special-j control. Evaluation uses only our derivation.
primes=(13,17,23,31,37,43,47,67,73,83,97)
terms=S.Poly(psi.as_expr(),x,beta).terms()
rterms=S.Poly(R.as_expr(),x,beta).terms()
def evaluate(ts,xx,b,p):
    return sum(int(v)*pow(xx,ix,p)*pow(b,ib,p) for (ix,ib),v in ts)%p
fibers=points_seen=0
mutants={"alter_constant":0,"omit_marked":0,"omit_ordinate":0}
j_controls=[]
for p in primes:
    for b in range(p):
        if b**5*(b*b-11*b-1)%p==0:continue
        inv4=pow(4,-1,p)
        c2=(b*b-6*b+1)*inv4%p;c1=(b*b-b)*pow(2,-1,p)%p;c0=b*b*inv4%p
        pts,mul5,squares=finite_curve(p,c2,c1,c0)
        actual={P for P in pts if mul5(P) is None}
        predicted={P for P in pts if evaluate(terms,P[0],b,p)==0}
        assert actual==predicted and len(actual) in (4,24)
        marked={(0,(-b*pow(2,-1,p))%p),(0,(b*pow(2,-1,p))%p),
                (b,(-b*b*pow(2,-1,p))%p),(b,(b*b*pow(2,-1,p))%p)}
        assert marked<=actual and len(marked)==4
        assert all(y!=0 for _,y in actual)
        mutants["alter_constant"]+=int(actual!={P for P in pts if (evaluate(terms,P[0],b,p)+1)%p==0})
        mutants["omit_marked"]+=int(actual!={P for P in pts if evaluate(rterms,P[0],b,p)==0})
        mutants["omit_ordinate"]+=int(actual!={min(P for P in actual if P[0]==xx) for xx,_ in actual})
        B2=b*b-6*b+1;B4=b*b-b
        C4=(B2*B2-24*B4)%p;C6=(-B2**3+36*B2*B4-216*b*b)%p
        if C4==0 or C6==0:j_controls.append([p,b,"j0" if C4==0 else "j1728",len(actual)+1])
        fibers+=1;points_seen+=len(pts)
assert all(mutants.values()) and {row[2] for row in j_controls}=={"j0","j1728"}

# Check the twist/radical/cyclotomic rules with a separately completed-square
# group law and additional finite fields not all present in the export.
categories={};field_fibers=0
for p in (11,19,29,89,101,149,191):
    for rr in range(p):
        if rr*rr%p!=5:continue
        dd=(5+2*rr)%p;phi=(1+rr)*pow(2,-1,p)%p;cc=pow(phi,5,p)
        for ll in range(p):
            if ll in (0,-5*rr%p,-cc%p):continue
            b=(11-5*rr)*ll*pow(2*(ll+5*rr)%p,-1,p)%p
            c2=dd*(b*b-6*b+1)*pow(4,-1,p)%p
            c1=dd*dd*(b*b-b)*pow(2,-1,p)%p;c0=dd**3*b*b*pow(4,-1,p)%p
            pts,mul5,squares=finite_curve(p,c2,c1,c0)
            count=1+sum(mul5(P) is None for P in pts)
            split=(pow((ll+cc)%p,(p-1)//5,p)==1) if p%5==1 else True
            dsq=dd in squares
            expected=((25 if split else 5) if dsq else 1) if p%5==1 else 5
            assert count==expected
            category=(p%5==1,dsq,split)
            categories[str(category)]=categories.get(str(category),0)+1
            field_fibers+=1
assert len(categories)==6
print(json.dumps({"status":"PASS","sympy":S.__version__,"exact_checks":checks,
 "own_generic_psi5_coefficients":[str(v) for v in S.Poly(p5,x).all_coeffs()],
 "own_residual_coefficients":[str(S.factor(v)) for v in R.all_coeffs()],
 "direct_fibers":fibers,"direct_affine_points":points_seen,"mutants_detected":mutants,
 "special_j_controls":j_controls,"arithmetic_fibers":field_fibers,"categories":categories,
 "scope":"Own symbolic derivation plus independent finite controls; arithmetic exact proof and cited inputs are separately required."},indent=2))
