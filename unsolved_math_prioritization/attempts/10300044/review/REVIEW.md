# Independent review: Godbillon–Vey growth on a fixed hyperbolic manifold

**Problem 10300044 / AMR-102-0044. Verdict: PASS_COMPLETE_FIXED_HYPERBOLIC_TAUT_COUNTEREXAMPLE.**

The frozen candidate gives a complete negative answer to the printed Question 10.6. No mandatory mathematical correction was identified. The conclusion follows from the classical compact-support suspension realization together with the candidate's relative gluing argument. It concerns smooth cooriented taut foliations on one fixed closed hyperbolic mapping torus. Historical priority is unconfirmed, and this independent AI audit is not human peer review.

The covered CANDIDATE.md SHA-256 is
**28d66c68f4497b1b2a3476d3f858902e8def73e65357320a743da43cb0564c6f**.
The author's mathematical files were not edited during review.

## 1. Exact source question and regularity

Calegari's [complete 2002 manuscript](https://arxiv.org/abs/math/0209081), printed p.25, asks:

> Is there a uniform bound on the Godbillon–Vey invariants of the taut foliations of a hyperbolic manifold in terms of its volume?

The rendered page was inspected independently. Definition 1.1 requires a single transverse circle intersecting every leaf. Section 13.1 discusses the ordinary differential-form invariant and allows C² regularity. The candidate works smoothly, so it satisfies that regularity. Question 10.6 adds no minimality or absence-of-compact-leaves condition. The same manuscript explicitly imposes minimality in the different Question 13.1.

The following normal-triangulation remark is real source context, but it supplies no stated differential estimate that defeats the construction. Fixing the smooth manifold and one hyperbolic metric makes its positive finite volume constant. A sequence of positive Godbillon–Vey numbers tending to infinity therefore excludes every finite volume-only bound, not just a linear bound.

## 2. The nonzero block is supported by the precise classical source

