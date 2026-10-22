#!/usr/bin/env python3
"""Exact GF(2) polynomial/rational diagnostics; no finite cohomology decision oracle.

The polynomial variables are beta,z,s,gamma for the differential certificate.
For the square-class diagnostics beta is renamed a=beta_original**2; then R
is contained in the kernel of d/da and S in the kernel of d/dz.  Symbolic
identities and bounded enumerations are kept distinct in the output.
"""
import argparse, hashlib, itertools, json, sys
N=4
ZERO=frozenset()
ONE=frozenset({(0,)*N})
def add(a,b): return a ^ b
def mul(a,b):
    out=set()
    for x in a:
        for y in b:
            m=tuple(i+j for i,j in zip(x,y))
            if m in out: out.remove(m)
            else: out.add(m)
    return frozenset(out)
def ppow(a,n):
    if n<0: raise ValueError('negative polynomial exponent')
    out=ONE
    while n:
        if n&1: out=mul(out,a)
        a=mul(a,a);n//=2
    return out
def deriv(p,i):
    return frozenset(tuple(e-(j==i) for j,e in enumerate(m)) for m in p if m[i]&1)
def mono(i): return frozenset({tuple(int(j==i) for j in range(N))})
class Q:
    __slots__=('p','q')
    def __init__(self,p=ZERO,q=ONE):
        if not q: raise ZeroDivisionError('zero denominator')
        if not p: self.p,self.q=ZERO,ONE;return
        # Remove common monomial factors only; no reliance on a CAS/GCD.
        mins=tuple(min(min(m[i] for m in p),min(m[i] for m in q)) for i in range(N))
        self.p=frozenset(tuple(m[i]-mins[i] for i in range(N)) for m in p)
        self.q=frozenset(tuple(m[i]-mins[i] for i in range(N)) for m in q)
    def __add__(a,b):
        b=coerce(b);return Q(add(mul(a.p,b.q),mul(b.p,a.q)),mul(a.q,b.q))
    __sub__=__add__
    def __mul__(a,b):
        b=coerce(b);return Q(mul(a.p,b.p),mul(a.q,b.q))
    def __truediv__(a,b):
        b=coerce(b);return Q(mul(a.p,b.q),mul(a.q,b.p))
    def __pow__(a,n):
        if n<0:return Q(ppow(a.q,-n),ppow(a.p,-n))
        return Q(ppow(a.p,n),ppow(a.q,n))
    def __eq__(a,b):
        b=coerce(b);return mul(a.p,b.q)==mul(b.p,a.q)
    def __bool__(a):return bool(a.p)
    def d(a,i):return Q(add(mul(deriv(a.p,i),a.q),mul(a.p,deriv(a.q,i))),mul(a.q,a.q))
    def fingerprint(a):return {'numerator':sorted(a.p),'denominator':sorted(a.q)}
def coerce(a):
    if isinstance(a,Q):return a
    if isinstance(a,int):return Q(ONE if a&1 else ZERO)
    raise TypeError(type(a).__name__)
Z=Q();U=Q(ONE)
X=tuple(Q(mono(i)) for i in range(N))
B,z,s,g=X

def df(q):return tuple(q.d(i) for i in range(N))
def plus(v,w):return tuple(a+b for a,b in zip(v,w))
def times(q,v):return tuple(q*a for a in v)
def dlog(q):return times(q**-1,df(q))
def wp(v):
    # Coordinatewise in the fixed logarithmic 2-basis dlog(beta,z,s,gamma).
    return tuple(((c*x)**2+c*x)/x for c,x in zip(v,X))
def require(condition,name):
    if not condition:raise ValueError('CHECK FAILED: '+name)
def veq(v,w):return all(a==b for a,b in zip(v,w))
def vand(v):return all(not a for a in v)

