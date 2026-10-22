#!/usr/bin/env python3
"""Dependency-free finite exact billiard controls; no universal theorem certificate.

All radicals use the positive real embedding of Q(sqrt(2),sqrt(3),sqrt(5),sqrt(13)).
Receipt writes occur only for an explicit --receipt PATH and use exclusive create.
"""
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from math import isqrt
import json
from pathlib import Path
import sys

PRIMES = (2, 3, 5, 13)
DIMENSION = 1 << len(PRIMES)
LIMITS = ('Finite exact controls for four specified polygons only. No universal '
          'analytic proof, interval certificate, novelty, priority, independent '
          'adversarial acceptance, Root acceptance, or publication conclusion.')

class VerificationError(Exception):
    pass

def require(condition, message):
    if type(condition) is not bool:
        raise TypeError('guard condition must be a bool')
    if not condition:
        raise VerificationError(message)

def rational(value):
    if type(value) is int:
        return Fraction(value)
    if type(value) is Fraction:
        return value
    raise TypeError('exact scalar must be int or Fraction, excluding bool and floats')

@dataclass(frozen=True)
class MQ:
    coefficients: tuple

    def __post_init__(self):
        if type(self.coefficients) is not tuple or len(self.coefficients) != DIMENSION:
            raise TypeError('field coefficient vector must be a 16-tuple')
        if any(type(c) is not Fraction for c in self.coefficients):
            raise TypeError('field coefficients must be exact Fraction values')

    def __bool__(self):
        raise TypeError('field truthiness is forbidden; compare exact values')

    def is_zero(self):
        return all(c == 0 for c in self.coefficients)

    def __add__(self, other):
        other = exact(other)
        return MQ(tuple(a+b for a,b in zip(self.coefficients, other.coefficients)))

    __radd__ = __add__

    def __neg__(self):
        return MQ(tuple(-a for a in self.coefficients))

    def __sub__(self, other):
        return self + (-exact(other))

    def __rsub__(self, other):
        return exact(other) + (-self)

    def __mul__(self, other):
        other = exact(other)
        out = [Fraction(0) for _ in range(DIMENSION)]
        for i,a in enumerate(self.coefficients):
            if a == 0:
                continue
            for j,b in enumerate(other.coefficients):
                if b == 0:
                    continue
                overlap = i & j
                factor = 1
                for bit,prime in enumerate(PRIMES):
                    if overlap & (1 << bit):
                        factor *= prime
                out[i ^ j] += a*b*factor
        return MQ(tuple(out))

    __rmul__ = __mul__

    def conjugate(self, bit):
        if type(bit) is not int or bit < 0 or bit >= len(PRIMES):
            raise TypeError('conjugation index must be an integer in 0..3')
        return MQ(tuple(-c if mask & (1 << bit) else c
                        for mask,c in enumerate(self.coefficients)))

    def inverse(self):
        if self.is_zero():
            raise ZeroDivisionError('zero exact field denominator')
        used = [i for i,c in enumerate(self.coefficients) if c != 0]
        maximum = max(used)
        if maximum == 0:
            return exact(1/self.coefficients[0])
        bit = maximum.bit_length()-1
        conjugate = self.conjugate(bit)
        norm = self*conjugate
        require(all(c == 0 for mask,c in enumerate(norm.coefficients)
                    if mask & (1 << bit)), 'conjugate norm failed to eliminate generator')
        return conjugate*norm.inverse()

    def __truediv__(self, other):
        return self*exact(other).inverse()

    def __rtruediv__(self, other):
        return exact(other)*self.inverse()

    def __eq__(self, other):
        return self.coefficients == exact(other).coefficients

    def __hash__(self):
        return hash(self.coefficients)

    def rational_value(self):
        require(all(c == 0 for c in self.coefficients[1:]),
                'this operation requires a rational field element')
        return self.coefficients[0]

    def sign(self):
        """Exact sign by rational enclosures with integer-square checked endpoints."""
        if self.is_zero():
            return 0
        for bits in (8,16,32,64,128,256,512,1024,2048,4096):
            scale = 1 << bits
            lower = Fraction(0)
            upper = Fraction(0)
            for mask,c in enumerate(self.coefficients):
                if c == 0:
                    continue
                radicand = basis_radicand(mask)
                floor = isqrt(radicand*scale*scale)
                lo = Fraction(floor,scale)
                hi = lo if floor*floor == radicand*scale*scale else Fraction(floor+1,scale)
                if c > 0:
                    lower += c*lo
                    upper += c*hi
                else:
                    lower += c*hi
                    upper += c*lo
            if lower > 0:
                return 1
            if upper < 0:
                return -1
        raise VerificationError('exact sign unresolved at finite enclosure budget')

    def json_value(self):
        return [{'radicand':basis_radicand(mask), 'coefficient':str(c)}
                for mask,c in enumerate(self.coefficients) if c != 0]

