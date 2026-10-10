# Definable quotients: literal formulation correction

Problem **30001405 / OWR-4196-003**, rank **975**. Queue disposition: **statement_needs_correction**, **1/5** substantive mathematical attempts. AI-assisted, unrefereed authored mathematics; no novelty or priority claim.

## Exact result and unresolved target

The [complete proof](corrected_author/PROOF.md) partitions a semialgebraic 2-sphere into its north pole and its complement. Both classes are definably contractible, and constant decreasing sequences satisfy the literal set-approximant condition. Their two-point logic quotient is discrete and locally contractible, with zero second homotopy group, while the definable sphere has nonzero second homotopy group. The projection is discontinuous.

This disproves **only the literal set-approximant wording**. The intended continuous version and the locally contractible/open-approximant version remain unresolved here. [Achille-Berarducci (2018)](https://doi.org/10.1007/s00029-018-0413-3) proves the comparison for a **triangulable** quotient with contractible **open** approximants. The [bridge lemmas](corrected_author/BRIDGE_LEMMAS.md) explain stabilization, finite quotients and first countability; they do not remove the missing triangulability/comparison gap.

Two complete independent reports, [Audit A](audit_a/INDEPENDENT_AUDIT.md) and [Audit B](audit_b/REVIEW.md), accept this narrow counterexample and the three bridge lemmas with no blocking mathematical correction. This disposition records a proved source formulation defect after one actual approach; it does not manufacture four additional attempts or mark the intended problem solved.

## Preserved evidence and citation refinement

All original files in `author`, `audit_a` and `audit_b` are preserved byte-for-byte, including both complete reports and Audit A's actual [pagination patch](audit_a/CITATION_REFINEMENT.patch). The patch is applied only in `corrected_author`, whose manifest is independently regenerated. It clarifies that the OWR contribution body occupies printed pp. 27–28 and its last reference continues on p. 29; no mathematics changes. The wrapper verifies that these are the only changes in the corrected copy.

The [source audit](corrected_author/SOURCE_AUDIT.md) and each independent source-verification record retain exact individual access limitations. The published 2011 Berarducci-Mamino assumptions were inspected in indexed primary-document text; no full 2011 PDF or pixel inspection or PDF hash is claimed. The original author, Audit A and Audit B encountered different access outcomes, which are deliberately not flattened into one retrieval history. This publication step replays frozen evidence, without claiming fresh literature retrieval or source inspection.

Only authored mathematics, code and public bibliographic/integrity metadata are included. No copied papers, source extracts, source images or dataset contents are present. Historical local dataset/PDF hash checks remain historical; source-free replay does not rerun them.

## Portable, externally anchored replay

Use Python 3.10+ and `sympy==1.14.0`. Obtain the trusted SHA-256 of `PUBLIC_MANIFEST.json` from the PR description, independently of this downloaded packet. From any working directory:

```sh
python3 -I -B /path/to/packet/verify_publication.py --expected-manifest TRUSTED_SHA256
python3 -I -O -B /path/to/packet/verify_publication.py --expected-manifest TRUSTED_SHA256
python3 -I -O -B /path/to/packet/mutation_tests.py --expected-manifest TRUSTED_SHA256
```

The validator authenticates the exact file/directory allowlist, sizes, hashes and all three original manifest pins before running code. It rejects extra/missing content and symlinks. It verifies every corrected-copy byte against the frozen actual patch. No network or source files are needed.

The author has 20 exact symbolic/finite-chain diagnostics; Audit B has 30 exact diagnostics, including 75 supplemental rational witnesses. Audit A replays the 20 author checks and rejects four mathematical mutations plus one byte mutation. `hardened_runner.py` preserves historical source bytes while compiling `assert` statements as explicit checks in memory, so assertions remain effective under `-O`. It also propagates the actual optimization flag to Audit A's child processes. Replay checks the actual mode of each direct and nested child. Byte-identical author/Audit B output is required. Audit A's historical dataset-only fields are explicitly omitted in source-free replay, not represented as freshly verified.

Finite algebra, chain, enumeration, witness and integrity checks do not formalize saturation, real-closed-field completeness, topology, homotopy invariance or the mathematical argument. Check counts are not proof certificates. The external pin must come from a trusted channel; self-consistent hashes alone do not authenticate a replacement packet.
