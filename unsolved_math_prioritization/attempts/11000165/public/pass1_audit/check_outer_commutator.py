"""Exact free reduction: independent word certificate, no numeric approximation."""
import json

def red(w):
    r = []
    for a in w:
        if r and r[-1] == -a:
            r.pop()
        else:
            r.append(a)
    return tuple(r)

def inv(w):
    return tuple((-a for a in reversed(w)))

def subst(w, aut):
    out = ()
    for a in w:
        v = aut[abs(a)]
        out = red(out + (v if a > 0 else inv(v)))
    return out

def comp(f, g):
    return {i: subst(g[i], f) for i in f}

def partial(g, j, sgn=1):
    out = {i: (i,) for i in range(1, g + 1)}
    out[1] = (sgn * j, 1, -sgn * j)
    return out

def power(f, n):
    out = {i: (i,) for i in f}
    for _ in range(n):
        out = comp(out, f)
    return out
rows = []
for g in (3, 4, 8):
    a = partial(g, 2)
    ai = partial(g, 2, -1)
    b = partial(g, 3)
    bi = partial(g, 3, -1)
    ident = {i: (i,) for i in a}
    if not comp(a, ai) == ident == comp(ai, a):
        raise RuntimeError('Exact supplementary check failed')
    if not comp(b, bi) == ident == comp(bi, b):
        raise RuntimeError('Exact supplementary check failed')
    k = comp(comp(comp(a, b), ai), bi)
    w = (-3, -2, 3, 2)
    expected = red(w + (1,) + inv(w))
    if not k[1] == expected:
        raise RuntimeError('Exact supplementary check failed')
    if not all((k[i] == (i,) for i in range(2, g + 1))):
        raise RuntimeError('Exact supplementary check failed')
    for n in range(1, 20):
        wn = red(w * n)
        if not len(wn) == 4 * n:
            raise RuntimeError('Exact supplementary check failed')
        kn = power(k, n)
        if not kn[1] == red(wn + (1,) + inv(wn)):
            raise RuntimeError('Exact supplementary check failed')
        if not len(kn[1]) == 8 * n + 1:
            raise RuntimeError('Exact supplementary check failed')
        if not all((kn[i] == (i,) for i in range(2, g + 1))):
            raise RuntimeError('Exact supplementary check failed')
    rows.append({'rank': g, 'commutator_images': k, 'conjugating_word': w, 'power_checks': 19})
print(json.dumps({'composition_convention': 'f*g = f after g; [f,g]=f*g*f^-1*g^-1', 'status': 'PASS', 'rows': rows, 'mathematical_certificate': 'w=x3^-1 x2^-1 x3 x2 is cyclically reduced. Every positive power fixes x2,x3 and is nonidentity on x1. An inner automorphism fixing x2,x3 has conjugator in <x2> intersect <x3> = 1. Thus every nonzero power is noninner for all rank g>=3.'}, indent=2))
