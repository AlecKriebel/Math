# Birational sequences for plabic Newton–Okounkov bodies: five partial approaches

## Disposition and target

Problem 30003070, OWR-14221-006. **Unsolved in this investigation after five approaches.** No proof, counterexample, verified full prior resolution, novelty, or global current-openness claim is made. The strongest original material here consists of elementary, fully proved comparison lemmas, a complete small semigroup calculation, and an exact obstruction test that fails to distinguish a known nonintegral plabic body from root-sequence bodies.

The target is the final question in Xin Fang's contribution, *Polytopes arising from mirror plabic graphs*, OWR 13/2016, printed pp. 626–628, especially p. 627 [O]. Its context is every reduced plabic graph for the **top cell** of a complex Grassmannian, and the line bundles O(r), r positive. The question asks whether the associated Newton–Okounkov bodies arise from birational root sequences with suitable total orders. It is not restricted to Gr(2,n), iterated sequences, rectangles graphs, degree-one convex hulls, or integral bodies. The preceding mirror-graph theorem and complement-cluster conjecture are separate assertions.

We use X=Gr(k,n), d=k(n-k), L=O(1), with 1≤k<n. The endpoint Grassmannians are points and have trivial zero-dimensional bodies. Replacing k by n-k translates the source convention. For a chart valuation v and a nonzero section s0 of L, put

    Γv = {(r, v(s/s0^r)): r≥0, 0≠s∈H⁰(X,L^r)},
    Δv = closure(conv{a/r: (r,a)∈Γv, r>0}).

Changing s0 translates Δv by an integral vector. For positive r, Δv(O(r))=rΔv(O(1)): one inclusion follows by restricting to section degrees divisible by r, and the reverse follows by raising every section to its r-th power. This cofinal-power argument retains all degrees. The homogeneous degree must not be discarded when comparing semigroups. We aim for affine unimodular equivalence, UΔ+b with U∈GLd(Z), b∈Zd; equality in chosen coordinates is stronger. An isomorphism of unpolarized toric special fibers is weaker and does not alone prove this equivalence. In particular [0,1] and [0,2] produce the same abstract projective toric curve but have different lattice lengths.

A root sequence is a length-d ordered list of positive type-A roots, repetitions allowed, whose product of corresponding negative-root subgroups, followed by projection to X, is birational onto the big cell [B, Definition 10]. Birationality is not merely dominance or a nonsingular Jacobian at one point. Lowest-term valuations use a translation-invariant total order on the exponent group whose restriction is an allowed monomial order; weighted opposite-lex orders require the positive-weight hypotheses in [F, §6]. Fixing one such order does not quantify over all orders.

## Approach 1. Inductive root charts and the tree classification

**Mechanism.** Start with a root chart and attach k parameters when increasing n. Compare the resulting iterated sequences to plabic degenerations through tropical Grassmannians.

### Lemma 1.1 (PBW big-cell chart, all k,n)
Let 1≤i≤k<j≤n. For any ordering of the d roots εi−εj, the product of I+tji Eji, acting on span(e1,…,ek), parametrizes the big cell isomorphically.

**Proof.** Every product Eji Eℓh is zero: i≤k and ℓ>k. Thus the product is I+Σtji Eji regardless of order. The image plane has matrix [Ik;T]. Its lower block T is uniquely recovered from the plane on the open set p[1,k]≠0. This gives polynomial mutually inverse maps with affine d-space. ∎

### Lemma 1.2 (row-extension construction)
Suppose a chart of Gr(k,n) is given birationally by a sequence S, and choose k distinct rows i1,…,ik of an n×k representative A. On the open set where the corresponding k×k submatrix is invertible, append a new bottom row Σh yh Aih. This produces a birational chart of Gr(k,n+1), implemented by left multiplication by the k commuting elementary matrices I+yh E(n+1,ih).