def core():
    f=U+B**2*z;h=B**2*z/f;dlz=dlog(z)
    xi=times(s**-4*(B**4*z**2)/(U+B**4*z**2),dlz)
    a=times(s**-2*h,dlz);b=times(s**-1*h,dlz)
    correction=df(s**-2*h)
    eq={
      'd_beta_squared_zero':vand(df(B**2)),
      'd_beta_nonzero':not vand(df(B)),
      'df_beta_squared_dz':veq(df(f),times(B**2,df(z))),
      'dlog_f_h_dlog_z':veq(dlog(f),times(h,dlz)),
      'h_squared_pullback':h**2==(B**4*z**2)/(U+B**4*z**2),
      'first_Artin_Schreier_descent':veq(plus(xi,a),wp(a)),
      'logarithm_change_mod_exact':veq(plus(times(s**-2+s**-1,dlog(f)),wp(b)),correction),
      'full_fixed_basis_certificate':veq(plus(xi,b),plus(plus(wp(a),wp(b)),correction)),
      'correction_is_nonzero_before_quotient':not vand(correction),
      'independent_gamma_sqrt_preserves_dz':not vand(df(z)),
    }
    for name,ok in eq.items():require(ok,name)
    # Exponent one must distinguish the base coordinate u (here B) from its
    # square root beta. Before adjoining beta, d(1+uz) has a NONZERO du term.
    f_base=U+B*z;h_base=B*z/f_base
    eq['exponent_one_base_du_term_nonzero']=not veq(dlog(f_base),times(h_base,dlz))
    require(eq['exponent_one_base_du_term_nonzero'],'exponent_one_base_du_term_nonzero')
    # After adjoining beta with beta**2=u, the pullback has d(u)=0. The
    # established certificate then says xi-[s^-1,f_base) lies in kernel L.
    # This proves membership in kernel L + kernel K, NOT equality in the base.
    eq['exponent_one_kernel_sum_after_pullback_certificate']=veq(plus(xi,times(s**-1,dlog(U+B**2*z))),plus(plus(wp(a),wp(b)),correction))
    require(eq['exponent_one_kernel_sum_after_pullback_certificate'],'exponent_one_kernel_sum_after_pullback_certificate')
    # Under z=eta**2 (use gamma=eta), dz maps to zero. This evaluates the
    # pullback by the chain rule; it does not evaluate denominator at z=0.
    eq['pfister_slot_z_chain_rule_zero']=vand(df(g**2))
    require(eq['pfister_slot_z_chain_rule_zero'],'pfister_slot_z_chain_rule_zero')
    return eq,(f,h,xi,a,b,correction)

def coefficient_checks():
    # Now B denotes a=beta_original**2. R=F2(a**2,z**2,gamma**2).
    basis=[ONE,ppow(mono(0),2),ppow(mono(1),2),ppow(mono(3),2),mul(ppow(mono(0),2),ppow(mono(1),2))]
    values=[]
    for mask in range(1<<len(basis)):
        p=ZERO
        for j,m in enumerate(basis):
            if mask>>j&1:p=add(p,m)
        values.append(Q(p))
    count=0;cross=0;rational=0
    f=U+B*z
    for i,u in enumerate(values):
      for j,v in enumerate(values):
        if not u and not v:continue
        c=u+v*z
        require(bool(c),'c nonzero by disjoint even/odd z monomials')
        # This is the universal obstruction numerator au+v in the bounded set.
        obstruction=B*u+v
        require(bool(obstruction),'au+v cannot vanish for nonzero u,v in R')
        require(not u.d(0) and not v.d(0),'u,v derivative da vanishes in R')
        count+=1
        # Check the actual rational quotient derivative, rather than just repeat
        # the parity argument, on a fixed grid that includes zeros and constants.
        if i<12 and j<12:
          q=f/c
          require(q.d(1)==obstruction/(c**2),'quotient derivative formula')
          require(bool(q.d(1)),'q not in S since dz derivative nonzero')
          cross+=1
        if i and j and i%5==0 and j%7==0:
          # Add genuinely rational R coefficients with independent denominators.
          ur=u/(U+B**2+g**2);vr=v/(U+z**2+B**4)
          cr=ur+vr*z;qr=f/cr
          require(qr.d(1)==(B*ur+vr)/(cr**2),'rational coefficient derivative formula')
          require(bool(qr.d(1)),'rational obstruction')
          rational+=1
    # Universal monomial tests used by the written proof: a has odd a-adic
    # order; all R monomials have even a-adic order. S omits z, R omits a.
    require(bool(B.d(0)),'a not in R by derivation')
    require(bool(z.d(1)),'z not in S by derivation')
    return {'R_polynomial_pairs':count,'actual_quotient_derivative_checks':cross,'rational_R_coefficient_checks':rational,'square_class_universal_derivation_tests':2}

