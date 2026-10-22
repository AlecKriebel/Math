# KP-4.51: checked partial results and the remaining gap

## 1. Exact target and scope

Let X be a closed, connected, oriented smooth four-manifold with π₁(X) ≅ Z. Write Λ = Z[x,x⁻¹], with involution x̄ = x⁻¹. The question is whether the nonsingular Hermitian intersection form on π₂(X), a finite free Λ-module, admits an integral Gram matrix in a Λ-basis. The ordinary involution and oriented interpretation are the conventions used here. The short question in K3 omits the word “oriented”; its remarks use that interpretation. We do not claim a result for the orientation-twisted nonorientable variant.

An integral extension must be isometric to the extension of its augmentation at x = 1: augment any purported Λ-isometry. Thus extension means actual isometry, not equality in a Witt group or after stabilization.

**Outcome:** no full resolution is claimed. Sections 2–5 establish partial statements and exact certificates. Section 6 isolates the unresolved step. The definite-case argument in Section 4 is provided in full for independent review; the underlying definite-case conclusion has prior claims in Kawauchi's work, so no novelty is claimed.

## 2. Elementary scope checks

### 2.1 Rank one

A nonsingular rank-one Hermitian form has Gram entry a ∈ Λ×. The units of Λ are ±xᵏ: comparing smallest and largest exponents in a product equal to 1 proves this immediately. The condition a = ā then forces k = 0, so a = ±1. Rank zero is vacuously extended.

### 2.2 High indefiniteness

Hambleton–Teichner's Theorem 2 proves that a nonsingular free Λ-Hermitian form of rank r and augmentation signature s is extended when r − |s| ≥ 6. Hence the target is already affirmative when min(b₂⁺,b₂⁻) ≥ 3. This is an imported theorem, not a new proof or an unrestricted cancellation rule. [HT97]

The threshold cannot be discarded merely because stable extension holds. In particular, the positive rank-four form below is non-extended, whereas adding three hyperbolic planes meets that theorem's threshold. Stable isometry and isometry are different assertions.

## 3. The classical test form and finite-cover obstruction

Set a = x + x⁻¹ and

L =

    [ 1+a+a²    a+a²    1+a    a   ]
    [ a+a²      1+a+a²  a      1+a ]
    [ 1+a       a       2      0   ]
    [ a         1+a     0      2   ].

Theorem 1 of [HT97] says L is not extended. Its augmentation is nevertheless standard. [FHMT07, Theorems 1.2 and 1.5] obstructs smooth closed realizations of L and an infinite related family. The imported catalogue's suggestion that smoothability of this particular L remains to be decided is therefore wrong.

Here are directly checkable controls, useful without taking a finite numerical experiment as a proof about every form.

Write L in 2×2 blocks as [[A,B],[B,2I]], where B = [[1+a,a],[a,1+a]]. Direct multiplication gives A − B²/2 = I/2. Consequently L is congruent over Z[1/2][x,x⁻¹] to diag(I/2,2I), and det L = 1. At every unit complex x this is a positive congruence. The denominators are essential: a rational or complex congruence supplies no integral Λ-basis.

Let Qₙ be the coefficient-of-identity integral form obtained from L modulo xⁿ−1. Put N = 1+x+⋯+xⁿ⁻¹, w = N(e₃+e₄), and c = w−2e₁. For every n, the pairing of w with xʲeᵢ is 5 for i=1,2 and 2 for i=3,4. Those have the parity of the corresponding diagonal entries, so w and c are characteristic. Also Qₙ(w,w)=4n. For n≥3, Qₙ(e₁,e₁)=3; hence Qₙ(c,c)=4n−8. A characteristic vector in the standard positive lattice Z^(4n) has all coordinates odd, so has norm at least 4n. Therefore Qₙ is not standard for n≥3. This is the obstruction of [FHMT07, Section 2], reconstructed here with the same explicit witness and full attribution.

A smooth closed realization would have smooth finite cyclic covers with these ordinary forms, contradicting Donaldson after surgery on the fundamental-group generator, as detailed below. This excludes L; it does not by itself exclude every non-extended form.

## 4. A complete algebraic reconstruction for the definite case

### Proposition 4.1: large-prime reconstruction

Let H be a nonsingular Hermitian r×r matrix over Λ, with H(1) positive definite. For n≥1 let Qₙ be the integral coefficient-of-identity form of H modulo xⁿ−1 on (Z[x]/(xⁿ−1))ʳ. If Qₚ is the standard positive lattice for arbitrarily large odd primes p, then H is Λ-isometric to Iᵣ.

