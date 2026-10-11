# Independent audit: row 1683 / problem 30004269

Date: 2026-10-11 UTC.

## Acceptance decision

**Accept the narrow printed-formula defect. Do not classify the intended conjecture as solved or refuted.** The candidate's (n=2) obstruction is correct. The official PDF visibly has the strict range (1<k\leq j<n), and the actual rank-one Newton-Okounkov body is a bounded interval. No supplementary bound in the inspected source context rescues the literal list.

Three refinements are required in any downstream account:

1. There are **two** independent superscript/subscript transcription errors in the corpus, affecting the weight vector and the padding rule.
2. The interval \([0,1]\) uses a normalizing section nonvanishing at the valuation point. Other choices translate it, which does not affect the unboundedness contradiction.
3. The general Minkowski-sum description is stated in a preliminary preprint; the later push-pull preprint discusses a future completion and develops a specific five-dimensional example. Neither is a checked proof of a repaired full Dyck-path inequality system.

The standalone proof is in `NARROW_PROOF.md`. It does not depend on the general Minkowski-sum result.

## A. Evidence and inspected scope

- **OWR 46/2019:** The complete Kiritchenko contribution, printed pp. 2893-2896 (PDF pp. 25-28), was read. Printed p. 2895 was independently rendered and visually inspected, including a high-resolution crop of Conjecture 1. A fresh download is byte-identical to the supplied source. [Official PDF](https://ems.press/content/serial-article-files/46825).
- **Kiritchenko 2017/2018 preprint:** Relevant definitions and statements in arXiv:1801.00334v1, pp. 1-8, were read; pp. 6-7 were visually inspected for notation. The new download matches the supplied bytes. [Version-pinned record](https://arxiv.org/abs/1801.00334v1).
- **Kiritchenko push-pull preprint:** arXiv:2012.15690v1, Sections 5.1-5.2 and especially pp. 12-14, was read; p. 12 was visually inspected. Fresh bytes match the supplied source. [Version-pinned record](https://arxiv.org/abs/2012.15690v1).
- **Flag-variety convention:** The author-hosted manuscript of *Newton-Okounkov polytopes of flag varieties*, Section 2.1/Theorem 2.1 and the FFLV definition, was read. The publisher confirms Transformation Groups 22 (2017), 387-402, online 16 March 2016. This is distinct from the Bott-Samelson preprint. [Author-hosted manuscript](https://publications.hse.ru/pubs/share/folder/x7xo3qyrfo/175928464.pdf), [publisher](https://doi.org/10.1007/s00031-016-9372-y).
- **Line-bundle degree:** Brion's notes, Sections 1.4.3-1.4.4, printed/PDF pp. 16-17, were read. [arXiv version](https://arxiv.org/abs/math/0410240v1).

These are targeted statement/convention and low-rank proof checks, not complete independent audits of every theorem in the cited papers.

## B. Exact notation audit

Use upper indices for the stage of the weight and the row of a coordinate, as the printed source does.

| Item | Official OWR p. 2895 | Corpus | Assessment |
|---|---|---|---|
| Stage-(i) weight | \(\Lambda_i=(\lambda_i^i,\ldots,\lambda_n^i)\) | \(\Lambda_i=(\lambda_i^i,\ldots,\lambda_i^n)\) | Corpus fixes the wrong index. |
| Padding for (j>i) | \(\lambda_i^j=\lambda_j^j\) | \(\lambda_j^i=\lambda_j^j\) | Corpus swaps the two indices on the left. |
| Coordinate | \(u_m^l\) | \(u_{lm}\) | Harmless only if explicitly defined as (u_{lm}:=u_m^l). |
| Endpoint | \(u_j^i\) | \(u_{ij}\) | Consistent with that explicit flattening. |
| Range | \(1<k\leq j<n\), \(1\leq i\leq n-j\) | Same strict lower bound | Genuine source-level defect; not introduced by corpus cleanup. |
| Bound | \(\sum_{s=1}^{j}(\lambda_k^s-\lambda_{i+j}^s)\) | Same upper/lower pattern | Prevents treating the other two transpositions as a consistent global renaming. |

The official padding rule has a clear role: the weight at stage (s) initially has entries only with lower index at least (s); it fills an entry \(\lambda_k^s\) when (k<s) by \(\lambda_s^s\). The corpus rule, left unchanged alongside the displayed right-hand side, does not perform that padding.

The report imports dominant weights and line bundles from Ki18. For a reconstructed self-contained statement, the weights should be integral and weakly decreasing within each stage. In Ki18, (G=GL_n), so (n=2) has root system (A_1), one simple reflection, and one coordinate. The (n=2) in the preceding OWR Example 1 denotes the ambient dimension of its input trapezoid in the general convex-geometric construction. That example produces a three-dimensional polytope in type (A_2); it is separately scoped and does not redefine the (n) imported for Conjecture 1.

The corpus record for problem 30004269 was checked directly against the full supplied problems dataset. The record matches exactly; the two transpositions are already in that record. The supplied inputs were unchanged.

## C. Could omitted conditions rescue the literal (n=2) formula?

**No, within the stated source formulation.**

- The source states a defining inequality list: nonnegativity plus the indexed path inequalities. The full contribution supplies no additional rank-one boundary inequalities and no restriction (n\geq3) or (n\geq4).
- The triangular FFLV display locates coordinates and path labels. A table does not independently impose numerical upper bounds.
- Ki18 defines ordinary FFLV polytopes with their own path bounds. Those define the proposed Minkowski summands, not an unstated additional list of inequalities imposed on the claimed sum in OWR Conjecture 1. Importing them would change the literal assertion being audited.
- For (n=2), no path in the quantified family exists because there is no admissible pair ((k,j)). Whether one includes endpoint labels in a path or which edge convention is used therefore cannot change the empty-family argument.
- Adding constant coordinates to a dominant (GL_2) weight leaves its ordinary line-bundle degree (a-b) unchanged. The test weight ((1,0)) is strictly dominant and its line bundle is very ample, so the countercheck does not exploit a non-big or borderline polarization.
- Changing the valuation normalization or reversing a coordinate cannot change boundedness.

Calling the intended object a polytope cannot serve as an unstated inequality. An unbounded intersection of the actual displayed half-spaces simply fails to be that object.

## D. Literature status and the intended corrected scope

### D1. Established flag-variety input

Kiritchenko's published flag-variety theorem identifies the relevant lowest-term Newton-Okounkov bodies on (GL_n/B_n) with ordinary FFLV polytopes. This uses dominant weights with entries decreasing from left to right and bounds of the form \(\lambda_i-\lambda_j\) for (i<j). The rank-one computation in `NARROW_PROOF.md` is compatible with that convention and is proved directly, so it does not need to assume the full theorem.

### D2. What arXiv:1801.00334v1 states, and what it does not provide

The arXiv record was checked live on 2026-10-11. It lists only v1, submitted 31 December 2017, and describes it as a preliminary version. Theorem 1.1 states Minkowski additivity for semiample line bundles for the specified Bott-Samelson word and valuation; Theorem 3.1 expresses the bodies as nested FFLV Minkowski sums. Immediately after Theorem 3.1, p. 6 explicitly identifies an inequality description for those sums as a further task.

It is therefore wrong to infer that Theorem 3.1 already proves the OWR all-path inequality list. Equality to a Minkowski sum and an explicit description of that sum by a particular half-space family are different statements. This audit has not independently reconstructed the omitted general combinatorial argument in Lemma 3.4 or all external ingredients of the Minkowski-sum proof. It records the theorem as stated rather than granting a new proof certification.

### D3. What the later push-pull paper establishes in the inspected version

The [publisher record](https://doi.org/10.1093/imrn/rnab331) confirms IMRN 2023(4), 3305-3328, published online 7 December 2021. The publisher PDF request returned HTTP 403, while the web tool returned the purchase/abstract page. The complete version of record was therefore **not inspected**; its detailed content must not be silently equated with the available preprint.

The accessible arXiv:2012.15690v1 has only its 31 December 2020 submission listed. Section 5.2 discusses a future direct completion of Ki18 and works through (R_{(1,2,1,3,2)}) in type (A_3). It gives a five-dimensional family with 16 inequalities and Proposition 5.3 comparing its Minkowski-sum volume polynomial with the corresponding intersection numbers. That is useful, specific progress. It is not a stated proof there of the repaired OWR formula for every (n).

The word “complete” in the later preprint does not by itself prove the earlier result false; nor does the earlier theorem label remove the need to verify the later explicit-formula claim. Both facts should be preserved without inventing a retraction or a general resolution.

### D4. Contemporary search check

A targeted primary-source search through 2026-10-11 found no verified later theorem establishing a repaired full OWR Dyck-path description. The following newer Kiritchenko works were distinguished from this problem:

- [*Simple geometric mitosis*, arXiv:2301.00225v1](https://arxiv.org/abs/2301.00225v1): its abstract, introduction and a full-text search for relevant terms were inspected. It constructs operations on faces, with type (A/C) Gelfand-Zetlin applications; it is not a resolution of the OWR inequality list in the inspected version.
- [*Valuations on polyhedra and topological arrangements*, arXiv:2601.03176v1](https://arxiv.org/abs/2601.03176v1), and [*Polynomial valuations on plane polygons*, arXiv:2606.19986v1](https://arxiv.org/abs/2606.19986v1): primary abstract and version records only were checked. Their stated subjects concern polyhedral valuations and scissors congruence, not the OWR Bott-Samelson inequality problem. No claim about uninspected full proofs is made.

This is a bounded literature search, not proof that no relevant result exists anywhere. The defensible conclusion is **general repaired formula unverified in this audit**, rather than a newly certified global “open” status.

## E. Exact remaining mathematical gap

The complete remaining task is to supply a precise corrected family of path inequalities, including boundary cases and the stage-weight indexing, and prove that its solution set equals the relevant nested Minkowski sum of FFLV polytopes and hence the Newton-Okounkov body under an adequately justified geometric identification.

At minimum this requires:

1. A fully specified admissible path family, endpoints and coordinate embedding of every smaller FFLV summand.
2. Validity of all proposed bounds on every Minkowski summand and on the sum.
3. The reverse inclusion: every point satisfying the proposed inequalities admits a sum decomposition, or an equally strong general separation/volume argument.
4. Compatibility with all dominant integral stage weights, including zero gaps, and with the source's fixed word and valuation.
5. Explicit checks that recover \([0,a-b]\) at (n=2) and the known low-dimensional examples without relying on OCR or inconsistent index/sign conventions.

The missing (k=1) inequality repairs the present one-dimensional test. This audit does not show it is the only repair required in higher rank.

## F. Reproducibility and exclusions

Public-source hashes, lengths, retrieval outcomes and inspected locations are recorded in `SOURCE_MANIFEST.json`; aggregate verification and public-dataset pins are recorded in `CHECK_RESULTS.json` and `INPUT_VERIFICATION.json`. The integrity and exact rank-one checks were rerun successfully in three interpreter modes. Their finite monomial sanity checks are not a substitute for the universal proof.

This packet distributes the authored narrow proof, mathematical audit and acceptance, together with public-source and aggregate verification metadata. Source PDFs, extracted source text, screenshots, dataset contents and executable verification tools are excluded.
