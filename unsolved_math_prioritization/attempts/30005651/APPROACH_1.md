# Approach 1: field-orbit reduction and representation-theoretic presentation obstructions

Target: rank 1205, corpus 30005651, source OWR-14297741-001.

Date: 10 October 2026 UTC. Corrected partial-result edition; approach 1/5.

## Disposition

**Partial result; the original stable-connectivity question is not solved.**

The rigorous output is:

1. A dimension bound for motivic localization evaluated on an essentially smooth equivariant scheme. In particular, localization of a Nisnevich-connective spectral sheaf is connective on every zero-dimensional equivariant field orbit, for every finite tame group.
2. An exact subgroup restriction/localization comparison. It imports an already established connectivity theorem for a subgroup to stalks with that set-theoretic stabilizer. Consequently, stabilizers of order at most two are covered by the nonequivariant theorem and Bachmann's published theorem.
3. Connectivity at all geometrically free equivariant Nisnevich germs over an infinite perfect field. Together with the subgroup reduction, this proves Nisnevich-local connectivity on the punctured standard S3-representation over C, using **all** scheme points. Its origin remains unresolved.
4. A representation/codimension obstruction to smooth finite-support presentations. The rank-one obstruction is explicitly credited to Heller--Voineagu--Østvær (2015); its codimension formulation and worked S3 example are proved here without a novelty claim.
5. Explicit reasons why field evaluation, closed-point testing, free atlases, and naive quotient induction do not close the remaining gap.

There is no constructed connective E whose motivic localization has negative homotopy. Conversely, no field-detection theorem for the uncovered nonabelian germs is proved. Presentation failure is not a counterexample to connectivity.

## 1. Exact problem and conventions

Let k be an infinite field and G a finite constant group with |G| invertible in k. Let Sm_k^G be the usual smooth equivariant site, with the ordinary equivariant Nisnevich topology. A covering has, over each scheme point x, a lift y inducing both an isomorphism of residue fields and equality of **set-theoretic** stabilizers. An equivalent description uses equivariant Nisnevich distinguished squares.

Write Sh_Nis(Sm_k^G, Sp) for spectral Nisnevich sheaves. The t-structure is the local one:

    E >= 0  iff  a_Nis pi_i(E) = 0 for every i < 0.

This does not say that E(X) is connective for every positive-dimensional X. Its negative homotopy can contain positive Nisnevich cohomology of the homotopy sheaves of E. Connectivity throughout this report means this spectral >=0 convention. Integer shifts translate any alternative connectedness convention in the workshop wording.

Let L_G be localization at projections X x A^1 -> X, where the interval A^1 has trivial G-action. The question is whether L_G preserves the local connective part for the full class above. This is S^1-spectral localization; no unannounced representation-sphere or P^1 stabilization is used.

The source is Bachmann's contribution to OWR 40/2023, pp.2309--2311. The published C2 theorem is Proposition 3.2(2) in the inspected arXiv:2310.08125v2, with journal version Journal of Algebra 667 (2025), 587--597. The public Sandeep--Sawant preprint assumes G abelian and primitive |G|-th roots of unity in k. The 7 October 2026 Belfiori seminar listing does not supply a complete theorem over nonsplitting fields or nonabelian groups. These are prior inputs, not discoveries of this approach. See SOURCE_LEDGER.md.

## 2. General dimension bound, with the localization interface proved

### 2.1 Spectral singular construction preserves Nisnevich descent

For a spectral presheaf E set

    Sing(E)(X) = | [n] -> E(X x Delta^n_k) |,

where Delta^n_k = Spec(k[t_0,...,t_n]/(sum t_i - 1)) has trivial G-action. As a scheme it is A^n_k.

Assume E is a Nisnevich sheaf. Multiplication of a distinguished square by Delta^n preserves the defining properties: the open immersion, the étale map, and the isomorphism over the reduced closed complement. Thus every degree of Sing(E) carries that square to a pullback square of spectra.

Geometric realization in spectra preserves finite limits: it preserves finite colimits, and in a stable category finite limits and finite colimits agree. It also preserves the value zero at the empty scheme. Therefore Sing(E) is again excisive for the equivariant Nisnevich distinguished squares.

