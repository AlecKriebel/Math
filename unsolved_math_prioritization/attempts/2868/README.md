# Kirby 3.70: surgery-generation partials

ID 2868, rank 915. Canonical status: **unsolved**, 3/5 approaches. Mathematical disposition: **stalled_partial**. Independent verdict: **ACCEPT_UNCHANGED_STALLED_PARTIAL**.

The unrestricted smooth integral homology cobordism generation question is unresolved by this work. The original report isolates three gaps: properness at every fixed genus does not establish properness of the union; the cited NST non-single-surgery examples satisfy [Y_k] = -2*A_1 + A_(k+1) for k > 0 and lie in G_2 (genus < 2); an ordinary one-two-handle trace has absolute H_2 = Z and is not a homology cobordism. These are credited deductions, with no novelty claim.

- [Original report](author/REPORT.md) and [approach log](author/ATTEMPT_LOG.md)
- [Independent audit](independent_audit/AUDIT_REPORT.md)
- [Exact acceptance](exact_acceptance/ACCEPTANCE.json)
- [Publication metadata](PUBLICATION_METADATA.json), [input replay](PUBLICATION_INPUT_REPLAY.json), and [test results](PUBLICATION_TEST_RESULTS.json)

All three frozen ZIPs and their externally anchored manifests are preserved in archives/. Extracted files match their archive members exactly. The original author STATUS.json still says the audit was pending and publication had not occurred at the author freeze; those are historical fields, preserved unchanged. Publication metadata supplies the later status. Audit/acceptance statements that no repository mutation occurred refer to their own earlier stages.

Run `python3 -B verify_publication.py --expected-manifest-sha256 TRUSTED_HASH --self-test` from this directory, then repeat with `python3 -B -O`. Use an independently supplied hash of PUBLICATION_MANIFEST.json, never a hash recomputed from an untrusted replacement as an authentication claim. The wrapper pins all frozen artifacts, checks exact member sets and acceptance bindings, and replays the audit, its four author modes, and independent controls.

Optional `--full-inputs CATALOG PROBLEMS REPORTS --source-dir SOURCE_DIRECTORY` performs a fresh local rehash of all three complete corpora and the k3.pdf, hhl.pdf, nst.pdf source files. Optional `--base-queue BASE --queue NEW` verifies that only this row's Status and Turns changed. Inputs are intentionally not distributed. Without optional inputs, the replay explicitly reports NOT_REQUESTED. Finite tests establish artifact integrity, not a mathematical proof.

No copied source PDFs/text/images, datasets, private sources, or private coordination files are included. No formal certification, human peer review, full solution/refutation, or exhaustive literature/novelty finding is claimed. The intended publication is an open draft PR, not a merge, release, DOI, or outreach.
