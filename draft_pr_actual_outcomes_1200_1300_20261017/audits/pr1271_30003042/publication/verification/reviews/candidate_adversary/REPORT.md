# PR1271 candidate mathematical adversary report

Verdict: the submitted literature-derived negative resolution survives this adversarial audit. The strongest verified conclusion is an existential counterexample at n=8 satisfying the original maximal-Clifford-index and ordinary Severi-Brauer function-field hypotheses. No mathematical defect requiring withdrawal was found. This is a dependency-scoped mathematical judgment, not a formal proof certificate or an independent proof of all source theorems.

The audit is bound to PR1271 head `69c35ca09cb09f1642b3a6f2deca766356a972f8` and the eight exact bodies listed in `SUBMITTED_SNAPSHOT.json`. All eight bodies match their byte counts and SHA-256 hashes. Input receipts are not authored-output membership. The complete submitted proof and audit were read before independent source work. No other review family's contents were read, and no external individual was contacted. Source copies, extraction text, renders, and exploratory code are confined to ignored `_local/` and are excluded from the authored manifest.

## Exact claim and success criterion

The original source is Karpenko's contribution on printed pp.226-227 of [OWR 5/2016](https://doi.org/10.4171/OWR/2016/5). Its Conjecture 3 excludes e_n from gamma term n+1-floor((n+1)/2), for n>=8, in the stated odd-dimensional maximal-Clifford-index model. The target at n=8 is therefore

    dim(phi)=17, ind C0(phi)=256 over F,
    X=OG8(phi), K=F(SB(C0(phi))),
    e8 not in gamma^5 K0(X_K).

A single instance with e8 in gamma^5 disproves the full universal assertion. It need not classify the other parameters or prove failure in every characteristic. The symbol 18 in the later index theorem is the dimension of an auxiliary even form; the source Grassmannian number 4 means vector dimension 4, hence a projective 3-space on the quadric.

## Hypothesis challenge: an actual maximal-index instance

Existence need not be accepted merely from the 2016 generic-model paragraph. Here is a characteristic-zero construction.

Take F=C((t1))...((t16)), with its composite rank-16 valuation, and

    phi=<1,-t1,...,-t16>.

In C0(phi), the sixteen elements ui=e0*ei satisfy ui^2=ti and ui*uj=-uj*ui for i!=j. Their squarefree monomials form the usual 2^16-dimensional Clifford basis. Assign ui valuation v(ti)/2. The valuations of the basis monomials occupy distinct cosets of the original value group in its half-lattice. Thus every nonzero element has a unique lowest term; the product of two lowest terms is nonzero and cannot cancel. C0(phi) has no zero divisors. Being finite-dimensional and central simple, it is division, with degree sqrt(2^16)=256. This also makes the initial maximal-index condition concrete.

Set psi=phi orthogonal-sum <-t1...t16>. Its signed discriminant is (t1...t16)^2, hence trivial, and its dimension is 18. The standard codimension-one Clifford identity gives C+(psi)=C0(phi); the corresponding maximal even component is isomorphic to OG8(phi). These identities are explicitly recorded on a16i5 pp.3-4 and remain standard Clifford/Grassmannian inputs; the valuation argument checks the division hypothesis independently.

Let A=C0(phi), S=SB(A), K=F(S). Over K, A splits, so psi_K has trivial discriminant and Clifford invariant. It is a Spin18 form. The pre-extension algebra still had index 256; its subsequent splitting is part of the target, not a lost hypothesis. The above construction avoids every characteristic-two ambiguity while providing a sufficient counterexample to the original universal conjecture.

## Index challenge: source theorem and independently checked arithmetic