The complete, regular, bounded cd-structure identifies this excision condition with Nisnevich descent. The boundedness here is by Krull dimension, locally on the site; it is not an assumed connectivity theorem. This is the geometric input of Heller--Voineagu--Østvær, Theorem 3.8 and Corollary 3.9. The usual finite-dimensional Nisnevich setting is locally of finite homotopy dimension, so the corresponding spectral descent/Postnikov calculations apply. There is no replacement by étale, fixed-point, or isovariant descent.

The algebraic singular construction is A^1-invariant, and E -> Sing(E) is an A^1-local equivalence. These statements use the contraction of the standard algebraic simplices and the interval structure, which is equivariant because the interval action is trivial. They do not use Gersten injectivity or stable connectivity. Consequently

    L_G E = Sing(E)

for a spectral Nisnevich sheaf E. This is also the localization formula used in Bachmann's Proposition 3.2, footnote 5. For an arbitrary presheaf first apply Nisnevich localization; local connectivity is unchanged by this first step.

### 2.2 Evaluation bound before realization

Let T be a noetherian essentially smooth G-scheme of finite Krull dimension d; evaluations on such objects use continuity. If E is Nisnevich-connective, then

    E(T x Delta^n) >= -d-n.                                      (2.1)

Indeed, the ordinary equivariant Nisnevich cohomological dimension of T x Delta^n is at most d+n. For its connective spectral sheaf restriction, the finite-dimensional descent spectral sequence has terms

    H^p_Nis(T x Delta^n, pi_q^Nis E)  ==>  pi_{q-p} E(T x Delta^n),

with q >= 0 and 0 <= p <= d+n. Nothing can contribute below -d-n. The bounded cohomological direction justifies this lower bound without an unbounded spectral-sequence convergence assumption.

For clarity about the essentially smooth interface, extend E by filtered colimits along finite-type smooth models with affine transition maps, using affine charts and Nisnevich descent when the object is not affine. Étale morphisms of finite presentation, their finite diagrams, and the distinguished-square relations descend along these affine inverse limits. Every Nisnevich stalk of the resulting small equivariant étale site is represented by a corresponding limit of ordinary equivariant Nisnevich neighborhoods. Negative homotopy sheaves therefore still vanish on the small site. The cd-bound is then applied to the noetherian scheme **T x Delta^n itself**, whose dimension is d+n. One must not substitute the dimensions of its finite-type approximating models.

The same dimension proof for the equivariant cd-structure works on this small site: its étale objects are noetherian, invariant open complements give the usual density structure, and finite G-orbits do not increase the length of specialization chains. Alternatively, the small étale quotient-stack presentation yields the same bound as BKRS Proposition A.4.4; this alternative is not used to claim an equivalence of global motivic t-structures.

### 2.3 Realization restores the simplicial degree

Here is the needed stable-category lemma, avoiding an unjustified termwise-connectivity claim.

**Lemma.** If a simplicial spectrum A satisfies A_n >= -d-n for all n >= 0, then |A| >= -d.

**Proof.** The latching object L_n A is a finite colimit of degenerate terms A_m with m < n. Each such term is at least (-d-n+1)-connective. Hence L_n A has the same lower bound. The cofiber

    N_n = cofib(L_n A -> A_n)

is at least (-d-n)-connective. In the skeletal filtration of realization, the nth successive cofiber is Sigma^n N_n, which is at least (-d)-connective. The zeroth skeleton is A_0 >= -d. Induction and closure of Sp_{>=-d} under filtered colimits prove the assertion. For n=0 the latching object is zero. This is a skeletal proof, so no convergence claim for a diagonal spectral sequence is needed. QED.

Applying the lemma to (2.1), and using that filtered colimits commute with geometric realization, proves:

**Proposition 2.4 (dimension bound).** If E is Nisnevich-connective, then

    (L_G E)(T) >= -dim T.                                      (2.2)

In particular, for every zero-dimensional essentially smooth G-scheme O, a finite disjoint union of spectra of finitely generated separable extensions with a compatible G-action,

    (L_G E)(O) >= 0.                                           (2.3)

