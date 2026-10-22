"""Independent exact audit; stdlib only, no repository or network mutations."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import random
import subprocess
import sys

def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


if "--require-false" in sys.argv:
    require(False, "DELIBERATE FALSE CONDITION: enforcement self-test")


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def det(a, b):
    return a[0]*b[1]-a[1]*b[0]


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c*x for x in a)


def area(points):
    return sum(det(a, b) for a, b in zip(points, points[1:]+points[:1]))/2


def vertices(lines):
    ans = []
    for (a, h), (b, k) in zip(lines, lines[1:]+lines[:1]):
        d = det(a, b)
        if not d:
            raise ValueError("Parallel or coincident consecutive lines")
        ans.append(((h*b[1]-k*a[1])/d, (k*a[0]-h*b[0])/d))
    return ans


def weights(lines):
    ans = []
    for (a, _), (b, _) in zip(lines, lines[1:]+lines[:1]):
        if not dot(a, a) or not dot(b, b):
            raise ValueError("Zero line normal")
        ans.append(2*det(a, b)*dot(a, b)/(dot(a, a)*dot(b, b)))
    return ans


def foot(line, m):
    a, h = line
    return add(m, scale((h-dot(a, m))/dot(a, a), a))


# Polynomial arithmetic is independent of the parent source.  Coefficients
# are exact rationals; each dictionary key is an (x exponent, y exponent).
def const(c):
    return {(0, 0): F(c)} if c else {}


def padd(a, b):
    c = dict(a)
    for k, v in b.items():
        c[k] = c.get(k, F(0))+v
    return {k: v for k, v in c.items() if v}


def pscale(c, a):
    return {k: c*v for k, v in a.items() if c*v}


def pmul(a, b):
    c = {}
    for (i, j), u in a.items():
        for (k, l), v in b.items():
            key = (i+k, j+l)
            c[key] = c.get(key, F(0))+u*v
    return {k: v for k, v in c.items() if v}


def psum(items):
    ans = {}
    for item in items:
        ans = padd(ans, item)
    return ans


def pdet(a, b):
    return padd(pmul(a[0], b[1]), pscale(-1, pmul(a[1], b[0])))


X, Y = {(1, 0): F(1)}, {(0, 1): F(1)}


def pedal_polynomial(lines):
    feet = []
    for n, h in lines:
        nn = dot(n, n)
        if not nn:
            raise ValueError("Zero line normal")
        f = psum([const(h), pscale(-n[0], X), pscale(-n[1], Y)])
        feet.append((padd(X, pscale(n[0]/nn, f)),
                     padd(Y, pscale(n[1]/nn, f))))
    return pscale(F(1, 2), psum(pdet(a, b) for a, b in
                              zip(feet, feet[1:]+feet[:1])))


def verify_identity(lines):
    t, w = vertices(lines), weights(lines)
    lhs = padd(pscale(8, pedal_polynomial(lines)), const(-4*area(t)))
    rhs = {}
    for v, wi in zip(t, w):
        dx, dy = padd(X, const(-v[0])), padd(Y, const(-v[1]))
        rhs = padd(rhs, pscale(wi, padd(pmul(dx, dx), pmul(dy, dy))))
    require(lhs == rhs, (lines, lhs, rhs))
    return t, w


def make_lines(points):
    ans = []
    for a, b in zip(points, points[1:]+points[:1]):
        v = sub(b, a)
        n = (v[1], -v[0])
        ans.append((n, dot(n, a)))
    return ans


def check_orbit(v, s):
    # Actual ellipse vertices are sqrt(s)*v.  All scale-free checks remain
    # rational.  Tangent contact points are checked inside each segment.
    require(len(v) == 4 and len(set(v)) == 4, 'Audit condition failed: len(v) == 4 and len(set(v)) == 4')
    inner = (F(16, 5), F(1, 5))
    contacts = []
    for i, p in enumerate(v):
        require(s*(p[0]**2/4+p[1]**2) == 1, 'Audit condition failed: s*(p[0]**2/4+p[1]**2) == 1')
        q = v[(i+1) % 4]
        edge = sub(q, p)
        n = (edge[1], -edge[0])
        h = dot(n, p)
        require(h and s*h*h == sum(d*x*x for d, x in zip(inner, n)), 'Audit condition failed: h and s*h*h == sum(d*x*x for d, x in zip(inner, n))')
        contact_in_v_coordinates = tuple(d*x/(s*h) for d, x in zip(inner, n))
        k = next(j for j in (0, 1) if edge[j])
        u = (contact_in_v_coordinates[k]-p[k])/edge[k]
        require(0 < u < 1, 'Audit condition failed: 0 < u < 1')
        require(contact_in_v_coordinates == add(p, scale(u, edge)), 'Audit condition failed: contact_in_v_coordinates == add(p, scale(u, edge))')
        contacts.append(str(u))
        incoming = sub(p, v[i-1])
        normal = (p[0]/4, p[1])
        reflected = sub(incoming, scale(2*dot(incoming, normal)/dot(normal, normal), normal))
        require(det(reflected, edge) == 0 and dot(reflected, edge) > 0, 'Audit condition failed: det(reflected, edge) == 0 and dot(reflected, edge) > 0')
    lines = [((p[0]/4, p[1]), F(1)) for p in v]
    tangent_vertices, w = verify_identity(lines)
    aa = s*area(v)
    ap = area(tangent_vertices)/s
    b0 = area([foot(line, (F(0), F(0))) for line in lines])/s
    require(all(wi == 0 for wi in w), 'Audit condition failed: all(wi == 0 for wi in w)')
    return {"A": str(aa), "A_prime": str(ap), "B_0": str(b0),
            "A_A_prime": str(aa*ap), "A_prime_B_0": str(ap*b0),
            "S": str(sum(w)), "contact_segment_parameters": contacts,
            "primitive_period": 4}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


inputs = [PARENT/"exact_classical_controls.py",
          PARENT/"EXACT_CONTROLS_RECEIPT.json",
          PARENT/"EXACT_CONTROLS_OPTIMIZED_RECEIPT.json"]
before = {str(path): sha(path) for path in inputs}
parent_run = subprocess.run([sys.executable, str(inputs[0])], check=True,
                            capture_output=True, text=True)
parent_result = json.loads(parent_run.stdout)
for receipt in inputs[1:]:
    require(json.loads(receipt.read_text()) == parent_result, 'Audit condition failed: json.loads(receipt.read_text()) == parent_result')

# Exact polynomial coefficient verification in both orientations of 224
# independently generated rational cycles (supports include zero).
rng = random.Random(5100014)
random_cycles = 0
for size in range(3, 11):
    for _ in range(28):
        while True:
            normals = [(F(rng.randrange(-5, 6)), F(rng.randrange(-5, 6)))
                       for _ in range(size)]
            if (all(dot(a, a) for a in normals)
                    and all(det(a, b) for a, b in zip(normals, normals[1:]+normals[:1]))):
                break
        lines = [(n, F(rng.randrange(-4, 5))) for n in normals]
        t, w = verify_identity(lines)
        rt, rw = verify_identity(lines[::-1])
        require(area(rt) == -area(t), 'Audit condition failed: area(rt) == -area(t)')
        require(pedal_polynomial(lines[::-1]) == pscale(-1, pedal_polynomial(lines)), 'Audit condition failed: pedal_polynomial(lines[::-1]) == pscale(-1, pedal_polynomial(lines))')
        require(sum(rw) == -sum(w), 'Audit condition failed: sum(rw) == -sum(w)')
        random_cycles += 2

# An explicit self-crossing pentagram, then a reversed side cycle.
outer = [(F(0), F(3)), (F(3), F(1)), (F(2), F(-3)),
         (F(-2), F(-3)), (F(-3), F(1))]
star = [outer[i] for i in [0, 2, 4, 1, 3]]
star_lines = make_lines(star)
star_t, star_w = verify_identity(star_lines)
verify_identity(star_lines[::-1])
require(area(star_t) != 0 and sum(star_w) != 0, 'Audit condition failed: area(star_t) != 0 and sum(star_w) != 0')

# Opposite normal pairing at the origin, and the same polygon translated.
normals = [(F(1), F(0)), (F(1), F(1)), (F(0), F(2)),
           (F(-1), F(0)), (F(-1), F(-1)), (F(0), F(-2))]
centered = [(n, F(1)) for n in normals]
ct, cw = verify_identity(centered)
central_S = sum(cw)
central_W = tuple(sum(wi*t[j] for wi, t in zip(cw, ct)) for j in (0, 1))
require(central_S == 4 and central_W == (0, 0), 'Audit condition failed: central_S == 4 and central_W == (0, 0)')
C = (F(2, 3), F(-5, 7))
translated = [(n, 1+dot(n, C)) for n in normals]
tt, tw = verify_identity(translated)
translated_W = tuple(sum(wi*t[j] for wi, t in zip(tw, tt)) for j in (0, 1))
require(translated_W == scale(central_S, C), 'Audit condition failed: translated_W == scale(central_S, C)')
require(translated_W != (0, 0), 'Audit condition failed: translated_W != (0, 0)')

axis = [(F(2), F(0)), (F(0), F(1)), (F(-2), F(0)), (F(0), F(-1))]
rectangle = [(F(4), F(1)), (F(-4), F(1)), (F(-4), F(-1)), (F(4), F(-1))]
phase1, phase2 = check_orbit(axis, F(1)), check_orbit(rectangle, F(1, 5))
require([phase1[k] for k in ["A", "A_prime", "B_0", "A_A_prime", "A_prime_B_0"]] == ["4", "8", "4", "32", "32"], 'Audit condition failed: [phase1[k] for k in ["A", "A_prime", "B_0", "A_A_prime", "A_prime_B_0"]] == ["4", "8", "4", "32", "32"]')
require([phase2[k] for k in ["A", "A_prime", "B_0", "A_A_prime", "A_prime_B_0"]] == ["16/5", "10", "5", "32", "50"], 'Audit condition failed: [phase2[k] for k in ["A", "A_prime", "B_0", "A_A_prime", "A_prime_B_0"]] == ["16/5", "10", "5", "32", "50"]')

trapezoid = [(F(0), F(0)), (F(2), F(0)), (F(1), F(1)), (F(0), F(1))]
trap_lines = make_lines(trapezoid)
trap_t, trap_w = verify_identity(trap_lines)
trap_S = sum(trap_w)
trap_W = tuple(sum(wi*t[j] for wi, t in zip(trap_w, trap_t)) for j in (0, 1))
trap_poly = pedal_polynomial(trap_lines)
require(trap_S == 0 and trap_W == (-1, 1), 'Audit condition failed: trap_S == 0 and trap_W == (-1, 1)')
require(trap_poly == {(0, 0): F(1, 2), (1, 0): F(1, 4), (0, 1): F(-1, 4)}, 'Audit condition failed: trap_poly == {(0, 0): F(1, 2), (1, 0): F(1, 4), (0, 1): F(-1, 4)}')

original_foot = foot(((F(1), F(1)), F(1)), (F(0), F(0)))
mapped_foot = (2*original_foot[0], original_foot[1])
new_foot = foot(((F(1, 2), F(1)), F(1)), (F(0), F(0)))
require(mapped_foot == (1, F(1, 2)) and new_foot == (F(2, 5), F(4, 5)), 'Audit condition failed: mapped_foot == (1, F(1, 2)) and new_foot == (F(2, 5), F(4, 5))')
require(mapped_foot != new_foot, 'Audit condition failed: mapped_foot != new_foot')

denominator_checks = 0
for invalid in [
        [((F(0), F(0)), F(1)), ((F(1), F(0)), F(1))],
        [((F(1), F(0)), F(1)), ((F(2), F(0)), F(1))]]:
    try:
        verify_identity(invalid)
    except ValueError:
        denominator_checks += 1
    else:
        raise RuntimeError("Undefined vertex or normal accepted")

after = {str(path): sha(path) for path in inputs}
require(before == after, "Audit input changed during verification")
result = {
    "status": "PASS_WITH_CONVENTION_CAVEATS",
    "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "workflow_completion_percent": 100,
    "workflow_scope": "Independent adversarial verification of exact classical algebraic controls only",
    "target_theorem_completion_percent": "not assessed",
    "parent_receipts_reproduced": True,
    "source_and_receipt_sha256": before,
    "random_rational_cycles_verified_by_all_polynomial_coefficients": random_cycles,
    "additional_exact_controls": ["self-crossing pentagram and reverse", "origin-centered central hexagon", "translated central hexagon", "two primitive confocal four-orbits", "zero-S trapezoid", "affine projection noncommutation"],
    "denominator_rejections_checked": denominator_checks,
    "pentagram_A_prime_signed": str(area(star_t)),
    "pentagram_S_signed": str(sum(star_w)),
    "central_S": str(central_S),
    "central_W": [str(x) for x in central_W],
    "translated_center": [str(x) for x in C],
    "translated_W": [str(x) for x in translated_W],
    "excluded_N4_phase1": phase1,
    "excluded_N4_phase2": phase2,
    "trapezoid_S": str(trap_S),
    "trapezoid_W": [str(x) for x in trap_W],
    "trapezoid_B_M": "1/2 + x/4 - y/4",
    "affine_mapped_original_foot": [str(x) for x in mapped_foot],
    "affine_new_euclidean_foot": [str(x) for x in new_foot],
    "caveats": ["Signed areas and preserved side-cycle order are required, including stars.", "delta is the oriented normal/tangent turn modulo pi, not an unsigned interior angle.", "Central first-moment cancellation requires symmetry center at the origin and paired side order.", "Nonzero real normals and nonparallel consecutive lines are required.", "S=0 does not imply zero first moment or a finite curvature centroid.", "The N=4 controls are excluded parity evidence only; they do not address the target theorem.", "Finite controls alone do not prove a universal Poncelet-family invariant."]
}
output = ROOT/("VERIFY_RESULTS_OPTIMIZED.json" if sys.flags.optimize else "VERIFY_RESULTS.json")
output.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
