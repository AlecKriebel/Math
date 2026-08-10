#!/usr/bin/env python3
"""Fail-closed wording and dependency audit for the theorem release."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import re
text=(ROOT/"manuscript"/"main.tex").read_text()
flat=re.sub(r"\\\\|\s+"," ",text)
required=[
 "at most three dynamically active species",
 "at most two active linkage classes",
 "no future activation is conditioned upon",
 "aggregate-debt",
 "actual target",
 "edgewise zero",
 "nonexplosive",
]
for phrase in required:
    assert phrase in flat,phrase
for forbidden in [
 "arbitrary number of linkage classes",
 "all bimolecular weakly reversible stochastic mass-action network is",
 "condition on the activation",
 "genealogical stack",
]:
    assert forbidden not in flat,forbidden
assert "W_\\tau\\le W_0-1" in text
print("claim_audit.py self-test: OK")
