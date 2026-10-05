# Square-grid random-labeling peaks: audited partial results

Problem 9500009 / AMR-094-0009, queue rank 777. **UNSOLVED, 5/5 approaches used.**
The general asymptotic question remains open in this investigation. No complete
solution, novelty, priority, journal acceptance, or merge-readiness claim is made.

The graph is the square P_n Cartesian-product P_n with ordinary boundary.
The target is convergence to zero of Manhattan graph distance divided by n,
conditional on exactly two peaks. Finite exact counts for n=2,3,4, elementary
proofs, 122 forest certificates, and counterexamples to simplifications are
scoped partial results. They do not determine the large-n limit.

## Preserved record and additive audit

- `author_freeze/` and its ZIP preserve the original author packet byte-for-byte,
  including historical pending-audit and unverified-review-hash fields.
- `independent_audit/` and its ZIP record an independent PASS for the limited
  claims, with no mathematical correction. The additive audit completes review
  hash verification and supplies an optimization-resistant verifier.
- Historical queued 0/5, remote-writes-false, and pending-review descriptions in
  either freeze describe their creation times. This publication's disposition is
  UNSOLVED, 5/5. Audit work did not add a proof-search turn.

The torus conjecture, square one-peak theorem, and tree two-peak theorems remain
distinct. Fixed-graph subdivision results do not provide a growing-square limit.

## Offline replay

Requires Python 3 and an installed C++17 compiler named `g++`. No installation,
network request, or packet rewrite is performed. From this directory:

    python3 verify_delivery.py
    PYTHONOPTIMIZE=2 python3 -O verify_delivery.py

The wrapper checks the complete inventory, both original manifests, and every
ZIP member against its expanded file. It launches the author's verifier in a
fresh normal Python child with `PYTHONOPTIMIZE` removed, verifies an assertion
sentinel, and compiles C++ without `-DNDEBUG`. Do not run the author verifier
under optimization: its Python assertions can otherwise disappear.

The independent verifier uses explicit exceptions. Its normal and `-O` runs
must pass; its deliberately false reference must fail in both modes. The wrapper
checks those failures. The optional `independent_audit/code/verify_provenance.py`
requires separately held complete corpus files and catalog; those source files
are deliberately excluded from this package.

## Publication boundary

`PUBLICATION_MANIFEST.json` covers all delivery files except itself. Only authored
mathematics, code, computed outputs, certificates, safe frozen archives, and public
verification metadata are added. No source PDFs, extracts, screenshots, raw
corpora, credentials, private sources, or private coordination files are included.

The queue patch changes only this row's Status and Turns, preserving every other
byte, including its existing header, Findings, Chat, and DOI fields. Local replay
does not establish GitHub CI success; CI must be inspected for the exact PR head.