The rank-zero case is vacuous; take r≥1 below. The proof gives a matrix-dependent threshold, not a uniform effective bound over all matrices. No finite list of successful cover tests verifies the hypothesis.

#### Step A: a uniform positive lower bound

Since det H is a Hermitian unit in Λ, it is ±1; positivity at 1 forces det H = 1. The eigenvalues of H(e^{iθ}) vary continuously, cannot vanish, and start positive. Thus all are positive, and compactness gives a real c>0 such that H(e^{iθ}) ≥ cI for every θ.

Use the convention h(v,w)=v*Hw and let B∞(v,w) be its coefficient of x⁰. Parseval gives

    B∞(v,v) ≥ c ∑ⱼ ||vⱼ||²

for each finitely supported integral coefficient sequence v = ∑vⱼxʲ. The finite Fourier transform gives, with the same c,

    Qₙ(v,v) ≥ c ∑ⱼ₌₀ⁿ⁻¹ ||vⱼ||².

Both identities follow by expanding the quadratic form and using orthogonality of the characters; no convergence issue arises. Choose a positive integer K ≥ max(1,1/c). A norm-one vector in any Qₙ therefore has at most K occupied coefficient positions (and at most K nonzero scalar coefficients).

Let d≥1 bound the absolute exponents in H. Constant matrices cause no difficulty and may also be assigned d=1. Put D=d(K−1), and choose an odd prime p>2dK for which Qₚ is standard.

#### Step B: unwrap every norm-one vector

For v in Qₚ of norm one, form a graph on occupied residues in Z/p. Join distinct residues whenever their cyclic difference has a representative of absolute value at most d. Distinct components have zero cross-pairing for Qₚ. Every nonzero component has positive integral norm, so their norms sum to one only if there is exactly one component.

This component has q≤K vertices. Pick a spanning tree and assign integer lifts of the vertices using the edge differences in [−d,d]. A difference along any tree path has absolute value at most d(q−1). For any extra graph edge, its prescribed residue difference differs from the assigned difference by a multiple of p of absolute value at most dq≤dK<p. That multiple must be zero. Thus all graph edges are unwrapped consistently. The assigned positions occupy an interval of diameter at most D.

Place the original integer coefficients at these positions, giving a Laurent vector ṽ. There is no aliasing in its self-pairing, since its exponent diameter plus d is at most dK<p. Therefore B∞(ṽ,ṽ)=Qₚ(v,v)=1. Multiplying by a power of x, we can and do place its support inside [0,D]. Its reduction modulo xᵖ−1 is then a deck translate of v.

#### Step C: a coefficient-norm-one vector has Laurent norm one

For k≠0, the vectors ṽ and xᵏṽ are linearly independent over R as finitely supported coefficient sequences. (A nonzero finitely supported sequence cannot equal a nontrivial translate up to a scalar.) Positivity and strict Cauchy–Schwarz therefore give

    |B∞(ṽ,xᵏṽ)| < 1.

These pairings are integers, hence zero. They are the nonconstant coefficients of h(ṽ,ṽ), up to reversing k. The constant coefficient is one. It follows that h(ṽ,ṽ)=1 in Λ.

#### Step D: extract r deck orbits

The norm-one vectors of the standard lattice Qₚ are exactly the 2rp signed vectors of an orthonormal integral basis. Deck multiplication T by x is an isometry, so it permutes their rp unoriented lines. Every line orbit has length 1 or p. A fixed line would have T acting by ±1; Tᵖ=1 and p odd force +1. Each length-p orbit has trace zero. In the original coefficient basis, T is the direct sum of r regular p-cycles, so trace T=0. Thus there are no fixed lines and exactly r line orbits, each of length p.

Choose one norm-one representative from each orbit. Apply Step B to obtain lifts ṽ₁,…,ṽᵣ with supports in [0,D]. Translating representatives in their own orbits does not merge different orbits. Every translate of one chosen line is orthogonal in Qₚ to every translate of another. Accordingly h(ṽᵢ,ṽⱼ) reduces to zero modulo xᵖ−1 for i≠j.

All exponents in such a pairing lie in [−D−d,D+d]. This interval has length 2(D+d)=2dK<p, so reduction modulo xᵖ−1 is injective on its coefficients. The pairing itself is zero. Step C supplies the diagonal pairings one.

