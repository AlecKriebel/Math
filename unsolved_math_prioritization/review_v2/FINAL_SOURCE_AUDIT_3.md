# Independent source and mathematical audit of four provisional leaders

Audit checkpoint: 2026-09-22 UTC. Completion: 100% of this bounded four-record audit; shard 3 desk coverage was already verified at 2,577/2,577. The individual review ledger remains untouched. These are ranking recommendations, not solutions or comprehensive literature certifications. Probabilities are subjective five-turn estimates.

| ID | Recommended decision | Impact | p_solve | p_valid_open | Reason |
|---|---|---:|---:|---:|---|
| 4700020 | defer | 5 | .01 | .85 | The proposed changing Perron norm does not supply global contraction; no new mechanism crosses that gap. |
| 4700004 | repair | 2 | .03 | .50 | Established cycle bounds; only a method-specific new proof is potentially unresolved. Keep out of the main queue until that scope is explicit. |
| 30005044 | candidate | 3 | .08 | .70 | Source-faithful existence question with a plausible heavy-tail construction; fixed-law and recovery arguments remain substantial. |
| 30006090 | repair | 3 | .03 | .45 | Extracted statement expands the source question; distinguish local diffusion limit, global existence, and annealed consensus. |

## 4700020 — absolute-Jacobian discrete Markus–Yamabe question

Gasull's Problem 20 really assumes the entrywise absolute Jacobian has spectral radius below one everywhere. Counterexamples for the weaker condition on the signed Jacobian do not settle it. The 2020 source explicitly leaves this planar question open. No later resolution was located in the bounded search. [Primary source, pp. 20–21](https://arxiv.org/pdf/2012.02524).

**Independent mathematical check.** Pointwise Perron weights cannot simply be made into a common contracting norm: the nonnegative matrices A=[[1/2,2],[0,1/2]] and B=A-transpose each have spectral radius 1/2, while AB has an eigenvalue larger than one. This is a diagnostic against the proposed inference, not a counterexample to the nonlinear problem: realizing derivatives of a single globally smooth map imposes extra constraints. A varying norm also needs control of its change along each step and escape to infinity. A trapping rectangle is itself an unproved central claim. This is proof-oriented and does not inherently need exhaustive search, but the present route is too generic to justify a leading .08 probability.

Recommended reason flag: `global_contraction_gap`; retain the original open status, lower five-turn priority. Reopen the route only with an actual integrability-based bound, common Lyapunov construction, or candidate smooth counterexample satisfying the hypothesis globally.

## 4700004 — Dulac proofs for low-degree Liénard systems

The source already states that Lie(3)=Lie(4)=1 is proved; Problem 4 asks for proofs using Dulac functions. Solving the cycle bound itself is therefore not novel. Both cubic and quartic cases belong to the requested bundle. [Gasull, pp. 6–7](https://arxiv.org/pdf/2012.02524).

A later paper supplies curvature-based Dulac functions for some Liénard systems; its classical-system argument has sign expression M=(y−F)^2 xF''. This is a relevant existing tool, not verified here as a solution for arbitrary cubic and quartic F. [Gasull–Giacomini, Section 3.3](https://arxiv.org/pdf/2101.03874).

**Independent mathematical check.** For a general quartic, xF'' has a nonzero cubic leading term and changes sign between the two ends of the line. Thus that displayed certificate does not uniformly settle the quartic case. For a cubic with a quadratic term, xF'' can also change sign. A proposed certificate must handle all coefficient regimes, the zero set, the topology of its complement, and degenerate center cases; finding a polynomial ansatz without those checks is insufficient. Symbolic exploration can be small, but there is no established bounded-degree certificate guarantee.

Recommended flags: `known_conclusion_new_method_only`, `method_novelty_unverified`. Repair the title to “New Dulac-function proofs of established cubic and quartic Liénard bounds.” Do not mark the entire method question solved; with the user's exclude-already-solved preference, hold it outside the principal unresolved-conclusion queue unless alternate-proof contributions are explicitly included.

## 30005044 — contact-process explosion for infinite-mean offspring

The original question asks whether explosion can occur when Eξ=∞; it does not demand explosion for every infinite-mean law. [OWR 12/2022, p. 619](https://ems.press/content/serial-article-files/46949). The current primary preprint still assumes finite Eξ and proves nonexplosion under that assumption in Theorem 3.2. Hence that theorem does not resolve this target. The newer model permits dependence between offspring and fitness, which must not silently replace assumptions of the 2022 question. [Cardona-Tobón–Ortgiese, Section 2 and Theorem 3.2](https://arxiv.org/pdf/2110.14537).

**Independent mathematical check.** A useful route is a heavy-tailed, almost-surely finite offspring law supporting a ray of rapidly increasing branching or fitness, with summable passage times. One must specify one fixed offspring/fitness law; choosing distributions separately at each generation is not the stated BGW model. Infection arrows must beat recovery, and infinitely many births before a finite time must be connected to the exact claimed explosion event. A no-recovery condition along an infinite ray costs an infinite product; positivity needs a summable remaining-time bound, not merely summable individual edge times. Dependencies introduced by selecting the ray need treatment. These are concrete probabilistic lemmas, not a large search.

Retain as a candidate with .08 rather than .15. Record whether the attempt targets positive-probability explosion, with what fitness law and independence assumptions, before spending the five-turn budget. No solved-status override is justified by this audit.

## 30006090 — stochastic Bures–Wasserstein continuous-time limit

The original source asks for a continuous-time description of its projected noisy exponential-map update. It does not append the dataset's full global well-posedness-and-consensus bundle. The update uses expΣ(T)=(I+T)Σ(I+T), a projection onto T≥−I+εI, and Gaussian tangent perturbations. [OWR 56/2024, pp. 3244–3245](https://ems.press/content/serial-article-files/50763).

A January 2026 paper by Borghi and Carrillo instead develops stochastic consensus in a *linearized* Bures–Wasserstein geometry, deliberately avoiding the original manifold's boundary difficulty. Its existence/convergence results must not be transferred to the original projected update. [Primary paper, Section 2](https://arxiv.org/pdf/2601.00632).

**Independent mathematical check.** In compact subsets of the positive-definite cone, a formal expansion of the source update contributes both covariance noise WΣ+ΣW and the quadratic Itô drift proportional to E[WΣW]. Omitting the latter yields the wrong candidate SDE. Specify the symmetric-noise covariance and the scaling of σ(k). With fixed 0<ε<1, zero lies inside the projection domain; other ε choices require separate treatment. Local consistency does not prove boundary avoidance or global weak convergence.

Moreover, independent nonvanishing additive mean noises obstruct exact asymptotic consensus: subtracting two mean equations gives dD=−D dt+σ(dB_i−dB_j), an Ornstein–Uhlenbeck difference with nonzero stationary variance for constant σ. Consensus requires additional noise assumptions such as suitable decay; it cannot be advertised as automatic. This observation diagnoses an overbroad target, not a resolution of the original limit problem.

Recommended flags: `source_scope_expansion`, `noise_and_boundary_assumptions_missing`, `adjacent_2026_result_different_geometry`. Repair to a rigorous limit for the exact update under explicit assumptions. Score the full extracted bundle at .03 pending repair; a local stopped-limit subproblem may be easier but is only partial progress. No extensive enumeration is required.
