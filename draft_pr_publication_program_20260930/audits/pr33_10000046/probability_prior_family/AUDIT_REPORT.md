# PR33 original-stage probability and prior-family report

**Disposition: accept the unresolved partial and qualified prior attribution. Do not promote a complete 4D proof certificate, a 3D solution, or a novelty claim.** The elementary probability claims are correct under complete SRW path marginals. Reproduction succeeds. The cited prior states the intended 4D result, but this fresh full relevant-source audit identifies more literal defects and a conditional-prefix issue than the package's two examples. Its explicit full-proof caveat is mandatory and must travel with the attribution.

Frozen scope: original head `de5877c38bf3604f0a8e074af7a9c55fca334522`, actual metadata base `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`; thirteen numeric snapshot files and fourteen original diff paths. Only this assigned audit folder was written. No Git/GitHub/shared research/paper mutation or external communication occurred. Original attempt count stays 1/5; this audit adds zero proof-attempt responses. All thirteen originals were read after INITIAL_SEAL.md was written, and no sibling family report was read.

## Target and mathematical conclusions

The literal [archived Benjamini notes](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf), dated 2013-10-30, define graph distance and nearest-neighbour SRW on printed p. 5; Open Problem 12.33 appears on printed p. 104. Thus the package's l1 distance-ten model agrees with the standing convention. The source does not explicitly quantify every orientation. The package fixes arbitrary vertices at that distance and should retain this explicit stronger reading. Its intended 4D prior covers every fixed nonzero start displacement in the final proof's formulation.

The target is positive mass under a joint law of two **complete** SRWs for

    X_i != Y_j for all i,j >= 0.

Both initial vertices are included. Each marginal has independent uniform increments from all 2d directions. Arbitrary joint couplings are allowed; one-time marginal distributions, simultaneous avoidance, and a Markovian joint construction are distinct requirements.

For synchronous translation Y_n=X_n+v, l1(v)=10, if a trace collision occurs then X_i-X_j=v, hence 10<=|i-j|<=N. It follows pathwise that the two N-step traces are disjoint for N<=9. Both finite marginal laws are complete SRW prefix laws, so the finite optimum indeed equals one at those horizons, in every displacement orientation.

At N=10 only (i,j)=(10,0) or (0,10) can collide. Let c(v)=10!/product(|v_k|!). A first collision occurs exactly when the ten increments sum to v or -v, two disjoint events with c(v) words each. Therefore this specific coupling has collision probability

    q(v)=2c(v)/(2d)^10.

In B disjoint ten-increment blocks, the endpoint events “block displacement is v or -v” are independent with probability q(v)>0. Full avoidance through 10B steps implies none occurs, so its probability is at most (1-q(v))^B. Taking B→∞ proves this translation coupling has infinite full-range avoidance probability zero. This does not assert that **every** coupling fails. Equal-time collision under this coupling is impossible at every n because v is fixed nonzero.

For any arbitrary coupling, X's event T_y<∞ forces intersection with Y_0=y. Consequently

    alpha(x,y) <= 1-P_x(T_y<∞) < 1.

Only the fixed marginal is used; no conditional-joint-filtration or independence assumption enters. At graph distance ten no earlier hitting time exists. Every path hitting by time ten must consist of ten geodesic coordinate steps of the fixed signs, so

    P_x(T_y<=10)=c(v)/(2d)^10.

These counts include zero coordinates and negative displacements. They are an upper obstruction to universal probability one, not a proof of alpha=0. Excluding time zero would remove this direct obstruction. The nearest-neighbour graph-distance assumption is essential: a Euclidean-distance-ten displacement can have graph distance greater than ten.

## Actual controls, original replay, and failures tested

`audit_controls.py` is independent of both original matching implementations. Its 6,993 passing exact checks include:

- 402 signed distance-ten endpoint orientations in d=3 and 2,720 in d=4, using full unrestricted positive/negative SRW recursion; correct total mass and parity at every step;
- exhaustive full-range collision pairs for small axial, spread and negative displacements, proving the exact first-collision horizon includes an initial vertex, with only endpoints at that horizon;
- the actual d=3/d=4 signed distance-ten probabilities and the independent-block geometric failure bound;
- exact processes with correct t=1 and t=2 endpoint marginals but a forbidden jump of graph distance three with positive probability (2d)^-3, demonstrating why one-time checks cannot certify a SRW path law;
- a fully specified iid-binary-sequence relation whose probability tends to zero under product law yet equals one under the complete-path-marginal-preserving complement coupling; this falsifies the inference from independent-law decay to impossibility under arbitrary couplings, without purporting to construct a lattice avoidance coupling;
- a two-step-return event of probability 1/8 falsifying the prior's literal unregularized typical-good-time claim, and a permitted x=(10,0,0,0), radius 20 counterexample to its negative literal A.3 upper bound.

Representative actual-distance-ten values:

| Dimension / displacement | Initial hit by ten | Translation collision by ten |
|---|---:|---:|
| 3, (10,0,0) | 1/60,466,176 | 1/30,233,088 |
| 3, (3,-3,4) | 175/2,519,424 | 175/1,259,712 |
| 4, (10,0,0,0) | 1/1,073,741,824 | 1/536,870,912 |
| 4, (3,-2,3,-2) | 1,575/67,108,864 | 1,575/33,554,432 |

