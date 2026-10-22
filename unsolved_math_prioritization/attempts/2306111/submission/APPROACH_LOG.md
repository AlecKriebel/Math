# Five-route research log

Problem 2306111; 2026-10-04 UTC. Author: Alec Kriebel.

The routes below were developed with some overlap, then written out in one self-contained proof artifact. They count as five substantive approach turns. Literature retrieval and tool calls do not add turns. No complete candidate was found, so no post-budget proof search is authorized by this log.

## Source gate (09:53–09:56 UTC; not a proof turn)

Started from the exact catalogue URL, which returned 403. Inspected the complete 2018 primary-source statement and Update 6.111, including a rendered page. Recovered the pinned corpus and prior report with matching repository-manifest hashes. Prior work is only OPEN-TRIAGE and offers no proof to extend. Live queue shows 0/5; exact-ID branch, PR, directory and code checks found no existing attempt. The known parameter assumptions leave exactly -1<=B<-(2+sqrt(3))/4 and B<A<-B. A relevant 2020 article was found but full text was not obtained; its consequences are unverified.

## Turn 1: derivative distortion and convex-domain integration

- Mechanism: integrate the Janowski lower real-part bound for the logarithmic derivative, then compare g' with f'.
- Artifact: FULL_PROOF.md, Proposition 1.
- Result: every g in the proposed coefficient ball is globally univalent for every parameter pair; Re(g'/f')>0.
- Exact gap: close-to-convexity and univalence do not supply Re(zg'/g)>0.
- Disposition: proved partial theorem, not a resolution.
- Completion estimate for the full target: 10% (subjective; not a probability or a solved fraction).

## Turn 2: dual functionals and exact operator norms

- Mechanism: express starlikeness as exclusion of a real pencil of linear functionals, compute each functional's exact weighted coefficient norm, and optimize a 2 by 2 Gram matrix.
- Artifact: FULL_PROOF.md, Proposition 2 and equations (5)–(9).
- Result: the complete question reduces exactly to sigma_f(z)>delta|z|. A single quadratic coefficient perturbation witnesses any failure.
- Exact gap: no uniform control of the off-diagonal Gram term Im(f' conjugate(f/z)) has been proved at the requested radius.
- Disposition: rigorous reduction; the central inequality is explicitly left unsupported.
- Completion estimate: 15%.

## Turn 3: extremal functions and sharp counter-perturbations

- Mechanism: solve the equality differential equation, perturb the quadratic coefficient, and inspect its first derivative on the negative radius.
- Artifact: FULL_PROOF.md, Proposition 1 sharpness and section 4.
- Result: every eta>delta fails local univalence for an explicit f0 in K[A,B]. The proposed upper bound is sharp for univalence and is an unavoidable upper bound for starlikeness. The extremal model saturates the boundary singular-value bound on the negative radius. A separate convex-quadratic class has an exactly computed neighbourhood radius.
- Exact gap: one extremal ray and one elementary subclass cannot establish a minimum over the entire Janowski class.
- Disposition: sharpness half proved; lower starlikeness assertion remains open in this attempt.
- Completion estimate: 15%.

## Turn 4: Herglotz measures and finite adversarial optimization

- Mechanism: represent the B=-1 slice by all probability measures on the circle, derive a certified finite-atomic Janowski subclass, and seek a singular-value violation.
- Artifact: FULL_PROOF.md section 5; finite_search.py; FINITE_SEARCH_RESULTS.json.
- Result: 15 bounded three-atom searches at fixed parameter pairs found no strict numerical violation; best values approach the known point-mass equality case. An initial four-seed exploratory optimization likewise produced no violation and did not alter the route.
- Exact gap: no reduction to finitely many atoms is proved. Arbitrary probability measures, interior points, excluded near-singular phases and, for B>-1, the rest of the Janowski class remain beyond these computations.
- Disposition: exact representation plus explicitly non-certifying empirical evidence. This is not a computational proof.
- Completion estimate: 15%.

## Turn 5: dilation into the known positive range

- Mechanism: normalize f(rz), use Schwarz's lemma to transform parameters to (rA,rB), and compare the scaled coefficient distance with the recorded valid radius.
- Artifact: FULL_PROOF.md, Proposition 3.
- Result: every function in the proposed neighbourhood is starlike on the disk of radius (2+sqrt(3))/(4|B|), at least 0.9330127018, conditional only on the stated known theorem.
- Exact gap: no argument reaches the remaining annulus while retaining the same sharp coefficient radius.
- Disposition: quantitative partial conclusion; fifth route exhausted.
- Completion estimate: 15%.

## Freeze disposition

The package contains complete proofs of its stated partial deductions. It contains no full candidate for Problem 6.111. Status must stay `unsolved`, with 5/5 turns used. The strongest exact residual is equation (8) of FULL_PROOF.md. An independent review may check these artifacts, but should not treat verification as additional proof-search turns.
