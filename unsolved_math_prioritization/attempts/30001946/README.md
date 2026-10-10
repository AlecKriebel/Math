# Rational Witt geometric isolation: corrected partial results

Problem **30001946 / OWR-11454-004**. Original target **unresolved**, five of five construction routes exhausted, zero new proof-search routes. This is an AI-assisted authored investigation and independent mathematical audit, not conventional human peer review or journal acceptance. No novelty, worldwide-openness, or counterexample to Friedman's existence question is claimed.

## Read the mathematics first

- `current/REPORT.md` is the complete corrected report, preserved byte for byte from the accepted audit.
- `current/AUDIT.md` is the complete independent audit, including the detailed pinch and separation quotients, local links, triangulation, collars, boundary signs, and source limitations.
- `current/REPORT_CORRECTIONS.patch` preserves the contextual correction from the superseded report to the corrected report. The old full report is deliberately omitted. This patch is a historical comparison, not an instruction to patch the already-corrected report again.
- `historical/INDEPENDENT_ACCEPTANCE.json` is the earlier scoped mathematical decision. `historical/SOURCE_REVIEW.json` and `historical/PUBLIC_SOURCE_METADATA.json` contain inspected scholarly titles, public URLs, public PDF hashes and byte counts, and exact historical retrieval/inspection limitations. No source document bodies are included.

The full audit is unchanged, so its references to `original/authored/REPORT.md`, the standalone audit archive, its former manifest, and its old replay receipts describe that earlier audit packet. Those artifacts are not members of this selected publication. Its closing historical replay discussion is not the final verification receipt for this delivery. The publication's current executable entry point is the externally authenticated bootstrap described below; final receipts remain outside the delivered inventory to avoid circular certification.

## What is accepted

1. The standard direct-cone range: odd dimensions, and even dimension `2m` when `IH_m(X;Q)=0`.
2. A sufficient boundary-surjectivity criterion in even dimensions at least four. For `X=M union_E N`, a surjection `H_m(E;Q) -> IH_m(N;Q)` kills the middle group of the residual cap. The written pinch, separation and cone traces give an actual finite oriented PL Witt bordism to `M union_E cE` with its required collars.
3. The product-cone corollary, with the zero-dimensional link handled separately as the interval case. Its degree-zero boundary map is surjective, not the inapplicable positive-dimensional cone-formula isomorphism.
4. The weighted-projective example `P(1,1,2,2,2)`: its signature is one, while the naive cap of its regular core has signature zero. Its regular locus has zero degree-four rational homology while middle intersection homology is one-dimensional. These refute two proposed intermediate recipes, not the original existence statement.
5. The restricted Banagl–Chriestenson application with dimension, equivariance, Moore approximation, and PL-compatibility assumptions preserved. Their local-duality hypothesis is not silently inserted into Proposition 10.1, and their equivariance hypothesis is not dropped.

For disconnected `E`, the pinch link and suspension have the same normalization, the disjoint union of the suspensions of the connected components. The suspension itself need not be normal. At vertex separation only the outgoing suspension poles are identified; incoming poles stay separate. The event codimension, outgoing apex line, orientation convention and collar gluing are explained in full in the audit.

The remaining problem is a universal geometric, terminating treatment of a capped singular neighborhood with nonzero middle intersection homology, arbitrary twisting and higher depth. Equality or classification of Witt classes is not supplied as a substitute for that missing construction.

## What the executable checks actually do

`current/independent_checks.py` and `current/CHECK_FIXTURES.json` are unchanged from the audit. The checker has runtime exception guards and no Python assertions. It computes:

- 200 cone cutoff/allowability cases (`m=2,...,201`)
- an eight-element sign orbit for the finite quotient example
- Kawasaki gcd/lcm coefficients `(1,2,4,8,8)` and the rational pairing `1/8`, with integral square `2` and exact rescaling
- the four supported sphere-bundle degrees `0,2,5,7` and the absence of possible supported differentials in the tested range
- the specified cokernel rank, and 17 rational diagonal-map rank cases

The recorded normalization component numbers and theorem-scope flags are **claim-consistency fixtures**, not computed PL invariants. Likewise the input homology dimensions and signatures come from the written proof; checking arithmetic with these inputs does not independently establish the topological inputs. Finite cone tests do not prove all dimensions, and finite spectral support checks do not supply the bundle or spectral sequence. No executable recognizes PL spaces, constructs a universal bordism, establishes novelty, or replaces the proof and source audit.

`check_case.py` adds recursive exact fixture types and runs controlled mutations of data or of the actual guarded checker in memory. It never changes the delivered checker. Per interpreter mode, `run_finite_checks.py` runs one positive checker case and exactly 64 intended rejections:

- 14 algorithm mutants
- 20 arithmetic fixtures
- 14 normalization/theorem-scope claim-consistency fixtures
- 15 fixture-schema controls
- one explicit false-condition exception guard

Every case is required by exact identity and order. Every full raw stdout/stderr byte, exact integer exit code, recursive JSON type, count, diagnostic and detail must match the fixed mode-specific contract. No output normalization, substring PASS, empty suite, SKIP, or expected-failure promotion is accepted. Each of normal, `-O`, and `-OO` is actually executed, rather than inferred from assertion-free source.

## Noncircular verification and final replay

Before execution, authenticate `BOOTSTRAP.py` against its SHA-256 published externally in the draft PR. Do not infer trust from an in-packet hash of the same file. The fixed bootstrap binds the entire `PUBLICATION_MANIFEST.json`, the verifier and the mutation harness before executing them. The noncircular manifest binds every other delivered file, including all proof text, metadata, fixtures, references and code; it excludes only itself and the externally anchored bootstrap. The verifier enforces the exact complete recursive inventory, not just a subset of files.

Use Python 3.12 as UID/EUID 1000; make each delivered file mode 0444 and each delivered directory mode 0555, including the root. Run from a clean external working directory, using a separately copied, independently hash-checked bootstrap:

```sh
python -I -S -B /trusted/BOOTSTRAP.py --controls /path/to/packet
python -I -S -B -O /trusted/BOOTSTRAP.py --controls /path/to/packet
python -I -S -B -OO /trusted/BOOTSTRAP.py --controls /path/to/packet
```

The final external receipt records complete before/after SHA-256 and size snapshots for every file and all three control runs. Controls separately exercise every changed member, omissions/additions, symlinks/hardlinks/FIFOs, resealing attacks, bootstrap/harness argument and authentication failures, strict JSON/schema and acceptance-scope corruption, and direct whole-output comparator attacks. Actual append/create/unlink attempts must fail physically under UID/EUID 1000. Hostile working-directory modules and Python environment hooks must not execute; the entire baseline stdout/stderr must remain byte-identical. Integrity and hostile replays add no mathematical coverage.

`CHECK_RUNS.json` records pre-seal captures only. The final run receipts, trust anchor, and held-out replay receipts are external; they are not self-certified members of the packet. Historical audit harnesses, the assertion-disabled original arithmetic checker, superseded full report, old replay receipts, source bodies and datasets are not run by this publication and are explicitly `NOT_RUN` in the current scope. No new source search is claimed.

## Publication boundary

Only this problem's selected authored proofs, audit, public scholarly metadata and verification support are delivered. No copied source texts, datasets, private sources, private coordination, or identifying names/hashes for excluded private files are included. The old broad manifest is omitted. No queue or unrelated repository file is changed.
