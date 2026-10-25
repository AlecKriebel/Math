# Independent analytic review: Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation

Zenodo 21699161, version 1.1.0. Review date: 24 October 2026 Pacific / 25 October 2026 UTC.

## Verdict

**No mathematical defect was identified in the stated results.** The complete published proof and fresh exact checks support the following claims at their explicitly stated scope:

1. For two inputs per party, local Hilbert-space dimension at most two, and every fixed finite input-dependent output architecture, the shared-randomness convex hull of POVM behaviors equals the corresponding convex hull of PVM behaviors.
2. In the heterogeneous `(2,2,3)`-by-`(2,2)` output architecture with three Alice inputs and two Bob inputs, the rational functional in equation (1) has an attained POVM value
   \[
   L_0=20\sqrt2+16/25
   \]
   exceeding the global PVM upper bound
   \[
   U=20\sqrt2+3/5+(4+3\sqrt2)/250.
   \]
   Their exact gap is `3(2-sqrt(2))/250 > 0`. Appendix B supplies the stronger attained lower bound `(16+8sqrt(7813))/25`; neither lower bound nor `U` is claimed to be the corresponding global optimum.
3. Therefore `3 x 2`, up to exchanging parties, is the minimum input architecture for a strict fixed-qubit separation by a linear Bell functional under these conventions.

**Exact mathematical gap identified: none.** This remains an AI-assisted analytic review with reproducible algebra, not external human peer review, proof-assistant formalization, or a novelty/priority certificate. The Zenodo record itself calls the manuscript an unreviewed preprint.

The scope restrictions are essential. The result does not establish equality of raw nonconvex strategy images, simulation on the original state, operator-level simulability of an individual POVM, a bound on private randomness, or an extension to higher dimension, more parties, or sequential instruments.

## Artifact binding and independence