**Proof.** On the open chart, recover the old n-plane representative and its S-coordinates by the old birational inverse. If z is the desired new row, solve y·A[I,:]=z. The inverse is rational by the adjugate formula, and the determinant is not identically zero on the old big cell. Conversely these y produce exactly z. The left multipliers modify only the new row, so they implement the construction. ∎

This supplies actual inverses, not just dimension counts. Repeating it from Gr(k,k+1) gives iterated sequences. The construction is the elementary mechanism behind [B, Lemma 2].

**Verified prior coverage.** [B, Theorem 2 and Remark 1], together with [P, Theorem 4.6 and Remarks 4.8–4.9], recover the Gr(2,n) plabic toric degenerations through iterated sequences. The comparison uses graded initial ideals and degree-one Khovanskii bases, not merely abstract toric-variety isomorphisms. [B, Corollary 2] records the unimodular comparison on the sequence side. The lattice argument in Lemma 3.2 below explains the required polarized step.

**Test beyond k=2.** The 2025 preprint [T, Theorems 5 and 7, concluding discussion] reports only four Gr(3,6) types from its iterated sequences and fixed order; its family misses plabic types including EEEG and GG. This is a restricted-family result, not a counterexample to all root sequences and orders. Its computational classification was inspected as a stated result, not independently rerun.

**Exact gap.** No construction here turns every reduced top-cell graph in arbitrary Gr(k,n) into such a row-extension sequence or into any other root sequence. Extrapolating the tree classification to k≥3 is unsupported. Closure under an arbitrary plabic move is also not proved.

## Approach 2. Transport the whole valuation through a chart factorization

**Mechanism.** Factor a network chart into root subgroup parameters and show that this transports valuations on all sections.

### Lemma 2.1 (monomial chart transport)
Let two birational coordinate systems x and t on the same function field satisfy xj=cj t^mj, cj≠0, with the exponent columns mj forming M∈GLd(Z). Suppose the chosen exponent orders obey a<xb if and only if Ma<tMb, and their restrictions are allowed monomial orders. Then

    vt(f)=M vx(f)

for every nonzero rational function f. With the same reference section the corresponding Newton–Okounkov bodies are related by M; with different reference sections they differ by an additional integral translation.

**Proof.** Distinct Laurent monomials x^a map to distinct Laurent monomials t^(Ma), since M is injective. Their nonzero coefficients only acquire nonzero scalar factors, so substitution cannot cancel different terms. Order compatibility identifies the least exponent with M times the old least exponent. Quotients are handled by subtracting numerator and denominator values. Apply this equality to every H⁰(X,L^r), divide values by r, and take closed convex hulls. The reference-section difference contributes r times its fixed integral value before division. ∎

The compatibility assumption is substantive: transporting an arbitrary ordered group structure through M need not yield a permitted well-order on the new nonnegative orthant.

### Exact failure of the weaker “both charts are birational” premise
Take y1=x1 and y2=x1(1+x2). This is birational, with x1=y1 and x2=y2/y1−1. In lowest lexicographic x-order,

    vx(y1)=vx(y2)=(1,0),  vx(y2−y1)=(1,1).

A monomial lowest-term valuation in independent y coordinates has values e1,e2. No invertible linear map sends both to (1,0). The cancellation in y2−y1 also shows why values on displayed generators do not determine the valuation on their span.

**Exact gap.** A general network chart has no demonstrated monomial, order-compatible root factorization. A rational change of coordinates, a positive parametrization, or a generic flag does not supply Lemma 2.1. Arbitrarily moving a flag changes the valuation; no identification with the fixed plabic valuation follows.

## Approach 3. Degree-one Khovanskii bases and matching graded toric ideals

**Mechanism.** Prove that all degrees are controlled by Plücker values, then compare the resulting semigroups.

### Lemma 3.1 (what degree-one semigroup generation actually gives)
If Γv is generated by finitely many (1,a1),…,(1,am), then Δv=conv(a1,…,am), an integral polytope.

**Proof.** Every (r,a) is Σj nj(1,aj) with nj≥0 and Σj nj=r. Hence a/r is a convex combination of the aj. Conversely each aj occurs at degree one. Taking the closed convex hull gives equality. ∎

