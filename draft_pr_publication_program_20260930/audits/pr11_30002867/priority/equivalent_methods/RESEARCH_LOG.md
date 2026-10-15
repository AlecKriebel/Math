# PR11 independent equivalent-methods priority audit

Scope: independently test earlier methods equivalent to the global affine matrix-characterization question, without reading the exact-question priority family's verdict. No outreach, canonical edits, Git operations, or publication in this family.

## 2026-10-01 05:15 UTC — initial mechanism checkpoint (35%)

- Read `source_snapshot/CANDIDATE.md` first. The target is finite positive colength in `C[x_1,...,x_d]`, regular multiplication representation, global generation by `d` polynomials.
- Read Kreuzer–Long–Robbiano arXiv:1903.09563v2, especially Definition 3.1, Propositions 3.2–3.3, Algorithms 3.4 and 3.6, Proposition 3.7, Remark 5.6, and its bibliography.
- Exact earlier mechanism established independently: reconstruct a finite polynomial presentation from the faithful matrix algebra `C[M_1,...,M_d]`; apply Algorithm 3.6 to every local factor; use Mohan Kumar's 1978 stable-range theorem to equate local complete intersection with global `d`-generation in this zero-dimensional polynomial-ring setting. This is an explicit, finite matrix-derived characterization even though it may construct a border basis and primary decomposition.
- Also identified a direct matrix/table version of Wiebe's criterion: recover local multiplication table, present the maximal ideal using a vector-space basis of the kernel of multiplication by shifted coordinates, and test nonzero maximal minors in the local finite algebra. It avoids reconstructing local polynomial generators, but needs a checked proof and examples.
- No conclusion yet about an earlier identical block-rank formula. Such a formula is not necessary for an equivalent-method priority obstruction.
- Next: validate the reconstruction, local/global distinction, earlier Kähler-different sources (2015 dissertation, 2017 article), journal/version history, and independent operator/Koszul bibliography.

## 2026-10-01 05:25 UTC — original-source and computational checkpoint (75%)

- Independently established and checked a direct matrix-only Wiebe criterion, without recovering a cyclic vector, polynomial ideal, or primary decomposition. It uses the matrix algebra basis, a coefficient-kernel basis, and determinant matrices. The full proof is being recorded separately.
- Exact standard-library rational computation passed eight cases after simultaneous similarity changes: univariate, nonreduced rectangular CI, square-zero non-CI, curved `C[t]/(t^4)` embedding, Gorenstein non-CI, three reduced supports, mixed multiple support, and multiple nonreduced CI factors. All prior-Wiebe Boolean results agree with the candidate's local Koszul rank predicate. Border recovery also returned a divisor-closed monomial basis and relations annihilating the original matrices.
- Retrieved Wiebe's original 1969 article through GDZ and independently inspected its printed p. 260, Satz 3. This verifies the Fitting criterion in the original source, rather than relying on its later restatements.
- Independently inspected Mohan Kumar's original printed p. 234. Theorem 4 is the direct local-to-global bridge: locally CI polynomial ideals require at most the ambient number of generators. Height then gives precisely `d` for the target. Theorem 5 also verifies the stronger minimum-generator formula in the candidate's stable range.
- KLR arXiv v1 already contains Algorithms 3.4 and 3.6. The university-hosted journal PDF is a seven-page extract omitting the central Section 3; do not cite nonexistent verified journal-page locators for those algorithms. Original arXiv v1/v2 provide the full checked text.
- The 2015 dissertation and 2016-online/2017 journal article concern projective/homogeneous coordinate data; do not misidentify those results as an exact affine criterion. The 2020 border-scheme paper's complete-intersection locus is the strict locus.
- A scoped adversarial response verified the polynomial-reconstruction/local-to-global mechanism and identified the requirement that the monomial enumeration use a multiplicative order. The implemented order is graded lex, which satisfies it. A second direct-matrix presentation check was sent for adversarial scrutiny.
- Provisional priority assessment: `already_solved_by_equivalent_methods` for the characterization task; not a located earlier identical block-rank formula. Remaining work is source/query manifest, bounded-search limits, and final proof/readability review.

## 2026-10-01 05:38 UTC — final family checkpoint (100%)

- Completed `CHECKABLE_MAPPING.md`, `REPORT.md`, `SOURCES.md`, `SEARCH_MANIFEST.md`, and structured `verdict.json`. Durable records contain own proofs and concise source/query summaries; primary fulltexts and foreign metadata remain under ignored temporary storage.
- Original Wiebe Satz 3 and Mohan Kumar Theorem 4 give a complete, direct matrix characterization of exactly the original global finite-colength ideal property. KLR Algorithm 3.6 and Remark 5.6(e) give independent algorithmic adapters after exact border reconstruction. All methods preserve nonreduced factors and multiple support.
- Re-inspected original Mohan Kumar printed p. 234 visually. The direct source URL was independently downloaded into this family's temporary directory and matched the earlier primary copy byte-for-byte. Verified publication metadata from the original publishers/arXiv.
- Root independently read the full direct-matrix Fitting mapping and found it sound; a fresh final disposition adversary is being assigned separately by root. This family does not claim that later review is finished.
- Completed the 42-query equivalent-method record, chronological version dates, precise arXiv/original printed page locators, and explicit fulltext/access limitations. An earlier identical `D_2` display was not located; absence was not proved.
- Final disposition is `already_solved` by verified equivalent methods / known reformulation. Reject a first-resolution or still-open-question advertisement. A narrow explicit Koszul-rank reformulation with complete classical attribution remains possible; algorithmic superiority is unestablished.
- Eight exact rational computational cases pass. Work scope complete, with no canonical edits, Git action, publication, or outreach.

## 2026-10-01 05:40 UTC — bibliographic repair and freeze (100%)

- Root identified an incorrect workshop title in S01. Rechecked the original cover and corrected it to *Multivariate Splines and Algebraic Geometry*, with workshop dates 19–25 April 2015. This did not affect the checked question or theorem locators.
- Root's independent rerun of all eight exact translation cases also passed. Family artifacts are frozen for fresh final acceptance review; any subsequent adversarial correction will receive a new checkpoint.