- All **34 pages** of the freshly acquired published PDF were read, including every appendix and the notation table.
- PDF SHA-256: `1a408e9d98f5166e8ffa6adf607413132facb51fa6f8d3108843b5f0280f2c66`; 238,228 bytes. This agrees with the fresh public Zenodo receipt and the originally identified PDF.
- Fresh software companion: [Zenodo 21699224](https://doi.org/10.5281/zenodo.21699224), ZIP SHA-256 `b34c0570a8ad1f98c8688d597bf9a2cfdc525ba5b20b90dc9638f7ec8af66e77`.
- Fresh TeX companion: [Zenodo 21699181](https://doi.org/10.5281/zenodo.21699181), archive SHA-256 `86b611349f562d06274ea10d9d01107dfc50da07838c2d4785ca9a2da01af83a`.
- The locally available released software archive was byte-identical to the fresh software archive. Each of the eight mathematical scripts/data files extracted for this review was also compared individually to the fresh public extraction. See `source_identity.json`, `local_source_archive_identity.json`, and `checked_code_hashes.json`.
- I read the full separation verifier, closure verifier, and rank-zero simulator before executing them. No archived review opinions, claimed audit verdicts, or parallel reviewers' conclusions were read before this verdict. Mathematical source, coefficients, and claimed identities were treated as inputs to verify.
- No source repair was attempted or needed. All work was confined to this analytic review directory. There were no website, spreadsheet, Git, Zenodo, or external-outreach changes.

## Exact model and assumptions checked

The state is an arbitrary density matrix on local spaces of dimension at most two. Measurements are local, finite-outcome POVMs; the projective comparison permits all qubit PVM rank patterns, including zero projectors and deterministic identity/zero measurements. Local dimension is not enlarged by a Naimark dilation. The shared classical variable may choose the state and all measurements together, and may encode deterministic relabelings of all inputs. Thus arbitrary stochastic postprocessing changes neither the convexified PVM set nor any linear optimum.

Compactness and finite-dimensional separation are used correctly. Embedding one-dimensional strategies into two-dimensional spaces does not change the set. A finite stochastic map is a convex combination of deterministic relabelings; merging orthogonal projectors under a deterministic relabeling remains projective. Convexification is genuinely needed in the conclusion: equality of support functions alone would not prove equality of raw strategy images. Finite-dimensional compactness also supplies finite shared-randomness decompositions.

## Reconstruction and stress tests of the proof

### A. The exact three-by-two witness

The simple strategy uses the maximally entangled state, Bob's `Z,X` observables, Alice's CHSH-optimal first two observables, and the three explicit rational rank-one effects. I independently evaluated its Born probabilities, normalization, determinants, and Bell value directly from the matrices, without importing the supplied verification code. The auxiliary probabilities are all `8/25`, producing `T=16/25` and the stated `L_0`.

The projective upper bound does not assume the optimizing state is maximally entangled. For fixed projective measurements, linearity permits a pure optimizing state; local changes of basis put it in Schmidt form with parameter `0 <= eta <= 1`. Its correlation matrix is `diag(sqrt(1-eta^2),-sqrt(1-eta^2),1)`.

Optimizing Alice's CHSH directions, using the top two eigenvalues of the correlation Gram matrix, and applying the contraction bound on Bob's directions give the two independent deficit estimates

\[
\delta=2\sqrt2-S\ge\eta^2/\sqrt2,
\qquad \delta\ge u^2/(2\sqrt2),
\quad u=|b_0\cdot b_1|.
\]

These are valid at product-state and parallel-axis boundaries as well: the latter can be handled by continuity or directly by the contraction expression, without dividing by a zero sum/difference direction. Degenerate CHSH observables `+/-I` give `S<=2`; their total auxiliary score is at most `7/5`, safely below `U`.

Every ternary qubit PVM has one of the six support patterns obtained from `(2,0,0)` or `(1,1,0)`. The manuscript checks all six, rather than assuming all declared outputs are nonzero. The two support pairs involving label 2 reduce to binary discrimination. The determinant is nonpositive, so the trace-norm expression used for its optimum remains valid at zero determinant as well.

The robust comparison `F_eta <= F_0(r)+2eta/5` follows from a polynomial identity whose factors are nonnegative on a larger rectangular domain than the physically allowed triples `(x,y,r)`. The square-root comparison has a positive right side, so squaring is legitimate. I independently checked that identity symbolically. Since the relevant `r` is at least `-u`, this yields `T<=3/5+2(eta+u)/5`. Combining the deficit bounds and completing a scalar square produces exactly `U`. This covers complex directions, arbitrary two-qubit states, all outcome supports, shared randomness, and stochastic postprocessing.

Appendix B's stronger strategy also passed the supplied exact replay. Its one-parameter optimization is explicitly limited to that subfamily. No global POVM optimality is inferred from it.

### B. One-binary-party simulation

A binary qubit POVM has the displayed spectral convex decomposition into a rank-one binary PVM and two deterministic PVMs. Taking the product of the two input decompositions is legitimate: the shared variable fixes both Bob inputs simultaneously.

With those Bob PVMs fixed, the compressed steered-state vector records trace and expectations of the two observables. For independent nontrivial Bloch axes, its cone is the cone over the projected Bloch ellipse. Every extreme compressed ray has a unique positive rank-one lift in the observable plane; a perpendicular Bloch component would violate positivity at an ellipse boundary point.

The cone-circuit argument is sound in the cone actually used. A minimal signed positive relation among distinct extreme rays has at most four vectors in three dimensions; extremality forbids a single ray against two or more distinct rays, and pointedness forbids all signs being equal. Thus its only nontrivial form is two against two. Finite ray decompositions and repeated subtraction terminate because a coefficient is removed at each step. The retained labels prevent illegal identification of outcomes.

Each two-by-two circuit lifts to two rank-one decompositions of the same positive operator `Omega`. Filtering by `Omega^{-1/2}` gives two orthonormal projective decompositions on its rank-two support. A qubit purification realizes both simultaneously; the transpose in Alice's projectors is correct under the manuscript's vectorization convention. Circuit traces supply weights summing to one. Rank-one `Omega`, repeated rays, zero terms, collinear axes, scalar observables, and repeated labels are covered by the degenerate constructions or a deterministic classical split.

This establishes one common decomposition of the entire behavior, not unrelated simulations of individual input pairs. It is allowed to change the state, as the theorem explicitly permits.

### C. Reduction to the genuine binary–ternary residual architecture

Choose an extreme point of the exposed global maximizing face. Since the raw qubit strategy image is compact, that point has a raw realization. Decomposing its state and each POVM preserves the behavior in every retained positive-weight component. A product state cannot supply a value above the PVM support because it is local; an entangled pure qubit state has full-rank reduced states.

The common-span filtering identity was checked directly: the two normalized branch probabilities are multiplied by `(1 +/- epsilon s_{a|x})/q_{+/-}`, and the weights are `q_{+/-}/2`. If the branches coincided with the original behavior, strictly positive marginals would force every coefficient to be the same, making the common operator scalar. Thus the two real operator spans intersect only in `R I`.

The four-dimensional Hermitian space forces one span to have dimension at most two. That measurement is a stochastic postprocessing of a binary spectral PVM, and extremality retains a deterministic projective component. A deterministic input would leave only one nontrivial input on that side and make the behavior local. The other span has dimension at most three. Its nonzero effects are linearly independent, and the support-perturbation rank-square bound forces a genuine residual measurement to have exactly three rank-one effects.

The reduction handles all excluded boundaries before entering the strict incidence model. Full-rank reduced states rule out nonzero effects with zero marginal; linear independence rules out repeated ternary rays; the scalar-only span intersection rules out a ternary ray coinciding with a binary ray. Hence all five local rays are distinct and all cross Lorentz products used in the strict inequalities are positive.

### D. Physical completeness of the incidence manifold

Four effects form a real basis of all Hermitian two-by-two matrices, including the Pauli `Y` direction. Thus the argument does not restrict to real measurements. Their Lorentz Gram matrix has the four-parameter affine normal form in equation (3). The pure-state steering map includes the required transpose and is invertible exactly when the Schmidt rank is full. Its determinant transformation gives the incidence equations and invertibility of the probability block `P`.

For a nearby allowed metric, a smooth Lorentz frame sends the normalization vector to the identity. Its five null coefficient rays therefore become positive rank-one Alice effects. The reconstructed steered operators have coordinates `E_A^{-T} P r_j / 2`; the factor `1/2` is required by the Pauli trace pairing. Their positive marginals select the future cone. Their sums define a positive full-rank state of trace one. Filtering its square root then produces positive rank-one Bob effects with the correct transpose, normalization, and every joint probability.

This construction is sufficient to handle even zero joint probabilities: nonnegativity follows from products of positive operators, not from assuming every joint probability is strictly positive. The true open conditions are positive marginals, full Schmidt rank, distinct rays, and invertible frames.

The five incidence gradients are independent because the matrices `r_j r_j^T` are independent and `Q P` is invertible. The radial probability variation annihilates the incidence derivatives but changes normalization, so that constraint adds one independent row. There are `16+4-5-1=14` dimensions. The regular-level-set theorem gives a two-sided physical curve for every tangent. No unsupported inference from an algebraic tangent to a physically allowed variation remains.

As an independent exact check, I built a full-frame example with complex effects, a tilted Bob binary axis, and the nonmaximally entangled Schmidt state with squared coefficients `3/5,2/5`. All conformal-Lorentz identities, incidences, reconstructed steered operators, marginals, and 25 joint entries agree exactly.

### E. Multiplier positivity

Finite POVM dual attainment is proved explicitly in Appendix E. Its cone is closed because convergence of the sum of positive effects bounds each effect; the slack variable is then bounded as well. The separating functional has nonzero negative scalar coefficient, and its normalization produces bounded approximate dual solutions with an attained limit.

Pulling the incidence stationarity equations back to arbitrary normalized Hermitian variations of a single Bob input gives the determinant adjugate term with factor `4|det Xi|^2`. The pullback applies to arbitrary Hermitian variations, not only variations already tangent to the rank-one locus. The incidence Lagrangian is stationary in the full ambient coordinates, which is why this is justified.

The normalization multiplier and the finite-POVM dual agree: their difference annihilates every nonzero effect range, and those ranges span the qubit space. Consequently each determinant multiplier is nonnegative. If any one vanishes, that outcome's score operator equals the dual, so replacing the whole input by its deterministic outcome preserves the total Bell score. With just one other Bob input the resulting nonsignaling behavior is local; the manuscript supplies the joint hidden-variable construction. A strict separator therefore requires all five multipliers positive and their weighted matrix positive definite.

### F. Second variation and the three ranks

I independently reconstructed the square completion. With `delta P=P W+H Q P`, the ambient second derivative of an incidence is twice `(P W r)^T Q(P W r)`. The weighted form is `q(W)=Tr(S W Lambda W^T)`, with `S=P^T Q P`. Since `S` has signature `(1,3)` and `Lambda` is positive definite, the form on sixteen matrix coordinates has inertia `(4,12)`.

The sign in the Bell second derivative is correct: differentiating the constraints twice along a physical curve and using the stated first-order Lagrange equations yields `L''=2q(W)`. The manuscript is not inadvertently excluding an uphill direction by a reversed sign.

Metric compatibility imposes `k=5-rank D` independent linear conditions, giving dimension `16-k`. Independence follows from invertible `S` and injectivity of the multiplier-to-matrix map. The identity matrix is a compatible null direction with zero cross term; adding it adjusts normalization without changing `q`.

- **Rank at least two:** compatible dimension is at least 13. A form of inertia `(4,12)` cannot be nonpositive on a 13-dimensional subspace. The resulting positive direction integrates physically and contradicts maximality.
- **Rank one:** Appendix G gives a genuine projective inverse away from four exceptional divisors. If its target has a nonzero inverse polynomial, another preimage cannot hide on an exceptional divisor. On each divisor the manuscript explicitly treats direct and cross branches, including zero target coordinates. The resultants leave one base root and at most one nonbase root; the strict metric inequalities exclude identically vanishing residual equations. Intersections are included before scaling. Thus distinct null rays cannot share a nonzero projective image. At most one of the five rows of `D` could then be nonzero, and its transpose kernel contains no strictly positive vector.
- **Rank zero:** the five transformed rays must permute the five base rays. Future orientation makes all scale factors positive. The unique two-versus-three circuit prevents a sign-reversing permutation, so only within-input permutations remain and all scale factors agree. Normalization then gives `P=g` after allowed relabelings. The resulting table has the exact symmetric zero-diagonal ternary block used in Appendix H.

The rank-zero transportation argument is valid: the three interval-intersection bounds are exactly the three inequalities `|d_i| <= (c_ij+c_ik)/2`. Pairwise intersection of closed intervals on a line guarantees a common point, including zero capacities. The constructed deterministic branches reproduce all four blocks together. My fresh rational grid check covered 1,035 allowed instances, 804 on a boundary; it is supplementary to this general interval proof.

Together these ranks exhaust the genuine residual stratum. One-input architectures are local by a direct nonsignaling decomposition, so the three-by-two witness completes the minimum-input conclusion.

## Primary references checked

The central proof is largely self-contained; no numerical optimization output is imported as a theorem.

- [D'Ariano, Lo Presti, Perinotti](https://arxiv.org/pdf/quant-ph/0408115), Theorem 1/2 and Corollary 1, provide the support-perturbation extremality criterion and the rank-square obstruction. Appendix D reproduces exactly the needed necessary condition. The qubit classification also agrees with the binary/ternary distinctions used here.
- [Vértesi and Bene](https://arxiv.org/pdf/1007.2578), especially the definitions of the CH-plus-three-outcome functional and the fixed-state versus unrestricted-two-qubit comparison, verify that a three-by-two advantage predates this paper. The present paper credits that result and claims the matching lower bound plus an explicit rational analytic witness; it does not claim to be the first POVM–PVM separation.
- [Panahi et al.](https://arxiv.org/html/2505.20519v1), Section II.2, discusses qubit realizations of convexly extremal correlations when one party has two binary settings. The present manuscript accurately treats this as a dimension statement, not a projectivization of the other party's arbitrary-output measurements. Its central simulation proof does not depend on the broader mixed-state formulation of that source's Lemma 4.
- [Cerf and Ollivier](https://arxiv.org/html/2603.26875v1) proves a local perturbative result near deterministic correlations and proposes a route concerning raw dimension-restricted measurement sets. It is not the global arbitrary-output convexified equality proved here. No inference from their local result is used as a substitute for the present argument.

This targeted primary-source verification does not certify exhaustive novelty or priority.

## Computational evidence and limits

The exact published checks were freshly replayed with SymPy 1.14.0 in an isolated dependency directory:

- `separation_replay.log`: both explicit strategies, coefficient files, positive factorizations, dual certificates, robust global-bound identities, complete PVM rank-pattern list, and both strict exact gaps passed.
- `closure_replay.log`: metric identities, inverse polynomial, exceptional resultants and factors, an exact state/frame example, a Hessian regression instance, independent-constraint witnesses, and transport identities passed.
- `rank_zero_replay.log`: the supplied exact deterministic simulator passed its symmetric example.
- `negative_coefficient_test.log`: a corrupted dense Bell coefficient was rejected with a nonzero exit. Only a disposable copy was changed.
- `independent_checks.py`, `.json`, and `.log`: independently written code, with no imports from the published implementation, checked the simple witness, robust polynomial, inverse/fiber identities, complex nonmaximally entangled incidence reconstruction, a **general symbolic** Hessian identity, and the 1,035 rational transportation instances.

These checks establish finite identities and examples. Compactness, extremal reductions, physical completeness, dual signs, and the exhaustion of the rank cases were reviewed analytically. Successful execution is not represented as formal proof of the entire theorem. No optimization solver's floating-point result was accepted as a global bound, and no raw-set or same-state equivalence was inferred.

## Disposition

The published claims are supported at the stated fixed-qubit, finite-output, shared-randomness-convexified scope. **No known mathematical repair or missing lemma remains after this review.** The remaining limitation is fallibility of this AI-assisted review and the absence of independent expert human confirmation, rather than an identified gap. Human expert scrutiny would be useful; no outreach was prepared or initiated.

The website description should lead with the two-input convexified equality and the resulting minimum input threshold, credit the earlier three-by-two separation, and retain the unreviewed-preprint status. It should not advertise equality of raw sets, same-state simulation, or global optimization of the displayed Bell functional.
