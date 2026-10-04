# Function Theory 5.46: MacLane arc tracts

Problem: **2305046 / AMR-022-5046**, queue rank **575**.

**Status: unsolved; five of five approaches used.** No solution or novelty claim.

The primary question asks for a disk-holomorphic function in the MacLane class,
with no critical points and an arc tract. The collection's terse progress note
misses substantial published restrictions; the 2017 specialist paper still
explicitly calls the full question open. A targeted search through 2026-10-04
found no later full resolution. This is not a claim of exhaustive literature
coverage.

The package provides complete proofs of partial results, including a quantitative
Cauchy growth-transfer estimate, a closed-barrier impossibility theorem, a
bounded-variation path lemma, and a fully analyzed exponential near-miss. It
also proves why Abel universal constructions supply high arcs while failing
the required boundary class. Published boundary-theory inputs are marked.

## Files

- PROOF.md: exact target, eight propositions, dependencies, remaining gap
- ATTEMPT_LOG.md: five materially different routes and their failure points
- SOURCE_GATE.md / SOURCE_MANIFEST.json: statement, prior-work and source checks
- STATUS.json: conservative machine-readable disposition
- verify.py / CHECKS.json: reproducible bounded controls and their limits
- verify_manifest.py / SHA256SUMS.json: public-file integrity

## Reproduce

Use Python 3.10 or later; only its standard library is required.

    python3 verify.py
    python3 verify_manifest.py
    python3 -m py_compile verify.py verify_manifest.py

The check script prints deterministic JSON. Compare it with CHECKS.json.
Optionally, `python3 verify.py --source-dir PATH` verifies the two primary PDFs
and the 2025 article against their source hashes when those files have been
obtained independently. No source PDF or bulk problem corpus is distributed.

Finite arithmetic controls are not a formal proof checker or an existence
search. They do not certify the imported theorems, a boundary limit, global
univalence, or the open target. The proof is the mathematical text and its
explicitly identified dependencies.
