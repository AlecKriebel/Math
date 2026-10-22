"""Standard-library independent verifier for K_{p/q} graph homomorphisms."""
import json
import sys


def verify(data):
    p, q = data['p'], data['q']
    assert type(p) is int and type(q) is int and q > 0 and p >= 2*q
    vertices = data['vertices']
    assert len(vertices) == len(set(vertices))
    colors = data['colors']
    assert set(colors) == {str(v) for v in vertices}
    assert all(type(c) is int and 0 <= c < p for c in colors.values())
    vs, seen = set(vertices), set()
    for u, v in data['edges']:
        assert u in vs and v in vs and u != v
        edge = frozenset((u, v))
        assert edge not in seen
        seen.add(edge)
        delta = (colors[str(u)] - colors[str(v)]) % p
        assert q <= delta <= p-q, (u, v, delta)
    return {'verified': True, 'vertices': len(vertices), 'edges': len(seen), 'p': p, 'q': q}


if __name__ == '__main__':
    for path in sys.argv[1:]:
        with open(path) as f:
            data = json.load(f)
        print(path, json.dumps(verify(data), sort_keys=True))