#### Step E: the vectors are a Laurent basis

Let V have columns ṽᵢ. We have V*HV=Iᵣ. Taking determinants gives det(V)*det(V)=1 since det H=1. Thus det(V) is a unit of Λ; the adjugate formula shows that V is invertible over Λ. This proves Proposition 4.1. ∎

### Corollary 4.2: definite smooth manifolds

Using the standard free-module identification and cover-pairing identification for π₁=Z (the framework in [FQ90] and [FHMT07, Lemma 2.2]), every closed oriented smooth X with π₁(X)=Z and definite ordinary intersection form has extended equivariant intersection form. Reverse orientation for the negative definite case. If b₂=0 the form is zero.

For completeness, the Donaldson input may be restricted to simply connected manifolds. For any finite cyclic cover Y of X, b₁(Y)=b₃(Y)=1, so χ(Y)=b₂(Y). Multiplicativity of χ and signature gives b₂(Y)=n b₂(X), σ(Y)=nσ(X); definiteness is preserved.

Take an embedded generator circle with tubular neighborhood S¹×D³ in Y. Its oriented normal bundle is trivial. Put Y₀=Y\int(S¹×D³), and replace S¹×D³ with D²×S². General position in codimension three identifies π₁(Y₀) with π₁(Y). Van Kampen therefore makes the surgered smooth manifold Y′ simply connected.

The relevant excision sequence for (Y,Y₀) has H₃(Y,Y₀)=Z and H₂(Y,Y₀)=0. The map H₃(Y)→Z is intersection with the primitive circle and is an isomorphism. Hence H₂(Y₀)→H₂(Y) is an isomorphism. For (Y′,Y₀), H₃(Y′,Y₀)=0 and H₂(Y′,Y₀)=Z; its boundary map to H₁(Y₀)=Z sends the generator to the circle and is an isomorphism. Hence H₂(Y₀)→H₂(Y′) is also an isomorphism. The ordinary pairings agree, because representatives can be taken in Y₀. Donaldson diagonalizes the definite form of Y′, and therefore Qₙ is standard. Proposition 4.1 applies.

This proof does not use a theorem descending a splitting from one finite cover. It also does not prove the indefinite case: indefinite lattices have no positive spectral bound on coefficient support and their norm-one vectors do not form a finite signed orthonormal basis.

## 5. Exact one-negative-direction stabilization of L

The following small certificate is independent of any general cancellation theorem. Let J=L⊕[−1] and

P =

    [ 0  0       1        −1       −1       ]
    [ 0  0       0         1       −1       ]
    [ 1  1    −1−x⁻¹       1     x+1+x⁻¹   ]
    [ 0  1      −x⁻¹       0     x+1+x⁻¹   ]
    [ 1  2    x−1−x⁻¹      1        1       ].

Direct Laurent polynomial multiplication gives det P=−1 and

    P*JP = [1] ⊕ [[0,1],[1,0]] ⊕ I₂.

Thus J is extended even though L is not. The supplied checker verifies every coefficient, not numerical evaluations. Here is a derivation rather than an unexplained matrix search.

Let f be the new negative unit vector, and continue using e₁,…,e₄ for L. Set u=e₃+f and A=e₃+e₄+2f. Then u has norm one, A has norm zero, and they are orthogonal. Let w=e₁−(1+a)u−a e₄. Direct calculation gives h(A,w)=1 and h(w,w)=−a. Therefore B=w+xA has norm zero and h(A,B)=1. For any vector z, the expression

    z⊥ = z − u h(u,z) − A h(B,z) − B h(A,z)

is orthogonal to u,A,B. Put C=(e₂)⊥ and E=(e₃)⊥. Their Gram matrix is [[2a²+2a+1,2a+1],[2a+1,2]]. Then C−aE and E−(C−aE) are orthonormal. The ordered five vectors u,A,B,C−aE,E−C+aE give precisely P above, and its unit determinant proves they form a basis.

Consequences are deliberately limited. Stabilizing the topological L-manifold with a negative projective-plane summand cannot supply a non-extended smooth counterexample: its form has already become extended. This does not say that every indefinite form extends or that every such stabilized topological manifold is smoothable.

## 6. Exact unresolved gap and prior-claim hold

After the definite argument and [HT97, Theorem 2], the uncovered ordinary signatures have min(b₂⁺,b₂⁻)=1 or 2. We have neither a general integral cancellation/descent theorem in these cases nor a smooth closed realization carrying a verified non-extended form.

