# Provenance of the proof-only edition

## Mathematical content and source dependence

The edition addresses the rank-one equilibrium-uniqueness question in Bernhard von Stengel's *Algorithms for Rank-1 Bimatrix Games*, Oberwolfach Reports 38/2018, printed p. 2332. Rank means rank(A+B); the decision concerns equilibrium strategy pairs, not merely payoffs. The source record is historical and is not evidence of the problem's current literature status.

The complete hardness reduction is supplied in PROOF.md. The complete rational-certificate argument is supplied in certificates/LEMMA_REPORT.md. The full independent audit and its later hash-specific acceptance are retained in independent_audit/. ACCEPTANCE.md binds these exact bytes and explains which decision supersedes which earlier qualification.

The parametric-flow construction is credited to Yann Disser and Martin Skutella. Their selected SSP/parametric-flow arc-use statement is not silently strengthened into an all-optimal-flows assertion: the present proof supplies the source-comparison-preserving perturbation and the residual-cycle uniqueness argument required for that step. The game/parameter-family correspondence is established rank-one game theory and is also proved directly in the manuscript. ATTRIBUTION.md records these dependencies and the bounded later-literature review.

## Exact preservation and editorial records

PROOF.md, certificates/LEMMA_REPORT.md, independent_audit/AUDIT.md and independent_audit/FINAL_ACCEPTANCE.md are preserved byte-for-byte from their reviewed versions. Their complete mathematical derivations, original headers, historical finite-check discussions, qualifications and conclusions remain intact. No proof step has been shortened or replaced by a checksum, summary or computational test.

README.md, ACCEPTANCE.md, STATUS.json and this document are new edition-level explanations. SOURCE_PROVENANCE.json selects public bibliographic facts, raw public PDF identities, public retrieval/inspection history and bounded search limits. Local storage paths, extracted-text identities and private coordination are omitted from that metadata. The manifest lists the edition's actual files and hashes every member except itself, preventing a circular self-hash.

The original proof's candidate label and the audit's initial conditional verdict are historical, not current blockers. The later final acceptance is tied to the unchanged proof hash. The certificate report's membership-only conclusion retains its own original scope; its argument is combined with the subsequent hardness proof at the edition level.

## Supplementary computational history

The written proof and audit refer to historical exact-arithmetic checks. The full audit prose records the six original full-game checks, 39 network checks and four additional cases. These are a historical supplementary record, not a machine-checkable deliverable in this edition and not a proof of the general theorem. Auxiliary script, fixture, result and log filenames are retained as ordinary references in the frozen authored documents, but none of those artifacts is supplied here. The previous authored draft is likewise omitted; the full audit records its identity and the complete final manuscript is supplied.

## Publication boundary and limits

Only the members named in MANIFEST.json belong to this edition. It contains no executable code, standalone computational fixtures, separate computational outputs or logs, copied third-party PDFs, extracted source text, HTML or images, dataset contents, derived source-text fingerprints, private sources, private storage paths or private coordination files. Public source titles, URLs, raw PDF byte counts and hashes, and inspection history are metadata only; the external source documents themselves are not reproduced.

No QUEUE.md or unrelated file change is proposed. Byte-identity checks and clean additive-patch replay establish packaging integrity only. They do not prove the theorem. The review is AI mathematical and source auditing, not human peer review, journal acceptance, or formal proof-assistant certification. The bounded literature review does not establish novelty, priority, or exhaustive current-open status.
