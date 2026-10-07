# Independent reconstruction: 2-converse ring-class limits and switches

Checkpoint: 2026-10-06 22:28 America/Los_Angeles (2026-10-07 05:28 UTC).
Reviewer: internal AI subagent `upstream_logic`. Assigned-sub-audit completion estimate: 100%. Overall mathematical and publication completion remain the lead researcher's responsibility. This audit extends the earlier family004 logic report; it does not independently certify all sections of the 2-converse manuscript.

## Result

I independently reconstructed all of `ring-limits.tex`, including its finite-stage contractions, character construction, all-sequence evaluation, exact common kernel, outer evaluation, residual bound and Chebotarev realization. I also independently checked the local derivative construction and the abstract determinant switch/outer rank-reduction portions of `ring-determinants.tex` through line 933. I found no concrete counterexample or unsupported step in these assigned mechanisms. Their arithmetic compatibility is supplied by actual finite-stage cochain maps, classes, local lifts and boundary witnesses, rather than by existence of abstractly isomorphic cohomology groups.

The important quantifier is: **a fixed finite number of derivative slots and a fixed inner ultrafilter are preserved while the finite-stage diagrams are extended**. No assertion of simultaneous construction with an unbounded number of derivative objects, no global density estimate, and no passage to a new unrelated subsequence is needed. In the outer argument, the initial cohomological rank is bounded, so only finitely many switches are necessary.

This verdict does not establish the entire pointwise 2-converse independently: central arithmetic determinant identification, binary-family clearing/interpolation, coefficient systems, graph constructions and analytic nonvanishing are separate indispensable mechanisms. The assigned parts do not remove the need to audit them.

## Sources and exact scope

Source clone `/Users/alec/Desktop/math` was read-only. All release reads were pinned to commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

Companion directory:
`preprints/A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-September-24-2026/build/sections/`.

- `ring-limits.tex`: all lines 1–981. Git blob `66b580aec1ce59f468e769bf904428b99cb95343`.
- `ring-determinants.tex`: lines 1–933, with emphasis on 64–565 and 577–881. Git blob `7ec6e3040f458cbd24369e8ed756d64a624d3cdf`.
- `pointwise.tex`: lines 1–220, for the interfaces and dependency ordering.

