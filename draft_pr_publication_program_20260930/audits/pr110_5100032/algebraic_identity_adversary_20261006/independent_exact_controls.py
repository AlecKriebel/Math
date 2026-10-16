"""Purposeful exact unit-normal controls; no author code or floating arithmetic.

Standard-library rational quadratic fields suffice for the hand-selected cases.
Checks are explicit exceptions, so Python -O cannot disable them.
"""
from fractions import Fraction as F
import json
import os
import sys


class K:
    """A rational element x+y*sqrt(d), d a fixed positive nonsquare integer."""
    def __init__(self, d, x=0, y=0):
        self.d, self.x, self.y = d, F(x), F(y)

    def coerce(self, other):
        if isinstance(other, K):
            if self.d != other.d:
                raise ValueError('Incompatible exact fields')
            return other
        return K(self.d, other)

    def __add__(self, other):
        other = self.coerce(other)
        return K(self.d, self.x+other.x, self.y+other.y)
    __radd__ = __add__

    def __neg__(self):
        return K(self.d, -self.x, -self.y)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return K(self.d, self.x*other.x+self.d*self.y*other.y,
                 self.x*other.y+self.y*other.x)
    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        denominator = other.x*other.x-self.d*other.y*other.y
        if not denominator:
            raise ZeroDivisionError('Exact zero denominator')
        return self * K(self.d, other.x/denominator, -other.y/denominator)

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __eq__(self, other):
        other = self.coerce(other)
        return self.x == other.x and self.y == other.y

    def __pow__(self, exponent):
        if exponent != 2:
            raise ValueError('Only squaring used in this exact audit')
        return self*self

    def sign(self):
        if not self.y:
            return (self.x > 0)-(self.x < 0)
        if not self.x:
            return (self.y > 0)-(self.y < 0)
        if self.x > 0 and self.y > 0:
            return 1
        if self.x < 0 and self.y < 0:
            return -1
        difference = self.x*self.x-self.d*self.y*self.y
        if not difference:
            return 0
        if self.x > 0:
            return 1 if difference > 0 else -1
        return -1 if difference > 0 else 1

    def encode(self):
        return {'rational': str(self.x), 'sqrt_coefficient': str(self.y),
                'radicand': self.d}


CHECKS = 0
NEGATIVE_CONTROLS = []


