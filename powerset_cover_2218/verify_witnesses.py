"""Verify positive witnesses without scipy or any optimization solver."""
from itertools import combinations
from pathlib import Path
import json, hashlib
HERE = Path(__file__).parent

def verify(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    f = {int(s): c for s, c in data['witness'].items()}
    n = data['n']
    h = data['h']
    if type(n) is not int or type(h) is not int or (not 1 <= n <= 11) or (not 0 <= h <= n):
        raise ValueError('Invalid parameters')
    if any((type(c) is not int for c in f.values())):
        raise ValueError('Invalid color type')
    if set(data['witness']) != {str(a) for a in range(1 << n) if a.bit_count() <= h}:
        raise ValueError('Invalid subset domain')
    if not all((0 <= s < 2 ** n and 0 <= c < n for s, c in f.items())):
        raise ValueError(path)
    if not len(f) == sum((__import__('math').comb(n, i) for i in range(h + 1))):
        raise ValueError(path)
    checks = 0
    for t in combinations(range(n), h):
        y = sum((1 << i for i in t))
        s = y
        colors = set()
        while True:
            colors.add(f[s])
            if not s:
                break
            s = s - 1 & y
        if not colors == set(range(n)):
            raise ValueError((path, y, colors))
        checks += 1
    return {'file': path.name, 'n': n, 'h': h, 'h_sets_checked': checks, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
if __name__ == '__main__':
    results = []
    for p in sorted(HERE.glob('*_n*_h*.json')):
        if p.stat().st_size == 0:
            continue
        data = json.loads(p.read_text())
        if isinstance(data, dict) and 'witness' in data:
            results.append(verify(p))
    print(json.dumps(results, indent=2))