This is stronger than generation of the *algebra* by degree-one sections. Sums of monomials may cancel their least terms. The implication “integral polytope ⇒ degree-one semigroup generation” is not used. Saturation, normality, equality of integer value sets, and a Minkowski-sum property are distinct assertions.

### Lemma 3.2 (graded lattice certificate)
Let Ahat,Bhat be (d+1)×m integral matrices with first row all ones. Assume their columns generate Z^(d+1) as groups and kerZ(Ahat)=kerZ(Bhat). Then a unique lattice automorphism T maps each column of Ahat to the corresponding column of Bhat. It has block form T(r,a)=(r,Ua+rb), where U∈GLd(Z), b∈Zd. Consequently their degree-one convex hulls are affine unimodularly equivalent.

**Proof.** Map Ahat z to Bhat z. Equality of kernels makes this well-defined; generation makes it a map on the whole lattice. Reversing A and B yields its inverse. On every generating column the first coordinate is preserved, so it is preserved everywhere. Thus T has the stated block form; det(T)=det(U)=±1. Restrict to r=1. ∎

A common homogeneous toric binomial ideal identifies the kernel lattice (up to any explicitly checked generator permutation). This can be used only after verifying degree-one semigroup generation and the actual value lattices. Full rational rank alone is insufficient to identify an ambient lattice.

### Proposition 3.3 (complete Gr(2,4) root-chart semigroup calculation)
Use the PBW chart [I2; (a b; c d)] and lowest lexicographic order a,b,c,d. After harmless signs, its degree-one Plücker polynomials are

    q=(1,b,d,a,c,bc−ad).

The graded value semigroup is generated by

    (1,0), (1,eb), (1,ed), (1,ea), (1,ec), (1,eb+ec).

Thus its complete O(1) body is conv(0,eb,ed,ea,ec,eb+ec).

**Proof.** Introduce formal degree-one variables z0,…,z5 and a homogenizing parameter h, so zi maps to h qi. The equation is

    z0 z5 − z1 z4 + z2 z3=0.

Every monomial can be reduced using z0z5=z1z4−z2z3 to a linear combination of monomials not divisible by z0z5; the exponent of z0 plus that of z5 decreases by two at each replacement. Their leading exponent map is (degree,a,b,c,d). Its integer kernel is generated by

    (1,−1,0,0,−1,1).

Indeed equality of a,d coordinates fixes exponents of z3,z2; equality of b,c and degree then gives exactly that relation. Two distinct normal monomials cannot have equal values: one side of a nonzero multiple of this relation would have positive exponents of both z0 and z5. Therefore normal monomials have distinct leading terms, are linearly independent after substitution, and span. A nonzero linear combination has the least value of one normal monomial, with no cancellation. All values are consequently sums of the six generator values. ∎

The exact replay counts these normal monomials and distinct values for 0≤r≤12 and checks the formula C(r+5,5)−C(r+3,5). This finite check is supplemental; the argument proves every r.

**Exact obstruction and gap.** [R, §9] supplies a nonintegral Gr(3,6) plabic body. Lemma 3.1 rules out any realization with a degree-one-generated value semigroup. It does not rule out birational sequences whose value semigroups require higher-degree generators. Thus the successful small SAGBI calculation and Gr(2,n) literature cannot simply be propagated to every graph.

## Approach 4. Lift mutations through rank-two root factorizations

**Mechanism.** Begin with a graph known to be realizable and transport the construction along graph moves.

### Lemma 4.1 (exact braid chart relation)
In SL3 put xi(t)=I+t E(i+1,i). On a+c≠0,

    x1(a)x2(b)x1(c)
      =x2(bc/(a+c)) x1(a+c) x2(ab/(a+c)).

**Proof.** The left matrix has entries (2,1)=a+c, (3,1)=bc, (3,2)=b, diagonal entries one, and all other off-diagonal entries zero. On the right these entries are respectively B, AB, A+C, with A=bc/(a+c), B=a+c, C=ab/(a+c). They coincide. The inverse uses the same form with the simple-root labels exchanged. ∎

