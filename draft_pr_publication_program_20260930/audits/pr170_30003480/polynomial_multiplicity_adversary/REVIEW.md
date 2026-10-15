# Independent adversarial review: exact polynomial multiplicity route

Verdict: **VERIFIED for the stated full claim**. For every integer n>=3, no real polynomial in the determinant coordinates alone cuts out the real binary tensor Gram locus of the closed Frobenius unit ball by a single condition P>=0 inside either C_n or H_n. No mathematical gap was found in this proof. This is an automated independent mathematical audit; no claim of novelty, priority, or human peer review is made.

The substantive first reconstruction was sealed before scientific comparison. FIRST_MATHEMATICAL_ASSESSMENT.md is mode 0444, SHA256 cf3d4cf7c428c1b70f84312ba3f6a3f56ad090b85be4aa28a2495210663fddc4; its separate seal was created at 2026-10-12T11:45:36.477337+00:00. Only the two permitted frozen submission files had been read at the initial gate. No author review/verifier/results, other agents' scientific notes, PR commentary, or operational conclusions were read.

## Strongest verified result and mechanism

The independent DERIVATION.md supplies a proof for arbitrary real polynomials and all integers n>=3. The actual three-mode boundary plane has an exact odd multiplicity in the pulled-back polynomial. The determinant-coordinate involution preserves exact multiplicity and transfers the plane factor to an interior feasible plane, where a nonzero residual factor forces even multiplicity. Both chosen local crossings lie strictly in the cube and in H_3. Exact rank-one removal and addition of real unit-vector factors transfers the contradiction through the closed determinant-zero face for every larger n.

The essential prerequisites were independently reconstructed: normalized marginal-eigenvalue polygon necessity; the monotone-ratio argument making that condition necessary for every squared norm s<=1; and the even-parity real norm-one three-mode construction giving sufficiency. The proof does not depend on the printed secondary inequalities of Seigal's Theorem 1.4 or on finite tensor sampling.

## Adversarial findings

- **Exactness:** divisibility alone is insufficient. The quotient after the exact maximal power is not identically zero on the plane; consequently every open plane patch has a point with nonzero residual. The involution preserves maximal multiplicity, not just a lower bound.
- **Nonzero polynomial:** the explicit infeasible point (55/256,28/256,28/256) lies strictly inside H_3. A zero polynomial F or zero higher-factor face restriction would incorrectly include it.
- **Domain crossings:** the true-boundary determinant margins are 2bc, 2c(1-b-c), 2b(1-b-c). On the reflected sum-one plane they are 2t_jt_k. Positive margins and interior coordinates justify full local neighborhoods in both domains.
- **Normalization:** using trace one directly for a tensor of norm below one would leave a gap. The ratio proof supplies the correct implication; zero determinants, zero tensor, maximal determinant, and the minimum permissible trace are explicitly covered.
- **Involution scope:** reflection is an algebraic action; it need not map the original boundary patch into the chosen interior patch or preserve the half-cube D.
- **All-n transfer:** zero Gram determinant implies rank-one real flattening; the unit factor preserves norm and every remaining Gram matrix. The iteration proves exact equality of slices, including the zero tensor.
- **Threshold and scope:** n=1 and n=2 admit the displayed single-polynomial descriptions. The all-n extension uses the closed zero-determinant face and makes no claim for a punctured higher-mode domain, auxiliary variables, several inequalities, or different tensor normalization.

## Retained checks

The original author checker was not read. The independently written audit_checker.py uses exact rational arithmetic and a small sparse polynomial implementation from Python's standard library. Both ordinary execution and Python -O passed the same 18 positive checks and rejected all 12 negative mutations. A 125-point rational eigenvalue grid includes zeros and one-half endpoints; 65 of those points satisfy the triangle conditions. Symbolic identities and exact multiplicities are retained, as are rational local crossings and real unit-factor embeddings from three through six modes.

The negative mutations alter the determinant coordinate map, parity support weights, affine reflection, exact exponent, residual nonvanishing, odd interior sign, even boundary sign, H margin, zero restriction, unit-factor normalization, trace-ratio direction, and determinant-only invariance. All failures use explicit exceptions. These checks survive optimization and are supplementary to the universal proof; finite checks are not presented as proving all-polynomial or all-n assertions.

## Primary-source interpretation

[Seigal's published paper](https://seigal.github.io/seigal2018gram.pdf), printed pages 352–354, defines the closed tensor unit ball, gives the determinant-polygon convex hull, and states Conjecture 1.5 within the determinant cube. The [OWR report](https://ems.press/content/serial-article-files/46684), printed page 1226, uses the same norm-ball locus and points to that conjecture. [Higuchi–Sudbery–Szulc](https://arxiv.org/pdf/quant-ph/0209085v2), PDF pages 2–3, proves the normalized polygon condition and explicitly constructs a real three-mode realization. The audit inspected rendered relevant pages and independently downloaded each PDF; all three source hashes match the frozen manifest.

## Exact remaining gap

None for the all-polynomial nonexistence theorem in the two stated closed domains. This family did not independently adjudicate the separate four-factor numerical formula counterexample, the secondary printed characterization issue, historical priority, or publication readiness of unrelated claims. Those are not premises of the verified theorem.

## Retention and publication

PUBLICATION_WHITELIST.json explicitly lists only this audit's own publishable outputs. Downloaded source bodies, extracted text, and page renders under private_sources/ are private. INVENTORY.json lists every retained regular file with byte count, SHA256, mode, and publication eligibility, excluding only itself to avoid a self-hash cycle. Its final SHA256 is pinned in the completion message. No outside individual was contacted and no Git/index/branch/ref/checkout or remote mutation was performed.
