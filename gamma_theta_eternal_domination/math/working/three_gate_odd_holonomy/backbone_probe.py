#!/usr/bin/env python3
"""Compute SAT backbones of a small boundary-cycle discovery formula."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile


def load_probe(path: Path):
    spec = importlib.util.spec_from_file_location("boundary_probe", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def solve(solver: Path, dimacs: str, literal: int) -> str:
    lines = dimacs.splitlines()
    header = lines[0].split()
    header[3] = str(int(header[3]) + 1)
    trial = "\n".join((" ".join(header), *lines[1:], f"{literal} 0", ""))
    with tempfile.NamedTemporaryFile(suffix=".cnf") as handle:
        Path(handle.name).write_text(trial, encoding="ascii")
        run = subprocess.run(
            [str(solver), "--quiet", handle.name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    return "SAT" if run.returncode == 10 else "UNSAT" if run.returncode == 20 else "ERROR"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    probe = load_probe(Path(__file__).with_name("probe_boundary_cycle.py"))
    cnf, metadata = probe.build(
        (0, 1, 2),
        (1, 1, 1),
        enforce_gamma=False,
        spare_vertices=0,
    )
    dimacs = cnf.dimacs()
    family = metadata["family"]
    edge = metadata["edge"]
    assert isinstance(family, dict)
    assert isinstance(edge, dict)

    forced_family_true: list[list[int]] = []
    forced_family_false: list[list[int]] = []
    forced_h: list[list[int]] = []
    forced_g: list[list[int]] = []
    for state, variable in family.items():
        if solve(args.solver, dimacs, -variable) == "UNSAT":
            forced_family_true.append(list(state))
        elif solve(args.solver, dimacs, variable) == "UNSAT":
            forced_family_false.append(list(state))
    for uv, variable in edge.items():
        if solve(args.solver, dimacs, -variable) == "UNSAT":
            forced_h.append(list(uv))
        elif solve(args.solver, dimacs, variable) == "UNSAT":
            forced_g.append(list(uv))

    result = {
        "formula": {
            "variables": len(cnf.names) - 1,
            "clauses": len(cnf.clauses),
        },
        "forced_family_true": forced_family_true,
        "forced_family_false": forced_family_false,
        "forced_h": forced_h,
        "forced_g": forced_g,
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "forced family true/false "
        f"{len(forced_family_true)}/{len(forced_family_false)}; "
        f"forced H/G {len(forced_h)}/{len(forced_g)}"
    )


if __name__ == "__main__":
    main()
