# Independent audit of the semiglobal homogeneous space counterexample

## Verdict

**PASS, full prior resolution.** Problem 30001148 / OWR-3388-006 has a published negative answer in the scope stated in the original 2009 report. The frozen author's recommendation `already_solved`, with one substantive turn used out of five, is justified. This is recovery of prior mathematics, not a new discovery, a formal proof certificate, or human peer review.

The decisive route is Colliot-Thélène, Parimala and Suresh (CTPS), *Lois de réciprocité supérieures et points rationnels*, Corollary 5.3 and Example 5.6(a). The second route, using a constant torus and the corrected six-author 2020 paper (CHHKPS), also passes. Neither route depends on Theorem 6.5 of that paper. No mathematical correction to the frozen result is required.

## Reviewed bytes and preservation

The author manifest SHA-256 is:

    380647dacb6bbc1e7c31784712465143b5feb90ff124a57c666c74cae68b0e2c

The reviewed `RESULT.md` SHA-256 is:

    dc851afdbd36a290d61b07b23c2b1ab389cbc44873e242092935400930d74303

All seven payload sizes and hashes match the manifest. The manifest plus those payloads are exactly eight files. This audit and its controls are separate, additive files; the frozen release remains unchanged. The author checker was run read-only and reproduced its original 21-check JSON receipt byte-for-byte under SymPy 1.14.0. The separate audit checker passes 22 integrity, algebra, and finite-bookkeeping controls. These counts do not measure or certify the arithmetic theorem.

## Exact target and scope

