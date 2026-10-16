#!/usr/bin/env python3
"""Bounded exact diagnostics for even_strand_markov.tex; Python standard library.
The universal proof and imported Markov theorems are not computed here.
Run with Python 3.9+; no files, network, repository state or random state changed.
SPDX-License-Identifier: MIT
"""
from collections import Counter
from dataclasses import dataclass
from itertools import product, permutations
import json
import random

CHECKS = 0
COVER = Counter()


def require(ok, message):
    global CHECKS
    if not ok:
        raise ValueError(message)
    CHECKS += 1


def s(i, sign=1): return (("s", i, sign),)
def v(i): return (("v", i, 1),)
def inv(w): return tuple((t, i, -e if t == "s" else 1) for t, i, e in reversed(w))
def shift(w): return tuple((t, i + 1, e) for t, i, e in w)


@dataclass(frozen=True)
class State:
    strands: int
    word: tuple


def valid(x, virtual=True):
    return type(x.strands) is int and x.strands >= 1 and all(
        type(i) is int and 1 <= i < x.strands and
        ((t == "s" and type(e) is int and e in (-1, 1)) or
         (virtual and t == "v" and type(e) is int and e == 1))
        for t, i, e in x.word)


def pad(x):
    return x if x.strands % 2 == 0 else State(x.strands + 1, x.word + s(x.strands))


def components(x):
    p = list(range(x.strands))
    for _, i, _ in x.word:
        p[i - 1], p[i] = p[i], p[i - 1]
    seen = set(); out = []
    for i in range(x.strands):
        if i in seen: continue
        cycle = []
        while i not in seen:
            seen.add(i); cycle.append(i); i = p[i]
        out.append(tuple(cycle))
    return out


def even_scheme(kind, n, a, b, g=(), virtual=True):
    """Displayed patterns with syntactic applicability, not group membership."""
    limits = {"C": n-1, "BC": n-2, "T": n-2, "D": n-1,
              "R": n-2, "L": n-2, "BR": n-3, "BL": n-3}
    if kind not in limits or type(n) is not int or n < 2 or n % 2:
        raise ValueError("even tag/scheme")
    if kind in ("R", "L", "BR", "BL") and not virtual:
        raise ValueError("classical category cannot use exchanges")
    if kind in ("BR", "BL") and n < 4:
        raise ValueError("buffered minimum")
    if not valid(State(n, a+b), virtual) or any(i > limits[kind] for _, i, _ in a+b):
        raise ValueError("syntactic block support")
    if kind in ("T", "D"):
        at = n-1 if kind == "T" else n
        if g not in (s(at), s(at, -1)) + ((v(at),) if virtual else ()):
            raise ValueError("permitted terminal generator")
    if kind == "C": pair = (State(n,b), State(n,a+b+inv(a)))
    elif kind == "BC": pair = (State(n,b+s(n-1)), State(n,a+b+inv(a)+s(n-1)))
    elif kind == "T": pair = (State(n,b+s(n-1)), State(n,b+g))
    elif kind == "D": pair = (State(n,b), State(n+2,b+g+s(n+1)))
    elif kind == "R": pair = (State(n,a+s(n-1,-1)+b+s(n-1)), State(n,a+v(n-1)+b+v(n-1)))
    elif kind == "L": pair = (State(n,shift(a)+s(1,-1)+shift(b)+s(1)), State(n,shift(a)+v(1)+shift(b)+v(1)))
    elif kind == "BR": pair = (State(n,a+s(n-2,-1)+b+s(n-2)+s(n-1)), State(n,a+v(n-2)+b+v(n-2)+s(n-1)))
    else: pair = (State(n,shift(a)+s(1,-1)+shift(b)+s(1)+s(n-1)), State(n,shift(a)+v(1)+shift(b)+v(1)+s(n-1)))
    return pair


