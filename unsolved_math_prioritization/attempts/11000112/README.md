# Credited prior negative answer: Problem 11000112

Rank 1012 / AMR-109-0112. Queue disposition: **already_solved, 0/5 proof-search turns**.

Baykur's published 2022 genus-three construction gives twelve positive Dehn twists whose product is the identity on the closed surface. Their integral homology quotient is Z^4, so b1=4>g=3. This refutes the proposed universal bound and is credited prior work, not a new counterexample.

Read [the unchanged authored reconstruction](author_original/packet/PROOF.md), [the independent AI mathematical audit](audit/AUDIT.md), and [the acceptance](audit/ACCEPTANCE.json). The audit checks the source hypotheses, cancellation/capping, all twelve relator abelianizations, and the integral quotient. The Hamada starting relation and Baykur's curve-to-word geometry are imported from the published construction, **not independently rebuilt**. The executable tests do not establish the mapping-class identity from diagrams. No new-result, priority, minimal-length, sharp g+1 bound, pointed-lift, formal-proof, or human-peer-review claim is made.

Primary credit: R. Inanc Baykur, *Small exotic 4-manifolds and symplectic Calabi-Yau surfaces via genus-3 pencils*, Open Book Series 5 (2022), 185–221, [doi:10.2140/obs.2022.5.185](https://doi.org/10.2140/obs.2022.5.185).

## Immutable provenance

All 13 author-freeze files and all 9 audit-delivery files are unchanged. Both exact ZIPs, original receipts and author controls are included. The historical author review-pending and no-remote-write flags remain historical snapshots; the later independent acceptance supplies the operative verdict. No correction patch was required. The historical rejected wrong-article retrieval remains metadata only, excluded from mathematical evidence.

The packet includes only authored mathematics, audit, code and public verification metadata. It contains no scholarly PDFs, source extractions, screenshots, dataset contents, private source or coordination material.

## Reproduction and trust

Use a trusted Python 3.10+ interpreter, standard library, OS and filesystem. Independently authenticate BOOTSTRAP.py against the externally published SHA-256 before executing it. The bootstrap pins the verifier and manifest; the manifest closes the payload inventory. This is an integrity boundary, not a general hostile-code sandbox. Simultaneous adversarial filesystem mutation is outside the replay model.

    python3 -I -S -B BOOTSTRAP.py
    python3 -I -S -B -O BOOTSTRAP.py
    python3 -I -S -B -OO BOOTSTRAP.py
    python3 -I -S -B TEST_MUTATIONS.py

Full replay must run as a non-root user. It copies authenticated bytes to disposable storage, genuinely makes the author freeze read-only, verifies that writes are denied, replays author and independent adversarial controls, and checks that the publication bytes did not change. The wrapper-control suite uses a separate trusted original bootstrap to reject malformed, missing, extra, forged, linked, nonregular and hostile candidate files before executing candidate code.

Default fresh source/corpus rehash, record joins, retrieval and source inspection are **NOT_RUN**. Historical reports are preserved; they are not represented as freshly rerun. Optional --source-dir expects mcgbook.pdf, baykur2022.pdf, baykur2015v2.pdf and hughes2022_wrong_article.pdf. Optional --problems and --research-results must both be supplied. These inputs are read locally and only their byte counts and SHA-256 matches are emitted. Matching the rejected wrong article never makes it evidence. No network retrieval occurs. Optional rehash does not repeat scholarly inspection or record joins.

These finite controls supplement the written mathematical audit. They are not proof-search turns, a formal topology proof, a novelty certificate, human peer review, or GitHub CI. Zero GitHub checks must not be reported as passing CI.
