# An effective semialgebraic model for the derived Weyl group action

## Status and scope

The AI-assisted mathematics has been accepted as an exact PARTIAL result by an independent internal AI mathematical audit. The proof and audit are unrefereed; no external human peer review or formal proof-assistant certification is claimed.

This note establishes a uniform, terminating algorithm which takes a finite reduced crystallographic root system and returns a bounded complex of finite free integral Weyl-group modules. After taking the indicated cochains over any field k, the result represents RΓ(G/T,k) for the free right action of W = N_G(T)/T, for every connected complex reductive G with that root system. The differential is specified by finite Weyl-valued incidence data, which the algorithm computes. No characteristic restriction is imposed.

This is an algorithmic description in the most permissive sense. It uses general semialgebraic triangulation, implemented below by a terminating search with decidable tests. It supplies neither a practical implementation nor a root-combinatorial formula for the resulting ranks and matrices. It is a general-topology consequence of classical constructive results, and no novelty is claimed. In particular, this note does not recommend declaring the original representation-theoretic question resolved merely because this algorithm exists. Sections 9–11 distinguish the exact result from that stronger interpretation.

Two additional results are completely explicit: a three-term answer in type A₁, including its nonzero characteristic-two extension class, and a tensor-product answer for root systems A₁ʳ. A general formality obstruction explains why the modular differential cannot be discarded.

Throughout, cohomological degree is written as a superscript. For a right W-space X, the induced left action on cochains is

    (w·f)(c) = f(c·w).

All topology is ordinary complex-analytic topology, and RΓ denotes derived global sections of the constant sheaf. The spaces used below are manifolds or finite cell complexes, so singular cochains compute these derived sections.

## 1  Passing to a compact flag without changing the right action

Choose a compact real form K of G for which S = K ∩ T is a maximal torus and T is the complexification of S. The inclusions S → T and K → G are homotopy equivalences by polar decomposition. In the diagram of principal bundles with fibers S and T, the long exact sequences of homotopy groups therefore show that

    i : K/S → G/T

is a weak homotopy equivalence. Both spaces have CW homotopy type, so i is a homotopy equivalence. This argument does not assert that an arbitrary polar retraction descends through T.

The standard identification N_K(S)/S = N_G(T)/T allows representatives of every w in N_K(S). With those representatives, i is right W-equivariant. Thus restriction on singular cochains is a W-linear quasi-isomorphism. An equivariant homotopy inverse is unnecessary for this conclusion.

The map from K to its compact semisimple adjoint quotient has central kernel contained in S and induces a W-equivariant diffeomorphism of the corresponding flag manifolds. Consequently the central torus and the isogeny type of G do not affect this right W-space. Only its reduced root system Φ matters. For Φ empty, W is trivial and the answer is k in degree zero.

This is the right normalizer action on K/S. No claim is made that it is the usual holomorphic left action on G/B or that it preserves the ordinary Schubert cells.

## 2  A compact semialgebraic model from finite root data

Let r be the rank of a nonempty Φ. Construct a rational Chevalley presentation of its semisimple Lie algebra and the usual compact real form 𝔲. Its compact Cartan subalgebra 𝔰 has a basis of imaginary simple coroots. A compatible Chevalley basis gives a rational bracket table for 𝔲: one may use iH_j and, for positive roots, E_α − E_{−α} and i(E_α + E_{−α}), after the standard compact-conjugation normalization. Alternatively the eigenbasis procedure in Appendix A avoids a root-vector sign convention. Write n = dim 𝔲, fix this rational basis, and let J be the n-by-r matrix of 𝔰 ↪ 𝔲.

The matrix B of minus the Killing form is rational and positive definite. Define the compact real algebraic group

    A = {a ∈ Mat_n(R) : aᵀBa = B and a[x,y] = [ax,ay] for all basis vectors x,y}.

These are finitely many polynomial equations over Q. Orthogonality makes a invertible, so A is precisely Aut(𝔲). Its identity component K_ad is the compact group of inner automorphisms. The identity component will be computed by the finite procedure of Section 4, rather than supplied by an oracle.

Now set

    X = {aJ : a ∈ K_ad} ⊂ Mat_{n,r}(R).

This is a compact semialgebraic set with a finite formula over Q, obtained by real quantifier elimination. The stabilizer of J in K_ad is the pointwise centralizer of 𝔰, which is its maximal torus S_ad. The orbit map identifies X with K_ad/S_ad. In particular, X is connected and has dimension n − r = 2|Φ⁺|.

