"""Independent exact exterior-algebra checks of the constructive lane's formulas."""
import itertools, json, math

def mon(t):
    if len(set(t)) < len(t):
        return {}
    n = sum((t[i] > t[j] for i in range(len(t)) for j in range(i + 1, len(t))))
    return {tuple(sorted(t)): (-1) ** n}

def plus(*xs):
    d = {}
    for x in xs:
        for t, v in x.items():
            d[t] = d.get(t, 0) + v
    return {t: v for t, v in d.items() if v}

def scale(x, c):
    return {t: v * c for t, v in x.items() if v * c}

def act_monomial(t, images):
    out = {}
    for choices in itertools.product(*(list(images[k].items()) for k in t)):
        labels = tuple((x[0] for x in choices))
        coeff = math.prod((x[1] for x in choices))
        out = plus(out, scale(mon(labels), coeff))
    return out

def action(v, images):
    return plus(*(scale(act_monomial(t, images), c) for t, c in v.items()))

def identity(g):
    return {i: {i: 1} for i in range(2 * g)}

def shear(g, j):
    x = identity(g)
    x[g + j] = {g + j: 1, j: 1}
    return x

def elementary(g, i, j):
    x = identity(g)
    x[j] = {j: 1, i: 1}
    x[g + i] = {g + i: 1, g + j: -1}
    return x
rows = []
for g in range(3, 9):
    abb = 0
    aab = 0
    aaa = 0
    for i in range(g):
        for j, k in itertools.combinations(range(g), 2):
            target = mon((i, g + j, g + k))
            if i not in (j, k):
                seed = mon((j, g + j, g + k))
                delta = plus(action(seed, elementary(g, i, j)), scale(seed, -1))
                if not delta == target:
                    raise RuntimeError('Exact supplementary check failed')
            abb += 1
    for i, j in itertools.combinations(range(g), 2):
        for k in range(g):
            anchor, move = (i, j) if j != k else (j, i)
            seed = mon((anchor, g + move, g + k))
            target = mon((anchor, move, g + k))
            delta = plus(action(seed, shear(g, move)), scale(seed, -1))
            if not delta == target:
                raise RuntimeError('Exact supplementary check failed')
            if not target in (mon((i, j, g + k)), scale(mon((i, j, g + k)), -1)):
                raise RuntimeError('Exact supplementary check failed')
            aab += 1
    for i, j, k in itertools.combinations(range(g), 3):
        seed = mon((i, j, g + k))
        target = mon((i, j, k))
        if not plus(action(seed, shear(g, k)), scale(seed, -1)) == target:
            raise RuntimeError('Exact supplementary check failed')
        aaa += 1
    W = [t for t in itertools.combinations(range(2 * g), 3) if any((x < g for x in t))]
    relations = []
    seen = set()
    pivots = []
    for x in range(2 * g):
        r = plus(*(mon((x, i, g + i)) for i in range(g)))
        if not len(r) == g - 1:
            raise RuntimeError('Exact supplementary check failed')
        if not not seen & set(r):
            raise RuntimeError('Exact supplementary check failed')
        seen.update(r)
        p = min(r)
        pivots.append(p)
        if not abs(r[p]) == 1:
            raise RuntimeError('Exact supplementary check failed')
        relations.append(r)
    if not len(set(pivots)) == 2 * g:
        raise RuntimeError('Exact supplementary check failed')
    rank = len(W) - len(pivots)
    if not rank == math.comb(2 * g, 3) - math.comb(g, 3) - 2 * g:
        raise RuntimeError('Exact supplementary check failed')
    if not len(W) == abb + aab + aaa:
        raise RuntimeError('Exact supplementary check failed')
    rows.append({'g': g, 'ABB': abb, 'AAB': aab, 'AAA': aaa, 'W_rank': len(W), 'disjoint_unit_pivots': len(pivots), 'closed_lattice_rank': rank})
print(json.dumps({'status': 'PASS', 'arithmetic': 'exact integers; canonical exterior monomials', 'scope': 'Finite checks supplement index-general identities in the proof. No saturation or rational linear algebra used.', 'rows': rows}, indent=2))
