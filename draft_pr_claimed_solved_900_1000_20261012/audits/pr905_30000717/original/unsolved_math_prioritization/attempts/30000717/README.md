# Robinson obstruction to ideal-only certificates

Problem 30000717 / OWR-1465-011, rank 963. Disposition: claimed_solved, 1/5 substantive proof-attempt turns, by a complete negative answer to the specified four-way equivalence.

The classical Robinson sextic is globally nonnegative, yet R+epsilon is not a finite sum of real polynomial squares modulo even the full real vanishing ideal, for every epsilon >= 0. This holds for both the catalogue tangency-minor ideal and the explicitly defined literal separate-product ideal. Thus conditions (iii) and (iv) fail. The separate nonattaining Q example refutes (ii) => (i) only for the product reading; the tangency reading retains (i) iff (ii).

Read [the frozen proof](author/PROOF.md) and [source assessment](author/SOURCE_ASSESSMENT.md). The source formula discrepancy is preserved, not silently repaired. The Robinson form, Schur nonnegativity and ten-zero cubic obstruction retain their classical credit. No historical novelty or exhaustive literature claim is made.

## Review record

- [Audit A](audit_a/report/AUDIT.md), [constant-perturbation supplement](audit_a/report/EPSILON_SUPPLEMENT.md), and [frozen-v2 acceptance](audit_a/report/FROZEN_ACCEPTANCE.md)
- [Audit B](audit_b/AUDIT_REPORT.md) and [correction log](audit_b/CORRECTION_LOG.md)

Audit A first checked the exact-only argument and developed the epsilon strengthening. The author checked and integrated it into v2. Audit B independently checked the entire frozen v2 without consulting Audit A. Both accept v2 unchanged. The author and audit files are preserved byte-for-byte, including historical author STATUS.json fields saying review/publication were pending and Audit A's exact-check output saying the finite controls alone give no epsilon conclusion. The final review and publication disposition is recorded here and in PUBLICATION_STATUS.json. The universal epsilon argument is in the written proofs, not in finite arithmetic controls.

## Reproduce

Requires Python 3 and SymPy 1.14.0. Obtain the trusted PUBLIC_MANIFEST.json SHA256 from the draft PR description. From any working directory, run:

    python /path/to/packet/verify_publication.py --expected-manifest TRUSTED_SHA256
    python /path/to/packet/mutation_tests.py --expected-manifest TRUSTED_SHA256

The verifier checks the exact file set, SHA256 hashes, byte counts, embedded frozen acceptance anchors and nested manifests before replaying in an isolated temporary copy. It reruns 185 author assertions, Audit A's independent exact controls, and Audit B's 51 controls, requiring byte-identical saved outputs. No source PDF, source corpus, network, numerical solver, or original workspace is required. It leaves the frozen originals untouched. The guard remains active under Python optimization, and replay children explicitly run without optimization. The manifest's external hash is essential; a newly computed hash from an untrusted download is not a trust anchor.

Mutation tests reject changed or missing listed files, an altered manifest, an unlisted file and a symlink. They test artifact integrity, not the truth of arbitrary mathematical claims.

## Limits and source boundary

This is AI-assisted, unrefereed mathematics with independent AI-assisted audits. It is not formal proof certification or conventional human peer review. Exact checks supplement the universal argument. No primary-source PDFs, renders, extracts, datasets, catalogue record contents or private coordination files are distributed. Public citations and verification metadata are included. This draft does not merge or release the result.
