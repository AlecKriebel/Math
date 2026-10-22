# Independent review of Davis's dimension-ratio problem (6200004)

## Verdict and reviewed object

**PASS: accept the five turns as correct, scoped partial progress. The original problem remains UNSOLVED by this work, with 5/5 substantive author turns consumed. No blocking correction is required.**

The reviewed object is the frozen local author packet identified by `FREEZE_MANIFEST.json`, SHA-256:

`f9a631c08f6624d9184b2afd71d8098ef4ad68fb0bb163cb29ff34fe3e733745`.

It extends the recovered [turn-4 commit fd707b73b09f2ea4ef325b7993f75ebb10e758e8](https://github.com/AlecKriebel/Math/commit/fd707b73b09f2ea4ef325b7993f75ebb10e758e8) in AlecKriebel/Math, directory `unsolved_math_prioritization/attempts/6200004`, on the author-designated branch `dot/math-6200004`.

This review was performed on 2026-10-03 UTC. It independently checks the written arguments, their cited hypotheses, and reproducible evidence. It is not a formal proof-assistant certificate, a claim of historical novelty, or an exhaustive current-literature clearance. No sixth author search was performed and no author file was changed. The review does not itself publish the work or update the shared queue.

## 1. Integrity, recovery, and replay

I independently verified the supplied freeze hash and all 45 listed file hashes and byte lengths. `TURN_5_MANIFEST.json` is byte-identical to `FREEZE_MANIFEST.json`; the two manifests are copies of the same binding, not independent evidence.

For the earlier checkpoint, I fetched a fresh directory listing at the immutable turn-4 commit through the GitHub connector. All 33 returned filenames, sizes, and Git blob SHAs match the actual local bytes, whose Git blob hashes were recomputed with the appropriate Git header. The 32 entries bound by the turn-4 manifest also verify.

All five historical/terminal manifests verify against the current bytes. Their respective file-entry counts are 10, 18, 25, 32, and 45. These are overlapping cumulative bindings; they must not be added and advertised as that many distinct files. The terminal freeze is the identity controlling this review, including the locally completed fifth turn. I do not imply that turn 5 was already present at the remote turn-4 commit.

All ten supplied source PDFs match their original saved source-manifest SHA-256 hashes, not merely a recovery receipt's assertion that they matched. PDF sources, text extractions, and recovered duplicate directories are local review inputs rather than proposed public author files.

Using Python 3.12.14, `python reproduce_checks.py` succeeds and its output agrees with `ALL_CHECKS.json`:

- Turn 1: 8,218 reported assertions
- Turn 2: 680
- Turn 3: 81,584
- Turn 4: 2,818
- Turn 5: 4,945
- Total: 98,245

The replay checks the prior checkpoint and source hashes as well as all five saved JSON results. I checked the terminal freeze separately, since the replay script does not itself validate that terminal manifest.

## 2. Source normalization

### Exact question

I independently rendered and visually inspected page 3 of the supplied hash-verified [Kapovich problem list](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf). Problem 4 is attributed to Mike Davis and asks for torsion-free hyperbolic groups with rational/integral cohomological-dimension ratio strictly below 2/3. The nearby background gives the boundary shift and existing equality examples.

The packet correctly treats:

- hyperbolicity as Gromov hyperbolicity;
- group cohomological dimension as projective dimension over the group ring, quantifying over coefficient modules;
- boundary cohomological dimension as relative Čech dimension;
- a strict inequality, so the known pair (2,3) does not suffice;
- the trivial group as unsuitable for a ratio with zero denominator;
- conformal dimension as a different invariant.

The primary list is a 2007 record of the earlier workshop question. This review establishes the identification and the scope of the supplied work; it is not a claim that the old list alone certifies the absence of later solutions.

### Dependencies and source-read scope

I checked the relevant primary-source statements and surrounding arguments in the supplied PDFs, including:

- Dranishnikov, [On Bestvina-Mess Formula](https://arxiv.org/abs/math/0503018), introduction and Theorem 1: the coefficient-sensitive boundary formula and equality of global and relative cohomological dimensions.
- Dicks-Leary, Proposition 9: prime-field detection under type FP, together with the scope of the preceding non-FP example.
- Davis's Coxeter book, Section 8.5: compact-support cohomology, closed-simplex punctures, virtual cohomological dimension, and the projective-plane example.
- Bowditch, Theorem 0.1, Proposition 1.2, definitions of bounded/hanging Fuchsian groups, and Section 6: the splitting and boundary inputs.
- Arora-Martínez-Pedroza, [Subgroups of word hyperbolic groups in rational dimension 2](https://arxiv.org/abs/1811.09220), Theorem 1.1 and its stated scope.
- The cited recent fibering paper's Corollaries D and E, and the distinction between its F2-not-F3 examples and weaker/general fibering claims.
- Dranishnikov, [Cohomological dimension of Markov compacta](https://arxiv.org/abs/math/0611028), the building-block definition, upper dimension theorem, top field-dimension lemma, unsymmetrized construction, Lemma 3.4, and the k=1 modifications through Proposition 3.12.

I also checked the definition of space cohomological degree in the 2025 fibering paper and the introductory scope of the conformal-dimension/Pontryagin-sphere paper. Their uses here are appropriately limited.

The original 1991 Bestvina-Mess paper is not among the supplied verified PDFs, and I did not independently recertify its full proof. The packet openly relies on the theorem as stated and developed in the later primary sources. Nor did I repeat the full earlier all-ref duplicate search, audit every construction in every cited paper, or claim an exhaustive novelty review. Those qualifications should remain visible in a publication.

## 3. Turn 1: coefficient profiles and low dimensions

**Accepted as necessary conditions and an algebraic obstruction analysis.**

A nontrivial torsion-free hyperbolic group is infinite and admits a finite classifying complex. The augmentation-splitting argument correctly rules out rational cohomological dimension zero.

The boundary shift is retained correctly. With q=cd_Q(G), d=cd_Z(G), r=q-1, and n=d-1, the target is 3r+1<2n, not 3r<2n. The q=1 argument is sound: vanishing relative rational degree-one cohomology makes degree-zero functions separate any pair of boundary points; these are locally constant functions. Compactness gives a clopen basis, hence covering dimension zero and d=1. Thus q>=2 for a witness, and the first possible pair is (2,4).

The group-ring base-change identity is justified by finite generation of the free/projective resolution terms and exact localization. It is not an identity about ordinary cohomology with trivial coefficients.

The top detection argument is correct. The highest nonzero group-ring cohomology detects finite cohomological dimension for the finite-projective resolution in use. Its top cokernel is finitely generated as a right group-ring module even without assuming the group ring is Noetherian. If that module is torsion as an abelian group, a common multiple of the additive orders of finitely many module generators annihilates the entire module. A nonzero bounded-exponent torsion module has nonzero reduction at some prime, yielding the integral top dimension over that prime field. This is properly credited to Dicks-Leary's detection result.

The finite-denominator argument is also sound. The rational projection onto a projective syzygy has finitely many matrix denominators. Clearing them preserves its three required identities and supplies a finite projective resolution over Z[1/N]. Reduction modulo p for p not dividing N remains exact because the augmented resolution splits successively over the coefficient ring as a module sequence. The proof correctly does not claim that F_p is flat over Z[1/N].

Only the top integral discrepancy is shown to have one common exponent. The weaker statement about N-power torsion in other degrees does not silently assume finite generation of all cohomology modules.

Finally, the artificial finite cochain models genuinely demonstrate that these algebraic restrictions alone do not impose the ratio. They are explicitly not asserted to be group resolutions or boundary realizations. The discussion of global cohomology of finite polyhedra versus relative dimension is correct.

## 4. Turn 2: closed PL manifold nerves

**Accepted with the stated manifold and Coxeter hypotheses.**

The punctured-nerve formula is used with the correct shift and the correct deletion: a closed geometric simplex, including the empty one. The barycentric-coordinate deformation onto the full subcomplex on the remaining vertices is valid; outside the deleted closed simplex the sum of the other coordinates is positive throughout.

For a closed connected orientable PL n-manifold nerve, the empty puncture gives nonzero top cohomology over both Z and Q. The Davis complex gives the matching upper dimension, so the two group dimensions are n+1.

For a nonorientable closed connected PL n-manifold, the top integral cohomology is Z/2 while rational top cohomology is zero. A regular neighborhood of a simplex is an n-ball, and its complement models the puncture. Top rational cohomology of the resulting manifold with nonempty boundary vanishes. Removing a vertex supplies the relative n-ball class in the long exact sequence, forcing a nonzero rational degree-(n-1) puncture class. Hence the dimensions are (n,n+1), with n>=2, and the ratio is at least 2/3.

The argument does not generalize that calculation to singular nerves. It also separates virtual cohomological-dimension computation from hyperbolicity. Barycentric subdivision gives flagness but can create induced squares. The displayed four-face cycle across an edge incident to two triangles is indeed induced.

The finite examples are used correctly: the icosahedral nerve passes flag/no-square, whereas the barycentric projective-plane nerve passes the cohomology computation but fails no-square. The latter cannot be substituted for a certified hyperbolic equality example.

## 5. Turn 3: operations on singular nerves

**Accepted for the explicitly generated construction class.**

For clique inflation, the deleted base vertices are exactly those whose complete fibers were removed. This is the central bookkeeping requirement. Choosing a surviving representative in every remaining fiber yields a simplicial section, and the union-of-faces argument proves contiguity with the identity. Every old puncture is realized by deleting whole fibers. Thus the all-puncture homotopy profiles, not just global cohomology, are preserved.

The no-square equivalence is correct. Two vertices in one inflated clique cannot occur as opposite square vertices, and adjacent ones have matching external neighbors that create a diagonal. A square upstairs therefore projects to a square downstairs.

Coning leaves the nontrivial puncture profiles unchanged. The group interpretation as a product with a finite C2 factor agrees with the calculation.

For proper clique sums, the intersection of punctured pieces is a simplex or empty. Mayer-Vietoris gives no extra positive-degree reduced cohomology; a disconnected union can add degree zero. Subgroup monotonicity and the infinite dihedral special subgroup give the reverse bounds. The separate degeneration when one side equals the intersection is correctly retained. Hence the maximum formula, including the possible additional dimension one, is valid.

Joins of two nonsimplex flag nerves have a cross-factor induced square and an infinite-product obstruction to hyperbolicity. Even without hyperbolicity, rational additivity and the integral upper bound suffice for the ratio comparison. The proof does not make the false general claim that integral cohomological dimension is always additive.

Consequently the stated seed-and-operation family is excluded. It is not a classification of all flag-no-square nerves, and the packet does not present it as one.

## 6. Turn 4: splitting and subgroup obstructions

**Accepted with the stated restrictions on edge groups and finiteness properties.**

The Bass-Serre dimension bounds follow from the tree's augmented induced-module complex, or the displayed long exact sequence for arbitrary group-ring modules. Subgroup monotonicity supplies the lower bound.

For torsion-free hyperbolic groups, finite or two-ended edge groups are trivial or infinite cyclic, and are quasiconvex. Bowditch's vertex quasiconvexity result supplies hyperbolicity of the vertex groups; arbitrary subgroups are not being assumed hyperbolic. With d>=4, the edge contribution cannot account for dimension d, so some vertex has the same d and rational dimension no larger than the ambient group's. A strict ratio violation therefore descends.

Accessibility yields a finite splitting over finite groups and gives the one-ended reduction. The quoted connectedness, local connectedness, and absence of global cut points are the appropriate boundary conditions. No absence of local cut points is inferred.

The JSJ statement is also properly qualified. Bowditch explicitly defines bounded Fuchsian groups to be convex cocompact but not cocompact, and hanging Fuchsian groups are virtually free. Their torsion-free versions have dimension at most one. The closed-surface exception is handled separately. A high-dimensional vertex is therefore type (3), but this does not prove absolute rigidity or termination of arbitrary iterated splittings.

The Arora-Martínez-Pedroza obstruction is applied with exactly finite presentation and cd_Q<=2. A torsion-free subgroup of type F2 but not F3 cannot be hyperbolic, because a torsion-free hyperbolic group has a finite classifying space. Thus such a subgroup forces q>=3. This excludes the cited d=3 and d=4 fiber-kernel examples without excluding all higher-dimensional fibered groups. In particular, F3 is not conflated with FP3 over Q.

## 7. Turn 5: simplex-seeded versus sphere-seeded Markov towers

**Accepted. The seed and unsymmetrized qualifications are essential.**

### 7.1 The boundary obstruction

Dranishnikov's boundary theorem supplies equality between global and relative cohomological dimension for the relevant PID coefficients, including fields. The proof uses it only in positive degree, so no reduced/unreduced degree-zero ambiguity enters. A compactum of relative field dimension n>0 with zero global degree-n Čech cohomology cannot be a hyperbolic-group boundary.

The inverse-system proposition is correct. Over a field, universal coefficients naturally dualize H_n to H^n. Isomorphisms on top homology therefore give isomorphisms on top cohomology. Čech continuity uses their direct limit, not an inverse limit of homology. The limit group is consequently isomorphic to the initial degree-n cohomology.

### 7.2 Why the relevant tower satisfies the homology hypothesis

I checked the unsymmetrized recursive construction and visually inspected the source's printed pages 15 and 19. Lemma 3.4 proves the top-homology preservation for the recursive blocks; Proposition 3.12 and the k=1 modification provide the corresponding ingredient in rational dimension one.

The packet reconstructs the required part rather than relying solely on the broad existence theorem:

- The m=1 starting block is the identity interval.
- For m>=2, the target K' of the auxiliary map from the lifted boundary B has dimension m-1, so its H_m is zero.
- That auxiliary map kills positive-degree mod-p homology.
- The mapping-cone exact sequence therefore identifies H_m(C_g) with H_(m-1)(B).
- The suspension of the previously constructed boundary projection gives the required relative top isomorphism over each m-simplex.
- Relative homology over the m-skeleton is a direct sum of the local terms, while the lifted (m-1)-skeleton has the inductively preserved top homology.
- The absolute top groups are the kernels of the relative connecting maps. The commutative square of isomorphisms identifies those kernels.

A useful explicit base-case clarification is that at m=2, B is a circle and a degree-p circle map has precisely the required positive mod-p vanishing and localized degree-one cohomology property. Thus the induction does not require an impossible assertion about unreduced H_0, or the simply connected hypothesis used in the earlier k>1 localization argument.

The source's mapping-cone notation has a slip: C_g/K' is the suspension of the domain B, not of K'. The packet corrects that and uses the right homology sequence. Its restriction to positive-degree homology likewise avoids the source's shorthand about killing all homology of connected spaces.

### 7.3 Dimensions and the role of symmetrization

The upper rational-dimension estimate must use the upper cohomological-dimension bound for the building block, not merely its lower map invariant. The k=1 version of Lemma 3.8 supplies the localized upper bound, which implies the rational upper bound used with Theorem 2.7. Lemma 2.10(2) supplies the full top prime-field dimension. That top-dimensional conclusion does not need optional symmetrization.

The unsymmetrized condition matters because it preserves the specific homology-isomorphism induction just audited. One should not replace the blocks by an arbitrary symmetrization and silently retain that conclusion.

For the simplex seed, H_n(K_0;F_p)=0. Every stage therefore has zero top mod-p homology, and the inverse limit has zero global top mod-p Čech cohomology. Its relative mod-p dimension is nevertheless n. The covering-dimension upper bound from the n-dimensional inverse system and the prime-field lower bound give covering dimension n. Rational dimension is exactly one: it is at most one, and zero would force covering dimension zero by the earlier clopen argument.

For a sphere seed with the same homology-preserving tower, H_n(K_0;F_p)=F_p survives. Thus the particular global/relative mismatch disappears. This is not a hyperbolic-group realization and does not verify other boundary constraints. It does not contradict the known two-dimensional Pontryagin-surface boundary examples.

The formal pair (2,n+1) for n>=3 would satisfy the target inequality only if an appropriate boundary were realized. The simplex-seeded construction instead fails the necessary boundary test. The packet does not claim a universal nonrealizability theorem for all compacta with that numerical profile.

## 8. What the computations establish

I read the five verifier scripts and their shared exact-linear and simplicial helpers, rather than treating a passing receipt as a proof.

The arithmetic uses rational numbers or exact prime-field elimination. Fixed seeds make the sampled matrix controls reproducible. The scripts check finite complexes, puncture profiles, contiguity, induced-square witnesses, and finite exact-sequence models. They do not algorithmically recognize hyperbolicity of arbitrary groups, prove the cited foundational theorems, or certify an infinite construction by finite sampling.

In particular:

- Turn 1's complexes are intentionally algebraic models, not group resolutions.
- Turn 2 computes rational and mod-2 homology; the general integral dimension conclusion still uses the written orientation/cohomology argument.
- Turn 3's all-ring claim follows from actual homotopy equivalences, not from testing a few fields.
- Turn 4's vector-space mapping cones only control dimension bookkeeping.
- Turn 5's cellular replacement checker is a two-dimensional degree-p prototype. It does not computationally construct the general higher-dimensional block. The source-supported induction and continuity arguments are what establish the unrestricted statement.

The counts measure tested identities, not research completion or probabilities of correctness.

## 9. Final disposition and remaining gap

No mathematical repair is required before describing these results as reviewed partial progress. A publication must retain the original question as unresolved and preserve five author turns consumed.

The surviving task is still either to construct a nontrivial torsion-free hyperbolic group with rigorously determined q,d and 3q<2d, or to prove 3q>=2d for every admissible group. General singular flag-no-square nerves and genuine boundary realization remain outside these exclusions.

Do not relabel a coefficient-sensitive compactum, a CAT(0)-only group, a ratio-equality example, or conformal-dimension growth as a solution. Do not extend the simplex-seeded Markov obstruction to sphere seeds or all Markov compacta.

The terminal author state contains an older generic `in_progress` field but also explicitly records five turns and `complete_unresolved_pending_independent_review`. That is a historical checkpoint convention, not permission for a sixth turn. Any reviewed-state/queue disposition should be additive, without rewriting frozen proofs or their source bindings. The 15 percent original-goal estimate is an explicitly heuristic author estimate and is not endorsed as a calibrated mathematical metric.

This review was completed before any publication action. Raw PDFs, extracted text, and recovery duplicates should remain outside the public packet unless separately requested.

