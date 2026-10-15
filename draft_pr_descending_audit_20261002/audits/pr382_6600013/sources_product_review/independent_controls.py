"""Independent controls: digit parity, exact rational rotations, sparse QQ rank.

No candidate module is imported. The Thue-Morse completeness argument uses
the 2-automatic digit-parity formula, not the candidate substitution routine.
The rotation language uses a rational isolating interval for sqrt(2), with
an explicit finite order certificate for the boundary points used here.
"""
from fractions import Fraction
from itertools import product
from math import prod, comb
import json
import sympy as S

COUNT = 0


def require(condition):
    global COUNT
    assert condition
    COUNT += 1


def tm_words(n):
    # If q >= n, every window lies inside at most two aligned q-blocks.
    # t(h*q+r)=t(h) xor t(r). The high labels t(0),...,t(8)
    # contain all four adjacent binary pairs, hence these finite windows
    # exhaust the infinite automatic sequence's length-n factors.
    q = 1
    while q < n:
        q *= 2
    high = [i.bit_count() % 2 for i in range(9)]
    require(set(zip(high, high[1:])) == set(product((0, 1), repeat=2)))
    digits = tuple(i.bit_count() % 2 for i in range(9 * q))
    return {digits[i:i+n] for i in range(len(digits)-n+1)}


P, Q = 195025, 470832
LOW = Fraction(P-1, Q)
HIGH = Fraction(P, Q)
require((LOW+1)**2 < 2 < (HIGH+1)**2)


def rotation_words(n):
    # For each k used here, prove k*alpha's floor and then the ordering of
    # {-k*alpha} using the rational enclosure LOW < alpha < HIGH.
    require(n * (HIGH-LOW) < 1)
    floors = {}
    for k in range(1, n+1):
        lo, hi = k*LOW, k*HIGH
        floors[k] = lo.numerator // lo.denominator
        require(floors[k] == hi.numerator // hi.denominator)
    bounds = {k: (floors[k]+1-k*HIGH, floors[k]+1-k*LOW)
              for k in range(1, n+1)}
    order = sorted(bounds, key=lambda k: sum(bounds[k]))
    for u, v in zip(order, order[1:]):
        require(bounds[u][1] < bounds[v][0])
    # Choose midpoint intercepts with guaranteed positions between the
    # exact irrational cuts. The finite rational code is constant throughout
    # each certified interval, including the final endpoints 0 and 1.
    cuts = [(Fraction(0), Fraction(0))] + [bounds[k] for k in order] + [(Fraction(1), Fraction(1))]
    out = set()
    for a, b in zip(cuts, cuts[1:]):
        x = (a[1]+b[0])/2
        fs = []
        for k in range(n+1):
            l, h = x+k*LOW, x+k*HIGH
            fl, fh = l.numerator//l.denominator, h.numerator//h.denominator
            require(fl == fh)
            fs.append(fl)
        out.add(tuple(fs[k+1]-fs[k] for k in range(n)))
    require(len(out) == n+1)
    return out


def crop(array, x, y, width, height):
    return tuple(row[x:x+width] for row in array[y:y+height])


def arrays(n, m, shear=True):
    xs = tm_words(n+m if shear else n)
    ys = rotation_words(m)
    return sorted({tuple(tuple((x[i+j], x[i+j+1], y[j]) if shear else (x[i],y[j])
                              for i in range(n)) for j in range(m))
                   for x in xs for y in ys})


def rectangular_homology(n, m):
    # Independent sparse cellular construction, using geometric direction
    # keys so coincident horizontal and vertical labels cannot be conflated.
    verts = arrays(n, m)
    h = arrays(n+1, m)
    v = arrays(n, m+1)
    faces = arrays(n+1, m+1)
    edges = [('h', a) for a in h] + [('v', a) for a in v]
    vi = {a:i for i,a in enumerate(verts)}
    ei = {a:i for i,a in enumerate(edges)}
    d1 = S.zeros(len(verts), len(edges))
    for e, (direction, a) in enumerate(edges):
        end = (1, 0) if direction == 'h' else (0, 1)
        d1[vi[crop(a, 0, 0, n, m)], e] -= 1
        d1[vi[crop(a, *end, n, m)], e] += 1
    d2 = S.zeros(len(edges), len(faces))
    for f, a in enumerate(faces):
        for key, sign in [(('h',crop(a,0,0,n+1,m)),1),
                          (('h',crop(a,0,1,n+1,m)),-1),
                          (('v',crop(a,1,0,n,m+1)),1),
                          (('v',crop(a,0,0,n,m+1)),-1)]:
            d2[ei[key], f] += sign
    require(d1*d2 == S.zeros(len(verts),len(faces)))
    # SymPy DomainMatrix elimination supplies an independent exact backend.
    rank1 = d1.to_DM().convert_to(S.QQ).rank()
    rank2 = d2.to_DM().convert_to(S.QQ).rank()
    betti = [len(verts)-rank1, len(edges)-rank1-rank2, len(faces)-rank2]
    cells = [len(verts), len(edges), len(faces)]
    chi = cells[0]-cells[1]+cells[2]
    require(betti[0] == 1)
    require(chi == betti[0]-betti[1]+betti[2])
    return dict(n=n,m=m,cells=cells,betti=betti,chi=chi)


def main():
    p = {n:len(tm_words(n)) for n in range(1,258)}
    require([p[n] for n in range(1,7)] == [2,4,6,10,12,16])
    for n in range(2,129):
        require(p[2*n] == p[n]+p[n+1])
        require(p[2*n+1] == 2*p[n+1])
    for n in range(1,257):
        require(p[n+1]-p[n] in (2,4))
        require(p[n] <= 4*n)
    extremes=[]
    for a in range(2,8):
        for n,expected in [(2**(a-1),2*2**(a-1)+6), (3*2**(a-2),-2*3*2**(a-2))]:
            chi=(n+2)*(p[2*n+2]-2*p[2*n+1]+p[2*n])+p[2*n+1]-p[2*n]
            require(chi == expected)
            extremes.append(dict(n=n,chi=chi))
    matrices=[rectangular_homology(n,m) for n,m in [(1,1),(2,2),(3,3),(2,3),(3,2),(1,4),(4,1),(4,4)]]
    for item in matrices:
        n,m=item['n'],item['m']
        require(item['cells'][0] == p[n+m]*(m+1))
        require(item['chi'] == (m+2)*(p[n+m+2]-2*p[n+m+1]+p[n+m])+p[n+m+1]-p[n+m])
    # Direct Cartesian product patterns generated literally for three
    # independent rotations and their Kunneth graded dimensions.
    for d in range(1,5):
        for n in range(1,7):
            langs=[rotation_words(n) for _ in range(d)]
            cubes={tuple(words) for words in product(*langs)}
            require(len(cubes)==(n+1)**d)
        require(sum(comb(d,k)*2**k for k in range(d+1))==3**d)
    for rs in product(range(11),repeat=4):
        require(prod(1+r for r in rs) <= 3**4*prod(max(1,r-1) for r in rs))
    print(json.dumps(dict(assertions=COUNT,tm_complete_lengths=257,
                         exact_shear_complexes=matrices,euler_extremes=extremes,
                         rotation_method='rational enclosure and all cut-order certificates',
                         tm_method='binary digit parity with nine aligned blocks',
                         limitation='Finite controls do not prove the arbitrary tiling implication.'),indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
