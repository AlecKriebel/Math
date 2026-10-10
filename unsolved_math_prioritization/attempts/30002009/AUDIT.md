# Independent audit of the derived Weyl group complex

## Decision and accepted scope

This is an independent internal AI mathematical audit of AI-assisted authored mathematics. Its acceptance is limited to the exact PARTIAL result below. The proof and audit are unrefereed; no external human peer review or formal proof-assistant certification is claimed.

**ACCEPT the stated mathematical results. Retain PARTIAL for problem 30002009 / OWR-11580-019.** No blocking mathematical gap was found in the supplied manuscript.

The accepted results are:

1. A uniform terminating procedure from finite reduced crystallographic root data to bounded finite free integral right Weyl-group cellular chains, whose indicated cochains represent RΓ(G/T,k) for every field k and every connected complex reductive G with that root system.
2. The explicit three-term A₁ complex and its nonzero characteristic-two Ext³ class, together with the A₁ʳ tensor-product models.
3. Formality exactly when the characteristic does not divide the Weyl-group order, with characteristic zero included.

The first result is generic computability via semialgebraic topology. It supplies no practical higher-rank computation, closed root-combinatorial differential, minimal representative, or novelty claim. This audit does not promote it to a full structural solution of Juteau's original question.

The manuscript, summary, status, source credits, and diagnostic material were reviewed. The accepted original proof has 23,794 bytes and SHA-256 2ba51c22621277170daef73ce3bc5ae299cb1477e824cf74c97521cd28bd5b7d. This prose edition adds explicit internal AI-review framing and the two expository clarifications recommended below; it preserves the complete mathematical argument. ACCEPTANCE.json distinguishes accepted original and distributed document identities. This is a mathematical audit supported by finite diagnostic checks, not a machine-checked formal proof.

## Compact reduction and action

