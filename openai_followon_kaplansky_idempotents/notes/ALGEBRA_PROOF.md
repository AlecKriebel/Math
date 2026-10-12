# Independent algebra and module audit

Checkpoint: 2026-10-06 22:12 America/Los_Angeles (2026-10-07 05:12 UTC).

Scope: an independent verification of the scalar algebra and module conclusions, the source's parity criterion and finite-presentation extraction. This note does **not** certify the upstream probability estimates, planar argument, asphericity, root protection, torsion-freeness or existence theorem. The full core theorem depends on those separate inputs.

Completion estimates for this audit: algebraic implication and handedness 100%; independent validation of the upstream existence theorem outside this audit 0%; publication package outside this audit 0%. These estimates are not mathematical evidence.

## 1. Exact hypotheses and theorem

Let R be a nonzero associative unital ring. Assume that a,b,c in R satisfy ab=1, ac=0 and c≠0. Set f=ba and e=1-f. Then:

* e is a scalar idempotent with e≠0 and e≠1.
* R_R=fR⊕eR=bR⊕eR and bR is isomorphic to R_R.
* P=eR is a nonzero cyclic finitely generated projective right R-module.
* R_R is isomorphic to R_R⊕P and [P]=0 in K_0(R).

Here R_R denotes the right regular module; all homomorphisms below are right R-linear. No field, group, characteristic, domain, commutativity or finite-dimensional assumption is used for this ring theorem.

For R=F_2[G], a verified finitely presented torsion-free G satisfying the hypotheses would therefore meet the algebraic core targets. The exact positive-characteristic assertion it would refute is: **for every torsion-free group H and every field k of positive characteristic, the only scalar idempotents in k[H] are 0 and 1**. Already its specialization to characteristic two, or k=F_2, would be false. This audit does not establish historical priority for that formulation.

## 2. Self-contained proof

First f²=b(ab)a=ba=f. Hence e²=(1-f)²=1-f-f+f²=1-f=e, with subtraction understood in R; the computation is valid in every characteristic. Also

    ae=a-aba=0,     eb=b-bab=0,     ec=c-bac=c.

Because c≠0, ec=c proves e≠0. If e=1, then ae=0 implies a=0, contradicting ab=1 in a nonzero ring. Thus e≠1. Equivalently, the nonzero annihilator proves ba≠1 via c=bac=b(ac)=0 if ba were 1.

The identities f+e=1 and fe=ef=0 give R=fR+eR. If r lies in both summands, then fr=r from r∈fR and fr=0 from r∈eR, so r=0. Thus R=fR⊕eR. Moreover fR⊆bR because f=ba, while b=fb gives bR⊆fR. Therefore fR=bR.

The map L_b:R_R→bR, r↦br, is surjective by definition and injective because abr=r. Its inverse on bR is L_a:br↦abr=r. Both maps are right R-linear: L_b(rs)=L_b(r)s, and likewise for L_a. Left multiplication is essential here; right multiplication by b is generally not right R-linear.

Since eR is a direct summand of the free module R_R, it is projective. It is cyclic with generator e and therefore finitely generated. It is nonzero because e=e·1 belongs to it and e≠0. An explicit absorption isomorphism is

    Φ:R_R→R_R⊕eR,       Φ(r)=(ar,er),
    Ψ:R_R⊕eR→R_R,       Ψ(u,p)=bu+p.

Indeed ΨΦ(r)=bar+er=r, while ΦΨ(u,p)=(abu+ap,ebu+ep)=(u,p), using ae=eb=0 and ep=p for p∈eR. In particular ker(L_a)=eR: ar=0 implies r=er, and a(er)=0.

By definition, K_0(R) is the Grothendieck group of the monoid of isomorphism classes of finitely generated projective right R-modules under direct sum. The displayed isomorphism gives [R]=[R]+[P], hence [P]=0 after cancellation in that *abelian group*. It does not give P=0. Indeed P contains the nonzero element e. Cancellation in the projective-module monoid itself fails: R⊕0≅R⊕P with 0≄P.

## 3. Coefficient extension and rank-zero consequences

If K is any characteristic-two field, the unique unital map F_2→K is injective. Every group-algebra element has a unique finite expansion ∑_g λ_g g in the basis G. The map

    F_2[G]→K[G],          ∑_g λ_g g ↦ ∑_g λ_g g

therefore preserves multiplication and is injective coefficient by coefficient. It preserves ab=1, ac=0, c≠0, and e²=e. It also preserves e≠0 and e≠1 by injectivity applied to e and e-1. This establishes the *same scalar e* over every characteristic-two extension field. Applying Section 2 in K[G] gives the same module statements for P_K=eK[G]. Equivalently P⊗_{F_2[G]}K[G]≅eK[G].

