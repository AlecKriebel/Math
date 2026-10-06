# Independent primary-source and scope audit of PR111

Problem 4900006 / AMR-048-0006. Reviewed immutable candidate SHA-256 `a9ea8220014aed7c082c995023a3bc7cdd10014544a85376d99267d908323266`. Completed 2026-10-06 UTC. This is an independent mathematical/source-admissibility review, not a completed priority search or publication approval.

## Verdict and corrected symbol inspection

**The analytic construction is admissible and is a complete counterexample to the literal imported unrestricted assertion under its explicitly stated nonnegative-partial-sum pointwise convention. It also refutes the later unrestricted fixed-global-index assertion at Parker–Goluskin equation (18), under that source's actual assumptions. No mandatory mathematical/source-definition correction remains in the immutable original candidate. The historical-scope qualifications already present in that candidate must be retained.**

Kuznetsov–Mokaev's printed equation (5) uses **nonnegative** partial sums. My initial 125dpi visual reading incorrectly treated the faint lower bar as absent. The dimension family's high-resolution crop and my independently rendered 300dpi original page both clearly show the nonnegative inequality. That earlier strict-positive claim and proposed mandatory repair are withdrawn. The exact wrong report, source-control program and receipt are preserved with explicit withdrawn filenames and byte pins in `WITHDRAWAL.json`; they are not acceptance authorities. The actual formula supports the stable-circle value 1 and neutral-torus type SS value 2. The candidate explicitly supplies dimension zero when the leading exponent is negative.

The root's diagnostic v1 candidate, SHA-256 `4943f2c38effe24e0aa049242f035091df100c1089612cd2ae4c585abc161ddb`, was read in full but must be rejected because it incorporates the false strict-positive source claim. The immutable original candidate remains mathematically/source-definition sound. This correction to my audit changes no vector field, attractor, derivative, spectrum, dimension table or orbit separation. No all-size mathematical gap was found. It does not follow that every historically named variant of “Eden's conjecture” is resolved.

## Exact target and source evidence

The full imported `SOURCE_STATEMENT.json` asks whether every smooth dissipative dynamical system with a global attractor has a local-dimension supremum realized at an equilibrium or unstable periodic orbit. Its hypotheses contain no chaos, transitivity, genericity, or Lorenz-system restriction. The full imported `PRIOR_REPORT.md` is triage. Its statements that the transcription is historically faithful, that the conjecture was raised in a 1994 book, and that it remains open in full generality are not established by that report's described search. Do not repeat those claims as authenticated historical facts.

**Eden (1989).** The complete nine-page article plus archive cover was retrieved. Printed pp. 408–411 were read, including rendered equations (3.1)–(3.5), Questions 1–3, and the immediately surrounding assumptions. Equation (3.4) inherits an index from global exponent sums. Question 1 asks for a point attaining the global dimension, without an equilibrium/periodic restriction. Question 2 concerns characterization of a critical trajectory. Question 3 occurs specifically in the Lorenz application. The preceding global framework uses a compact invariant subset of a separable Hilbert space, a continuous semigroup with full invariance, and compact linear derivative operators. This finite-dimensional smooth flow satisfies those framework assumptions. It nevertheless refutes neither Question 1 nor the Lorenz Question 3. The article points to Eden's thesis for an abstract dimension example; that thesis has not been read in this audit. [Primary article](https://www.numdam.org/article/M2AN_1989__23_3_405_0.pdf).

