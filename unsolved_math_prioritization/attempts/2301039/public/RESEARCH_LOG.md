# Five substantive approach records

**Target:** 2301039 / AMR-022-1039, both parts of Function Theory Problem 1.39.  
**Work date:** 4 October 2026 UTC.  
**Budget:** five substantive approaches; no large exhaustive search. Individual tool calls are not counted as attempts. The route records below are logical checkpoints; source reading, independent modular work and drafting overlapped in time. Estimates are subjective progress toward resolving the original sharp-constant question, not probabilities or claims of completion.

## 1. Reciprocal/Riccati growth reduction

Explored approximately 07:31–07:35 UTC; checkpointed in the final proof note.

Mechanism: replace zero-free meromorphic f by holomorphic u=1/f. Derive exact characteristic equality up to a constant and identify the divisor of u′+u². Attempted to turn derivative omission into global zero-freeness of this differential polynomial.

Outcome: Proposition 1 is proved. The naive global zero-freeness condition is false when multiple poles are allowed; f=2/(m z^m) gives exact admissible controls for every m. This rules out a potential false restriction of part (b). The true condition is zero multiplicity m-1 exactly at a zero of u of order m.

Gap: no sharp characteristic estimate or high-growth u satisfying that divisor condition is obtained. Progress estimate: **5%**.

## 2. Integrating-factor and primitive construction

Explored approximately 07:34–07:40 UTC; checkpointed in Propositions 2–3.

Mechanisms: (i) exponentiate a primitive of 1/f to write f=F/F′; (ii) set q=(f′-1)/f and solve f′-qf=1 globally. Integer negative residues are essential for the single-valued integrating factor. Pole cancellation was checked explicitly rather than ignored.

Outcome: two complete exact parametrizations, including higher-order poles. The analytic case is F,F′,F″ all zero-free. The second parametrization reduces admissibility to omission of one value by a primitive J of 1/H. At a pole of H, cancellation produces a prohibited simple zero of f, so that omitted-value requirement holds at poles too.

Gap: the needed omitted primitive with suitably large logarithmic characteristic is not constructed. These equivalent formulations do not transfer the central difficulty into a solved lemma. Progress estimate: **8%**.

## 3. Boundary-singularity and exponential models

Explored approximately 07:33–07:42 UTC; checkpointed in Proposition 4 and Theorem 5.

Mechanisms: rational/bounded-quotient candidates, followed by exp(P((1+z)/(1-z))). The latter has adjustable boundary concentration and a directly computable characteristic.

Outcome: bounded quotients and all rational functions have alpha=0. For polynomial P of degree at least two, alpha=∞, outside the target. For affine P=aw+b, alpha=|Im a|/π exactly. Every positive-alpha affine model has infinitely many derivative 1-points, proved by a contracting logarithmic equation in the right half-plane. Real positive a with sufficiently large real b gives valid nonconstant alpha=0 controls.

Gap: this excludes the whole stated model family but says nothing universal about arbitrary holomorphic functions. Progress estimate: **10%**.

## 4. Sharp value-distribution and normal-family transfer

Explored approximately 07:31–07:46 UTC, alongside the preceding constructions.

Mechanism: test whether a newer sharp deficiency theorem or a small-logarithmic-derivative theorem eliminates the loss in the historical bounds. The independent construction researcher and main investigation both identified the recent Nadi preprint about adjacent Problem 1.40.

Outcome: the exact scope mismatch is explicit. In a proposed application, a zero-free f with positive alpha contributes deficiency 1 at zero, but the right side still contains the derivative-zero Valiron deficiency and the pole term. The hypothesis f′≠1 does not give the missing upper bound for that derivative-zero term. Affine and quadratic zero-free disk examples show that f′ can have or lack zeros while still omitting 1. No inference from omission of 1 to omission of 0 is valid. Gunsul's narrower class requires m(r,f′/f)=o(T(r,f)); it cannot be silently assumed for all finite-alpha f.

Gap: no theorem controlling those missing terms from the target hypotheses is proved. The cited results are not imported as a full answer, and unread source dependencies are recorded. Progress estimate: **10%**.

## 5. Modular covering and rational cusp constructions

Independent construction work approximately 07:33–07:46 UTC; complete argument in MODULAR_OBSTRUCTION.md.

Mechanism: use the modular lambda function, whose contextual logarithmic growth makes it a natural extremal candidate. Combine its convergent cusp expansion with the quadratic disk-coordinate derivative factor. Solve each prescribed nonzero derivative-value equation by locally uniform convergence and Rouché.

Outcome: the modular candidate's derivative assumes every nonzero value infinitely often. The proof extends to R composed with the modular function whenever R has a zero at 0, 1 or infinity, and it survives arbitrary disk-automorphism precomposition. The symmetric h/h′ quotient fails exactly at the origin. Its needed local nonvanishing is proved by the q-product and a rational inequality. The broader assertion for every zero-free rational composition is deliberately separated as conditional on uninspected surjectivity.

Gap: non-rational modifications and general zero-free functions remain untouched. No positive-alpha admissible witness or improved unrestricted bound was found. Progress estimate: **12%**.

## Final checkpoint

Five substantive routes are complete. **Unsolved, 5/5.** Both sharp constants remain undetermined. The public packet supplies only exact reductions, credited source distinctions and rigorous exclusions of construction families. No original-resolution or historical-priority claim is made. No sixth search route is opened during verification. A fresh independent audit may check and correct these artifacts but must not be represented as additional discovery work hidden outside the attempt budget.

Finite verification: the main script performs 119 exact symbolic controls; the modular script checks the independent Möbius/cusp algebra and the local rational inequality. These controls do not formally certify infinite analytic arguments. The manifest binds the final review package.
