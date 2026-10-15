"""Independent direct-geometry certificate. Does not import submitted code."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "dependencies"))
import sympy as z

def det(u, v):
    return u[0]*v[1]-u[1]*v[0]

def dot(u, v):
    return u[0]*v[0]+u[1]*v[1]

def sub(u, v):
    return tuple(u[j]-v[j] for j in range(2))

def area(v):
    return z.simplify(sum(det(v[j], v[(j+1)%len(v)]) for j in range(len(v)))/2)

def derived(v, f):
    foot, anti, determinants = [], [], []
    for j, p in enumerate(v):
        q = v[(j+1)%len(v)]
        e = sub(q, p)
        t = z.simplify(dot(sub(f,p), e)/dot(e,e))
        foot.append(tuple(z.simplify(p[r]+t*e[r]) for r in range(2)))
        u, t = sub(p,f), sub(q,f)
        d = z.simplify(det(u,t))
        assert d != 0
        determinants.append(str(d))
        h, g = dot(u,p), dot(t,q)
        r = (z.simplify((h*t[1]-g*u[1])/d), z.simplify((u[0]*g-t[0]*h)/d))
        assert z.simplify(dot(u,sub(r,p))) == 0
        assert z.simplify(dot(t,sub(r,q))) == 0
        anti.append(r)
    return area(foot), area(anti), determinants

def validate(v, a, b, lam):
    for j,p in enumerate(v):
        q, prev = v[(j+1)%len(v)], v[j-1]
        assert z.simplify(p[0]**2/a**2+p[1]**2/b**2-1) == 0
        n = (p[1]-q[1], q[0]-p[0])
        assert z.simplify((a*a-lam)*n[0]**2+(b*b-lam)*n[1]**2-dot(n,p)**2) == 0
        incoming, outgoing = z.Matrix(sub(p,prev)), z.Matrix(sub(q,p))
        incoming /= z.sqrt(dot(incoming,incoming))
        outgoing /= z.sqrt(dot(outgoing,outgoing))
        normal = z.Matrix((p[0]/a**2,p[1]/b**2))
        reflected = incoming-2*dot(incoming,normal)/dot(normal,normal)*normal
        assert all(z.simplify(x)==0 for x in reflected-outgoing)

a,b = z.Integer(3),z.Integer(1)
lam = z.Rational(9,16)
sqrt7,sqrt15 = z.sqrt(7),z.sqrt(15)
f = (2*z.sqrt(2),z.Integer(0))
orbits = {
    "major_axis_phase": [(3,0),(z.Rational(9,4),sqrt7/4),(-z.Rational(9,4),sqrt7/4),(-3,0),(-z.Rational(9,4),-sqrt7/4),(z.Rational(9,4),-sqrt7/4)],
    "minor_axis_phase": [(0,1),(-3*sqrt15/4,z.Rational(1,4)),(-3*sqrt15/4,-z.Rational(1,4)),(0,-1),(3*sqrt15/4,-z.Rational(1,4)),(3*sqrt15/4,z.Rational(1,4))]
}
receipt = {"ellipse_semiaxes":[str(a),str(b)],"caustic_parameter":str(lam),"caustic_semiaxes":[str(z.sqrt(a*a-lam)),str(z.sqrt(b*b-lam))],"focus":[str(x) for x in f],"orbits":{}}
products=[]
for name,v0 in orbits.items():
    v=[tuple(map(z.sympify,p)) for p in v0]
    assert len(set(v))==6
    validate(v,a,b,lam)
    ap,ab,dd=derived(v,f)
    am,bm,_=derived(v,(-f[0],0))
    assert z.simplify(ap-am)==0 and z.simplify(ab-bm)==0
    ap12,ab12,_=derived(v+v,f)
    assert z.simplify(ap12-2*ap)==0 and z.simplify(ab12-2*ab)==0
    prod=z.simplify(ap*ab)
    products.append(prod)
    receipt["orbits"][name]={"vertices":[[str(x) for x in p] for p in v],"least_period":6,"signed_pedal_area":str(ap),"signed_antipedal_area":str(ab),"signed_product_6":str(prod),"signed_product_repeated_12":str(z.simplify(ap12*ab12)),"normal_determinants":dd,"verified":"outer incidence; common caustic tangency; specular reflection; finite intersections; both foci; area doubling under repetition"}
assert z.simplify(products[0]-products[1]) != 0
receipt["product_difference_6"]=str(z.simplify(products[0]-products[1]))
receipt["product_difference_repeated_12"]=str(z.simplify(4*(products[0]-products[1])))
receipt["scope"]="Exact counterexample to closure-only 12-period interpretation; not a counterexample to least-period-divisible-by-four theorem."
print(json.dumps(receipt,indent=2))
