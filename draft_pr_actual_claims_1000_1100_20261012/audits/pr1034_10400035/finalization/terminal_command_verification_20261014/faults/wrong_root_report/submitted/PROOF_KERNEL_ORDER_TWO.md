# The order-two vanishing kernel is zero for every k ≥ 2

Problem 10400035 / AMR-103-0035, Stanford Question 2.13.
Continuation, substantive approach 2 of a shared maximum of 5.

**Disposition: scoped proof complete; independent audit requested.**

## 1. Exact claim and its limits

Let SL_k be ordinary unframed smooth ordered upward-oriented k-string links in D²×[0,1], with fixed matching endpoints and product endpoint collars. Upward refers to orientation, not height monotonicity. Let V_2(k) be rational ordinary Vassiliev invariants of order at most two, including constants, and let F_k be the string links with actual three-dimensional exterior group abstractly isomorphic to the free group of rank k. No special meridian-basis hypothesis is imposed. Put

N_2(k) = {v ∈ V_2(k): v(L)=0 for every L∈F_k}.

**Theorem. For every integer k≥2, N_2(k)=0.**

The theorem concerns the nontriviality clause at order two, for all strand counts at least two. It also gives N_n(k)=0 for k≥2 and 0≤n≤2 by inclusion V_n(k)⊆V_2(k). It does not decide N_n(k) for k≥2 and n≥3. The classical one-strand case is distinct: the normalized Conway coefficient is nonzero and vanishes on the unknot, the only one-strand free-exterior example under the classical cyclic-knot-group theorem. That familiar exception is not a consequence of the present proof.

The previously accepted first approach established the negative span result M_2(2)+N_2(2)≠V_2(2) and the entire-intersection formula M_2(2)=span_Q{1,ell,ell²}. Its files and independent audit are frozen and unchanged. The present proof does not need a general filtered Milnor-algebra theorem: it acts directly on the complete ordinary order-two space.

## 2. Complete order-two coordinates

Write c(K) for a knot's Conway z² coefficient, a_i(L)=c(the individual closure of strand i), ell_ij for pairwise linking, and

w_ij(L)=c(standard plat of the two-component sublink L_i∪L_j)−a_i(L)−a_j(L).

Let μ_ijk denote the based length-three string-link Milnor invariant in Meilhan's convention, for i<j<k. Meilhan's Theorem 2.4 [M], in the ordinary unframed fixed-endpoint category, gives every v∈V_2(k) an expansion

v(L)=Q((ell_ij(L))_{i<j}) + Σ_{i<j<h} d_ijh μ_ijh(L)
      + Σ_i b_i a_i(L) + Σ_{i<j} e_ij w_ij(L),            (2.1)

where Q is a polynomial of total degree at most two in all pairwise-linking variables. Its monomials include every square, every product with one shared strand, and every product on four distinct strands, as well as constants and linear terms. Thus (2.1) does not omit any quadratic part of the classification. We only need the asserted spanning formula.

## 3. What pure braids detect

### 3.1 Their exteriors and knot/plat coordinates

Every ordinary pure braid belongs to F_k. Its exterior is the product, up to the braid's height-dependent disk trivialization, of a k-punctured disk with an interval. Its actual group is F_k. This is the forward braid implication only.

Each individual strand of a pure braid is an unknotted long arc. Deleting all but two strands gives a two-strand pure braid. Every two-strand braid has unknotted two-plat closure: its successive twists are removed against an endpoint cap, or equivalently its plat has one bridge. Consequently

a_i(P)=0 and w_ij(P)=0 for every pure braid P.       (3.1)

### 3.2 A triple test with an exact Magnus calculation

On three strands take A=σ_1², B=σ_2² and the pure braid β=ABA^{-1}B^{-1}. Every two-strand deletion is the identity braid: deletion makes either A or B trivial, after which the remaining factor cancels its inverse. In particular all pairwise linking numbers of β are zero.

For precision, use the Artin action

Φ_{σ_i}(x_i)=x_i x_{i+1} x_i^{-1},
Φ_{σ_i}(x_{i+1})=x_i,

fixing all other generators, and use Φ_{AB}=Φ_A∘Φ_B for the written product of automorphisms (the rightmost map acts first). For a pure braid write Φ(x_j)=c_j x_j c_j^{-1} and normalize the exponent sum of x_j in c_j to zero. Multiplication of c_j on the right by a power of x_j does not change the conjugation, so this is the preferred self-linking normalization. The crossing and longitude interpretation follows the Wirtinger/parallel description in [BN], Sections 4.1 and 5.2; that source's displayed conjugation direction may invert the c_j. We use the standard Magnus expansion x_i↦1+X_i, not its optional exponential normalization.

