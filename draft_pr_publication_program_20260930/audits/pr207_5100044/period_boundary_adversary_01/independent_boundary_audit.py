"""Independent exact audit; never imports or executes the proposed checker.

Run: /opt/homebrew/bin/python3.11 independent_boundary_audit.py
Outputs only inside this audit directory.  SymPy is used for exact radical
arithmetic, and the continuous-family proof is recorded in PROOF.md.
"""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sympy as sp

R = sp.Rational
sqrt = sp.sqrt
HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'inputs'
checks = []

def exact_zero(expression, label):
    residual = sp.simplify(sp.radsimp(expression))
    assert residual == 0, (label, residual)
    checks.append(label)

def strict_positive(expression, label):
    expression = sp.simplify(expression)
    assert expression.is_positive is True, (label, expression)
    checks.append(label)

def dot(a, b):
    return (a.T * b)[0]

def determinant(a, b):
    return sp.det(sp.Matrix.hstack(a, b))

def triangle_area(vertices):
    a, b, c = vertices
    return sp.simplify(determinant(b-a, c-a)/2)

def winding_area(vertices):
    return sp.simplify(sum(determinant(p, vertices[(i+1) % len(vertices)])
                           for i, p in enumerate(vertices))/2)

def normal(point):
    return sp.Matrix([point[0]/8, point[1]/5])

def unit(vector):
    return sp.simplify(vector / sqrt(dot(vector, vector)))

A, B = sp.Integer(8), sp.Integer(5)
alpha, beta = R(32, 9), R(5, 9)
lam = A-alpha
focus = sp.Matrix([sqrt(3), 0])
p = [sp.Matrix([2*sqrt(2), 0]),
     sp.Matrix([-4*sqrt(2)/3, R(5, 3)]),
     sp.Matrix([-4*sqrt(2)/3, -R(5, 3)])]
minus_p = [-point for point in p]
exact_zero((A-B)-(alpha-beta), 'confocal squared-axis difference')
exact_zero(lam-(B-beta), 'same confocal parameter in each axis')
for value, label in [(alpha, 'inner first squared semiaxis'),
                     (beta, 'inner second squared semiaxis'),
                     (A-alpha, 'strict first-axis nesting'),
                     (B-beta, 'strict second-axis nesting')]:
    strict_positive(value, label)

orbits = {}
for name, vertices in [('P', p), ('minusP', minus_p)]:
    assert len({tuple(point) for point in vertices}) == 3
    checks.append(name + ': three distinct collision vertices')
    contacts, distances, inverse = [], [], []
    for i, point in enumerate(vertices):
        label = f'{name} vertex {i}'
        exact_zero(point[0]**2/A+point[1]**2/B-1, label + ': outer ellipse')
        previous = vertices[(i-1) % 3]
        following = vertices[(i+1) % 3]
        incoming = unit(point-previous)
        outgoing = unit(following-point)
        n = normal(point)
        reflection = incoming - 2*dot(incoming, n)/dot(n, n)*n
        for coordinate in range(2):
            exact_zero(reflection[coordinate]-outgoing[coordinate],
                       label + f': reflection coordinate {coordinate}')
        exact_zero(dot(n, incoming)-R(1,3), label + ': incoming normal dot')
        exact_zero(dot(n, outgoing)+R(1,3), label + ': outgoing normal dot')
        edge = following-point
        line_n = sp.Matrix([-edge[1], edge[0]])
        line_c = dot(line_n, point)
        exact_zero(alpha*line_n[0]**2+beta*line_n[1]**2-line_c**2,
                   label + ': dual-conic tangency')
        contact = sp.simplify(sp.Matrix([alpha*line_n[0], beta*line_n[1]])/line_c)
        parameter = sp.simplify(dot(contact-point, edge)/dot(edge, edge))
        for coordinate in range(2):
            exact_zero(contact[coordinate]-point[coordinate]-parameter*edge[coordinate],
                       label + f': contact on line coordinate {coordinate}')
        exact_zero(contact[0]**2/alpha+contact[1]**2/beta-1,
                   label + ': contact on inner ellipse')
        strict_positive(parameter, label + ': contact beyond first endpoint')
        strict_positive(1-parameter, label + ': contact before second endpoint')
        contacts.append({'point': list(map(str, contact)), 'segment_parameter': str(parameter)})
        relative = point-focus
        distance = sp.expand(dot(relative, relative))
        strict_positive(distance, label + ': inversion denominator')
        distances.append(distance)
        inverse.append(sp.simplify(relative/distance))
    signed_area = triangle_area(vertices)
    inverse_area = sp.radsimp(triangle_area(inverse))
    relative = [point-focus for point in vertices]
    inverse_homogeneous = sp.radsimp(sum(determinant(relative[i], relative[(i+1)%3])*distances[(i+2)%3]
                                      for i in range(3))/(2*sp.prod(distances)))
    exact_zero(inverse_homogeneous-inverse_area, name + ': homogeneous inverse-area crosscheck')
    exact_zero(winding_area(vertices)-signed_area, name + ': area determinant crosscheck')
    strict_positive(signed_area, name + ': positive orientation')
    strict_positive(inverse_area, name + ': positive inverse signed area')
    repeated = vertices*4
    repeated_inverse = inverse*4
    exact_zero(winding_area(repeated)-4*signed_area, name + ': repeated area scales by four')
    exact_zero(winding_area(repeated_inverse)-4*inverse_area, name + ': repeated inverse area scales by four')
    product = sp.simplify(sp.expand(signed_area*inverse_area))
    repeated_product = sp.simplify(sp.expand(winding_area(repeated)*winding_area(repeated_inverse)))
    exact_zero(repeated_product-16*product, name + ': product scales by sixteen')
    orbits[name] = {'contacts': contacts, 'inversion_denominators': list(map(str, distances)),
                    'signed_area': str(signed_area), 'inverse_signed_area': str(inverse_area),
                    'product': str(product), 'four_traversal_product': str(repeated_product),
                    'least_collision_period': 3, 'displayed_length': 12}

