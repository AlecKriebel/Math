# Fat connected components of multigraded Hilbert schemes: reductions and obstructions

## Status and scope

Problem 20000822 / AIM-ARITHMETIC_GEOMETRY-0068. **Unresolved; corrected bounded partial results accepted by the accompanying mathematical audit.** No example of the requested component is claimed, and no impossibility theorem for the full question is claimed.

This AI-assisted manuscript and audit are unrefereed. Acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. No novelty or priority is claimed. The proof is self-contained relative to the explicitly cited mathematical theorems and does not depend on any omitted program, dataset, raw output or generated certificate.

AIM Problem 21 asks whether a multigraded Hilbert scheme has a connected component isomorphic to a fat point. We use the Haiman–Sturmfels functor for a polynomial ring S=k[x_1,...,x_n], an abelian-group grading deg:Z^n→A, and a fixed FULL Hilbert function h:A→N. A fat point means Spec B with B a finite-dimensional, local, nonreduced k-algebra. Work over an algebraically closed field k unless specified otherwise.

This note proves a rank-one-kernel reduction, an explicit integrability obstruction covering all squarefree monomial supports, and a sharper local-isolation criterion. The previously studied four-coordinate SST obstruction is not claimed as new work. The separate three-variable connectedness question is not addressed.

## 1. A local Artin ring already certifies an entire component

**Lemma 1.** Let X be a finite-type k-scheme and p a closed k-point. If the completed local ring at p is Artinian and nonreduced, then the connected component supported at p is an open-and-closed subscheme isomorphic to Spec O_{X,p}, a fat point.

**Proof.** Completion is faithfully flat and preserves dimension for a Noetherian local ring. Thus O_{X,p} has dimension zero and is Artinian. An Artinian local ring equals its completion. There is no proper generization of p, so {p} is an irreducible component of X. Remove the finitely many other irreducible components. The resulting open neighborhood has underlying space {p}, and its scheme is Spec O_{X,p}. Since p is closed, this neighborhood is also closed. It is connected and is the entire connected component at p. Nonreducedness follows from its completed local ring. ∎

**Correction to the prior discussion.** If one has computed the FULL completed local ring of the intended Hilbert scheme and shown it is nonreduced Artinian, a separate global-isolation computation is unnecessary. The finite-type hypothesis supplies isolation automatically. This does not rescue a computation of only an irreducible component, a closed slice, a tangent cone, an invariant subring, or a ring up to smooth equivalence.

## 2. Every possible example reduces to one character direction

Let T=(G_m)^n act on the Hilbert scheme by rescaling the variables. The fine grading is the Z^n-grading with deg(x_i)=e_i.

**Theorem 2 (cyclic-kernel extraction).** Suppose X=H_S^h has a fat connected component C. Then:

1. Its unique closed point corresponds to a monomial ideal M.
2. There is a nonzero c∈ker(deg:Z^n→A) such that the Hilbert scheme for the grading A_c=Z^n/Zc and the FULL Hilbert function h_c of S/M has a fat connected component at M.
3. If A is torsion-free, c can be chosen primitive, so A_c is free abelian of rank n−1.
4. If the original grading is positive, then c has both positive and negative coordinates, and A_c is positive. By Hering–Maclagan Theorem 1.1, one may then replace h_c by a finite-support Hilbert function without changing the Hilbert scheme, equivariantly.

**Proof.** The connected torus T preserves each connected component. Since C has only one underlying point p, the orbit morphism T→C factors through the reduced point. Thus p is fixed by all variable rescalings. A T-stable ideal is a direct sum of the one-dimensional fine weight spaces of S, hence is monomial; write it M.

By Haiman–Sturmfels Proposition 1.6 the tangent space is Hom_S(M,S/M)_0 for the A-grading. It is a finite-dimensional representation of T. Its fine degree-zero subspace vanishes: a fine degree-zero map sends every monomial generator x^u to a scalar multiple of x^u, which is zero in S/M. Since C is nonreduced Artinian, its tangent space is nonzero. Choose a nonzero fine-homogeneous tangent direction of degree c. Its A-degree is zero, so c∈ker(deg), and c≠0.