A direct free-word calculation for β gives

c_1 = x_1 x_2 x_1^{-1} x_3 x_1 x_2^{-1} x_1^{-1} x_3^{-1},
c_2 = x_3^{-1} x_1^{-1} x_3 x_1,
c_3 = x_3^{-1} x_1^{-1} x_3 x_1 x_2^{-1} x_1^{-1}
      x_3^{-1} x_1 x_3 x_1 x_2 x_1^{-1}.

Their Magnus expansions through degree two are

E(c_1)=1+X_2X_3−X_3X_2+O(3),
E(c_2)=1−X_1X_3+X_3X_1+O(3),
E(c_3)=1+X_1X_2−X_2X_1+O(3).                     (3.2)

All linear terms are zero. Thus the selected triple Milnor value is ε=±1, with the sign depending only on whether the longitude convention uses c_3 or its inverse. The nonzero magnitude is all that is used. Meilhan's possible lower-linking corrections between basings/orders vanish here because every pairwise linking number is zero.

These word substitutions, inverse-generator identities, the Artin braid relation, all three deletion identities, and the standard Magnus truncations are checked exactly in a supplementary script not included in this theoretical edition. They are also explicit finite algebra in (3.2), not an inference from a claimed closure picture.

### 3.3 Any labeled triple, including nonadjacent labels

Choose any three distinct labeled endpoints. There is a subdisk of D² containing exactly these points and no others; braid the three points inside it by the above β and leave all outside points vertical. Equivalently, identify a standard three-punctured disk with this subdisk, preserving orientation and the selected labels. This is still a pure braid on all k strands.

It has zero pairwise linking everywhere. Its selected triple Milnor value remains ±1. To check basing, an ambient meridian for an active strand is a conjugate of its local meridian, with the same degree-one Magnus term. Substituting conjugate meridians into a longitude whose first nonconstant term has degree two does not change that degree-two term. Conjugating the longitude likewise does not change it. Hence inclusion into the larger marked disk preserves (3.2) with labels substituted; it cannot introduce an outside variable at degree two.

Alternatively, deletion to a triple different from the chosen one leaves at most two active strands; the resulting braid is the identity because every such deletion of β is the identity, while the inactive strands are stationary outside the supporting disk. Naturality of the based Milnor invariants under deletion makes all other distinct-index triple values zero. This proves an isolating pure-braid test for every d_ijh in (2.1).

### 3.4 Arbitrary linking vectors and all quadratic terms

There is a pure braid with any prescribed integer vector of pairwise linking numbers. For each unordered pair, use a positive full twist supported in a small disk containing that pair, along an arc avoiding every other point. Its linking with that pair is 1 and its other pairwise linking numbers are zero. Powers and products of these generators realize any integer vector, because linking numbers add under braid multiplication. This multiplication is only used within pure braids, whose free exteriors have already been proved.

Suppose v∈N_2(k). Evaluation on the identity gives Q(0)=0. On the triple tests, (3.1), zero linking, and isolation of one triple give ε d_ijh=0. Hence every d_ijh is zero. Evaluating on arbitrary-linking pure braids now gives Q(z)=0 for every z∈Z^{binom(k,2)}. A rational polynomial vanishing on that full integer lattice is zero, by induction on the number of variables and the one-variable root theorem. Thus every coefficient of Q is zero.

We have reduced (2.1) to

v(L)=Σ_i b_i a_i(L)+Σ_{i<j} e_ij w_ij(L).          (3.3)

This establishes the necessary faithfulness of the entire degree-at-most-two linking/triple part on pure braids; no unstated all-order faithfulness theorem is imported.

## 4. Two certified free two-string witnesses

### 4.1 Rational witness R

Take the rational tangle R=[1]+1/[2] in the Kauffman–Lambropoulou convention. Its fraction is 3/2, with vertical connectivity NW–SW and NE–SE. Mark the southwest/southeast endpoints as the bottom ones, northwest/northeast as the top ones, and choose the ball-to-cylinder identification to carry both numerator cap arcs to the standard bottom/top plat caps.

The complete primary drawing in [KL-D], p.30, Figure 20, identifies its numerator as a trefoil. [KL-K], Section 5, Theorem 6, verifies the vertical connectivity; the explicit three-crossing endpoint trace gives the same result. Rationality is an actual homeomorphism of the ball pair to a trivial two-tangle, so the exterior is a genus-two handlebody. Each individual arc is boundary-parallel; after forgetting the other strand its closure is an unknot. The cap-preserving marking makes the standard plat exactly the cited trefoil. Therefore

