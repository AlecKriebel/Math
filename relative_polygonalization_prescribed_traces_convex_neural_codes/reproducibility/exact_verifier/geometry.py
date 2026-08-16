from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from typing import Iterable

Point = tuple[F, F]
Ineq = tuple[tuple[F, ...], F, bool]  # a dot x <= rhs; strict means <


def frac(x) -> F:
    return x if isinstance(x, F) else F(str(x))


def point(p) -> Point:
    return frac(p[0]), frac(p[1])


def signed_area2(poly: list[Point]) -> F:
    return sum(x1*y2-x2*y1 for (x1,y1),(x2,y2) in zip(poly, poly[1:]+poly[:1]))


def ccw(poly_raw) -> list[Point]:
    p=[point(q) for q in poly_raw]
    if signed_area2(p)<0:
        p.reverse()
    if signed_area2(p)<=0:
        raise ValueError('polygon must have positive area')
    return p


def polygon_inequalities(poly_raw, strict: bool) -> list[Ineq]:
    p=ccw(poly_raw)
    out=[]
    for (x1,y1),(x2,y2) in zip(p,p[1:]+p[:1]):
        dx,dy=x2-x1,y2-y1
        # CCW interior: dx(y-y1)-dy(x-x1)>0
        # equivalent to dy*x-dx*y < dy*x1-dx*y1.
        out.append(((dy,-dx),dy*x1-dx*y1,strict))
    return out


def fm_feasible(ineqs: Iterable[Ineq], nvars: int) -> bool:
    work=[(tuple(map(F,a)),F(rhs),bool(st)) for a,rhs,st in ineqs]
    for k in range(nvars-1,-1,-1):
        pos=[]; neg=[]; zero=[]
        for a,rhs,st in work:
            c=a[k]
            rest=a[:k]+a[k+1:]
            if c>0: pos.append((c,rest,rhs,st))
            elif c<0: neg.append((c,rest,rhs,st))
            else: zero.append((rest,rhs,st))
        new=list(zero)
        for cp,ap,rp,sp in pos:
            for cn,an,rn,sn in neg:
                # (-cn)*(cp*x+ap<=rp)+cp*(cn*x+an<=rn)
                aa=tuple((-cn)*u+cp*v for u,v in zip(ap,an))
                rr=(-cn)*rp+cp*rn
                new.append((aa,rr,sp or sn))
        work=new
    for a,rhs,st in work:
        assert len(a)==0
        if st:
            if not F(0)<rhs: return False
        else:
            if not F(0)<=rhs: return False
    return True


def atom_feasible(ambient, neurons: dict[str,list], active: frozenset[str]) -> bool:
    base=polygon_inequalities(ambient,True)
    for i in active:
        base.extend(polygon_inequalities(neurons[i],True))
    inactive=[i for i in neurons if i not in active]
    if not inactive:
        return fm_feasible(base,2)
    violation_lists=[]
    for i in inactive:
        opts=[]
        for a,rhs,_ in polygon_inequalities(neurons[i],True):
            opts.append((tuple(-x for x in a),-rhs,False))
        violation_lists.append(opts)
    for choice in product(*violation_lists):
        if fm_feasible(base+list(choice),2):
            return True
    return False


def complete_code(ambient, neurons: dict[str,list]) -> set[str]:
    keys=sorted(neurons)
    code=set()
    for mask in range(1<<len(keys)):
        active=frozenset(keys[j] for j in range(len(keys)) if mask>>j&1)
        if atom_feasible(ambient,neurons,active):
            code.add(''.join(sorted(active)))
    return code


def point_in_open(poly_raw,p_raw) -> bool:
    p=point(p_raw)
    return all(sum(a[j]*p[j] for j in range(2))<rhs
               for a,rhs,_ in polygon_inequalities(poly_raw,True))


def line_interval(polys: list[tuple[list,bool]], p_raw, d_raw):
    p=point(p_raw); d=point(d_raw)
    lower=None; upper=None; lower_closed=True; upper_closed=True
    for poly,strict in polys:
        for a,rhs,_ in polygon_inequalities(poly,strict):
            A=sum(a[j]*d[j] for j in range(2))
            C=rhs-sum(a[j]*p[j] for j in range(2))
            if A==0:
                if (strict and not F(0)<C) or ((not strict) and not F(0)<=C):
                    return None
                continue
            v=C/A
            closed=not strict
            if A>0:
                if upper is None or v<upper:
                    upper=v; upper_closed=closed
                elif v==upper:
                    upper_closed=upper_closed and closed
            else:
                if lower is None or v>lower:
                    lower=v; lower_closed=closed
                elif v==lower:
                    lower_closed=lower_closed and closed
    if lower is not None and upper is not None:
        if lower>upper: return None
        if lower==upper and not (lower_closed and upper_closed): return None
    return lower,upper,lower_closed,upper_closed


def interval_as_json(I):
    if I is None: return None
    lo,hi,lc,uc=I
    return [str(lo),str(hi),lc,uc]
