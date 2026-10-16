"""Finite consistency checks only; the infinite proof is in PROOF.md."""
from collections import Counter, deque
from itertools import product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def shift(f, k):
    n = len(f)
    return tuple(f[(i - k) % n] for i in range(n))


def t_move(x, k=1):
    f, pos = x
    return (shift(f, k), (pos + k) % len(f))


def lamp_move(x, at=0, amount=1, q=2):
    f, pos = x
    out = list(f)
    out[at % len(f)] = (out[at % len(f)] + amount) % q
    return (tuple(out), pos)


def cyclic_states(length, q):
    return [(f, p) for f in product(range(q), repeat=length) for p in range(length)]


def slab_neighbors(x, m, q):
    r = x[1] % m
    out = {lamp_move(x, amount=1, q=q), lamp_move(x, amount=-1, q=q)}
    if r < m - 1:
        out.add(t_move(x))
    if r > 0:
        out.add(t_move(x, -1))
    out.discard(x)
    return out


def normalize(x, m):
    return (t_move(x, -(x[1] % m)), x[1] % m)


def components(states, m, q):
    unseen = set(states)
    sizes = Counter()
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        frontier = [root]
        size = 0
        while frontier:
            x = frontier.pop()
            size += 1
            for y in slab_neighbors(x, m, q):
                if y in unseen:
                    unseen.remove(y)
                    frontier.append(y)
        sizes[size] += 1
    return dict(sorted(sizes.items()))


def sparse(f):
    return tuple(sorted((k, v) for k, v in f.items() if v))


def s_shift(f, n):
    return sparse({k + n: v for k, v in f})


def s_add(f, g):
    out = dict(f)
    for k, v in g:
        out[k] = out.get(k, 0) + v
    return sparse(out)


def multiply(x, y):
    f, k = x
    g, l = y
    return (s_add(f, s_shift(g, k)), k + l)


def inverse(x):
    f, k = x
    return (s_shift(tuple((i, -v) for i, v in f), -k), -k)