For each w ∈ W, let M_w be its matrix on the simple-coroot basis. These integral matrices are obtained by closing the finite set of simple reflections under multiplication. Put

    x·w = xM_w.

This is a right action since M_uv = M_u M_v. It agrees with the right normalizer action under the orbit identification. It is free: x = aJ has rank r, so xM_w = x implies M_w = 1, and the reflection representation of W is faithful. This also proves directly that no normalizer-extension splitting is being assumed.

All the real algebraic work in this section occurs in characteristic zero. The coefficient field k enters only after the integral cell data have been constructed; hence none of the real-algebraic steps divides by an element of k.

## 3  An explicit finite quotient map

Flatten the coordinates of x into a vector in R^N, where N = nr, and put m = |W|. Introduce independent variables t,z₁,…,z_N. Form the polynomial

    P_x(t,z) = ∏_{w∈W} (t − Σ_j z_j (x·w)_j).

Let q(x) be the finite ordered list of all coefficients of P_x; use any fixed ordering of monomials. Its entries are explicitly computable rational polynomials in x. They are W-invariant because right multiplication permutes the factors.

These coefficients separate orbits. Indeed, if P_x = P_y, uniqueness of factorization in R[t,z₁,…,z_N] matches the monic factor t − Σ_j z_j y_j with a factor belonging to some x·w. Thus y = x·w. The reverse implication is immediate.

It follows that q induces a continuous bijection X/W → Y := q(X). The source is compact and the target is Hausdorff, so this is a homeomorphism. Since the finite W-action on X is free, q : X → Y is a covering with m sheets. The set Y has an explicit formula over Q: eliminate x from X(x) and y = q(x).

This construction uses neither an unproved degree bound for generators of an invariant ring nor division by m. It is a separating map; generation of the full invariant ring is not needed.

## 4  A fully specified terminating triangulation subroutine

We use two classical results of real algebraic geometry: effective quantifier elimination for real closed fields, and semialgebraic triangulation over the field of real algebraic numbers. See the source credits. The following deliberately inefficient subroutine makes clear exactly what is decidable and why no topological recognition oracle occurs.

For a nonempty compact semialgebraic set Z defined over Q, define TRI(Z) as follows.

1. Enumerate all pairs (L,F), in increasing finite encoding length with a fixed tie-breaking order. L is a finite abstract simplicial complex. Its standard realization |L| uses its vertices as distinct coordinate unit vectors. F(u,z) is a quantifier-free formula with integer polynomial atoms, proposed as the graph of a map |L| → Z.
2. Replace F by its restriction to |L| × Z. Decide by real quantifier elimination whether this restricted relation is the graph of a total single-valued, injective, surjective, continuous map.
3. Return the first pair which passes.

The graph conditions are first-order sentences in ordered fields. For example, continuity can be tested with

    ∀u∈|L| ∀ε>0 ∃δ>0 ∀v∈|L| ∀a,b,
    [F(u,a) and F(v,b) and ||u−v||²<δ²] ⇒ ||a−b||²<ε².

Totality and uniqueness are checked separately. All domains and all norm expressions are polynomial formulas. A continuous bijection from compact |L| to Hausdorff Z is a homeomorphism, so an inverse-continuity test is unnecessary.

Termination follows from semialgebraic triangulation over the real algebraic numbers. Every algebraic coefficient is definable by an integer polynomial together with a rational isolating interval. Eliminating these auxiliary constants gives a graph formula of the enumerated kind. Replacing the vertices of a finite triangulation by standard unit-vector vertices merely composes its homeomorphism with a piecewise-linear map having algebraic coefficients. Therefore at least one enumerated pair passes, and every preceding test terminates.

This specifies a Turing algorithm. It does not give an efficient complexity bound, and it must not be described as an implementation that has been run on arbitrary root systems. A standard effective triangulation algorithm can replace this search without changing any subsequent proof.

A useful derived operation is COMP(Z): run TRI(Z), compute the ordinary graph-connected components of the finite complex, and return their images under its semialgebraic homeomorphism. These images have formulas obtained by quantifier elimination and are exactly the connected components of Z. Thus K_ad in Section 2 is computed as the unique component of A containing the identity matrix; membership of that matrix is decidable.

## 5  Lifts and Weyl-valued incidence coefficients

Apply TRI to Y. Denote its output by h : |L| → Y. Order the vertices of L once and orient every simplex by increasing vertex order. Write L_d for its d-simplices.

For each nonempty closed simplex σ of L, form the compact pullback

    E_σ = {(u,x) ∈ σ × X : q(x) = h(u)}.

