"""Exact support routines; no floating-point geometry."""
from exact_geometry import F, pt, cross, sub, inside


def hull(points):
    points = sorted(set(points))
    def chain(seq):
        out = []
        for p in seq:
            while len(out) > 1 and cross(sub(out[-1], out[-2]), sub(p, out[-1])) <= 0:
                out.pop()
            out.append(p)
        return out
    return chain(points)[:-1] + chain(points[::-1])[:-1]


def section(poly, y):
    xs = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        if a[1] == b[1]:
            if y == a[1]:
                xs.extend((a[0], b[0]))
        elif min(a[1], b[1]) <= y <= max(a[1], b[1]):
            xs.append(a[0] + (y-a[1]) * (b[0]-a[0]) / (b[1]-a[1]))
    return (min(xs), max(xs)) if xs else None


def longest_horizontal(poly):
    # Section endpoints are piecewise affine with breakpoints at vertex heights.
    # Thus the piecewise affine chord length attains its maximum at one of them.
    return max((section(poly, y)[1]-section(poly, y)[0], y, section(poly, y)[0])
               for y in {p[1] for p in poly})


def difference(poly):
    return hull([sub(a, b) for a in poly for b in poly])


def rows(points):
    out = {}
    for x, y in points:
        out.setdefault(y, []).append(x)
    return out


def row_span(values):
    return max(values)-min(values)


def row_piercing(poly, first, second):
    reflected = hull([(-x, -y) for x, y in poly])
    ell, v, u = longest_horizontal(reflected)
    selected = 0 if all(row_span(xs) <= ell for xs in rows(first).values()) else 1
    points = (first, second)[selected]
    rr = rows(points)
    assert all(row_span(xs) <= ell for xs in rr.values())
    piercing = [(min(xs)-u, y-v) for y, xs in rr.items()]
    return selected, piercing


def row_system_piercing(poly, first, second):
    """At most two points when each input has row separation >= height(poly)."""
    H = max(y for x,y in poly)-min(y for x,y in poly)
    for points in (first, second):
        ys = sorted(rows(points))
        assert all(b-a >= H for a,b in zip(ys, ys[1:]))
    reflected = hull([(-x,-y) for x,y in poly])
    ell, v, u = longest_horizontal(reflected)
    for i, points in enumerate((first, second)):
        rr = rows(points)
        if len(rr) == 1:
            y, xs = next(iter(rr.items()))
            assert row_span(xs) <= 2*ell
            return i, [(min(xs)-u, y-v), (min(xs)+ell-u, y-v)]
    assert len(rows(first)) <= 2 and len(rows(second)) <= 2
    return row_piercing(poly, first, second)
