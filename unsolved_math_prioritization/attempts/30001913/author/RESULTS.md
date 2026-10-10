# Scoped mathematical results

## 0. Exact target and credit

The target is the question posed in Alessio Corti's contribution, joint with Tom Coates, Sergey Galkin, Vasily Golyshev and Alexander Kasprzyk, to OWR 47/2011, printed pp. 2681–2683. The workshop was in 2011; the issue was published in 2012. The short catalog sentence omits important hypotheses.

Let P be a full-dimensional reflexive lattice polytope in Z³. Consider a complex Laurent polynomial f with Newton polytope exactly P, coefficient 0 at the origin, coefficient 1 at every vertex, and binomial coefficients along each edge: if E=[μ,μ+eν] with ν primitive, its face term is x^μ(1+x^ν)^e. For each facet F, compactify the face curve f_F=0 in the toric surface of F and take its normalization. The genus-zero condition is understood componentwise for a reducible curve; otherwise the source's Minkowski examples would not fit. The question is whether this condition forces f to be extremal.

Write π_f(t)=Σ_{n≥0} CT(f^n)t^n. Let L_f be its minimal-order rational differential equation and V=Sol(L_f) on its nonsingular open set U⊂P¹. Extremality means that V is irreducible, nonconstant, and

    rf(V) := Σ_{s∈P¹\U} codim ker(T_s−I) = 2 rank(V).

Apparent singularities contribute zero. The ordinary direct image j_* is intended below, not Rj_*. The coordinate of the Laurent map f and the period variable are reciprocals; changing by that Möbius transformation changes no ramification total.

This packet does not equate the facet condition with a limiting mixed-Hodge or p-adic Hodge–Tate condition. Nor does it infer rigidity, mirror-duality to a smooth Fano variety, or a global compactification theorem from facet genera alone.

