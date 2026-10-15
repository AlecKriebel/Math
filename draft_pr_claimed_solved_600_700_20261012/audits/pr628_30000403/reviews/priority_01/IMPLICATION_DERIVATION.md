# Prior compression theory implies the claimed Hurwitz bound

This is an authored priority-audit derivation, not a transcription of a source or a proposed new paper. It concerns PR628 at immutable head `677673860f9e67dffc610f52384f0bd60e65e363`. Its purpose is to expose every step between the earlier general theory and the exact coarse claim. The prior general results are identified in SOURCE_LEDGER.json; no unverified historical first claim is made.

## 1. Construct the correct faithful structured object

Let k have characteristic zero and let x be the reduced **inner coarse** Hurwitz k-point in the packet. Set H=PGL2 over k. Let F be the reduced scheme underlying the ordinary coarse fiber over x. Passing to the reduced fiber changes no field-valued points. The geometric quotient property gives a transitive H action on F geometrically; choosing p0 over the algebraic closure identifies F geometrically with H/E. Here E is the stabilizer of the **marked coarse cover point**, not necessarily the full stabilizer of its branch divisor. It is finite because r>=3 and E acts faithfully on the target and hence on its r branches.

Consider the quotient stacks

    G = [F/H],                 P = [(F x P1)/H],

where H acts diagonally. There is a representable morphism P -> G whose geometric fibers are P1. Over the algebraic closure one has

    G = BE,                   P = [P1/E].

Thus G is a finite étale gerbe, and P -> G is a genus-zero universal family. This is an instance of the compression formalism of Bresciani–Vistoli, arXiv:2210.04789v1, section 5.1, especially Definition 5.3 and the surrounding cartesian diagram (manuscript pp.10–11). Bresciani's arXiv:2303.01409v2, Definition 5, Lemma 6, Theorem 2 and Corollary 10, give an explicit general formalization of these faithful structures and twisted quotients.

The faithfulness condition is satisfied: an automorphism of an object of G is a subgroup of H acting on its associated genus-zero curve by the same inclusion into PGL2. In particular, the source-cover central automorphisms Z(G_deck) do not appear. One must **not** replace this gerbe by the gerbe of actual marked-cover objects, whose forgetful map to target curves can have central kernel. We have started from F, an already coarse Hurwitz fiber, precisely as the original question requires.

Let Y be the coarse space of P. After algebraic extension it is P1/E. In characteristic zero the quotient of P1 by a finite subgroup is a smooth projective genus-zero curve. Formation of this coarse space commutes with the flat field extension. Consequently Y itself is a smooth projective geometrically connected genus-zero curve over k, hence a conic. These are exactly the curves called compressions in the earlier sources.

## 2. The split-target bridge, with no second quadratic extension

Remove from P1 all points fixed by nonidentity elements of E. This removes a finite set: a nonidentity projective transformation has at most two fixed points. The resulting E action is free. Its image defines a nonempty open V in Y over k. The morphism P -> Y is an isomorphism over V, since there the quotient stack has trivial inertia. This free-open construction is explicit in Bresciani–Vistoli's proof of Theorem 5.4, arXiv:2210.04789v1, p.11; in the divisor instance see Bresciani, arXiv:2211.03438v1, section 1, pp.2–3, and the published paper section 3.4, p.88.

Suppose K/k is an extension and y belongs to V(K). It gives an actual K-point of the quotient stack P. By the definition of a quotient stack, this consists of an H-torsor T over K and an H-equivariant map

    T -> F x P1.

The P1 component is a K-section of the associated conic T x^H P1. An H=PGL2 torsor is determined by that genus-zero form of P1; a section makes the conic split. Hence T is trivial as an H-torsor. Choosing a trivialization of T and evaluating its F component gives a point of F(K).

Equivalently, the P1 component reduces T to a split Borel B=G_a semidirect G_m, and H1(K,B)=1 by additive and multiplicative Hilbert 90. Either description proves that the **same** field K supplies an ordinary coarse point on a **split** target. Merely obtaining an arbitrary conic cover and then adjoining another quadratic extension would not prove the claimed bound; that weaker argument is not being used.

This bridge uses no actual source-cover model, no centerless assumption, no choice of compatible source isomorphisms, and no assertion that the residue field k was the smallest possible absolute field of moduli. It works over the chosen k and all its finite extensions.

## 3. Every open conic has a point of degree at most two