The compact-to-complex comparison is valid. Choose a compact real form K compatible with T and let S=K∩T. Polar decomposition gives homotopy equivalences on the total groups and torus fibers. The maps of homogeneous-space fibrations then give a weak equivalence K/S→G/T; the spaces have CW homotopy type. This avoids an unjustified assertion that a polar retraction descends through T. The polar-decomposition input is stated for reductive real groups in [Yun, §1.7](https://math.stanford.edu/~conrad/JLseminar/Notes/L6.pdf); a complex reductive group is considered as a real group here.

The standard normalizer identification supplies representatives in N_K(S), so the inclusion is right W-equivariant. An ordinary homotopy equivalence together with equivariance suffices to obtain a W-linear cochain quasi-isomorphism; an equivariant homotopy inverse is unnecessary.

The center of K is contained in every maximal torus, including disconnected central elements. Consequently the central quotient induces K/S≅K_ad/S_ad and preserves the normalizer action. This eliminates both the central torus and the central isogeny ambiguity. The empty-root-system case is correctly separated. [Conrad–Landesman, Corollary 11.5 and the central-quotient discussion](https://math.stanford.edu/~conrad/210CPage/handouts/lie_groups_notes.pdf) support these compact-group inputs.

This action is right multiplication by normalizer classes. No substitution of the holomorphic left action on G/B, preservation of Schubert cells, or splitting of the normalizer extension is used.

## Finite rational Lie input

Appendix A removes the sign ambiguity that can otherwise afflict compact Chevalley-basis constructions. In [Geck, §3](https://arxiv.org/abs/1602.04583v5), the upward root-string coefficient is m_i⁻(α)=q+1, where q is the number of downward steps. The coefficient on u_j is |⟨α_i,α_j∨⟩|. Both agree with the manuscript. The identity H_i=[E_i,F_i], Geck's root-system identification in Theorem 4.6, and the coroot identification in Remark 4.7 have the needed conventions. Geck assumes irreducibility for Theorem 4.6; the manuscript explicitly takes direct sums for reducible inputs.

Closure under brackets is a finite rational-linear-algebra computation: every new independent bracket increases a span inside a fixed finite-dimensional matrix space. The involution Ω reverses roots, D records height parity, and conjugation by DΩ sends E_i to −F_i and H_i to −H_i. The two matrices commute and square to one. Its rational eigenspaces are computable, and replacing the negative eigenspace by its imaginary copy produces rational structure constants because brackets of two such vectors acquire a factor −1.

The compact-real-form theorem identifies this as the compact form. Its minus Killing form is positive definite. Automorphisms preserve the Killing form, so the polynomial equations for bracket preservation and B-orthogonality describe precisely Aut(𝔲), a compact real algebraic group. Semisimplicity is essential here: all derivations are inner, hence Aut(𝔲)⁰ is the adjoint compact group. These imported Lie-theoretic facts are independently corroborated by [Knapp, §3, especially p.15, and §4, p.21](https://www.math.stonybrook.edu/~aknapp/pdf-files/1-27.pdf).

The frame J fixes a basis pointwise, not merely the Cartan subspace setwise. Its stabilizer is therefore the Cartan centralizer, namely the maximal torus. The orbit X=Aut(𝔲)⁰J is the correct compact flag manifold. For a column-coordinate convention, coroot reflections use the transpose Cartan indexing relative to root reflections. The equation Ad(n_w)J=JM_w yields x·w=xM_w, with M_uv=M_uM_v. Since every x has full column rank and the reflection representation is faithful, this action is free.

The finite input computations stay over Q and R. Arbitrary fields enter only through scalar cochains on integral data. The result does not require an algorithm for arithmetic in every possible coefficient field.

## Quotient construction

The coefficient vector of

P_x(t,z)=∏_{w∈W}(t−z·(x·w))

is finite, rational-polynomial, and invariant. Equality of coefficient vectors gives equality of polynomials. Unique factorization matches the monic linear factor t−z·y with a factor from x's orbit, proving orbit separation. This works without invariant-ring generation or a degree bound.

The induced map X/W→q(X) is a homeomorphism by compactness and the Hausdorff property. A free action of a finite group on this manifold is a covering action; the quotient has |W| sheets. The semialgebraic image is obtained by quantifier elimination. No division by |W| is present.

## Decidability and termination of triangulation

TRI enumerates finite syntactic objects. For each candidate, totality, single-valuedness, injectivity, surjectivity, and the displayed epsilon–delta continuity condition are first-order statements over real closed fields. Restricting the relation to |L|×Z does not invalidate these tests. Strict inequalities and squared Euclidean distances express the needed topology, with positive epsilon and delta. Each test terminates by effective real quantifier elimination.

A passing candidate is a homeomorphism because its domain is a finite compact polyhedron and its codomain is Hausdorff. The procedure does not ask whether two unrestricted finite complexes are homeomorphic. It verifies a proposed finite semialgebraic graph.

Existence of semialgebraic triangulations ensures a passing candidate. Algebraic constants are definable by integer polynomials and rational isolating intervals, so their graph formulas reduce to integer-coefficient formulas after quantifier elimination. Standard unit-vector realizations cause no obstruction. [Basu, §§2.1 and 3.5](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf) explicitly discusses effective quantifier elimination and semialgebraic triangulation. The field issue can also be checked independently: for a fixed finite graph syntax with finitely many real coefficients, the statement that some coefficient tuple satisfies the homeomorphism tests is first-order over Q. If true over R, it is true over the real algebraic numbers. Thus even an ordinary semialgebraic triangulation witness has an algebraic-coefficient replacement for this purpose.

COMP terminates by TRI followed by finite graph connectivity. Images of the resulting subcomplexes are the actual connected components over R, and their formulas follow by quantifier elimination. Selecting the component of Aut(𝔲) containing the identity is decidable. Every input to TRI or COMP here is nonempty and compact. There is no circular use of a connected-component oracle to justify triangulation termination.

The argument proves termination, not a useful running time. No higher-rank triangulation has been executed. In particular, none of the low-rank Lie-algebra diagnostics can be described as a computed higher-rank flag complex.

## Lifted simplices and incidences

Each E_σ is the pullback of the covering to a closed simplex. A closed simplex is connected, locally path connected, and simply connected; its covering is therefore a disjoint union of |W| copies of that simplex. Its connected components are compact semialgebraic graphs of continuous sections. COMP computes these graphs without selecting an uncomputable real point.

The barycenter of a nonempty face is rational. Equality of two section values after a candidate Weyl translate is a first-order statement involving their graph formulas. A unique candidate exists because each fiber is a free W-orbit. Equality at that point extends throughout the connected face by covering-space uniqueness of lifts.

The translated characteristic simplices have disjoint interiors, cover X, and meet along entire lifted faces. More precisely, the intersection of two base simplices is a face; two restricted covering sections on that connected face either agree everywhere or have disjoint images. This justifies the regular cell structure and its compatible simplex parametrizations. No arbitrary characteristic maps for a general CW complex are being mistaken for an exact singular chain map.

## Group-ring order and cochains

With right chains, the restriction identity ℓ_σ|τ=ℓ_τg_(σ,i) gives

∂e_σ=Σ_i (−1)^i e_(∂ᵢσ)g_(σ,i).

Applying ∂ once more places a codimension-two coefficient in the order g_(τ,j)g_(σ,i). That order is forced by right-linearity. The two paths to the same face describe the same restricted lift; their coefficients agree and their signs cancel. Reversing the order is generally wrong.

The pullback convention (v·f)(σ,w)=f(σ,wv) is a left action: applying v₂ and then v₁ evaluates at wv₁v₂. The differential evaluates at g_(σ,i)w, so it commutes with this action. The regular-module identification a↦δ_(a⁻¹) is correct. No unannounced commutative-group convention is used in the general construction.

Independent tests on an S₃ covering of a tetrahedron verify integral ∂²=0 and cochain equivariance for every group element. They reject the reversed incidence product on five simplices and the left-argument substitute for the cochain action in fifteen tests. This is a convention check on a toy covering, not a triangulation of the SL₃ flag manifold.

## Comparison with singular cochains

The characteristic simplices define an actual right W-linear chain map into singular chains. Their face restrictions agree exactly, by the incidence equations. The applicable imported theorem is [Hatcher, Theorem 2.27](https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf): the canonical characteristic-simplex map of a Δ-complex induces the singular-homology isomorphism. Its hypotheses apply to the lifted structure just verified.

One small explanatory point deserves emphasis. Hom_Z(−,k) is not an exact functor for arbitrary integral modules. Here both chain complexes are degreewise free abelian and bounded below, and their comparison is an integral quasi-isomorphism. Its acyclic free mapping cone is contractible as an abelian-group complex; equivalently one can first use the free-chain coefficient theorem and then exact vector-space duality. Thus cochains over every field do give a quasi-isomorphism. The contraction need not be W-equivariant: the comparison itself is W-linear, and quasi-isomorphism is detected on the underlying complexes. No averaging or modular semisimplicity is needed.

Finite-dimensionality of X and invariance of dimension give dim L=2|Φ⁺|. Hence the resulting cochain complex is bounded in the asserted degrees and finite free over k[W]. The compact comparison completes the claimed representation of the derived global sections of the constant sheaf. Smooth manifolds and finite complexes have the local properties needed for singular cochains to compute those sections.

## Rank one and products

In type A₁ the Cartan-frame model is S² with the antipodal involution; the quotient is RP². Lifting its standard CW structure gives right-chain coefficients s−1 and 1+s. These commute, and s=s⁻¹, so dualization gives the displayed cochain arrows in degrees 0,1,2. The kernel and cokernel calculations yield trivial H⁰, zero H¹, and sign H² over every field.

In characteristic two, A=k[ε]/(ε²) and both differentials are ε. The canonical truncation triangle has connecting map H²[−2]→H⁰[1], hence class in Ext³_A(k,k). The exact sequence with three middle copies of A is the first three steps of the periodic free resolution, with the third syzygy εA identified with k. Under dimension shifting it maps to the nonzero identity of that syzygy, so its class generates Ext³_A(k,k). Applying Hom_A(−,k) to the periodic resolution makes every differential zero. This proves the nonsplitting, rather than merely comparing Betti numbers.

The A₁ʳ formula uses tensor products over the field, external product group actions, and the ordinary Koszul sign determined by preceding degrees. Product cells provide the comparison. A central quotient does not couple or alter the adjoint product flag. The empty product gives the already separated torus case.

## Formality criterion

For a connected finite free W-CW complex, the bounded free cochains form a perfect object and H⁰ is trivial k. If the complex were formal, k would be a direct summand of a perfect object and would itself be perfect. A module perfect in degree zero has finite projective dimension.

When p divides |W|, a subgroup C_p exists. Restriction of projectives remains projective because the group algebra is free over the subgroup algebra. But k[C_p]≅k[t]/(t^p), and the resolution alternating t and t^(p−1) is exact and has zero differentials after Hom to k. It has nonzero Ext in arbitrarily large degrees. This contradicts finite projective dimension.

When the characteristic is nonmodular, Maschke's theorem gives splittings of the cycles and boundaries in every degree, hence formality. Connectedness, finiteness, and freeness are all used and are all established for the compact flag. The theorem does not assert anything about disconnected reductive groups. The conclusion is a standard consequence of these facts, with no novelty claimed.

## Original question and literature boundary

The original question is on printed p.804 of [Oberwolfach Report 13/2012](https://ems.press/content/serial-article-files/46383). Its comparison to the characteristic-zero graded regular representation supports a structural reading. Generic computability does not provide that representation-theoretic structure in higher irreducible rank. The recommendation to keep PARTIAL is therefore appropriate.

[Garnier v5](https://arxiv.org/pdf/2011.06338v5) treats an equivariant-cell construction whose Proposition 3.2 requires a regular CW structure on the Dirichlet–Voronoi domain with specified wall compatibility and codimensions. Its explicit S₃ complex is for the real SL₃ flag. These extra hypotheses are not silently imported into the generic semialgebraic proof. The arXiv version date is 30 June 2026, while the manuscript's front-page date is 1 July 2026; both dates can be reported precisely. [Chirivì–Garnier–Spreafico v2](https://arxiv.org/abs/2006.14417v2) likewise has a real-SL₃ scope. Neither is evidence of an unrestricted complex-group solution.

The Delfs–Knebusch bibliographic endpoint was unavailable during this audit; it was not inspected theorem by theorem. This does not block the argument because the triangulation input is independently corroborated by Basu and the algebraic-parameter reduction above. This review is targeted verification, not exhaustive literature or priority research.

## Accepted result and remaining work

No correction is required to preserve the exact stated theorem. Two optional expository improvements would make an eventual presentation easier to audit: state the free-chain reason for arbitrary-field dualization explicitly, and distinguish Garnier's version date from its manuscript date. These are clarifications, not failures of the proof.

The remaining limitation is substantive and already disclosed: a usable, structural higher-rank description has not been supplied. The audit accepts generic computability, the explicit A₁ʳ family, and the formality criterion while rejecting any stronger solved, implemented, efficient, canonical, or novel interpretation.
