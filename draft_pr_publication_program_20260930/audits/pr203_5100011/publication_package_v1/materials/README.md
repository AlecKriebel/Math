# A flag-curve proof of an original-side pedal-area invariant
Alec Kriebel, 16 October2026. Extensive AI assistance; unrefereed preprint.

This attributed note presents the signed original-side-line pedal-area product for a>b>0,0<lambda<b², proper confocal elliptical caustic, primitive LEAST N divisible by4, every fixed finite real M, all coprime stars and both orientations, including zero/negative pedals. The analytic manuscript supplies the universal proof. Finite computations do not.

Ferudun's October15 note DOI10.5281/zenodo.23400541, TheoremA,p2, already states the exact theorem and stronger complex-point form. Its complementary poles/zeros method, N4 formula and star example are credited. Steiner radiality and established Schwartz–Tabachnikov/AST/Chavez flag/meromorphic methods are credited; complete N4 also follows from Bialy–Tabachnikov's distance product. Neither theorem/method novelty, first disclosure nor independently verified discovery is claimed.

The current public PR203 server record was created2026-10-01T05:24:27Z; immutable original HEAD8edca9d773c085adb4ed0611357a7a2957e3395d has the archived proof. The exact-result deposit was created2026-10-15T16:11:42.588744Z. These separately labeled record dates do not establish historical visibility at every earlier moment, discovery times or independent discovery. The source table does NOT print least period. Exact doubled-6 nominal12 products56000/729 vs57344/729 show why an unrestricted repeated-length reading is false.

## Reproduce
Python3.14.6, SymPy1.14.0 and mpmath1.3.0 were validated. Requirements are in requirements.txt; no dependency software or installer is included. Other Python versions are unvalidated and must rerun the checks. From this extracted directory, in an environment containing those versions:
python -B verification/run_checks.py
python -B -O verification/run_checks.py
python -B verification/run_checks.py --full-physical
python -B verification/run_checks.py --legacy-replay
python -B verification/run_checks.py --guard-false
python -B -O verification/run_checks.py --guard-false

The final two commands MUST fail with DELIBERATE FALSE CONDITION. The default runs282 explicit-exception exact geometry controls,7 symbolic N4 identities and rejects an actual8->9 coefficient mutation. No checks depend on removable assert statements. --full-physical additionally reconstructs39 physical caustics without Jacobi functions (107962 checks) and fixed zero/negative-M coefficient diagnostics. These are finite noninterval computations; high precision is not an interval certificate. Full runs may take several minutes. All output writes go to disposable temporary copies, never package inputs. The runner verifies the complete material manifest first.

--legacy-replay replays unchanged original author/reviewer code ordinarily in a disposable copy and requires byte-identical historical result JSON/stdout. It refuses optimized legacy validation. Historical code uses asserts: under -O all enforcement disappears while counters continue; actual false identities pass. The archived RAM replay receipts distinguish24,110/20,578 ordinary enforced assertions from zero optimized enforcement. Historical receipts alone do not certify unknown original runtime settings.

PORTABILITY_PROVENANCE.json identifies exact original and portable code hashes: two repository-specific dependency-path insertion lines were removed from each main checker; signed_edge_checks.py is unchanged. Mathematical operations and explicit checks were preserved. Raw historical programs, failed conditioning attempts, transport limitations, source ledgers and reports remain under audit/. Partial Euclidean higher-period routes are honestly labeled blocked; they are not additional universal proofs.

## Files, integrity and disclosures
The three intended uploads are original_pedal_flag.pdf, its identical standalone LaTeX source, and verification-package.zip. This archive includes manuscript source, exact metadata, portable controls and the explicit authored audit gate allowlists, including ALL18 unchanged original submission files and their custody. Historical gate/status records describe their own stages, not final publication clearance. They are preserved for accountability, including initially failed diagnostic/transport attempts and the subsequently documented repairs.

Full third-party PDFs, scans/OCR, raw API payloads, local operational caches, credentials, browser state and dependency implementations are excluded. Primary receipts retain URLs, editions and hashes. The gate allowlists exclude their own gate file from self-reference; the material MANIFEST excludes itself. The external PACKAGE_SEAL and subsequent whole-package reviews live beside this package in the repository, outside the ZIP. A hash is integrity evidence, not a signature or mathematical proof. The final PDF/ZIP and publication-operation state are outside the archive to avoid circularity.

The mathematical statement is scoped to proper noncircular confocal elliptic caustics, signed areas, side lines and least period. No nonconfocal, hyperbolic, degenerate, unsigned-face or arbitrary-padding extension follows. AI tools were used extensively in research, proofs, auditing, computation, searches and drafting. AI adversarial audits are not conventional human peer review or proof-assistant certification. Bounded priority research does not exhaust worldwide prior work.

License: CC BY4.0 for authored material. No redistribution license to excluded third-party fulltexts is asserted.
