"""Small exact checks of proved identities, not evidence of asymptotic resolution."""
import itertools, json
import sympy as s
x = s.symbols('x')
results = {'finite_field_counts': [], 'composition_examples': []}
for p in (3, 5):
    for n in (2, 3, 4):
        square_residues = {a * a % p for a in range(p)}
        counts = {'zero': 0, 'nonzero_square': 0, 'nonsquare': 0}
        for aa in itertools.product(range(p), repeat=n):
            f = x ** n + sum((a * x ** i for i, a in enumerate(aa)))
            d = int(s.discriminant(f, x)) % p
            counts['zero' if d == 0 else 'nonzero_square' if d in square_residues else 'nonsquare'] += 1
        expected = (p ** n + p ** (n - 1)) // 2
        if not counts['zero'] + counts['nonzero_square'] == expected:
            raise AssertionError('Exact identity check failed')
        if not counts['nonzero_square'] == counts['nonsquare']:
            raise AssertionError('Exact identity check failed')
        results['finite_field_counts'].append(dict(p=p, n=n, expected_square_or_zero=expected, **counts))
for m in range(1, 7):
    g = x ** m + x + 2 if m > 1 else x + 2
    lhs = s.discriminant(g.subs(x, x * x), x)
    rhs = (-1) ** m * 4 ** m * g.subs(x, 0) * s.discriminant(g, x) ** 2
    if not lhs == rhs:
        raise AssertionError('Exact identity check failed')
    results['composition_examples'].append(dict(m=m, g=str(g), discriminant=str(lhs), match=True))
print(json.dumps(results, indent=2))
