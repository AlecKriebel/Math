# Ordinary versus immersive simplicial volume: partial results and a local obstruction

Problem 30001810 / OWR-5158-010; queue rank 980. Prepared 2026-10-07.

## Status and exact scope

The equality asked in Bucher's 2011 Oberwolfach contribution is **not resolved here**. This report proves several elementary structural reductions and a concrete obstruction to one proposed local proof strategy. No novelty or independent discovery claim is made for the structural facts.

Let M be a smooth, closed, connected, oriented n-manifold. Chains are finite ordinary singular chains with real coefficients. A top-dimensional singular simplex σ:Δⁿ→M is admissible, or immersive, when it is the restriction of a smooth immersion U→M from an open neighborhood U of Δⁿ in its affine span Rⁿ. Thus the differential has rank n on the whole simplex, including its boundary. Equivalently in equal dimensions, the extension is a local diffeomorphism. Injectivity on the whole simplex is not required.

Set

    μ(M) = inf { ||z||₁ : ∂z=0, [z]=[M] in H_n(M;R),
                          every simplex of z is immersive }.

The infimum is over representatives of the fundamental class in ordinary homology. Bounding chains need not be immersive. In fact, no (n+1)-simplex can immerse into an n-manifold, so the top homology of the truncated immersive chain complex must not be confused with ordinary top homology.

Write ν(M)=||M|| for ordinary real simplicial volume. Smooth triangulation supplies an admissible integral fundamental cycle; hence 0≤ν(M)≤μ(M)<∞. The only foundational smooth-topology existence input used here is the standard smooth triangulation theorem in the form that closed simplices admit smooth nondegenerate extensions in their affine spans. The question is whether μ(M)=ν(M) whenever M is aspherical. The source adds no dimension exclusion. For n=0 both norms of a connected oriented point equal 1. The arguments below use n≥1 when faces or coverings are discussed.

Neither relative/noncompact norms, nonorientable conventions, integral simplicial volume, nor Lipschitz simplicial volume are substituted for this definition. A pseudomanifold below is only an auxiliary source for a cycle; the question's target remains a smooth manifold.

## 1. Exact rational reduction

**Proposition 1.** In the definition of μ(M), rational cycles give the same infimum. More precisely,

    μ(M) = inf { ||c||₁/d : d is a positive integer,
                  c is an integral immersive cycle, [c]=d[M] }.

Here the class on the right can be taken in integral homology. The same formula without the word immersive holds for ν(M).

**Proof.** Fix an integral immersive fundamental cycle t from a smooth triangulation. Given a real immersive fundamental cycle z=Σ a_i σ_i, ordinary homology gives a finite real chain w=Σ b_j τ_j such that z−t=∂w. Treating the finitely many distinct singular n-simplices occurring in z, t, and ∂w as a basis makes this relation a finite affine linear system in the a_i and b_j. Its matrix and right-hand side have integer entries. A nonempty real solution set of such a system has a rational particular solution and a basis of its direction space over Q, by Gaussian elimination. Its rational points are therefore dense in its real points.

Approximate the a_i and b_j simultaneously by such a rational solution. The new z' has support among the same immersive σ_i, satisfies z'−t=∂w', and has ||z'||₁ arbitrarily close to ||z||₁, because the ℓ¹ norm on a finite-dimensional coefficient space is continuous. Multiplying z', w', and t by a common positive denominator d gives integral chains c and u with c−dt=∂u. Thus c represents d[M] integrally and ||c||₁/d=||z'||₁. Conversely c/d is an admissible real fundamental cycle. Taking infima proves the assertion. The proof with an ordinary integral t and ordinary z proves the ordinary statement. ∎

## 2. Exact pseudomanifold reformulation

Allow finite oriented face-paired n-dimensional pseudomanifolds P, possibly disconnected, with self-identifications of faces and arbitrary singular lower-dimensional links. Each codimension-one face occurrence is paired with exactly one other occurrence by an orientation-reversing boundary identification. No smooth manifold structure on P or global immersion P→M is asserted.

**Proposition 2.** μ(M) is the infimum of N/d over such P with N oriented top-simplex occurrences and continuous maps F:P→M whose restriction to every parametrized top simplex is immersive, and for which the sum of oriented simplex images represents d[M], d>0. The analogous formula with unrestricted simplex maps equals ν(M).

**Proof.** Expand the integer coefficients of a cycle c in Proposition 1 as signed copies of its singular simplices. Because ∂c=0 in the free singular-chain group, every occurrence of every parametrized face with positive induced sign can be paired with an occurrence of that same face map with negative induced sign. Glue each such pair using the affine map that respects the face parametrizations. The source orientations match with opposite induced boundary orientations; all faces are paired. The simplex maps descend to a continuous F. There are exactly ||c||₁ top-simplex occurrences, and their pushforward is c.