The frozen author's `verify.py` was run unchanged in `.tmp/unchanged_original_replay/`. Its generated verification.json is byte-identical to the original. The frozen prior review's independent_checks.py also emits byte-identical independent_results.json. Hashes of all thirteen originals before and after replay agree. The twelve original matching cases and the old review's twenty-eight cases / 665 assertions remain finite diagnostics. The author's 292 shortest-path checks use positive-coordinate words through lengths 1–6; the old reviewer extends actual distance-ten endpoint checks. Neither receipt verifies a uniform infinite-horizon lower bound. All replay outputs and copied originals are ignored temporary evidence, not first-party deliverables.

Reproduce only this own receipt by running `python3 audit_controls.py` from any directory. It is standard-library-only, locates the adjacent frozen snapshot itself, and writes exclusively in this own folder. It deliberately implements no new finite optimizer and makes no asymptotic extrapolation from endpoint counts.

## Deep prior status and verified boundary

[Benjamini–Kozma, v1](https://arxiv.org/abs/2412.16600v1) was freshly recovered along with source TeX and hidden explanations; the complete main proof and appendix were read, and the suspect rendered formulas were inspected. The exact old PDF and TeX hashes match. The current primary record still lists only v1 and no journal reference. Full locations, explicit hypotheses, literal failures, and own bounded conditional repairs are in PRIOR_AUDIT.md.

The reported Lemma 8 polarity and growing Cn_1^6 term are confirmed. A full repair also needs the 8^T normalization, bad/hittable-path loss bookkeeping, strict Hall thresholds and epsilon range, regularized good-time kernels, a consistent near-exit definition, proper trace versus temporal-intersection quantities, spatial logarithms, and the final induction's conditional-probability accounting. These are not answered by merely flipping the two advertised symbols.

I independently checked the Hall mechanism **given** the corrected quantitative hittability estimates. The finite uniform permutation preserves both complete prefix marginals. Tightness on the countable stopped-path space gives the stated stopped-law limit even for arbitrary one-walk exception events. I also supplied a bounded averaged-induction repair:

    p_(n+1) >= p_n(1-C(log n)^2/n^2)-C/(n+1)^4.

This avoids incorrectly assuming that an unconditional rare H event is uniformly rare after fixing an arbitrary joint past. If the corrected source lemmas and fixed-x initial probability c_x/n_1 are available, the summable multiplicative error and O(n_1^-3) additive loss yield a positive lower bound. This is a conditional audit certificate of the architecture; it leaves the source's main quantitative estimates and arbitrary-fixed-x initialization independently unverified.

The retrieved [Lawler–Limic author PDF](https://math.uchicago.edu/~lawler/srwbook10.pdf) exactly matches the package's old checksum. The relevant harmonic-measure estimate is **Lemma 6.3.7**, printed pp. 130–131 of that author draft, not the source preprint's cited 6.7.3. Its hypotheses are a finite-range symmetric irreducible increment law p∈P_d, large radius, start in C_(radius/4), and an outside exit-boundary point. The Harnack extension in Theorem 6.3.9 requires a nonnegative harmonic function on a scaled open connected set and evaluation on a compact interior subset. For SRW C_r is Euclidean B(r), and the positive harmonic exit-probability function permits comparison of starts in B(r/2). Thus the r^-3 scale used in the 4D annular endpoint estimate is supported with an explicit outer/inner boundary convention. The Green asymptotic and hitting-probability relation (Theorem 4.3.1, printed pp. 81–82) support a regularized 4D hitting kernel of order (1+|z|)^-2. This does not automatically repair all the distinct-trace moments.

## Fresh Shi source scope

[Shi et al., arXiv:2609.25968](https://arxiv.org/abs/2609.25968), current v1 submitted 2026-09-22, was read in full relevant detail; rendered pp. 2–4 were inspected. Definitions (1)–(4), §II, and (10)–(16) use independent walk laws, with a common initial collision removed analytically or distinct sites in a fixed box for simulations. Continuous moments retain an independent probe law; nonlinear empirical moments have finite-sample bias discussed explicitly. Tables and fits give numerical exponent estimates, not a uniform arbitrary-coupling or Hall-deficiency theorem. This scope cannot decide the target. No later version or journal reference is listed on its current primary record. Its numerical estimates were not independently reproduced, because no claim about their numerical correctness is promoted here.

The bounded primary-record/search check found no verified modern 3D coupling resolution. Say precisely that; do not claim that this proves the 3D problem is still open as a global literature fact.

## Strongest accepted partial and residual gap

Accepted: the package's complete-law/full-trace formulation, nine-step translation construction, almost-sure all-time failure of that specific translation coupling, initial-vertex obstruction, exact geodesic first-hit probability, and honest finite-only receipt scope. Accept the 4D result as an attributed **intended theorem stated by the existing preprint**, with the explicit lack of complete independent proof certification retained. The conditional architecture repairs clarify where further verification is required without changing the bundled goal.

Residual: no 3D construction or universal obstruction, no positive horizon-uniform 3D matching bound, and no independently completed 4D source-proof repair. The source's quantitative hittability / prefix lemmas and arbitrary-fixed-x initialization remain the exact full-proof audit boundary. The original standard equivalent reformulation is blocked at its central unsupported bound; this audit does not reopen it or spend a new proof-attempt response.

Required publication language: **“The combined target remains unresolved. Benjamini–Kozma v1 states the intended four-dimensional result; the present package attributes that prior result and does not independently certify its complete proof. No three-dimensional solution or novelty claim is established.”** The existing PARTIAL.md caveat already supports this limited disposition; preserve it, and keep the additional source-repair findings available with the audit.
