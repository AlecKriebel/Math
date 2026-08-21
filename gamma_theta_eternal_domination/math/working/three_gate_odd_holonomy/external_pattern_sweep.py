#!/usr/bin/env python3
"""Enumerate extendible H-neighborhood patterns of one external vertex."""

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
        spare_vertices=1,
    )
    edge = metadata["edge"]
    assert isinstance(edge, dict)
    q = 12
    base_lines = cnf.dimacs().splitlines()
    compatible: list[int] = []
    with tempfile.TemporaryDirectory() as directory:
        instance = Path(directory) / "trial.cnf"
        for mask in range(1 << 12):
            units = []
            for vertex in range(12):
                variable = edge[probe.pair(vertex, q)]
                units.append(variable if mask & (1 << vertex) else -variable)
            header = base_lines[0].split()
            header[3] = str(int(header[3]) + len(units))
            instance.write_text(
                "\n".join(
                    (
                        " ".join(header),
                        *base_lines[1:],
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
                compatible.append(mask)
            elif run.returncode != 20:
                raise RuntimeError(f"solver exit {run.returncode}")

    result = {
        "compatible_count": len(compatible),
        "patterns": [
            [vertex for vertex in range(12) if mask & (1 << vertex)]
            for mask in compatible
        ],
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"compatible patterns: {len(compatible)} / 4096")


if __name__ == "__main__":
    main()