Set D=D(A_c)=Spec k[A_c], the diagonalizable closed subgroup of T whose characters are Z^n/Zc. Its trivially restricted T-characters are exactly Zc. This subgroup is permitted even when c is nonprimitive; in that case D need not be a torus. For an affine D-scheme Spec R the fixed scheme is

    Spec R / (R_χ : χ≠0 in A_c).

This is the fixed-scheme quotient, not the invariant subring. Apply it to the T-stable affine scheme C=Spec B. The result C^D is still a local Artin scheme with residue field k. Modulo the square of the maximal ideal, the fixed quotient retains exactly the D-trivial cotangent weights. The chosen tangent weight, up to the harmless dual sign convention, lies in Zc and survives. Consequently C^D has nonzero tangent space, so it is nonreduced.

The D-fixed ideals are exactly the A_c-homogeneous ideals. Since Zc⊂ker(deg), the A_c-grading refines the A-grading. In an Artin family reducing to M, the refined weight pieces of each coarser quotient piece are direct summands of a finite locally free module. Their ranks are therefore fixed by the special fiber and equal h_c. Thus the fixed family C^D is precisely the inverse image of C under the Haiman–Sturmfels closed embedding H_S^{h_c}→H_S^h. It is open and closed in H_S^{h_c}, and its support is the singleton M. It is the desired fat connected component for the cyclic-kernel grading.

If A is torsion-free and c=rc_0 for primitive c_0, then c_0∈ker(deg). Repeating the construction using Zc_0 retains the selected tangent direction and gives the assertion with primitive c. If the original grading is positive, no nonzero nonnegative vector lies in ker(deg); therefore c is mixed-sign. A multiple of a mixed-sign vector cannot be nonzero and nonnegative, so Z^n/Zc is positive. The final finite-support replacement is the cited equivariant isomorphism theorem. ∎

**What this does and does not establish.** To answer the positive-grading existence question it suffices to find a mixed-sign integer vector c, a finite monomial order ideal B, and a nonreduced Artin local chart at its complementary monomial ideal for the grading Z^n/Zc. Conversely any such chart answers the original question by Lemma 1. This is a reduction of an EXISTING fat component; retaining a tangent weight at an arbitrary nonisolated point does not make the point isolated. Torsion must not be silently discarded when the original grading group has torsion.

## 3. An explicit one-step integrability obstruction

Write G(M)={x^u:u∈U} for the minimal monomial generators of M, and put E_i=max_{u∈U} u_i.

**Theorem 3 (one-step integrability).** Let 0≠φ∈Hom_S(M,S/M)_c be a fine-homogeneous map. Suppose some coordinate i satisfies

    c_i=−b_i<0 and E_i<2b_i.

Then φ integrates to a nonconstant flat one-parameter family with initial ideal M. If deg(c)=0, the family lies in the multigraded Hilbert scheme with the full Hilbert function of S/M. In particular M is not an isolated point of that Hilbert scheme.

**Proof.** For each u∈U write

    φ(x^u)=λ_u x^{u+c} modulo M,

where λ_u=0 if u+c has a negative coordinate or x^{u+c}∈M. Some λ_u is nonzero. In particular c has a negative coordinate; if c were nonnegative every proposed target would lie in M. Choose a positive weight vector w with w·c<0 and refine its weighted monomial order. Define, over k[t],

    f_u=x^u+t λ_u x^{u+c}.

The leading monomial is x^u. For u,v∈U let ℓ=max(u,v), componentwise. Their monic S-polynomial is

    t(λ_u−λ_v)x^{ℓ+c},

up to overall sign, with zero terms omitted. If its coefficient is nonzero, the target exponent is nonnegative and S-linearity of φ forces x^{ℓ+c}∈M. Choose a minimal generator x^q dividing it. Its i-th exponent satisfies

    q_i≤ℓ_i−b_i≤E_i−b_i<b_i.