(a_1(R),a_2(R),w(R))=(0,0,1).                    (4.1)

The separate lemma RATIONAL_FREE_WITNESS.md proves all marking, cap, smoothing, exterior and individual-closure details. Arbitrary endpoint re-markings are not claimed to preserve the plat. No numerical value of ell(R) is needed.

### 4.2 Nogueira witness L and exchanged labeling L^s

Use Nogueira's complete Coimbra preprint 14–09 appendix [N], pp.14–15, Figures 9–10. The source constructs a free two-tangle, with first capped arc a trefoil and second capped arc the torus knot T(3,−4). Its tunnel construction gives an actual genus-two handlebody exterior. Smooth its finite PL arc system and choose an ordinary endpoint marking, as in the accepted geometric lemma. Individual capped knot types are preserved under this marking, since the other strand is forgotten before comparing boundary caps.

Unlike the first accepted proof, the present step uses the source's explicit second-strand identification as well. Willerton [W], §1, identifies v_2 with the Conway z² coefficient and, in §3, gives the normalized torus formula

c(T(p,q))=((p²−1)(q²−1))/24.

Consequently c(T(3,−4))=8·15/24=5. Mirroring or reversing the individual knot does not change this even coefficient. Thus

(a_1(L),a_2(L))=(1,5).                            (4.2)

A separate copy with the component labels exchanged and endpoints carried to their new matching locations gives L^s, still a smooth ordered fixed-endpoint string link with the same free exterior, and

(a_1(L^s),a_2(L^s))=(5,1).                        (4.3)

For example, use a product disk diffeomorphism exchanging the two basepoints and then relabel the carried strands. This is a construction of a new labeled example, not a quotient of the string-link category. Neither w(L), w(L^s), nor their linking numbers is needed. They may be different and are left unspecified.

Both witnesses are source-backed geometrically certified examples. We do not claim independent machine recognition of their group or knot types from a marked crossing list. Source PDFs and page renderings are private evidence.

## 5. Adding separated trivial strands: exact freeness and cross-pair values

Fix a selected pair {i,j} of the k endpoints. Choose a proper separating arc δ in the base disk, avoiding all endpoints, which cuts off a subdisk containing exactly p_i,p_j. Such an arc exists by taking a thin regular neighborhood of an embedded tree joining the two selected points to a boundary interval, avoiding the finite other points. Its complement is another disk. Identify the cut-off disk, with its two points, with the base disk of a given two-string witness, put that witness into its product subcylinder, and put all other strands vertically in the other subcylinder. Denote this split inclusion by J_ij.

### 5.1 Group freeness under this particular operation

The properly embedded disk δ×[0,1] is disjoint from all strings and from sufficiently small regular neighborhoods of them. Cutting the full exterior along that disk separates the given two-string exterior from the trivial (k−2)-string exterior. Their intersection in the uncut description is a disk. Van Kampen gives

π_1(E(J_ij(S))) ≅ π_1(E(S)) * F_{k−2}.

If S has free exterior F_2, the result is F_k. For k=2 the second factor is trivial. In the present examples both pieces are handlebodies, and this is also their boundary connected sum. This proves freeness for the exact separated-trivial-strand insertion being used. It is not a statement about arbitrary stacking, arbitrary gluing, or deletion of strands from free exteriors.

### 5.2 Every component and plat coordinate needed

The two active component coefficients retain their original values; every other a_h is zero. On the active pair, the product identification carries the original top/bottom caps into the subdisks. After deleting the inactive strands, these cap arcs are isotopic in the endpoint disks to the standard caps, so w_ij retains the original two-string value.

For a mixed pair consisting of one active component and one outside straight component, the inherited separating disk puts the two long arcs on opposite sides. The standard top and bottom caps can be chosen to cross that disk once each: after deleting the other strands there are no extra punctures constraining these cap isotopies. Complete the separator to a sphere in the outside closure ball. It meets the plat knot in exactly two points and exhibits that plat as the connected sum of the individual knot closures, with a possible orientation reversal of one summand. Conway additivity under connected sum and orientation invariance therefore give

w_{active,outside}=0.

Pairs of outside strands are trivial and also have w=0. Thus no uncomputed cross-pair plat term enters the coefficient tests. Forgetting components here is used to evaluate the already-defined a and w functions only, never to infer that a forgotten-component exterior is free.

## 6. Eliminate all remaining coefficients

For every pair i<j, evaluate (3.3) on J_ij(R). Its exterior is F_k by §5.1; all component coefficients are zero, w_ij=1, and every other w is zero by §5.2. Therefore e_ij=0 for every pair.