The proof actually works for every nonzero unital commutative coefficient ring of characteristic two, because F_2 injects into it. This is a standard extension, not a new mechanism.

For a group algebra, the augmentation ε:R→F_2 is a unital ring map. From ε(a)ε(b)=1 one has ε(a)=ε(b)=1 and ε(e)=0. Tensoring the absorption isomorphism with the augmentation module F_2 gives P⊗_R F_2=0. Thus P is nonzero despite having zero augmentation dimension. The relation P⊕R≅R makes P stably free with equal stabilizing free ranks, commonly described as stably free of rank zero. Group algebras have invariant basis number: an isomorphism R^m≅R^n, tensoring with F_2, gives F_2^m≅F_2^n and m=n. There is consequently no ambiguity about the zero difference of free ranks in this assertion.

## 4. Verification of the pinned parity criterion

Reviewed source: `sources/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build/sections/algebra.tex`, SHA-256 `71fe26eab4e6a01564a687c522bbceb8923182c0201af9685eac84d9f86a141f`.

The source uses finite loopless graphs Γ_A,Γ_B immersed in the same signed rose. A cone kills every closed path in each graph component. With root x_A in A and root x_B in B, it defines A',B' to be their components and g_x,h_y to be the labels in the cone group of paths from the respective roots. Independence of the chosen path follows because any two such paths differ by a closed path killed by a cone. Consequently g_{x·t}=g_x t and h_{y·t}=h_y t.