The components of O need not be k-rational or have trivial action. A zero-dimensional orbit can be a nontrivial field torsor. This result does not use an abelian hypothesis or a splitting-field hypothesis.

This is a formal extension of the dimension/singular portion of the known argument, not a claim to a new full connectivity theorem. Its exact limitation is that dim(X^h_{Gx}) can be positive. Formula (2.2) then permits negative degrees. Evaluating the residue orbit instead does not identify it with that henselian germ.

## 3. Exact subgroup reduction

Let H <= G. On schemes let

    j_H(U) = G x_H U,        r_H(X) = X with action restricted to H.

The standard scheme adjunction j_H left-adjoint r_H implies an adjunction on presheaves

    j_H^* E(U) = E(G x_H U),
    j_{H,*} F(X) = F(r_H X).

Both formulas are important: the second is not the fixed-locus functor.

### 3.1 Topology and t-structure checks

An equivariant scheme over G x_H U is induced from its inverse image over the component indexed by the identity coset. This is an equivalence of the corresponding slice categories. It identifies equivariant étale covers and preserves residue fields and the appropriate set-theoretic stabilizers. Therefore j_H^* commutes with Nisnevich sheafification and is t-exact for the local spectral t-structures.

Restricting a G-Nisnevich cover to H gives an H-Nisnevich cover: the stabilizers become the intersections of the original stabilizers with H. Thus j_{H,*} also takes Nisnevich sheaves to Nisnevich sheaves.

Both scheme functors commute with product by the trivially acted-on interval. Both displayed presheaf functors consequently preserve A^1-local sheaves. The adjunction and the universal property of localization now give, without an assumption on connectivity,

    j_H^* L_G E = L_H j_H^* E.                                 (3.1)

One can also see (3.1) directly from the spectral singular formula. The adjunction proof records why the topology and local t-structure have not changed.

### 3.2 Stalks with a known subgroup

For x in X let H=G_x be its set-theoretic stabilizer. The action on its residue field is retained. The canonical étale map

    G x_H r_H X -> X

has a selected orbit mapping isomorphically to Gx. Henselizing along that orbit gives

    X^h_{Gx} = G x_H (r_H X)^h_x.                              (3.2)

Here the right-hand henselization has the H-action fixing the point set-theoretically. This identity also follows directly from the equivalence of pointed étale neighborhoods. Unwanted additional orbits of the finite étale map are not included in the selected henselization.

If stable connectivity is known for H over k, equations (3.1)--(3.2), t-exactness of j_H^*, and continuity imply

    pi_i (L_G E)(X^h_{Gx}) = 0  for i < 0.

For H=1 this is the usual field theorem; for H=C2 it is Bachmann's result under the present infinite-field and tame hypotheses. Thus a counterexample for any finite G cannot occur at a point with set-theoretic stabilizer of order at most two. It also cannot occur at a zero-dimensional germ, by Section 2.

This does **not** replace set-theoretic stabilizers with geometric inertia groups. A point with free geometric action can still have a large set-theoretic stabilizer acting faithfully on its residue field. The next section gives a minimal illustration.

### 3.3 Free germs over perfect fields: the additional comparison

Here is a separate, proved comparison within this same restriction/descent approach. It handles arbitrary free torsors, not merely split-free objects G x U.

**Proposition 3.3.** Suppose k is infinite and perfect. For any finite tame G and any Nisnevich-connective E, the negative homotopy sheaves of L_G E vanish at every equivariant Nisnevich germ represented by a geometrically free G-scheme. Without perfectness, the proof applies when the quotient residue field at that germ is separably generated over k.

**Proof, Step 1: a compatible coefficient field and a smooth model.** Let Q be smooth over k, let y be any scheme point, put A=O_{Q,y}, and put F=k(y). Assume F/k is separably generated. Choose a separating transcendence basis bar(t_1),...,bar(t_r) of F/k, and lifts t_i in A. A nonzero polynomial over k in the t_i has nonzero residue; it is therefore a unit in A. Thus K0=k(t_1,...,t_r) is a subfield of A, identified with the corresponding rational subfield of F, and F/K0 is finite separable.