Now v=Σ_i b_i a_i. Evaluate on J_ij(L) and J_ij(L^s). Freeness is again proved by §5.1, and all inactive component coefficients are zero. Equations (4.2)–(4.3) give

b_i+5b_j=0,     5b_i+b_j=0.

The determinant of this system is 1−25=−24, hence b_i=b_j=0 over Q. Since k≥2, choosing pairs (1,j), j=2,…,k, kills every b_i. Therefore v=0. This proves N_2(k)=0 for every k≥2.

For k=2 the entire six-coordinate free-exterior evaluation matrix can be displayed with unknown linking and plat values:

columns: (1,ell,ell²,a_1,a_2,w)
P_0:   (1, 0,   0, 0,0,0)
P_1:   (1, 1,   1, 0,0,0)
P_-1:  (1,−1,   1, 0,0,0)
R:     (1, r, r², 0,0,1)
L:     (1, s, s², 1,5,u)
L^s:   (1, t, t², 5,1,v).

Its determinant is −48, independently of r,s,t,u,v. This proves full rank six without computing any marking-dependent linking number or the Nogueira plats. The general-k proof is the same coefficient elimination augmented by the isolated triple tests.

## 7. Source identities and verification

[M] J.-B. Meilhan, *On Vassiliev invariants of order two for string links*, arXiv:math/0402036v2 (10 November 2004), Theorem 2.4, §2.1 and Definitions 1.1–1.3. https://arxiv.org/pdf/math/0402036v2 . The exact source already retained for turn 1 is used read-only.

[BN] D. Bar-Natan, *Vassiliev homotopy string link invariants*, J. Knot Theory Ramifications 4 (1995), 13–32; author PDF edition 17 February 2015, §§4.1,5.2. https://www.math.toronto.edu/drorbn/papers/homotopy/homotopy.pdf . Only braid exterior, Wirtinger and longitude interpretation are used; the repeated-index Milnor-algebra theorem is not needed in this continuation. Standard integer Magnus normalization is stated explicitly in §3.2 above.

[N] J. M. Nogueira, *Knot complements with meridional essential surfaces of arbitrarily high genus*, Coimbra preprint 14–09, received 27 February 2014, Appendix §4, pp.14–15, Figures 9–10. https://www.mat.uc.pt/preprints/ps/p1409.pdf . The complete retained source is used read-only; in addition to the previously used first-strand/freeness assertions, its second-strand T(3,−4) assertion is now used explicitly.

[W] S. Willerton, *On the first two Vassiliev invariants*, arXiv:math/0104061v1 (5 April 2001), §1 p.1 and §3 p.5. https://arxiv.org/pdf/math/0104061v1 . Retained PDF 402625 bytes, SHA256 7a86e5bdfdc024ff9938eb5e294b807cdb85efe40088d132c1372d4f136f29f7. The publisher request returned a bot-block HTML page, not a PDF; no publisher-byte or inspected-publisher claim is made.

[KL-D] L. H. Kauffman and S. Lambropoulou, *From Tangle Fractions to DNA*, author-hosted PDF, p.30/Figure 20. https://homepages.math.uic.edu/~kauffman/Dresden.pdf . Retained PDF 1388506 bytes, SHA256 53cd49ea0448fe796c3baa07e2246f89d16352398293cb0e2b1d9019dbfa5fd1.

[KL-K] L. H. Kauffman and S. Lambropoulou, *On the Classification of Rational Knots*, arXiv:math/0212011v2 (27 November 2003), pp.6–9,20–21,39–41, especially Theorem 6. https://arxiv.org/pdf/math/0212011v2 . Retained PDF 459279 bytes, SHA256 de77c7cf69cd5464ed7b9044dc4842004c23c5c2820f334c30b5ecbd8cf4fc10.

The rational-witness inspection covered the complete specified figures and endpoint/cap conventions. The torus formula's normalization and the exact appendix second-strand sentence were read. Exact checks verify free-word substitutions, Magnus coefficients, polynomial determinants, and selected negative controls, not smooth embeddings or the truth of the cited geometric sources. The source-backed assumptions remain visible for independent mathematical audit.

## 8. Completion boundary

This is approach 2, extending the finite-basis free-evaluation mechanism from two strings to all k≥2. It is not four separately charged approaches for its lemmas. Proof search stops at this scoped theorem and requests independent audit. There are three unspent approaches in the shared five-approach cap. No source or audit input in the accepted turn-1 packet was changed; no queue edit, publication, outreach, or novelty claim occurred.