The official [published Spin paper](https://doi.org/10.5565/PUBLMAT6722310), printed pp.751-752, explicitly gives generic Spin18 index 8 for the fourth Grassmannian. The final author preprint §6 agrees. The publication metadata and official Article link were independently checked; the downloaded publisher PDF and author preprint match the candidate's recorded hashes. This is authentication of the exact theorem used, not reliance on the candidate's labels.

The decisive numerical upper bound was also checked independently. `COMPUTATION.py`, `COMPUTATION_RESULT.json`, and `COMPUTATION_NOTES.md` give two distinct exact computations of the integral pairing

    integral_IG(5,16) a^3*c2(T)^9*c3(T)
       = -14668659594398531584
       = 2^22 * (-3497280977821),

where a is the eight-factor polynomial specified in the published Appendix A and equals 2^8*ztilde. One method sums 1792 exact fixed-point fractions; another performs integer vertical-Pieri multiplication in Gr(5,16), using its normal Euler class. Neither uses Maple, the source's package, or the source's Schubert coefficients. Three weight sets, tangent/normal consistency, small known degrees, a below-dimension zero, and two deliberately incorrect arithmetic variants were checked.

An integral pairing of valuation 22 disproves divisibility of a^3 by 2^23. It does not prove the exact class-level valuation or reproduce the full printed Schubert expansion. The sufficient index upper bound follows either from Theorem 4.1 or directly from Proposition 3.4 rationality: ztilde^3*c2^9*c3 is a rational integral zero-cycle on generic Spin17 OG5 of degree

    -27978247822568 = 8*(-3497280977821).

The factor between symplectic and odd-orthogonal top degrees is 2^5, visible from the five diagonal tangent roots. Since the index is a power of two, it divides 8. This checks the needed published computation by a smaller independent witness and separately audits the upper-bound mechanism. Proposition 3.4's rationality, the characteristic-map interpretation, and standard Chow/localization/Schur theorems remain inputs.

The index bound for OG4 follows by the isotropic flag projection: OG_(4,5)->OG5 has Grassmannian fibers, hence preserves index; OG_(4,5)->OG4 then gives ind(OG4)|ind(OG5). For an 18-dimensional form, a nondegenerate 17-dimensional subform has the same relevant Clifford invariant; after harmless similarity normalization it is a Spin17 form. Its OG4 includes into the even OG4, preserving the upper divisibility bound. These are independent checks of the mechanism used in published §6. Only the bound is needed; the published exact lower bounds and other index entries are unnecessary.

## Genericity and field challenge

[DKM Proposition 2.1](https://doi.org/10.1017/fms.2021.30), printed p.3, was independently read and visually inspected. It puts the generic Chow image inside the arbitrary twisted-flag Chow image. In top degree,

    ind(generic)*Z subset ind(arbitrary)*Z,

so ind(arbitrary) divides ind(generic). Reversing this is wrong: a split torsor has index 1. Pages 8-9 explicitly place even Clifford-trivial forms under Spin torsors, so the proposition applies to psi_K with G=Spin18 and P for OG4. Therefore ind OG4(psi_K) divides 8.

The 2016 Clifford-splitting model need not literally equal the later generic torsor. No specialization assumes that equality. The generic group can be considered over the base field K itself, and the theorem supplies the universal divisibility bound. Similarity does not change isotropic Grassmannians. A characteristic-zero instance suffices; source statements allowing arbitrary characteristic were checked for consistency, but this audit does not independently rebuild the characteristic-two quadratic-form theory.

## Transfer and integral identity challenge

The index is a gcd. From ind OG4(psi_K)|8, there are finitely many closed-point degrees d_i and integers b_i with sum b_i*d_i=8. Each residue extension supplies a projective 3-space on the 16-dimensional quadric Y, whose structure-sheaf class lies in T^13. Finite transfer preserves support codimension. After passage to a common splitting field it maps that class to d_i*l3. The relevant K-theory restriction injectivity and rational l_j classes are the standard split-Clifford quadric facts used in the original p.12 proof. Thus the integer sum gives 8*l3 in T^13 without requiring any extension of degree exactly 8.

The integral relation can be checked geometrically. On the split quadric, a linear section of dimension j with rank-two restricted quadratic form is the union of two projective j-spaces meeting along a projective (j-1)-space. The structure-sheaf exact sequence and Koszul formula for the linear section give

    h^(16-j)=2*l_j-l_(j-1), j=1,2,3.

Iterating yields

    8*l3=l0+h^15+2*h^14+4*h^13.

The relation descends through the relevant K-theory identification. Every hyperplane term lies in T^13, hence l0 lies there. There is no division by 8 and no replacement of K-theory by Chow theory. A rational point on the anisotropic quadric is never assumed.

## Incidence and gamma challenge

Use the even maximal component, whose tautological bundle has rank 9. The incidence P(T)->X has relative dimension 8; its projection to the quadric is smooth, with a 28-dimensional homogeneous fiber. Thus pullback preserves codimension and pushforward lowers it by at most 8. Over a splitting field, the inverse image of a point on Y maps isomorphically to the special Schubert variety. The K-theoretic identity checked in a16i5 p.11 identifies its class with e8. Consequently

    l0 in T^13 implies e8 in T^(13-8)=T^5.

The original odd form and the exact field K meet [a16i5 Theorem 4.3](https://sites.ualberta.ca/~karpenko/publ/a16i5.pdf), so T=gamma there. This theorem and its proof were read on pp.9-11, including the maximal-index condition and the ordinary SB extension. Its argument compares K-theory and Chow-image indices, then uses the projective-bundle description of X times S to generate the associated graded by Chern classes. At n=8 both index exponents are 8*2^7=1024. The final generation-to-filtration step follows by finite descending induction. The proof does not infer topological-filtration equality from base change to an algebraic closure.

The core Panin K-theory theorem, the split flag Chow presentation, and the projective-bundle/Clifford facts remain literature dependencies, not independently reproved foundations. No circular use of the target nonmembership conjecture is needed. The actual proof on a16i5 p.12 is pointwise in dimension, so its conclusion really is the n=8 prohibited membership rather than only an unspecified failure of a universal conjecture.

## Adversarial disposition and exact remaining scope

The materially distinct challenges were: existence by valuations; independent index arithmetic and upper-bound construction; generic-torsor divisibility direction; transfer as a gcd; integral K-theory recurrence; incidence geometry; and special-field gamma equality. None produced a counterexample to the candidate's inference. Several tempting shortcuts would fail, but the submitted candidate explicitly avoids them: genericity equality, a degree-exactly-8 extension, division by 8, use of the odd rank-8 bundle against the even quadric, and topological-filtration equality after arbitrary base change.

The strongest verified result is

    exists F,phi with dim(phi)=17 and ind C0(phi)=256,
    K=F(SB(C0(phi))), X=OG8(phi), e8 in gamma^5 K0(X_K).

This is the full existential negation needed for problem 30003042. There is no claim that every n>=8 fails, that the optimal threshold is determined, that arbitrary models have exact index 8, that all characteristics were independently reconstructed, or that source theorem dependencies have disappeared. No new novelty or priority assessment was undertaken. No route was left blocked by an equivalent unsupported central conjecture; all remaining dependencies are identified published or standard theorems, with their authentication/read scopes in `SOURCE_LEDGER.json`.

## Root tooling feedback after the independent derivation

Before sealing, root observed that Python -O/-OO removes assertion checks. This was tooling feedback only, received after the two independent mathematical calculations and draft verdict; no peer mathematical results were supplied. All 18 checks were replaced by explicit ArithmeticError guards. Normal, -O and -OO runs now pass and emit byte-identical mathematical results; a deliberately false guard raises in every mode. The chronology and pre-correction program hash are recorded separately in TOOLING_FEEDBACK.json, and validation is recorded in TOOLING_VALIDATION.json. No version had been sealed when the feedback arrived.
