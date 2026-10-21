"""Exact exhaustive graph recurrence; no floating point solver used."""
import functools, json
from pathlib import Path

def solve(n, t):
    adj = [0] * n
    for d in range(t, n):
        for a in range(d, n - d + 1, d):
            b = a + d
            adj[a - 1] |= 1 << b - 1
            adj[b - 1] |= 1 << a - 1

    @functools.lru_cache(None)
    def rec(s):
        if not s:
            return (0, 0)
        start = s & -s
        comp = start
        front = start
        while front:
            p = front & -front
            front -= p
            new = adj[p.bit_length() - 1] & s & ~comp
            comp |= new
            front |= new
        if comp != s:
            a, x = rec(comp)
            b, y = rec(s ^ comp)
            return (a + b, x | y)
        v = max((i for i in range(n) if s >> i & 1), key=lambda i: (adj[i] & s).bit_count())
        p = 1 << v
        a, x = rec(s ^ p)
        b, y = rec(s & ~(p | adj[v]))
        b += 1
        return (b, y | p) if b > a else (a, x)
    size, bits = rec((1 << n) - 1)
    A = [i + 1 for i in range(n) if bits >> i & 1]
    if not all((b - a < t or b % (b - a) for j, a in enumerate(A) for b in A[j + 1:])):
        raise RuntimeError('verification guard failed')
    return {'N': n, 't': t, 'maximum': size, 'witness': A, 'recurrence_states': rec.cache_info().currsize}
if __name__ == '__main__':
    results = [solve(n, t) for t in range(1, 7) for n in range(1, 51)]
    out = Path(__file__).with_name('exact_results.json')
    out.write_text(json.dumps(results, indent=2) + '\n')
    for t in range(1, 7):
        r = [x for x in results if x['t'] == t]
        print('t', t, [(x['N'], x['maximum']) for x in r if x['N'] % 5 == 0])
    print('t2 first construction mismatch:')
    for r in results:
        if r['t'] != 2:
            continue
        n = r['N']
        L = n.bit_length() - 1
        lower = (n + 1) // 2 + (L + 1) // 2
        if r['maximum'] != lower:
            print(r, 'lower', lower)
            break