def norms():
    # Quadratic D-algebra with pi**2=s*pi+s. Pairs mean A+B*pi.
    def pmul(v,w):
        a,b=v;c,d=w
        return (a*c+b*d*s,a*d+b*c+b*d*s)
    def conj(v):a,b=v;return(a+b*s,b)
    def norm(v):return pmul(v,conj(v))
    require(norm((Z,U))[0]==s and not norm((Z,U))[1],'Norm(pi)=s')
    cases=0
    vals=[Z,U,B,z,g,B+z,U+B*z]
    for a,b in itertools.product(vals,repeat=2):
        n=norm((a,b));require(not n[1],'norm fixed by conjugation')
        require(n[0]==a**2+a*b*s+b**2*s,'norm formula')
        cases+=1
    return {'quadratic_norm_identity_cases':cases,'Norm_pi_equals_s':True}

WRONG=['differentiate_square','wrong_h_frobenius','wrong_s_power','omit_exact_correction','gamma_kills_dz','a_belongs_R','wrong_quotient_derivative','slot_z_preserves_dz','invalid_exponent_one_base_dlog']
def wrong(name):
    checks,(f,h,xi,a,b,correction)=core()
    if name=='differentiate_square':require(veq(df(B**2),df(B)),'wrong d(beta squared)=d beta')
    elif name=='wrong_h_frobenius':require(h**2==(B**2*z**2)/(U+B**2*z**2),'wrong beta exponent in h squared')
    elif name=='wrong_s_power':require(veq(plus(times(s**-2*h**2,dlog(z)),a),wp(a)),'wrong s^-2 in xi')
    elif name=='omit_exact_correction':require(veq(times(s**-2+s**-1,dlog(f)),wp(b)),'wrong equality of differential representatives')
    elif name=='gamma_kills_dz':require(vand(df(z)),'wrong independent gamma kills dz')
    elif name=='a_belongs_R':require(not B.d(0),'wrong a belongs R')
    elif name=='wrong_quotient_derivative':
        u=U+B**2;v=z**2;require(((U+B*z)/(u+v*z)).d(1)==(u+B*v)/(u+v*z)**2,'wrong quotient obstruction numerator')
    elif name=='slot_z_preserves_dz':require(not vand(df(g**2)),'wrong square-root slot preserves dz')
    elif name=='invalid_exponent_one_base_dlog':require(veq(dlog(U+B*z),times(B*z/(U+B*z),dlog(z))),'wrong base-field dlog(1+uz) with du term omitted')
    else:raise ValueError('unknown wrong mode')
    raise RuntimeError('wrong result unexpectedly passed')

def main():
    p=argparse.ArgumentParser();p.add_argument('--wrong',choices=WRONG);args=p.parse_args()
    if args.wrong:wrong(args.wrong)
    checks,_=core()
    out={'status':'PASS','arithmetic':'exact GF(2) multivariate polynomials and rational cross multiplication','finite_checks_are_diagnostics_only':True,'symbolic_identities':checks,'bounded_square_class_diagnostics':coefficient_checks(),'quadratic_algebra_diagnostics':norms(),'wrong_modes':WRONG}
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