A formula for E_σ is obtained by substituting the graph formula for h and eliminating auxiliary variables. Projection E_σ → σ is the pullback of a covering. Since σ is contractible, E_σ is the disjoint union of m copies of σ, and each connected component projects homeomorphically to σ.

Run COMP(E_σ), choose its first component in a fixed finite enumeration, and regard that component as the graph of a section

    ℓ_σ : σ → X,       qℓ_σ = h|σ.

This is an explicit semialgebraic section. There are only finitely many σ and every invocation terminates. No choice of an uncomputable point or continuous lifting oracle is part of the algorithm.

If τ is the i-th codimension-one face of σ, there is a unique g_{σ,i} ∈ W with

    ℓ_σ|τ = ℓ_τ · g_{σ,i}.                         (1)

To compute it, enumerate the finite W and test equality at the barycenter of τ by quantifier elimination, using the two graph formulas. Existence follows because q's fibers are W-orbits, and uniqueness follows from freeness. Equality at that one point implies (1) on the whole face by uniqueness of lifts on a connected space. Thus the algorithm computes an actual Weyl-group element for every incidence.

For each σ take all its m lifted cells ℓ_σ(σ)·w, with orientation pulled back from σ. Their interiors partition X and their boundaries are unions of lifted faces, by (1). These cells give a finite regular W-cell structure; the characteristic maps satisfy the usual simplex face identities. Equivalently they provide a finite Δ-complex structure with a free W-action on cells. This is sufficient for the chain and comparison constructions below.

## 6  The exact complex and its comparison map

The right integral cellular chain group in degree d is

    C_d = ⊕_{σ∈L_d} e_σ Z[W],

with boundary determined on the chosen basis by

    ∂e_σ = Σ_{i=0}^d (−1)^i e_{∂ᵢσ} g_{σ,i},       d>0.       (2)

In degree zero the boundary is zero. Extend (2) right Z[W]-linearly. If a codimension-two face is reached in two ways, the corresponding products of group elements agree, because both express the same restricted lift. The order is important: the coefficient is

    g_{τ,j} g_{σ,i},

when τ is a face of σ. Paired terms have opposite incidence signs. Hence ∂² = 0 over Z[W], including for noncommutative W.

For an arbitrary field k define the cochain complex D_k = Hom_Z(C_*,k). A completely coordinate-level specification is

    D_k^d = {functions f : L_d × W → k},
    (v·f)(σ,w) = f(σ,wv),
    (df)(σ,w) = Σ_i (−1)^i f(∂ᵢσ, g_{σ,i}w).        (3)

These formulas specify both the action and every differential. They show immediately that d is left k[W]-linear and d² = 0. For each σ the functions on W form a left regular module: the isomorphism sends a ∈ W to the delta function at a⁻¹. Thus D_k^d is free of rank |L_d| over k[W]. It vanishes outside 0 ≤ d ≤ 2|Φ⁺|.

For the comparison, send e_σw to the singular simplex given by the characteristic map ℓ_σ·w, with the affine parametrization of σ in increasing vertex order. Equation (1) shows that this is an exact chain map, not merely a map on cohomology. It is right W-equivariant. The standard simplicial-to-singular comparison theorem makes it a homology isomorphism, since these characteristic maps form the finite lifted cell structure just described. After taking cochains over the field k, it is a W-linear quasi-isomorphism. Equivalently, this is the usual cellular cochain comparison; no averaging is used.

For completeness, dualization here does not assume that Hom_Z(−,k) is exact on arbitrary integral modules. The integral comparison is a quasi-isomorphism between degreewise free abelian chain complexes bounded below. Its mapping cone is again degreewise free, bounded below, and acyclic. Its cycle groups, as subgroups of free abelian groups, are free; hence the short exact sequences from cycles to chains to cycles split, and the cone is contractible as an abelian-group complex. Applying Hom_Z(−,k) therefore gives an acyclic cochain cone over every field k. The contraction need not be W-equivariant: the comparison itself is W-linear, and quasi-isomorphism is detected on the underlying complexes.

Combining it with the equivariant inclusion in Section 1 gives W-linear quasi-isomorphisms

    S*(G/T;k) → S*(X;k) → D_k.

Consequently D_k represents RΓ(G/T,k) in Dᵇ(k[W]). The finite data (L, W, all g_{σ,i}) determine its differential and all of its derived extension information, rather than only its cohomology groups. Arbitrary choices of enumerations or lifted components change the representative, but not this derived isomorphism class.

## 7  Summary of the uniform algorithm