The original contribution occupies printed pages 317–318 of [OWR 05/2009](https://publications.mfo.de/bitstream/handle/mfo/3106/OWR_2009_05.pdf?isAllowed=y&sequence=1). Both pages were inspected in their full context, including the statement spanning the page break. It asks whether a homogeneous variety under a connected linear group over a one-variable function field F of a complete discretely valued K must have an F-point if it has points in every rank-one discrete completion. Valuations nontrivial on K are explicitly included. Neither projectivity of the homogeneous variety nor finiteness of the residue field is assumed. The latter is introduced subsequently for a separate specialization.

A torsor under a connected torus is already a homogeneous variety in the specified class. Its trivial geometric stabilizer satisfies smoothness and connectedness as well. Consequently a single such torsor with the required local points negates the full question. The title's reference to p-adic curves cannot override the broader displayed hypotheses.

## Decisive route over C((t))

### Field and model hypotheses

Take A=C[[t]], K=C((t)), and the smooth projective curve C whose affine equation is y²=x³+x²+t³. The cubic polynomial has discriminant −t³(4+27t³), so the affine curve is smooth; the point at infinity in its projective Weierstrass model is smooth as well. It is an elliptic curve, and F=K(C) is a one-variable regular extension of K.

A is a complete excellent henselian DVR; its residue field C is separably closed of characteristic zero. In particular, 2 is invertible. CTPS Lemma 5.5 identifies the proper minimal regular model as having split I₃ reduction, and Example 5.6(a) expressly applies it to this curve. The Weierstrass invariants independently check the reduction calculation: c₄=16 and Δ=−16t³(4+27t³), giving multiplicative reduction of order three; the two tangent directions of the reduced node are defined over C. The three smooth rational components meet pairwise transversely at distinct C-points. Thus the model is integral, regular, projective over A, with smooth geometrically integral generic fiber and the triangle required by Corollary 5.3.

### Functions and the acting group

The functions π₁,π₂,π₃ are existential choices with the full divisor avoidance conditions of CTPS §5.2. They are not arbitrary uniformizers. Each divisor is Lᵢ+Dᵢ; the extra supports avoid the triangle vertices, each other's components, and the specified intersection points. This makes the restriction at the three vertices the semilocal configuration used in Proposition 5.1, and ensures at least one πᵢ is a unit at every closed point of the model. The release correctly invokes those choices rather than supplying unsupported formulas.

Set a=π₂π₃, b=π₃π₁, c=π₁π₂π₃ and let E be the norm-product fiber displayed in the release. Each quadratic algebra is finite étale because its parameter is nonzero and the characteristic is zero. Over a separable closure, the product of the three norm maps is multiplication on six invertible coordinates. The character map has primitive vector (1,1,1,1,1,1), so its kernel is Gₘ⁵. The kernel G over F is therefore a smooth connected affine torus of dimension five. Since c is nonzero, every norm factor on E is invertible. The action of G on E is geometrically free and transitive: E is a G-torsor, hence a smooth geometrically integral homogeneous F-variety with trivial stabilizer.

### Why all valuations really occur

Corollary 5.3(i) is explicitly quantified over every discrete valuation; CTPS's introductory convention specifies rank one with value group Z. It is not merely a list of divisors on a fixed model.

The proof's extension from model points to arbitrary valuations can be checked directly in the present example. Every unit of A has iterated square roots in A. A homomorphism from this 2-divisible unit group to Z is zero, so any discrete valuation w of F vanishes on A×. As t=1−(1−t), the valuation inequality gives w(t)≥0; hence A is contained in the valuation ring of w. Properness of the model supplies a center, including when w restricts nontrivially to K. Applying this also to the henselian valuation ring reduces the question to the two types of center covered by Proposition 5.2.

At codimension-one points the residue fields have 2-cohomological dimension at most one: vertical components have one-variable function fields over C, and horizontal points have finite extensions of C((t)). The divisor avoidance conditions imply that at most one πᵢ has nonzero order there. If the orders of a and b are both even, the order of c is even; otherwise one of the first two orders is odd. Thus the forbidden pattern in Proposition 4.2 cannot occur, giving local solubility.

At a closed center the residue field is C. Choose i with πᵢ a unit and choose r with r²=−πᵢ in the henselian local ring. Explicit local points are obtained by setting the unused norm pairs to (1,0), and using the following remaining pair:

- If i=1, use (X₁,Y₁)=(0,r).
- If i=2, use (X₂,Y₂)=(0,r).
- If i=3, use (X₃,Y₃)=(0,1/r).

The resulting product is c in each case. This verifies the relevant closed-center argument without relying on compressed coordinate prose in the source.

Finally, the henselization of a discretely valued field embeds over that field into its completion by the universal property of henselization. Points over the henselization therefore give points over the completion. No converse or approximation argument is required.

### Why no global point exists

The source's global contradiction is the residue-complex calculation in Proposition 5.1. Its arithmetic inputs are the quaternion residue calculations of Proposition 4.3 and the fact that consecutive residue maps in the dimension-two Bloch–Ogus/Kato complex compose to zero. Exactness of an unproved Gersten conjecture is not needed for this step.

In the semilocal surface at the three vertices, the potential residue boundary vectors in (Z/2)³ have the following choices, one from each row:

    L₁: (0,0,1) or (0,1,0)
    L₂: (0,0,0) or (1,0,1)
    L₃: (0,0,0) or (1,1,0)

Their sum cannot vanish: the sum of its three coordinates is always one modulo two. The first row has odd coordinate sum, and the other rows have even coordinate sum. Other divisors contribute zero because a,b,c are units there. A hypothetical F-point would evaluate the quaternion class to a global Brauer class and force the total boundary to be zero, a contradiction. This recovers the actual obstruction underlying Proposition 5.1, Proposition 5.2(i), and Corollary 5.3(ii).

Accordingly E(F) is empty while E(F_w) is nonempty for every required w. This route alone establishes the verdict. The flasque-resolution identification used in the second route is not needed here.

## Independent constant torus corroboration

### Explicit data and elementary checks

The second construction uses k=C((u))((v)), R=k[[t]], K=k((t)), L=k(√u,√v), and T=R¹_{L/k}Gₘ. The symbols are independent. Successive v-adic and u-adic parity checks prove u and v independent modulo squares; hence L/k is biquadratic and T is a three-dimensional connected torus. A flasque resolution over k extends by base change to R and to the model. There is no finite-residue-field requirement in the invoked theorem.

The quadratic form ⟨1,u,−v⟩ is anisotropic. The binary form ⟨1,u⟩ is anisotropic over C((u)) by u-adic parity. Consequently a nonzero value x²+uy² over k has even v-order, including when x and y have equal v-order because their residual leading terms cannot cancel. The term vz² has odd order if z is nonzero. The cases with zero entries cause no exception.

Let N be the group of norm-one elements of L× and I the augmentation subgroup generated by g(w)/w. The element i∈C has norm one. If i=(σ(r)/r)(τ(s)/s), put θ=σ(r)/r and write θ=A+B√u+C√v+D√uv. Its norms to k(√v) and k(√u) are 1 and −1. Their constant terms add to 2(A²−uvD²)=0. Since uv is nonsquare, A=D=0. The first norm then gives 1+uB²−vC²=0, contradicting the anisotropy just proved. Therefore [i] is nonzero in N/I. The class has order two: i²=−1=σ(√u)/√u. This is an additional consistency check, not a replacement for the nonvanishing argument.

The model Proj R[x,y,z]/(xyz−t(x+y+z)³) is projective and flat over R: reduction of its defining equation modulo t is nonzero, and its affine-chart quotients have no t-torsion. The smooth generic fiber is integral, implying the total model is integral. For a generic singular point, the three derivative equations give yz=xz=xy=3t(x+y+z)². The zero-sum case is impossible projectively; otherwise x=y=z and 27t=1, also impossible. Thus the generic cubic is geometrically smooth and integral.

At [0:0:1], the local relation t=xy/(1+x+y)³ gives regular parameters x,y and two transverse branches. The other vertices are identical by symmetry; elsewhere the special fiber is smooth. Every component is P¹_k, and the three intersections are k-rational. The dual graph is a triangle; the bipartite patching graph is its six-cycle subdivision. Both have first integral Betti number one.

### Arithmetic theorem chain and corrected version

CHHKPS §8.1 identifies H¹(k,S) for a flasque resolution of the norm-one torus with the Tate group N/I, crediting Colliot-Thélène–Sansuc (1977), Proposition 15. Example 8.1 supplies the relevant nonvanishing mechanism. This published identification is explicitly an input, not a newly proved claim.

The needed comparison is Theorem 4.4: for a torus extending over the normal-crossings model, the patching kernel equals the kernel over all discrete-valuation completions defined in §1.2. Theorem 6.4(c) then gives Sha(F,T)≅H¹(k,S) because the model has rational components, rational nodes, and one cycle. Its proof runs through the graph/coefficient comparison in Lemma 6.2 and Proposition 6.3. All their base and extension hypotheses are met here.

The corrected [arXiv v3](https://arxiv.org/abs/1906.10672v3), dated November 23, 2020, was checked rather than relying solely on the publisher copy. The correction notice concerns Theorem 6.5, with associated rewording. Theorem 4.4, Theorem 6.4(c), and Examples 8.1 and 8.7 retain the inputs used above. This construction requires none of the disputed extra injectivity or generality of Theorem 6.5.

A nonzero class of Sha(F,T) corresponds to a T_F-torsor Y. Its class is nontrivial globally and trivial in every required completion, giving precisely the same negative answer. An explicit cocycle or affine equation for this particular Y is not necessary to refute an existential implication; the existence follows from the verified nonzero cohomology class and the stated arithmetic theorem.

## Exclusions and interpretation controls

- Neither displayed complete base field is a finite extension of Q_p. The review does not turn these two examples into a p-adic-specific construction, or suggest that all p-adic variants remain open.
- The torsors are positive-dimensional affine varieties. Compactification does not preserve transitivity automatically. No projective-homogeneous counterexample is claimed.
- The original rational-group positive theorem has additional rationality and extension hypotheses. It cannot be applied to arbitrary connected tori by omitting rationality.
- Linh's [2024 paper](https://arxiv.org/abs/2211.08986v2), Theorem A and introduction, uses p-adic function fields, a specified class of stabilizers, generic-curve places, and a refined cohomological obstruction. Its assertion is not bare local solubility implying a global point. It does not undo either counterexample.
- The live catalogue's current page state and any exhaustive repository duplicate claim were not certified by this audit. The exact source question and its mathematical resolution are independently established. The author's bounded duplicate-search description is appropriately qualified.
- The public audit files contain analysis, citations, hashes and original controls only. Full papers, extracted source texts, screenshots, raw catalogue/corpus material, private coordination, credentials and unrelated context are excluded.

## Sources and reproduction

Primary references, with locations actually checked:

1. [OWR 05/2009](https://doi.org/10.4171/OWR/2009/05), contribution on printed pp. 317–318; full two-page scope inspection.
2. [CTPS final arXiv v3](https://arxiv.org/abs/1302.2377v3), §1 conventions; §2.1 residue complex; §3.1 torus description; Propositions 4.2–4.3, 5.1–5.2; Corollary 5.3; Lemma 5.5; Example 5.6(a). Published in Transactions AMS 368 (2016), 4219–4255, [DOI 10.1090/tran/6519](https://doi.org/10.1090/tran/6519).
3. [CHHKPS publisher paper](https://content.algebraicgeometry.nl/2020-5/2020-5-022.pdf) and [corrected v3](https://arxiv.org/abs/1906.10672v3), §1.2; Theorem 4.4; §6.1, Lemma 6.2, Proposition 6.3, Theorem 6.4(c); §8.1, Examples 8.1 and 8.7. Published in Algebraic Geometry 7 (2020), 607–633, [DOI 10.14231/AG-2020-022](https://doi.org/10.14231/AG-2020-022).
4. [Linh v2](https://arxiv.org/abs/2211.08986v2), introduction and Theorem A; [DOI 10.1112/jlms.12842](https://doi.org/10.1112/jlms.12842).

The primary reading copies match the source hashes recorded in the frozen `SOURCE_AUDIT.md`. The official OWR PDF, CHHKPS publisher PDF, and corrected v3 were independently opened; version histories were checked. The CTPS PDF endpoint failed in the web reader, but its full local v3 PDF was readable, its SHA-256 matched, its version identification was checked, and its decisive pages were visually inspected. That reader failure does not leave the theorem text unverified.

Run `python audit/controls/audit_controls.py release` from a directory containing the frozen `release` and additive `audit` directories. It prints JSON and never writes into the release. The author checker is separately reproducible with `python release/checks/check.py`. During audit-control development, a structural symbolic equality test was changed to compare an expanded difference; no mathematical formula changed. Final controls pass.

The audit's stopping condition is met: exact target, decisive published theorem, full application hypotheses, all-valuation coverage, group/stabilizer class, source-version issues, and package integrity have been checked. No publication or remote mutation was performed by this review.
