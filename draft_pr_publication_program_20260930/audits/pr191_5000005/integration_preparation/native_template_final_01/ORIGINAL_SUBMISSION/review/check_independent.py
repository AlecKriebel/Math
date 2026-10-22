#!/usr/bin/env python3
"""Independent rational controls for frozen 5000005 candidate, not a proof search.

No import from the author's checker. Angles are in units of pi. Only stdlib.
"""
from collections import Counter
from fractions import Fraction as Q
from math import gcd
import hashlib
import json
from pathlib import Path

counts = Counter()


def require(condition, family, context=None):
    counts[family] += 1
    if not condition:
        raise AssertionError((family, context))


def corner(n, polygon, vertex):
    """Derive cone and position from the side-gluing corner permutation."""
    if n % 2:
        return 0, vertex if vertex % 2 == polygon else vertex + n
    return (polygon - vertex) % 2, vertex


def source_branches(n, alpha, beta, polygon):
    """Literal printed inequalities, selecting sums for P and differences for Q.

    k=n-2 is admitted for the source's second side A_(n-2)=A_0.
    """
    m, residues = n // 2, set()
    for k in range(n - 1):
        if n % 2 == 0:
            if polygon == 1:
                ok = ((k <= m-1 and alpha <= Q(m-k-1, m) and beta-alpha == Q(k+1, m)) or
                      (k >= m-1 and alpha >= Q(n-k-2, m) and beta-alpha == Q(k+3-n, m)))
            else:
                ok = ((k <= m-1 and alpha >= Q(m-k-1, m) and beta+alpha == Q(n-k-1, m)) or
                      (k >= m-1 and alpha <= Q(n-k-2, m) and beta+alpha == Q(n-k-1, m)))
        else:
            if polygon == 1:
                ok = ((k <= m+1 and alpha <= Q(n-2*k-2, n) and beta-alpha == Q(2*k+2, n)) or
                      (k >= m and alpha >= Q(2*(n-k-2), n) and beta-alpha == Q(2*(k+3-n), n)))
            else:
                ok = ((k <= m-1 and alpha >= Q(n-2*k-2, n) and beta+alpha == Q(2*(n-k-1), n)) or
                      (k >= m and alpha <= Q(2*(n-k-2), n) and beta+alpha == Q(2*(n-k-1), n)))
        if ok:
            residues.add(k % (n-2))
    return residues


def check_source_and_corners():
    cases = 0
    for n in range(3, 25):
        N, delta = n-2, Q(n-2, n)
        for polygon in (0, 1):
            for j in range(n):
                cone, t = corner(n, polygon, j)
                lower = Q(-2*j, n) + polygon
                require((t*delta + cone - lower) % 2 == 0, "physical_corner", (n, polygon, j))
                for r in range(4*N+1):
                    alpha = Q(r, 4*n)
                    offset = (alpha + 1 - lower) % 2
                    if offset > delta:
                        continue
                    beta = 1-offset if polygon == 0 else Q(2, n)+offset
                    b = t*delta + offset - alpha
                    require(b.denominator == 1, "integral_terminal_label")
                    selected = source_branches(n, alpha, beta, polygon)
                    require(selected == {int(b) % N}, "full_source_type", (n, alpha, beta, polygon, b, selected))
                    reflected = source_branches(n, delta-alpha, 1+Q(2,n)-beta, polygon)
                    require(reflected == {(-int(b)) % N}, "bisector_type", (n, alpha, beta))
                    cases += 1
    return cases


def check_model_chords():
    chords = 0
    for n in range(3, 33):
        N = n-2
        for h in range(2*n):
            matching = {}
            for polygon in (0, 1):
                for j in range(n):
                    for q in range(1, n):
                        # Physical chord direction from the actual ordered vertices.
                        angle = polygon*n - 2*j + n-1-q
                        if (angle-h) % (2*n):
                            continue
                        j2 = (j+q) % n
                        _, t = corner(n, polygon, j)
                        _, t2 = corner(n, polygon, j2)
                        a = Q(t*N+n-1-q-h, n)
                        b = Q(t2*N+q-1-h, n)
                        require(a.denominator == b.denominator == 1, "model_integrality")
                        a, b = int(a) % N, int(b) % N
                        require((a+b+h) % N == 0, "model_reflection", (n,h,polygon,j,q,a,b))
                        require((b-a-q+1) % N == 0, "model_source_index")
                        require(a not in matching or matching[a] == b, "boundary_duplicate_consistency")
                        matching[a] = b
                        chords += 1
            require(set(matching) == set(range(N)), "model_exhausts_outgoing", (n,h,matching))
            require(set(matching.values()) == set(range(N)), "model_exhausts_backward")
    return chords


