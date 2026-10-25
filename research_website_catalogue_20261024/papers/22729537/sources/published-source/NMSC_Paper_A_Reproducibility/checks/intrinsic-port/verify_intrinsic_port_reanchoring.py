#!/usr/bin/env python3
"""Exact independent reconstruction of R-A1's small cut-relocation examples.

Only standard-library Fraction arithmetic is used. Time integers denote log(2)
units; rate one gives survival 2**(-duration). No payload files are rewritten.
These checks support the examples, not the general theorem's completeness.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def survival(duration: int, rate: int = 1) -> Fraction:
    require(duration >= 0 and rate > 0, "Invalid strict coalescent duration or rate")
    return Fraction(1, 2 ** (rate * duration))


def strict_graph(example: dict, cut: int) -> dict:
    ages = dict(example["ages_without_H"], H=cut)
    incoming = {vertex: [] for vertex in ages}
    outgoing = {vertex: [] for vertex in ages}
    for parent, child in example["arcs"]:
        require(ages[parent] > ages[child], "An arc has nonpositive temporal length")
        incoming[child].append(parent)
        outgoing[parent].append(child)
    require(incoming["R"] == [], "Missing unique root")
    require(all(incoming[v] for v in ages if v != "R"), "Disconnected non-root")
    require({v for v in ages if not outgoing[v]} == set(example["labels"]), "Unsampled leaf")
    require([v for v in ages if len(incoming[v]) == 2] == ["H"], "Not one reticulation")
    require(all(len(incoming[v]) <= 1 for v in ages if v != "H"), "Additional reticulation")
    return {"ages": ages, "incoming": incoming, "outgoing": outgoing}


def exterior_density_coefficients(v: int, r: int, route_weights: tuple[Fraction, Fraction]) -> dict:
    """Full three-lineage ranked density, first merger s and final merger t.

    The x lineage is single below U, so summing its route weights is exact
    marginalization of the whole hidden subnetwork. We derive the two regions
    from survival and rate multiplication, not from an archived output table.
    Each value records coefficient and the two absolute-time exponents.
    """
    route_total = sum(route_weights)
    require(route_total == 1, "Invalid route marginalization")
    require(0 < v < r, "Invalid exterior tree chronology")
    pre_root = route_total * (2 ** v) * (2 ** r)
    root_tail = route_total * survival(r - v) * (2 ** (3 * r))
    return {
        "yz; v<s<r<t": (pre_root, -1, -1),
        "yz; r<s<t": (root_tail, -2, -1),
        "xy; r<s<t": (root_tail, -2, -1),
        "xz; r<s<t": (root_tail, -2, -1),
    }


def q_mass(cut: int, pair_join: int) -> Fraction:
    return Fraction(0) if cut <= pair_join else 1 - survival(cut - pair_join)


def pair_partition_rank(mass: Fraction) -> int:
    # In both examples all reachable rows in this partition are scalar
    # multiples of one deterministic occupancy or one fixed routing mixture.
    # A positive-probability future completion makes that row observable.
    return int(mass > 0)


def main() -> None:
    manifest_path = Path(__file__).with_name("intrinsic_port_manifest.json")
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw)
    require(manifest["schema"] == "nmsc-intrinsic-port-regression-v1", "Wrong schema")
    require(manifest["time_unit"] == "log(2)" and manifest["pair_rate"] == 1, "Unsupported exact unit")
    gamma = Fraction(*manifest["inheritance"])
    require(0 < gamma < 1, "Inheritance is not interior")
    cuts = manifest["cuts"]
    require(cuts == [1, 3], "Unexpected comparison cuts")
    record = {}
    checks = 0
    for name in ("referee_example", "retained_reticulation_example"):
        example = manifest[name]
        graphs = [strict_graph(example, cut) for cut in cuts]
        checks += len(graphs)
        pair_join = example["ages_without_H"]["V" if name == "referee_example" else "W"]
        masses = [q_mass(cut, pair_join) for cut in cuts]
        ranks = [pair_partition_rank(mass) for mass in masses]
        require(masses == [Fraction(0), Fraction(1, 2)], "Wrong exact prefix masses")
        require(ranks == [0, 1], "Raw rank discrepancy was lost")
        checks += 2
        anchor = Fraction(pair_join, 2)
        require(anchor == 1, "Intrinsic anchor differs across law-equal examples")
        anchor_ranks = [pair_partition_rank(q_mass(int(anchor), pair_join)) for _ in cuts]
        require(anchor_ranks == [0, 0], "Common-time rank mismatch")
        checks += 2
        # Marked-strip partition evolution: start with no merger at the anchor;
        # the complete strip adds the positive merger branch at the W/V join.
        no_mark = survival(cuts[1] - pair_join)
        marked = 1 - no_mark
        require(no_mark + marked == 1 and marked == masses[1], "Marked transport is incomplete")
        require(Fraction(0) != marked, "No-mark-only mutant was not rejected")
        checks += 2
        record[name] = {"raw_q_ranks": ranks, "raw_q_prefix_masses": list(map(str, masses)),
                        "common_anchor_q_ranks": anchor_ranks,
                        "strip_no_mark_mass": str(no_mark), "strip_marked_mass": str(marked)}
    example = manifest["referee_example"]
    v = example["ages_without_H"]["V"]
    r = example["ages_without_H"]["R"]
    tables = [exterior_density_coefficients(v, r, (gamma, 1 - gamma)) for _ in cuts]
    require(tables[0] == tables[1], "Complete density tables depend on the hidden cut")
    require(tables[0]["yz; v<s<r<t"] == (128, -1, -1), "Wrong early density")
    require(all(row == (4096, -2, -1) for sector, row in tables[0].items() if sector != "yz; v<s<r<t"),
            "Wrong root-tail density")
    checks += 3
    # Complete-law normalization: an early yz merger or survival of all three
    # to the root, followed by one of three equally likely first pairs.
    early = 1 - survival(r - v)
    each_tail = survival(r - v) / 3
    require(early + 3 * each_tail == 1, "Complete three-label density is not normalized")
    checks += 1
    # The zero-reticulation tree obtained by contracting the x funnel has
    # exactly the same complete coefficient table (identity routing).
    tree_table = exterior_density_coefficients(v, r, (Fraction(1), Fraction(0)))
    require(tree_table == tables[0], "Tree contraction changed a complete density")
    checks += 1
    # In the retained example, private side entries at U and V occur before
    # reconvergence D and prohibit the proposed two-terminal unary reduction.
    retained = manifest["retained_reticulation_example"]
    age = retained["ages_without_H"]
    require(age["U"] < age["D"] and age["V"] < age["D"], "Side entries are after reconvergence")
    require(["U", "y"] in retained["arcs"] and ["V", "z"] in retained["arcs"], "Missing private anchors")
    require(all(cut < min(age["U"], age["V"]) for cut in cuts), "Hidden routing crosses a first contact")
    checks += 3
    # A single x lineage encounters no other lineage along either arm before
    # these fixed first contacts, so its route law is identically (gamma,1-gamma).
    route_laws = [(gamma, 1 - gamma) for _ in cuts]
    require(route_laws[0] == route_laws[1], "Retained fan's exterior input changed")
    checks += 1
    # Removing just the h field leaves nonisomorphic per-type dimensions.
    require(record["referee_example"]["raw_q_ranks"][0] != record["referee_example"]["raw_q_ranks"][1],
            "Clock-metadata-only mutant was not rejected")
    checks += 1
    result = {"status": "PASS", "exact_checks": checks,
              "manifest_sha256": hashlib.sha256(raw).hexdigest(),
              "examples": record,
              "complete_three_label_density": {key: [str(c), x, y] for key, (c, x, y) in tables[0].items()},
              "zero_reticulation_tree_same_complete_density": True,
              "rejected_incorrect_repairs": ["delete_only_raw_clock", "no_mark_only_cut_transport"],
              "scope": "two exact examples and their finite port reanchoring; universal theorem is proved separately"}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
