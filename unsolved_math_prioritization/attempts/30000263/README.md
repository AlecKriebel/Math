# Bahri-Xu discrete interaction inequality: audited partial results

**Problem 30000263 / OWR-1050-014, rank 806: unsolved, 5/5 approaches.** The independent agent audit accepts the stated partial results with no mandatory mathematical correction. The general three-dimensional inequality is not proved or disproved by this work.

## Accepted scope

- Real collinear pointwise zero exclusion follows from a cubic identity, a finite Kelvin inversion center, and strict negative distance energy for nonzero zero-sum weights.
- A quantitative support-transfer bound handles inactive sites, with explicit support-zero and support-one boundary cases. Pointwise zero exclusion is proved through five active sites.
- A six-point spatial zero system has a planar representative, and a planar one embeds into three dimensions. This is a zero-system reduction, not invariance of a quantitative ratio under inversion.
- Two regular concentric rings cannot give a zero system when charges are constant on each ring. Arbitrary charges are outside this result.
- A concrete configuration refutes a minimum-enclosing-ball assertion in the 2011 author-hosted manuscript. A separate complex-weight example invalidates one local inference on the inspected 2021 journal page. Neither example is a counterexample to the full published theorem or a solution of its full simultaneous zero system.

**Uniform constants retain an external dependency.** The published collision/escape theorem (Theorem 1.4 and its inductive Theorem 2.6) is imported in a fixed ambient dimension with all smaller point counts covered. Pointwise zero exclusion on a noncompact configuration space alone does not establish uniformity. The audit does not independently reprove all collision/escape estimates.

The planar mixed-sign, full-support six-point case remains unresolved, as does the unrestricted target. Twenty-four saved numerical outputs replay, but their positive observed ratios are not global lower bounds. Optimizer trajectories were not rerun; budget exhaustion remains recorded. No novelty, priority, human peer review, exhaustive literature review, or present-day global openness is asserted.

Read [the authored report](author/RESEARCH_REPORT.md), [the full independent audit](audit/AUDIT_REPORT.md), [mandatory corrections: none](audit/MANDATORY_CORRECTIONS.md), and [the precise verdict](VERDICT.json).

## Clarifications without changing frozen files

The Kelvin citation is arXiv Proposition 2.3 / journal Proposition 2.4. The numerical search uses a smooth nonnegative squared-residual objective on its valid domain; the residual vector is signed, and the invalid-input penalty is not a globally smooth extension. A future exploratory tool revision should retain a computed floating-point zero for rigorous validation rather than reject it. None of these nonblocking suggestions changes the accepted proof or the 24 positive saved rows.

The 14 author files, 14 audit files, and two safe ZIPs are byte-for-byte unchanged. Historical pending-audit and no-publication statements describe those freeze stages; this wrapper records the later acceptance and publication. The archive digests are:

- Author, 33182 bytes: e2f02d9bcc751e0551ccde2a32ab3ff701e2355b0394aeb24c56b96adb44a14e
- Audit, 28682 bytes: 6ed153156d617c2c14d3761fb5fdb68680b2bfa2e380076198f151d0fac3f643

## Verification

Python 3.10+ and the standard library suffice. From this directory:

    python3 verify_package.py
    python3 -O verify_package.py
    python3 run_package_controls.py
    python3 author/test_verifier.py
    python3 audit/audit_controls.py --author-zip archives/DISCRETE_INTERACTION_30000263_AUTHOR_SAFE_FREEZE.zip

The wrapper checks exact file/directory inventory, byte counts, hashes, frozen manifests, ZIP CRCs and member-byte equality, and executes both mathematical checkers in ordinary and optimized Python. Package controls repeat clean verification after relocation and reject tested corruptions in both modes. These are finite integrity and computation checks; the mathematical arguments require the independent audit and are not formal machine proofs.

Optional external source checks can be repeated without including private files in this package:

    python3 verify_package.py --corpora CATALOG.json PROBLEMS.json REPORTS.json --source-dir PDF_DIRECTORY

The five PDF filenames and public URLs are in the frozen source metadata. If the corpora or PDFs are omitted, the current run reports NOT_PROVIDED. Historical supplied-input checks are separate evidence, never a claim that omitted inputs were checked in this run. Optimizer trajectory rerun is NOT_RUN.

For the exact queue patch, supply original and branch queue files:

    python3 verify_package.py --queue-base BASE_QUEUE.md --queue-updated BRANCH_QUEUE.md

Only this row's Status and Turns become unsolved and 5/5. All other bytes, including the existing header, are preserved. There is no global queue, ranking, state, or history regeneration and no extra proof-search turn. The publication manifest excludes itself and must be anchored to a trusted Git commit or retained receipt; a replaced verifier can lie.

Only authored analysis/code/audit/results and public verification metadata are included, together with the two safe archives. No copied source documents, extracts, raw datasets, private sources, or private coordination are published. This is draft review only, with no merge, release, DOI, or outside outreach.