The local ring A is essentially smooth over K0. To check this, take a smooth affine neighborhood in Q on which the t_i are regular. Their differentials are linearly independent in Omega_{Q/k} tensor F because their images form a basis of Omega_{F/k}. The differential criterion makes the map to A^r_k defined by the t_i smooth near y. Its image at y is the generic point. Base change to that generic point and localization give the assertion.

Form B=A tensor_{K0} F. It is finite étale over A. The map B -> F given by reduction in A followed by multiplication has a prime kernel n with residue F. The local F-algebra B_n is essentially smooth over F, and A -> B_n is essentially étale with unchanged residue field. Henselizations are consequently isomorphic over A:

    S=A^h = (B_n)^h.

This supplies both a compatible embedding F -> S and an essentially smooth F-presentation of S. An arbitrary formal coefficient field would not have supplied the latter. For perfect k the separably generated hypothesis holds at every point of Q.

**Step 2: the residual torsor.** Work at a free orbit. One may first pass to an affine equivariant Nisnevich neighborhood; for a point with set stabilizer H, intersect the H-translates of an affine neighborhood containing that point and then induce from H to G. Separatedness makes these finite intersections affine. This construction preserves the selected residue orbit and permits a scheme quotient Q=X/G. The free map X -> Q is a finite étale G-torsor, and Q is smooth by étale descent.

For y in Q, the equivariant henselian orbit is T=X x_Q Spec(S), with S=O^h_{Q,y}. Let P=T x_S Spec(F) be its residual G-torsor. Finite étale algebras over S are equivalent to finite étale algebras over F. Using the coefficient embedding from Step 1, full faithfulness, including the finite G-action and the torsor isomorphism, gives

    T = P x_F Spec(S).

P need not split over F. This is not a claim that a free torsor becomes G x S in the Nisnevich topology.

**Step 3: the exact change of base field.** Extend E by continuity to essentially smooth k-objects and restrict to smooth G-schemes over F, with G fixing the base field. Call the result E_F. Since F/k is separably generated, these objects have smooth k-models after shrinking a smooth finitely generated k-subalgebra of F. The finite G-action and every finite-presentation étale diagram descend. Covers of an F-object inherit its F-structure. Restriction therefore commutes with homotopy-sheafification and is t-exact, so E_F is connective. The explicit Sing formula and commutation of filtered colimits with realization give

    (L_G^k E)_F = L_G^F(E_F).

This establishes the needed topology, t-structure, and localization comparison, rather than assuming a connectivity theorem over the positive-dimensional base Q.

**Step 4: fixed-torsor restriction.** On the ordinary smooth F-site define R_P(A)(U)=A(P x_F U). An equivariant étale map to P x_F U inherits a map to P. Torsor descent identifies it with the pullback of an ordinary étale map to U, and identifies the respective Nisnevich covers. For the separated finite-presentation étale maps in question the descended objects are schemes; alternatively one can work on the usual admissible affine basis. Hence R_P is t-exact on Nisnevich sheaves. It commutes directly with Sing, since the interval action is trivial:

    R_P L_G^F(E_F) = L^F R_P(E_F).

By ordinary stable connectivity over the field F, the right side is a connective ordinary Nisnevich spectral sheaf. Evaluate at S, which Step 1 identifies as the henselization of an essentially smooth local F-algebra. This stalk is connective. The identifications above make its value precisely (L_G^k E)(T), completing the proof. QED.

This is a formal deduction from ordinary stable connectivity and étale descent; no novelty claim is made. The condition on F/k is essential to the argument as written. Smooth schemes over imperfect fields can have inseparable residue extensions, so this proof does not settle every free germ under the original arbitrary-infinite-field hypotheses.

## 4. The remaining detection problem is real

### 4.1 Precise missing bridge

A sufficient bridge would be the following statement, for the uncovered G and k:

    If K is an A^1-local spectral Nisnevich sheaf and K(O) >= 0
    for every zero-dimensional essentially smooth G-orbit O,
    then K is Nisnevich-connective.                             (FD)

