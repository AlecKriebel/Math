# Boundary fixed points in rank-zero Hénon components

Problem 5300080 / AMR-052-0080; rank 793.

**UNSOLVED. Five of five substantive approaches used. Zero original solution credit.** The independent AI-assisted audit passes the scoped partial results and requires no mathematical correction. This is not human peer review, formal proof certification, a novelty claim, or a determination of worldwide open status.

## Exact scope

The historical target assumes that **one subsequence** converges locally uniformly to a finite boundary point. It does not assume full convergence or that every limit map has rank zero. The desired eigenvalue is 1 for the same chosen return map.

The packet retains fixedness, strict dissipation, boundary sink exclusion, conditional full-convergence arguments, and a carefully scoped stable-curve obstruction. Lyubich–Peters' full-convergence theorem and small-Jacobian classification are credited prior work. Saddle returns do not imply convergence. The stable-curve argument explicitly assumes a holomorphic lift. Its Wiman growth threshold is strictly below 1/2; the endpoint subharmonic example is not a Hénon counterexample.

Arbitrary dissipative Jacobian with mixed-rank limits and unbounded excursions remains unresolved. The author stopped after the five-route budget; publication and validation add no proof-attempt route.

## Preserved history

Read `author/PROOF.md`, `author/APPROACHES.md`, `independent_audit/AUDIT.md`, and `independent_audit/CORRECTIONS.md`. Both frozen directories and both original archives are preserved byte for byte. Earlier statements such as “independent review pending” and “no remote writes” describe their historical research stages. The accompanying audit and this publication addendum supply the later status without silently changing those records.

The source PDF hashes in the records concern complete cached bytes. Publication replay does not claim fresh live downloads or new scholarly inspection. Source PDFs, extracts, screenshots, raw corpora, copied records, and private coordination are excluded. Missing source inputs are not reported as successfully checked.

## Reproduce

Python 3, standard library only:

    python3 -B verify_publication.py --expected-manifest-sha256 <digest from PR description>
    python3 -O -B verify_publication.py --expected-manifest-sha256 <same digest>
    python3 -B test_publication_integrity.py

The wrapper requires an external manifest digest, checks every recursive file and directory, verifies both archive identities and their exact equality with the expanded frozen files, then runs the audit. The audit replays 14,006 author assertions in normal, optimized, and relocated optimized configurations, rejects 14 package mutations, and runs 42,428 independently implemented finite assertions. These computations do not certify the analytic theorems. `test_publication_integrity.py` also tests the publication wrapper's rejection behavior in disposable copies.

To recheck provenance against separately available sources, use the audit's documented optional PDF and full-corpus inputs. No source inputs are needed for the portable replay. A source-free replay explicitly reports those provenance checks as not run.

Only this attempt directory and the selected queue row's Status and Turns cells are changed. Findings, other rows, and the preexisting stale queue header are preserved exactly. This is a draft-PR checkpoint, not a merge, release, DOI deposit, or external outreach.
