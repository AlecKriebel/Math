# A classical Wu-manifold witness for the fixed-space free-rank question

Problem **30001522 / OWR-4413-005**, catalog rank **828**. Queue status: **claimed_solved**, **2/5** substantive approaches used.

## Accepted mathematical result

The single fixed finite complex W = SU(3)/SO(3), with the real orthogonal inclusion, is a simply connected closed smooth five-manifold, rationally equivalent to S^5. Its **actual continuous free-action ranks on W itself** satisfy:

- free toral rank = free 2-rank = 0;
- free p-rank = 1 for every odd prime p.

The fixed circle embedding diag(z,z,z^(-2)) restricts to a free cyclic action for every odd order. The circle itself is only almost free. The nonzero tangent Stiefel–Whitney number <w_2 w_3,[W]> = 1 excludes a free continuous involution via the topological covering quotient, hence excludes every positive-rank free torus action. The odd-primary upper bound uses the Borel spectral sequence. The finite diagnostics do not prove these topological or infinite-family assertions.

Read [the full proof](author/PROOF.md), [the first mathematical audit](audit/AUDIT.md), [its independent lemmas](audit/INDEPENDENT_LEMMAS.md), and [the second adversarial review](second_review/REVIEW.md).

## Review status and attribution

**Two separate AI mathematical audits accept the full literal fixed-space free-action theorem, with no mathematical corrections required.** These are AI audits only, not human peer review or formal proof-assistant certification. The author packet's pending-audit labels remain unchanged as historical statements. Subsequent acceptance is recorded separately in [first acceptance](audit/ACCEPTANCE.json) and [second acceptance](second_review/ACCEPTANCE.json).

This is a classical witness. Kuhn and Lloyd, *Chromatic fixed point theory and the Balmer spectrum for extraspecial 2-groups*, [Example 2.25](https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-kuhn-lloyd-FINAL.pdf), already record the Wu-manifold no-free-involution observation. Their surrounding admissibility hypotheses are not substituted for the covering argument covering arbitrary continuous involutions here. Debray and Yu, [*What Bordism-Theoretic Anomaly Cancellation Can Do for U*](https://doi.org/10.1007/s00220-024-04937-4), provide the classical cohomology and tangent-class computation and its historical credits. Yeroshkin, [*Orbifold biquotients of SU(3)*](https://arxiv.org/abs/1401.7565), provides circle-isotropy context. The target is Hanke's actual free-action question on [printed page 1912 of Oberwolfach Report 32/2010](https://ems.press/content/serial-article-files/46287).

No novelty, publication priority, present-day open status, or exhaustive literature search is certified. The bounded reviews neither establish nor rule out a prior explicit combination answering Hanke's question. This statement concerns the fixed space's actual free-action ranks, not almost-free or rational-homotopy toral rank.

## Frozen inputs and reproducibility

[PUBLICATION_METADATA.json](PUBLICATION_METADATA.json) pins all three unchanged ZIPs and their inner manifests. The readable author, audit, and second-review directories are byte-for-byte equivalents of those ZIP members. [PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json) binds the complete publication inventory. Obtain its SHA-256 from the trusted PR receipt before running the verifier.

From any working directory, using Python 3.10+ and its standard library:

```sh
python3 -I -B /path/to/verify_publication.py TRUSTED_MANIFEST_SHA256 --full
python3 -I -B -O /path/to/verify_publication.py TRUSTED_MANIFEST_SHA256 --full
```

The verifier checks exact files, directories, regular-file types, hashes, archive/member equivalence, and acceptance bindings before running all three packages' verified-source diagnostics and control suites. Relocation and normal/optimized damage controls are also exercised. A correctly rehashed replacement cannot authenticate itself; the external manifest/archive pin remains necessary. No network or third-party packages are used and no files are written inside the publication directory.

The additional wrapper controls can be reproduced with `python3 -I -B PUBLICATION_CONTROL_TESTS.py /path/to/publication /outside/path/results.json`. They execute pinned pristine verifier bytes against temporary damaged copies.

Optional full-corpus identity replay, with separately supplied exact corpora:

```sh
python3 -I -B /path/to/identity_recheck.py --catalog catalog.json --problems problems.json --research-results research_results.json
```

A separate publication-time full-corpus identity replay passed in normal and optimized modes; [PUBLICATION_IDENTITY_RESULTS.json](PUBLICATION_IDENTITY_RESULTS.json) contains metadata only. The first audit records its full-corpus inspection. The second review explicitly did not repeat that inspection, and its historical metadata is unchanged. The optional publication replay reports only hashes, byte counts, record counts, and match results. Source inspection records are historical; public replay does not retrieve or authenticate omitted PDFs, source extracts, or corpus contents.

Only authored mathematics/code/results, unchanged safe ZIPs, and public verification/citation metadata are included. Source documents, dataset contents, and private material are excluded. Nothing in this package constitutes a release, DOI registration, or external peer review.