assert {tuple(point) for point in p}.isdisjoint({tuple(point) for point in minus_p})
checks.append('the two collision vertex sets are disjoint; no cyclic relabeling identifies the orbits')
base_difference = sp.simplify(sp.sympify(orbits['P']['product'])-sp.sympify(orbits['minusP']['product']))
repeated_difference = sp.simplify(sp.sympify(orbits['P']['four_traversal_product'])-
                                 sp.sympify(orbits['minusP']['four_traversal_product']))
strict_positive(-base_difference, 'base product difference strictly negative')
exact_zero(repeated_difference-16*base_difference, 'product difference scales by sixteen')

# Algebraic core of the independent continuous-family construction.
X, Y = sp.symbols('X Y', real=True)
D = 9*X**2+36*Y**2
S = sqrt(D-4)
r = sp.Matrix([(-6*X-6*Y*S)/D, (-12*Y+3*X*S)/D])
s = sp.Matrix([(-6*X+6*Y*S)/D, (-12*Y-3*X*S)/D])
for name, point in [('r', r), ('s', s)]:
    exact_zero(dot(point, point)-1, name + ': explicit neighbor is on normalized circle')
    exact_zero(3*X*point[0]+6*Y*point[1]+2,
               name + ': explicit neighbor obeys tangent chord relation')
scale = sp.diag(2*sqrt(2), sqrt(5))
for i, point in enumerate([sp.Matrix([X,Y]), r, s]):
    endpoint0 = scale*point.subs({X: 1, Y: 0})
    endpoint_pi = scale*point.subs({X: -1, Y: 0})
    for coordinate in range(2):
        exact_zero(endpoint0[coordinate]-p[i][coordinate], f'family vertex {i}: theta zero is P coordinate {coordinate}')
        exact_zero(endpoint_pi[coordinate]+p[i][coordinate], f'family vertex {i}: theta pi is minusP coordinate {coordinate}')
theta, phi = sp.symbols('theta phi', real=True)
chord_support = (9*sp.cos((phi-theta)/2)**2-4*sp.cos((phi+theta)/2)**2-sp.sin((phi+theta)/2)**2)
chord_relation = 2+3*sp.cos(theta)*sp.cos(phi)+6*sp.sin(theta)*sp.sin(phi)
exact_zero(sp.trigsimp(sp.expand_trig(chord_support-chord_relation)),
           'normalized caustic support equation equals bilinear chord relation')
rxsx = (4-36*Y**2)/D
rysy = (4-9*X**2)/D
exact_zero(r[0]*s[0]-rxsx, 'explicit neighbors x-coordinate product')
exact_zero(r[1]*s[1]-rysy, 'explicit neighbors y-coordinate product')
exact_zero((3*rxsx+6*rysy+2).subs(X**2, 1-Y**2),
           'two tangent neighbors are themselves joined by a tangent chord')

# The same-caustic directions have equal absolute normal component:
# A n_x^2+B n_y^2-(n dot p)^2 = AB (N dot v)^2 on E.
x, y, u, v = sp.symbols('x y u v', real=True)
left = A*v**2+B*u**2-(-v*x+u*y)**2
right = A*B*(x*u/A+y*v/B)**2
residual = sp.expand(left-right)
exact_zero(sp.expand(residual.subs(y**2, B*(1-x**2/A))),
           'confocal support identity implies the exact Euclidean reflection rule')

source_pins = {name: {'bytes': len((SOURCE/name).read_bytes()),
                      'sha256': hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()}
               for name in ('exact_repetition_boundary_v2.py', 'EXACT_BOUNDARY_RESULT.json')}
result = {'schema': 'pr207-independent-boundary-audit-v1',
          'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_WITH_SCOPE',
          'SymPy': sp.__version__, 'source_pins': source_pins,
          'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'checks_passed': len(checks), 'checks': checks, 'orbits': orbits,
          'three_collision_product_difference': str(base_difference),
          'twelve_entry_product_difference': str(repeated_difference),
          'continuous_family_proof': 'PROOF.md, normalized circle construction',
          'scope': 'Refutes only allowing repeated least-period-three cycles as displayed-length-twelve cases; does not refute a least-period-divisible-by-four assertion. Signed area is the algebraic shoelace area, with traversal multiplicity.'}
(HERE/'INDEPENDENT_RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps({key: result[key] for key in ['status', 'checks_passed', 'three_collision_product_difference', 'twelve_entry_product_difference']}, indent=2))
for name, item in orbits.items():
    print(name, {key: item[key] for key in ['signed_area', 'inverse_signed_area', 'product', 'four_traversal_product']})
