"""Exact controls for implications that a general-theorem audit must reject.

These are N=4 controls, not counterexamples to the N=2 mod 4 target.
No assertions are used: failures raise in normal and optimized Python.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import sys
import sympy as s


def eq(a, b, context):
    if s.simplify(a - b) != 0:
        raise ValueError(context + ': ' + str(s.simplify(a - b)))


def area(vertices):
    return s.simplify(sum(
        s.det(s.Matrix.hstack(vertices[i], vertices[(i+1) % len(vertices)]))
        for i in range(len(vertices))) / 2)


def check_family(vertices, expected):
    x, y = s.symbols('x y', real=True)
    M = s.Matrix([x, y])
    Dinv = s.diag(s.Rational(1, 4), 1)
    caustic = s.diag(s.Rational(16, 5), s.Rational(1, 5))
    nraw = [Dinv * p for p in vertices]
    tangents = []
    feet = []
    dist2 = 0
    units = []
    for i, p in enumerate(vertices):
        eq((p.T * Dinv * p)[0], 1, 'boundary')
        r = nraw[i]
        d = s.simplify(r.dot(r))
        feet.append(s.simplify(M + (1-r.dot(M)) * r/d))
        dist2 += (1-r.dot(M))**2 / d
        units.append(s.simplify(r/s.sqrt(d)))
        rn = nraw[(i+1) % 4]
        tangents.append(s.simplify(s.Matrix.vstack(r.T, rn.T).inv()*s.ones(2, 1)))
        edge = vertices[(i+1) % 4] - p
        normal = s.Matrix([edge[1], -edge[0]])
        eq((normal.T * caustic * normal)[0], normal.dot(p)**2, 'caustic tangency')
        incoming = p - vertices[(i-1) % 4]
        incoming = incoming / s.sqrt(incoming.dot(incoming))
        outgoing = edge / s.sqrt(edge.dot(edge))
        reflected = incoming - 2 * incoming.dot(r) * r/d
        for j in range(2):
            eq(reflected[j], outgoing[j], 'reflection')
    A = area(vertices)
    Ap = area(tangents)
    B = area(feet)
    centroid = s.simplify(sum(feet, s.zeros(2, 1))/4)
    for j in range(2):
        eq(centroid[j], M[j]/2, 'centroid')
    eq(dist2, 10+2*(x*x+y*y), 'arbitrary-point squared-distance sum')
    eq(A*Ap, 32, 'credited even-period area product')
    eq(B, expected['B'], 'pedal area')
    eq(Ap*B, expected['product'], 'outer pedal product')
    S = sum(2*units[i].dot(units[(i+1)%4]) *
            s.det(s.Matrix.hstack(units[i], units[(i+1)%4])) for i in range(4))
    eq(S, 0, 'Steiner radial coefficient')
    return {k:str(s.simplify(v)) for k,v in {
        'A':A, 'A_prime':Ap, 'B_M':B, 'A_prime_B_M':Ap*B,
        'AA_prime':A*Ap, 'squared_distance_sum':dist2,
        'centroid_x':centroid[0], 'centroid_y':centroid[1], 'S':S}.items()}


rt5=s.sqrt(5)
first=[s.Matrix(v) for v in [(2,0),(0,1),(-2,0),(0,-1)]]
second=[s.Matrix(v) for v in [(4/rt5,1/rt5),(-4/rt5,1/rt5),(-4/rt5,-1/rt5),(4/rt5,-1/rt5)]]

# A general centrally symmetric six-line fixture checks the independently
# derived radial pedal-area identity, without any billiard hypotheses.
x,y=s.symbols('x y',real=True)
M=s.Matrix([x,y])
half=[s.Matrix([1,0]),s.Matrix([s.Rational(3,5),s.Rational(4,5)]),
      s.Matrix([s.Rational(-5,13),s.Rational(12,13)])]
normals=half+[-v for v in half]
support=[s.Integer(h) for h in [2,3,4,2,3,4]]
feet=[M+(h-n.dot(M))*n for n,h in zip(normals,support)]
centerfeet=[h*n for n,h in zip(normals,support)]
S=s.simplify(sum(2*normals[i].dot(normals[(i+1)%6]) *
    s.det(s.Matrix.hstack(normals[i],normals[(i+1)%6])) for i in range(6)))
eq(area(feet),area(centerfeet)+(x*x+y*y)*S/8,'central radial identity')

# An anisotropic affine map does not commute with Euclidean foot projection.
L=s.diag(2,1)
q=L*s.Matrix([s.Rational(1,2),s.Rational(1,2)])
qprime=s.Matrix([s.Rational(2,5),s.Rational(4,5)])
if q==qprime:
    raise ValueError('affine projection counterlimitation vanished')

results={
    'UTC':datetime.now(timezone.utc).isoformat(),
    'scope':'Exact N=4 counterlimitation for all-N moment/perimeter/area-product transfer; excluded from target',
    'first':check_family(first, {'B':4,'product':32}),
    'second':check_family(second, {'B':5,'product':50}),
    'central_six_line_fixture':{'B_M':str(area(feet)),'B_0':str(area(centerfeet)),'S':str(S)},
    'affine_projection_counterlimitation':{
        'line':'x+y=1; image line x/2+y=1; M=0; L=diag(2,1)',
        'L_of_original_foot':str(list(q)),
        'foot_on_image_line':str(list(qprime))},
    'status':'PASS: same centroid, squared-distance sum, AA-prime; distinct outer-pedal products'
}
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('exact_gap_controls.json')
out.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
