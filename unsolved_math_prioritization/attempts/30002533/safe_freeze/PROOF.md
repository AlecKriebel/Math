# Complete deduction of the existential answer from published results

## 1. Target and normalization

The controlling source is Martin Möller's contribution, joint work with Christian Weiss, in *Mini-Workshop: Negative Curves on Algebraic Surfaces*, Oberwolfach Report 10/2014, printed pp. 563–564, DOI https://doi.org/10.4171/owr/2014/10 [O]. Its target is a Kobayashi-geodesic algebraic curve in a real-quadratic Hilbert modular surface with normalized foliation-degree ratio outside

`S = {1, 1/2, 1/3, 1/5, 1/7}`.

The report allows immersed curves: on the universal cover the map is a graph `z -> (z,phi(z))`, with the uniformizing factor selected after exchanging factors if necessary. The exponent is the nonuniformizing degree divided by the uniformizing degree. The source prints `L1/L2`; the Gothic paper prints `omega2/omega1`. We use the dictionary `L1 = omega2`, `L2 = omega1`, so the normalization agrees with the source's examples rather than accidentally taking the reciprocal.

On a Gothic curve, this ratio is the exponent denoted `lambda_P`, not necessarily the second-largest exponent of its entire genus-four Hodge bundle. The Prym summand has real rank four; on the real-multiplication curve its two real rank-two eigensystems have nonnegative exponents `1` and `lambda_P`. Other rank-two summands come from elliptic factors.

## 2. Published inputs and their exact roles

We use the following results, not numerical estimates.

1. McMullen–Mukamel–Wright [G], Theorems 1.4, 1.6, 1.7 and Section 5: the Gothic locus `M = Omega G` is an irreducible affine invariant manifold of complex dimension four. Its relative tangent space identifies with the absolute cohomology of a two-dimensional abelian quotient, so projection `p` from relative to absolute cohomology is injective on `TM`. Its real-multiplication loci are finite unions of Teichmüller curves. Their nonsquare-discriminant components form an infinite series and are geometrically primitive.

2. Avila–Eskin–Möller [A], Theorem 1.4: the absolute tangent image of any affine invariant manifold is symplectic, hence has even complex dimension.

3. Eskin–Mirzakhani–Mohammadi [E], Theorem 2.3 and Corollary 2.5: affine probability measures have subsequential affine probability limits with eventual containment in the limiting affine manifold; in particular, a sequence escaping every proper affine submanifold equidistributes to its ambient manifold.

4. Bonatti–Eskin–Wilkinson [B], Theorem 2.8 and its Section 5 proof: Lyapunov exponents are continuous under this convergence of affine measures. The proof works on the continuous invariant summands of the Hodge cocycle. Thus it applies to the Gothic Prym summand and retains that summand's exponents, rather than selecting an unspecified position in the full spectrum.

5. Möller–Torres-Teigell [T], Theorem 11.2: the nontrivial Prym exponent for the affine measure of the Gothic locus is exactly `3/13`. Section 11 identifies the curve exponent with the foliation-degree ratio. Section 4 and Theorem 6.1 place the components in Hilbert modular surfaces attached to norm-six ideals and `(1,6)`-polarized abelian surfaces. The paper's Corollary 1.2 states the varying-exponent conclusion, but our deduction below explicitly handles disconnected loci.

These are the substantive dependencies of the verification. Their proofs are credited to the cited authors; this packet establishes the implication to [O], rather than pretending to reprove their theorems.

## 3. Proper orbit closures inside the Gothic locus are curves

Let `N` be a connected proper affine invariant submanifold of `M`. Its tangent lies in `TM`; consequently `p|TN` is injective. By [A], `p(TN)` is symplectic. Thus `dim_C N` is even. It is at least two because it contains a `GL^+(2,R)` orbit. It is less than four: a closed affine invariant submanifold of the same dimension would contain an open subset of the connected manifold `M`, and hence would equal `M`. Therefore `dim_C N = 2`.

Its area-one locus has real dimension three, equal to the dimension of an `SL(2,R)` orbit. The action is locally free on translation surfaces of genus at least two. Each orbit is therefore open in this connected locus, so the locus is a single orbit. It carries the affine finite invariant measure. This is exactly a closed finite-volume orbit, or a Teichmüller curve after projection. Consequently a proper connected affine invariant submanifold of `M` contains no two distinct such closed orbits.

Finite markings or finite covers used to specify the involution, the elliptic maps, or a bundle structure do not change this dimension argument. They also do not change the Lyapunov exponents or normalized degree ratios.

## 4. Equidistribution for actual individual components

Choose pairwise distinct nonsquare-discriminant Gothic Teichmüller components `C_n` from the infinite primitive series in [G]. Let `N_n` be their area-one orbits and `mu_n` their normalized affine probability measures. All lie in `M`.

By Section 3, no proper connected affine invariant submanifold of `M` can contain an infinite subsequence of distinct `N_n`. A finite union of proper components cannot do so either. Corollary 2.5 of [E] therefore gives

`mu_n -> mu_M`.

Equivalently, use compactness and eventual containment in [E]: any subsequential limit has to contain all sufficiently late `N_n` in that subsequence, so cannot be a proper closed orbit; it must be `M`. This also rules out escape of mass. This step concerns individual ergodic curve measures, not measures averaged over all components of `G_D`.

