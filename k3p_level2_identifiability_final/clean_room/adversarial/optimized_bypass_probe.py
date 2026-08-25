#!/usr/bin/env python3
"""Demonstrate that optimized Python strips the corrected verifier's gates."""
from __future__ import annotations

import copy
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CLEAN_ROOM = HERE.parent
sys.path.insert(0, str(CLEAN_ROOM))

import verify_h21_transport_and_fourteen_orbits as verifier


if not sys.flags.optimize:
    raise RuntimeError("this probe must be run with python -O")

record = copy.deepcopy(verifier.RECORDS["H21-01"])
record["raw_members"] = record["raw_members"][:-1]
record["raw_member_transports"] = record["raw_member_transports"][:-1]
reconstruction = verifier.reconstruct_record(record)

if len(record["raw_members"]) != 3 or len(reconstruction["double_coset"]) != 4:
    raise RuntimeError("optimized bypass probe did not reach the intended state")

print("OPTIMIZED_ASSERT_BYPASS_CONFIRMED claimed=3 reconstructed=4")