In the simultaneous-step multigraph on A'×A', each common outgoing label t supplies an edge from (x,x') to (x·t,x'·t); its reverse is the step with inverse label. Immersion ensures each outgoing label occurs at most once, so the degree at (x,x') is exactly |S_x∩S_x'|. Looplessness of the factor graphs excludes loops in the product. Parallel edges are permitted and their multiplicities count toward degree. The product coefficient g_x g_x'^{-1} is constant across each such edge because

    (g_x t)(g_x' t)^{-1}=g_x g_x'^{-1}.

By the handshake lemma, every finite component has an even number of odd-degree vertices. Under the source parities every vertex except (x_A,x_A) has odd degree and that exceptional vertex has even degree. Every component not containing the exception has even cardinality. The component containing it has odd cardinality and its constant coefficient is 1. Hence

    a=∑_{x∈A'}g_x,     b=∑_{x∈A'}g_x^{-1},     ab=1.

The same reasoning on A'×B', where *all* degrees are odd, gives even cardinality for every component and ac=0 for c=∑_{y∈B'}h_y^{-1}. Distinct components are allowed to have the same group contribution: componentwise cancellation is still valid. Distinct vertex labels within A' or B' are not required for these two products.

To conclude c≠0, the coefficient of 1 must be controlled. Root protection means that for every y≠x_B in B', any path from x_B to y has nontrivial label, so h_y≠1. Because h_{x_B}=1, the coefficient of 1 in c is exactly 1. Root protection for x_A is unused for this final coefficient test. This is a complete conditional proof of the source's Proposition “Parity criterion.”

The outgoing-set parity calculations in `random.tex` were independently checked at the elementary incidence level (SHA-256 `bb172b92ba622e262c2bf124e70c3cd55922200083c09db658615759b81323c4`). An ordinary part is a projective-plane line with 129 points; two equal lines intersect in 129 points and two distinct lines in one. Extra parts are empty, four-element complements of Fano lines, or the unique seven-element root part. Intersections of extra parts have even cardinality except the root part with itself. Thus all required parities follow. For an extra letter, the A-incidence count is 4a_m+1=129m and the B-incidence count is 4b_m=129(m-1), agreeing with ordinary letters and supporting balanced inverse-label matchings. This validates the elementary types-to-algebra correspondence, but does not validate the probabilistic avoidance theorem.

## 5. Finite presentation and coefficient data: exact extraction

Given a **specific finite matching outcome**, choose one representative generator from each inverse pair of T. In every connected graph component Λ, choose a spanning tree and a root q_Λ. Let w_x be the free-group word labeling the tree path q_Λ→x. For every non-tree unoriented edge choose one orientation x→y with label t and take the relator

    w_x t w_y^{-1}.

Then a finite presentation of the cone group is

    G=⟨ one generator per inverse pair | w_x t w_y^{-1}, one per non-tree edge ⟩.

This follows directly from van Kampen: π_1 of the rose is the free group on its edges, attaching the cone on Λ kills the image of π_1(Λ), and the non-tree edges give a free generating set for π_1(Λ). Relators for tree edges freely reduce to 1 and can be omitted. For components not containing x_A or x_B choose arbitrary roots; for their respective components choose the designated roots. The finite sums of the resulting w_x and their inverses give exactly a,b,c above. Every word and coefficient is then specified and can be multiplied in the presented group if an appropriate equality certificate is available.

The source alphabet has |T|=16520, so this presentation uses 8260 generators before simplification. There is no specific matching outcome in the audited source. The source's `assembly.tex` explicitly selects an existential outcome and states that its edges are not listed (SHA-256 `3987e23ea7c5c8d217ca539d5a307d59f8eac5b8381a0afe411125e57f0bee4a`). Thus the audited result is a finite extraction algorithm conditional on an admissible outcome, **not** an actual numerical presentation or multiplication certificate. A fully verified existence proof would meet the user's existential core without such a certificate; these algebra sections alone do not prove an admissible outcome exists.

## 6. Additional exact, standard consequences

Because the source defines b=∑g_x^{-1} from a=∑g_x, it has b=a* for the group-ring involution (∑λ_g g)*=∑λ_g g^{-1}. Therefore e*=e: (ba)*=a*b*=ba. Thus its e is a self-adjoint scalar idempotent for this purely algebraic involution. No analytic positivity or C*-algebra conclusion follows from this characteristic-two statement.

For n≥0 define e_n=b^n e a^n. Since a^n b^n=1, e_n²=e_n and a^n e_n b^n=e≠0. Hence e_n is nonzero. The identities ae=0 and eb=0 give e_m e_n=0 whenever m≠n, in both multiplication orders. For m<n, reduce a^m b^n=b^{n-m} and use eb=0; for m>n reduce a^m b^n=a^{m-n} and use ae=0. Maps L_{b^n}:eR→e_nR and L_{a^n}:e_nR→eR are inverse right-module isomorphisms. Thus R contains arbitrarily many pairwise orthogonal nonzero scalar idempotents whose right ideals are all isomorphic to P. Iterating R≅R⊕P gives R≅R⊕P^{⊕n} for each finite n. For the source's b=a*, every e_n is also self-adjoint. These are classical consequences of a proper one-sided inverse and should not be presented as an independent new solution.

The following conditions are equivalent for a nonzero unital ring: failure of direct finiteness; existence of a triple ab=1, ac=0,c≠0; existence of a nonzero projective P with R_R≅R_R⊕P. The first gives the triple by taking c=1-ba. The triple gives absorption by Section 2. Conversely, an absorption isomorphism identifies R with a direct summand of itself with nonzero complement. Its inclusion and projection are endomorphisms of R_R and hence left multiplications L_b,L_a, with ab=1 and ba≠1. The complement is automatically a cyclic finitely generated projective, as a summand of R.

## 7. Falsification tests and boundaries

* The ring proof fails to produce a nonzero e if c≠0 is dropped: take a=b=1,c=0 in any field. Then e=0. Nonzero annihilator information, or an independent proof ba≠1, is necessary.
* Nonzero unital ring is necessary to distinguish e from 0 and 1: in the zero ring, 0=1.
* A nontrivial scalar idempotent alone does not imply failure of direct finiteness. F_2[C_3] is finite-dimensional over F_2 and hence directly finite, but e=g+g² is a nontrivial idempotent for a generator g of C_3. This also distinguishes the direction of the classical implication: a ring having no nontrivial idempotents implies direct finiteness, while direct finiteness does not imply that it has no idempotents.
* The same 0/1 coefficients do not transfer idempotency to odd characteristic or characteristic zero. For e=g+g² in Z[C_3], e²-e=2·1. It is idempotent modulo 2 and is not idempotent over any odd-characteristic field or over Q. This torsion example is only a coefficient-extension boundary test, not a torsion-free witness.
* In the exact ring End_{F_2}(F_2[t]), let b(t^n)=t^{n+1}, a(1)=0 and a(t^{n+1})=t^n. Then ab=1 and e=1-ba projects onto the constant coefficient. Taking c=e gives ac=0 and c≠0. This exact infinite-dimensional shift model realizes the abstract ring theorem and its handedness. It is **not** a group-algebra witness. An independent Python sanity check of these definitions on the 20 monomial basis vectors and all 64 binary coefficient vectors of degree at most five passed (84 vectors); a separate exact coefficient convolution check confirmed the C_3 boundary above. These finite checks supplement the exact displayed proofs and do not certify an upstream group.
* The summand maps use left multiplication in right modules. Exchanging it for right multiplication would silently change handedness and generally destroy right linearity.
* [P]=0 in K_0 is group cancellation, not vanishing of P or cancellation of projective modules. Claiming a nonzero K_0 class would contradict the proved relation.
* Torsion-freeness and finite presentation must be supplied by the exact October 4 construction, not by this ring lemma or the earlier September torsion-containing example. A mismatched Lean formalization cannot certify that construction.

Strongest result verified here: the complete ring/module/extension theorem under the source triple, together with the source's deterministic parity calculation and finite extraction procedure. Exact remaining core gap: independently verify existence of an admissible finite matching outcome whose cone group is torsion-free and whose B-root is protected.