Thus q+c has a negative i-th coordinate and λ_q=0. Therefore f_q=x^q is a monomial and reduces this S-polynomial to zero in one step. Every S-polynomial reduces to zero. Buchberger's monic criterion over k[t] gives a Gröbner basis with constant initial ideal M.

The monomials outside M are consequently a free k[t]-basis of the quotient, and, when deg(c)=0, each A-graded piece has its original finite rank. The family has exactly the required FULL Hilbert function. Its derivative at t=0 is φ, so it is nonconstant. A nonconstant k[t]-family cannot factor through an Artinian local component: any map from an Artinian k-algebra to the reduced ring k[t] kills its nilpotents. Hence M is not isolated. ∎

**Corollary 4 (necessary exponent bounds).** If a monomial ideal M supports a fat connected component, every nonzero fine tangent weight c must satisfy

    E_i≥2|c_i| for every i with c_i<0.

Violation for even one negative coordinate produces the explicit curve in Theorem 3. This is only a necessary condition; equality does not certify an obstruction or a fat component.

**Corollary 5 (squarefree supports excluded).** A squarefree monomial ideal cannot support a fat connected component of any Haiman–Sturmfels multigraded Hilbert scheme, in any characteristic.

**Proof.** A nonzero fine tangent map has a negative coordinate, and at such a coordinate squarefreeness forces c_i=−1 while E_i≤1<2. Theorem 3 gives a nonconstant curve. Every nonreduced Artin local ring has a nonzero tangent vector, and Theorem 2 shows that the support of a candidate component must be monomial. ∎

**Attribution.** Altmann–Sturmfels, Theorem 17(a), already identifies the directional Schubert scheme at a squarefree ideal with its homogeneous tangent space for mixed-sign c. For mixed-sign c, the squarefree obstruction is a consequence of that result; no novelty is claimed for the underlying integrability fact. The purely negative case used in Corollary 5 is supplied directly by Theorem 3, rather than by the mixed-sign statement of Altmann–Sturmfels. The displayed exponent-bound version is proved here directly and includes non-squarefree ideals and purely negative degrees. Its novelty has not been established.

## 4. A second classical chart is also excluded

**Proposition 6 (characteristic zero).** Let k be an algebraically closed field of characteristic zero. In the SST nonnormal example of Section 4, at the monomial initial ideal for the weight (0,0,276,220,0,0,215), no refinement diagonal on the five minimal chart coordinates z32,z35,z37,z42,z44 has an isolated nonreduced fixed locus at the origin. This includes diagonalizable finite-group refinements.

**Proof.** SST's complete local chart has, among its five primary components, the two reduced coordinate components defined by (z44,z37) and (z42,z35). The first contains the z32-, z35-, and z42-axes; the second contains the z32-, z37-, and z44-axes. Thus every coordinate axis is a reduced curve contained in the FULL chart. A diagonalizable fixed quotient kills every coordinate of nontrivial restricted weight. If all five are killed it is the reduced origin. If any coordinate survives, its entire axis survives, giving a positive-dimensional fixed locus through the origin. This proves the claim. ∎

This is a different example from the previously studied four-coordinate chart. It explains why extracting the visible nilpotent direction from only the nonnormal coherent hypersurface is insufficient: the other components restore a reduced curve in that direction. The proof uses the published complete primary-component list, visually checked on PDF page 21. The source computes over QQ and describes the associated complex chart; the result here is used only over characteristic-zero field extensions. No positive-characteristic specialization of that full Hilbert-scheme chart has been verified. No fresh computation of the 44-generator universal chart is claimed.

## 5. Computational search and its limits

The historical exploratory computations constructed exact commutator equations for homogeneous border-basis charts of finite monomial order ideals. The variables are border-to-standard-monomial coefficients with exponent difference in Zc. Commutativity of the multiplication matrices is a scheme-theoretic chart condition, not a tangent-space substitute.