I read and visually checked printed pp.1, 3 and 6 of [Tsuboi's full 1981 paper](https://aif.centre-mersenne.org/item/10.5802/aif.828.pdf). Page 1 records the surjective smooth Godbillon–Vey map. Page 3 identifies the compactly supported real-line diffeomorphism group, Mather's H₂-to-H₃ isomorphism, and the commutative diagram relating it to the actual foliated circle-bundle suspension. Page 6 states surface representability of integral group-homology 2-classes. The bars and smoothness conventions in the classifying-space notation were checked in the images.

These statements supply an actual smooth compact-support suspension with a nonzero ordinary Godbillon–Vey integral. Merely citing arbitrary foliations on S³ would not supply this. The candidate correctly uses the stronger, geometrically compatible input. It does not need the separate genus-reduction sentence on p.3.

For the application, choose one positive class, then a connected surface representative with positive value. If a representative has several components, positivity of their sum ensures a positive component exists. Adding trivial handles is implemented by a degree-one collapse to that component, so it preserves the represented class. Thus one may arrange a closed connected base of genus at least two. Neither an explicit value for its genus nor a genus bound uniform over all real Godbillon–Vey numbers is needed: this single base is fixed before stacking begins.

The full six-page [Tsuboi 2013 conference text](https://tsuboiweb.matrix.jp/faculty-html-gf2013/abstract_files/gf2013_195-200.pdf), Theorem 2.1 and the subsequent compact-support discussion, corroborates the input. The original Mather–Thurston proofs are imported classical theorems, not independently reconstructed in this review.

## 3. Relative trivialization, collars and defining forms

A surface group is finitely generated. The supports of the images of a finite generating set lie in a single compact interval. Every word fixes the complement of that interval. Under an increasing identification with the interior of [0,1], the suspension is therefore genuinely a product on two common endpoint collars, with equality of all derivatives.

The relative trivialization argument is valid. Take a finite local bundle atlas subordinate to the compact base. In each chart choose the fiber coordinate agreeing with the already fixed collar coordinates. A partition-of-unity average of these functions has strictly positive vertical derivative and takes the endpoint values 0 and 1. It is consequently a smooth coordinate on each interval, with a smooth inverse and the prescribed collar behavior. This is a trivialization of the bundle; it is not a trivialization of the flat foliation.

In this trivialization the horizontal foliation is transverse to the global vertical vector field V. Its coorientation allows a global defining form α with α(V)=1. On the collars α=ds. Frobenius gives
\[
0=\iota_V(\alpha\wedge d\alpha)
  =d\alpha-\alpha\wedge\iota_Vd\alpha.
\]
Hence η=ι_Vdα has the required sign in dα=α∧η, and η vanishes identically on both collars.

Closing the interval fiber with the complementary identity-holonomy arc recovers exactly the circle suspension in the classical diagram. Extend the defining form by the circle coordinate form and η by zero. The complementary region contributes zero. Thus the integral over the interval block equals the nonzero closed-suspension integral a. This establishes a relative integral with a fixed boundary normalization; it does not assume arbitrary boundary primitives have invariant integrals.

## 4. The fixed hyperbolic mapping torus and its transversal

An orientation-preserving pseudo-Anosov mapping class exists on every closed oriented surface of genus at least two. Its smooth representative can fix a small disk. In the stated twist construction, the finitely many thin annuli leave a small complementary disk untouched. Equivalently, a smooth representative can be isotoped on a disk without altering its mapping class. There is no claim that the disk-fixing representative itself has pseudo-Anosov singular-foliation normal form.

Theorem 0.1, Proposition 2.6 and §5 of the full [Thurston mapping-torus preprint](https://arxiv.org/abs/math/9801045) were checked. They give a finite-volume hyperbolic structure for the mapping torus of this closed surface and pseudo-Anosov mapping class. Because the fiber is closed, the mapping torus is compact. The mapping class, representative and resulting manifold are fixed before N is chosen.

The cited Penner theorem is the standard positive/negative twist criterion. Its publisher PDF returned 403 during this review, as disclosed in the author's source audit. I independently retrieved the complete [Fathi 1992 primary proof](https://www.numdam.org/article/BSMF_1992__120_4_467_0.pdf), read its source conventions and theorem on pp.467–468, and visually checked the latter page. The theorem supplies exactly the required mapping class; its formulation also distinguishes the twist representative from a pseudo-Anosov representative of the same class. Only this existence theorem and the elementary support argument are needed here; the full historical proof is not recertified.

The vector field ∂t descends through the mapping-torus gluing because the gluing acts only in the surface coordinate. A point p in the fixed disk gives the smooth embedded vertical circle γ.

The crucial global tautness check is affirmative. In an interval suspension, a leaf through any point projects onto the entire connected base: lift a base path to p in the universal-cover model. Its interval coordinate remains a legitimate point of the compact interval, and the quotient gives a leafwise path ending over p. This is complete holonomy of a suspension by full interval diffeomorphisms, not an assumption that an arbitrary transverse connection is complete.

Consequently every block leaf meets γ. In the complementary product slabs every leaf is a surface fiber and meets γ as well. The interface leaves are product leaves. The inserted blocks never touch the mapping-torus seam. Thus the same circle is positively transverse and meets every leaf of every constructed foliation, exactly as the source requires. No Reeb-component or weaker Reebless argument is substituted for tautness.

## 5. Smooth stacking and exact additivity

For each finite N choose N disjoint interior intervals with positive gaps. On a slab of length ℓ use h(x,t)=(x,(t-a)/ℓ) and
\[
\alpha_{\rm slab}=\ell h^*\alpha,\qquad
\eta_{\rm slab}=h^*\eta.
\]
The factor ℓ makes α equal to dt on the collars. Both defining equations and coorientation are preserved. On the complement take dt and zero. All forms agree on open collars, hence glue smoothly, including at the mapping-torus seam.

There are no cross terms: η vanishes in neighborhoods of all interfaces. Orientation-preserving change of variables gives
\[
\int_{\rm slab}\eta_{\rm slab}\wedge d\eta_{\rm slab}
=\int_{\Sigma\times I}\eta\wedge d\eta=a.
\]
Therefore the total integral is Na. The lengths of the slabs do not enter the answer. Large derivatives as N increases are permitted because the source imposes no uniform derivative bound; every individual foliation remains smooth.

Compact leaves are essential to this convenient construction and are allowed in the printed question. It gives no answer to a modified minimal-foliation question. The fiber foliation of the same mapping torus has η=0, also independently refuting the imported report's positive volume lower bound; that separate diagnostic alone would not refute the requested upper bound.

## 6. Reproducibility and disposition

The author checker was copied with the frozen proof into author_replay/ and rerun. All **2,660 assertions** pass, and its output reproduces the submitted receipt byte for byte. All **1,641 independent exact controls** also pass. They use a different vector-calculus/SymPy implementation of the contraction and Frobenius identities, an integrable local family, exact rational tests, compression Jacobians and integrals, positive fiber-coordinate averages, and separated slabs.

These computations do not construct the classical representation, certify a hyperbolic metric, or prove global tautness. Those are the source-backed and geometric arguments audited above. A bounded literature search and the 2026 Kitano–Mitsumatsu–Morita preprint corroborate the classical context but do not establish historical priority for this assembly.

**Recommendation:** classify the printed target as **claimed_solved, 2/5**, matching the author's research log, after this separate full audit. Preserve the classical attribution, exact closed/smooth/cooriented/taut scope, unchanged frozen proof, source-access qualifications, and unconfirmed priority. No mathematical correction is required.