Conversely the sum of the oriented top-simplex maps of any such P is a cycle. Its ℓ¹ norm is at most N, since equal singular simplex maps can cancel or combine. Dividing by d gives a real admissible fundamental cycle. These two constructions and Proposition 1 give equality of the infima. ∎

This formulation exposes the remaining optimization problem: can ordinary degree-d pseudomanifold representatives be replaced by simplexwise-immersive ones with top-simplex count at most the original count plus o(d)? Asphericity alone does not provide that replacement.

## 3. Finite covers, self-covers, and equality inheritance

**Proposition 3.** If p:N→M is a d-sheeted smooth covering between connected closed oriented n-manifolds, with orientations chosen so its degree is d>0, then

    μ(N)=d μ(M),       ν(N)=d ν(M).

Consequently μ(M)=ν(M) if and only if μ(N)=ν(N).

**Proof.** Composition with the local diffeomorphism p sends immersive simplices to immersive simplices and is an ℓ¹-nonincreasing chain map. For an immersive fundamental cycle z_N, p_*z_N/d represents [M]. Hence μ(M)≤μ(N)/d.

In the other direction, define transfer T on each singular simplex by summing its d lifts to N. Restrictions of the d lifts to a face are exactly all d lifts of that face, so ∂T=T∂. If a simplex extends immersively to U⊂Rⁿ, choose a smaller convex open neighborhood V of its compact convex domain inside U. Each lift extends across V by the covering lifting theorem and remains an immersion because the covering is a local diffeomorphism. Thus T preserves admissibility. Also ||Tz||₁≤d||z||₁. In homology, p_*T=d id, while p_*[N]=d[M]. Since H_n(N;R) is generated by [N], T[M]=[N]. It follows that μ(N)≤dμ(M). The reverse inequality already proved gives equality. Removing immersion restrictions proves the same statements for ν. ∎

**Corollary 3.1.** If M has a smooth self-cover of d>1 sheets, then μ(M)=ν(M)=0. If a connected finite cover of M has such a self-cover, the same conclusion holds for M. In particular all positive-dimensional tori, all smooth manifolds finitely covered by a torus, and all products N×S¹ with N closed oriented satisfy equality with value zero.

**Proof.** Finiteness of μ and μ=dμ force μ=0; ν≤μ. For the last product, the map (x,z)↦(x,zᵏ) is a smooth k-sheeted self-cover for every k≥2. ∎

A general map of nonzero degree is not an allowable substitute for a local diffeomorphism: postcomposing an immersive simplex with a map having a critical point can destroy its rank. Thus the familiar ordinary degree inequality cannot be imported wholesale. Likewise, an arbitrary finite-cover tower gives only μ(M_i)=d_i μ(M), not vanishing. One still needs an independent sublinear upper bound for μ(M_i).

## 4. A product inequality

**Proposition 4.** For smooth closed connected oriented manifolds Mᵖ and Nᑫ,

    μ(M×N) ≤ binomial(p+q,p) μ(M) μ(N).

In particular if either factor has μ=0, both immersive and ordinary simplicial volume of the product vanish.

**Proof.** For top simplices σ and τ, form the usual shuffle chain σ×τ. A (p,q)-shuffle gives an affine map A:Δ^(p+q)→Δᵖ×Δᑫ whose vertices follow a staircase in the product vertex grid. The successive edge increments are the p independent M-coordinate increments and the q independent N-coordinate increments, in some order. Thus A is an affine isomorphism onto its full-dimensional image. If σ and τ extend as immersions to U and V, their product is an immersion on U×V. Its composite with A extends immersively to the inverse image under A of U×V, an open neighborhood of Δ^(p+q). Every term of σ×τ is therefore immersive.

For clarity, the signed shuffle chain uses one sign for each permutation of the p first-factor and q second-factor increments. Deleting an interior path vertex gives a face shared by the two orders of one adjacent mixed pair, with opposite induced orientations, so these faces cancel. The remaining faces are precisely the shuffle terms for factor faces. This proves the boundary identity

    ∂(a×b) = (∂a)×b + (−1)^p a×(∂b).

The cross product of fundamental cycles is the fundamental cycle for the product orientation; this can be checked locally on the product of oriented coordinate charts by this staircase triangulation. There are binomial(p+q,p) terms for every input pair, each with coefficient magnitude equal to the product of the input magnitudes. Hence

    ||a×b||₁ ≤ binomial(p+q,p) ||a||₁ ||b||₁.

