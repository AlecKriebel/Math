# Distinct progression differences: verified prior partial resolution

**Problem 2487 / EP-1097, rank 904. Queue: unsolved, 0/5.**

The uniform O(n^(3/2)) subquestion is false by prior work. The main optimal-exponent and full-order question remains unresolved in the inspected sources. This is an authored exposition and audit of known mathematics, with no novelty, new solution, or improved bound claimed.

## Accepted scope

The [original proof](author_original/PROOF.md) and [full independent audit](independent_audit/AUDIT.md) give the exact integer comparisons F(n) <= M(n) and M(N) <= F(3N)+1. The classical Ruzsa digit construction has n = 2^(k+1)-1 and at least 3^k-1 nonzero signed progression differences, disproving a uniform three-halves bound. Positive differences change only a factor two.

The stronger interval 1.77898 < gamma <= 11/6 is theorem-dependent: [Lemm, Theorem 2.1](https://arxiv.org/pdf/1404.3745v2) and [Katz-Tao, Theorem 1.1](https://arxiv.org/pdf/math/9906097v3), with the audited integer and tensor transfers. No decimal optimizer certification, extra endpoint digits, exact endpoint big-O estimate, exact n^gamma growth law, or full literature census is claimed. Tracker access limits remain explicit in the frozen source records.

The [exact acceptance](independent_audit/ACCEPTANCE.json) accepts the six-file author archive unchanged. No mathematical correction or derivative was required. Both original ZIPs, both external manifests, and all 13 extracted members are byte-preserved. Historical pending-audit and no-publication fields describe their freeze stages and have not been rewritten.

## Reproduction

From this folder, run `python -I -S -B verify_publication.py` and `python -I -S -B -O verify_publication.py`. These check the publication inventory, immutable archives and members, internal manifest and exact acceptance bindings, and conservative scope flags. `test_publication.py` exercises relocation and corruption controls under both modes.

Supply `--catalog`, `--problems`, `--reports`, and `--pdf-directory` together to either program to replay the frozen audit against all three complete nonbundled corpus files and all four pinned nonbundled PDFs. The audit verifies exact record/report identity, 128 forward subsets, 512 reverse graphs, and seed depths 1 through 6. Supply `--queue-base` and `--queue-current` together to the verifier for byte-exact validation of the one-row queue change. Omitted external inputs are explicitly reported as skipped. Programs use explicit fail-closed checks, including under Python optimization, and make no network requests.

Integrity checks and bounded examples are not formal proof verification or a new mathematical approach. All-n arguments are in the authored proof and audit. Publication replay does not repeat the source-theorem inspection or retrieve fresh literature. `PUBLICATION_TEST_RESULTS.json` records the actual local test scope. Remote CI is reported separately; zero checks does not mean CI passed.

No raw corpus contents, source PDFs, extracts, rendered pages, private sources or coordination files are included. The existing queue is preserved except for this target's Status and Findings; Turns remains 0/5. This is a draft publication only, with no merge, auto-merge, release, DOI or outreach.