The field k is infinite. Embed Y as a smooth plane conic, and choose a k-line which is not tangent and whose intersection with Y avoids the finite complement of V. Such lines form a nonempty open subset of the dual projective plane and therefore contain a k-point. The intersection is a reduced effective divisor of degree two supported in V. Its support contains a closed point of degree one or two. Take K to be that residue field. Section 2 gives F(K) nonempty, so

    m_k(x) <= [K:k] <= 2.

The only geometric input beyond the prior compression construction is the elementary index bound for a conic. No classification of all finite subgroups, Brauer period-index assertion, or unresolved descent problem is transferred into this argument. The bound is independent of the branch number, group, inertia classes and stabilizer.

## 4. Earlier theory also gives the V4 improvement

Bresciani, arXiv:2211.03438v1, Proposition 2, pp.3–4, considers an arbitrary finite étale gerbe Phi and a rational map Y -> Phi from a nonsplit genus-zero curve, with geometrically irreducible genus-zero fibers. It concludes in particular that the geometric band must be cyclic. This is not restricted to a reduced divisor in its statement. The same statement is Proposition 28, printed pp.89–91, in Journal of Algebra 647 (2024), 72–98, DOI 10.1016/j.jalgebra.2024.02.021.

Our rational map Y -> G has geometric form P1/E -> BE and geometric fiber a nonempty open of P1, so the hypotheses hold. If E=V4, it is noncyclic; therefore Y cannot be nonsplit. Since Y=P1 over k, V(k) is nonempty and Section 2 gives F(k) nonempty. Thus m_k(x)=1.

In fact this prior implication gives F(k) nonempty for **every noncyclic E**, which is stronger than the packet's stated V4 improvement. One can check the characteristic-zero reason directly from the branch signatures of P1 -> P1/E. For V4 the three branch points have signature (2,2,2); their descended divisor on Y has odd degree three, so Y is split. For D_(2n), n>=3, signature (2,2,n) supplies a distinguished rational branch point. For A4, S4 and A5 the signatures (2,3,3), (2,3,4), (2,3,5) likewise supply a distinguished branch point. This is the ramification mechanism behind the earlier proposition, not the packet's elliptic 2-torsion realization.

The trivial stabilizer E=1 is cyclic and permits a nonsplit conic. It is correctly covered by Section 3, not by the noncyclic conclusion. Nothing here asserts that every divisor with trivial stabilizer descends to a split line over k.

## 5. Sharpness was already known; the small certificate is a refinement

Cadoret's GPGL2 author manuscript, Remark 3.14, manuscript p.15, explicitly supplies C2-cover examples with cyclic target stabilizer C_n for odd n>=7 for which the lifting degree is two. The discussion uses Huggins' examples and identifies the relevant ordinary and reduced coarse fields of moduli. Thus, independently of whether the exact six-point formula in this packet previously appeared, examples needing two were already available before the universal upper-bound implication above. This is the appropriate use of Remark 3.14: its lower bound is verified prior evidence, while its expressed uncertainty and its nonoptimal upper bounds are **not** a prior proof of the universal theorem.

The packet's six branches over Q(i), with reduced point over Q and no real coarse lift, are a compact verified explicit certificate. Marinatto's 2013 divisor paper already constructs nonsplit-target examples for every even cardinality >=6, as independently reported and explained by Bresciani's published introduction, p.73. We have not obtained Marinatto's complete primary text in this audit and do not claim that his six-point formula or base field is identical to the packet's formula. No novelty certification is available for that formula.

## 6. Priority conclusion and exact limit

The full universal constant-two result, its uniform sharpness, and the V4 degree-one assertion are checkable short consequences of earlier general compression theory and earlier lower bounds. A safe independently dated prior chain is Bresciani–Vistoli v1 (10 October 2022), Bresciani divisor v1 (7 November 2022), and Cadoret's 2008 publication/author manuscript. Bresciani's 2023 structures theorem makes the generality particularly explicit. These sources need not have printed Cadoret's question verbatim for the implication to be valid.

This does not establish the earliest person who noticed that consequence, that it was historically considered a named solved problem in 2022, that all literature was searched, or that the packet's elliptic realization and exact numerical certificate were copied. The obstruction to a new-open-problem-resolution claim is the verified prior implication itself. A more explicit proof of a known consequence is a possible expository contribution, but it is a different publication claim and does not restore novelty of the central result.