Passing to a degree-n cover increases the minimum index to n·min(b₂⁺,b₂⁻); thus high enough covers enter the proven high-indefiniteness range. Descending the resulting topological splitting or Λₙ-basis is the missing step, not a formal consequence of multiplicativity. In particular, after restriction to the subgroup nZ the relevant group-ring variable is xⁿ; this is not the same operation as quotienting Λ by xⁿ−1 to get an ordinary finite-cover lattice.

Kawauchi's 2013 Theorem 1.1 states this descent theorem, and his 2014 Corollary 1.2 states the full smooth result. These are genuine published prior claims, with matching intended topological meaning. They are not verified in this package. The 2013 proof reduces to Lemma 2.2 (double-cover descent), via Lemmas 2.3–2.4 and the exact-leaf machinery from earlier papers. In particular, Sublemma 2.3.1 asserts vanishing of the intersection form on a neighborhood of two intersecting 3-sphere leaves. Its last intersection-vanishing argument and the cited exact-leaf equivalence have not been reconstructed here. No counterexample to that sublemma is asserted.

K3 (2026) still poses the question. A 2024 census preprint quoted the full splitting assertion; the May 2026 arXiv v2 and February 2026 journal version omit that passage and the Kawauchi references. None of these bibliographic facts alone proves or disproves Kawauchi's result. The responsible outcome is **unsolved in this attempt, with an unverified prior full-resolution claim**, rather than “already solved,” “disproved,” or a new solution.

## 7. Reproducibility limits

`controls.py` uses only Python's standard library and exact integers/Fractions. It checks the 5×5 polynomial isometry and determinant, the block Schur identity, and finite-cover determinants, positive LDL pivots, characteristic parity and norms for n=1,…,12. Generated extended controls check Gram reconstruction and deck action for prime cover degrees 3,5,7,11.

These tests do not decide arbitrary Laurent equivalence, prove the large-prime hypothesis from finitely many covers, validate the geometric descent claim, construct a smooth counterexample, or establish novelty. Proposition 4.1 is an analytic/combinatorial proof, not an inference from the finite tests.

## References

- [K3] R. İ. Baykur, R. C. Kirby, D. Ruberman (eds.), *K3: A New Problem List in Low-Dimensional Topology*, AMS, 2026, Problem 4.51, printed pp. 230–231. [Author preliminary version](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf).
- [HT97] I. Hambleton, P. Teichner, *A non-extended Hermitian form over Z[Z]*, Manuscripta Math. 93 (1997), 435–442. [DOI](https://doi.org/10.1007/BF02677483), [author manuscript](https://math.berkeley.edu/~teichner/Papers/form.pdf).
- [FHMT07] S. Friedl, I. Hambleton, P. Melvin, P. Teichner, *Non-smoothable Four-manifolds with Infinite Cyclic Fundamental Group*, IMRN 2007, rnm031. [DOI](https://doi.org/10.1093/imrn/rnm031), [author copy](https://math.berkeley.edu/~teichner/Papers/Nonsmooth.pdf).
- [FQ90] M. Freedman, F. Quinn, *Topology of 4-manifolds*, Princeton University Press, 1990. Standard classification/free-module results are used through the precise applications explained in [HT97] and [FHMT07]; no complete reproof of that book is claimed.
- [Don83] S. Donaldson, *An application of gauge theory to four-dimensional topology*, J. Differential Geom. 18 (1983), 279–315. [DOI](https://doi.org/10.4310/jdg/1214437665).
- [Kaw13] A. Kawauchi, *Splitting a 4-manifold with infinite cyclic fundamental group, revised*, JKTR 22 (2013), 1350081. [DOI](https://doi.org/10.1142/S0218216513500818).
- [Kaw14] A. Kawauchi, *Splitting a 4-manifold with infinite cyclic fundamental group, revised in a definite case*, JKTR 23 (2014), 1450029. [DOI](https://doi.org/10.1142/S0218216514500291).
- [Kaw18] A. Kawauchi, *Splitting criteria for a definite 4-manifold with infinite cyclic fundamental group*, [arXiv:1804.01380v1](https://arxiv.org/abs/1804.01380v1).
- R. Burke, B. Burton, J. Spreer, census paper: [2024 v1](https://arxiv.org/abs/2412.04768v1), [2026 v2](https://arxiv.org/abs/2412.04768v2), [journal version](https://doi.org/10.1007/s00454-026-00818-w).