Input: a finite reduced root datum, or just its finite-type root system Φ. For empty Φ, output k in degree zero. Otherwise:

1. Construct the rational compact Lie bracket, B, J, and the finite reflection matrices M_w.
2. Form A by its displayed polynomial equations, and compute its identity component with COMP.
3. Eliminate variables to obtain X = A⁰J.
4. Expand P_x and form the finite polynomial map q. Eliminate variables to obtain Y = q(X).
5. Run TRI(Y), obtaining L and h.
6. For every simplex σ, run COMP(E_σ) and select its section ℓ_σ.
7. For every codimension-one face, decide the unique element g_{σ,i} at its barycenter.
8. Output the integer group-ring boundary (2), or equivalently the free k[W]-cochain complex (3).

Every loop is finite except a TRI search, and each such search has its own termination proof. The input contains no continuous or transcendental parameter. No oracle for contractibility, homeomorphism of arbitrary complexes, or equivariant triangulation is invoked. The homeomorphism verification in TRI applies to a *proposed semialgebraic graph* and is first-order decidable; it is not a decision procedure for unrestricted topological homeomorphism.

## 8  The explicit rank-one complex and its extension

Suppose Φ = A₁. Then X = SU(2)/U(1) is S², and the nonidentity element s of W = C₂ acts antipodally in the Cartan-frame model. Therefore X/W is RP². Lift the standard CW structure of RP², with one cell in each of dimensions 0,1,2. With compatible orientations its right integral chain complex has boundary coefficients

    ∂₁ = s − 1,           ∂₂ = 1 + s.

For example, a lifted one-cell joins a chosen vertex to its antipode. The boundary of a lifted two-cell traverses that one-cell and its antipodal translate with the same induced coefficient. This also verifies (s−1)(1+s)=0 directly. Taking the cochain convention of (3), and using the commutativity of k[C₂], gives

    D_k :  k[C₂] --(s−1)--> k[C₂] --(1+s)--> k[C₂],
             degree 0          degree 1          degree 2.          (4)

Its cohomology is k in degree zero, zero in degree one, and the sign representation in degree two. Indeed ker(s−1)=k(1+s), ker(1+s)=k(s−1), and the last cokernel is k[C₂]/(1+s). These identities hold in characteristic two as well.

If char(k)=2, write ε=s−1=s+1 and A=k[ε]/(ε²). Both arrows in (4) are multiplication by ε. The corresponding exact sequence

    0 → k → A --ε--> A --ε--> A → k → 0              (5)

has first map 1↦ε and last map the quotient A→A/(ε). It represents the degree-three Postnikov extension of D_k. The infinite resolution of k by copies of A with differential ε is exact; applying Hom_A(−,k) makes every differential zero. Sequence (5) is its three-extension and represents a nonzero generator of Ext³_A(k,k). In particular (4) is not isomorphic to k ⊕ k[−2] in Dᵇ(A).

When char(k)≠2 the group algebra is semisimple, so (4) splits in the derived category as k ⊕ k_sgn[−2]. Thus replacing (4) by its graded cohomology loses essential data exactly in the modular case.

For Φ=A₁ʳ, take the tensor product over k of r copies of (4), one for each generator s_j. Its module in degree d is one copy of k[(C₂)ʳ] for every a∈{0,1,2}ʳ with Σa_j=d. The differential from a to a+e_j is zero if a_j=2; otherwise its coefficient is

    (−1)^(a₁+⋯+a_{j−1}) (s_j−1),  if a_j=0,
    (−1)^(a₁+⋯+a_{j−1}) (1+s_j),  if a_j=1.

The product cell structure on (S²)ʳ proves the equivariant comparison. This answers the full derived question for this family, including arbitrary central factors and central isogenies.

## 9  A general modular obstruction

Let X be any connected finite free W-CW complex and k a field whose characteristic p divides |W|. Its equivariant cochain complex is perfect. It cannot be formal as a k[W]-complex.

Indeed, formality would make H⁰(X;k)=k a direct summand of that perfect derived object. Perfect objects are closed under direct summands, so the trivial k[W]-module would have finite projective dimension. Choose a subgroup C_p by Cauchy's theorem. Restriction preserves projectivity, because k[W] is free over k[C_p], so k would have finite projective dimension over k[C_p]. This is impossible: with u a generator, the resolution alternating u−1 and 1+u+⋯+u^(p−1) is exact, and applying Hom_{k[C_p]}(−,k) gives nonzero Ext in every nonnegative degree. Both maps become zero under augmentation in characteristic p.

