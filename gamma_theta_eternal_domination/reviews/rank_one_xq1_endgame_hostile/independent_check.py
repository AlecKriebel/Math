#!/usr/bin/env python3
"""Clean-room ordinary-set audit of the rank-one XQ1 implication.

This checker does not import candidate code or campaign evaluators.  It
reconstructs the named incidence table from the theorem hypotheses and the
accepted C-150 ladder, verifies both C-064 applications at targets outside
the paired ridge states, and exhausts every named or external completion
pattern relevant to the final C-108/one-guard contradiction.

It is a bookkeeping audit of the symbolic proof.  It does not independently
prove the accepted C-064, C-108, or C-150 dependencies.
"""

from __future__ import annotations

import hashlib
import itertools
import json


VERTICES = ("u", "x", "p", "q", "r", "y", "z")


def pair(a: str, b: str) -> frozenset[str]:
    assert a != b
    return frozenset((a, b))


def state(*vertices: str) -> frozenset[str]:
    assert len(vertices) == len(set(vertices))
    return frozenset(vertices)


def swap_object(
    obj: frozenset[str], a: str, b: str
) -> frozenset[str]:
    def image(v: str) -> str:
        if v == a:
            return b
        if v == b:
            return a
        return v

    return frozenset(image(v) for v in obj)


