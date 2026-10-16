#!/usr/bin/env python3
"""Independent exact Hessian-group audit over Q[w]/(w^2+w+1).

No third-party dependencies, floating point, or assert statements. A nonzero
exit status signals a failed explicit check, including under python -O.
"""
from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction as F
import argparse
import json
from pathlib import Path


@dataclass(frozen=True)
class Q:
    a: F = F(0)
    b: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))
    @staticmethod
    def coerce(x):
        return x if isinstance(x, Q) else Q(x)
    def __add__(self, other):
        y = Q.coerce(other)
        return Q(self.a+y.a, self.b+y.b)
    __radd__ = __add__
    def __neg__(self):
        return Q(-self.a, -self.b)
    def __sub__(self, other):
        return self + -Q.coerce(other)
    def __rsub__(self, other):
        return Q.coerce(other) + -self
    def __mul__(self, other):
        y = Q.coerce(other)
        return Q(self.a*y.a-self.b*y.b,
                 self.a*y.b+self.b*y.a-self.b*y.b)
    __rmul__ = __mul__
    def conjugate(self):
        return Q(self.a-self.b, -self.b)
    def inverse(self):
        norm = self.a*self.a-self.a*self.b+self.b*self.b
        if not norm:
            raise ZeroDivisionError('zero in Q(omega)')
        z = self.conjugate()
        return Q(z.a/norm, z.b/norm)
    def __truediv__(self, other):
        return self * Q.coerce(other).inverse()
    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        x, y = Q(1), self
        while n:
            if n % 2:
                x = x*y
            y = y*y
            n //= 2
        return x
    def __bool__(self):
        return bool(self.a or self.b)
    def encoded(self):
        return [str(self.a), str(self.b)]