Conversely, if char(k) does not divide |W|, Maschke's theorem makes every bounded complex of k[W]-modules split into its cohomology in the derived category. Applied to the compact flag, this yields the exact criterion

    RΓ(G/T,k) is formal as a k[W]-complex
    if and only if char(k)=0 or char(k) does not divide |W|.

This is an elementary consequence of perfection and connectedness, not a claimed new formality theorem. It rules out the zero-differential coinvariant-algebra answer in every genuinely modular case. It is a counterexample to that tempting proposed answer, not a counterexample to the original request for a description.

## 10  What the algorithm does and does not answer

Merely saying that a smooth free finite-group action admits a finite equivariant triangulation proves existence of a perfect complex but does not display one or specify how its incidences are to be obtained. Sections 2–7 go further: they give finite rational input, a separating quotient map, a terminating search with explicit decidable predicates, procedures for selecting the lifted cells, and formulas for all Weyl-valued differentials and the equivariant comparison. Thus they meet a *computability-based* meaning of a uniform finite cochain model.

The distinction remains substantial. The general construction works for any compact semialgebraic free action of a finite group after suitable rational input is supplied. It does not reveal the desired Weyl representation structure, produce tractable matrices from Bruhat or root combinatorics, identify a canonical or minimal object, or explain the extensions in higher irreducible rank. The root-system dependence of the output is hidden inside potentially enormous general real-algebraic searches. None of the higher-rank TRI searches has been executed here.

Juteau's original question follows the characteristic-zero graded regular representation and asks for a description “as above.” That context reasonably asks for structural representation-theoretic information beyond generic computability. The present algorithm therefore should not be advertised as settling that interpretation. A safe report is: a complete generic algorithmic encoding is established; an explicit small model is established for A₁ʳ; a structural general formula remains unprovided. Whether the weak algorithmic interpretation is the intended endpoint is a question of scope, not a missing proof disguised as a solved open problem.

## 11  Relation to the checked literature

The original question is Daniel Juteau's contribution to the problem session of Oberwolfach Report 13/2012, printed page 804. The compact right action used here agrees with the action discussed in Arthur Garnier's work on equivariant flag cell structures.

Garnier's arXiv:2011.06338 version 5 has arXiv version date 30 June 2026 and manuscript front-page date 1 July 2026. It develops a geometric method with hypotheses on a Dirichlet–Voronoi domain and gives an explicit complex for the *real* SL₃ flag manifold. Its general construction retains conditions to be verified. Neither that result nor the earlier Chirivì–Garnier–Spreafico real-flag construction is being claimed to solve the all-complex-G problem. The brute-force semialgebraic method in this note is of a different, much less structural kind. The A₁ calculation and the general topology used above are classical.

## Appendix A  A finite rational compact-form construction without sign ambiguity

One can replace the Chevalley-basis normalization in Section 2 by the following finite procedure. Construct the integral root-string matrices E_i,F_i,H_i on the space with basis {u_j}∪{v_α} using Geck's construction, §§3–4. Concretely E_i sends u_j to |⟨α_i,α_j∨⟩|v_{α_i}, sends v_{−α_i} to u_i, and sends v_α to (q+1)v_{α+α_i} when that root exists, where q is the length of the downward α_i-string through α. F_i has the reversed-root formula; H_i=[E_i,F_i]. All entries are integers calculated from the finite root system.

Start with these matrices and repeatedly adjoin brackets which increase their rational linear span. This process stops inside a finite-dimensional matrix space and yields the split rational semisimple Lie algebra 𝔤_Q. Let Ω fix u_j and interchange v_α and v_{−α}; let D fix u_j and multiply v_α by (−1)^(height α). Conjugation by DΩ is the rational involution θ with θ(E_i)=−F_i, θ(F_i)=−E_i and θ(H_i)=−H_i. Compute its ±1 eigenspaces by rational linear algebra.

The real Lie algebra

    𝔲 = (𝔤_Q^+ ⊗R) ⊕ i(𝔤_Q^- ⊗R)

is the usual compact real form, and its bracket has rational structure constants: brackets of two imaginary basis vectors pick up a minus sign. Its compact Cartan is the span of iH_i. This supplies B and J by finite rational matrix operations. The standard compact-real-form theorem supplies negative definiteness of the Killing form; positive definiteness of the computed B can also be checked by rational principal minors. For reducible Φ, use the direct sum of its irreducible constructions.

The root-string matrix construction and its identification with the semisimple Lie algebra are credited to Geck's exposition of Lusztig's construction. No part of that prior construction is claimed as new here.
