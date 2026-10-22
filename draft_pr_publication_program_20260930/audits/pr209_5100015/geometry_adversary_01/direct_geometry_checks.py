"""Independent Cartesian billiard checks; no inherited executable imports.

Run Python -E -S -B -P; insert only the verified existing site directory.
All output is confined to the explicitly supplied output JSON path.
"""
import sys
sys.path.insert(0, "/Users/alec/Library/Python/3.11/lib/python/site-packages")
import json
from pathlib import Path
import mpmath as mp
import sympy as sp

mp.mp.dps = 150
TOL = mp.mpf("1e-85")
COUNT = 0


def check(condition, label):
    global COUNT
    COUNT += 1
    if not condition:
        raise AssertionError(label)


def dot(p, q):
    return p[0]*q[0] + p[1]*q[1]


def det(p, q):
    return p[0]*q[1] - p[1]*q[0]


def sub(p, q):
    return p[0]-q[0], p[1]-q[1]


def scale(c, p):
    return c*p[0], c*p[1]


def norm(p):
    return mp.sqrt(dot(p, p))


def area(points):
    return sum(det(p, points[(j+1) % len(points)])
               for j, p in enumerate(points))/2


def step(p, A, B, lam):
    """Choose CCW tangent using Joachimsthal, then intersect outer ellipse.

    This uses Cartesian square roots; no Jacobi functions or author code.
    """
    n = p[0]/A, p[1]/B
    s = dot(n, n)
    kap = mp.sqrt(lam/(A*B))
    t = mp.sqrt(s-kap*kap)/s
    v = -kap*n[0]/s-t*n[1], -kap*n[1]/s+t*n[0]
    flight = 2*kap/(v[0]*v[0]/A + v[1]*v[1]/B)
    return (p[0]+flight*v[0], p[1]+flight*v[1]), v


def advance_angle(A, B, lam, N):
    p = mp.sqrt(A), mp.mpf(0)
    old = mp.mpf(0)
    advance = mp.mpf(0)
    for _ in range(N):
        p, _ = step(p, A, B, lam)
        theta = mp.atan2(p[1]/mp.sqrt(B), p[0]/mp.sqrt(A))
        advance += (theta-old) % (2*mp.pi)
        old = theta
    return advance


def closing_lambda(A, B, N, winding):
    lo = B*mp.mpf("1e-75")
    hi = B*(1-mp.mpf("1e-75"))
    target = 2*mp.pi*winding
    check(advance_angle(A, B, lo, N) < target, "lower root bracket")
    check(advance_angle(A, B, hi, N) > target, "upper root bracket")
    for _ in range(480):
        mid = (lo+hi)/2
        if advance_angle(A, B, mid, N) < target:
            lo = mid
        else:
            hi = mid
    lam = (lo+hi)/2
    check(abs(advance_angle(A, B, lam, N)-target) < TOL,
          "rotation closure")
    return lam


def orbit_data(A, B, lam, N, theta):
    p0 = mp.sqrt(A)*mp.cos(theta), mp.sqrt(B)*mp.sin(theta)
    p = p0
    points = []
    velocities = []
    normals = []
    for _ in range(N):
        points.append(p)
        normals.append((p[0]/A, p[1]/B))
        p, v = step(p, A, B, lam)
        velocities.append(v)
    closure = norm(sub(p, p0))
    check(closure < TOL, "Cartesian orbit closes at arbitrary phase")
    R, Q, tangent_det = [], [], []
    kap = mp.sqrt(lam/(A*B))
    for j, p in enumerate(points):
        n = normals[j]
        nn = normals[(j+1) % N]
        d = det(n, nn)
        check(abs(d) > mp.mpf("1e-60"), "finite outer intersection")
        r = (nn[1]-n[1])/d, (n[0]-nn[0])/d
        q = scale(1/dot(n, n), n)
        R.append(r)
        Q.append(q)
        tangent_det.append(abs(d))
        v = velocities[j]
        prior = velocities[(j-1) % N]
        chord = sub(points[(j+1) % N], p)
        u = -v[1], v[0]
        h = dot(u, p)
        pole = A*u[0]/h, B*u[1]/h
        check(abs(p[0]*p[0]/A+p[1]*p[1]/B-1) < TOL, "outer ellipse")
        check(abs(dot(v, v)-1) < TOL, "unit velocity")
        check(abs(h*h-((A-lam)*u[0]*u[0]+(B-lam)*u[1]*u[1])) < TOL,
              "actual chord caustic tangency")
        check(norm(sub(v, scale(1/norm(chord), chord))) < TOL,
              "forward physical velocity")
        check(norm(sub(prior, sub(v, scale(-2*kap, q)))) < TOL,
              "normal foot velocity jump reflection")
        check(abs(dot(n, q)-1) < TOL and abs(det(n, q)) < TOL,
              "actual perpendicular foot")
        check(abs(dot(n, r)-1) < TOL and abs(dot(nn, r)-1) < TOL,
              "intersection of successive boundary tangents")
        check(norm(sub(r, pole)) < TOL, "outer intersection equals chord pole")
    ar, aq = area(R), area(Q)
    return dict(points=points, R=R, Q=Q, outer=ar, pedal=aq, product=ar*aq,
                closure=closure, min_tangent_det=min(tangent_det))


