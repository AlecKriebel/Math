# Multiplicatively weighted centers: verification package

The research note resolves the finite algorithmic version of Ducoffe's OWR8/2026 Open Problem1: exact vertex centers with nonnegative multiplicative real weights on a promised finite connected simple unit-edge median graph supplied by adjacency lists. A center, optimum radius, and all centers take deterministic O(n log^5(2n)) exact operations, with no dimension bound. The contribution is a short capped threshold/complement observation and its consequence from credited algorithms. The additive BDH algorithm, weighted-midpoint optimization method, and earlier cube-free result are prior work. Historical firstness and continued open status today are not asserted.

Read `weighted_centers.tex` / the separately deposited `weighted_centers.pdf` for the current submission text. `CURRENT_PRIORITY_ASSESSMENT.json` is the current bounded priority assessment. `CORRECTIONS.md` maps all changes from the immutable original. The source correction is deliberately specific to arXiv2410.10235v1, not a claim about uninspected final SODA typesetting.

The `original/` tree contains all 16 unchanged PR-head artifacts, including both ordinary SHA256SUMS files. These retain historical pending-stage language and do not supersede the current note. The four new independent families in `reviews/` contain early-independent checkpoints, adversarial proofs, controls, full source comparisons, query ledgers, limitations, and their authored-only SHA256SUMS seals. Raw third-party full texts, OCR, screenshots, credentials, account files and other projects are excluded.

## Offline reproduction

Use standard CPython 3.11 or later, with assertions enabled. No third-party Python package, account, network access, compiler or source PDF is needed for the mathematical controls. Extract the ZIP and, from its sole root directory, run:

```
python3 run_all.py
```

This verifies the entire outer inventory, all six nested SHA256SUMS manifests, and every original snapshot hash. It runs all five registered controls in separate temporary copies, comparing complete mathematical JSON outputs with sealed records. The only normalized fields are the three execution-clock fields in `reviews/oracle01/controls.py`: start time, completion time and elapsed seconds. Every count, case, exact value, bound, script hash, explanatory field and all other output fields must match. No original or expected record is rewritten. The final output must report PASS and `frozen_payloads_unchanged: true`.

The original bundle tests 10,626 optimizations and 145,644 feasibility sets. The historical independent audit tests 180,102 graph profiles, 2,500,246 feasibility sets and 298,602 abstract searches. The new oracle family tests 54,959 profiles, 199,663 pivots and 17 complete source-recursion profiles; the new search family tests 48,641 graph cases, 579,377 feasibility sets, 243,120 abstract optimizations and 65,535 cube-subset edge bounds. The new priority family adds 143,170 threshold checks and 10,004 optimizations. Exact case details and caveats are in the individual JSON records. Counts overlap across families and must not be presented as a count of distinct independent problem instances.

All-pairs reference routines and brute structural preprocessing are deliberately slow. They falsify finite errors in the new bridge, search invariants and source-recursion identities. They do not implement the fast general BDH oracle or experimentally establish its asymptotic running time. Universal correctness and complexity rest on the proofs and named classical dependencies. Original profile comparisons can be made exactly on rationals; their bit cost depends on input encoding length. No arbitrary-edge-length, recognition, infinite-encoding or local-unimodality result is claimed.

## Building and integrity

`BUILD.json` and `PDF_QA.json` document the exported five-page PDF. Rebuild it with Tectonic0.16.9 and the recorded SOURCE_DATE_EPOCH; the desktop compiler was also checked without changing the open PR521 editor. A TeX installation can require network access for fonts/packages; that is separate from the offline controls. The source date is a reproducibility setting, not evidence of a discovery date. `make_package.py` deterministically recreates the ZIP from the audit checkout and is included for inspection; it is not intended to run inside the extracted archive.

`MANIFEST.json` inventories every payload except itself; nested seals and the independently recorded original snapshot preserve earlier freezes. The producer validates source containment and excludes forbidden components in both lexical and resolved audit-relative paths and in archive member names. Internal aliases cannot erase these exclusions. The same checkout can be rebuilt under ordinary, `.cache` or `scratch` ancestors outside the audit. Integrity hashes establish consistency, not authenticity, historical priority, proof-assistant certification or human peer review. Fresh final package adversaries and their acceptance receipts are stored beside the publication in the repository, outside this archive to avoid self-reference.

## Disclosure and reuse

AI tools were used extensively in solving, development, writing, reproduction and adversarial verification. This is an unrefereed preprint; internal AI adversarial reviews are not human peer review. No human peer review or proof-assistant certification has been obtained. Priority remains bounded: no earlier explicit same-scope resolution was located, but inaccessible original tree-center ancestors, uninspected final SODA typesetting and incomplete indexing prevent a worldwide-first guarantee. Full public author preprints and accessible primary descendants were compared; the note makes no claim of independently reading inaccessible texts. No outside individual was contacted.

Author: Alec Kriebel, independent researcher, ORCID0009-0001-9320-500X. Authored materials are released under CC-BY-4.0. Primary publications retain their own rights and are linked, not redistributed here.
