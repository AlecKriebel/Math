# Boundary frequency gap: accepted sharp cone theorem and realization partials

Problem **30005990 / OWR-14298587-002**, rank 958. **UNSOLVED, 5/5 substantive approaches.**

The accepted result proves the sharp half-space cone threshold 5/2, equality classification tY, cone-class attainment, and the universal spectral lower bound under the cited source hypotheses. Four additional realization approaches establish scoped results and obstructions. Actual attainment by a bounded-domain global spectral-sum optimizer remains unproved.

Start with [Acceptance and exact scope](ACCEPTANCE.md). Read the two manuscripts in [reading/PROOF.md](reading/PROOF.md) and [reading/REALIZATION_APPROACHES.md](reading/REALIZATION_APPROACHES.md), or inspect the byte-identical reviewed originals in author/. The reading copies apply only the two optional clarifications recorded in audit B.

## Independent reviews

- Audit A: [sharp lift theorem](audit_a/INDEPENDENT_AUDIT.md) and [four realization routes](audit_a/REALIZATION_AUDIT.md).
- Audit B: [full second independent audit](audit_b/reports/AUDIT.md), [verdict](audit_b/reports/VERDICT.json), and [optional patch](audit_b/reports/OPTIONAL_CLARIFICATIONS.patch).

Both accept the original manuscripts without mandatory mathematical corrections. This is unrefereed research with extensive AI assistance. Finite controls do not replace the analytic proofs or imported theorems.

## Portable verification

The author and audit A controls use the Python standard library. Audit B additionally uses numpy 2.3.5, sympy 1.14.0, and mpmath 1.3.0; replay/requirements.txt records the tested environment. Exact numerical output replay is version-sensitive. Verification makes no network calls, installs no packages, and does not read source PDFs or datasets.

Obtain the PUBLIC_MANIFEST.json SHA-256 from the draft PR description or a separately trusted record, then run from any directory:

    python3 -I -B /path/to/30005990/verify_publication.py --manifest-sha256 TRUSTED_SHA256
    python3 -I -O -B /path/to/30005990/verify_publication.py --manifest-sha256 TRUSTED_SHA256
    python3 -I -B /path/to/30005990/mutation_tests.py --manifest-sha256 TRUSTED_SHA256

The external anchor is required: deriving it from the copy under test would not authenticate that copy. The outer verifier checks exact file/directory membership, rejects symlinks, pins all bytes, checks nested manifests and the author archive, verifies the optional patch produces the reading copies, and replays all three independent control sets. Author controls report 19,141 exact predicates. Audit A checks exact algebra and tree interpolation. Audit B reports 16 grouped symbolic/numerical controls. Both ordinary and optimized Python modes are exercised, with explicit guards in the portable adapter.

Original audit B code is preserved in audit_b/checks/. Its original layout and result-writing behavior are recreated only in a disposable source-free temporary directory for its ordinary-mode replay. replay/audit_b_controls.py changes only path resolution, disables result-file writing, and converts four Python assert statements to explicit RuntimeError guards so optimized Python cannot suppress them. replay/AUDIT_B_PORTABILITY.patch records every adapter change. No mathematical formulas or thresholds change. Original and adapted ordinary runs must exactly match the frozen results, and the adapted optimized run must match too.

Mutation tests attack mathematical text, each audit, results, manifests, archives, reading copies, missing/extra files and directories, symlinks, coherent rehashing, false solved status, path traversal, and duplicate inventory entries. They use independent retained anchors and test rejection under normal and optimized Python. These are integrity controls, not new proof-attempt turns.

## Provenance and exclusions

AUTHOR_FREEZE.zip is the original 32,339-byte, 14-file author freeze: SHA-256 c7a113b0dd87bad1e80995cf8d5d6660f13097595987e5720ec30f1dd10c1196. Its manifest SHA-256 is 0fd5ecb3dac1b270540014c9a3b7de0c043cb0b63ba5ec3930eb5b278f15661c. All audit reports, manifests, checks, results, and optional patches are retained unchanged. The outer manifest inventories the publication files.

Only authored mathematics, audits, checks, and public verification metadata are included. Third-party source PDFs, text extracts, renderings, dataset records, and private coordination files are excluded. Source-hash records describe historical inspected bytes; offline replay does not repeat the historical literature retrievals. See author/SOURCE_AUDIT.md, the two audit manifests, and FRESH_GATE.json.
