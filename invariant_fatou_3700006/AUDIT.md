# Independent adversarial audit: queue 1820

Audit date: 2026-10-20 UTC. Scope: the source context summarized in SOURCES.md and DYNAMICS.md (including Section 9), CONSTRUCTION.md (including the Laurent extension), and BOUNDARY.md. This audit does not accept a resolution of the unrestricted conjecture.

## Verdict

**The stated partial conclusions pass this audit. No substantive mathematical error was found.** This is a check of the arguments and cited hypotheses, not an independent proof of the source papers. The unrestricted transcendental-entire at-most-one conjecture remains unresolved by these notes. No novelty claim is warranted.

The strongest new-to-this-attempt endpoint is a limitation result: all the listed individual attracting disk conditions can hold simultaneously for an abstract disk self-map obtained from the corrected 2019 example. This does not supply the coupled dynamical embeddings needed for two completely invariant Fatou components.

The publication copy makes explicit the following standard intermediate step in the all-iterate argument: after the composition lemma excludes interior asymptotic curves for b^n, Fatou's radial-limit theorem makes b^n inner, because almost every radial limit exists and none can lie in the open disk. The factorization lemma can then be applied. Alternatively, closure of nonconstant inner functions under composition suffices. This exposition improvement is incorporated in DYNAMICS.md, Sections 4 and 9.3; it is not an outstanding proof gap.

## 1. Exact imported hypotheses checked

The arXiv:1801.06359v3 text was inspected directly, not merely its abstract. Theorem 1.3 assumes a transcendental entire map, two disjoint simply connected domains G1,G2, and connectedness of the full preimage of G1. Under each listed additional hypothesis it concludes that the full preimage of G2 is disconnected. In particular:

- Part (b) requires G1 intersect S(f) to be compactly contained in G1. Boundedness in the plane alone is not enough.
- Part (e) requires one common boundary point accessible from both domains.
- Part (f) concerns accessibility of infinity from the target domain G1, not merely from one preimage component.
- Part (h) concerns an omitted value anywhere, not necessarily in G1 or G2.

The notes meet the base hypotheses in each application. For hypothetical completely invariant Fatou components, periodic simple connectivity and full-preimage equality provide them. For the 2019 consistency construction, the domains and connected full preimages are furnished by Theorem 1.2. For the polynomial/Laurent family, the second domain is a distinct translate of the hypothetical component, whose complete invariance is verified separately.

Corollary 1.4 and the subsequent paragraph explicitly support the attracting/parabolic restriction. A Siegel disk is excluded by injectivity and infinite valence; a Baker domain has accessible infinity. Neither conclusion is imported from Baker's invalid 1970 proof.

The 2019 common-boundary input is genuinely available: Observation 4.5 proves the modification for two domains; Remark 1.13 records it, and Section 5 verifies that exp(z)+z satisfies the vanilla hypotheses. Thus BOUNDARY.md does not infer common boundary from the unmodified statement of Theorem 1.2 alone.

The primary arXiv:2002.03320v4, Proposition 1.1, was also checked directly. It makes an associate inner for arbitrary source and target Riemann maps. Its infinite-Blaschke conclusion generally needs suitable coordinates; it does NOT automatically make the dynamical associate a Blaschke product. DYNAMICS.md correctly supplies its own stronger no-asymptotic-curve/factorization proof instead of silently strengthening that proposition. The same paper explicitly distinguishes independent source/target maps from a dynamical conjugacy and states simple connectivity of forward-invariant entire Fatou components. Its compact-singular-set Theorem 1.2 is not used outside its hypotheses.

## 2. Dynamical necessities

The omitted-value obstruction first gives surjectivity of f. Complete invariance then implies f(U)=U and f^(-n)(U)=U. Picard is used only initially to obtain an infinite fiber outside the possible exceptional value; this is sufficient for infinite degree and unboundedness. Unboundedness is never confused with accessibility of infinity.

If an iterate has an asymptotic value inside U, complete invariance puts the asymptotic curve eventually in U, contradicting inaccessible infinity. This works for every iterate without any direct/logarithmic singularity assumption.

The coordinate argument is sound: if phi(gamma) had a finite cluster point, continuity of f^n and full-preimage equality would put that point back in U. Continuity of phi inverse then contradicts compact escape in the disk. With no finite cluster point, phi(gamma) tends to infinity. No boundary extension of phi is assumed.

The singular-inner-factor argument is valid. At almost every point for a nonzero singular measure, its density relative to arc length tends to infinity. The lower Poisson-kernel estimate on arcs of length comparable to 1-r forces the singular inner factor, hence the bounded product, radially to zero. Applying this to every automorphic postcomposition proves indestructibility. The deduction does not reverse this implication.

Every shifted iterate is a pure Blaschke product. A finite fiber would make its zero set finite and hence make it finite degree, contradicting the inherited infinite fiber. This correctly removes the Picard exception for every value and every iterate.

The equality S(f) intersect U = closure in U of CV(f) intersect U is justified: any sequence converging to an interior point is eventually inside U, where there are no asymptotic values. Consequently compact relative closure of internal critical values would trigger Theorem 1.3(b). Distinct critical values imply distinct critical points, and discreteness of zeros of f' justifies their plane-compact escape. The values themselves may instead approach a finite boundary point, as the notes correctly emphasize.

## 3. Consistency models and iterates

