#!/usr/bin/env python3
"""Fresh standard-library exact diagnostics. No author code is imported.
The finitely many checks supplement the written audit; they are not universal proofs.
"""
from fractions import Fraction as Q
from math import gcd, isqrt
import json

counts = {}
negatives = []
def check(value, family):
    if not value:
        raise RuntimeError('independent check failed: ' + family)
    counts[family] = counts.get(family, 0) + 1

def convolution(a, b, length=None):
    n = len(a) + len(b) - 1 if length is None else length
    out = [0] * n
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b[:max(0, n-i)]):
                out[i+j] += x*y
    return out

def series_power(a, m, length):
    out = [1] + [0]*(length-1)
    for _ in range(m):
        out = convolution(out, a, length)
    return out

def root_series(m, terms, target):
    # Solve h^m = target coefficient by coefficient, only dividing by m.
    h = [Q(1)] + [Q(0)]*(terms-1)
    for j in range(1, terms):
        known = series_power(h, m, j+1)[j]
        h[j] = (Q(target[j]) - known)/m
    return h

def compose_mod(a, b, p, length):
    out = [0]*length
    for x in reversed(a[:length]):
        out = [z % p for z in convolution(out, b, length)]
        out[0] = (out[0]+x) % p
    return out

def degree_order(a):
    return next((i for i,c in enumerate(a) if c), None)

def trim(a):
    a = list(a)
    while len(a)>1 and not a[-1]: a.pop()
    return a

def poly_add(a,b):
    out = [0]*max(len(a),len(b))
    for i,x in enumerate(a): out[i]+=x
    for i,x in enumerate(b): out[i]+=x
    return trim(out)

def poly_sub(a,b): return poly_add(a,[-x for x in b])
def derivative(a): return [j*a[j] for j in range(1,len(a))] or [0]
def poly_power(a,n):
    out=[1]
    for _ in range(n): out=convolution(out,a)
    return out

def homogeneous(a, num, den):
    out=[0]
    for j,c in enumerate(a):
        out=poly_add(out,[c*x for x in convolution(poly_power(num,j),poly_power(den,len(a)-1-j))])
    return out

class Cyclo:
    """Independent exact quotient Q[x]/Phi_(p^n), using fixed-length vectors."""
    def __init__(self,p,n):
        self.q=p**n
        self.step=p**(n-1)
        self.d=(p-1)*self.step
        self.zero=(Q(0),)*self.d
        self.one=(Q(1),)+(Q(0),)*(self.d-1)
        self.x=self.reduce([0,1])
    def reduce(self,v):
        a=list(map(Q,v)) + [Q(0)]*max(0,self.d-len(v))
        for i in range(len(a)-1,self.d-1,-1):
            c=a[i]
            if c:
                for j in range(0,self.d,self.step): a[i-self.d+j]-=c
        return tuple(a[:self.d])
    def add(self,a,b): return tuple(x+y for x,y in zip(a,b))
    def mul(self,a,b): return self.reduce(convolution(a,b))
    def power(self,a,n):
        out=self.one
        for _ in range(n): out=self.mul(out,a)
        return out
    def scale(self,a,n): return tuple(x*n for x in a)
    def matrix_product(self,a,b):
        return tuple(tuple(self.add(self.mul(a[i][0],b[0][j]),self.mul(a[i][1],b[1][j])) for j in range(2)) for i in range(2))

def integer_matrix_product(a,b):
    return tuple(tuple(a[i][0]*b[0][j]+a[i][1]*b[1][j] for j in range(2)) for i in range(2))