Primary outside-source check, 2026-10-06: actual [Nekovář, Selmer complexes, Astérisque 310 (2006)](https://www.numdam.org/item/AST_2006__310__R1_0.pdf), Proposition 5.2.4, definitions/lemmas 6.2.5–8 and Theorem 6.3.4. PDF SHA-256 `61c84e5ad3252a2e520747215ac57a282addc2b58c824a3637bcd77bbe02153f`. Read from a research cache after the browser parser rejected its 43-MB size. The reviewer removed this own third-party research cache after recording the URL and hash, at the lead researcher's request to recover disk space; no third-party PDF/text is present for publication. The primary [Bogomolov publication record](https://www.mathnet.ru/eng/im1843) confirms the stated Lie-algebra homothety theorem; I used the release's explicit central-scalar construction, not a modern 2-converse imported from a different source.

## 1. Finite free models: proof rather than a bounded-matrix assumption

`ring-limits.tex` 121–174 works for an arbitrary complex D of flat modules over an Artin local ring A whose residual cohomology is finite and bounded.

Every flat A-module is free, even if its rank is infinite. Lift a residual basis and map the corresponding free module to it. Nilpotence of the maximal ideal kills the cokernel. Flatness identifies the reduction of the kernel with zero, and nilpotence kills that kernel. This establishes the needed actual graded bases.

Over the residue field, split the residual complex into its finite cohomology (zero differential) and contractible disks. Lift the bases and the disk differential d0. The difference epsilon=d−d0 has all coefficients in the nilpotent maximal ideal. With a disk contraction h0, both 1+h0 epsilon and 1+epsilon h0 have finite geometric inverses. The displayed perturbation formulas construct a differential on the finite lifted cohomology module and actual maps i,p,h satisfying pi=1 and 1−ip=dh+hd. Infinite disk sums do not create an infinite geometric series: each operator is an honest module homomorphism and the nilpotence exponent terminates every series.

Consequently an original cochain map f is represented by p' f i. Composition identities and other arithmetic identities are retained with the contraction homotopies. This is stronger than selecting a finite complex with the right cohomology dimensions.

Continuous cochains with finite free Artin coefficients are flat (176–185): locally constant functions are a filtered union of finite partition-function modules. Totally imaginary global fields and nonarchimedean local fields give finite, bounded residual cohomology. The original complexes may be infinite; their residual cohomology determines the finite model ranks.

## 2. Matrix limits preserve actual maps and every old evaluation

For A_i=(Z/2^i)[t]/t^i, every fixed lower coefficient quotient is finite. Fix bounded graded ranks on an ultrafilter-large set. The entrywise ultrafilter limits at each quotient are unique and compatible, yielding matrices over Lambda=Z_2[[t]]. Every specified finite chain identity or homotopy identity is polynomial in finitely many entries, so survives (187–217).

Keep one inner ultrafilter and all original contractions. To add a derivative slot, extend each existing finite stage, build the new object's finite model, and represent comparisons using the old contractions. The old objects and their maps to cochains are not replaced. Thus old evaluations on every group-element sequence are unchanged, even though only finitely many diagram objects are stored. Slowing all coefficient precisions cofinally preserves the same old limits. An arbitrary subsequence or a new ultrafilter would not establish this conclusion; the manuscript explicitly forbids that substitution.

At fixed K, active support, G and finitely many derivative slots, the target ranks are bounded by residual Kummer theory and the fixed class group of K(E[2]) (219–281). Growing ring-class extensions are not retained as source complexes. All descent, Shapiro transfer, coefficient weighting and coset sums are performed first; then the resulting target cochains and local boundary witnesses are contracted. A boundary witness is one vector in a bounded-rank target model, rather than an increasing list of source cosets.

## 3. Local conditions and the named duality theorem

The derived Kummer condition at 2N (285–346) includes its torsion-derived degree zero: for M_F=B(F)^wedge_2, the perfect complex M_F[-1] reduces to B(F)[2^n] in degree zero and B(F)/2^n in degree one. It maps isomorphically to local invariants and injectively to finite Kummer cohomology. The finite Kummer images are exact orthogonal complements. Derived reduction and Nakayama establish the perfect local orthogonality morphism.

The derivative-prime conditions include local H0 and omit local H2; the finite/singular planes are genuinely distinct from full and strict conditions (348–378). Each required local map is an isomorphism on H0 and an injection on H1.

Nekovář's actual Theorem 6.3.4 requires bounded finite-type coefficient complexes, a perfect coefficient pairing and exact orthogonal-complement local conditions. It gives a duality triangle with local error terms, and an isomorphism when those error terms vanish. It does **not** provide varying-prime limits or missing arithmetic classes. The companion supplies these local conditions and isotropy homotopies at finite Artin stages, then uses the theorem only for their finite duality diagrams (380–403). A_i and A_i[G] are finite Frobenius coefficient rings; the Weil pairing and conjugate character transport give the relevant coefficient duality. Thus no ordinary-reduction or residual-irreducibility hypothesis from an unrelated Euler-system theorem is inserted here.

## 4. The moving character is arithmetically constructible

The character prescription (407–533) can be reconstructed as a presentation of the ring-class group.

Choose oriented split prime ideals p_j generating the required class group and take the relation lattice R=ker(Z^s→Cl(K)). For a relation m^(a), choose beta_a with divisor product p_j^m_j^(a). Give weight 1 to every specified odd prime and weight 0 to the extra generators and all primes above 2N. Over K(mu_2∞), prescribe the action on the 2^n-th roots of beta_a/bar(beta_a) with exponent −sum m_j^(a)w_j.

These prescriptions respect every Kummer relation: at a nonzero-weight odd prime, the cyclotomic extension is unramified, so a radicand combination which is a 2^n-th power has valuation divisible by 2^n. Multiplying those divisibilities by the weights proves that the prescribed combined exponent is zero mod 2^n. Zero-weight primes over 2 impose no division by their ramification index. Kummer duality therefore gives a genuine automorphism of the radical extension.

For a split rational prime r, the inertia kernel in the ring-class exact sequence is F_r^×, because the only units are ±1 and their images are diagonal. A primitive power-residue character on that group extends across the class-group relations precisely when it has the prescribed beta_a/bar(beta_a) values. Thus the Frobenius weights, inertia surjectivity and triviality at 2N are actual compatible characters, not arbitrary assignments to Frobenius symbols.

The extra Tate trace conditions do not destroy those radical prescriptions. In the non-CM case, a fixed open subgroup of SL2 in the commutator image fixes every abelian radical extension. In the CM case, choose gamma with cyclotomic value 625; the element gamma u gamma^-1 u^-625 fixes every radicand extension and acts on Tate matrices by rho(u)^−624. A fixed power maps an open norm-one Cartan to an open subgroup. These arguments give a fixed-E open Tate kernel independent of the prescribed prime list. Each allowed compact Tate coset therefore contains an element with trace different from ±2; finitely many cosets give one bounded valuation constant. Finite Chebotarev realizes the simultaneous radical, Tate and cyclotomic conditions. At each stage these conditions involve one finite extension, never splitting in an infinite extension.

## 5. Height-one local acyclicity and the outer rank bound

At the moving r, inertia minus one is t times a unit. It is invertible on the relevant residue fields unless t=0 in characteristic zero. At that fiber the bounded nonzero Frobenius determinants make the unramified/tame directions acyclic. At an active quadratic conductor prime, −2 is invertible in characteristic zero. At the characteristic-two (2)-test, the quadratic character disappears and an odd Frobenius exponent makes (1+t)^a a nonconstant series. No nonzero polynomial over the finite constant field vanishes at it, so the relevant two Frobenius matrices are invertible over F_2((t)) (542–580).

For the outer residual bound (582–625), remove active primes after characteristic-two reduction: their local complexes become acyclic after inverting t, with actual comparison maps. The remaining allowed support is bounded. Over F=Q(E[2]), the field FK has degree at most two. The maximal pro-2 group with bounded ramification support has bounded generator number by residual Kummer theory; the index-two subgroup has bounded generator number by Schreier. A finite Galois 2-extension of FK has 2-power Galois closure over F, so the subgroup does control the needed extensions. Restriction, the global Euler characteristic and the bounded local conditions give bounded residual cohomology. These are model-size bounds only; they do not assert bounded torsion exponents.

## 6. All-sequence evaluation and injectivity after arbitrary base change

Here is the explicit construction behind lines 630–716. Let iota_i:C_i→D_i be the retained chain map to original global cochains. For every sequence g=(g_i), evaluate iota_i in degrees 0,1,2. The matrices have bounded source ranks and finite coefficient entries. One fixed ultrafilter gives their entrywise limits for **every** g and every pair (g,h). Thus no diagonal extraction over the uncountable set of sequences is needed.

With rho(g)=lim rho_i(g_i), the actual differential identities give

    e_g^1 d = (rho(g)−1)e^0,
    e_(g,h)^2 d = rho(g)e_h^1 − e_(gh)^1 + e_g^1.

Therefore any cycle after any field base change gives an abstract crossed homomorphism, and any boundary gives a coboundary. The target is abstract group cohomology; no unjustified continuity of the limit action or cocycle is asserted.

To prove injection uniformly under base change, use the residual finite-dimensional space of pairs (residual H1 representative, m in k^2). The common kernel of all evaluations b_c(g)−(rho(g)−1)m consists exactly of zero classes and invariant m. A list of at most dim H1+2 elements detects that intersection. Evaluation to the resulting two-term complex is an isomorphism on residual H0 and injective on residual H1. For a Selmer complex, the asserted local H0-isomorphisms and H1-injections imply precisely the required global detection via the cone long exact sequence.

The cone of this finite detecting map has no residual cohomology in degrees ≤0. Cancel its unit blocks over the local scalar ring to obtain a finite free cone beginning in degree 1. After **every** field base change its H0 remains zero, so the long exact sequence gives H1 injection. The same cone gives H0 injection. This establishes the stronger base-change assertion; merely checking one field would be insufficient.

## 7. Exact-kernel restriction: an explicit Sah-type calculation

Let H consist of sequences whose entries are exactly trivial on T, every ring-class field of K, and the quadratic characters in use (731–777). They act trivially on the coefficient representation.

Choose a fixed scalar Tate homothety uI, u in 1+4Z_2 and u≠1, with lift g. The element

    z = g² tau g² tau^-1

belongs to G_K, is trivial on every ring-class extension by their generalized-dihedral action, and is trivial on quadratic characters. Its Tate action is u^4 I. The commutator of z with any element of G_K is in H, so z is central in the quotient by H. For a crossed cocycle b on that quotient, comparison at zg and gz gives

    (u^4−1)b(g) = (g−1)b(z).

In characteristic zero u^4−1 is invertible, so b is a coboundary. Inflation–restriction then proves injection on H. Its valuation is fixed independently of K.

In the characteristic-two (2)-test, take the sequence of inertia generators at r_i. Tate inertia is exactly trivial because E is good at r_i, all ring-class images commute, and the quadratic characters are unramified there. It is central modulo H and acts as 1+t. Since t is invertible in F_2((t)), the same identity proves injection. Defining H by actions merely converging to the identity would break this proof; the manuscript correctly uses exact actions at every stage.

## 8. Outer evaluation, including approximate cycles

For an outer ultrafilter U, quotient the ultraproduct of O_j by elements with 2-valuation tending to infinity (781–847). Every surviving nonzero element has bounded valuation on a U-large set; a finite partition makes that valuation one fixed integer n. It is 2^n times a unit. Hence the quotient is a domain with a discrete nonnegative valuation and every ideal is generated by an element of its smallest valuation. It is a DVR, and no positive power of 2 vanishes. Its fraction field has characteristic zero.

Extend the original evaluation maps to O_j and transport them through integral unit-pivot contractions to bounded minimal models. Every entry remains integral. Thus the degree-two identity survives even for vectors x_j whose coboundaries only tend to zero: if v(d_j x_j)→∞, multiplying by the integral degree-two evaluation matrix still gives valuation →∞. No exact inner cycle lift is assumed.

A bounded residual detecting list and its cone contraction also pass to the quotient; the cone still begins in degree 1, giving outer H1 injection. The product of the same fixed central z-elements proves restriction injection to the product of exact kernels. Arbitrary evaluations of old group sequences remain defined from the old contractions.

A possible denominator concern is resolved by the actual construction: contractions after completion may have coefficients such as t^-1, unavailable in the nilpotent Artin rings. Chebotarev is applied to the finite original cochain coordinates before those scalar combinations. Matching all finitely many original basis evaluations at a stage makes their O_j-linear combinations match after taking the inner limit. For each fixed outer instance one can increase the inner precision beyond every finite needed t-degree and approximate 2-adic coefficient precision; no uniform t-degree bound across outer instances is required. The cohomology/evaluation identities are already integral over O_j, so there is no division by a scalar tending to zero in the outer quotient.

Absolute irreducibility also survives concretely (849–890). The possible index≤2 subgroups of the fixed compact Tate image form a finite list. Choose one on a U-large set and choose finitely many fixed Tate matrices spanning M2(Q_2). Their spanning determinant is one fixed nonzero 2-adic number, so survives the quotient. Multiplying them by character units does not change that conclusion. Moving inertia distinguishes Psi and Psi^-1; it has infinite order because every nonzero fixed power of (1+t)−1 is nonzero modulo 2 and hence an O_j-unit. This supplies a finite witness, rather than inferring irreducibility from each component individually.

## 9. Actual derivative primes and finite arithmetic classes

Chebotarev realization (893–939) uses every required coordinate of a retained finite-model map to original cochains. At a fixed Artin stage these are finitely many locally constant functions, so factor through one finite Galois quotient. Enlarge that quotient to contain the finite Tate/ring-class/character data. An exact-kernel element u has rational Frobenius tau u on that quotient; choose a prime and a place with this representative. It is inert in K, its Tate matrix tends to J, and its Frobenius-square localization is evaluation on (tau u)^2. For crossed cocycles restricted to the exact kernel,

    b((tau u)^2) = (1+tau)b(u).

The same finite argument applies separately to each inner sequence in the outer construction and preserves every old finite diagram.

The derivative classes in `ring-determinants.tex` 182–409 are genuinely constructed before taking these limits. The cyclic operators satisfy (sigma−1)D=(ell+1)−Norm. Trace/reduction relations of the CM points make their Kummer classes invariant to sufficiently high finite precision. The exact-kernel scalar z kills ring-class 2-primary torsion by one fixed 2^e. Therefore the obstruction and ambiguity in inflation–restriction are both killed by that same factor, and multiplication by 2^(2e) descends once from the complete conductor. There is no new factor for each derivative prime.

The Shapiro map followed by the character coefficient map is an actual finite coset sum with weights chi Psi, in every cochain degree, with no division by the ring-class group order. Restriction/corestriction naturality supplies local lifts and comparison homotopies. Transfer happens before target contraction; increasing field degrees therefore do not become increasing retained matrix ranks.

At the fixed 2N places the extensions are unramified. The identity-component descent obstruction vanishes by connected special-fiber Lang and the unramified formal-group filtration; the remaining component-group factors come from finitely many fixed local types and enter one fixed L. Psi is trivial at those places, so the weighted transfer preserves that Kummer condition.

For one derivative prime the local computation gives

    f = (a_ell F_ell−(ell+1)) Q,
    s = (a_ell−(ell+1)F_ell) Q,
    (F_ell−a_ell)(a_ell F_ell−(ell+1)) = a_ell−(ell+1)F_ell.

Thus s=Jf in the retained limit. The ambiguity is bounded by comparing the descended-cocycle correction with the actual integer-quotient point ((ell+1)/2^a)Y−(a_ell/2^a)X, not with arbitrary division points. The finite derivative coordinate vanishes when ell+1 has one **extra** power of 2, because the derivative reduction has factor ell(ell+1)/2. Passing from torsion precision a to retained precision m with a−m≥e kills the bounded ambiguity. These are the two significant 2-adic boundary cases, and the manuscript explicitly accommodates both.

Equality of transferred local classes supplies an actual target local boundary witness. Retain it together with the split local complexes, zero plane-isotropy homotopies and comparison maps. This is the concrete finite diagram to which the limit lemma applies; it is not the assertion that a missing derivative class would be convenient.

## 10. Determinant switch and outer rank reduction

The exact switch lemma (473–565) can be checked entirely over a DVR. Nonzero localization of the old spanning class A makes strict H1 zero. The relaxed image is a two-dimensional self-annihilating subspace of the four-dimensional finite-plus-singular local space. It contains (v0,0) and (0,Jv0), so its intersections with the opposite planes are precisely those lines and the switched class B spans generic H1.

With relaxed basis A,B and dual basis A*,B*, the finite-plane boundary is a unit times <x,v0>B*. Choose a fractional x mapping to B*. Then v0 wedge x has unit volume, even if v0 is divisible by an arbitrary power of 2. The analogous singular-plane volume is also a unit. The two exact determinant triangles share the strict determinant factor, so the coordinates of the paired tensors A and B have exactly equal valuation. The use of a fractional complement is legitimate: it is the exterior volume, rather than integrality of the complement, that is required. Nonprimitive indices are retained in the common torsion determinant factors.

For two independent classes whose exact-kernel restrictions are injective, their joint evaluations span W⊕W by absolute irreducibility and scalar endomorphisms (577–615). The additive image need not itself be the entire field span. Nevertheless a determinant quadratic polynomial cannot vanish on that additive image and become nonzero on its field span: polarization on u+v gives the required cross terms in every characteristic. Hence one actual group element has rank-two finite localization. This justifies passing from a span to a single derivative prime.

In the outer bound (745–881), transport original classes, uniformly cleared paired functionals and evaluation/duality maps through unit-pivot contractions. These remain integral. A sequence of primitive inner generic kernel vectors has a nonzero outer limit because some coordinate remains a unit. If the outer H1 rank exceeds one, use the preceding rank-two evaluation and finite Chebotarev to add a derivative prime. The relaxed image equals the whole finite plane; switching to the singular condition removes two fiber dimensions. The generic inner localization is nonzero because its outer value is nonzero, so the exact switch preserves each inner determinant valuation, even when the arithmetic class is a highly divisible multiple of the primitive vector.

The old finite stages, ultrafilters and contractions are extended, not rebuilt. Approximate extra outer cycles are acceptable because of the integral degree-two identity. New inner generic kernels again provide primitive vectors, so outer rank never drops below one. There are only finitely many rank reductions. At rank one a nonzero maximal boundary minor survives in the outer DVR, so the inner minors have one bounded valuation on a U-large set. The elementary Schur-complement formula

    u_i = ± alpha_i beta_i / det A_i

with integral alpha_i and a uniformly cleared beta_i gives a lower valuation bound, contradicting the proposed unbounded losses. Bounded matrix size alone would fail for [2^i]; the rank-reduction operations and surviving terminal minor are the additional arithmetic mechanism.

The central-specialization lemma (892–933) is also valid as an algebraic statement under its explicit constant rational cohomology dimensions. Over Lambda_(t), any nonunit disk would add central cohomology in two adjacent degrees. The specified central and generic dimensions therefore exclude it. Determinant base change retains all 2-primary elementary divisors in the central integral complex. This lemma alone does not identify those divisors with the claimed Heegner/Sha expression; that subsequent arithmetic identification must still be checked independently.

## Boundaries and promotion status

No repair is needed in the mechanisms above on the evidence of this independent reconstruction. The claim “all limits were abstract, so no arithmetic evaluation exists” is not a valid objection to this pinned version: it includes the actual original-cochain contractions and all-sequence evaluations, finite-stage arithmetic maps, degree-two identities and exact kernels needed to answer that objection.

Equally, acceptance of these mechanisms is not acceptance of the entire companion. The final base nonvanishing assertion uses further arithmetic central identification and a uniformly cleared group-ring interpolation across growing binary families. Those are not consequences of the fixed-G compactness lemma or bounded minimal rank alone. They remain distinct checks in the dependency ledger. A substantive failure there would still block the unconditional H10(Q) and geometric follow-on, despite the internally coherent limit/switch machinery checked here.
