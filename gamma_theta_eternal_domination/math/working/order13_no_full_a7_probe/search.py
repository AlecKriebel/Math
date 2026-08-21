#!/usr/bin/env python3
"""Discovery probe for the residual order-13 no-full branch.

This wrapper imports the already audited full-signature-sorted no-full
formula from ``order13_no_full_decomposition/decompose.py`` and adds the
single canonical census cut ``|Q_S| <= 3``.  With the ten outside vertices
sorted by their three-bit complement signature to S={0,1,2}, this is exactly
the assertion that vertex 6 has nonzero signature.

The cut is currently justified only by the provisional four-neutral
micro-exclusion.  Therefore every output of this script remains exploratory
until that lemma, this wrapper, and any proof are independently audited.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys


S = (0, 1, 2)


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(
        "order13_no_full_decomposition_for_a7", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(campaign: Path):
    source = (
        campaign
        / "math"
        / "working"
        / "order13_no_full_decomposition"
        / "decompose.py"
    )
    module = load_module(source)
    cnf, edge, _ = module.build_relaxed_base(campaign)

    # Signature zero is neutrality.  The full S_10 sorter places all zero
    # signatures first, so Q_S has size at most three iff label 6 is
    # nonneutral.
    cnf.add(*(edge[(anchor, 6)] for anchor in S))
    return cnf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--instance", type=Path, required=True)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--solver-log", type=Path, required=True)
    args = parser.parse_args()

    campaign = Path(__file__).resolve().parents[3]
    cnf = build(campaign)
    args.instance.parent.mkdir(parents=True, exist_ok=True)
    args.instance.write_text(cnf.dimacs(), encoding="ascii")

    command = [str(args.solver), "--quiet", "--binary=false", str(args.instance)]
    if args.proof is not None:
        command.append(str(args.proof))
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=args.timeout,
            check=False,
        )
        status = (
            "SAT"
            if completed.returncode == 10
            else "UNSAT"
            if completed.returncode == 20
            else f"EXIT_{completed.returncode}"
        )
        output = completed.stdout
    except subprocess.TimeoutExpired as error:
        status = "TIMEOUT"
        output = (error.stdout or "") + (error.stderr or "")

    args.solver_log.write_text(output, encoding="utf-8")
    print(
        f"variables={len(cnf.names)-1} clauses={len(cnf.clauses)} "
        f"status={status}"
    )
    if status == "SAT":
        sys.exit(10)
    if status == "UNSAT":
        sys.exit(20)
    if status == "TIMEOUT":
        sys.exit(124)
    sys.exit(1)


if __name__ == "__main__":
    main()
