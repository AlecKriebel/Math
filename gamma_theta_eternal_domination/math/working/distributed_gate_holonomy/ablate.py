#!/usr/bin/env python3
"""Single-unit ablation of the shortest distributed-gate probe."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import tempfile


PROBE_PATH = Path(__file__).with_name("probe.py")
SPEC = importlib.util.spec_from_file_location("distributed_gate_probe", PROBE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load probe.py")
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
build = PROBE.build


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    args = parser.parse_args()
    cnf, _ = build(2, 1, enforce_gamma=False)
    units = [
        (index, clause[0], cnf.names[abs(clause[0])])
        for index, clause in enumerate(cnf.clauses)
        if len(clause) == 1
    ]
    with tempfile.TemporaryDirectory(prefix="gate-ablate-") as tmp:
        root = Path(tmp)
        for index, literal, name in units:
            clauses = cnf.clauses[:index] + cnf.clauses[index + 1 :]
            body = "".join(
                " ".join(map(str, clause)) + " 0\n"
                for clause in clauses
            )
            instance = root / "instance.cnf"
            instance.write_text(
                f"p cnf {len(cnf.names) - 1} {len(clauses)}\n{body}",
                encoding="ascii",
            )
            run = subprocess.run(
                (
                    str(args.solver),
                    "--quiet",
                    "--binary=false",
                    str(instance),
                ),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            status = "SAT" if run.returncode == 10 else "UNSAT"
            sign = "+" if literal > 0 else "-"
            print(f"{status:5} remove {sign}{name}")


if __name__ == "__main__":
    main()
