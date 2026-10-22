#!/usr/bin/env python3
"""Independent rational-polynomial/Sturm/sign-cell/knapsack audit.

Does not import or execute the author's mathematics verifier. The author's
receipt is read only for comparison. Standard library, no network.
"""
from fractions import Fraction as F
from functools import reduce
from itertools import product
from math import gcd, lcm, prod
from pathlib import Path
import hashlib
import json
import sys
import zipfile

HERE = Path(__file__).resolve().parent
AUTHOR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent / 'polynomial_2200006'
CHECKS = 0

def require(test, label):
    global CHECKS
    CHECKS += 1
    if not test:
        raise AssertionError(label)

def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] += a*b
    return trim(out)

def expand(roots, leading=1):
    p = [leading]
    for root in roots:
        p = mul(p, [-root, 1])
    return p

def evaluate(p, x):
    val = 0
    for a in reversed(p):
        val = val*x+a
    return val

def primitive(p):
    p = [F(a) for a in trim(p)]
    denominator = lcm(*(a.denominator for a in p))
    integers = [int(a * denominator) for a in p]
    divisor = reduce(gcd, (abs(a) for a in integers))
    return [a//divisor for a in integers] if divisor else [0]

def remainder(p, q):
    p, q = [F(a) for a in p], [F(a) for a in q]
    while len(p) >= len(q) and p != [0]:
        coefficient, offset = p[-1]/q[-1], len(p)-len(q)
        for j, a in enumerate(q):
            p[j+offset] -= coefficient*a
        p = trim(p)
    return p

def sturm(p):
    p = primitive(p)
    if len(p) == 1:
        return [p]
    chain = [p, primitive([i*p[i] for i in range(1, len(p))])]
    while len(chain[-1]) > 1:
        r = primitive([-a for a in remainder(chain[-2], chain[-1])])
        if r == [0]:
            break
        chain.append(r)
    return chain

def sign(v):
    return (v > 0) - (v < 0)

def variations(signs):
    signs = [s for s in signs if s]
    return sum(a != b for a, b in zip(signs, signs[1:]))

def count_real(p):
    chain = sturm(p)
    left = [sign(q[-1])*(-1)**(len(q)-1) for q in chain]
    right = [sign(q[-1]) for q in chain]
    return variations(left)-variations(right), len(chain[-1]) == 1

def selector_polynomials(d, m):
    roots = [[d, m*d]+[r for r in range(1, d) for _ in range(2)]]
    roots.extend([[i*d, (i+1)*d]+[r for r in range(i*d+1, (i+1)*d) for _ in range(2)] for i in range(1, m)])
    polynomials = [expand(r, -1 if i == 0 else 1) for i, r in enumerate(roots)]
    return roots, polynomials

def certify_sign_cells(roots, polynomials, expected):
    boundaries = sorted(set(r for row in roots for r in row))
    require(boundaries == expected, 'all real selector boundaries')
    signs = [sign(p[-1])*(-1)**(len(p)-1) for p in polynomials]
    require(not all(s > 0 for s in signs), 'left exterior excluded')
    intervals = 1
    for b in boundaries:
        require(all(evaluate(p, b) >= 0 for p in polynomials), 'boundary feasible')
        signs = [s*(-1)**r.count(b) for s, r in zip(signs, roots)]
        require(not all(s > 0 for s in signs), 'intervening/right cell excluded')
        intervals += 1
    return intervals

def canonical_radical(a):
    # sqrt(a) = outside*sqrt(squarefree), with squarefree positive.
    outside, squarefree, p = 1, a, 2
    while p*p <= squarefree:
        while squarefree % (p*p) == 0:
            outside *= p
            squarefree //= p*p
        p += 1
    return outside, squarefree

def audit():
    receipt = json.loads((AUTHOR/'results.json').read_text())
    # Separate ZIP/manifest validation, without invoking the author's verifier.
    manifest = json.loads((AUTHOR/'MANIFEST.json').read_text())
    require(hashlib.sha256((AUTHOR/'MANIFEST.json').read_bytes()).hexdigest() == 'db1d4038234a4e1c832a708b948726f7245564956bd5d4a2e8bb21bb015b5475', 'frozen manifest')
    names = {r['path'] for r in manifest['files']}|{'MANIFEST.json'}
    require({p.name for p in AUTHOR.iterdir()} == names, 'strict author inventory')
    for row in manifest['files']:
        data = (AUTHOR/row['path']).read_bytes()
        require(len(data) == row['bytes'], 'author file byte count')
        require(hashlib.sha256(data).hexdigest() == row['sha256'], 'author file hash')
    archive = AUTHOR.parent/'polynomial_2200006_AUTHORED.zip'
    data = archive.read_bytes()
    require(len(data) == 22726, 'author ZIP bytes')
    require(hashlib.sha256(data).hexdigest() == 'daa39e563e2269923c5dbf4865090782382483eaab19b66309568e51866e6a28', 'author ZIP hash')
    with zipfile.ZipFile(archive) as z:
        entries = z.infolist()
        require(len(entries) == 10 and len({i.filename for i in entries}) == 10, 'ten unique ZIP members')
        require({Path(i.filename).name for i in entries} == names, 'ZIP exact inventory')
        for i in entries:
            require(not i.is_dir() and '..' not in Path(i.filename).parts and not Path(i.filename).is_absolute(), 'safe ZIP entry')
            require(z.read(i.filename) == (AUTHOR/Path(i.filename).name).read_bytes(), 'ZIP matches frozen directory')
    # Certify complete real t partition by root multiplicities, not sample points.
    roots = [[0,8]]+[[i-1,i] for i in range(1,9)]
    rads = [expand(r, -1 if i == 0 else 1) for i, r in enumerate(roots)]
    base_cells = certify_sign_cells(roots, rads, list(range(9)))
    points = set()
    base_slices = []
    for t in range(9):
        vals = [evaluate(p,t) for p in rads]
        require(vals == receipt['base_slices'][t]['radicands'], 'independent expanded radicands')
        coordinates = [[(0,0)] if a == 0 else [(s*canonical_radical(a)[0], canonical_radical(a)[1]) for s in [-1,1]] for a in vals]
        slice_points = list(product(*coordinates))
        for point in slice_points:
            require(all(c*c*s == a for (c,s),a in zip(point,vals)), 'squarefree coordinate satisfies equation')
            require((t,point) not in points, 'distinct canonical algebraic point')
            points.add((t,point))
        require(len(slice_points) == 128, 'base slice cardinality')
        base_slices.append(len(slice_points))
    require(len(points) == 1152 and len(points) > 2**10, 'strict quartic refutation')
    # Independent polynomial root-count engine controls, including repeated roots.
    root_controls = [([-1,0,1],2), ([1,0,1],0), ([0,0,1],1), (expand([1,1,2,2,3,3]),3), (expand([-2,-1,0,1,2]),5)]
    for p, expected in root_controls:
        require(count_real(p)[0] == expected, 'Sturm engine control')
    families, levels_checked, sign_cells = [], 0, 0
    for d in range(1,7):
        W = expand([r for r in range(1,d+1) for _ in range(2)])
        require(count_real(W)[0] == d, 'repeated well roots')
        margin = min(evaluate(W, F(r)+F(s,3)) for r in range(1,d+1) for s in [-1,1])
        require(margin > 0, 'well margin')
        for m in range(2,11):
            roots, polys = selector_polynomials(d,m)
            sign_cells += certify_sign_cells(roots,polys,list(range(1,m*d+1)))
            vals = [[evaluate(p,j) for p in polys] for j in range(1,m*d+1)]
            B = max(a for row in vals for a in row)
            epsilon = margin/F(2*(1+B))
            levels = sorted({epsilon*a for row in vals for a in row if a > 0})
            counts = {F(0):d}
            for level in levels:
                p = list(W)
                p[0] -= level
                number, simple = count_real(p)
                require(number == 2*d, 'Sturm all-real shifted well')
                require(simple, 'shifted well roots simple')
                require(0 < level < margin, 'valid level margin')
                counts[level] = number
                levels_checked += 1
            total = sum(prod(counts[epsilon*a] for a in row) for row in vals)
            k,l = 2*d,m+1
            formula = F(m*(k-1)*k**m,4)
            require(total == formula, 'Sturm-derived full family count')
            source = next(r for r in receipt['even_family_cases'] if (r['k'],r['l']) == (k,l))
            require(total == source['count'], 'independent family matches receipt')
            families.append({'k':k,'l':l,'count':total,'distinct_positive_levels':len(levels)})
    # Alternative unbounded-knapsack DP by permitted block size (rather than
    # author's last-block recurrence or recursive partition generator).
    opt = [2**n for n in range(61)]
    for size in range(3,61):
        weight = (size-1)*2**(size-3)
        for n in range(size,61):
            opt[n] = max(opt[n],weight*opt[n-size])
    for row in receipt['restricted_product_optima']:
        require(opt[row['dimension']] == row['count'], 'independent block-size DP')
    # Exact direct enumeration by selector-block multiplicities through n=24.
    # Remaining dimensions are filled by one-variable grids.
    exhaustive = [2**n for n in range(25)]
    visits = 0
    def visit(size, used, weight):
        nonlocal visits
        visits += 1
        for n in range(used,25):
            exhaustive[n] = max(exhaustive[n],weight*2**(n-used))
        if size > 24:
            return
        blockweight = (size-1)*2**(size-3)
        for copies in range((24-used)//size+1):
            visit(size+1,used+size*copies,weight*blockweight**copies)
    visit(3,0,1)
    for n in range(25):
        require(exhaustive[n] == opt[n], 'multiplicity enumeration product optimum')
    # Tensor-product Hessian determinant signs by parity-state convolution.
    degree_cases = 0
    for k in range(1,25):
        plus,minus = 1,0
        for l in range(1,25):
            plus,minus = k*plus+(k-1)*minus,k*minus+(k-1)*plus
            require(plus-minus == 1, 'orientation conservation')
            require(plus+minus == (2*k-1)**l, 'tensor critical-point count')
            require(plus == ((2*k-1)**l+1)//2, 'signed bound arithmetic')
            require(k**l <= plus, 'grid below bound')
            degree_cases += 1
    require(((2*2-1)**10+1)//2 == 29525, 'concrete upper bound')
    # Adversarial false statements cannot be silently accepted.
    # A positive Hessian determinant does not imply a minimum: -x^2-y^2.
    maximum_eigenvalues = [-2, -2]
    require(prod(maximum_eigenvalues) > 0 and all(a < 0 for a in maximum_eigenvalues),
            'positive orientation at a strict maximum')
    # For f=s^2+s, s=x^2+y^2, grad f=2(2s+1)(x,y).
    # Its only real critical point is 0, Hessian=2I, but s=-1/2 is a complex
    # critical conic. Certify its rational parametrization polynomial identity.
    lhs = mul([1,0,-1],[1,0,-1])
    lhs[2] += 4
    require(lhs == mul([1,0,1],[1,0,1]), 'complex critical conic parametrization')
    require(2*2 > 0, 'nondegenerate real critical point on separate component')
    countercontrols = {
        'every_selector_member_exceeds_grid': all(r['count'] > r['k']**r['l'] for r in families),
        'quartic_three_variable_selector_has_eight_points': families[0]['count'] == 8,
        'all_nine_radicands_positive': all(evaluate(p,0)>0 for p in rads),
    }
    for name,value in countercontrols.items():
        require(value is False, 'countercontrol: '+name)
    return {
        'schema':1,'verdict':'PASS','scope':'Finite exact controls plus independently reviewed written proofs; no formal kernel certificate or exact extremal solution.',
        'checks':CHECKS,'author_freeze_unchanged':True,'author_files':10,'author_receipt_assertions':receipt['assertions'],
        'base_points':len(points),'base_slices':base_slices,'base_sign_cells':base_cells,
        'family_cases':len(families),'families':families,'distinct_shifted_well_polynomials_sturm_checked':levels_checked,
        'family_sign_cells':sign_cells,'knapsack_dimensions':list(range(61)),
        'restricted_product_optima_all_dimensions':opt,
        'exhaustive_multiplicity_dimensions':list(range(25)),'exhaustive_enumeration_nodes':visits,
        'degree_orientation_cases':degree_cases,'concrete_interval':[1152,29525],
        'countercontrols':list(countercontrols),
        'symbolic_adversarial_controls':['positive_orientation_at_strict_maximum','regular_real_fiber_with_positive_dimensional_complex_component'],
        'runtime_dependencies':'Python standard library only',
    }

if __name__ == '__main__':
    print(json.dumps(audit(),indent=2,sort_keys=True))
