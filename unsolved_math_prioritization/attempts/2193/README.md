# Erdős Problem 584: scoped prior obstruction and independent audit

**ID 2193 / EP-584, rank 898. Queue: unsolved, 0/5.**

The literal unrestricted H2 density-power assertion is refuted by a previously documented high-girth obstruction; consequently the joint unrestricted H1/H2 assertion fails. The intended sparsity-qualified internal strong-C6 problem remains unresolved by this work. This is a scope and attribution audit, not a new mathematical discovery.

Read [the accepted scope](accepted_author/PROOF_SCOPE.md), [independent audit](independent_audit/INDEPENDENT_AUDIT.md), and [exact acceptance](exact_acceptance/EXACT_ACCEPTANCE.md). The [actual clarification patch](independent_audit/CLARIFICATIONS.patch) reproduces all five accepted files from the preserved original. Only three of those files change. All four frozen archives, manifests, and the independent receipt are preserved byte for byte, including nested archive copies.

## Mathematical boundary

Lazebnik–Ustimenko–Woldar, Proposition 2.1(i),(iii), supplies D(5,q), with n=2q^5, m=q^6 and girth at least 10. With delta=m/n^2, delta^2*n^2=q^2/4 tends to infinity but every qualifying H2 has at most one edge, even with ambient witnesses. This is the same obstruction credited to the publicly accessible ULAM note bearing the printed date April 21, 2026. The original online publication date is not independently archived here.

This family gives delta^3*n^2=1/(16q^2), so it does not refute H1 alone. It does not refute fixed-density statements with density-dependent n-thresholds. Fox–Sudakov's small-exponent qualifications are retained. The June 2026 Eric Li manuscript and ULAM Proposition 4 are not certified. The named published girth theorem is an external dependency; its proof is not reproduced.

The inherited full background is retained in the scope analysis, although dataset contents are excluded from publication. Both live problem pages failed retrieval in the recorded audit; no current live status, exhaustive novelty search, human peer review, or proof-assistant certificate is claimed.

## Reproduction and limitations

Run `python -I -S -B verify_publication.py` here. Optimized mode `python -I -S -B -O verify_publication.py` performs the same explicit checks. Optional `--catalog`, `--problems`, `--reports` and `--sources-directory` accept the nonbundled complete corpus files and source PDFs. Omitting them explicitly skips those input checks. No downloads or uploads occur.

The new publication verifier checks immutable pins, exact archive and loose-member inventories, nested equality, acceptance/receipt bindings, exact patch replay and arithmetic consistency. It does not modify or supersede the accepted audit. The historical `independent_audit/replay_audit.py` uses assertions: its optimized execution is NONVALIDATING because Python disables those assertions. Its unchanged normal execution is recorded separately. The publication verifier does not trust that historical program's exit status or success flags.

[Publication tests](PUBLICATION_TEST_RESULTS.json) record normal, optimized, relocated and corruption controls, including complete-corpus and five-source-PDF hash verification. These are integrity and finite arithmetic checks, not a machine proof of the infinite-family theorem. [Manifest](PUBLICATION_MANIFEST.json) binds the complete public package. Historical no-publication and pending-review fields describe their original freeze stages; the independent acceptance and this publication wrapper are subsequent records.

Only this queue row's Status and Findings cells change; Turns remains 0/5. All unrelated bytes, notes, chat links and DOI cells are preserved. Draft PR only: no merge, auto-merge, release, DOI, or outreach. CI status is reported separately after publication.
