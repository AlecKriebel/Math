# Referee-revision change log

**Revision base:** `04b6eb46d7fa15669f7fa353a7ced28d21d78a6a`

**Revision date:** 2026-07-29

**Mathematical scope:** unchanged. The equality theorem concerns
shared-randomness-convexified behavior sets and Bell support functions. It
does not assert equality of raw strategy images or same-state simulation.

Line numbers below refer to the revised source. Stable LaTeX labels are
included where possible because they survive later typesetting changes.

## A. Scope and literature

1. **Title changed.** `paper/main.tex:48`; synchronized in
   `submission/title_and_abstract.md:3`, `submission/arxiv_metadata.md:3`,
   `submission/journal_metadata.md:3`, `submission/cover_letter.md:5`,
   `README.md:1`, and `CITATION.cff:3`.
2. **Page-one Main Theorem added.** `paper/main.tex:80-99` states the
   arbitrary-output convexified \(2\times2\) equality, the exact \(3\times2\)
   separation using \(L_0\), and the minimum-setting conclusion.
3. **Raw sets, convex hulls, and support functions distinguished.**
   `paper/main.tex:245-357`, especially `prop:support-functions`.
4. **Historical and adjacent literature added.** Gisin, Cerf--Ollivier, and
   Panahi et al. are discussed at `paper/main.tex:118-151`; verified records
   are in `paper/references.bib`. The expanded source audit is
   `reports/priority_audit.md:9-366`.
5. **Exact limitation sentence added.** `paper/main.tex:1712-1716` states
   that all two-input linear Bell separations are ruled out only after
   shared-randomness convexification and explicitly disclaims raw-set
   equality.
6. **Vértesi--Bene comparison table added.** `paper/main.tex:196-222`.
7. **Novelty language qualified.** `paper/main.tex:144-148` and
   `reports/priority_audit.md:44-51` use “To our knowledge” and do not claim
   that the broad \(3\times2\) phenomenon is new.

## B. Abstract

- Replaced at `paper/main.tex:62-78` and synchronized at
  `submission/title_and_abstract.md:19-37` and
  `submission/arxiv_metadata.md:22-40`.
- The abstract names Vértesi--Bene, states convexified equality and the exact
  \(3\times2\) consequence, summarizes the proof mechanism, and explicitly
  disclaims raw-set and same-state equality.
- All occurrences of the line-break artifact “binary- ternary” were removed;
  the compound is typeset as `binary--ternary`.

## C. One-binary-party theorem

1. The formal pointed-cone circuit lemma is `paper/main.tex:666-700`.
2. Positive coefficients are explicitly absorbed into ray vectors at
   `paper/main.tex:672-674` and `paper/main.tex:750-752`.
3. One-versus-one, repeated-ray, zero-ray, rank-one-total, and
   lower-dimensional cases are treated at `paper/main.tex:686-699`,
   `paper/main.tex:731-739`, and `paper/main.tex:779-805`, with further
   degeneracies in `paper/appendices.tex:176-198`.
4. Canonical-purification projectors, including the transpose convention, are
   displayed at `paper/main.tex:759-778`.
5. The rank-one \(\Omega\) product-state construction is
   `paper/main.tex:779-796`.
6. The single shared variable reconstructing the complete behavior is
   explicit at `paper/main.tex:797-808`.

## D. Residual-architecture theorem

1. Extreme points of a compactly generated convex hull are handled by
   `lem:extreme-hull`, `paper/main.tex:823-835`.
2. Pure-state, extremal-measurement, and deterministic-postprocessing
   selections are separated at `paper/main.tex:889-953`.
3. Every two-dimensional real operator system containing the identity is
   shown to be commuting and a postprocessing of a binary spectral PVM at
   `paper/main.tex:925-940`.
4. The exactly-three-rank-one-effects conclusion, including deterministic and
   two-effect cases and the rank-square bound, is
   `paper/main.tex:954-970`; the support-perturbation proof is
   `paper/appendices.tex:199-218`.
5. The four selected effects are proved to form a basis of
   \(\operatorname{Herm}(2)\) at `paper/main.tex:995-1006`.

## E. Lorentz incidence model

1. The complete representation lemma is `lem:lorentz-representation`,
   `paper/main.tex:1052-1109`.
2. Determinant scaling and polarization derive the conformal-Lorentz identity
   at `paper/main.tex:1075-1091`.
3. The Pauli-coordinate trace pairing is fixed at
   `paper/main.tex:975-983`.
4. The strict residual metric and complete open physical domain are defined
   at `paper/main.tex:1035-1050`.

## F. Physical completeness

1. Smooth Lorentz Gram--Schmidt and the local negative frame are constructed
   at `paper/main.tex:1128-1145`.
2. The factor \(1/2\) in the steered coordinates is derived at
   `paper/main.tex:1152-1162`.
3. State normalization is checked at `paper/main.tex:1168-1188`.
4. Positivity, including zero joint probabilities, is explained at
   `paper/main.tex:1189-1194`.
5. The regular-level-set chart and integration of every tangent to a
   two-sided physical curve are at `paper/main.tex:1195-1206`.

## G. Strict multiplier positivity