The exploratory searches sample staircases, first discard cases with no variables or excessive variable counts, compute the linear tangent quotient, and only attempt exact elimination and Gröbner dimension tests when the surviving tangent dimension is at most three. They are bounded experiments, not a classification, and a skipped instance is not a negative certificate. The completed sparse-staircase run admitted 19,836 of 20,000 generated candidates to its initial size filter, and the box-staircase run admitted 2,640 of 3,000. Many admitted candidates were then skipped by the variable-count or tangent-dimension filters; these are NOT counts of complete local-ring certifications. A separate denser run was interrupted during symbolic elimination after its last progress checkpoint at 1,500 generated candidates; it has no completed-run receipt and contributes no negative conclusion. The sparse and box seeds are 1336 and 1338 respectively. The original box receipt misrecorded 1336 because of a hard-coded metadata error; independent regeneration with seed 1338 recovers the stated 2,640 size-admitted candidates. The interrupted dense run used seed 1337; its unused completed-summary writer had the same hard-coded seed error. Corrections to these receipt writers do not change the sampled candidates, admitted counts, or absence of a reported construction.

No construction was obtained. The historical methods, counts and limitations are reported here and in the mathematical audit; raw outputs are not distributed. The symbolic elimination and dimension tests are over characteristic zero. They test the dimension of the entire affine border chart, not the local ring at its origin, and can therefore miss an isolated origin component when other components of the chart have positive dimension. No search-negative claim covers such rejected charts or other characteristics. Historical exact checks covered explicit charts and the one-step S-pair mechanism. They do not certify an unbounded search. Normal and optimized Python runs agreed exactly: 532 generator antichains, 13,606 basis directions in the tested shift box, and 6,352 directions meeting the theorem's cutoff, including 6,105 at non-squarefree ideals. The three-variable antichains here test a dimension-independent algebraic lemma; they do not address the separate three-variable connectedness question.

## 6. Literature and residual obstruction

The original AIM question and Haiman–Sturmfels definitions were read directly. Historical current-source checks were supplemented with exact-wording searches and primary-source inspection of Altmann–Sturmfels and Hering–Maclagan. No exact published or preprint solution to Problem 21 was located in these bounded searches. This is absence of located evidence, not a theorem that the question remains open worldwide.

Erman's theorem supplies singularity types up to smooth equivalence and does not control the zero-dimensional FULL local ring. The known SST first chart remains blocked for the previously recorded reason. The separate SST nonnormal coherent chart was also inspected over characteristic zero: its coherent toric hypersurface can have a fat fixed slice, but the FULL Hilbert-scheme chart has four additional components. Its five minimal coordinates each lie on a reduced coordinate axis in at least one component, so retaining any such coordinate leaves a curve. One must not replace the full chart by the coherent component.

The remaining exact task is to construct (or rule out) a monomial ideal with nonzero graded tangent space but Artinian full graded local deformation ring. In the positive case Theorem 2 reduces the search to finite staircases and a cyclic kernel. Theorem 3 rules out every direction with a sufficiently large negative step relative to a generator exponent. None of these facts supplies the missing Artinian chart.

## References

1. AIM, Components of Hilbert schemes, Problem 21, https://aimath.org/WWN/hilbertschemes/hilbertschemes.pdf .
2. M. Haiman and B. Sturmfels, Multigraded Hilbert Schemes, J. Algebraic Geom. 13 (2004), 725–769; https://arxiv.org/abs/math/0201271 . Definitions, Theorem 1.1, Proposition 1.5 and Proposition 1.6.
3. K. Altmann and B. Sturmfels, The Graph of Monomial Ideals, J. Pure Appl. Algebra 201 (2005), 250–263; https://arxiv.org/abs/math/0209152 . Theorem 17(a); the local copy is arXiv v1, whose numbering agrees for this theorem.
4. M. Hering and D. Maclagan, The T-graph of a multigraded Hilbert scheme; https://arxiv.org/abs/1110.1861 . Theorem 1.1 and its proof in Section 2.
5. M. Stillman, B. Sturmfels and R. R. Thomas, Algorithms for the Toric Hilbert Scheme; https://arxiv.org/abs/math/0010130 . Sections 3–4, especially PDF pages 14–16 and 20–22.
6. D. Erman, Murphy's Law for Hilbert function strata in the Hilbert scheme of points; https://arxiv.org/abs/1205.0587 . Theorem 1.2.