def unrestricted(kind, m, a, b, g):
    """Independent definition of an unrestricted Markov edge."""
    if kind == "conjugation": return State(m,b), State(m,a+b+inv(a))
    if kind == "stabilization": return State(m,b), State(m+1,b+g)
    if kind == "right_exchange": return State(m,a+s(m-1,-1)+b+s(m-1)), State(m,a+v(m-1)+b+v(m-1))
    if kind == "left_exchange": return State(m,shift(a)+s(1,-1)+shift(b)+s(1)), State(m,shift(a)+v(1)+shift(b)+v(1))
    raise ValueError(kind)


def relation_pairs(m, virtual):
    """Every defining relation family, with valid indices at fixed count m."""
    for i in range(1,m):
        yield s(i)+s(i,-1), (); yield s(i,-1)+s(i), ()
        if virtual: yield v(i)+v(i), ()
    for i in range(1,m-1):
        yield s(i)+s(i+1)+s(i), s(i+1)+s(i)+s(i+1)
        if virtual:
            yield v(i)+v(i+1)+v(i), v(i+1)+v(i)+v(i+1)
            yield s(i)+v(i+1)+v(i), v(i+1)+v(i)+s(i+1)
    for i in range(1,m):
        for j in range(i+2,m):
            yield s(i)+s(j), s(j)+s(i)
            if virtual:
                yield v(i)+v(j), v(j)+v(i)
                yield s(i)+v(j), v(j)+s(i)
                yield s(j)+v(i), v(i)+s(j)


def fox3(x):
    """Count closed Fox3 colorings exactly; positive generator passes left over right."""
    if not valid(x,False): raise ValueError("classical coloring domain")
    count = 0
    for top in product(range(3), repeat=x.strands):
        colors = list(top)
        for _, i, e in x.word:
            left,right = colors[i-1:i+1]
            colors[i-1:i+1] = ((2*left-right)%3,left) if e == 1 else (right,(2*right-left)%3)
        count += tuple(colors) == top
    return count


def ordered_crossings(x):
    """Signed ordered intercomponent counts; ignores virtual crossings."""
    cycles = components(x); membership = {i:c for c,cycle in enumerate(cycles) for i in cycle}
    matrix = [[0]*len(cycles) for _ in cycles]; labels = list(range(x.strands))
    for t,i,e in x.word:
        left,right = labels[i-1:i+1]
        if t == "s":
            over,under = (left,right) if e == 1 else (right,left)
            a,b = membership[over],membership[under]
            if a != b: matrix[a][b] += e
        labels[i-1],labels[i] = right,left
    return tuple(map(tuple,matrix))


def relabels(a,b):
    if len(a) != len(b): return False
    return any(all(a[i][j] == b[p[i]][p[j]] for i in range(len(a)) for j in range(len(a)))
               for p in permutations(range(len(a))))


