# Verification package: the odd outer focal-inverse area product

This folder supports the accompanying research note on the invariant labelled
`k904,a` in Reznik–Garcia–Koiller, arXiv:2004.12497v11, Table 10. It contains
checkable derivations, independently authored controls, their frozen results,
and the complete 19-file original submission from PR211 head
`9d7b623203b525386da3d9d91548c79e7445a11c`.

The claim is phase independence of the product of the two **signed straight-edge
areas** obtained by unit inversion of the **outer tangent-intersection vertices**
about the **original billiard foci**. The domain is a strictly nested nondegenerate
confocal ellipse pair, every odd least period at least three, and all admitted
coprime star windings. An r-fold repetition multiplies each signed area by r and
the product by r². Original-vertex inversion and inversion about the outer
locus's own foci are different constructions.

The universal argument is in the accompanying note and the independent
derivations. Finite computations support that argument. High-precision numerical
agreement is **uncertified diagnostic evidence**, without interval enclosures.
The checks do not constitute formal proof-assistant verification, human peer
review, or historical priority certification.

## Reproduce

Use Python 3.10 or newer, with exactly the two versions in `requirements.txt`.
The exercised environment was Python 3.14.6, SymPy 1.14.0, mpmath 1.3.0.
No network access, repository checkout, private data, special directory, or
absolute workspace path is required to run the package. The integrity check
alone uses only the Python standard library.

From this folder:

```text
python -B run_verification.py
python -B run_verification.py --list
python -B run_verification.py --run core
python -B run_verification.py --run scope
```

`--run all` runs all ten jobs; each job ID printed by `--list` can be run alone.
Do not use Python's `-O` or `-OO` options, which disable assertions. The harness
rejects optimized execution and mismatched library versions. A scientific-result
mismatch is an error requiring investigation, rather than automatic acceptance
at a looser tolerance.

Each archived checker writes a result beside its own script. The harness copies
only the required inputs into a temporary folder, runs the unmodified checker
there, compares its JSON with the frozen result, and removes the temporary
folder. It checks the entire frozen payload before and after replay. It never
runs a checker in the archived original submission. Python-version text is
excluded from the scientific comparison only for the two new algebra/divisor
results that record it; all their mathematical fields must match exactly.
The harness reports both scientific equality and raw byte equality.

The five core jobs contain both exact and numerical parts, except the source
geometry job, which is numerical throughout. They take longer than a checksum
check. Dependency installation is optional preparation by the reader; the
harness never installs or downloads anything. If needed, create your own
environment outside this frozen folder and install from `requirements.txt`.

## What is checked

| Job | Exact evidence | Separate uncertified numerical evidence |
|---|---|---|
| `author` | 102,770 assertions: eight symbolic/Laurent controls plus eleven controls on each of 9,342 finite coprime rotations | 3,288 diagnostics at 85 decimal digits, 60 families |
| `inherited_independent` | 8,438 assertions, including 1,053 rational-lattice rotations and symbolic geometry/edge identities | 5,412 diagnostics at 90 digits, 54 families |
| `source_geometry` | None; its well-definedness/incidence tests are numerical diagnostics | 10,530 diagnostics at 80 digits, 42 families, including direct tangent intersection, reflection, reversal and repetition |
| `geometry_algebra` | Nine zero polynomial residuals; one rational Jacobi datum and exact inverse edge `1521√14/39500`; two exact scaling factors | 100-digit diagnostics: 96 local cases, 70 closed families, 280 phases, 40 families with reversed outer-axis ordering |
| `meromorphic_divisor` | Eight zero polynomial residuals; 1,053 finite rational-lattice pairs through N=101 | 24 real/complex cases at 90 digits, including pole orders, cancellation and the N=3 critical residue |

These assertion counts overlap in what they test and must not be added to claim
that many independent theorems. Finite lattice enumeration corroborates the
written universal arithmetic; it does not prove all periods by exhaustion.
The numerical normalizations sometimes use `max(1, abs(value))`, so a small
absolute residual need not be a small relative error for a tiny product.

Five optional `scope` jobs separate nearby constructions and test proposed
priority transfers. One uses standard-library exact biquadratic arithmetic;
the others use the pinned libraries. They include two exact triangular phases
of one billiard with original inverse-area product `1/324` and outer product
`1/3600`, and two exact counterexamples to a broader concentric-Poncelet
transfer. Those counterexamples are **not** counterexamples to the theorem in
the note. The classical-transfer job also has explicitly labelled numerical
diagnostics. None supplies a missing all-period inverse-area-ratio theorem.

## Files and provenance

- `original_submission/` preserves all 19 submitted files byte-for-byte,
  including nested `independent_review/` files. Its pending-review metadata,
  imported triage dates and older status language are historical evidence;
  they are not the current priority assessment. Do not edit them.
- `audits/` preserves the five new, distinct audit families' authored reports,
  mathematical derivations, source/version ledgers, controls, results and their
  original manifests. Family reports retain their original limited remits.
- `audit_receipts/` contains root's mathematical/priority integration and
  isolated replay receipts. The earlier mathematical receipt's “priority not
  yet audited” is chronological; `ROOT_PRIORITY_ACCEPTANCE.json` records the
  later bounded priority decision.
- `scope_controls/` contains root's independent exact constructions and
  transfer-obstruction controls with results.
- `PROVENANCE.json` gives the original native head, all 19 original hashes and
  byte sizes, and five validated family-manifest hashes.
- `PRIORITY_AND_CREDITS.md` explains the qualified claim and known earlier work.
- `MANIFEST.json` binds every file in this verification folder except itself.
  `build_verification.py --seal` regenerates it after an intentional revision;
  resealing is a packaging step, not a review or publication clearance.

Run only the documented harness for portable replay. In particular,
`audits/priority_classical_general_01/build_audit_ledgers.py` is preserved as a
historical ledger-generation utility: it requires deliberately excluded
private reading copies and is **not a portable replay target**. Historical
reports may show original local command paths; no such path is required by the
harness. The original family manifests retain their source-directory path
bases; the portable `MANIFEST.json` provides the current folder-level seal.

All third-party primary PDFs, extracted texts, HTML payloads, rendered pages,
private transport records and caches are excluded. Primary URLs, edition
locators, source hashes, authored analyses and access limitations remain.

## Research status

This packet was prepared after mathematical and source-scope acceptance and a
bounded priority audit. Its preparation log describes preparation milestones,
not publication authorization. Root must integrate the final manuscript and
metadata, obtain the required fresh sequential whole-package reviews, resolve
their findings, and separately seal the final publication bundle. Extensive AI
assistance was used in the work and adversarial checks. No independent human
peer review is represented, and no first-proof or absolute-novelty claim is made.