Choose admissible fundamental cycles with norms converging to μ(M) and μ(N), respectively, and take the limit. Finiteness of the two norms makes the zero-factor conclusion immediate. ∎

This proposition is not a sharp product formula. In particular, it does not establish equality of ordinary and immersive volume for arbitrary products of positive-volume factors. The locally symmetric product cases mentioned by the original report use additional geometric input.

## 5. Explicit failure of face-fixed immersive replacement

**Proposition 5.** There is a smooth singular 2-simplex in an aspherical 2-torus whose three edges are immersive, but whose boundary is not the boundary of any immersive singular 2-simplex with the same parametrized faces.

**Proof.** Work first with the oriented triangle

    D = conv{ (−2,0), (1,1), (1,3) }
      = { −2≤x≤1, (x+2)/3≤y≤x+2 }.

An orientation-preserving affine map from the standard 2-simplex to D turns all the following maps into singular simplices. Let f:D→R² be f(x,y)=(x²,y). For each of the three edges, a linear parametrization has nonzero y-velocity: the y-coordinate changes respectively by 1, 2, or 3, up to sign. Therefore the derivative of f along that edge has nonzero second component. Every edge map extends as an immersion to an open interval containing the whole edge parameter domain.

Consider the two points

    a=(1/4,3/5),       b=(1/4,2).

A preimage of either must have x=±1/2. At x=−1/2 the interior y-range is (1/2,3/2); at x=1/2 it is (5/6,5/2). Thus a has exactly one preimage in D, namely (−1/2,3/5), and b has exactly one preimage, namely (1/2,2). Neither point lies in f(∂D). Since det Df=2x, their Brouwer degrees are

    deg(f,D°,a)=−1,       deg(f,D°,b)=+1.

Now let π:R²→T²=R²/(10Z)² be the smooth covering and set σ=π∘f. The torus is smooth, closed, oriented, and aspherical. Suppose g:D→T² is an immersive simplex and agrees with σ on all of ∂D. Because D is simply connected, g lifts to G:D→R². Adjusting by one deck transformation makes G equal f at one boundary point, and uniqueness of path lifting then gives G=f on all of the connected boundary. A sufficiently small convex open neighborhood of D supports a smooth lift of the immersion extending g; hence G has nonzero determinant everywhere on D.

Since D is connected, det DG has a constant sign. For any point outside G(∂D), the degree of G is the sum of this same sign over its finitely many interior preimages, or zero if there are none. All such degrees are therefore nonnegative, or all nonpositive.

On the other hand, G and f have identical boundary values, so the straight-line homotopy between them fixes ∂D. Homotopy invariance of degree at a and b gives degrees −1 and +1 for G. This contradicts their required common sign. Thus no such g exists. ∎

The ingredients of this argument are only the elementary lifting theorem, the inverse function theorem, and the regular-value formula and boundary-fixed homotopy invariance for Brouwer degree. No unproved claim about immersive simplicial volume is used.

The proposition is a counterexample to a local extension strategy, not to μ=ν. Indeed μ(T²)=ν(T²)=0 by Corollary 3.1. It also explains why contractibility of a universal cover is insufficient: it supplies continuous fillings, but imposes no nonvanishing-Jacobian condition or ℓ¹ budget on those fillings. Ordinary subdivision can change the situation, but repeated barycentric subdivision has a potential factor ((n+1)!)^k in the chain norm after k iterations and therefore supplies no norm-preserving argument by itself.

## 6. Exact dual formula and a sharp remaining extension problem

For an ordinary singular n-cochain φ define

    ||φ||_imm = sup { |φ(σ)| : σ is an immersive n-simplex }.

This quantity may be finite even when the usual supremum over all singular n-simplices is infinite. A singular cocycle means a linear cochain annihilating the ordinary boundary space B_n=∂C_(n+1)(M;R).

**Proposition 6 (duality).**

    μ(M) = sup { <φ,[M]> : φ is an ordinary singular n-cocycle,
                            ||φ||_imm≤1 }.

The supremum is attained. The same assertion with a bound on all singular simplices gives ν(M).

**Proof.** Write C=C_n(M;R), equipped with the ℓ¹ norm on finite chains; let I⊂C be the span of immersive n-simplices, and Z=I∩ker ∂. Since H_n(M;R)=R[M], each z∈Z has [z]=deg(z)[M]. By the definition of μ,

    μ(M)|deg(z)| ≤ ||z||₁.

Indeed, if deg(z)≠0, then z/deg(z) is an immersive fundamental cycle; otherwise the inequality is trivial. Therefore L:Z→R, L(z)=μ(M)deg(z), is linear of norm at most one. The real Hahn–Banach theorem extends it to a linear E:I→R with |E(i)|≤||i||₁.