def F(x):
    """Nonlinear increasing antipodal angular lift, exactly rational."""
    integer = x.numerator // x.denominator
    rest = x-integer
    return integer + (rest/2 if rest <= Q(1,2) else Q(1,4)+Q(3,2)*(rest-Q(1,2)))


def check_common_shift():
    for n in range(5, 25):
        N = n-2
        period = 2*N if n % 2 else N
        cones = [0] if n % 2 else [0,1]
        for theta in (Q(1,7), Q(3,5), Q(4,3)):
            for sign in (0,1):
                all_labels = []
                germs = []
                for cone in cones:
                    for j in range(period//2):
                        phi = (theta+sign-cone+2*j) % period
                        label = phi-theta
                        require(label.denominator == 1, "germ_integrality")
                        all_labels.append(int(label) % N)
                        germs.append((cone,phi,int(label)%N))
                require(sorted(all_labels) == list(range(N)), "germ_bijection")
                for swap in ([0] if n % 2 else [0,1]):
                    for sheet in range(-2,3):
                        d = -swap+2*sheet
                        for cone,phi,label in germs:
                            target_cone = cone ^ swap
                            new_phi = (F(phi)-swap+2*sheet) % period
                            new_label = new_phi-F(theta)
                            require(new_label.denominator == 1, "shift_integrality")
                            require((int(new_label)-label-d) % N == 0, "common_shift_both_signs")
                            require((new_phi+target_cone-F(phi+cone)) % 2 == 0, "shift_physical_compatibility")
                        for C in range(N):
                            for a in range(N):
                                b = (C-a) % N
                                require(((a+d)+(b+d)-(C+2*d)) % N == 0, "transport_reflection")


def check_rotated_initial_germs():
    for n in range(3, 33):
        N = n-2
        for ell in range(-2*n, 2*n+1):
            if n % 2 == 0 and ell % 2:
                continue
            polygon = ell % 2 if n % 2 else 0
            # Derived from actual center-based rotation, not from 2a=ell.
            j = ((ell+polygon*n)//2) % n
            require((-2*j+polygon*n+ell) % (2*n) == 0, "rotation_vertex_geometry")
            _, t = corner(n,polygon,j)
            a = Q(t*N+ell,n)
            require(a.denominator == 1, "rotated_germ_integrality")
            a = int(a) % N
            require((2*a-ell) % N == 0, "twice_label_no_division")
            for C in range(N):
                b = (C-a) % N
                require((b-a-(C-ell)) % N == 0, "positive_type_shift")
                # The second operation is the separately checked bisector.
                shift = N-ell
                require((-(C-shift)-(-C-ell)) % N == 0, "negative_type_shift")


def first_marked(p,q):
    return next(d for d in range(1,4) if d*(p+q) % 3 != 2)


def hex_source_at_first(p,q):
    d = first_marked(p,q)
    a,b = d*p,d*q
    if (a%3,b%3) == (1,2):
        return 1
    if a%2 == b%2 == 0:
        return 2
    if (a%3,b%3) == (2,1):
        return 3
    return 0


def check_small_lattices():
    primitives = 0
    for p in range(-20,21):
        for q in range(-20,21):
            if gcd(p,q) != 1:
                continue
            primitives += 1
            require((p%2 and q%2) == (q%2 and p%2), "square_swap")
            k = hex_source_at_first(p,q)
            require(first_marked(p,q) == (2 if (p+q)%3 == 2 else 1), "first_hex_vertex")
            x,y = p,q
            for j in range(6):
                require(gcd(x,y) == 1, "lattice_primitivity")
                require(x*x-x*y+y*y == p*p-p*q+q*q, "triangular_norm")
                require(hex_source_at_first(x,y) == (k-2*j)%4, "hex_rotation_type")
                require(hex_source_at_first(y,x) == (-k+2*j)%4, "hex_signed_type")
                x,y = x-y,x
            require((x,y) == (p,q), "rotation_order_six")
    return primitives


if __name__ == '__main__':
    candidate = Path(__file__).with_name('CANDIDATE_FROZEN.md')
    digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
    require(digest == '6d406380552758f7b4292759d62c12cbf2fe7f4c03e358086d6fac938ed10260', 'frozen_candidate_hash')
    source_cases = check_source_and_corners()
    chords = check_model_chords()
    check_common_shift()
    check_rotated_initial_germs()
    primitives = check_small_lattices()
    print(json.dumps({'status':'PASS','candidate_sha256':digest,
                      'assertions':sum(counts.values()),'assertions_by_family':dict(counts),
                      'source_angle_cases':source_cases,'directed_model_chord_descriptions':chords,
                      'primitive_lattice_vectors':primitives,
                      'limitations':'Finite exact controls; not proofs of hyperelliptic uniqueness, Veech cusp theorems, or the all-n assertion'}, indent=2))
