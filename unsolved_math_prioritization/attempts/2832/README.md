# KP-3.34: audited Heegaard stabilization partials

Problem **2832 / KP-3.34**, rank **912**, remains **unsolved**, with **4/5** substantive approaches recorded. The accepted corrected derivative preserves all four structural proofs and adds the missing initial-genus-at-least-2 hypothesis in its attribution of Johnson's flip theorem.

## Accepted scope

- Exact absolute-genus tower truncation and the equal-genus deficit law.
- Strong triangle inequality and the fixed-genus ultrametric.
- Reduction to possibly unequal-genus unstabilized cores; a smallest counterexample has at least one unstabilized input.
- Equivalence between common genus at most H and a finite stabilization path staying below height H.

These reductions do not prove the universal final-genus-at-most-2g bound or produce a counterexample. There is no novelty, formal proof, finite-computation proof, exhaustive literature coverage, or human peer-review claim. Ordered ambient isotopy, unordered equivalence and equivalence by arbitrary homeomorphism are kept distinct. P[h] denotes absolute final genus, not h added handles.

Read the [corrected proof](independent_audit/corrected/proof.md), [approach log](independent_audit/corrected/approach_log.md), [full analytic audit](independent_audit/audit/audit_report.md), [actual patch](independent_audit/audit/correction.patch), and [exact acceptance](exact_acceptance/acceptance_report.md). The [acceptance JSON](exact_acceptance/acceptance_report.json) binds its decision to exact bytes. The [original packet](independent_audit/author_original/) and all four ZIPs are preserved unchanged. Historical pending-audit and not-published statements describe the frozen stages; [publication metadata](PUBLICATION_METADATA.json) gives this checkpoint's disposition.

## Verification boundaries

All four ZIPs, their external manifests, every member, the acceptance binding and the actual zero-fuzz patch replay are checked. The publication wrapper is static integrity and file-derivation validation. The six-file original and corrected packets contain no executable checks. Running the wrapper does not independently prove the four mathematical propositions or the conjecture.

Full retained corpus hashes, exact record/report identity and four locally retained PDF pins were replayed. Only public hashes, sizes and match results are included. No copied source PDFs, extracts, dataset contents, exact record text or private coordination files are published. This publication replay is not a new literature search or source inspection. Source inspection was bounded, and the cited literature's full proofs were not independently certified. The 2011 upper-bound manuscript's observed arXiv status is not a publication or correctness certification.

## Reproduce

Python 3.10+ with the standard library and the system patch utility. Independently authenticate PUBLICATION_MANIFEST.json and the wrapper before execution. A verifier cannot authenticate its own malicious replacement. The external manifest hash is stated in the PR description.

    python3 -B verify_publication.py . --manifest-sha256 HASH
    python3 -B -O verify_publication.py . --manifest-sha256 HASH

Both modes enforce explicit fail-closed guards, exact inventories, original/corrected/audit/acceptance equality and fresh patch derivation. Negative controls are listed in PUBLICATION_TEST_RESULTS.json. Optional paired --base-queue and --queue paths verify that only this row's Status and Turns changed. Optional --catalog, --problems, --research-reports and --source-dir paths rehash the private inputs without publishing them. The source directory contains k3.pdf, johnson_upper.pdf, hass_thompson_thurston.pdf and johnson_flipping.pdf.

Only the target queue row's Status and Turns change; Findings and all unrelated queue bytes are preserved. Local checks are separate from remote CI. This is a draft research PR, with no merge, auto-merge, release, DOI or external outreach.
