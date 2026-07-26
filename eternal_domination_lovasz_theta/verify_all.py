#!/usr/bin/env python3
"""Run every exact verifier for the eternal-domination theta note."""

from __future__ import annotations

import json
from pathlib import Path

from verify_eternal import load_and_verify as verify_eternal
from verify_theta_certificate import load_and_verify as verify_theta


HERE = Path(__file__).resolve().parent


def main() -> None:
    theta = verify_theta()
    eternal = verify_eternal()
    graph_record = (HERE / "graph.g6").read_text(encoding="ascii").strip()
    if graph_record != theta["graph6"]:
        raise ValueError("graph.g6 does not match the theta certificate")
    if theta["graph6"] != eternal["graph6"]:
        raise ValueError("theta and eternal certificates use different graphs")
    if theta["order"] != eternal["order"] or theta["size"] != eternal["size"]:
        raise ValueError("theta and eternal graph metadata disagree")
    if eternal["gamma_infinity_one_guard"] != 3:
        raise ValueError("unexpected eternal domination number")
    if not theta["theta_strictly_greater_than_3"]:
        raise ValueError("theta certificate does not disprove the proposed bound")
    print(
        json.dumps(
            {
                "valid": True,
                "graph6": theta["graph6"],
                "order": theta["order"],
                "size": theta["size"],
                "gamma_infinity_one_guard": 3,
                "lovasz_theta_lower_bound": theta["objective"],
                "strict_counterexample": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