If i∈I∩B_n, then i is an immersive cycle homologous to zero, so E(i)=L(i)=0. It follows that the rule

    F(i+b)=E(i),       i∈I, b∈B_n,

is a well-defined linear functional on I+B_n. Extend F algebraically to the whole vector space C by choosing a vector-space complement. Call the resulting cochain φ. It annihilates B_n and so is a singular cocycle. It satisfies |φ(σ)|≤1 on every immersive simplex. An immersive fundamental cycle t belongs to Z and satisfies φ(t)=μ(M), proving attainment of at least that value.

Conversely, for any cocycle with ||φ||_imm≤1 and any immersive fundamental cycle z,

    |<φ,[M]>| = |φ(z)| ≤ ||z||₁.

Taking the infimum over z proves that the displayed supremum is at most μ(M). No positivity assumption was used; when μ=0 the construction can use φ=0. Repeating the argument with I=C gives the ordinary dual formula and an ordinary bounded cocycle attaining ν(M). ∎

**Corollary 6.1 (exact comparison criterion).** The following are equivalent:

1. μ(M)=ν(M).
2. Every singular n-cocycle φ with ||φ||_imm≤1 is cohomologous, in ordinary real cohomology, to a cocycle ψ with |ψ(σ)|≤1 on every singular n-simplex.

**Proof.** Assume equality and write a=<φ,[M]>. Proposition 6 gives |a|≤μ(M)=ν(M). If ν(M)>0, choose an ordinary bounded cocycle ψ₀ with supremum norm at most one and evaluation ν(M), using ordinary duality. Then ψ=(a/ν(M))ψ₀ has supremum norm at most one and the same evaluation as φ. Evaluation on [M] is an isomorphism Hⁿ(M;R)→R for a connected closed oriented n-manifold, so ψ and φ are cohomologous. If ν(M)=0, the equality assumption gives a=0 and φ is cohomologous to zero, which provides ψ.

Conversely apply condition 2 to a maximizing immersive-bounded cocycle from Proposition 6. Its replacement has evaluation μ(M) and ordinary supremum norm at most one, so ordinary duality gives μ(M)≤ν(M). Together with ν≤μ this proves equality. ∎

Hahn–Banach alone has not solved the problem: its controlled extension stops at I, whereas extension past I+B_n was purely algebraic and has no norm bound. The exact outstanding issue is whether asphericity forces condition 2. Equivalently, it must permit global near-optimal immersive cycles despite the explicit fixed-boundary obstruction in Section 5.

## 7. What is established, and what remains

The proved statements apply to all smooth closed connected oriented manifolds, without an asphericity hypothesis: rational/pseudomanifold formulas, cover multiplicativity, the product upper bound, and the duality/comparison criterion. Equality is established here for the self-cover and zero-product families specified above. The fold obstruction uses an aspherical target and definitively excludes a face-fixed local repair argument. It is not a counterexample to the proposed equality.

The arbitrary-aspherical case remains open in this work. In particular, no general immersive straightening, isometric homology theorem, bounded-extension theorem, or strict inequality for a closed aspherical manifold has been proved. The fact that an arbitrary chain can be smoothed, or that immersed-simplex homology agrees with ordinary homology in certain lower degrees, supplies none of the missing top-dimensional norm control.

### Source dependencies and attribution

- The exact problem and its immersion definition come from Michelle Bucher's contribution, “Euler characteristic, simplicial volume and the Schläfli volume formula,” in *Arithmetic Groups vs. Mapping Class Groups: Similarities, Analogies and Differences*, Oberwolfach Report 30/2011, printed pp. 1673–1675, especially Question 4 on p. 1675. [Official report](https://ems.press/content/serial-article-files/46346), [DOI](https://doi.org/10.4171/owr/2011/30).
- That report announces |χ(M)|≤μ(M) for smooth closed oriented M and records equality in certain locally symmetric cases. Its supporting Bucher manuscript is listed as “Preprint in preparation 2011.” The proof of that announcement was not independently recovered or used in any proposition above. The corpus's second URL is the same report PDF, not a second independently checked manuscript.
- The proofs above use standard foundational results stated at their points of use: smooth triangulation, finite-cover lifting and transfer, top-dimensional orientation homology/cohomology, Brouwer degree, and the real Hahn–Banach theorem. The propositions' substantive arguments are supplied here; no unpublished Euler-cocycle construction is assumed.
- The source/status record separately distinguishes later neighboring results from a solution of the immersive comparison. A literature search that finds no resolution is evidence of the search outcome, not proof of perpetual openness.