**Parker–Goluskin, version 2.** Complete 46-page PDF retrieved; full introduction and Section 2.1 read, all scope/assumption/conjecture occurrences across the full text inspected, including Section 3 and bibliography. Definitions 2.1–2.2 maximize tangent/exterior-vector asymptotic growth over initial directions. Definition 2.3 chooses a fixed global index using the supremal next partial sum. The paragraph after equation (18) states an equilibrium-or-periodic maximizing assertion for global attractors. Its assumptions are C1 regularity, forward-invariant state space, and forward-bounded trajectories; it attaches no chaos, transitivity, genericity, or polynomial restriction. Polynomial assumptions concern later computational relaxations. Section 3 separately describes an equilibrium-only assertion for systems with equilibria embedded in chaotic attractors. These are different scopes. Both conjecture passages cite Eden's thesis and Leonov–Lyashko (1993), not the imported report's claimed 1994 origin. This modern source substantiates the unrestricted assertion being tested, but does not prove that Eden originally used identical universal quantifiers. [Versioned primary preprint](https://arxiv.org/abs/2510.14870v2).

**Kuznetsov–Mokaev (2018).** Complete three-page paper read, with Section II and its index formula rendered at high resolution. The statement refers to stationary points or unstable periodic orbits embedded in a strange attractor. A separate conjecture has typical-system and self-excited-attractor qualifications. Its formulas use finite-time local dimensions, a spatial supremum, and then an infimum over time. Equation (5)'s index includes nonnegative partial sums, hence handles the neutral examples consistently with the candidate. Section II cites Eden's thesis p. 98. This paper does not authenticate an unrestricted historical all-global-attractor quantifier. [Primary preprint](https://arxiv.org/abs/1807.00235).

The PDF hashes independently match all three immutable citations in the inherited review. Matching a citation hash does not imply agreement with every historical interpretation; exact symbol checks require adequate image resolution.

## Independent admissibility derivation

Write F(s)=−(s−1)(s−4)/(1+s²), g(r)=rF(r²), with angular rates 1 and √2 and a fifth rate −100. The Cartesian denominators are 1+(x²+y²)², strictly positive on real coordinates. Thus the vector field is real analytic on all R5.

For every s≥0, direct algebra gives

- F(s)+4=(3s²+5s)/(1+s²)≥0;
- 3/2−F(s)=[(5/2)(s−1)²+3]/(1+s²)>0.

Consequently |g(r)|≤4r. Both radii and w can grow at most exponentially in either time direction; local existence cannot end at a finite time. This yields a complete real-analytic flow, rather than merely a forward semiflow on an artificially restricted state space.

One planar oscillator has divergence 2F(s)+2sF′(s). Clearing the positive denominator gives the global certificate

8−2sF′(s) = {5[(s−1)²+s²+s⁴]+3(s²−1)²+10s³}/(1+s²)² ≥0.

Thus each oscillator divergence is at most 11, and total divergence is at most −78 everywhere. “Dissipative” is satisfied both by uniform ambient volume contraction and by bounded-set attraction below. The fifth coordinate is not a missing center or a direction of finite-time escape.

The only nonnegative radial equilibria are 0, 1, 2. Radial signs are negative, positive, negative on (0,1), (1,2), (2,∞). Scalar uniqueness prevents crossings of those equilibria. Every trajectory starting in [0,2] remains in that interval in both time directions, so A=closed-D2×closed-D2×{0} is compact and fully invariant. Here D2 means a planar disk of radius two.

For any bounded initial set, choose a common upper radial bound R. Scalar order preservation bounds either radial distance from [0,2] by max(r(t;R)−2,0), tending to zero. The bounded initial w coordinates converge uniformly to zero. Euclidean distance to A therefore tends uniformly to zero on every bounded initial set. This verifies bounded-set attraction, rather than mere pointwise attraction. Any closed bounded-set-attracting set must contain A, because it must attract A itself and its image is A at every time. Hence A is the actual minimal global attractor, not an optional union with a saddle torus.

Every forward trajectory on all of R5 is bounded: a radius is bounded by its initial value or 2, and w decays. We may take Parker–Goluskin's state space as all of R5, or the compact fully invariant A. Their general differentiability and forward-boundedness conditions are met. Their ambient tangent space is R5, so the fifth transverse stable exponent is included even if the invariant set is lower dimensional. Nothing in the checked general definition restricts perturbations to a four-dimensional tangent bundle of A.

## Exhaustive orbit and exponent checks

The only equilibrium is the origin. A nonzero complex coordinate always has a nonzero angular velocity, and w must vanish at an equilibrium. In a periodic orbit, w=0 and both radii are constant, since a nonconstant scalar autonomous radial solution is strictly monotone. An active radius is 1 or 2. If both oscillators are active, a common period T>0 would require T=2πm and √2T=2πn for positive integers m,n, contradicting irrationality of √2. Thus exactly four periodic circles exist: one active oscillator at radius 1 or 2. Radius-one circles are unstable; radius-two circles are stable.

For a nonzero radial trajectory, rotating orthonormal input/output frames give an exactly diagonal variational map, with logarithmic diagonal entries ∫g′(r(t))dt and ∫F(r(t)²)dt. Angular velocity has no radial derivative, so there is no shear. At the origin the exact planar derivative is exp(−4t) times a rotation. The limits elsewhere follow from convergence of the radius and Cesàro averages of the continuous coefficients, avoiding any unsupported multidimensional linearization theorem:

| Type | Radius condition inside A | Exact limiting planar rates |
|---|---|---|
| O | 0≤r<1 | −4, −4 |
| U | r=1 | 3, 0 |
| S | 1<r≤2 | 0, −24/17 |

Orthogonal frame changes preserve singular values and exterior norms. An initial exterior-coordinate blade realizes the sum of its selected limiting rates. An arbitrary fixed initial exterior vector is a finite combination of these blades, whose rate cannot exceed the maximum selected sum. Therefore Parker–Goluskin's directional supremum outside the time limsup gives the calculated leading partial sums; no order of supremum and time limit is exchanged.

The nine ordered type combinations were independently recomputed using all exterior-coordinate subsets. Their six distinct dimensions are:

| Type | Pointwise nonnegative-index dimension | Fixed global-index expression D4 |
|---|---:|---:|
| OO | 0 | 96/25 |
| OU | 11/4 | 79/20 |
| OS | 1 | 332/85 |
| UU | 203/50 | 203/50 |
| US | 6827/1700 | 6827/1700 |
| SS | 2 | 1688/425 |

The supremal leading sums are (3,6,6,6,−94); hence the smallest global index with a negative next sum is exactly 4. Every fifth exponent is −100, so D4=4+M4/100. Both dimension columns have their unique maximal type UU, realized exactly on {|z1|=|z2|=1,w=0}. Every trajectory on this torus is aperiodic. All possible equilibria and periodic circles are strictly below 203/50 in either column.

This attractor is neither chaotic nor transitive. Its large dimension is carried by unstable transverse directions at a normally hyperbolic saddle torus. Irrationality is essential: replacing √2 by a rational ratio makes the UU torus periodic and removes this obstruction. No genericity or perturbation-stability conclusion follows. The construction meets the unrestricted hypotheses precisely; it does not provide a hidden proof for narrower variants.

For the explicitly nonnegative finite-time singular-value convention, the torus and the constant-radius candidate orbits have exact exponential singular values at every t>0. Their pointwise values are therefore constant in time, and inf(t>0) sup(x∈A) dKY(t,x)≥203/50 follows directly from the torus. Computing that entire finite-time infimum exactly is unnecessary and has not been done. The actual printed nonnegative index agrees with the candidate's treatment. Do not extrapolate the asymptotic dimension maximum into equality of the finite-time spatial supremum or its time infimum.

## Checkable controls, limits, and promotion conditions

`independent_scope_checks.py` runs in a separate audit directory, with standard-library exact fractions, no inherited verifier execution, and no original input mutation. The actual completed run and its PID/check count are in `INDEPENDENT_SCOPE_CHECKS.json`. It authenticates the immutable candidate and three primary PDFs, verifies global-bound algebra on wide rational controls, recomputes all exterior subset sums and dimension values, confirms all equilibrium/periodic comparisons, and verifies the nonnegative zero-exponent indices. The all-real bounds, completeness, uniform attraction, irrationality and all asymptotic limits are analytic deductions above; finite samples do not establish them. The earlier PID6713 receipt containing the false documentary claim is preserved as withdrawn even though its rational dimension arithmetic passed.

Promotion framing: retain explicit index conventions and preserve all historical-scope exclusions. The import's prior report must remain labeled as unauthenticated triage. Publication title/abstract must describe a counterexample to the unrestricted global-attractor maximizer assertion, rather than claim an unqualified resolution of every historical Eden conjecture. Original-thesis text, 1994-book provenance and novel priority remain separate source/priority questions. No individual was contacted, no outreach was prepared, and no Git, PR, native-state, tracker, or publication-service mutation was performed.

This phase is 100% complete: mathematical/source admissibility checked, the mistaken symbol finding withdrawn, and no mandatory defect remaining in the original mathematical candidate. Global PR acceptance and publishing remain incomplete; this report is not their approval.