def compute():
    counts = Counter()
    models = []
    for length, q in [(2, 3), (3, 2), (4, 2), (6, 2)]:
        states = cyclic_states(length, q)
        divisors = [m for m in range(1, length + 1) if length % m == 0]
        for m in divisors:
            for x in states:
                z, r = normalize(x, m)
                require(z[1] % m == 0, 'base residue')
                require(t_move(z, r) == x, 'coordinate inverse')
                az, ar = normalize(lamp_move(x, q=q), m)
                require(ar == r and az == lamp_move(z, at=-r, q=q), 'lamp conjugation sign')
                counts['coordinate_identities'] += 3
                if r < m - 1:
                    tz, tr = normalize(t_move(x), m)
                    require(tz == z and tr == r + 1, 'interior shift identity')
                    counts['interior_shift_identities'] += 1
                for y in slab_neighbors(x, m, q):
                    require(x in slab_neighbors(y, m, q), 'undirected slab')
                    counts['edge_symmetry_checks'] += 1
            actual = components(states, m, q)
            expected = {m * q ** m: (length // m) * q ** (length - m)}
            require(actual == expected, 'complete slab component inventory')
            models.append({'length': length, 'lamp_modulus': q, 'slab_width': m,
                           'state_count': len(states), 'component_sizes': actual})
            counts['complete_component_inventories'] += 1
        for m in divisors:
            for n in divisors:
                if n % m:
                    continue
                for x in states:
                    require(slab_neighbors(x, m, q) <= slab_neighbors(x, n, q), 'divisor monotonicity')
                    counts['nested_slab_vertex_checks'] += 1
        for x in states:
            for i in range(length):
                for j in range(length):
                    require(lamp_move(lamp_move(x, i, q=q), j, q=q) ==
                            lamp_move(lamp_move(x, j, q=q), i, q=q), 'commuting lamps')
                    counts['lamp_commutations'] += 1

    # A finite pullback witnesses the exact algebra in the topological lifting lemma.
    for length, q, m, n in [(2, 2, 2, 6), (3, 2, 3, 12), (4, 2, 2, 8)]:
        base = cyclic_states(length, q)
        space = [(x, j) for x in base for j in range(n) if x[1] % m == j % m]
        space_set = set(space)
        require(len(space) == len(base) * (n // m), 'pullback fiber cardinality')
        counts['pullback_cardinality_checks'] += 1
        for x, j in space:
            for kind in ['a', 't']:
                y = lamp_move(x, q=q) if kind == 'a' else t_move(x)
                delta = 0 if kind == 'a' else 1
                out = (y, (j + delta) % n)
                require(out in space_set, 'pullback invariant')
                require(out[1] % m == y[1] % m, 'lift compatibility')
                counts['pullback_generator_checks'] += 2

    # W arithmetic uses honest finitely supported integer lamps, no cyclic reduction.
    lamps = [sparse(dict(zip([-1, 0, 1], vals))) for vals in product([-1, 0, 1], repeat=3)]
    group_sample = [(f, k) for f in lamps for k in range(-2, 3)]
    identity = ((), 0)
    for x in group_sample:
        require(multiply(x, inverse(x)) == identity, 'group inverse')
        counts['inverse_checks'] += 1
        for g in group_sample:
            y = multiply(g, x)
            qx = s_shift(x[0], -x[1])
            qy = s_shift(y[0], -y[1])
            expected = s_add(s_shift(g[0], -(g[1] + x[1])), qx)
            require(qy == expected, 'integer-height normalization cocycle')
            require(y[1] == x[1] + g[1], 'height cocycle')
            counts['normalization_cocycle_checks'] += 2

    # Explicit short words realizing lamps supported in a fixed positive interval.
    for d in range(1, 5):
        for vals in product(range(-2, 3), repeat=d):
            x = identity
            used = 0
            for i, v in enumerate(vals):
                # right multiplication changes the lamp at the cursor position
                x = multiply(x, ((((0, v),) if v else ()), 0))
                used += abs(v)
                if i + 1 < d:
                    x = multiply(x, ((), 1))
                    used += 1
            x = multiply(x, ((), -(d - 1)))
            used += d - 1
            require(x == (sparse(dict(enumerate(vals))), 0), 'lamp word endpoint')
            require(used == sum(abs(v) for v in vals) + 2 * (d - 1), 'lamp word length')
            counts['lamp_word_checks'] += 2

    # Deliberate wrong-sign and wrap controls must be detected.
    wrong_sign_detected = 0
    wrap_detected = 0
    for x in cyclic_states(6, 2):
        z, r = normalize(x, 6)
        az, _ = normalize(lamp_move(x), 6)
        if az != lamp_move(z, at=r):
            wrong_sign_detected += 1
        bz, br = normalize(x, 3)
        if br == 2:
            tz, tr = normalize(t_move(x), 3)
            require(tr == 0, 'wrap residue')
            if tz != bz:
                wrap_detected += 1
    require(wrong_sign_detected > 0, 'wrong sign negative control')
    require(wrap_detected > 0, 'uncut wrap negative control')

    # Increasing interval grids on Z miss the same edge forever in this control.
    for exponent in range(1, 25):
        m = 2 ** exponent
        require((-1) // m != 0 // m, 'persistent boundary control')
        counts['persistent_boundary_checks'] += 1

    # Finite analog of the bounded-height pullback exhaustion.
    base_points = list(range(16))
    lifted = [(z, h) for z in base_points for h in range(-4, 5)]
    previous = set()
    for stage in range(5):
        width = 2 ** stage
        relation = {(x, y) for x in lifted for y in lifted
                    if x == y or (abs(x[1]) <= stage and abs(y[1]) <= stage and x[0] // width == y[0] // width)}
        require(previous <= relation, 'bounded height nested')
        classes = {x: set() for x in lifted}
        for x, y in relation:
            classes[x].add(y)
        for x in lifted:
            cls = classes[x]
            require(len(cls) <= (2 * stage + 1) * width, 'bounded height class size')
            for y in cls:
                require(classes[y] == cls, 'bounded height equivalence')
                counts['bounded_height_class_checks'] += 1
        previous = relation
    require(len(previous) == len(lifted) ** 2, 'bounded height final exhaustion')

    return {'schema': 1, 'scope': 'finite consistency checks, not an infinite proof',
            'counts': dict(sorted(counts.items())), 'models': models,
            'negative_controls': {'wrong_sign_witnesses': wrong_sign_detected,
                                  'uncut_wrap_witnesses': wrap_detected},
            'all_checks_passed': True}