Z, O, W = Q(), Q(1), Q(0, 1)
I = tuple(O if i//3 == i%3 else Z for i in range(9))
A = tuple(map(Q.coerce, (0,0,1, 1,0,0, 0,1,0)))
B = (O,Z,Z, Z,W,Z, Z,Z,W**2)
C = (O,Z,Z, Z,O,Z, Z,Z,W)
D = (W**2,W,O, W,W**2,O, O,O,O)


def mm(a, b):
    return tuple(sum((a[3*i+k]*b[3*k+j] for k in range(3)), Z)
                 for i in range(3) for j in range(3))


def mv(a, v):
    return tuple(sum((a[3*i+k]*v[k] for k in range(3)), Z)
                 for i in range(3))


def normalize(v):
    d = next((x for x in v if x), None)
    if d is None:
        raise ValueError('zero projective representative')
    return tuple(x/d for x in v)


def pm(a, b):
    return normalize(mm(a, b))


def power(a, n):
    x = I
    for _ in range(n):
        x = pm(x, a)
    return x


def adjoint(a):
    return tuple(a[3*j+i].conjugate() for i in range(3) for j in range(3))


def determinant(a):
    return (a[0]*(a[4]*a[8]-a[5]*a[7])
            -a[1]*(a[3]*a[8]-a[5]*a[6])
            +a[2]*(a[3]*a[7]-a[4]*a[6]))


def charpoly(a):
    # det(zI-a) = z^3 + bz^2 + cz + d.
    tr = a[0]+a[4]+a[8]
    c = a[0]*a[4]+a[0]*a[8]+a[4]*a[8]-a[1]*a[3]-a[2]*a[6]-a[5]*a[7]
    return (-tr, c, -determinant(a))


def discriminant(a):
    b,c,d = charpoly(a)
    return b*b*c*c-4*c**3-4*b**3*d-27*d*d+18*b*c*d


CHECKS = []
def require(condition, description):
    if not condition:
        raise RuntimeError('CHECK FAILED: '+description)
    CHECKS.append(description)


def closure(generators):
    words = {I: ''}
    todo = deque([I])
    while todo:
        x = todo.popleft()
        for name,y in generators:
            z = pm(x,y)
            if z not in words:
                words[z] = words[x]+name
                todo.append(z)
                if len(words)>1000:
                    raise RuntimeError('closure exceeded 1000 exact projective classes')
    return words


def cycle_type(p):
    seen, sizes = set(), []
    for i in range(len(p)):
        if i not in seen:
            j,n = i,0
            while j not in seen:
                seen.add(j)
                n += 1
                j = p[j]
            sizes.append(n)
    return sorted(sizes)


def mat2mul(x, y):
    return tuple(sum(x[2*i+k]*y[2*k+j] for k in range(2))%3
                 for i in range(2) for j in range(2))


def mat2inverse(x):
    return (x[3]%3, -x[1]%3, -x[2]%3, x[0]%3)


def run(args):
    require(W**3 == O and W != O and W**2+W+O == Z, 'field relation and primitive cube root')
    for name,g,k in [('A',A,1), ('B',B,1), ('C',C,1), ('D',D,3)]:
        require(mm(adjoint(g),g) == tuple(k*x for x in I), name+' is projectively unitary')
        require(bool(determinant(g)), name+' is invertible')
    require(mm(B,A) == tuple(W*x for x in mm(A,B)), 'GL central commutator BA=omega AB')
    if args.negative_control == 'gl_commutes':
        require(mm(B,A) == mm(A,B), 'NEGATIVE CONTROL: false GL commutation')
    require(mm(mm(C,A),power(C,2)) == mm(A,B), 'GL identity CAC^-1=AB')
    require(mm(mm(C,B),power(C,2)) == B, 'GL identity CBC^-1=B')
    # D^-1 = D*/3. These identities retain their GL scalar factors.
    require(mm(D,A) == tuple(W**2*x for x in mm(power(B,2),D)), 'GL identity DA=omega^2 B^2 D')
    require(mm(D,B) == tuple(W**2*x for x in mm(A,D)), 'GL identity DB=omega^2 AD')
    for a in (1,2):
        for b in range(3):
            for c in range(3):
                monomial = mm(mm(power(A,a),power(B,b)),power(C,c))
                require(charpoly(monomial) == (Z,Z,-W**c), 'weighted three-cycle charpoly z^3-omega^c')
    p0 = (O,-O,Z)
    labels = [(a,b) for a in range(3) for b in range(3)]
    translations = {ab: pm(power(A,ab[0]),power(B,ab[1])) for ab in labels}
    points = [normalize(mv(translations[ab],p0)) for ab in labels]
    require(len(set(points)) == 9, 'translation orbit has nine distinct projective points')
    for p in points:
        require(sum((x**3 for x in p), Z) == Z and p[0]*p[1]*p[2] == Z,
                'each orbit point is a Hesse-pencil base point')
    for name,g in [('C',C),('D',D)]:
        require(normalize(mv(g,p0)) == normalize(p0), name+' fixes the chosen p0')
    group = closure([('A',A),('B',B),('C',C),('D',D)])
    complement = closure([('C',C),('D',D)])
    expected = 215 if args.negative_control == 'group_order' else 216
    require(len(group) == expected, 'projective group has expected order '+str(expected))
    require(len(complement) == 24, 'point-stabilizer complement has order 24')
    require(len(set(translations.values())) == 9, 'translation subgroup has order nine')
    require(set(complement).intersection(translations.values()) == {I}, 'complement intersects translations trivially')
    require({pm(k,l) for k in translations.values() for l in complement} == set(group),
            'all 216 elements have unique translation-complement form')
    perms, affines, records = {}, {}, []
    for n,(g,word) in enumerate(group.items()):
        perm = tuple(points.index(normalize(mv(g,p))) for p in points)
        require(len(set(perm)) == 9, 'matrix action permutes all nine flexes')
        t = labels[perm[0]]
        e1,e2 = labels[perm[labels.index((1,0))]], labels[perm[labels.index((0,1))]]
        l = ((e1[0]-t[0])%3,(e2[0]-t[0])%3,(e1[1]-t[1])%3,(e2[1]-t[1])%3)
        require((l[0]*l[3]-l[1]*l[2])%3 == 1, 'linear part has determinant one')
        require(all(labels[perm[i]] == ((l[0]*a+l[1]*b+t[0])%3,
                                        (l[2]*a+l[3]*b+t[1])%3)
                    for i,(a,b) in enumerate(labels)), 'complete nine-point action equals affine formula')
        fixed = [i for i,j in enumerate(perm) if i == j]
        repeated = not discriminant(g)
        require(bool(fixed) or not repeated, 'fixed-flex-free element has nonzero spectral discriminant')
        require(not determinant(g) == Z, 'group representative remains invertible')
        perms[g], affines[g] = perm, (l,t)
        order,x = 1,g
        subgroup = {I,g}
        while x != I:
            x = pm(x,g)
            order += 1
            subgroup.add(x)
            if order > 216:
                raise RuntimeError('element order exceeded group order')
        if g == I:
            order = 1
        require(power(g,order) == I, 'exact projective order verified')
        records.append({'id': n, 'word': word or 'I', 'matrix_Qomega': [x.encoded() for x in g],
                        'affine_L': list(l), 'affine_t': list(t), 'permutation': list(perm),
                        'fixed_flex_labels': [labels[i] for i in fixed], 'cycle_type': cycle_type(perm),
                        'order': order, 'repeated_eigenvalue': repeated,
                        'charpoly_b_c_d': [x.encoded() for x in charpoly(g)],
                        'discriminant': discriminant(g).encoded()})
    require(len(set(perms.values())) == 216, 'nine-flex permutation representation is faithful')
    sl2 = {l for l,t in affines.values() if t == (0,0)}
    require(len(sl2) == 24 and {g for g in group if perms[g][0] == 0} == set(complement),
            'exact stabilizer is the order-24 complement')
    require(affines[normalize(C)] == ((1,0,1,1),(0,0)), 'C induces lower shear')
    require(cycle_type(perms[normalize(C)]) == [1,1,1,3,3], 'C monodromy is 1^3 3^2')
    if args.negative_control == 'c_fixes_all':
        require(perms[normalize(C)] == tuple(range(9)), 'NEGATIVE CONTROL: false full-nine-sheet trivialization')
    unit = (1,0,0,1)
    unipotents = {l for l in sl2 if l != unit and (l[0]+l[3])%3 == 2}
    require(len(unipotents) == 8, 'eight nontrivial determinant-one unipotents')
    remaining, classes = set(unipotents), []
    while remaining:
        x = min(remaining)
        cl = {mat2mul(mat2mul(q,x),mat2inverse(q)) for q in sl2}
        require(cl.issubset(unipotents), 'unipotent conjugacy class remains unipotent')
        classes.append(sorted(cl))
        remaining -= cl
    expected_classes = 1 if args.negative_control == 'one_unipotent_class' else 2
    require(len(classes) == expected_classes, 'nontrivial unipotents have expected number of SL2 classes '+str(expected_classes))
    require(sorted(map(len,classes)) == [4,4], 'both unipotent classes have size four')
    require(all(any(u in cl for cl in classes) for u in [(1,0,1,1),(1,0,2,1)]),
            'the two lower shears represent the classes')
    require(not any((1,0,1,1) in cl and (1,0,2,1) in cl for cl in classes),
            'inverse lower shears are not SL2-conjugate')
    subgroups = {}
    for g in group:
        x, subgroup = I,{I}
        while True:
            x = pm(x,g)
            if x == I:
                break
            subgroup.add(x)
        subgroups[frozenset(subgroup)] = True
    subgroup_records = []
    id_of = {g:i for i,g in enumerate(group)}
    for subgroup in subgroups:
        common = [i for i in range(9) if all(perms[g][i] == i for g in subgroup)]
        circle_eligible = all(not discriminant(g) for g in subgroup)
        if circle_eligible:
            require(bool(common), 'every circle-eligible cyclic subgroup has a common fixed flex')
        subgroup_records.append({'elements': sorted(id_of[g] for g in subgroup), 'order': len(subgroup),
                                 'circle_eligible': circle_eligible,
                                 'common_fixed_flex_labels': [labels[i] for i in common]})
    eligible = [s for s in subgroup_records if s['circle_eligible']]
    require(Counter(s['order'] for s in eligible) == Counter({1:1,2:9,3:12}),
            'circle-eligible subgroups: trivial, nine C2, twelve C3')
    require(sum(not r['fixed_flex_labels'] for r in records) == 56, '56 fixed-flex-free elements')
    require(sum(r['repeated_eigenvalue'] for r in records) == 34, '34 repeated-spectrum elements including identity')
    summary = {'status':'PASS', 'arithmetic':'exact rational pairs in Q(omega); omega^2+omega+1=0',
               'group_order':len(group), 'complement_order':len(complement),
               'fixed_flex_histogram':dict(sorted(Counter(len(r['fixed_flex_labels']) for r in records).items())),
               'projective_order_histogram':dict(sorted(Counter(r['order'] for r in records).items())),
               'spectrum_by_order':{str(o):dict(Counter('repeated' if r['repeated_eigenvalue'] else 'simple'
                                                     for r in records if r['order']==o))
                                    for o in sorted({r['order'] for r in records})},
               'generator_affine_actions':{name:{'L':list(affines[normalize(g)][0]),'t':list(affines[normalize(g)][1])}
                                           for name,g in [('A',A),('B',B),('C',C),('D',D)]},
               'unipotent_conjugacy_classes':classes,
               'cyclic_subgroups':len(subgroups),
               'circle_eligible_subgroup_orders':dict(sorted(Counter(s['order'] for s in eligible).items())),
               'eligible_common_fixed_counts':dict(sorted(Counter(len(s['common_fixed_flex_labels']) for s in eligible).items())),
               'explicit_checks_passed':len(CHECKS)}
    if args.output:
        out = Path(args.output)
        out.mkdir(parents=True,exist_ok=True)
        (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
        (out/'elements.json').write_text(json.dumps(records,indent=2)+'\n')
        (out/'cyclic_subgroups.json').write_text(json.dumps(subgroup_records,indent=2)+'\n')
        (out/'checks.json').write_text(json.dumps(CHECKS,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    parser.add_argument('--negative-control', choices=['group_order','gl_commutes','c_fixes_all','one_unipotent_class'])
    run(parser.parse_args())
