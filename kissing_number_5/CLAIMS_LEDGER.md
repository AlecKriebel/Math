# Claims Ledger

Last updated: 2026-07-23T19:32:06Z

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
| C013 | The rational measure in `proofs/two_point_lp_barrier.md` has total mass 41, strict off-diagonal support below \(1/2\), and positive dimension-five Gegenbauer moments in every degree. | PROVED | Degrees 1--53 are exact-rationally checked; all larger degrees follow from the proved uniform integral estimate. Independent adversarial audit pending. |
| C014 | Ordinary Delsarte LP can prove \(A(5,1/2)<41\). | REFUTED | C013 is a feasible dual-cone witness, so every admissible auxiliary polynomial has \(f(1)/f_0\geq41\). |
| C015 | A symmetric matrix with positive diagonal, nonpositive off-diagonal entries, and at most one negative eigenvalue always has rank at least half its order. | REFUTED | The quadratic kernel of the exact 60-point \(D_6\) root code has order 60 and rank at most \(1+6+20=27\), while being PSD minus a rank-one matrix. |
| C016 | A fixed-\(41\) three-point distribution satisfies \(\sum_{u,v}x(u,v,t)=41x(t,t,1)\) as a measure identity. | PROVED | Direct counting of ordered triples; formulation and normalization still undergoing independent audit. |
| C017 | The fixed normalized \(D_5\) configuration cannot accept an additional point. | PROVED | For sorted \(a_1\geq a_2\) among the absolute coordinates of a unit vector, the maximum root inner product is \((a_1+a_2)/\sqrt2\geq\sqrt{2/5}>1/2\); exact proof and verifier supplied. |
| C018 | The failure to append a point to fixed \(D_5\) proves \(\tau(5)\leq40\). | REFUTED | It says nothing about moving or replacing existing points and is only a saturation statement. |
| C019 | The first construction round found a 41--44 point code at threshold \(1/2\). | REFUTED | Every numerical candidate found has maximum inner product strictly above \(1/2\); search failure is not nonexistence. |
| C020 | The quadratic kernel of every hypothetical \(N\)-point five-dimensional code has diagonal 1, nonpositive off-diagonal entries, rank at most 20, and at most one negative eigenvalue. | PROVED | Exact harmonic decomposition \(K=(4/5)H_2+G/2-(3/10)J\). |
| C021 | The properties in C020, even together with the exact entry range and a fixed-coefficient PSD-minus-rank-one decomposition, imply \(N\leq40\). | REFUTED | Exact \(\mathbb F_7^2\) graph matrix has order 49 and rank 19; a 41-principal restriction has exactly one negative eigenvalue. |
| C022 | For \(R=(4/5)H_2+G/2\), an actual five-dimensional Gram source forces top-five and top-fourteen eigenvalue sums at least \(N/2\) and \(4N/5\), respectively. | PROVED | Loewner domination plus the Ky Fan variational principle; the abstract graph counterexample fails this split-factor constraint. |