def exact(value):
    if type(value) is MQ:
        return value
    coeff = [Fraction(0) for _ in range(DIMENSION)]
    coeff[0] = rational(value)
    return MQ(tuple(coeff))

def basis_radicand(mask):
    if type(mask) is not int or not 0 <= mask < DIMENSION:
        raise TypeError('basis index must be integer in 0..15')
    result = 1
    for bit,prime in enumerate(PRIMES):
        if mask & (1 << bit):
            result *= prime
    return result

def basis(mask):
    basis_radicand(mask)
    coeff = [Fraction(0) for _ in range(DIMENSION)]
    coeff[mask] = Fraction(1)
    return MQ(tuple(coeff))

def sqrt_rational(value):
    value = rational(value)
    require(value > 0, 'edge squared length must be positive')
    residual = value.numerator*value.denominator
    coefficient = 1
    mask = 0
    for bit,prime in enumerate(PRIMES):
        exponent = 0
        while residual % prime == 0:
            residual //= prime
            exponent += 1
        coefficient *= prime**(exponent//2)
        if exponent % 2:
            mask |= 1 << bit
    rest = isqrt(residual)
    require(rest*rest == residual, 'edge length radical outside supported exact field')
    root = basis(mask)*Fraction(coefficient*rest,value.denominator)
    require(root*root == value and root.sign() == 1, 'positive edge square-root check failed')
    return root

def positive_integer(value, minimum=1):
    if type(minimum) is not int or minimum < 1:
        raise TypeError('integer minimum must be a positive int')
    if type(value) is not int:
        raise TypeError('integer parameter must be int, excluding bool and Fraction')
    require(value >= minimum, 'integer parameter below supported minimum')
    return value

def polygon(points):
    if type(points) not in (list,tuple):
        raise TypeError('polygon must be a finite list or tuple')
    require(len(points) >= 3, 'polygon must contain at least three vertices')
    out = []
    for point in points:
        if type(point) not in (list,tuple) or len(point) != 2:
            raise TypeError('each vertex must have exactly two exact coordinates')
        out.append((exact(point[0]),exact(point[1])))
    result = tuple(out)
    require(len(set(result)) == len(result), 'polygon vertices collide or repeat')
    return result

def dot(p,q):
    return p[0]*q[0]+p[1]*q[1]

def cross(p,q):
    return p[0]*q[1]-p[1]*q[0]

def subtract(p,q):
    return (p[0]-q[0],p[1]-q[1])

def signed_area(points, repetitions=1):
    points = polygon(points)
    repetitions = positive_integer(repetitions)
    cycle = points*repetitions
    total = exact(0)
    for i,p in enumerate(cycle):
        total += cross(p,cycle[(i+1) % len(cycle)])
    return total/2

def invert_polygon(points, focus, radius=1):
    points = polygon(points)
    focus = exact(focus)
    radius = rational(radius)
    require(radius > 0, 'inversion radius must be positive')
    out = []
    for x,y in points:
        dx = x-focus
        denominator = dx*dx+y*y
        require(denominator.sign() == 1, 'inversion denominator must be strictly positive')
        out.append((focus+radius*radius*dx/denominator,
                    radius*radius*y/denominator))
    return polygon(out)

EXPECTED_COUNTS = {
    'arithmetic_basis':4, 'arithmetic_inverse':3, 'arithmetic_sign':6,
    'arithmetic_distributivity':1, 'orbit_contract':4, 'primitive_vertices':4,
    'strict_confocal':4, 'outer_incidence':14, 'cyclic_edges':14,
    'edge_length':14, 'caustic_tangency':14, 'segment_tangency':14,
    'reflection_law':28, 'convex_winding':4, 'inversion_dot':28,
    'inversion_collinearity':28, 'area_expected':8, 'area_reversal':8,
    'area_repetition':8, 'area_radius_scaling':8, 'product_expected':4,
    'product_reversal':4, 'product_repetition':4, 'product_radius_scaling':4,
    'even_product_distinct':1, 'area_physical_similarity':8,
    'product_physical_similarity':4,
}

class Ledger:
    def __init__(self):
        self.counts = Counter()

    def check(self, group, condition):
        require(type(group) is str and group in EXPECTED_COUNTS, 'unknown check group')
        require(condition, 'failed exact check: '+group)
        self.counts[group] += 1

    def finish(self):
        require(dict(self.counts) == EXPECTED_COUNTS, 'exact group counts differ from fixed nonempty contract')
        require(all(type(n) is int and n > 0 for n in self.counts.values()), 'empty check group')
        return dict(sorted(self.counts.items()))

def validate_orbit(points, period, a2, b2, lam, ledger):
    period = positive_integer(period,3)
    points = polygon(points)
    ledger.check('orbit_contract',len(points) == period)
    ledger.check('primitive_vertices',len(set(points)) == period)
    a2,b2,lam = rational(a2),rational(b2),rational(lam)
    ledger.check('strict_confocal',0 < lam < b2 < a2)
    orientation = signed_area(points).sign()
    require(orientation in (-1,1), 'zero oriented base polygon')
    convex = True
    for i,p in enumerate(points):
        q = points[(i+1) % period]
        r = points[(i-1) % period]
        ledger.check('outer_incidence',p[0]*p[0]/a2+p[1]*p[1]/b2 == 1)
        edge = subtract(q,p)
        ledger.check('cyclic_edges',not dot(edge,edge).is_zero())
        outgoing_length = sqrt_rational(dot(edge,edge).rational_value())
        incoming = subtract(p,r)
        incoming_length = sqrt_rational(dot(incoming,incoming).rational_value())
        ledger.check('edge_length',outgoing_length*outgoing_length == dot(edge,edge))
        determinant = cross(p,q)
        require(not determinant.is_zero(), 'chord cannot be normalized to line dot X = 1')
        ell = ((q[1]-p[1])/determinant,(p[0]-q[0])/determinant)
        ledger.check('caustic_tangency',(a2-lam)*ell[0]*ell[0]+(b2-lam)*ell[1]*ell[1] == 1)
        contact = ((a2-lam)*ell[0],(b2-lam)*ell[1])
        fraction = dot(subtract(contact,p),edge)/dot(edge,edge)
        ledger.check('segment_tangency',fraction.sign() == 1 and (1-fraction).sign() == 1)
        normal = (p[0]/a2,p[1]/b2)
        din = (incoming[0]/incoming_length,incoming[1]/incoming_length)
        dout = (edge[0]/outgoing_length,edge[1]/outgoing_length)
        scale = 2*dot(din,normal)/dot(normal,normal)
        for coordinate in range(2):
            ledger.check('reflection_law',din[coordinate]-scale*normal[coordinate] == dout[coordinate])
        convex = convex and orientation*cross(p,q).sign() == 1
        for j,other in enumerate(points):
            if j not in (i,(i+1) % period):
                convex = convex and orientation*cross(edge,subtract(other,p)).sign() == 1
    ledger.check('convex_winding',convex and orientation == 1)
    return points

def fixed_controls():
    r2,r3,r5,r13 = (basis(1 << bit) for bit in range(4))
    return [
        {'name':'H','period':3,'lambda':Fraction(40,9),
         'vertices':[(2*r2,0),(-4*r2/3,Fraction(5,3)),(-4*r2/3,-Fraction(5,3))],
         'areas':[r2/10-r3/80,r2/10+r3/80],'product':Fraction(5,256),
         'provenance':'Original submitted triangle control.'},
        {'name':'V','period':3,'lambda':Fraction(40,9),
         'vertices':[(0,r5),(-Fraction(8,3),-r5/3),(Fraction(8,3),-r5/3)],
         'areas':[r5/16,r5/16],'product':Fraction(5,256),
         'provenance':'Original submitted triangle control.'},
        {'name':'diamond','period':4,'lambda':Fraction(40,13),
         'vertices':[(2*r2,0),(0,r5),(-2*r2,0),(0,-r5)],
         'areas':[r2*r5/10,r2*r5/10],'product':Fraction(1,10),
         'provenance':'Root post-exposure derivation; not independent discovery.'},
        {'name':'rectangle','period':4,'lambda':Fraction(40,13),
         'vertices':[(8*r13/13,5*r13/13),(-8*r13/13,5*r13/13),
                     (-8*r13/13,-5*r13/13),(8*r13/13,-5*r13/13)],
         'areas':[exact(Fraction(13,40)),exact(Fraction(13,40))],'product':Fraction(169,1600),
         'provenance':'Root post-exposure derivation; not independent discovery.'},
    ]

FAULTS = ('wrong-area','wrong-product','empty-polygon','colliding-polygon',
          'nan-coordinate','inf-coordinate','bool-coordinate','wrong-period',
          'bool-repetition','fraction-repetition','missing-count',
          'wrong-physical-area','wrong-physical-product')

def run_suite(fault=None):
    if fault is not None:
        require(type(fault) is str and fault in FAULTS, 'unknown fault injection')
    ledger = Ledger()
    radicals = [basis(1 << bit) for bit in range(4)]
    for root,prime in zip(radicals,PRIMES):
        ledger.check('arithmetic_basis',root*root == prime)
    samples = (1+radicals[0]+radicals[1]/2+radicals[2]/3+radicals[3]/4,
               radicals[3]/13,2-radicals[0])
    for value in samples:
        ledger.check('arithmetic_inverse',value*value.inverse() == 1)
    for value,expected in [(exact(0),0),(exact(1),1),(exact(-1),-1),
                           (2-radicals[0],1),(radicals[0]-2,-1),
                           (radicals[1]-radicals[0],1)]:
        ledger.check('arithmetic_sign',value.sign() == expected)
    x,y,z = samples
    ledger.check('arithmetic_distributivity',x*(y+z) == x*y+x*z)
    cases = fixed_controls()
    if fault == 'wrong-area':cases[0]['areas'][0] += 1
    elif fault == 'wrong-product':cases[0]['product'] += 1
    elif fault == 'empty-polygon':cases[0]['vertices'] = []
    elif fault == 'colliding-polygon':cases[0]['vertices'][1] = cases[0]['vertices'][0]
    elif fault in ('nan-coordinate','inf-coordinate','bool-coordinate'):
        bad = {'nan-coordinate':float('nan'),'inf-coordinate':float('inf'),'bool-coordinate':True}[fault]
        cases[0]['vertices'][0] = (bad,0)
    elif fault == 'wrong-period':cases[0]['period'] = Fraction(3)
    physical_scale = Fraction(3,2)
    results = []
    for case in cases:
        points = validate_orbit(case['vertices'],case['period'],8,5,case['lambda'],ledger)
        focal_areas = []
        reversed_areas = []
        repeated_areas = []
        scaled_areas = []
        physical_areas = []
        physical_points = [(physical_scale*x,physical_scale*y) for x,y in points]
        for index,focus in enumerate((radicals[1],-radicals[1])):
            image = invert_polygon(points,focus)
            for (x,y),(u,v) in zip(points,image):
                ledger.check('inversion_dot',(u-focus)*(x-focus)+v*y == 1)
                ledger.check('inversion_collinearity',(u-focus)*y-v*(x-focus) == 0)
            area = signed_area(image)
            ledger.check('area_expected',area == case['areas'][index])
            reverse = signed_area(invert_polygon(tuple(reversed(points)),focus))
            ledger.check('area_reversal',reverse == -area)
            repetitions = True if fault == 'bool-repetition' else Fraction(3) if fault == 'fraction-repetition' else 3
            repeated = signed_area(image,repetitions)
            ledger.check('area_repetition',repeated == 3*area)
            scaled = signed_area(invert_polygon(points,focus,2))
            ledger.check('area_radius_scaling',scaled == 16*area)
            # Physical similarity scales the orbit AND focus; inversion radius stays one.
            physical_area = signed_area(invert_polygon(physical_points,physical_scale*focus,1))
            physical_target = area/(physical_scale*physical_scale)
            if fault == 'wrong-physical-area' and case['name'] == 'H' and index == 0:
                physical_target += 1
            ledger.check('area_physical_similarity',physical_area == physical_target)
            physical_areas.append(physical_area)
            focal_areas.append(area)
            reversed_areas.append(reverse)
            repeated_areas.append(repeated)
            scaled_areas.append(scaled)
        product = focal_areas[0]*focal_areas[1]
        ledger.check('product_expected',product == case['product'])
        ledger.check('product_reversal',reversed_areas[0]*reversed_areas[1] == product)
        ledger.check('product_repetition',repeated_areas[0]*repeated_areas[1] == 9*product)
        ledger.check('product_radius_scaling',scaled_areas[0]*scaled_areas[1] == 256*product)
        physical_product = physical_areas[0]*physical_areas[1]
        physical_product_target = product/(physical_scale**4)
        if fault == 'wrong-physical-product' and case['name'] == 'H':
            physical_product_target += 1
        ledger.check('product_physical_similarity',physical_product == physical_product_target)
        results.append({'name':case['name'],'primitive_period':case['period'],'winding':1,
                        'lambda':str(case['lambda']),'focal_areas': [a.json_value() for a in focal_areas],
                        'product':product.json_value(),'provenance':case['provenance'],
                        'physical_similarity':{'scale':str(physical_scale),'inversion_radius':1,
                            'focal_areas':[a.json_value() for a in physical_areas],
                            'product':physical_product.json_value()}})
    ledger.check('even_product_distinct',exact(cases[2]['product']) != cases[3]['product'])
    if fault == 'missing-count':ledger.counts['outer_incidence'] -= 1
    counts = ledger.finish()
    return {'status':'PASS','mode':'finite_exact_standard_library','counts':counts,
            'total_checks':sum(counts.values()),'expected_counts':dict(sorted(EXPECTED_COUNTS.items())),
            'all_groups_nonempty':True,'field_primes':list(PRIMES),'outer_squared_axes':['8','5'],
            'physical_similarity_scale':str(physical_scale),
            'focus_coordinates': [{'sign':1,'radicand':3},{'sign':-1,'radicand':3}],
            'controls':results,'limits':LIMITS}

def parse_cli(argv):
    if type(argv) is not list or any(type(a) is not str for a in argv):
        raise TypeError('CLI arguments must be strings')
    if argv == ['--help']:
        return {'help':True,'receipt':None,'fault':None}
    out = {'help':False,'receipt':None,'fault':None}
    i = 0
    while i < len(argv):
        key = argv[i]
        require(key in ('--receipt','--fault'), 'unknown command-line argument')
        require(i+1 < len(argv), 'missing command-line value')
        name = key[2:]
        require(out[name] is None, 'duplicate command-line argument')
        value = argv[i+1]
        require(bool(value) and '\x00' not in value, 'empty or invalid command-line value')
        out[name] = value
        i += 2
    if out['fault'] is not None:
        require(out['fault'] in FAULTS, 'unknown fault injection')
    return out

def write_exclusive_receipt(destination, serialized):
    if type(serialized) is not str:
        raise TypeError('serialized receipt must be a string')
    if type(destination) is not str:
        raise TypeError('receipt destination must be an explicit string path')
    require(bool(destination) and '\x00' not in destination, 'invalid receipt destination')
    path = Path(destination)
    require(path.parent.is_dir(), 'receipt parent must already exist')
    # Exclusive mode rejects existing files, directories and symlink collisions.
    with path.open('x',encoding='utf-8') as handle:
        handle.write(serialized)
        handle.flush()

def runtime_binding():
    return {'python':sys.version,'flags':repr(sys.flags),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    runtime = {'python':sys.version,'flags':repr(sys.flags)}
    try:
        runtime.update(runtime_binding())
        options = parse_cli(argv)
        if options['help']:
            result = {'status':'HELP','usage':'python portable_exact_verifier.py [--receipt PATH] [--fault NAME]',
                      'faults':list(FAULTS),'limits':LIMITS,'runtime':runtime}
        else:
            result = run_suite(options['fault'])
            result['runtime'] = runtime
        serialized = json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+'\n'
        if options['receipt'] is not None:
            write_exclusive_receipt(options['receipt'],serialized)
        sys.stdout.write(serialized)
        return 0
    except Exception as error:
        failure = {'status':'FAIL','error_type':type(error).__name__,'error':str(error),
                   'runtime':runtime,'limits':LIMITS}
        sys.stdout.write(json.dumps(failure,sort_keys=True,indent=2,allow_nan=False)+'\n')
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
