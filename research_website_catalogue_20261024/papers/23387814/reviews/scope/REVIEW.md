# Source and scope review — Zenodo 23387814

Disposition: **PASS_SCOPE_ONLY**. The published source identity, reader-file coverage, target formulation, attribution interfaces and proposed editorial scope are mapped. This is not a mathematical PASS, permission to publish, conventional peer review, a successful scientific-code replay, or historical-priority clearance. Independent mathematical reviews and the root decision remain separate.

## Source identity and coverage

The official record is *A Minimal-Surface Counterexample to a Seshadri Lower Bound*, Alec Kriebel, independent researcher, ORCID 0009-0001-9320-500X, DOI [10.5281/zenodo.23387814](https://doi.org/10.5281/zenodo.23387814). The record identifies version **1.0**, publication date **14 October 2026**, and preprint/CC-BY-4.0 status. The PDF prints 14 October 2026, with no printed version number. Record creation on 15 October is upload metadata, not a replacement publication date. No identity mismatch was found.

Both public assets were freshly downloaded through the official Zenodo API and checked against its declared sizes and MD5s. SHA256 bindings are:

| Asset | Bytes | SHA256 |
|---|---:|---|
| `seshadri_counterexample.pdf` | 71,160 | `8f50f329fac5b30ffea3d98f82e36ec71af0d3d5df44e38a21f992eb45aa4c48` |
| `verification_package.zip` | 197,194 | `6af7c815f863d44ba4b24708d5ae70bec4d5e0fd55789114083a605c08a27a20` |

The ZIP has 102 regular files. Extraction checked member paths, duplicates, file types, size limits and CRCs. Final read-only revalidation found all 102 extracted payloads byte-identical to their ZIP entries and all 101 outer-manifest payload hashes matching. These are integrity checks, not authentication of authorship or proof correctness.

There is exactly one reader PDF: the five-page standalone manuscript. The ZIP contains no reader PDF and no nested archive. See `sources/reader-pdf-map.json`. The complete PDF text, complete corresponding TeX and the original author mathematical `PROOF.md` were read. PDF page 1 was also visually inspected for title, date, complete abstract, target denominator and Theorem 1. The main source is `sources/published-source/seshadri_counterexample_verification/seshadri_counterexample.tex`.

The whole sole abstract, TeX lines 19–27, is preserved in `abstract.tex`, normalized in `abstract.txt`, and included without omission in `candidate-content.json`. Normalization changes whitespace and seven math expressions only; its reproducible receipt is `abstract-receipt.json`. It includes the classical-ingredients, priority and AI/human-review qualifications. The normalized text has 97 whitespace-separated tokens; that count is a notation-dependent convenience, not a semantic measure.

## Exact claim and construction interface

Theorem 1 asserts that for **every integer d ≥ 7** there exist a **smooth integral complex projective surface S**, an **ample integral line bundle L**, and a **closed point x**, with **K_S ample**, satisfying

`K_S² = 6(d−1)(d−3), L² = 6, ε(S,L;x) ≤ 1/(d−1) < 1/(2+(K_S²)^(1/4)).`

The Seshadri constant is the infimum of `L·C / mult_x C` over integral curves through x. The point is special. The surface varies with d. Minimal means no smooth rational (−1)-curve, not a surface that minimizes area in differential geometry. Ample canonical bundle is stronger than the asserted minimal-general-type consequence.

The manuscript’s proof obligations, mapped without substituting a numerical test for geometry, are:

| Location | Submitted mathematical mechanism | Essential qualification |
|---|---|---|
| PDF p.2; TeX 69–108 | An explicit degree-d plane curve has an ordinary (d−1)-fold point. A dimension argument plus Bertini chooses a second member so that every pencil member is integral and reduced and there are d² simple base points. | The second member is a nonempty-open existence choice, not an exhibited polynomial with all coefficients. The high-multiplicity point is away from the base points. |
| PDF p.2; TeX 110–120 | On the blowup Y, the fibre F is nef and E₁ is a section. `A=2F+E₁` has square 3 and positive intersection with every integral curve. | Integrality/reducedness of **every** fibre supports the vertical-curve case. Checking only the listed intersection numbers is insufficient. |
| PDF pp.2–3; TeX 122–169 | A double base change is branched at four distinct smooth fibres, avoiding the selected singular fibre. It yields a connected smooth integral projective S with `K_S=π*(K_Y+2F)`. | Branching away from singular fibres is material. Connectedness and smoothness of the fibre product are stated; no hidden resolution is part of the construction. |
| PDF p.3; TeX 152–169 | `N=K_Y+2F=(d−3)H+F` has positive square and positive degree on every curve for d≥4; Nakai–Moishezon and finite pullback give K_S ample. | This is an all-curve ampleness argument. It establishes minimality through adjunction, rather than assuming the original blowup is minimal. |
| PDF pp.3–4; TeX 171–198 | The unbranched selected fibre splits into two isomorphic copies. On either chosen copy, degree 1 and multiplicity d−1 give the upper bound. | One uses a degree-one lift, not the whole degree-two preimage as a connected curve. The strict comparison is asserted for d≥7. |

At d=7 the claimed witness has K_S²=144, L²=6, curve L-degree 1 and point multiplicity 6. This is a family of special-point **upper bounds**, not an exact-value theorem. The manuscript expressly excludes inferences about one fixed surface, very-general points, Picard-rank-one bounds, canonical/adjoint polarization bounds, and an optimal smallest d or smallest canonical square among all counterexamples. For d=4,5,6 only the displayed curve’s failure to produce the strict comparison is stated.

No scope contradiction was found in these formulations. That observation does not independently certify the whole construction; that is the mathematical review gate.

## Primary-source interfaces and attribution

Fresh primary files and their URL/hash receipts are in `cache/primary-sources` and `primary-source-receipts.json`; exact reading extents and exclusions are in `primary-reading-map.json`. Reference PDFs are ignored caches, while receipts and notes are retained.

1. **The target is correctly delimited.** [Szemberg, arXiv:0711.0584v1](https://arxiv.org/abs/0711.0584v1), final question p.7, was read and visually inspected. Although that paper’s main theorem concerns Picard number 1, its final challenge is broader. [Oberwolfach Report 21/2009](https://ems.press/journals/owr/articles/3471), printed p.1124, Conjecture 2, was also read and visually inspected: it explicitly says arbitrary Picard number and arbitrary point. In both, the additive2 is **outside** the fourth root. [Primer v2](https://arxiv.org/abs/0810.0728v2), Question 6.1.6 p.17, confirms the same minimal-surface formulation. The immediately adjacent very-general-point discussion is a distinct statement.
2. **The small-quotient pencil is classical.** [Ein–Lazarsfeld1993](https://numdam.org/item/AST_1993__218__177_0/), Example 3.1 p.182, explicitly credits Miranda. [Bauer1999, cited arXiv edition](https://arxiv.org/abs/math/9903072v1), Proposition 3.3 and its proof, gives the blowup construction and an asymptotic degree choice. The submitted note supplies its own finite-degree argument and does not validly obtain d=7 merely by citing that asymptotic statement. [Bauer–Szemberg2010 v1](https://arxiv.org/abs/1011.0979v1), Proposition 2.1 p.2, gives the same section-plus-two-fibres polarization and arbitrary positive rational values on a blowup. These sources support the required classical attribution, not a firstness claim for the present minimal-surface application.
3. **The cover formula is classical.** [Fuentes García, v2](https://arxiv.org/abs/math/0511547v2), §2 p.3, assumes a smooth reduced branch divisor `B∼nM` and records `K_X=π*(K_Y+(n−1)M)`. With n=2 and M=2F this is the exact formula used in the note. Its separate Picard-rank-one/very-general-point and ramification-point Seshadri theorems are not being applied to the chosen unbranched singular fibre.
4. **Nearby examples are not the same assertion.** [Bauer–Szemberg, surfaces of general type v1](https://arxiv.org/abs/0801.3245v1), Example 1.3, was read in full: its curve has canonical degree 1 and multiplicity2, giving a quotient 1/2 for the canonical polarization. This displayed quotient is not a counterexample to the proposed smaller bound. Ein–Lazarsfeld’s Example 3.7 statement concerns unbounded very-ampleness indices, not this specific minimal-surface estimate.
5. **Other classical inputs are mapped, not recertified here.** Bertini/transversality, Bézout, blowup intersection theory, Nakai–Moishezon, Riemann–Hurwitz, finite pullback of ampleness, the projection formula and adjunction are identified at their uses. This scope review does not independently re-prove these theorems or replace the mathematical reviewers’ assessment of their application.

Reading was targeted; none of the above establishes exhaustive priority clearance. Full final journal versions were not globally compared. The publisher metadata and exposed snippets for Bansal–Majumder2025 were inspected, but its full body and the Roy2019 thesis were not read. Focused searches did not supply a basis for claiming that the exact problem was still open immediately before the note. No such claim is proposed. Search snippets from nonprimary sites were not relied on as mathematical evidence.

## Package and independence boundaries

The fresh package’s `run_all.py`, `JOBS.json` and `requirements.txt` were inspected to map reproducibility: the driver expects SymPy 1.14.0 and mpmath 1.3.0, assertions enabled, inventories verified, and nine jobs in disposable copies. It compares complete recorded JSON outputs. **No scientific job, full launcher, original independent checker or nested replay was run by this scope role.** No saved historical success is counted as a fresh reproduction. Only the independent source-byte and outer-manifest checks described above were performed.

No current sibling report or dedicated historical REPORT/VERDICT/priority-audit body was opened. There was incidental historical assessment exposure: the official record description and required manuscript §5 describe old internal AI/priority reviews; the author `PROOF.md` has a candidate-status preface. `ROOT_EARLY_PROOF.md` was opened as mathematical support and proved to be an old root verification note whose assessment was visible. This exposure is disclosed, and its verdict is not adopted as evidence. The present scope disposition rests on the actual published text, fresh source identity and the primary passages above. Mathematical independence and clearance are supplied by the separately assigned reviewers, not asserted here.

## Editorial candidate and remaining gates

`candidate-content.json` preserves the exact title, full abstract, record date/version, two asset names and hashes. It proposes the plain slug `minimal-surface-seshadri-counterexample`, an explanatory description, the all-d≥7 scope, the L²=6 feature, the d=7 witness, classical credit, clear special-point/varying-surface limits and explicit unrefereed/AI status. The collaboration invitation is professional and passive; no outreach was initiated or drafted to any individual.

`follow_up` is null. No extension was established here as both substantial and genuinely unresolved. Routine variants, unmotivated exact-value requests or numerical optimization would not meet the user’s high bar.

**Strongest verified result of this role:** the fresh two-asset publication is completely inventoried and bound; its exact target matches the independently inspected primary formulations; the proposed page scope and complete abstract accurately represent that version with appropriate attribution and limitations.

**Exact remaining gap:** independent mathematical approval of the universal geometric construction and any desired submitted-checker reproduction, followed by root editorial/publication clearance. Historical firstness and independently verified immediately-prior openness remain unestablished. Nothing in this scope review warrants repairing the source, publishing the candidate, or treating source integrity as proof validity.