def check(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError('Failed independent exact control: '+label)


def negative(condition, label):
    check(condition, label)
    NEGATIVE_CONTROLS.append(label)


def dot(x, y):
    return x[0]*y[0]+x[1]*y[1]


def cross(x, y):
    return x[0]*y[1]-x[1]*y[0]


def direct_antipedal(A, B, focal_x):
    X = (A[0]-focal_x, A[1])
    Y = (B[0]-focal_x, B[1])
    determinant = cross(X, Y)
    if determinant == 0:
        return None
    r2, s2 = dot(X, X), dot(Y, Y)
    Z = ((r2*Y[1]-s2*X[1])/determinant,
         (X[0]*s2-Y[0]*r2)/determinant)
    check(dot(Z, X) == r2, 'direct perpendicular equation at A')
    check(dot(Z, Y) == s2, 'direct perpendicular equation at B')
    return Z, dot(Z, Z), determinant


def make_case(name, a, b, c, u, v, rho, root_lambda):
    return dict(name=name, a=F(a), b=F(b), c=F(c), u=F(u), v=F(v),
                rho=rho, root_lambda=root_lambda)


def verify_case(case):
    a,b,c,u,v,rho,root = [case[k] for k in
                         ('a','b','c','u','v','rho','root_lambda')]
    H2 = a*a*u*u+b*b*v*v
    lam = root*root
    check(lam.y == 0, 'rational lambda')
    lam = lam.x
    kappa = b*b-lam
    check(a >= b > 0 and c*c == a*a-b*b, 'ellipse/focal parameters')
    check(u*u+v*v == 1, 'unit outward normal')
    check(0 < lam < b*b, 'strict elliptical caustic range')
    check(rho.sign() > 0 and root.sign() > 0, 'positive support and sqrt(lambda)')
    check(rho*rho == H2-lam, 'confocal caustic support')
    center = (rho*a*a*u/H2, rho*b*b*v/H2)
    half = a*b*root/H2
    tangent = (-v,u)
    A = (center[0]-half*tangent[0],center[1]-half*tangent[1])
    B = (center[0]+half*tangent[0],center[1]+half*tangent[1])
    for P in (A,B):
        check(P[0]*P[0]/(a*a)+P[1]*P[1]/(b*b) == 1,
              'chord endpoint on outer ellipse')
        check(u*P[0]+v*P[1] == rho, 'support line at endpoint')
    T = ((a*a-lam)*u/rho,(b*b-lam)*v/rho)
    check(T[0]*T[0]/(a*a-lam)+T[1]*T[1]/(b*b-lam) == 1,
          'contact point on actual inner ellipse')
    check(u*T[0]+v*T[1] == rho, 'support line touches inner ellipse')
    check(T[0]/(a*a-lam)*v == T[1]/(b*b-lam)*u,
          'inner ellipse gradient parallel to chord normal')
    check(cross((B[0]-A[0],B[1]-A[1]),(-A[0],-A[1])).sign() > 0,
          'caustic center strictly left of directed chord')
    hs,qs = [],[]
    for sigma in (1,-1):
        h = rho-sigma*c*u
        check(h.sign() > 0, 'strict positive ordinary focal height')
        r = a-sigma*c*A[0]/a
        s = a-sigma*c*B[0]/a
        check(r.sign() > 0 and s.sign() > 0, 'positive endpoint focal distances')
        check((A[0]-sigma*c)**2+A[1]**2 == r*r,
              'first endpoint actual focal norm')
        check((B[0]-sigma*c)**2+B[1]**2 == s*s,
              'second endpoint actual focal norm')
        product = r*s
        check(product == (a*a*h*h+b*b*lam)/H2,
              'independent support-coordinate focal product')
        q = product/h
        check(q.sign() > 0, 'ordinary unsigned antipedal norm candidate')
        solved = direct_antipedal(A,B,sigma*c)
        check(solved is not None, 'nonsingular actual antipedal intersection')
        Z,q2,determinant = solved
        check(q*q == q2, 'positive expression equals direct antipedal norm')
        check(determinant == 2*half*h, 'direct determinant and focal height')
        check(q == (a*a*h+b*b*lam/h)/H2,
              'positive antipedal distance support expression')
        check(q == ((a*a+b*b*lam/kappa)*rho+
                    sigma*c*(-a*a+b*b*lam/kappa)*u)/H2,
              'rationalized expression for each focus')
        hs.append(h); qs.append(q)
    check(hs[0]*hs[1] == kappa, 'strict positive focal-height product')
    delta_y = B[1]-A[1]
    coefficient = c*(-a*a+b*b*lam/kappa)/(a*b*root)
    check(delta_y == 2*a*b*root*u/H2, 'actual vertical displacement')
    check(qs[0]-qs[1] == coefficient*delta_y,
          'direct antipedal norm difference equals telescoping displacement')
    if u and coefficient.sign():
        negative(qs[0]-qs[1] != -coefficient*delta_y,
                 case['name']+': wrong coefficient sign detected')
        negative(qs[0]-qs[1] != coefficient*delta_y/2,
                 case['name']+': missing factor two detected')
        negative(qs[0]*qs[0]-qs[1]*qs[1] != coefficient*delta_y,
                 case['name']+': squared-norm substitution detected')
        check(qs[0]-qs[1] == -coefficient*(A[1]-B[1]),
              'reversed orientation requires reversed coefficient')
    if case['name'].startswith('zero_coefficient'):
        check(coefficient == 0 and qs[0] == qs[1], 'zero coefficient is valid')
    if case['name'] == 'circle':
        check(qs[0] == a*a/rho and qs[0] == qs[1], 'circle limit directly valid')
    return {'case':case['name'],'axes':[str(a),str(b)],'normal':[str(u),str(v)],
            'lambda':str(lam),'kappa':str(kappa),
            'rho':rho.encode(),'focal_heights':[h.encode() for h in hs],
            'ordinary_distances':[q.encode() for q in qs],
            'coefficient':coefficient.encode(),'delta_y':delta_y.encode()}


def main():
    cases = [
        make_case('vertical_normal',5,3,4,0,1,K(5,2),K(5,0,1)),
        make_case('negative_vertical_normal',5,3,4,0,-1,K(5,2),K(5,0,1)),
        make_case('horizontal_negative_coefficient',5,3,4,1,0,K(19,F(9,2)),K(19,0,F(1,2))),
        make_case('negative_horizontal_normal',5,3,4,-1,0,K(19,F(9,2)),K(19,0,F(1,2))),
        make_case('mixed_quadrant_1',5,3,4,F(3,5),F(4,5),K(2,3),K(2,F(12,5))),
        make_case('mixed_quadrant_2',5,3,4,F(-3,5),F(4,5),K(2,3),K(2,F(12,5))),
        make_case('mixed_quadrant_3',5,3,4,F(-3,5),F(-4,5),K(2,3),K(2,F(12,5))),
        make_case('mixed_quadrant_4',5,3,4,F(3,5),F(-4,5),K(2,3),K(2,F(12,5))),
        make_case('positive_coefficient',5,3,4,1,0,K(111,F(17,4)),K(111,0,F(1,4))),
        make_case('zero_coefficient_horizontal',5,3,4,1,0,K(34,0,F(25,34)),K(34,0,F(15,34))),
        make_case('zero_coefficient_vertical',5,3,4,0,1,K(34,0,F(9,34)),K(34,0,F(15,34))),
        make_case('near_outer_caustic',5,3,4,1,0,K(9999,F(4999,1000)),K(9999,0,F(1,1000))),
        make_case('near_degenerate_caustic',5,3,4,1,0,K(8991999,F(4001,1000)),K(8991999,0,F(1,1000))),
        make_case('circle',3,3,0,F(3,5),F(4,5),K(5,2),K(5,0,1)),
        make_case('uniform_scaling',10,6,8,F(3,5),F(4,5),K(2,6),K(2,F(24,5))),
    ]
    results = [verify_case(case) for case in cases]
    check(results[4]['coefficient'] == results[14]['coefficient'],
          'coefficient is dimensionless under uniform scaling')
    for focus in (0,1):
        original = results[4]['ordinary_distances'][focus]
        scaled = results[14]['ordinary_distances'][focus]
        check(F(scaled['rational']) == 2*F(original['rational']) and
              F(scaled['sqrt_coefficient']) == 2*F(original['sqrt_coefficient']),
              'ordinary focal distance scales by length')
    z = K(2,0)
    degenerate = ((K(2,5),z),(K(2,5),z))
    negative(direct_antipedal(*degenerate,4) is None,
             'lambda zero: repeated chord endpoint singularity detected')
    # lambda=b^2: line x=c meets the degenerate focal caustic at a focus.
    degenerate = ((K(2,4),K(2,F(-9,5))),
                  (K(2,4),K(2,F(9,5))))
    negative(direct_antipedal(*degenerate,4) is None,
             'lambda b squared: focal antipedal singularity detected')
    # A chord beyond the permitted elliptic range exposes the absolute-height issue.
    A,B = (K(2,3),K(2,F(-12,5))), (K(2,3),K(2,F(12,5)))
    plus = F(169,25)
    minus = F(1369,175)
    solved_plus,solved_minus = direct_antipedal(A,B,4),direct_antipedal(A,B,-4)
    check(solved_plus[1] == plus*plus and solved_minus[1] == minus*minus,
          'outside-range ordinary norms independently solved')
    negative(plus-minus != -plus-minus,
             'lambda above b squared: signed-height extension fails')
    print(json.dumps({'schema':'pr110-independent-purposeful-exact-controls/v1',
                      'PID':os.getpid(),'python':sys.version,'optimized':bool(sys.flags.optimize),
                      'checks':CHECKS,'purposeful_admissible_cases':len(cases),
                      'negative_controls_detected':len(NEGATIVE_CONTROLS),
                      'negative_controls':NEGATIVE_CONTROLS,'all_passed':True,
                      'author_code_or_verifier_imported':False,'cases':results},indent=2))


if __name__ == '__main__':
    main()