An even narrower bridge, sufficient for this problem, restricts K to objects L_G E with E Nisnevich-connective. Section 2 proves the hypothesis for those K. Neither version of (FD) is proved here for general nonabelian groups. A modified Gersten injection at every equivariant henselian germ would suffice; such an injection must include the correct stabilizer and residue-field information.

Bachmann's C2 argument supplies precisely a detection input in addition to the dimension calculation. Removing the detection input is not a proof for larger groups.

### 4.2 Field evaluation does not detect arbitrary Nisnevich sheaves

This failure already occurs nonequivariantly. Let X=A^2_k, let B=Bl_0 X, and let

    F = coker(Z_Nis[B] -> Z_Nis[X])

in abelian Nisnevich sheaves. Here Z_Nis[-] denotes the free abelian sheaf on a representable.

Every field-valued point of X lifts to B: outside the origin the blow-up is an isomorphism, and above the origin its fiber is P^1, which has a rational point over every field. Thus F(K)=0 for every finitely generated field K/k.

Let S=Spec(O^h_{A^2,0}). The identity germ S -> A^2 does not lift to B. Such a lift would make the ideal (x,y) invertible; this ideal in the regular local ring of dimension two is not principal. More concretely, a lift must land in one blow-up chart because S is local and the chart containing its closed point contains all of S. It would force y in (x) or x in (y), both impossible. Evaluation on a Nisnevich-local S is exact and unaffected by sheafification. The basis element [S -> X] therefore survives in the free-abelian cokernel, so F(S) is nonzero.

This F is not A^1-invariant. The map (x,y,t) -> (tx,ty) defines a class on X x A^1 whose restriction at t=0 is zero and at t=1 is the nonzero identity class. Thus this example disproves blanket field detection, not (FD) and not stable connectivity. Composing F with the underlying-scheme functor produces the same warning on the ordinary G-equivariant site.

### 4.3 Closed-point henselizations are not a substitute

Even over C, closed-point Nisnevich tests are not conservative. Let Y -> X=G_m be the square map, and form coker(Z_Nis[Y] -> Z_Nis[X]). On any henselian local smooth C-algebra with closed residue C, every unit has a square root by Hensel's lemma, so this sheaf is zero. At Spec C(t), the basis class corresponding to t does not lift, so it is nonzero.

An étale neighborhood of a closed point can fail to be a Nisnevich neighborhood of a generic point. Jacobsonness of the underlying varieties does not fix that residue-field obstruction. Accordingly, this report does not claim that checking rational closed stabilizers suffices for the full smooth site.

### 4.4 A free atlas need not be a Nisnevich cover

Take k=R, G=C2, and X=Spec C with conjugation. The action is geometrically free. The action map G x X -> X, with G acting on the first factor of the source, is étale and surjective. But the unique underlying point of X has set-theoretic stabilizer C2, whereas each of the two source points has trivial set-theoretic stabilizer. It is not an ordinary equivariant Nisnevich cover.

Thus descent along the atlas of a quotient stack, or replacement by the fixed-point topology, cannot be silently used. Likewise, the known smooth-scheme theorem for the quotient of a free object does not identify all equivariant presheaves with presheaves on that one quotient. The relevant category and t-structure comparison must be established.

## 5. Representation/codimension obstruction

The rank-one tangent obstruction is already stated by Heller--Voineagu--Østvær on p.272 of their 2015 paper. The following local formulation records a stronger necessary condition for any smooth finite-support presentation. It is an elementary consequence of tangent spaces and dimension, not a novelty certification.

**Proposition 5.1.** Let x be a G-fixed k-rational point of a smooth G-scheme X of dimension d. Let Z be an invariant closed subscheme through x with local dimension d-c at x. Suppose that, after an equivariant étale neighborhood X' -> X with a fixed rational lift x', there is an equivariant map p:X' -> W to a smooth G-scheme, smooth of positive relative dimension r at x', such that p restricted to Z x_X X' is quasi-finite at x'. Then T_x X has a G-subrepresentation of dimension r, and

    1 <= r <= c.                                              (5.1)

