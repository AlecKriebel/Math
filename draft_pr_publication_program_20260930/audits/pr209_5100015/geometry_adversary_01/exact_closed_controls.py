"""New exact Cartesian N=3 and N=6 controls, independently constructed."""
import sys
sys.path.insert(0, "/Users/alec/Library/Python/3.11/lib/python/site-packages")
import json
from pathlib import Path
import sympy as s

COUNT = 0


def check(value, label):
    global COUNT
    COUNT += 1
    if not value:
        raise AssertionError(label)


def zero(x):
    y = s.radsimp(s.simplify(s.sqrtdenest(s.simplify(s.expand(x)))))
    if y == 0:
        return True
    return s.to_number_field(y).as_expr() == 0


def det(p, q):
    return p[0]*q[1]-p[1]*q[0]


def area(P):
    return s.simplify(sum(det(p, P[(j+1) % len(P)]) for j, p in enumerate(P))/2)


def examine(name, raw, lam):
    P = [s.Matrix(p) for p in raw]
    N = len(P)
    R, Q = [], []
    for j, p in enumerate(P):
        nxt, prior = P[(j+1) % N], P[(j-1) % N]
        n = s.Matrix((p[0]/4, p[1]))
        nn = s.Matrix((nxt[0]/4, nxt[1]))
        c, incoming = nxt-p, p-prior
        u = s.Matrix((-c[1], c[0]))
        h = u.dot(p)
        q = n/n.dot(n)
        r = s.Matrix.vstack(n.T, nn.T).inv()*s.ones(2, 1)
        reflected = incoming-2*n*(n.dot(incoming))/n.dot(n)
        check(zero(p[0]**2/4+p[1]**2-1), name+" boundary")
        check(zero(h*h-(4-lam)*u[0]**2-(1-lam)*u[1]**2), name+" chord tangency")
        check(zero(det(reflected, c)), name+" reflection parallel")
        forward = s.simplify(s.sqrtdenest(s.simplify(reflected.dot(c))))
        check(forward.is_positive is True, name+" exact reflection forward sign")
        check(zero(n.dot(q)-1) and zero(det(n, q)), name+" actual foot")
        check(zero(n.dot(r)-1) and zero(nn.dot(r)-1), name+" actual tangent intersection")
        R.append(r)
        Q.append(q)
    ar = s.simplify(s.sqrtdenest(area(R)))
    aq = s.simplify(s.sqrtdenest(area(Q)))
    product = s.to_number_field(s.simplify(s.sqrtdenest(s.simplify(ar*aq))), s.sqrt(13)).as_expr()
    return dict(name=name, N=N, lam=str(lam), outer=ar, pedal=aq, product=product)


root13 = s.sqrt(13)
lam3 = (8*root13-20)/9
alpha = 2*(root13-1)/3
beta = (4-root13)/3
h = s.sqrt(lam3)/2
triangle_axis = examine("triangle major-axis phase", [(2, 0), (-alpha, h), (-alpha, -h)], lam3)
triangle_top = examine("triangle minor-axis phase", [(0, 1), (-2*s.sqrt(lam3), -beta),
                                                     (2*s.sqrt(lam3), -beta)], lam3)
check(zero(triangle_axis["product"]-triangle_top["product"]), "two exact triangle phases")
lam6 = s.Rational(4, 9)
six_axis = examine("six major-axis phase", [(2, 0), (s.Rational(4, 3), s.sqrt(5)/3),
                   (-s.Rational(4, 3), s.sqrt(5)/3), (-2, 0),
                   (-s.Rational(4, 3), -s.sqrt(5)/3), (s.Rational(4, 3), -s.sqrt(5)/3)], lam6)
six_top = examine("six minor-axis phase", [(0, 1), (-4*s.sqrt(2)/3, s.Rational(1, 3)),
                  (-4*s.sqrt(2)/3, -s.Rational(1, 3)), (0, -1),
                  (4*s.sqrt(2)/3, -s.Rational(1, 3)), (4*s.sqrt(2)/3, s.Rational(1, 3))], lam6)
check(zero(six_axis["product"]-40) and zero(six_top["product"]-40), "two exact six products 40")
result = dict(assertions=COUNT, controls=[{k: str(v) for k, v in row.items()}
                                       for row in [triangle_axis, triangle_top, six_axis, six_top]])
Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