def main():
    rng = random.Random(10600042)
    def block(k, virtual, length):
        if k < 1: return ()
        letters = [("s",i,e) for i in range(1,k+1) for e in (-1,1)]
        if virtual: letters += [("v",i,1) for i in range(1,k+1)]
        return tuple(rng.choice(letters) for _ in range(length))
    edges = relations = 0
    for virtual in (False,True):
        for m in range(1,10):
            for length in (0,1,2,5):
                ordinary = block(m-1,virtual,length)
                conjugator = block(m-1,virtual,5-length)
                jobs = [("conjugation",conjugator,ordinary,())]
                choices = (s(m),s(m,-1)) + ((v(m),) if virtual else ())
                jobs += [("stabilization",(),ordinary,g) for g in choices]
                if virtual and m >= 2:
                    a,b = block(m-2,True,length),block(m-2,True,5-length)
                    jobs += [(k,a,b,()) for k in ("right_exchange","left_exchange")]
                for kind,a,b,g in jobs:
                    old = unrestricted(kind,m,a,b,g); new = tuple(map(pad,old)); n = m+m%2
                    names = {"conjugation":("C","BC"),"stabilization":("D","T"),
                             "right_exchange":("R","BR"),"left_exchange":("L","BL")}
                    name = names[kind][m%2]
                    explicit = even_scheme(name,n,a,b,g,virtual)
                    require(all(valid(x,virtual) for x in old),"unrestricted indices")
                    require(new == explicit and new[::-1] == explicit[::-1],"both exact lifted endpoints")
                    require(all(valid(x,virtual) and x.strands%2 == 0 for x in new),"even valid tags")
                    require(len(components(old[0])) == len(components(old[1])),"edge component diagnostic")
                    require(all(len(components(x)) == len(components(pad(x))) for x in old),"padding components")
                    require(max(x.strands for x in new) == 2*((max(x.strands for x in old)+1)//2),"height conversion")
                    COVER[("virtual_" if virtual else "classical_")+name] += 1; edges += 1
            for lhs,rhs in relation_pairs(m,virtual):
                for left,right in ((lhs,rhs),(rhs,lhs),(inv(lhs),inv(rhs))):
                    before,after = block(m-1,virtual,2),block(m-1,virtual,2)
                    old = (State(m,before+left+after),State(m,before+right+after))
                    tail = s(m) if m%2 else (); n = m+m%2
                    require(tuple(map(pad,old)) == (State(n,before+left+after+tail),State(n,before+right+after+tail)),"whole relation context retained")
                    require(all(valid(pad(x),virtual) for x in old),"relation support")
                    require(len(components(old[0])) == len(components(old[1])),"relation component diagnostic")
                    relations += 1
    wanted = {"classical_"+x for x in ("C","BC","T","D")} | {"virtual_"+x for x in ("C","BC","T","D","R","L","BR","BL")}
    require(set(COVER) == wanted,"all four/eight families")
    require(pad(State(1,())) == State(2,s(1)),"one-strand boundary")
    require(len(components(State(2,()))) == 2 and len(components(State(4,()))) == 4,"tags retained")
    rejected = []
    for label,job in [("T_terminal_block",("T",2,(),s(1)+s(1),s(1,-1),False)),
                      ("R_terminal_blocks",("R",2,s(1),s(1),(),True)),
                      ("BR_tail_block",("BR",4,s(2),s(2),(),True)),
                      ("BL_too_small",("BL",2,(),(),(),True))]:
        try: even_scheme(*job)
        except ValueError: rejected.append(label)
        else: raise ValueError("unsafe support accepted "+label)
    require(fox3(State(2,s(1)*3)) == 9 and fox3(State(2,s(1))) == 3,"T Fox3 countercontrol")
    require(fox3(State(2,s(1))) == fox3(State(2,s(1,-1))) == 3,"legal T boundary")
    for x,y,z in product(range(3),repeat=3):
        op = lambda a,b: (2*b-a)%3
        require(op(x,x) == x and op(op(x,y),y) == x,"Fox RI/RII identities")
        require(op(op(x,y),z) == op(op(x,z),op(y,z)),"Fox RIII identity")
    first = ordered_crossings(State(2,s(1)*2)); second = ordered_crossings(State(2,s(1)+v(1)+s(1)+v(1)))
    require(first == ((0,1),(1,0)) and second == ((0,2),(0,0)) and not relabels(first,second),"ordered virtual R countercontrol")
    buffered = (State(4,s(2)*2+s(3)),State(4,s(2)+v(2)+s(2)+v(2)+s(3)))
    require(len(components(buffered[0])) == len(components(buffered[1])) == 3 and not relabels(*map(ordered_crossings,buffered)),"ordered BR countercontrol")
    require(len(components(State(1,()))) != len(components(State(2,()))),"idle-strand padding is false")
    print(json.dumps({"status":"PASS_BOUNDED_DIAGNOSTICS","checks":CHECKS,"edge_cases":edges,
        "relation_context_cases":relations,"scheme_coverage":dict(sorted(COVER.items())),
        "support_mutants_rejected":rejected,"Fox3_counts":{"sigma1_cubed":9,"sigma1":3},
        "ordered_R_matrices":[first,second],"limits":["Finite diagnostics supplement a universal written proof",
        "No link-equivalence oracle or braid word-problem solver","Imported Markov theorems not reproved",
        "No formal certification, novelty or publication assertion"]},sort_keys=True,indent=2))


if __name__ == "__main__": main()
