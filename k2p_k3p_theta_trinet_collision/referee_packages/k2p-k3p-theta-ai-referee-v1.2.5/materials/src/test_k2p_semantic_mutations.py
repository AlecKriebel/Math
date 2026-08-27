#!/usr/bin/env python3
"""Negative tests for compact-K2P certificate field consumption."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / "certificate_k2p_simple.json").read_text(encoding="utf-8"))


def main() -> None:
    certificate = copy.deepcopy(BASE)
    certificate["network_transition_probabilities"]["K_odot_K"][0][0] = "999"
    with tempfile.TemporaryDirectory(prefix="k2p-semantic-mutation-") as temp_name:
        directory = Path(temp_name)
        shutil.copy2(ROOT / "verify_k2p_simple.py", directory / "verify_k2p_simple.py")
        (directory / "certificate_k2p_simple.json").write_text(
            json.dumps(certificate, indent=2) + "\n", encoding="utf-8"
        )
        command = [sys.executable]
        if sys.flags.optimize:
            command.append("-" + "O" * sys.flags.optimize)
        command.append(str(directory / "verify_k2p_simple.py"))
        completed = subprocess.run(
            command,
            cwd=directory,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    combined = completed.stdout + completed.stderr
    diagnostic = "K_odot_K stored transition row"
    if completed.returncode == 0:
        raise RuntimeError("mutated K_odot_K transition row unexpectedly passed")
    if diagnostic not in combined:
        raise RuntimeError(
            "mutated K_odot_K transition row failed for the wrong reason; "
            f"expected {diagnostic!r}\n{combined}"
        )
    print(f"[mutation rejection] PASS  stored K_odot_K transition row: {diagnostic}")
    print("\nALL K2P SEMANTIC MUTATION CHECKS PASSED")


if __name__ == "__main__":
    main()
