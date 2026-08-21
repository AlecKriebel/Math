#!/usr/bin/env python3
"""Classify one external common neighbor of a cyclic special pair."""

from __future__ import annotations

import argparse
import importlib.util
from itertools import product
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    args = parser.parse_args()

    probe = load_probe(Path(__file__).with_name("probe_boundary_cycle.py"))
    cnf, metadata = probe.build(
        (0, 1, 2),
        (1, 1, 1),
        enforce_gamma=False,
        spare_vertices=1,
    )
    edge = metadata["edge"]
    family = metadata["family"]
    assert isinstance(edge, dict)
    assert isinstance(family, dict)
    q = 12
    base_units = [edge[probe.pair(4, q)], edge[probe.pair(6, q)]]
    direct = [
        family[tuple(sorted(({0, 1, 2} - {omitted}) | {q}))]
        for omitted in range(3)
    ]
    dimacs = cnf.dimacs().splitlines()
    rows = []
    with tempfile.TemporaryDirectory() as directory:
        instance = Path(directory) / "trial.cnf"
        for anchor_h, cap_h, list_bits in product(
            (False, True),
            (False, True),
            product((False, True), repeat=3),
        ):
            units = list(base_units)
            units.append(
                edge[probe.pair(0, q)]
                if anchor_h
                else -edge[probe.pair(0, q)]
            )
            units.append(
                edge[probe.pair(11, q)]
                if cap_h
                else -edge[probe.pair(11, q)]
            )
            units.extend(
                variable if bit else -variable
                for variable, bit in zip(direct, list_bits, strict=True)
            )
            header = dimacs[0].split()
            header[3] = str(int(header[3]) + len(units))
            instance.write_text(
                "\n".join(
                    (
                        " ".join(header),
                        *dimacs[1:],
                        *(f"{literal} 0" for literal in units),
                        "",
                    )
                ),
                encoding="ascii",
            )
            run = subprocess.run(
                [str(args.solver), "--quiet", str(instance)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            if run.returncode == 10:
                rows.append(
                    {
                        "anchor_h": anchor_h,
                        "cap_h": cap_h,
                        "list": [
                            index
                            for index, bit in enumerate(list_bits)
                            if bit
                        ],
                    }
                )
            elif run.returncode != 20:
                raise RuntimeError(f"solver exit {run.returncode}")
    for row in rows:
        print(row)
    print(f"SAT rows: {len(rows)} / 32")


if __name__ == "__main__":
    main()