Sources: [original OWR](https://doi.org/10.4171/OWR/2011/47), [Fanosearch paper](https://arxiv.org/abs/1212.1722), [2021 MMLP classification](https://arxiv.org/abs/2107.14253). The latter classifies a different class. The paper [Shamoto, 2018](https://arxiv.org/abs/1709.03244) concerns a rescaling/relative-cohomology condition, with separate geometric hypotheses; it is not used as a proof of the facet conjecture.

## 1. A global defect formula

**Proposition 1.** For a nonconstant irreducible rational local system V of rank r on a nonempty open U⊂P¹,

    rf(V)−2r = dim H¹(P¹,j_*V) ≥ 0.

**Proof.** The stalk of j_*V at s is ker(T_s−I). Additivity of Euler characteristic for U and its finite complement gives

    χ(P¹,j_*V)=rχ_c(U)+Σ_s dim ker(T_s−I)=2r−rf(V).

Global sections are monodromy invariants and vanish because V is irreducible nonconstant. Also H²(P¹,j_*V)=0: the exact sequence 0→j_!V→j_*V→⊕_s ker(T_s−I)_s→0 identifies H²(j_*V) with H²_c(U,V), which by Poincaré duality is dual to H⁰(U,V^∨)=0. Thus the Euler characteristic is −h¹. ∎

This is the standard Euler–Poincaré criterion, already used by Coates–Corti–Galkin–Golyshev–Kasprzyk, §2. It is not claimed as new.

## 2. Compactification and a quantitative genus bound

**Theorem 2.** Let g:Z→P¹ be a projective surjective morphism from a smooth projective complex threefold. Let U be a nonempty smooth locus for g, and let V be a nonconstant irreducible direct summand of R²(g|_U)_*Q. Then

    0 ≤ rf(V)−2 rank(V) ≤ b₃(Z).

In particular b₃(Z)=0 implies V is extremal.

**Proof.** Apply the decomposition theorem to Rg_*Q_Z[3]. On U its degree−1 cohomology sheaf is R²g_*Q. Consequently the full-support, perverse-degree-zero part includes IC_{P¹}(V)=j_*V[1] as a direct summand. Taking degree-zero hypercohomology embeds H¹(P¹,j_*V) as a noncanonical direct summand of H³(Z,Q). Proposition 1 proves the inequality. No assertion that the entire Leray spectral sequence degenerates for an arbitrary singular-fiber morphism is needed. ∎

The decomposition input is the Beilinson–Bernstein–Deligne–Gabber theorem; see de Cataldo–Migliorini, [§1.6](https://www.math.stonybrook.edu/~mde/papers/bams.pdf). The same vanishing route in the Landau–Ginzburg setting is explicitly described near Definition 4.15 of [Doran–Harder–Katzarkov–Ovcharenko–Przyjalkowski, final 2025 version](https://arxiv.org/abs/2307.15607v2). This application is credited, not a novelty claim.

**Corollary 3.** Suppose Z is obtained from a smooth projective toric threefold X by finitely many blowups in smooth points and smooth projective connected curves C_i. Under the period-summand hypotheses of Theorem 2,

    rf(V)−2 rank(V) ≤ 2 Σ_i genus(C_i).

If every C_i is rational, V is extremal.

**Proof.** A smooth projective toric variety has no odd rational cohomology. The blowup formula for a smooth center C of codimension c is

    H^k(Bl_C X,Q) ≅ H^k(X,Q) ⊕ ⨁_{j=1}^{c−1} H^{k−2j}(C,Q)(−j).

For k=3 a point contributes zero and a curve contributes H¹(C,Q), of dimension 2 genus(C). Induction gives the exact formula b₃(Z)=2Σ_i genus(C_i), then Theorem 2 applies. ∎

**Scope.** A genus-zero normalization of every original facet curve does not certify the genera or smoothness of every center in a global resolution. A rational threefold alone need not have b₃=0: blowing up a positive-genus curve is already a counterexample to that shortcut. For the Minkowski subclass the rational-center construction is established in [Przyjalkowski, Lemma 25, Proposition 26 and Theorem 27](https://arxiv.org/abs/1609.09740v2). The broader smooth-component construction in the 2025 paper is subject to its weak-nondegeneracy hypotheses. Those hypotheses are not silently added to the target.

## 3. A completely analyzed one-parameter family

Put

    F_a=x+y+z+x^(−4)y^(−2)z^(−1)+2x^(−2)y^(−1)+a x^(−1),  a∈C.

**Proposition 4.** Every F_a satisfies the target's polytope, origin, vertex and edge normalizations. Its facet curves have genus zero exactly when a∈{0,4,−4}.

**Proof.** Its Newton polytope is the tetrahedron with vertices e₁,e₂,e₃ and w=(−4,−2,−1). Its four supporting inequalities have right-hand side 1 and primitive integer normals

    (1,1,1), (1,1,−7), (1,−3,1), (−1,1,1).

The origin lies strictly inside, so the polytope is reflexive. The only nonprimitive edge direction occurs from w to e₃, of lattice length 2; its midpoint (−2,−1,0) has coefficient 2. The coefficient a is a facet-interior coefficient, not an edge coefficient. The other three facets give two unimodular triangles and an A₂ triangle, hence rational curves.

On the fourth facet multiply the face polynomial by x and use lattice characters U=x²yz and V=x^(−1)y^(−1). Their exponent vectors form a basis of the facet's difference lattice: their cross product is the negative primitive facet normal. The resulting Laurent polynomial is

    h_a(U,V)=(U^(−1)+2+U)V+V^(−1)+a.

Its equation, after multiplication by UV, is

    Q_a(U,V)=(U+1)²V²+aUV+U=0.

As a quadratic in V it has discriminant

    Δ_a(U)=−4U[U²+(2−a²/4)U+1].

The quadratic bracket has distinct nonzero roots except when a²(a²−16)=0. Away from these exceptions the associated degree-two function-field extension of C(U) has four simple branch points, including infinity, so Riemann–Hurwitz gives genus one. At a=0 or a=±4 the discriminant has respectively the forms −4U(U+1)² or −4U(U−1)². The function field is then C(U)(√U), a rational function field. It remains a genuine quadratic extension because U is not a square in C(U), so no reducibility assumption is hidden. These computations determine the genus of the smooth projective normalization and are independent of the chosen toric compactification. ∎

**Proposition 5.** All three genus-zero members in Proposition 4 are extremal.

**Proof.** We separate prior input from our exact reductions. F₄ is precisely the extremal non-Minkowski polynomial of Coates–Corti–Galkin–Golyshev–Kasprzyk, Example 6.6. Its extremality is credited to that source; the finite ODE checks below are not an independent proof of its monodromy.

The identity

    F_(−a)(x,y,z)=−i F_a(ix,iy,iz)

implies π_(−a)(t)=π_a(−it), because constant-term extraction is unchanged by a nonzero torus scaling. A base automorphism preserves irreducibility, nonconstancy and the ramification total, proving the a=−4 case.

For a=0 all nonzero constant terms have degree divisible by four. More generally the multinomial theorem gives the exact all-order formula

    CT(F_a^N)=Σ_{8l+4m+2n=N} N! 2^m a^n /
      [(4l+2m+n)!(2l+m)! l! l! m! n!].

For N=4q and a=0, this simplifies to

    (4q)!/[(2q)!q!] · Σ_{l=0}^{⌊q/2⌋} 2^(q−2l)/[l!²(q−2l)!]
      = (4q)!/(q!⁴).

The equality follows by taking the constant coefficient of (s+2+s^(−1))^q=s^(−q)(1+s)^(2q). These are exactly the constant terms of G=x+y+z+(xyz)^(−1). Thus π₀=π_G, so the minimal operators and their solution local systems agree. G is the standard Minkowski mirror of P³, whose extremality follows from the credited Minkowski result and rational-center construction above. ∎

This is a source-based verification of one explicit family. It proves neither that these are all possible non-Minkowski examples nor that a guessed differential operator from finitely many coefficients is minimal. The computational check includes 100 coefficients against the published F₄ operator

    D³−16t²(D+1)(3D²+6D+4)+512t⁴(D+1)(D+2)(D+3), D=t d/dt,

solely as a transcription/arithmetic control.

## 4. What the singular facet actually does

For a=±4, Q_a has a singular point (U,V)=(1,−a/8) in the torus. Both first derivatives vanish there; its Hessian has diagonal entries 1/2 and 8 and zero off-diagonal entries, hence nonzero determinant 4. This is an ordinary node. Proposition 4 showed the curve is irreducible, so this is a singular irreducible component, not merely the crossing of two globally smooth components. Therefore the smooth-component condition in Definition 3.4 of the 2025 paper does not apply directly.

**Local lemma 6.** The ideal I=(u,yz) on affine three-space is principalized by blowing up (u,y), then the residual base ideal (v,z) in the chart u=yv.

**Proof.** In the u-chart y=uw, the ideal becomes u(1,wz), already principal. In the y-chart u=yv, it becomes y(v,z). Blowing up (v,z) produces charts z=vr and v=zs, in which the total ideals are yv(1,r) and yz(s,1), respectively. Both are principal. Each center is smooth of codimension two in its chart. ∎

Near an ordinary node of a facet lying in the smooth part of the polar divisor, a local analytic equation reduces to this ideal: adding a multiple of u to the numerator does not change (u,F). This calculation explains why that local singularity alone is not a counterexample. It does **not** select globally algebraic branches of an irreducible nodal curve, settle interactions with other boundary components, or supply principalization for arbitrary rational singularities. The unresolved global step remains explicit.

## 5. A precise local-monodromy obstruction

The following construction is deliberately outside the Laurent target; it prevents replacing the facet condition by a local-unipotence shortcut.

Let A=[[1,2],[0,1]], B=[[1,0],[−2,1]], C=(AB)^(−1). They define an integral rank-two local system on P¹\{0,1,∞}. It is irreducible because the unique invariant lines of A and B are different. Each matrix has determinant one, so the system preserves the standard alternating form. A and B are nontrivial unipotent; C has one nontrivial Jordan block with eigenvalue −1. The ramification is 1+1+2=4, so it is extremal.

Pull back by s↦s^m for m≥1. There are m preimages of 1, each with conjugate monodromy B. The monodromies at 0 and ∞ are A^m and C^m. The restricted representation remains irreducible: choosing the real path to the root 1 gives B, and the loop around 0 gives A^m, whose fixed lines are still distinct. Therefore

    rf(V_m)=m+3 if m is odd, and m+2 if m is even;
    defect(V_m)=m−1 if m is odd, and m−2 if m is even.

For even m≥4 both branch-point monodromies are nontrivial unipotent of the same local Jordan type, but the defect is positive and unbounded. This is a rigorous global-local distinction, not a counterexample to the source conjecture and not a claim that these abstract representations have the required facet realization.

## 6. Final scope

The target remains unresolved by this five-approach packet. The useful sufficient condition is global b₃-vanishing for a suitable compactification and the correct period summand. A universal rational-center resolution, a replacement vanishing theorem, or a certified target counterexample is still needed. No novelty inference is drawn from the bounded literature/repository search. Independent review is required before any publication.
