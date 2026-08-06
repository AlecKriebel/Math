#!/usr/bin/env python3
"""Exact Bellman difference certificates for finite reward automata."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Iterable, Sequence

try:
    from .reward_cycle import RewardEdge
except ImportError:  # direct script execution
    from reward_cycle import RewardEdge

Vertex=Hashable


@dataclass(frozen=True, slots=True)
class BellmanCertificate:
    potential: tuple[tuple[Vertex, Fraction], ...]
    epsilon: Fraction


def solve_nonpositive_cycle_bellman(
    vertices: Iterable[Vertex], edges: Sequence[RewardEdge], strict_vertices: Iterable[Vertex]=()
) -> BellmanCertificate:
    """Construct h with r+h(t)-h(s)<=-eps on selected sources, <=0 elsewhere.

    This elementary exact solver uses rational linear programming through
    SymPy.  Feasibility requires that no directed cycle have positive reward;
    strict feasibility additionally requires every directed cycle meeting a
    selected source to have negative total reward.
    """
    import sympy as sp
    vertices=tuple(vertices); strict=set(strict_vertices)
    hvars=sp.symbols(f"h0:{len(vertices)}")
    eps=sp.symbols("eps")
    idx={v:i for i,v in enumerate(vertices)}
    cons=[eps >= 0, eps <= 1, sp.Eq(hvars[0], 0)]
    for e in edges:
        rhs=-eps if e.source in strict else 0
        cons.append(sp.Integer(e.reward)+hvars[idx[e.target]]-hvars[idx[e.source]] <= rhs)
    if not strict:
        cons.append(sp.Eq(eps, 0))
    try:
        val,sol=sp.solvers.simplex.lpmax(eps,cons)
    except Exception as exc:
        raise ValueError("Bellman inequalities are infeasible") from exc
    qeps=Fraction(int(val.p),int(val.q))
    h=[]
    for v,var in zip(vertices,hvars):
        q=sp.Rational(sol[var]);h.append((v,Fraction(int(q.p),int(q.q))))
    cert=BellmanCertificate(tuple(h),qeps)
    verify_bellman(edges,cert,strict)
    return cert


def verify_bellman(edges: Sequence[RewardEdge], cert: BellmanCertificate, strict_vertices: Iterable[Vertex]=()) -> None:
    h=dict(cert.potential);strict=set(strict_vertices)
    for e in edges:
        lhs=Fraction(e.reward)+h[e.target]-h[e.source]
        rhs=-cert.epsilon if e.source in strict else Fraction(0)
        if lhs>rhs: raise AssertionError("Bellman inequality failed")


def self_test() -> None:
    vs=(0,1)
    es=(RewardEdge(0,1,0),RewardEdge(1,0,-1))
    c=solve_nonpositive_cycle_bellman(vs,es)
    assert c.epsilon>=0


if __name__=="__main__":
    self_test();print("bellman_certificate.py self-test: OK")
