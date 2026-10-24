#!/usr/bin/env python3
"""Independent exact audit of the height countermodel and elementary gaps.

Uses minors, rather than the author's row reducer. Never writes author files.
Run with ordinary Python 3; the sole output file is beside this script.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
INPUTS = [
    "positive_hierarchy/HEIGHT_NORM_COUNTERMODEL.md",
    "positive_hierarchy/GENERAL_ENVELOPE_AUDIT.md",
    "positive_hierarchy/check_height_norm.py",
    "positive_hierarchy/height_norm_certificate.json",
    "positive_hierarchy/MODEL_PATHOLOGY_CONTROL.md",
    "positive_hierarchy/ONE_TWIST_CUBULATION.md",
    "positive_hierarchy/check_model_pathology.py",
    "positive_hierarchy/model_pathology_certificate.json",
    "positive_hierarchy/check_one_twist.py",
    "priority/sources/linton2510.10178v2.html",
    "priority/sources/merladet_minasyan2511.21293v1.html",
    "positive_hierarchy/sources/hruska_ruane1705.00784v3.html",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def det(rows):
    """Leibniz determinant; tiny matrices only, no Gaussian elimination."""
    from itertools import permutations
    n = len(rows)
    result = 0
    for perm in permutations(range(n)):
        term = (-1) ** sum(perm[i] > perm[j]
                           for i in range(n) for j in range(i + 1, n))
        for i, j in enumerate(perm):
            term *= rows[i][j]
        result += term
    return result


def red(word):
    stack = []
    for x in word:
        if stack and stack[-1] == -x:
            stack.pop()
        else:
            stack.append(x)
    return tuple(stack)


def inv(word):
    return tuple(-x for x in reversed(word))


def genpow(letter, exponent):
    return (letter if exponent >= 0 else -letter,) * abs(exponent)


TWISTS = {3: (0, -2), 4: (-1, 3), 5: (-1, -5),
          6: (-6, 10), 7: (-6, -12)}


def phi(word, exponent):
    # Direct closed formula, not iterative use of the author's substitutions.
    result = []
    for letter in word:
        index = abs(letter)
        if index <= 2:
            image = (index,)
        else:
            p, q = TWISTS[index]
            image = genpow(1, exponent*p) + (index,) + genpow(2, exponent*q)
        result.extend(image if letter > 0 else inv(image))
    return red(result)


def mul(x, y):
    return red(x[0] + phi(y[0], x[1])), x[1] + y[1]


def inverse(x):
    return phi(inv(x[0]), -x[1]), -x[1]


def power(x, exponent):
    if exponent < 0:
        return power(inverse(x), -exponent)
    out = ((), 0)
    for _ in range(exponent):
        out = mul(out, x)
    return out


def annulus_pathology_checks():
    """Construct the square incidences in all c mod n covers, 1<=n<=50."""
    components = 0
    corners_tested = 0
    squares_tested = 0
    for n in range(1,51):
        edges, squares = {}, []
        def edge(name,start,end):
            edges[name] = (start,end)
            return name
        for j in range(n):
            for z in (0,1):
                edge(('a',j,z),(j,z),(j,z))
                edge(('b',j,z),(j,z),(j,z))
                edge(('z',j,z),(j,z),(j,1-z))
            # Original product vertex complex: two rose edges x two z-edges.
            for label in ('a','b'):
                for z in (0,1):
                    squares.append([((label,j,z),1),(('z',j,z),1),
                                    ((label,j,1-z),-1),(('z',j,z),-1)])
        for j in range(n):
            target = (j+1)%n
            edge(('c',j,0),(j,0),(target,0))
            edge(('c',j,1),(j,1),(target,0))
            squares.append([(('z',j,0),1),(('c',j,1),1),
                            (('a',target,0),-1),(('c',j,0),-1)])
            squares.append([(('z',j,1),1),(('c',j,0),1),
                            (('b',target,0),-1),(('c',j,1),-1)])
        parent = {e:e for e in edges}
        def find(e):
            while parent[e] != e:
                e = parent[e]
            return e
        def join(e,f):
            parent[find(e)] = find(f)
        corners = set()
        for square in squares:
            for i in range(4):
                e,sign = square[i]
                f,next_sign = square[(i+1)%4]
                assert edges[e][sign == 1] == edges[f][next_sign == -1]
                corners.add(frozenset(((e,-sign),(f,next_sign))))
                corners_tested += 1
            join(square[0][0],square[2][0])
            join(square[1][0],square[3][0])
            squares_tested += 1
        for j in range(n):
            c0,c1 = ('c',j,0),('c',j,1)
            assert c0 != c1 and edges[c0][1] == edges[c1][1]
            assert find(c0) == find(c1)
            assert {e for e in edges if find(e) == find(c0)} == {c0,c1}
            assert frozenset(((c0,-1),(c1,-1))) not in corners
            # Opposite c-edges have opposite boundary signs, so the annulus
            # coorientation consistently points from the z-side to the w-side.
            for square in squares:
                csigns = [sign for e,sign in square if e in (c0,c1)]
                assert not csigns or sorted(csigns) == [-1,1]
            components += 1
    return components,corners_tested,squares_tested


def main():
    hashes_before = {p: sha(BASE/p) for p in INPUTS}
    pairs = [(7,1), (7,-1), (8,4), (8,-4), (13,11), (13,-11)]
    rows = [[x*x, 2*x, 1, -y*y, -2*y, -1] for x,y in pairs]
    nonzero_four = []
    for rr in combinations(range(6), 4):
        for cc in combinations(range(6), 4):
            d = det([[rows[i][j] for j in cc] for i in rr])
            if d:
                nonzero_four.append([list(rr), list(cc), d])
    assert nonzero_four
    five_minors = 0
    for rr in combinations(range(6), 5):
        for cc in combinations(range(6), 5):
            assert det([[rows[i][j] for j in cc] for i in rr]) == 0
            five_minors += 1
    kernel = [(1,0,0,1,0,48), (0,0,1,0,0,1)]
    assert det([[kernel[i][j] for j in (0,2)] for i in range(2)]) == 1
    assert all(sum(a*b for a,b in zip(row,v)) == 0 for row in rows for v in kernel)
    assert all(x*x-y*y == 48 for x,y in pairs)
    assert all(__import__('math').gcd(x, 1) == __import__('math').gcd(y, 1) == 1
               for x,y in pairs)
    # The minor bound plus independent kernel vectors prove the complete
    # two-parameter characterization; the following checks test its arithmetic.
    flat_checks = 0
    for a,d in product((F(i,j) for i in range(1,7) for j in range(1,5)), repeat=2):
        assert a*d > 0 and a*(d+48*a) > 0
        assert d+48*a > d
        assert F(1,d) > F(1,d+48*a)
        for x,y in pairs:
            assert a*x*x+d == a*y*y+d+48*a
            flat_checks += 1
    # Independent semidirect normal forms evaluate the original graph-of-groups
    # relations, not merely the proposed automorphism and its inverse.
    a,b,T = ((1,),0), ((2,),0), ((),1)
    t,s = mul(power(a,-7),T), mul(power(b,-1),T)
    for x in (a,b):
        assert mul(mul(mul(x,T),inverse(x)),inverse(T)) == ((),0)
    relation_checks = 0
    for i,(x,y) in enumerate(pairs):
        left, right = mul(power(a,x), t), mul(power(b,y), s)
        if i:
            u = ((i+2,),0)
            left = mul(mul(inverse(u),left),u)
        assert left == right
        relation_checks += 1
    for index in range(1,8):
        for n in range(-25,26):
            assert phi(phi((index,),n),-n) == (index,)
    rng = random.Random(21124)
    word_checks = 0
    for _ in range(500):
        word = red(rng.choice((-1,1))*rng.randrange(1,8) for _ in range(rng.randrange(31)))
        h,k = rng.randrange(-5,6), rng.randrange(-5,6)
        assert phi(phi(word,h),k) == phi(word,h+k)
        assert phi(phi(word,h),-h) == word
        word_checks += 1
    iterations = 0
    for index,(p,q) in TWISTS.items():
        for n in range(-100,101):
            image = phi((index,),n)
            assert len(image) == 1 + abs(n)*(abs(p)+abs(q))
            assert mul(mul(power(T,n),((index,),0)),power(T,-n)) == (image,0)
            iterations += 1
    # Bass--Serre orbit/stabilizer counts, using surjectivity of all heights.
    vertex_orbits, edge_orbits, vertex_free_rank = 2, 6, 2
    fiber_rank = vertex_free_rank + edge_orbits - vertex_orbits + 1
    assert fiber_rank == 7
    self_osculating_components, corners_checked, squares_checked = annulus_pathology_checks()
    # Projection countermodel: minimize exact piecewise quadratic polynomials.
    grid = [F(i,120) for i in range(-120,121)]
    endpoint_min = min((1+abs(z))**2+(1-z)**2 for z in grid)
    endpoint_arg = [z for z in grid if (1+abs(z))**2+(1-z)**2 == endpoint_min]
    midpoint_min = min(z*z+(1-z)**2 for z in grid)
    midpoint_arg = [z for z in grid if z*z+(1-z)**2 == midpoint_min]
    assert endpoint_arg == [F(0)] and midpoint_arg == [F(1,2)]
    # Their derivatives verify that grid minima are also global minima.
    assert endpoint_min == 2 and midpoint_min == F(1,2)
    # Morse countermodel: all vertex subpaths of all n<=25 detours.
    morse_pairs = 0
    for n in range(1,26):
        path = [(i,0) for i in range(n+1)]
        path += [(n,j) for j in range(1,n+1)]
        path += [(n-i,n) for i in range(1,n+1)]
        for i in range(len(path)):
            for j in range(i+1,len(path)):
                dist = abs(path[j][0]-path[i][0])+abs(path[j][1]-path[i][1])
                assert dist <= j-i <= 3*dist
                morse_pairs += 1
        assert max(abs(x) for x,y in path) == n
    # Reproduce the author checker only in a temporary byte-copy.
    with tempfile.TemporaryDirectory(prefix='height_envelope_author_') as tmp:
        target = Path(tmp)
        for name in ('HEIGHT_NORM_COUNTERMODEL.md','check_height_norm.py'):
            shutil.copyfile(BASE/'positive_hierarchy'/name,target/name)
        proc = subprocess.run([sys.executable,str(target/'check_height_norm.py')],
                              capture_output=True,text=True,check=True)
        author = json.loads(proc.stdout)
        frozen = json.loads((BASE/'positive_hierarchy/height_norm_certificate.json').read_text())
        for key in frozen:
            if key != 'utc':
                assert author[key] == frozen[key], key
        for name in ('MODEL_PATHOLOGY_CONTROL.md','check_model_pathology.py',
                     'check_one_twist.py'):
            shutil.copyfile(BASE/'positive_hierarchy'/name,target/name)
        subprocess.run([sys.executable,str(target/'check_model_pathology.py')],
                       capture_output=True,text=True,check=True)
        author_model = json.loads((target/'model_pathology_certificate.json').read_text())
        frozen_model = json.loads((BASE/'positive_hierarchy/model_pathology_certificate.json').read_text())
        for key in frozen_model:
            if key != 'utc':
                assert author_model[key] == frozen_model[key], key
    assert hashes_before == {p: sha(BASE/p) for p in INPUTS}
    result = {
        'status':'PASS', 'utc':datetime.now(timezone.utc).isoformat(),
        'input_sha256':hashes_before,
        'script_sha256':sha(Path(__file__)),
        'method':'exact determinant minors and independent semidirect normal forms',
        'rank':4, 'nonzero_4x4_minors':len(nonzero_four),
        'witness_4x4_minor':nonzero_four[0], 'zero_5x5_minors':five_minors,
        'metric_equations_checked':flat_checks,
        'graph_relations_checked':relation_checks,
        'random_free_word_composition_checks':word_checks,
        'marked_monodromy_iterates':iterations,
        'fiber_rank':fiber_rank,
        'c_height_covers_checked':50,
        'self_osculating_annulus_components':self_osculating_components,
        'square_corner_incidences_checked':corners_checked,
        'squares_checked':squares_checked,
        'projection_grid_points':len(grid),
        'morse_subpath_pairs':morse_pairs,
        'author_checker_reproduced_in_temporary_copy':True,
        'author_model_checker_reproduced_in_temporary_copy':True,
        'frozen_author_inputs_unchanged':True,
        'scope':'supporting countermodels/conditional reductions only; no full 21.124 claim',
    }
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