For positive leading coefficients, so that a+c has no leading cancellation, its tropical map is

    τ(α,β,γ)=(β+γ−m,m,α+β−m),  m=min(α,γ).

On α≤γ and γ≤α it is represented respectively by the determinant-one matrices

    [−1 1 1; 1 0 0; 0 1 0],   [0 1 0; 0 0 1; 1 1 −1].

It is not globally linear. For p=(1,1,2), q=(2,1,1), one has τ(p)+τ(q)=(3,2,3), whereas τ(p+q)=(2,3,2). The two formulas agree on their common wall, but their union is not a single lattice automorphism.

**Exact gap.** The identity is a local rank-two root-factorization result. It does not show that every square move of every top-cell plabic graph lifts to an allowed root sequence and one globally compatible order. A tropical/cluster mutation gives a piecewise-linear transformation; it cannot be replaced silently by a single GLd(Z) change. Positivity for coordinate mutation also does not remove cancellations in arbitrary linear combinations of sections.

## Approach 5. A universal multilinearity obstruction, then an exact failed test

**Mechanism.** Seek a necessary property of every root-sequence body and try it on a nonintegral plabic body.

### Theorem 5.1 (cube bound without a Khovanskii assumption)
For any birational length-d sequence of type-A root subgroups on Gr(k,n), its O(1) lowest-term Newton–Okounkov body, with the highest Plücker reference section, lies in [0,1]^d. The assertion holds for every permitted total monomial order, and permits repeated roots. With a different reference section the body is integrally translated. It does not assert that the body is integral or generated in degree one.

**Proof.** A root operator Eji acts on a basis vector eI of ∧k Cn by zero unless i∈I and j∉I; otherwise it replaces i by j, up to sign. Applying that operator twice is zero. Hence on the exterior representation each factor exp(ts Eji) acts as 1+ts Dji. The product applied to the highest wedge therefore has each parameter's degree at most one. Every Plücker coordinate is a coefficient of this product and is multiaffine in the d distinct parameter positions, even when roots repeat. The highest coordinate is identically one on the negative-unipotent chart.

The Plücker section ring is generated in degree one: equivalently the Cartan multiplication Sym^r H⁰(L)→H⁰(L^r) is surjective. One can see surjectivity from the nonzero equivariant multiplication map onto the irreducible highest-weight summand of weight rωk (or projective normality of the Plücker embedding). Thus every section of L^r is a linear combination of products of r Plücker coordinates. Each product, and hence the entire sum, has every parameter's degree at most r. Cancellation deletes monomials; it cannot create an exponent outside [0,r]^d. Its least nonzero exponent consequently lies in that box. Divide by r and take closed convex hulls. A new denominator contributes −r times its valuation and gives the claimed translation. ∎

The representation argument also proves the weight constraint: a monomial t^a in the Plücker coordinate pI has Σs as βs=ωk−weight(eI). Applying root height gives Σs as ht(βs)=Σi∈I i−k(k+1)/2. Hence height weights tie on each fixed Plücker polynomial; they do not by themselves distinguish its terms. This does not identify valuations of sums of different weights.

### Proposition 5.2 (the nonintegral test body still fits a unit cube)
Here is a reproducible calculation using [R, Theorem 15.1 and §9]. Its inputs are mathematical coordinates, not a downloaded polytope dataset. Order the nine Young diagrams as

    μ=((3,3,3),(3,3,2),(2,2,2),(1,1,1),(3,3,0),
       (2,1,0),(1,1,0),(3,0,0),(2,0,0)).

For each of the 20 partitions λ inside a 3×3 square, form vλ whose μ-coordinate is the maximum number of boxes in μ\λ with equal row-minus-column index. The known additional vertex is

    c=(3/2,3/2,1,1/2,1,1/2,1/2,1/2,1/2).

