# Claims Ledger

Last updated: 2026-07-23T18:39:53Z

Allowed labels are `PROVED`, `COMPUTATIONALLY CERTIFIED`,
`NUMERICAL EVIDENCE ONLY`, `CONJECTURAL`, and `REFUTED`.

| ID | Claim | Status | Evidence / caveat |
|---|---|---|---|
| C001 | The exact \(D_5\) certificate contains 40 distinct vectors \(r/\sqrt2\in S^4\). | COMPUTATIONALLY CERTIFIED | Exact standard-library verifier; also proved by support/sign counting. |
| C002 | All distinct pairs in the \(D_5\) certificate have inner product at most \(1/2\). | COMPUTATIONALLY CERTIFIED | Exact integer dot products satisfy \(r\cdot s\leq1\); human proof in `proofs/lower_bound_d5.md`. |
| C003 | \(\tau(5)\geq40\). | PROVED | C001--C002. |
| C004 | \(\tau(5)\leq44\). | PROVED | Imported published baseline from Mittelmann--Vallentin (2010), assumed as baseline by the task; standalone certificate not yet reconstructed here. |
| C005 | A size-\(N\) code exists iff there is a symmetric \(G\succeq0\) with diagonal 1, off-diagonal entries at most \(1/2\), and rank at most 5. | PROVED | Gram factorization / spectral theorem; write-up pending. |
| C006 | A hypothetical 41-point Gram matrix has nullity at least 36. | PROVED | Rank-nullity from C005. |
| C007 | \(\tau(5)=40\). | CONJECTURAL | No universal exclusion of 41 points yet. |
| C008 | Some configuration of 41--44 points exists. | CONJECTURAL | Unrestricted construction search active; no feasible certificate. |
| C009 | Every extremal 40-point configuration is isometric to \(D_5\). | REFUTED | At least \(D_5,L_5,Q_5,R_5\) are pairwise non-isometric. |
| C010 | Every extremal configuration is antipodal. | REFUTED | Known 40-point examples are non-antipodal. |
| C011 | A floating-point SDP objective below 41 proves \(\tau(5)\leq40\). | REFUTED | Dual feasibility, PSD, polynomial-domain signs, and rounding all require rigorous certification. |
| C012 | It is safe to omit `rank(G)<=5` in the Gram formulation. | REFUTED | The resulting elliptope relaxation contains Gram matrices of arbitrarily larger rank. |