The sine model is correctly limited: it has only the two internal critical values ±1/R, so it does not satisfy the noncompact-critical-value condition. It cannot alone establish consistency of the full package. The direct argument excluding finite asymptotic values of sine is valid, including the repeated-root case.

The stronger exp(z)+z associate does satisfy the full stated individual attracting package. Connected full preimages are proper simply connected domains; the Jordan-curve/argument-principle proof of the latter property is valid even if the image of the Jordan curve is not simple, because winding number about a point outside the simply connected target is zero.

Independent normalizations phi(0)=z0 and psi(0)=F(z0) give b(0)=0. Infinite valence rules out a rotation, so Schwarz's lemma yields |b'(0)|<1. This is attraction for iteration of b, not attraction for F.

The no-asymptotic-curves composition lemma survives the main adversarial test: an intermediate curve need not either converge or escape. If it has an interior cluster point, discreteness of the outer map's fiber permits a small disk with a positive boundary image gap. Eventual closeness to the limiting image traps the intermediate curve after a late entry; its only possible cluster point is the selected fiber point. Therefore it converges, contradicting the inner map's assumed lack of interior asymptotic curves. No properness or finite degree is needed.

For every iterate, infinite fibers follow as above. Surjectivity permits lifting a critical point of b through b^(n-1), proving CV(b) is contained in CV(b^n). Hence the noncompact critical-value property also persists. It does not rely on forward images of critical values staying away from the attracting fixed point.

The global limitation is essential and correctly retained: b^2 inserts phi composed with psi inverse between successive applications of F. It is not psi inverse composed with F^2 composed with phi. No equality between source and target domains is supplied. The construction therefore cannot be used as a counterexample to the Fatou-component conjecture, or as a realization of prescribed attracting dynamical conjugacies for F.

## 4. Polynomial and Laurent family exclusion

Translation symmetry commutes with every iterate, preserves normality, and transports complete invariance. Distinct finite limiting fixed points p+kT ensure that an attracting/parabolic component is disjoint from every nontrivial translate. This is genuine dynamical input, not merely a statement about normality on a smaller trapping set.

The no-finite-asymptotic-values proof is valid. In the Laurent case, bounded real part along any subsequence would keep exp(z) in a compact annulus and P(exp(z)) bounded, contradicting cancellation of z. Thus the real part tends to one of the two infinities, with its sign eventually fixed by continuity. The dominating nonzero Laurent exponent then gives Re(z)=O(log|z|), so the imaginary part tends continuously to one signed infinity. The cancellation equation forces a convergent exponential phase, which the intermediate value theorem prohibits. The argument handles complex coefficients and negative exponents.

The critical equation 1+wP'(w)=0 is a nonzero Laurent polynomial because its constant coefficient is 1. It has finitely many nonzero roots. Critical values consequently form finitely many translation orbits, with no finite accumulation. Each attracting/parabolic component meets each orbit at most once. Its internal singular set is therefore finite and compactly contained, allowing the exact Theorem 1.3(b) contradiction.

For arbitrary nonzero lambda, the conjugacy L(z)=lambda z transforms the map into w+lambda P(exp(w)), preserving the hypotheses and conclusions. The restriction that P be nonconstant matters; no assertion about general holomorphic functions on the punctured plane or arbitrary translation-equivariant maps is established.

The explicit preimage calculation for z+a-a exp(z), 0<a<2, also checks out. The invariant horizontal boundary lines escape; continuity of the displayed real equation provides preimages of zero in arbitrarily distant strips. This independently witnesses failure of complete invariance for those immediate attracting basins.

## 5. Common boundary and Janiszewski

The precise pair-separation form of Janiszewski's theorem was verified in the primary arXiv:math/0309022v6, PDF page 6. The lemma's compact sets cover K, intersect exactly at the hypothesized cut point, and each fails to separate the selected points in U,V. Their union must then fail to separate them, a contradiction. Local connectivity of K is not needed.

Complete invariance and density of a nonexceptional backward orbit give the common boundary J(f). Unboundedness puts infinity in both spherical boundaries. Applying the no-cut-point lemma at infinity yields planar connectedness of J(f). The warning against inferring that planar J(f) has no finite cut point is correct: that would remove two points from the spherical continuum.

For the 2019 common-boundary examples, their infinitely many critical values are unbounded since the critical-value set is discrete. The same lemma and Theorem 1.3(e),(f) give all the stated boundary/accessibility properties without complete invariance. Thus neither common boundary nor dense accessibility on each side closes the dynamical gap. The singular-value accumulation dichotomy also follows from failure of compact containment; it supplies no common accessible accumulation point.

## Acceptance boundary and source links

Accept only the conditional necessities, the specified family exclusion, the topological necessary conditions, and the abstract individual-model consistency result. Do not accept a general theorem, a dynamical counterexample, or a novelty claim.

Primary sources checked:

- Rempe-Gillen–Sixsmith, https://arxiv.org/pdf/1801.06359 (v3; theorem hypotheses, common-boundary modification and relevant proof sections).
- Evdoridou–Rempe–Sixsmith, https://arxiv.org/pdf/2002.03320 (v4; Proposition 1.1 and introduction). The DOI opening failed once; the primary arXiv text succeeded.
- Rempe-Gillen, https://arxiv.org/pdf/math/0309022 (v6; precise Janiszewski statement on PDF page 6).

This audit does not independently inspect Baker's unavailable original chapter or establish an exhaustive current-literature status. It does not publish copied source material or alter the problem queue.
