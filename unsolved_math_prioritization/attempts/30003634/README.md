# A third-derived pure-braid counterexample

Problem 30003634 / OWR-15955-011, queue rank 1002. Disposition: **claimed_solved, 1/5**.

The universal inclusion is false already at n=1, m=3. The explicit 104-letter nested commutator beta belongs to P_3^(3), but its closure has signature -2. Every integral smooth 1-solvable algebraically split link has signature zero. Adding split trivial strands extends this n=1 counterexample to all m>=3.

Read `original/PROOF.md`, `audit1/FULL_AUDIT.md`, `audit2/AUDIT_REPORT.md`, and `PUBLICATION_ACCEPTANCE.md`. The three original frozen slices are preserved byte for byte. Their historical statements that independent review was pending or publication had not occurred are dated provenance, superseded only by this wrapper's review status. No mathematical proof correction was required by either audit.

## Reproduce

Tested with Python 3.12.14 and SymPy 1.14.0. Author verification itself uses only the standard library. Obtain the independently supplied SHA-256 pins for BOOTSTRAP.py and PUBLICATION_MANIFEST.json from the publication receipt. Copy and authenticate BOOTSTRAP.py outside the packet. Run from any directory:

    python -I -B /trusted/BOOTSTRAP.py --packet /path/to/30003634 --expected-manifest <independently-supplied-SHA256>

The trusted bootstrap pins the verifier; the external manifest pin binds every other publication file. Do not take the only trust anchor from the packet being tested. The wrapper checks exact pathsets, bytes, hashes, modes, strict JSON types, source-free scope and frozen inner manifests before running any preserved verifier. Default replay uses normal, -O and -OO modes, genuine read-only relocated fixtures, and an unrelated working directory. It also reproduces the author's 88 hostile/malformed-input rejections and the second audit's four-mode portable test. Imported topology is mathematically audited, not formally verified by these finite programs.

For independent transport adversaries, authenticate and copy TEST_MUTATIONS.py outside the packet as well, then run:

    python -I -B /trusted/TEST_MUTATIONS.py --packet /path/to/30003634 --bootstrap /trusted/BOOTSTRAP.py --expected-manifest <independently-supplied-SHA256>

`--check-only` checks artifact identity without running the mathematics. `--filesystem-profile readonly` requires files 0444 and directories 0555; the baseline requires 0644/0755. Sanitized subprocess environments and isolated Python startup ignore hostile PYTHONPATH and PYTHONOPTIMIZE values; the requested modes are explicit.

This is AI-assisted, unrefereed mathematical work. No claim of historical novelty, human peer review, proof-assistant verification, or separate failure at every higher n is made. Source citations and metadata are included; scholarly PDFs, extracts, screenshots and dataset contents are not redistributed.
