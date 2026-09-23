#!/usr/bin/env python3
"""Replay retained certificates and compare all final state probabilities."""
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys

import independent
import verify


def main():
    folder = Path(__file__).resolve().parent
    for script, certificate in (("verify.py", "certificate.json"),
                                ("independent.py", "independent-results.json")):
        expected = json.loads((folder / certificate).read_text())
        for flags in ([], ["-O"]):
            actual = json.loads(subprocess.check_output(
                [sys.executable, *flags, str(folder / script)], text=True))
            if actual != expected:
                raise RuntimeError(f"Certificate mismatch: {script}, flags={flags}")
    chain = independent.FibreChain()
    _, pi = verify.stationary()
    checks = {}
    for label, letters, word in (("full", independent.FULL, verify.WORD),
                                  ("censored", independent.CENSORED, verify.CENSORED)):
        (numerators, denominator), _ = chain.run(letters)
        law, _ = verify.run(word, pi)
        for state, numerator in zip(chain.states, numerators):
            if Fraction(numerator, denominator) != law.get(state, Fraction(0)):
                raise RuntimeError(f"Methods disagree: {label}, state {state}")
        checks[label + "_matching_states"] = len(chain.states)
    result = {"status": "PASS", "checks": checks,
              "note": "Every probability in both final laws agrees between separately "
                      "constructed neighbour-count rational and global Gibbs-fibre "
                      "integer implementations."}
    if result != json.loads((folder / "crosscheck.json").read_text()):
        raise RuntimeError("Crosscheck receipt mismatch")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
