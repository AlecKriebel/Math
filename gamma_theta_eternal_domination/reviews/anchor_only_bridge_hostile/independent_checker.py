#!/usr/bin/env python3
"""Clean-room symbolic audit of the anchor-only bridge argument.

This checker does not read or import the candidate.  It exhausts the finite
response-list cases used in the proof and separately checks the named-vertex
collision and frozen-component bookkeeping.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


U, V, W = 1, 2, 4
ANCHORS = U | V | W
NONEMPTY_PROPER = tuple(m for m in range(1, 8) if m != ANCHORS)


def covers(missing: int, outside_lists: tuple[int, ...]) -> bool:
    union = 0
    for mask in outside_lists:
        union |= mask
    return missing & ~union == 0


def main() -> None:
    # Exact odd-terminal lists.
    ls, lt = V, U

    # From D_s={u,w,s}, attack t.  The two alternative successors violate
    # arbitrary-state restoration, while the u->t successor is not excluded.
    successor_audit = {
        "w_to_t_state_u_s_t": covers(V | W, (ls, lt)),
        "s_to_t_state_u_w_t": covers(V, (lt,)),
        "u_to_t_state_w_s_t": covers(U | V, (ls, lt)),
    }
    assert successor_audit == {
        "w_to_t_state_u_s_t": False,
        "s_to_t_state_u_w_t": False,
        "u_to_t_state_w_s_t": True,
    }

    # At a bridge vertex z, restoration of {s,t,z} forces w into L(z).
    restoration_survivors = tuple(
        mask for mask in NONEMPTY_PROPER if covers(ANCHORS, (ls, lt, mask))
    )
    assert restoration_survivors == (W, U | W, V | W)

    # These are exactly the three nonempty proper lists containing w.
    all_proper_w_lists = tuple(mask for mask in NONEMPTY_PROPER if mask & W)
    assert restoration_survivors == all_proper_w_lists

    # Collision audit.  Under the hypotheses:
    #   ut, vs, ws, wt are G-edges;
    #   z in W means sz and tz are H-edges.
    # Hence no anchor can play z.  Open H-neighborhoods also exclude s,t.
    named = ("u", "v", "w", "s", "t", "fresh")
    g_edges = {
        frozenset(("u", "t")),
        frozenset(("v", "s")),
        frozenset(("w", "s")),
        frozenset(("w", "t")),
    }

    def may_be_bridge(name: str) -> bool:
        if name in ("s", "t"):
            return False  # no loops in either open neighborhood
        return (
            frozenset((name, "s")) not in g_edges
            and frozenset((name, "t")) not in g_edges
        )

    collision_candidates = tuple(name for name in named if may_be_bridge(name))
    assert collision_candidates == ("fresh",)

    # Component bookkeeping.  A vertex lies in the outside part of the
    # frozen-u projection iff u is absent from its list, and similarly for v.
    component_membership = {}
    for mask in restoration_survivors:
        in_k_vertex_set = not (mask & U)
        in_m_vertex_set = not (mask & V)
        # The complement edges sz and tz then put z into the corresponding
        # components whenever it belongs to that projection's vertex set.
        component_membership[str(mask)] = {
            "in_K": in_k_vertex_set,
            "in_M": in_m_vertex_set,
        }
    assert component_membership == {
        str(W): {"in_K": True, "in_M": True},
        str(U | W): {"in_K": False, "in_M": True},
        str(V | W): {"in_K": True, "in_M": False},
    }

    result = {
        "schema": "anchor-only-bridge-hostile-symbolic-v1",
        "model": (
            "unoccupied attacks only; one adjacent guard moves; every retained "
            "state dominates"
        ),
        "checks": {
            "forced_u_to_t_by_restoration": successor_audit,
            "bridge_list_masks": restoration_survivors,
            "named_collision_candidates": collision_candidates,
            "component_membership": component_membership,
            "bridge_G_clique_reason": (
                "a retained {s,t,z} must dominate distinct z'; sz' and tz' "
                "are H-edges, so zz' is a G-edge and is the unique move edge"
            ),
            "wz_reason": (
                "if wz were an H-edge, z would lie in Z_s={u}; the collision "
                "audit excludes z=u"
            ),
        },
        "verdict": "PASS_SYMBOLIC",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out = Path(__file__).with_name("independent_result.json")
    out.write_text(payload, encoding="utf-8")
    print(payload, end="")
    print("result_sha256", hashlib.sha256(payload.encode()).hexdigest())


if __name__ == "__main__":
    main()
