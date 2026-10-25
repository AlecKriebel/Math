#!/usr/bin/env python3
"""Fresh analytic-review controls. Standard library only; no submitted imports.

Fraction checks audit proof margins. Decimal complex arithmetic independently
evaluates the nonlinear natural-coordinate inverse with an integrated binomial
series. These samples supplement the uniform proof; no extremizer is computed.
"""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json


class C:
    def __init__(self, x=0, y=0):
        self.x, self.y = D(x), D(y)

    @staticmethod
    def coerce(z):
        return z if isinstance(z, C) else C(z)

    def __add__(self, z):
        z = C.coerce(z)
        return C(self.x + z.x, self.y + z.y)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.x, -self.y)

    def __sub__(self, z):
        return self + (-C.coerce(z))

    def __rsub__(self, z):
        return C.coerce(z) - self

    def __mul__(self, z):
        z = C.coerce(z)
        return C(self.x*z.x - self.y*z.y, self.x*z.y + self.y*z.x)

    __rmul__ = __mul__

    def __truediv__(self, z):
        z = C.coerce(z)
        q = z.x*z.x + z.y*z.y
        return C((self.x*z.x + self.y*z.y)/q,
                 (self.y*z.x - self.x*z.y)/q)

    def __rtruediv__(self, z):
        return C.coerce(z) / self

    def __pow__(self, n):
        result = C(1)
        for _ in range(n):
            result = result*self
        return result

    def sqrt(self):
        # Positive real part; y/(2r) avoids subtraction of nearly equal terms.
        r = (((self.x*self.x+self.y*self.y).sqrt()+self.x)/2).sqrt()
        return C(r, self.y/(2*r))

    def norm1(self):
        return abs(self.x)+abs(self.y)


def poly_mul(a, b):
    c = [C() for _ in range(len(a)+len(b)-1)]
    for j, x in enumerate(a):
        for k, y in enumerate(b):
            c[j+k] = c[j+k]+x*y
    return c


def poly_eval(a, z):
    value = C()
    for x in reversed(a):
        value = value*z+x
    return value


def evaluate_case(label, A, B, coefficient4=1, epsilon='1e-24'):
    E = D(epsilon)
    # x(v)=P(v)-1 = i E (A-Bv^2+c4 v^4).
    x = [C(0, E)*A, C(), -C(0, E)*B, C(), C(0, E)*coefficient4]
    # Compute the primitive of sqrt(1+x) through x^4 independently of d,q.
    power, primitive, choose = [C(1)], [C(), C(1)], D(1)
    for k in range(1, 5):
        power = poly_mul(power, x)
        choose *= (D('1.5')-k)/k
        while len(primitive) < len(power)+1:
            primitive.append(C())
        for j, c in enumerate(power):
            primitive[j+1] = primitive[j+1]+choose*c/(j+1)
    samples = []
    for t in (D(1), D(7)/4):
        v = C(t)
        for _ in range(8):
            p = (1+poly_eval(x, v)).sqrt()
            v = v - (poly_eval(primitive, v)-t)/p
        p = (1+poly_eval(x, v)).sqrt()
        z = t/(v*p)
        residual = (poly_eval(primitive, v)-t).norm1()
        samples.append({'t':str(t), 'Im_Z_over_epsilon':str(z.y/E) if E else str(z.y),
                        'Re_Z':str(z.x), 'primitive_residual':str(residual)})
    return {'label':label,'samples':samples,
            'reversal':D(samples[0]['Im_Z_over_epsilon'])*D(samples[1]['Im_Z_over_epsilon'])<0}


def run(precision):
    with localcontext() as context:
        context.prec = precision
        H = D('1e-12')
        cases = [evaluate_case('central enclosure values', C(-2), C(3))]
        # All 16 combinations of independent cardinal-direction uncertainty.
        # Some may not be realizable coefficients of an extremizer.
        dirs = [C(1),C(-1),C(0,1),C(0,-1)]
        for j,u in enumerate(dirs):
            for k,v in enumerate(dirs):
                cases.append(evaluate_case(f'enclosure cardinal {j},{k}',
                             C(-2)+106*H*u, C(3)+24*H*v))
        controls = [evaluate_case('a4 only: omit -3a3', C(10),C(6)),
                    evaluate_case('a3 only', C(4),C(1),0),
                    evaluate_case('epsilon=0', C(-2),C(3),1,'0')]
        assert all(c['reversal'] for c in cases)
        assert not any(c['reversal'] for c in controls)
        return {'precision':precision,'nonlinear_samples':cases,'negative_controls':controls}


def exact_controls():
    h,e,T=F(1,10**12),F(1,10**24),F(7,4)
    # Separate exact audit, deliberately expressed as margins.
    margins = {
        'a2 norm enclosure':64-52,
        'a3 area enclosure':25-F(52,3),
        'H disk error':5-(F(8,3)+2),
        'Hprime disk error_squared_tail':F(9,4)-F(56,25),
        'f value error':2-F(28,15),
        'f derivative first error':6-F(152,27),
        'f derivative second error':2-F(88,75),
        'tip error coefficient':7-(2+F(40,9)),
        'tip below radius gate':F(3,10)-(F(7,25)+7*h),
        'actual versus candidate radius gap':F(25,81)-F(3,10),
        'P closeness margin':111-(110+322*h),
        'Rouche disk boundary separation':1-333*e,
        'sqrt remainder allowance':1-F(111**2,2)*h,
        'inverse remainder allowance':1-18315*h,
        'derivative remainder allowance':1-45621*h,
        'Z remainder allowance':2000-(1541+4662*h),
        'endpoint1 beyond half':F(3,5)-2000*h-F(1,2),
        'endpointT beyond half':F(441,640)-2000*h-F(1,2),
        'orientation bound':223*e-F(222)*e/(1-111*e),
        'first variation zero lies between endpoints lower':F(5,2)-1,
        'first variation zero lies between endpoints upper':T*T-F(5,2),
    }
    assert all(x>0 for x in margins.values())
    q=lambda t:t*t-F(2,5)*t**4
    assert q(F(1))==F(3,5) and q(T)==-F(441,640)
    mutations={
        'remove quartic q term':not (F(1)*T*T<0),
        'remove -3a3 functional term':not ((2-F(2,5))*(2*T*T-F(2,5)*T**4)<0),
        'raise eta to 1e-4 without reproof':not (1-45621*F(1,10**4)>0),
        'reverse candidate-tip ordering':not (F(3,10)>F(25,81)),
        'claim strict sign at epsilon zero':not (F(0)*q(1)>0),
        'identify inward tangent as outward':not (-2>0),
    }
    assert all(mutations.values())
    return {'positive_margins':{k:str(v) for k,v in margins.items()},
            'mutations_rejected':mutations,
            'q_endpoint_values':[str(q(F(1))),str(q(T))]}


if __name__=='__main__':
    numerical=[run(100),run(130)]
    # Stability at 65 decimal places after division by epsilon.
    differences=[]
    with localcontext() as context:
        context.prec=140
        for low,high in zip(numerical[0]['nonlinear_samples'],numerical[1]['nonlinear_samples']):
            for a,b in zip(low['samples'],high['samples']):
                difference=abs(D(a['Im_Z_over_epsilon'])-D(b['Im_Z_over_epsilon']))
                assert difference<D('1e-65')
                differences.append(difference)
    print(json.dumps({'status':'passed','exact':exact_controls(),'numerical':numerical,
                     'maximum_precision_difference':str(max(differences)),
                     'limits':'Decimal samples are supplemental, not interval proofs or maximizing maps. Analytic proof supplies uniformity and actual slit identification.'},indent=2))