- `lem:determinant-pullback`, `paper/main.tex:1288-1334`, defines the
  adjugate, proves \(F_j=4|\det\Xi|^2\det N_j\), differentiates the
  determinant, and derives a separate normalization multiplier for each
  input under arbitrary effect variations.
- `prop:positive-multipliers`, `paper/main.tex:1336-1392`, supplies
  complementary slackness, multiplier uniqueness, identification with the
  finite POVM dual, \(\lambda_j\ge0\), the explicit local hidden-variable
  construction when \(\lambda_j=0\), and strict positivity at a strict
  separator.
- The finite-dimensional dual-attainment details are
  `paper/appendices.tex:220-269`.

## H. Second variation

1. The first-order tangent equation is derived at
   `paper/main.tex:1420-1439`.
2. Fredholm compatibility is derived at `paper/main.tex:1439-1448`.
3. Independence and \(\dim\mathcal H_K=16-k\) are proved at
   `paper/main.tex:1449-1462`.
4. The identity direction, \(q(I)=0\), normalization shift, and invariance of
   \(q\) are `paper/main.tex:1486-1507`.
5. The exact inertia \((4,12)\) remains at `paper/main.tex:1476-1485`; the
   square completion is expanded in `paper/appendices.tex:271-306`.

## I. Projective-fiber theorem

- Target coordinates were renamed to
  \(\xi_0,\ldots,\xi_3\) at `paper/appendices.tex:308-329`.
- Generic inversion, all scale choices, direct and cross branches, both
  resultants, strict-metric coefficient exclusions, and every exceptional
  intersection are explicit at `paper/appendices.tex:330-538`.
- Each resultant is followed by the argument yielding at most one nonbase
  preimage.

## J. Rank-zero simulation

1. Partition preservation and the common scale are proved from the unique
   circuit kernel at `paper/main.tex:1580-1601`.
2. \(a_i,b_i,c_{ij}\) are defined as Bell-table entries and \(q_{ii}=0\) is
   imposed at `paper/main.tex:1610-1630`.
3. The deterministic branch table is `paper/main.tex:1631-1642`.
4. Reconstruction of the ternary--ternary, both mixed, and binary--binary
   blocks is checked at `paper/main.tex:1643-1657`.
5. The bounded-transportation interval proof remains
   `paper/appendices.tex:540-587`.

## K. Exact \(3\times2\) separation

1. The main theorem now uses
   \(L_0=20\sqrt2+16/25\): `paper/main.tex:443-458`.
2. \(L_1=(16+8\sqrt{7813})/25\) is a separate attained-lower-bound
   proposition, with no global-optimality claim:
   `paper/appendices.tex:87-173`.
3. All six ternary-PVM supports are tabulated at
   `paper/main.tex:629-647`.
4. Both CHSH-deficit inequalities are derived at
   `paper/main.tex:548-592`.
5. The common-label embedding is identified with the heterogeneous
   \((2,2,3)\)-by-\((2,2)\) architecture at
   `paper/main.tex:421-426`.
6. Positivity and normalization of the simple POVM are checked separately at
   `paper/main.tex:474-491`.

## L. Notation and exposition

- State matrix \(C\) was renamed \(\Xi\); the Bell matrix was renamed
  \(\mathsf B_c\); the stability constant is \(\kappa\); metric variations
  use dotted lower-case coordinates; and fiber target coordinates use
  \(\xi_i\).
- A notation table is `paper/main.tex:367-406`.
- The input-count convention for “\(3\times2\)” is stated at
  `paper/main.tex:101-103`.
- Raw-set equality, same-state simulation, exact-global-optimum claims, and
  private-randomness conclusions remain explicitly excluded at
  `paper/main.tex:1703-1723`.

## M. Reproducibility package

1. `run_all.sh` executes every exact verifier and checks all eight immutable
   artifact hashes.
2. `paper/build.sh:7-24` builds both PDFs and fails on reference, citation,
   UTF-8, overfull/underfull, or other LaTeX warnings.
3. `paper/review.tex` and `paper/review.pdf` supply the line-numbered review
   version.
4. `review_packet/theorem_to_artifact_map.md` separates manuscript proofs,
   exact symbolic checks, regression checks, and examples.
5. Repository CI is `.github/workflows/qubit-povm-pvm.yml`.
6. Python 3.14.6 is pinned in `.python-version`; SymPy 1.14.0 is pinned in
   `requirements.txt`.
7. `submission/arxiv_source.tar.gz` is regenerated from the revised source.
8. `SHA256SUMS.txt` is regenerated only after the complete package is frozen.
9. `CITATION.cff` points to immutable release tag
   `qubit-povm-pvm-minimum-settings-v1.1.0`.
10. The baseline commit is preserved; this revision is a new commit.

## Disclosure revision

The AI-use disclosure was revised for accuracy without itemizing private
workflow details. It states substantive use across exploration, derivation,
proof analysis, software, literature support, and manuscript preparation;
human-directed scope; author responsibility; independent checkability; and
the absence of prior independent expert verification. See
`paper/main.tex:1752-1762` and
`submission/submission_statements.md:24-41`.

## Blocking issues

None found in the internal mathematical and exact-artifact audits. The work
has not yet received independent expert peer review, and the priority claim
remains deliberately qualified.