**Proof.** Let w=p(x'); it is fixed and k-rational. Étaleness identifies T_{x'}X' with T_xX. Smoothness of p gives an exact sequence of G-representations

    0 -> ker(dp) -> T_xX -> T_wW -> 0,

where dim ker(dp)=r and dim T_wW=d-r. Quasi-finiteness on Z' gives the local dimension inequality

    d-c = dim_{x'}Z' <= dim_w W = d-r.

This is (5.1). The tangent kernel is the asserted subrepresentation. Since |G| is invertible it is also a direct summand, although the inequality does not require choosing a splitting. QED.

**Corollary 5.2.** If every nonzero subrepresentation of T_xX has dimension at least delta, no such positive-relative-dimension presentation exists when c<delta.

For an irreducible tangent representation of dimension d>1 and an invariant divisor through x, c=1<d. This excludes not only a product with an equivariant affine line, but also any smooth positive-rank vector-bundle presentation with support quasi-finite over the smooth base. Raising the relative rank does not remove the dimension obstruction.

The support condition matters. For Z={0} in a representation V, taking W=Spec k and relative dimension dim V is compatible with quasi-finiteness on Z. Proposition 5.1 rules out a specific presentation format; it does not rule out a different effacement or connectivity argument.

## 6. Concrete nonabelian test: S3 over C

Take

    V = {(a,b,c) in C^3 : a+b+c=0},

with the permutation action. In coordinates x=a, y=b, c=-x-y, generators s=(12) and t=(123), with a choice of cyclic orientation, act by

    s = [[0,1],[1,0]],       t = [[-1,-1],[1,0]].

They satisfy s^2=t^3=1 and sts=t^-1. A one-dimensional representation of S3 sends t to 1, because t is a commutator and the abelianization has order two. But det(t-I)=3, so V has no one-dimensional invariant subspace. Since dim V=2, it is irreducible.

The polynomial

    q=x^2+xy+y^2

is invariant. Hence Z=V(q) is an invariant divisor through the fixed origin. Proposition 5.1 rules out every positive-relative-dimension smooth finite-support presentation at the origin, even after an equivariant Nisnevich neighborhood. This remains a clean nonabelian example over a splitting field, outside the stated abelian prior result.

**Corollary 6.1 (punctured representation).** For every Nisnevich-connective spectral sheaf E on Sm_C^{S3}, the negative homotopy sheaves of L_{S3}E restrict to zero on V minus the origin, in the ordinary equivariant Nisnevich topology.

**Proof.** Put V^circ=V minus the origin. To test the entire small equivariant Nisnevich site, take an arbitrary equivariant étale morphism U -> V^circ and an arbitrary scheme point u of U, including nonclosed points. We must test all such pairs (U,u), rather than just points of the base object V^circ. Write H for the set-theoretic stabilizer of u and I=ker(H -> Aut_C(k(u))) for its geometric inertia.

Choose a geometric point above u. Its image is a nonzero vector in V over the same algebraically closed field. Equivariance embeds I into the stabilizer of that vector. Such a stabilizer is either trivial or generated by one transposition: a 3-cycle has no nonzero fixed vector, and two distinct transposition fixed lines meet only at zero. Thus I is either 1 or C2.

If I=1, u belongs to the geometrically free invariant open of U. Proposition 3.3 applies to its equivariant henselian germ because C is perfect. If I=C2, I is normal in H by its definition as a kernel, so H is contained in N_{S3}(I)=I. Hence H=I=C2, and Section 3.2 applies. In both cases all negative homotopy groups vanish at U^h_{S3 u}. These orbit-henselian points, with U varying over all objects of the small site, form a conservative family and prove the asserted sheaf vanishing. QED.

The conclusion is local connectivity on the punctured object's small Nisnevich site, not connectivity of all of its global section spectra. It does not use the false closed-point criterion. Every small-site germ not controlled by this argument lies over the origin; no failure at any such germ has been proved.

Two further traps can be made explicit here.

1. **Induction through an abelian normal subgroup loses smoothness.** Diagonalize the action of C3=<t> with coordinates u,v and weights 1,-1. The invariant ring is

       C[u,v]^(C3) = C[A,B,C]/(AB-C^3),
       A=u^3, B=v^3, C=uv.

   To verify generation, every invariant monomial u^a v^b has a-b divisible by three. Remove (uv)^min(a,b); the remaining exponent is divisible by three. The displayed single relation gives the ring (or use the resulting monomial normal forms). Its origin has tangent dimension three and Krull dimension two, so the quotient is singular. One cannot simply apply the smooth C2 theorem to this quotient and conclude for S3.

2. **A representation's contraction does not automatically contract its henselization.** The global V is equivariantly A^1-contractible by scalar multiplication. But on R=O^h_{V,0}, a scalar contraction would have to send the unit 1-x to 1-tx in R[t]. The latter is not a unit: a polynomial over the domain R is a unit only if its positive-degree coefficients are zero. Thus that global contraction does not define a morphism Spec R x A^1 -> Spec R. Connectivity at the global representation is not the needed connectivity at its equivariant Nisnevich stalk.

## 7. What remains

The unresolved target is the vanishing of negative stalk groups at positive-dimensional equivariant henselian germs with genuinely uncovered set-theoretic stabilizers. For the S3 fixed origin, the general bound gives only >=-2, while the required conclusion is >=0. No class in degrees -1 or -2 is exhibited.

A useful next approach would prove an actual local detection/effacement statement that tolerates higher-dimensional irreducible tangent representations, or construct a spectral sheaf and a surviving negative stalk class. Quotient-stack or stabilizer-stratum methods must show their exact topology and t-structure comparisons. Repeating the impossible smooth finite-support presentation is not a promising next step.

The attempted closed-point-conservativity shortcut was rejected during checking and is not part of the claimed result. The corrected proof of Corollary 6.1 uses all point orbits in every equivariant étale object over the punctured representation, the coefficient-field comparison of Proposition 3.3, and normalizers of the actual inertia groups. Points of the base object alone are not asserted to be conservative for its small Nisnevich site. The arbitrary-imperfect-field free case is not settled by that comparison.

Approach count remains **1/5**. The general problem remains unresolved. The correction history and exact acceptance limits are recorded in REPAIR_LEDGER.md and ACCEPTANCE.json.

## References

- Tom Bachmann, OWR 40/2023 contribution, pp.2309--2311: https://ems.press/content/serial-article-files/47480
- Tom Bachmann, A C2-equivariant Gabber presentation lemma, arXiv:2310.08125v2, especially Lemma 3.1, Proposition 3.2, and footnote 5: https://arxiv.org/abs/2310.08125v2 . Published DOI: https://doi.org/10.1016/j.jalgebra.2024.11.037
- J. Heller, M. Voineagu, P. A. Østvær, Equivariant Cycles and Cancellation for Motivic Cohomology, Documenta Mathematica 20 (2015), 269--332, especially p.272 and Section 3: https://ems.press/content/serial-article-files/26271
- T. Bachmann, A. A. Khan, C. Ravi, V. Sosnilo, Categorical Milnor squares and K-theory of algebraic stacks, Appendix A.4: https://www.preschema.com/papers/milnor.pdf
- Sandeep S and Anand Sawant, An equivariant version of the Gabber presentation lemma, Conventions 1.1 and Theorem 1.2: https://mathweb.tifr.res.in/~asawant/GP.pdf . Public author listing: https://mathweb.tifr.res.in/~asawant/research.html
- Filippo Belfiori seminar listing, 7 October 2026: https://indico.math.cnrs.fr/event/17487/
- Fabien Morel, The Stable A1-Connectivity Theorems, K-Theory 35 (2005), ordinary field-base theorem: https://fangzhoujin.github.io/Morel_The%20stable%20A1-connectivity%20theorems.pdf
- J. Heller, A. Krishna, P. A. Østvær, Motivic homotopy theory of group scheme actions, arXiv:1408.2348v2, ordinary equivariant topology and henselian-orbit points: https://arxiv.org/abs/1408.2348v2
- Stacks Project, finite étale algebras over henselian local rings, Tag 04GK: https://stacks.math.columbia.edu/tag/04GK ; henselization, Tag 0BSK: https://stacks.math.columbia.edu/tag/0BSK