The source identifies its example with P=conv({vλ}∪{c}). The following independently calculated matrix has determinant one and maps P into [0,1]^9:

    U = [ 0  1  0  0 −1 −1  0  0  1
          0  0  0  0  1  0  0 −1 −1
          0  1 −1  0  0 −1  1  0  0
          0  0  1  0  0 −1 −1  0  0
          0  0  0  0  0  1  0  0 −1
          0  0  1 −1  0  0 −1  0  0
          0  0  0  1  0  0 −1  0  0
          1 −1  0  0  0  0  0  0  0
          0  0  0  0  0 −1  1  0  1 ].

**Proof and exact certificate.** Calculate each of the 20 vectors directly by counting boxes on the finitely many diagonals. Matrix multiplication gives Uvλ∈{0,1}^9 for every λ, and

    Uc=(1/2,0,1/2,0,0,0,0,0,1/2).

Fraction-free/rational Gaussian elimination gives det(U)=1. Convexity proves the containment. All arithmetic is independently recomputed by the standard-library script in this packet. It also checks that the 20 vλ are distinct and span the ambient lattice by exhibiting a 9-column determinant −1. ∎

An exact separation certificate retains the degree-one obstruction:

    w=(0,−1,1,0,1,0,−1,0,−1),
    w·vλ∈{0,1} for every λ,  w·c=−1/2.

Thus c is outside conv{vλ}. This finite verification proves that specific assertion, not a universal realization theorem.

**Exact gap.** Cube containment is necessary, not sufficient, for a root chart and order. The known nonintegral example passes this test. The matrix U alone produces neither a sequence of roots nor an order nor equality of all value semigroups. No obstruction excluding all sequences for this example, and no construction realizing it, is established here.

## Stopping boundary

Five different mechanisms have been pursued: iterated chart induction; monomial chart transport; graded SAGBI/semigroup comparison; rank-two mutation lifting; and a universal representation-theoretic obstruction. Each has a proved retained result and a specific unsatisfied bridge to the all-graphs claim. Further finite cases or repetitions of those bridges would not resolve the target. A genuine next step would need either a root-factorization/order theorem valid for arbitrary reduced plabic graphs, or a proved invariant stronger than cube containment that excludes every admissible sequence and order for one verified graph.

## Primary references

[O] X. Fang, *Polytopes arising from mirror plabic graphs*, in *Mini-Workshop: PBW Structures in Representation Theory*, Oberwolfach Reports 13/2016, pp. 626–628. https://doi.org/10.4171/owr/2016/13 ; full report https://ems.press/content/serial-article-files/46617

[F] X. Fang, G. Fourier, P. Littelmann, *Essential bases and toric degenerations arising from birational sequences*, Advances in Mathematics 312 (2017), 107–149. Inspected arXiv:1510.02295v3. https://arxiv.org/abs/1510.02295

[P] L. Bossinger, X. Fang, G. Fourier, M. Hering, M. Lanini, *Toric degenerations of Gr(2,n) and Gr(3,6) via plabic graphs*, Annals of Combinatorics 22 (2018), 491–512. Inspected arXiv:1612.03838 version returned 2026-10-05. https://arxiv.org/abs/1612.03838

[B] L. Bossinger, *Birational sequences and the tropical Grassmannian*, Journal of Algebra 585 (2021), 784–803. Author-hosted published article inspected. https://doi.org/10.1016/j.jalgebra.2021.04.028 ; https://www.matem.unam.mx/~lara/birat_published.pdf

[R] K. Rietsch, L. Williams, *Newton-Okounkov bodies, cluster duality, and mirror symmetry for Grassmannians*, Duke Mathematical Journal 168 (2019), 3437–3527. Inspected arXiv:1712.00447v2. https://arxiv.org/abs/1712.00447

[T] J. Torres Henestroza, *Birational sequences for the Grassmannian Gr(3,n)*, arXiv:2511.03885v1 (2025). The inspected arXiv page lists a preprint, with no journal reference. https://arxiv.org/abs/2511.03885
