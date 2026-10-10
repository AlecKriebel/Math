# Local-knot genus in orientable three-manifolds: accepted partial results

Problem **30004818 / OWR-8415345-008**, queue rank **944**. Publication package prepared 7 October 2026.

**Current disposition: independently accepted partial results; full problem unresolved; five of five author approaches completed. Queue status: `unsolved`, turns `5/5`.** The independent mathematical assessments are AI-assisted, source-scoped reviews. There is no claim of novelty, human peer review, or machine-checked formal verification.

The target asks whether a classical knot K, placed in a ball in an orientable smooth three-manifold M, can bound a compact connected orientable smooth surface in M × I of genus strictly less than its ordinary smooth four-genus. No such example and no universal equality theorem is established here.

## Accepted scope

1. **Finite-image stable bound.** If the surface has genus g and its fundamental-group image has finite order d, a connected lifted surface has d boundary components and genus 1 + d(g − 1). The boundary-band construction proves g₄(#ᵈK) ≤ dg and hence g_st(K) ≤ g. This does not imply equality with ordinary four-genus without an additional sharpness hypothesis.
2. **Abelian-image hyperbolic obstruction.** An abelian-image surface in a complete orientable hyperbolic three-manifold gives an ordinary four-ball surface of the same genus. In particular, genus-one savings are impossible in those products. No general nonabelian-image extension is claimed.
3. **Conditional companion criterion.** The specified disjoint two-component companion-link concordance would give a genus-at-most-one surface. An absorbing annulus with r spectator intersections only yields genus at most 1 + r. Neither the required disjoint concordance nor a sufficient equivariant surface has been constructed.
4. **Relative and intersection obstructions.** The integral local-boundary relative class vanishes, including when H₁(M) has torsion, and the absolute product intersection form vanishes. The capped absolute class need not vanish. Only the stated closed-dual and intersecting-tori transplantations are excluded.
5. **Concordance norm and Floer bound.** A single-surface strip construction proves the stated definite integer-valued concordance norm properties. Relative adjunction, local filtration normalization, nonzero Floer classes and conjugate Spinᶜ structures give |τ(K)| ≤ g_{M×I}(K) for all closed connected oriented M. The compactness/doubling reduction extends the obstruction to the orientable existential setting. The capped class is retained until its Chern pairing cancels.

Miller's order-two family with arbitrarily large ordinary four-genus survives these bounds as a test family. It is not an orientable-product counterexample. The exact remaining gap is the existence or exclusion of a genus-saving product surface outside the retained obstructions.

## Read the proofs and reviews

- [Five frozen original proofs and author reports](local_knot_genus_30004818/authored/)
- [Full independent mathematical audit](local_knot_genus_audit/MATHEMATICAL_AUDIT.md)
- [Acceptance report](local_knot_genus_audit/ACCEPTANCE_REPORT.md)
- [Detailed Floer/Miller source audit](local_knot_genus_audit/floer/FLOER_AND_MILLER_AUDIT.md)
- [Optional clarification patch](local_knot_genus_audit/OPTIONAL_CLARIFICATIONS.diff)
- [Two clarified reading copies](clarified/local_knot_genus_30004818/authored/), obtained by applying that exact patch

All frozen author files and audit files are preserved byte for byte. In particular, the author's original completion report and manifest retain their pre-review status, and the early source report retains its one-approach snapshot. Historical `publication_performed: false`, `queue_modified: false`, and pending-review labels record their preparation state, not this publication's current disposition. This cover and the acceptance report state the current accepted scope. The clarified copies make only the already-audited editorial/citation changes and do not replace the original accepted inputs.

The acceptance report SHA-256 is `6972cbca8d53737613854c6d4bb3d55caad2ba3958dd2cdcb54ebf11b71bd2a1`.

## Source-free verification

From this directory run:

```sh
python3 verify_public_package.py
```

This separately named Python standard-library checker verifies the exact public file inventory and SHA-256/byte counts, frozen author/audit pins, exact patch application to the two clarified copies, and the finite arithmetic checks: 601 covering cases, 23 equivariant records, 1,001 smoothing cases, 40,401 norm triangle inequalities, and 2,001 determinant cases. It neither downloads sources nor checks their contents. These are integrity and arithmetic checks, not proof certification.

`PUBLICATION_MANIFEST.json` pins the published files other than itself. Its external Git blob/commit identity anchors that manifest. `PORTABLE_CHECK_RESULTS.json` records the expected source-free check result; the checker compares its independently computed result to that record.

**Historical checker limitation:** `local_knot_genus_audit/verify_audit.py` is retained unchanged solely as historical evidence. It requires the omitted raw PDFs, saved text extractions and the `pdftotext` executable. It is deliberately not the public entry point and cannot pass using this source-free package alone. The historical reports and `source_reextraction_checks.json` record checks performed during the audit; the new checker does not replay, sanitize, rebind, or replace that acceptance or claim to reverify those source-dependent checks.

Only authored mathematical material, public scholarly citations, and permitted verification metadata are included. No source PDFs, extracted source text, screenshots, source datasets, private sources, personal information, or private coordination files are included. Source filenames and hashes in historical manifests identify omitted inputs; they do not indicate included source files.

## Primary source boundary

The original target is Ruppik's contribution to [Oberwolfach Report 42/2021](https://doi.org/10.4171/owr/2021/42), pp. 2358–2360. The source audit identifies [Park–Wu–Yang's March 2026 preprint](https://arxiv.org/abs/2603.18619) as explicitly stating the full question as open while proving a restricted theorem. The retained source reports document the bounded literature checks and distinguish product collars from other fillings. Search non-detection does not establish that no later solution exists.
