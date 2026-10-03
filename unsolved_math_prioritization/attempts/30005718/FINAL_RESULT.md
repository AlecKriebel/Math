# Final results for matrix ultra log concavity 30005718

**Original disposition: unresolved, five of five substantive author turns used. Independent review pending.**

The exact source is Germain Poullot's Problem 6, OWR 58/2023, printed pp.3308–3309, asking whether the original polynomial V_n from the three-state matrix recursion has an ultra-log-concave coefficient sequence for every n. The normalization uses the actual degree `d_n=floor(3(n−1)/2)` and retains the leading zero coefficients. A second, qualitative question asks about tools for polynomial matrix recursions. The packet provides sufficient tools and scoped theorems, not a complete general classification or a proof for every n.

## Strongest proved claims in the packet

1. The original matrix reduces exactly to a positive two-state transfer. Its first and last nontrivial ULC inequalities hold for every n, with explicit polynomial certificates. A unipotent reversal gives polynomial formulas for fixed upper coefficients.
2. An exact positive Perron inverse-variance gap gives eventual strict original ULC on every fixed proportional interior band. The proof verifies spectral suppression and a uniform corrected saddle expansion.
3. Coefficient-marking inequalities and the bulk theorem give eventual full-row unimodality. Every fixed lower or upper ULC index is eventually strict.
4. A uniform small-saddle expansion, including two correction orders, controls the lower shrinking band. An exact parity coefficient reduction controls the upper band. Together with the bulk result, this proves: **there exists N such that every original row V_n is ULC for all n≥N**. No numerical N is supplied.
5. Exact Newton-basis certificates prove **all-size** ULC for the lower indices k=4 through 63 and the upper distances d_n−k=1 through 40, whenever these are original interior indices. Polynomial degree bounds make these finite exact certificates valid for infinitely many row sizes. A rational Sturm computation excludes the direct real-rootedness shortcut already at n=7.

The all-index finite computation through n=500 is exact evidence. It does not establish that 500 overlaps the unspecified threshold N. The Newton-certified bands have fixed cutoffs and are not an all-index theorem.

## Sharp unresolved part

An all-size proof is missing for the finite but presently unbounded set of possible exceptional rows below N. Equivalently, an effective rigorous N together with verified overlap would complete this particular route. No propagation proof for nonnegative Newton coefficients at arbitrary lower index has been obtained. The exact all-n source assertion is therefore unresolved here, despite the eventual theorem.

The five author turns are frozen without a sixth search. Earlier source, proof, check and manifest bytes are preserved. The controls total 1,508,018 exact assertions across five receipts; 25 separate 80-digit bulk diagnostics are explicitly non-interval and are not proofs. The small-saddle estimates require mathematical review independently of the algebra controls.

## Credit and reading order

Read SOURCE_GATE.md before TURN_1 through TURN_5. The gate identifies an unrelated background paragraph in the imported dataset record and fixes scope from the original EMS report. It checks the later 2025 and 2026 primary papers and records which eigenvalue, degree and fixed-coefficient facts are already in the source literature. Classical Perron, saddle-point, Newton interpolation and Sturm tools are credited as standard. Historical priority of the scoped consequences has not been certified.

The source addition records the author-linked Flajolet–Sedgewick book and the exact version/hash used. The proof supplies its own matrix-specific and endpoint uniformity arguments rather than invoking a scalar theorem with unchecked positivity hypotheses. Raw source PDFs and source-page images remain outside the public packet.