The rank-four Prym summand is defined by the two elliptic maps and their cohomological complement; after finite auxiliary markings it is a continuous flat summand of the Hodge bundle. Its positive exponents are `1,lambda_P(C_n)` on each curve and `1,3/13` on `M`. Applying [B] on this summand and [T]'s exact value gives

`lambda_P(C_n) -> 3/13`.

This is convergence of genuine component exponents. It does not identify any particular finite-index term with its limit.

## 5. Exact exclusion and rationality

The exact distances between `3/13` and the five old values are

`10/13, 7/26, 4/39, 2/65, 8/91`,

respectively. The minimum is `2/65`. Therefore the open interval

`I = (3/13 - 1/65, 3/13 + 1/65) = (14/65,16/65)`

is disjoint from `S`. By convergence, some `n0` satisfies `lambda_P(C_n) in I` for every `n >= n0`.

For each individual curve the degree-ratio formula in [T], p. 1207, reads

`lambda_P(C_n) = deg(omega_nonuniformizing|C_n) / deg(omega_uniformizing|C_n)`.

These are rational orbifold degrees with nonzero positive denominator. Alternatively, after a finite level cover and unipotent cusp reduction they are ordinary degrees of the corresponding extended algebraic line bundles, divided by the same finite covering degree. Their quotient is rational. This rationality certificate is algebraic; no finite-time numerical dynamical exponent is used.

Thus there exist primitive Teichmüller curves yielding Kobayashi geodesics with an actual rational exponent outside `S`. Indeed, all sufficiently late terms of the chosen sequence do. This proves the existential target from prior published results.

## 6. Hilbert modular surface and polarization compatibility

The original contribution starts with `H^2/SL2(O_D)`. Gothic curves naturally map into `X_D(b)` for an ideal `b` of norm six, as described in [T], Section 4. We do not silently equate these arithmetic quotients or their polarizations.

The groups defining them are arithmetic lattices in the same `SL2(K)` with `K=Q(sqrt(D))`, obtained from commensurable full `O_D`-lattices. Their intersection has finite index in each. On the common finite cover, pull back a Gothic curve and choose one component. It remains algebraic and its universal cover has the same graph form. Push it to the standard Hilbert modular surface and normalize the image. This is an immersed Kobayashi curve. For every finite map of the resulting orbifold curves, both relevant foliation degrees multiply by the same degree. The ratio is unchanged.

This supplies the literal standard-surface version if required; it does not assert that the norm-six and principal polarizations agree. The source has no fixed discriminant requirement and no condition excluding these finite-level correspondences. Geometric primitiveness of the originating genus-four translation surface is supplied independently by [G], Theorem 1.7; it is not inferred from a cover of the parameter curve. The special congruence `D = 5 mod 8` in the report's earlier twisting-volume theorem is not a hypothesis of the later new-exponent question.

## 7. Limits of the conclusion

The formula in [T], Proposition 11.3, for a possibly disconnected `G_D(b)` is explicitly a volume-weighted average. For example the tabulated values at `D=33` give an average `1/4`. The two old values `1/3` and `1/5` can already have average `1/4` with weights `3/8,5/8`. Even the limiting number `3/13` is a convex combination of those old values with weights `3/13,10/13`. Hence an average outside `S` proves no individual example. Sections 3–5 are essential, not optional rhetoric.

No connectedness of `G_D(b)`, component-specific value `1/4`, attainment of `3/13`, effective threshold `n0`, finiteness/infinity on a fixed Hilbert modular surface, or complete classification is claimed. The result is a verification of prior mathematics answering the existential 2014 target. The exact live problem-page text was inaccessible; the original report controls this conclusion.

## References

- [O] Martin Möller, *Twisted Teichmüller curves* (joint with Christian Weiss), pp. 563–564 in *Mini-Workshop: Negative Curves on Algebraic Surfaces*, OWR 10/2014. https://ems.press/content/serial-article-files/46498
- [G] Curtis T. McMullen, Ronen E. Mukamel, Alex Wright, *Cubic curves and totally geodesic subvarieties of moduli space*, Annals of Mathematics 185 (2017), 957–990. https://doi.org/10.4007/annals.2017.185.3.6
- [A] Artur Avila, Alex Eskin, Martin Möller, *Symplectic and isometric SL(2,R)-invariant subbundles of the Hodge bundle*, J. reine angew. Math. 732 (2017), 1–20; inspected author version arXiv:1209.2854v2, Theorem 1.4. https://doi.org/10.1515/crelle-2014-0142
- [E] Alex Eskin, Maryam Mirzakhani, Amir Mohammadi, *Isolation, equidistribution, and orbit closures for the SL(2,R) action on moduli space*, Annals of Mathematics 182 (2015), 673–721. https://doi.org/10.4007/annals.2015.182.2.7
- [B] Christian Bonatti, Alex Eskin, Amie Wilkinson, *Projective cocycles over SL(2,R) actions: measures invariant under the upper triangular group*, Astérisque 415 (2020), 157–180; inspected 28 July 2017 author PDF, Theorem 2.8 and Section 5. https://doi.org/10.24033/ast.1103
- [T] Martin Möller, David Torres-Teigell, *Euler characteristics of Gothic Teichmüller curves*, Geometry & Topology 24 (2020), 1149–1210, published 30 September 2020. https://doi.org/10.2140/gt.2020.24.1149