def exact_controls():
    A, B, lam = sp.Integer(4), sp.Integer(1), sp.Rational(4, 5)
    root5 = sp.sqrt(5)
    cases = [
        ("axis diamond", [(2, 0), (0, 1), (-2, 0), (0, -1)], 8, 4, 32),
        ("inscribed rectangle", [(4/root5, 1/root5), (-4/root5, 1/root5),
                                 (-4/root5, -1/root5), (4/root5, -1/root5)],
         10, 5, 50),
    ]
    out = []
    for name, raw, expected_r, expected_q, expected_product in cases:
        P = [sp.Matrix(p) for p in raw]
        normals = [sp.Matrix((p[0]/A, p[1]/B)) for p in P]
        Q = [sp.simplify(n/n.dot(n)) for n in normals]
        R = []
        for j, p in enumerate(P):
            nxt = P[(j+1) % 4]
            n, nn = normals[j], normals[(j+1) % 4]
            R.append(sp.simplify(sp.Matrix.vstack(n.T, nn.T).inv()*sp.ones(2, 1)))
            c = nxt-p
            v = sp.simplify(c/sp.sqrt(c.dot(c)))
            incoming = p-P[(j-1) % 4]
            incoming = sp.simplify(incoming/sp.sqrt(incoming.dot(incoming)))
            u = sp.Matrix((-v[1], v[0]))
            h = u.dot(p)
            check(sp.simplify(h*h-(A-lam)*u[0]**2-(B-lam)*u[1]**2) == 0,
                  name+" exact common caustic")
            check(sp.simplify(incoming-v-2*sp.sqrt(lam/(A*B))*Q[j]) == sp.zeros(2, 1),
                  name+" exact reflection")
            check(sp.simplify(p[0]**2/A+p[1]**2/B-1) == 0, name+" exact boundary")
        AR = sp.simplify(sum(sp.det(sp.Matrix.hstack(r, R[(j+1) % 4]))
                            for j, r in enumerate(R))/2)
        AQ = sp.simplify(sum(sp.det(sp.Matrix.hstack(q, Q[(j+1) % 4]))
                            for j, q in enumerate(Q))/2)
        check(AR == expected_r and AQ == expected_q and AR*AQ == expected_product,
              name+" exact areas")
        out.append(dict(name=name, outer=str(AR), pedal=str(AQ), product=str(AR*AQ)))
    return out


def main():
    exact = exact_controls()
    families = []
    specs = [("moderate", "4", "1", n, tau)
             for n, tau in [(3, 1), (5, 1), (5, 2), (6, 1), (7, 2), (7, 3),
                            (9, 2), (9, 4), (10, 3), (11, 5), (14, 5), (18, 7)]]
    specs += [("near_circle", "1.0001", "1", 7, 3),
              ("eccentric", "100", "1", 5, 2),
              ("long_small_rotation", "4", "1", 51, 1),
              ("near_separatrix", "4", "1", 19, 9)]
    for tag, aa, bb, N, winding in specs:
        A, B = mp.mpf(aa), mp.mpf(bb)
        lam = closing_lambda(A, B, N, winding)
        phase_data = [orbit_data(A, B, lam, N, th)
                      for th in [mp.mpf(0), mp.mpf(".137"), mp.mpf(".81"),
                                 mp.pi/2, mp.mpf("2.71"), mp.mpf("5.321")]]
        products = [d["product"] for d in phase_data]
        drift = max(abs(x-products[0]) for x in products)
        check(drift < TOL*max(1, abs(products[0])), "phase invariant product")
        base = phase_data[2]
        check(abs(area(list(reversed(base["R"])))+base["outer"]) < TOL,
              "outer reversal")
        check(abs(area(list(reversed(base["Q"])))+base["pedal"]) < TOL,
              "foot reversal")
        for repeat in [2, 3, 5]:
            check(abs(area(base["R"]*repeat)*area(base["Q"]*repeat)
                      -repeat**2*base["product"]) < TOL*max(1, abs(base["product"])),
                  "displayed repetition squared scaling")
        # Negative normalization checks: omit the |n|² denominator and use P itself.
        wrong_normal = []
        wrong_P = []
        for d in phase_data:
            ns = [(p[0]/A, p[1]/B) for p in d["points"]]
            wrong_normal.append(d["outer"]*area(ns))
            wrong_P.append(d["outer"]*area(d["points"]))
        families.append(dict(tag=tag, A=str(A), B=str(B), N=N, winding=winding,
                             lam=mp.nstr(lam, 85),
                             product=mp.nstr(products[0], 75),
                             relative_phase_drift=mp.nstr(drift/max(1, abs(products[0])), 8),
                             max_closure=mp.nstr(max(d["closure"] for d in phase_data), 8),
                             min_tangent_det=mp.nstr(min(d["min_tangent_det"] for d in phase_data), 8),
                             wrong_normal_spread=mp.nstr(max(wrong_normal)-min(wrong_normal), 8),
                             wrong_vertex_spread=mp.nstr(max(wrong_P)-min(wrong_P), 8)))
        print(json.dumps({"family": tag, "N": N, "winding": winding,
                          "relative_phase_drift": families[-1]["relative_phase_drift"]}), flush=True)
    result = dict(python=sys.version, sympy=sp.__version__, mpmath=mp.__version__,
                  dps=mp.mp.dps, tolerance=str(TOL), assertions=COUNT,
                  exact=exact, families=families,
                  scope="Finite high-precision diagnostics, not interval certification or universal proof")
    Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+"\n")


if __name__ == "__main__":
    main()
