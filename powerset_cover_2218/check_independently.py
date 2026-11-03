"""Independent exact-integer checks; no optimization solver is imported."""
from pathlib import Path
from itertools import combinations, product
import json, hashlib
ROOT = Path(__file__).resolve().parent
SRC = ROOT
OUT = Path(__file__).resolve().parent
checks = []
for p in sorted([*SRC.glob('milp_n*_h*.json'), SRC / 'local_n10_h4.json', SRC / 'local_n11_h4.json']):
    r = json.loads(p.read_text())
    if 'witness' not in r:
        continue
    n, h = (r['n'], r['h'])
    f = {int(k): v for k, v in r['witness'].items()}
    expected = {a for a in range(1 << n) if a.bit_count() <= h}
    if set(f) != expected or any((not isinstance(v, int) or not 0 <= v < n for v in f.values())):
        raise ValueError(p)
    f = {a: f.get(a, 0) for a in range(1 << n)}
    count = 0
    for y in range(1 << n):
        if y.bit_count() < h:
            continue
        seen = set()
        a = y
        while True:
            seen.add(f[a])
            if a == 0:
                break
            a = a - 1 & y
        if seen != set(range(n)):
            raise ValueError((p, y, seen))
        count += 1
    checks.append({'file': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'n': n, 'h': h, 'full_supersets_checked': count, 'passed': True})
edges = list(combinations(range(7), 2))
ix = {e: i for i, e in enumerate(edges)}

def solve(vertices):
    constraints = []
    for tri in combinations(range(7), 3):
        es = tuple((ix[e] for e in combinations(tri, 2)))
        vc = {vertices[v] for v in tri}
        allowed = [c for c in product(range(6), repeat=3) if len(vc | set(c)) >= 5]
        constraints.append((es, allowed))
    nodes = 0

    def dfs(dom):
        nonlocal nodes
        nodes += 1
        while True:
            changed = False
            for es, allowed in constraints:
                rows = [r for r in allowed if all((r[j] in dom[e] for j, e in enumerate(es)))]
                if not rows:
                    return False
                for j, e in enumerate(es):
                    new = {r[j] for r in rows}
                    if new != dom[e]:
                        dom[e] = new
                        changed = True
            if not changed:
                break
        choices = [e for e in range(21) if len(dom[e]) > 1]
        if not choices:
            return True
        e = min(choices, key=lambda e: len(dom[e]))
        for c in sorted(dom[e]):
            dd = [s.copy() for s in dom]
            dd[e] = {c}
            if dfs(dd):
                return True
        return False
    sat = dfs([set(range(6)) for _ in edges])
    return {'singleton_pattern': vertices, 'satisfiable': sat, 'nodes': nodes}
csp = [solve(v) for v in [[0, 0, 1, 2, 3, 4, 5], [0, 0, 1, 1, 2, 3, 4], [0, 0, 1, 1, 2, 2, 3]]]
if any((r['satisfiable'] for r in csp)):
    raise ValueError(csp)
record = {'witness_checks': checks, 'n7_h3_independent_csp': csp, 'all_passed': True}
print(json.dumps(record, indent=2))