def main() -> None:
    # Primitive named incidences, grouped by their mathematical sources.
    edge_sources = {
        "active_edge": (("u", "x"),),
        "XQ1_row": (("u", "r"), ("x", "r"), ("p", "r")),
        "private_y": (("p", "y"),),
        "private_z": (("u", "z"),),
        "C150_ladder": (("x", "y"), ("x", "z"), ("y", "z")),
    }
    nonedge_sources = {
        "T_independent": (("x", "p"), ("x", "q"), ("p", "q")),
        "XQ1_row": (("q", "r"),),
        "private_y": (("u", "y"), ("r", "y"), ("q", "y")),
        "private_z": (("r", "z"), ("p", "z"), ("q", "z")),
    }

    edges = {
        pair(a, b)
        for incidences in edge_sources.values()
        for a, b in incidences
    }
    nonedges = {
        pair(a, b)
        for incidences in nonedge_sources.values()
        for a, b in incidences
    }
    assert not edges & nonedges

    all_pairs = {
        pair(a, b) for a, b in itertools.combinations(VERTICES, 2)
    }
    optional = all_pairs - edges - nonedges
    assert optional == {pair("u", "p"), pair("u", "q")}
    assert (len(edges), len(nonedges), len(optional)) == (9, 10, 2)

    # The accepted independent ladder and the two C-064 applications.
    jy = state("y", "r", "q")
    jz = state("z", "r", "q")
    kz = state("z", "p", "q")
    t = state("x", "p", "q")
    for facet in (jy, jz, kz, t):
        assert all(
            pair(a, b) in nonedges
            for a, b in itertools.combinations(facet, 2)
        )

    assert swap_object(jz, "r", "p") == kz
    assert swap_object(kz, "z", "x") == t

    attack = "y"
    response = state("z")
    covariance = []
    for before, after, exchanged in (
        (jz, kz, ("r", "p")),
        (kz, t, ("z", "x")),
    ):
        assert attack not in before | after
        assert attack not in exchanged
        assert swap_object(before, *exchanged) == after
        next_attack = next(iter(swap_object(state(attack), *exchanged)))
        next_response = swap_object(response, *exchanged)
        covariance.append(
            {
                "before": sorted(before),
                "after": sorted(after),
                "exchanged": list(exchanged),
                "attack_before": attack,
                "attack_after": next_attack,
                "list_before": sorted(response),
                "list_after": sorted(next_response),
                "target_outside_both": True,
            }
        )
        attack = next_attack
        response = next_response

    # At J_z only z is physically adjacent to y, and its successor is J_y.
    eligible_at_jz = {
        guard for guard in jz if pair(guard, "y") in edges
    }
    assert eligible_at_jz == {"z"}
    assert jz - {"z"} | {"y"} == jy
    assert attack == "y" and response == {"x"}

    retained_x_successor = t - {"x"} | {"y"}
    omitted_p_successor = t - {"p"} | {"y"}
    assert retained_x_successor == state("y", "p", "q")
    assert omitted_p_successor == state("x", "y", "q")
    omitted = omitted_p_successor

    # Enumerate the two optional named edges.  A third member of a maximal
    # independent set extending {u,y} can collide with a named vertex only
    # when it is nonadjacent to both u and y.
    optional_order = (pair("u", "p"), pair("u", "q"))
    named_rows = []
    for mask in range(4):
        chosen = {
            optional_order[i] for i in range(2) if mask & (1 << i)
        }

        def named_adjacent(a: str, b: str) -> bool:
            ab = pair(a, b)
            if ab in edges:
                return True
            if ab in nonedges:
                return False
            assert ab in optional
            return ab in chosen

        named_completions = [
            v
            for v in VERTICES
            if v not in {"u", "y"}
            and not named_adjacent("u", v)
            and not named_adjacent("y", v)
        ]
        expected = [] if pair("u", "q") in chosen else ["q"]
        assert named_completions == expected

        if named_completions:
            i_state = state("u", "y", "q")
            assert all(
                not named_adjacent(a, b)
                for a, b in itertools.combinations(i_state, 2)
            )
            active_successor = i_state - {"u"} | {"x"}
            assert active_successor == omitted

        named_rows.append(
            {
                "optional_mask": mask,
                "optional_edges": sorted(
                    sorted(ab) for ab in chosen
                ),
                "named_completion_candidates": named_completions,
                "s_equals_q_immediately_forces_omitted_state": bool(
                    named_completions
                ),
            }
        )

    # For an external completion s, independence fixes su=sy=0.  Exhaust
    # every remaining adjacency from s to the named vertices.  Once the
    # retained active successor {x,y,s} dominates unoccupied q, sq is forced;
    # xq=yq=0 then make s the unique legal one-guard responder.
    external_variable_neighbors = ("x", "p", "q", "r", "z")
    external_cases = 0
    domination_compatible_cases = 0
    unique_response_cases = 0
    for optional_mask in range(4):
        # Optional named edges do not affect the external argument, but
        # include all four named incidence completions in the exhaustion.
        for s_mask in range(1 << len(external_variable_neighbors)):
            external_cases += 1
            s_neighbors = {
                v
                for i, v in enumerate(external_variable_neighbors)
                if s_mask & (1 << i)
            }
            # q is unoccupied in P={x,y,s}.  Because q misses x and y,
            # domination of q is equivalent to sq.
            p_state = state("x", "y", "s")
            assert "q" not in p_state
            dominates_q = "q" in s_neighbors
            if not dominates_q:
                continue
            domination_compatible_cases += 1

            eligible = set()
            if pair("x", "q") in edges:
                eligible.add("x")
            if pair("y", "q") in edges:
                eligible.add("y")
            if "q" in s_neighbors:
                eligible.add("s")
            assert eligible == {"s"}
            successor = p_state - {"s"} | {"q"}
            assert successor == omitted
            unique_response_cases += 1

    assert external_cases == 128
    assert domination_compatible_cases == 64
    assert unique_response_cases == 64

    result = {
        "schema": "rank-one-XQ1-hostile-clean-room-v1",
        "verdict": "PASS",
        "frozen_candidate_note_sha256": (
            "ddb77704f2edad1cec7ff95629b34b56ed4182d211fc26089f69bc2a9b7bbf06"
        ),
        "pair_partition": {
            "edges": sorted(sorted(ab) for ab in edges),
            "nonedges": sorted(sorted(ab) for ab in nonedges),
            "optional": sorted(sorted(ab) for ab in optional),
            "counts": [len(edges), len(nonedges), len(optional)],
        },
        "physical_start_list": {
            "state": sorted(jz),
            "attack": "y",
            "eligible": sorted(eligible_at_jz),
            "successor": sorted(jy),
        },
        "covariance": covariance,
        "transported_list_at_T_for_y": sorted(response),
        "retained_x_successor": sorted(retained_x_successor),
        "omitted_p_successor": sorted(omitted),
        "named_completion_rows": named_rows,
        "external_completion_exhaustion": {
            "all_local_edge_patterns": external_cases,
            "patterns_where_retained_successor_dominates_q": (
                domination_compatible_cases
            ),
            "patterns_with_unique_s_to_q_response_forcing_omitted_state": (
                unique_response_cases
            ),
        },
        "scope": (
            "Clean-room ordinary-set audit; accepted C-064, C-108, and "
            "C-150 remain proof dependencies."
        ),
    }
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    result["sha256_without_this_field"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