def main():
    # Hensel recurrence rather than the author's generalized-binomial loop.
    for p in (2,3,5,7,11):
        for m in range(1,13):
            if gcd(p,m)!=1: continue
            terms=18
            h=root_series(m,terms,[(-1)**j for j in range(terms)])
            check(series_power(h,m,terms)==[(-1)**j for j in range(terms)],'hensel_equation')
            for c in h: check(c.denominator % p != 0,'hensel_integrality')
            length=max(14,2*m+4)
            sigma=[0]*length
            for j,c in enumerate(h):
                if 1+j*m<length: sigma[1+j*m]=(c.numerator*pow(c.denominator,-1,p))%p
            identity=[0,1]+[0]*(length-2)
            iterate=identity
            for j in range(1,p+1):
                iterate=compose_mod(iterate,sigma,p,length)
                check((iterate==identity)==(j==p),'special_action_exact_order')
                if j<p: check(iterate[m+1] == (-j*pow(m,-1,p))%p,'special_action_leading_term')
            inverse=identity
            for _ in range(p-1): inverse=compose_mod(inverse,sigma,p,length)
            check(compose_mod(sigma,inverse,p,length)==identity and compose_mod(inverse,sigma,p,length)==identity,'special_action_two_sided_inverse')
    # Exact cyclotomic matrix powers, including every proper iterate.
    for p in (2,3,5,7):
        for n in (1,2,3):
            if p**n>125: continue
            ring=Cyclo(p,n)
            I=((ring.one,ring.zero),(ring.zero,ring.one))
            M=((ring.x,ring.zero),(ring.one,ring.one))
            B=I
            for j in range(1,ring.q+1):
                B=ring.matrix_product(B,M)
                check((B==I)==(j==ring.q),'cyclotomic_mobius_exact_order')
            for m in (1,2,3,5,7):
                if gcd(m,ring.q)==1:
                    alpha=ring.power(ring.x,pow(m,-1,ring.q))
                    check(ring.power(alpha,m)==ring.x and ring.power(alpha,ring.q)==ring.one,'lift_linear_coefficient')
            if n>1:
                check(ring.q//p==p**(n-1) and ring.q!=p,'lost_reduction_kernel')
    # Independently derive the complete C3 Mobius orbit, quotient and derivative.
    I=((1,0),(0,1)); M=((1,-3),(1,-2))
    orbit=[I]; B=I
    for _ in range(3): B=integer_matrix_product(B,M); orbit.append(B)
    check(orbit[3]==I and all(A[0][1] or A[1][0] or A[0][0]!=A[1][1] for A in orbit[1:3]),'unmarked_c3_exact_order')
    check(integer_matrix_product(orbit[1],orbit[2])==I and integer_matrix_product(orbit[2],orbit[1])==I,'unmarked_c3_inverse')
    N=[1]; D=[1]
    for A in orbit[:3]:
        N=convolution(N,[A[0][1],A[0][0]])
        D=convolution(D,[A[1][1],A[1][0]])
    N,D=trim(N),trim(D)
    # This product representation has both numerator and denominator negated.
    check(N==[0,-9,9,-2] and D==[-2,3,-1],'derived_norm_parameter')
    a,b=[-3,1],[-2,1]
    lhs=convolution(homogeneous(N,a,b),D)
    rhs=convolution(convolution(N,b),homogeneous(D,a,b))
    check(trim(lhs)==trim(rhs),'norm_invariance_identity')
    W=poly_sub(convolution(derivative(N),D),convolution(N,derivative(D)))
    check(W==[2*x for x in poly_power([3,-3,1],2)],'good_model_different_factorization')
    check(degree_order([c%3 for c in W])==4,'good_model_special_different')
    check(all(c%3==0 for c in [3,-3]) and 3%9!=0,'fixed_section_eisenstein')
    # The nonzero constant coefficient is 3/2: reduction is local, not section-fixed.
    check(Q(N[0],D[0])==0 and Q(-3,-2)==Q(3,2),'constant_translation_in_maximal_ideal')
    perturbed=((1,-4),(1,-2)); B=I
    for _ in range(3): B=integer_matrix_product(B,perturbed)
    check(B[0][1]!=0 or B[1][0]!=0 or B[0][0]!=B[1][1],'negative_mobius_perturbation')
    negatives.append('Changing the C3 numerator constant from -3 to -4 destroys order three.')
    # lambda=zeta_3-1 identities in Q[zeta_3], independently from lambda polynomials.
    R=Cyclo(3,1); lam=R.add(R.x,R.scale(R.one,-1))
    check(R.add(R.add(R.power(lam,2),R.scale(lam,3)),R.scale(R.one,3))==R.zero,'lambda_relation')
    check(R.mul(lam,R.add(R.scale(lam,-1),R.scale(R.one,-3)))==R.scale(R.one,3),'coefficient_3_over_lambda')
    check(R.mul(R.power(lam,2),R.add(lam,R.scale(R.one,2)))==R.scale(R.one,3),'coefficient_3_over_lambda_squared')
    disc=R.add(R.power(lam,6),R.scale(R.power(lam,4),-4))
    check(disc!=R.zero,'bad_model_separable_zeros')
    # Newton polygon exact slopes for coefficients valuations (4,3,0).
    check(Q(0-4,2-0)==-2 and Q(3)>Q(4)+(Q(0)-Q(4))/2,'bad_model_newton_polygon')
    branch_orders=(-2,1,1)
    generic_different=sum(3-gcd(3,abs(v)) for v in branch_orders)
    t_num,t_den=[0,0,0,1],[1,0,-1]
    der=poly_sub(convolution(derivative(t_num),t_den),convolution(t_num,derivative(t_den)))
    special_different=degree_order([x%3 for x in der])
    check(generic_different==6 and special_different==4,'bad_model_different_mismatch')
    check(sum(3-gcd(3,abs(v)) for v in (-1,1))==special_different,'remove_extra_pole_positive_control')
    negatives.append('The bad birational model has generic different 6 versus special different 4; deleting its extra pole restores the necessary degree 4.')
    # Independent order-p composita can never create a cyclic order-p-squared element.
    for p in (2,3,5,7):
        for a in range(p):
            for b in range(p):
                order=next(j for j in range(1,p+1) if j*a%p==j*b%p==0)
                check(order<=p,'elementary_abelian_exponent')
    # Explicit first-order descent obstruction modulo p^2, not sampled integer valuations.
    for p in (2,3,5,7,11):
        for r in range(2,14):
            check(not any(pow(a,r,p*p)==p for a in range(p*p)),'no_descent_point_mod_p_squared')
            check(pow(0,r,p)==0,'descent_special_point_exists')
    negatives.append('X^r = p has a special point but no point even modulo p^2 for the tested primes and r > 1.')
    # The m coprime p assumption cannot be discarded.
    for p in (2,3,5,7):
        h=root_series(p,3,[1,-1,1])
        check(h[1].denominator%p==0,'negative_nonunit_root_index')
    negatives.append('When m = p, the first coefficient of (1+X)^(-1/m) is nonintegral.')
    # Completeness is needed for the nonzero-section translation in the standalone lemma.
    h=root_series(2,25,[1,2]+[0]*23)
    check(all(c.denominator%3 for c in h),'translation_counterexample_integral_coefficients')
    check(series_power(h,2,25)==[1,2]+[0]*23,'translation_counterexample_square_identity')
    check(isqrt(7)**2!=7,'translation_counterexample_no_rational_square_root')
    negatives.append('Over Z_(3), sqrt(1+2Z) exists in the formal-series ring but translation by 3 would force a rational square root of 7; completeness is required.')
    negatives.append('For n > 1 the generic order p^n ansatz reduces with kernel of size p^(n-1).')
    return {'schema':'cyclic-lifts-independent-controls-v1','total_checks':sum(counts.values()),'families':dict(sorted(counts.items())),'negative_controls':negatives,'scope':'Finite exact diagnostics plus independent proof audit; no solution of the universal problem.'}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
