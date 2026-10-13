#!/usr/bin/env python3
"""Independent exact controls. Imports no author or historical checker."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
import json
import math
import sympy as S

COUNTS = Counter()
u, t, s, Z = S.symbols('u t s Z')

def require(condition, category):
    if not condition:
        raise AssertionError(category)
    COUNTS[category] += 1

@lru_cache(None)
def weights(d, k):
    result = []
    for q in range(d+1):
        cardinal = S.Integer(1)
        for j in range(d+1):
            if j != q:
                cardinal *= (Z-j)/S.Integer(q-j)
        result.append(S.expand(cardinal).coeff(Z, k)/S.binomial(d, k))
    return tuple(result)

def anti(poly, xs, axis):
    ans = 0
    for powers, coeff in S.Poly(poly, *xs).terms():
        altered = list(powers)
        altered[axis] += 1
        monomial = coeff / S.Integer(altered[axis])
        for x, power in zip(xs, altered):
            monomial *= x**power
        ans += monomial
    return S.expand(ans)

def decompose(vector, xs):
    """Construct shears from rational cardinal weights and antiderivatives."""
    n = len(xs)
    if n == 1:
        require(S.expand(S.diff(vector[0], xs[0])) == 0, 'n1_derivative')
        return [(vector[0], (S.Integer(1),))]
    require(S.expand(sum(S.diff(f,x) for f,x in zip(vector,xs))) == 0,
            'divergence_input')
    remaining = vector[-1]
    shears = []
    for i in range(n-1):
        H = anti(vector[i], xs, n-1)
        require(S.expand(S.diff(H, xs[-1])-vector[i]) == 0, 'antiderivative')
        remaining += S.diff(H, xs[i])
        for powers, coeff in S.Poly(H, *xs).terms():
            d, k = powers[i]+powers[-1], powers[-1]
            if d == 0:
                continue
            a = coeff
            for j, (x, power) in enumerate(zip(xs, powers)):
                if j != i and j != n-1:
                    a *= x**power
            for q, w in enumerate(weights(d,k)):
                if not w:
                    continue
                v = [S.Integer(0)]*n
                v[i], v[-1] = S.Integer(q), S.Integer(-1)
                h = S.expand(a*w*d*(xs[i]+q*xs[-1])**(d-1))
                shears.append((h,tuple(v)))
    remaining = S.expand(remaining)
    require(S.diff(remaining,xs[-1]) == 0, 'remaining_independence')
    if remaining:
        shears.append((remaining,tuple([S.Integer(0)]*(n-1)+[S.Integer(1)])))
    rebuilt = [sum(h*v[i] for h,v in shears) for i in range(n)]
    for old,new in zip(vector,rebuilt):
        require(S.expand(old-new) == 0, 'vector_reconstruction')
    for h,v in shears:
        translated = h.subs(dict(zip(xs,(x+s*a for x,a in zip(xs,v)))),
                            simultaneous=True)
        require(S.expand(translated-h) == 0, 'exact_shear_invariance')
        require(S.expand(sum(a*S.diff(h,x) for x,a in zip(xs,v))) == 0,
                'directional_derivative')
    return shears

class Quotient:
    """Sparse polynomials over Q[u]/u^2, with optional t^m quotient.

    Multiplication and substitution are implemented independently of SymPy's
    composition, so jet checking does not share the symbolic proof mechanism.
    """
    def __init__(self, xs, m):
        self.xs, self.n, self.m = xs, len(xs), m
        self.symbols = tuple(xs)+(t,u)
        self.zero = (0,)*(self.n+2)
        self.one = {self.zero:Fraction(1)}
        self.variables = []
        for i in range(self.n+2):
            powers = list(self.zero)
            powers[i] = 1
            self.variables.append({tuple(powers):Fraction(1)})
    def clean(self,p):
        return {a:c for a,c in p.items() if c and a[-1]<2 and
                (self.m is None or a[-2]<self.m)}
    def from_expr(self,e):
        p = {}
        for a,c in S.Poly(S.expand(e),*self.symbols).terms():
            p[a] = Fraction(int(S.numer(c)),int(S.denom(c)))
        return self.clean(p)
    def to_expr(self,p):
        out = 0
        for a,c in p.items():
            mon = S.Rational(c.numerator,c.denominator)
            for x,power in zip(self.symbols,a):
                mon *= x**power
            out += mon
        return out
    def add(self,*ps):
        out = {}
        for p in ps:
            for a,c in p.items():
                out[a] = out.get(a,Fraction(0))+c
        return self.clean(out)
    def scale(self,p,c):
        return self.clean({a:c*b for a,b in p.items()})
    def mul(self,p,q):
        out = {}
        for a,c in p.items():
            for b,d in q.items():
                powers = tuple(i+j for i,j in zip(a,b))
                if powers[-1]>=2 or (self.m is not None and powers[-2]>=self.m):
                    continue
                out[powers] = out.get(powers,Fraction(0))+c*d
        return self.clean(out)
    def power(self,p,k):
        out = self.one
        while k:
            if k&1:
                out = self.mul(out,p)
            p = self.mul(p,p)
            k >>= 1
        return out
    def subst(self,p,images):
        full = tuple(images)+tuple(self.variables[self.n:])
        cache = {}
        out = {}
        for a,c in p.items():
            term = {self.zero:c}
            for i,k in enumerate(a):
                if not k:
                    continue
                if (i,k) not in cache:
                    cache[i,k] = self.power(full[i],k)
                term = self.mul(term,cache[i,k])
                if not term:
                    break
            out = self.add(out,term)
        return out
    def compose(self,a,b):
        return tuple(self.subst(p,b) for p in a)
    def identity(self):
        return tuple(self.variables[:self.n])
    def mapping(self,exprs):
        return tuple(self.from_expr(e) for e in exprs)
    def derivative(self,p,i):
        out = {}
        for a,c in p.items():
            if a[i]:
                powers = list(a)
                powers[i] -= 1
                out[tuple(powers)] = c*a[i]
        return self.clean(out)
    def determinant(self,a):
        out = {}
        for perm in permutations(range(self.n)):
            inversions = sum(perm[i]>perm[j] for i in range(self.n)
                             for j in range(i+1,self.n))
            term = self.scale(self.one,(-1)**inversions)
            for i,j in enumerate(perm):
                term = self.mul(term,self.derivative(a[i],j))
            out = self.add(out,term)
        return out
    def next_coefficient(self,a,r):
        result=[]
        for p,x in zip(a,self.identity()):
            delta=self.add(p,self.scale(x,-1))
            require(all(power[-2]>=r for power in delta),'residual_order')
            selected={power[:self.n]+(0,power[-1]):c
                      for power,c in delta.items() if power[-2]==r}
            result.append(self.to_expr(selected))
        return result

def monomials(n,d):
    if n == 1:
        return [(d,)]
    return [(k,)+tail for k in range(d+1) for tail in monomials(n-1,d-k)]

def divergence_kernel(n,d,xs):
    mons=monomials(n,d)
    if d == 0:
        matrix=S.zeros(0,n)
    else:
        targets=monomials(n,d-1)
        row={a:i for i,a in enumerate(targets)}
        matrix=S.zeros(len(targets),n*len(mons))
        for i in range(n):
            for j,powers in enumerate(mons):
                if powers[i]:
                    lowered=list(powers)
                    lowered[i]-=1
                    matrix[row[tuple(lowered)],i*len(mons)+j]=powers[i]
    basis=matrix.nullspace()
    for vector in basis:
        result=[]
        for i in range(n):
            f=0
            for j,powers in enumerate(mons):
                mon=vector[i*len(mons)+j]
                for x,k in zip(xs,powers):
                    mon *= x**k
                f += mon
            result.append(S.expand(f))
        yield result

def run():
    X,Y=S.symbols('X Y')
    for d in range(10):
        for k in range(d+1):
            reconstructed=sum(w*(X+q*Y)**d for q,w in enumerate(weights(d,k)))
            require(S.expand(reconstructed-X**(d-k)*Y**k)==0,
                    'rational_interpolation')
    bases=0
    for n in range(2,5):
        xs=S.symbols('x0:'+str(n))
        for d in range(4):
            kernel=list(divergence_kernel(n,d,xs))
            expected=n*math.comb(n+d-1,d)-(math.comb(n+d-2,d-1) if d else 0)
            require(len(kernel)==expected,'kernel_dimension')
            for index,vector in enumerate(kernel):
                # Rational plus nilpotent coefficient. u is never inverted.
                multiplier=S.Rational(index+1,index+2)+u
                decompose([S.expand(multiplier*f) for f in vector],xs)
                bases += 1
            if kernel:
                combined=[sum((j+1+u*(-1)**j)*v[i] for j,v in enumerate(kernel))
                          for i in range(n)]
                decompose([S.expand(f) for f in combined],xs)
    exact_shear_cases=0
    for n in range(1,5):
        xs=S.symbols('x0:'+str(n))
        ring=Quotient(xs,None)
        candidates=[(S.Integer(3)+u,tuple([1]+[0]*(n-1)))]
        if n>=2:
            other=xs[1] if n>2 else 1
            for q in (-2,0,3):
                v=[0]*n
                v[0],v[-1]=q,-1
                h=(1+u)*other*(xs[0]+q*xs[-1])**2+u
                candidates.append((h,tuple(v)))
        for h,v in candidates:
            a=t+u*t**2
            forward=ring.mapping([x+a*h*c for x,c in zip(xs,v)])
            inverse=ring.mapping([x-a*h*c for x,c in zip(xs,v)])
            require(ring.compose(forward,inverse)==ring.identity(),'exact_inverse_left')
            require(ring.compose(inverse,forward)==ring.identity(),'exact_inverse_right')
            require(ring.determinant(forward)==ring.one,'exact_untruncated_determinant')
            exact_shear_cases += 1
    jet_cases=0
    jet_shear_count=0
    for n in range(1,4):
        xs=S.symbols('x0:'+str(n))
        for m in range(1,6):
            ring=Quotient(xs,m)
            identity=ring.identity()
            if n==1:
                base=ring.mapping([xs[0]+u+2])
                base_inverse=ring.mapping([xs[0]-u-2])
                templates=[(1+u,(1,),1),(2-u,(1,),2)]
            elif n==2:
                base=ring.mapping([xs[1]+u,-xs[0]])
                base_inverse=ring.mapping([-xs[1],xs[0]-u])
                templates=[(xs[1]**2+u*xs[1],(1,0),1),
                           (xs[0]+u*xs[0]**2,(0,1),2),
                           ((xs[0]+xs[1])**2+u,(1,-1),1)]
            else:
                base=ring.mapping([xs[1]+u,xs[2],xs[0]])
                base_inverse=ring.mapping([xs[2],xs[0]-u,xs[1]])
                templates=[(xs[1]+u*xs[2]**2,(1,0,0),1),
                           (xs[0]**2+u*xs[2],(0,1,0),2),
                           (xs[1]*(xs[0]+xs[2])+u,(1,0,-1),1)]
            require(ring.compose(base,base_inverse)==identity,'base_inverse')
            residual=identity
            for h,v,r in templates:
                E=ring.mapping([x+t**r*h*c for x,c in zip(xs,v)])
                residual=ring.compose(residual,E)
            sigma=ring.compose(base,residual)
            require(ring.determinant(sigma)==ring.one,'input_jet_determinant')
            residual=ring.compose(base_inverse,sigma)
            accumulated=base
            for r in range(1,m):
                F=ring.next_coefficient(residual,r)
                # F is canonical in the dual-number quotient, so equality is
                # checked over Q[u] without cancelling any ring coefficient.
                require(S.expand(sum(S.diff(f,x) for f,x in zip(F,xs)))==0,
                        'successive_divergence')
                shears=decompose(F,xs)
                phi,phi_inverse=identity,identity
                for h,v in shears:
                    E=ring.mapping([x+t**r*h*c for x,c in zip(xs,v)])
                    Ei=ring.mapping([x-t**r*h*c for x,c in zip(xs,v)])
                    require(ring.determinant(E)==ring.one,'correction_jet_determinant')
                    phi=ring.compose(phi,E)
                    phi_inverse=ring.compose(Ei,phi_inverse)
                    jet_shear_count += 1
                require(ring.compose(phi,phi_inverse)==identity,'correction_inverse')
                residual=ring.compose(phi_inverse,residual)
                for p,x in zip(residual,identity):
                    difference=ring.add(p,ring.scale(x,-1))
                    require(all(power[-2]>=r+1 for power in difference),'order_improved')
                accumulated=ring.compose(accumulated,phi)
                require(ring.compose(accumulated,residual)==sigma,'induction_invariant')
            require(residual==identity,'final_residual_identity')
            require(accumulated==sigma,'final_lift_reduces_exactly')
            jet_cases += 1
    # Four independently falsifiable mutations, plus a characteristic-p scope control.
    require(S.expand(S.diff(S.diff(X*Y,Y),X)+S.diff(S.diff(X*Y,X),Y))!=0,
            'mutant_hamiltonian_wrong_sign_rejected')
    malformed=sum(S.expand(S.prod((Z-j)/S.Integer(q-j)
                  for j in range(3) if j!=q)).coeff(Z,1)*(X+q*Y)**2
                  for q in range(3))
    require(S.expand(malformed-X*Y)!=0,'mutant_binomial_factor_omission_rejected')
    bad=Quotient((X,),None)
    f=bad.mapping([X+t*X])
    fi=bad.mapping([X-t*X])
    require(bad.compose(f,fi)!=bad.identity(),'mutant_noninvariant_inverse_rejected')
    require(bad.determinant(f)!=bad.one,'mutant_noninvariant_determinant_rejected')
    dual=Quotient((X,),None)
    require(dual.mul(dual.variables[-1],dual.variables[-1])=={},'nonreduced_nilpotent_square')
    require(dual.variables[-1]!={},'nonreduced_nilpotent_nonzero')
    # Characteristic 2: derivative of x^2 is 0; the truncated inverse
    # equality is checked in F_2[t,x]/t^2, outside the theorem.
    compose_char2=S.Poly(S.expand((X-t*X**2)+t*(X-t*X**2)**2),X,t,modulus=2)
    reduced=sum(S.Integer(int(c)%2)*X**a[0]*t**a[1]
                for a,c in compose_char2.terms() if a[1]<2)
    require(S.expand(reduced-X)==0,'characteristic2_truncated_inverse')
    require(S.Poly(S.diff(X+t*X**2,X)-1,X,t,modulus=2).is_zero,
            'characteristic2_determinant_one')
    out={'schema':'independent-divergence-shear-controls-v1',
         'status':'PASS','sympy_version':S.__version__,
         'total_assertions':sum(COUNTS.values()),'checks_by_kind':dict(sorted(COUNTS.items())),
         'divergence_kernel_basis_vectors':bases,
         'exact_untruncated_dual_number_shear_cases':exact_shear_cases,
         'dual_number_jet_cases':jet_cases,'jet_correction_shears':jet_shear_count,
         'coverage':{'rational_interpolation_degrees':'0..9',
                     'divergence_kernel':'n=2..4, homogeneous degrees=0..3; complete rational nullspace bases and combined vectors, with Q[u]/u^2 coefficients',
                     'jets':'n=1..3, m=1..5, supplied compositions and constant special bases over Q[u]/u^2',
                     'exact_shears':'n=1..4; inverse and determinant checked before any t truncation'},
         'limitations':['Finite computations supplement INDEPENDENT_PROOF.md; they do not enumerate all rings, dimensions or truncation lengths.',
                        'Complete composite lifts are checked as jets; their exact invertibility before reduction follows from the universal shear/product proof.',
                        'No author or historical independent checker is imported or rerun.']}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    run()
