# Boundary fixed points in rank-zero Hénon components

Problem 5300080 / AMR-052-0080, rank 793. Research date: 2026-10-05.

## Disposition and exact target

**Unsolved by this investigation; five substantive routes examined.** There is no claimed counterexample, full proof, new theorem of historical significance, or priority claim. The stronger full-convergence question has a credited prior answer. It must not be substituted for the historical subsequence question.

The governing source is Milnor's contribution, section 4, printed page 10 of Bielefeld's *Conformal Dynamics Problem List*, IMS 1990/1. It concerns a polynomial automorphism of **complex** two-space. Let U be a connected component of the interior of the forward-bounded set K⁺. After replacing the map by the return iterate of a periodic component, f(U)=U. A subsequence f^{n_j}|U converges locally uniformly to a holomorphic map g. The target is the case g≡p with p in the finite boundary ∂U: must Df(p) have eigenvalue 1?

The quantifier is **one subsequence**, not all iterates, and not all limit maps. The parameter 1 belongs to the derivative of the already chosen return map. A neutral multiplier for the original map may become 1 under a return iterate; this does not justify taking another iterate of an invariant component and calling that a proof for its original map. Real attracting-region arguments and limits on the projective line at infinity do not answer this target.

For the Hénon-type case below, use the standard bounded-orbit normal-family properties: iterates on U have holomorphic subsequential limits in C², and the fixed-point set is finite. These are classical inputs, also used in [LP, sections 2 and 8]. They are not asserted for arbitrary holomorphic self-maps or arbitrary nonpolynomial automorphisms.

## 1. What a single rank-zero limit actually proves

**Proposition 1.** Under the target assumptions, p is fixed, 0<|δ|<1 for δ=det Df, and its two multipliers can be labelled so that

0<|λ_s|<1 and |λ_c|≥1.

Proof. For z in U, the identity f^{n_j}(f(z))=f(f^{n_j}(z)) has limits p and f(p), respectively, because f(z) is also in U. Thus f(p)=p. Cauchy estimates for locally uniform holomorphic convergence give Df^{n_j}(z)→0. Its determinant is δ^{n_j}; consequently |δ|<1. Invertibility implies δ≠0, and hence both multipliers are nonzero. At least one has modulus below one.

Both cannot have modulus below one. In that case p is an attracting fixed point: in a suitable norm a sufficiently small neighborhood V has all forward iterates bounded and converging to p. Hence p lies in the interior of K⁺. But no point of the boundary of a connected component of an open set can lie in that open set. For completeness, a small connected ball in the open set around such a boundary point would intersect U and would therefore belong to the same component, contradicting its being a boundary point. This proves the assertion. ∎

This proves neither |λ_c|=1 nor λ_c=1. In particular, excluding a saddle by placing **every** orbit in its stable manifold is invalid when only a subsequence converges.

**Elementary-type reduction.** Suppose f is polynomially conjugate to a triangular automorphism T(z,w)=(az+P(w),bw+c), a,b≠0. A rank-zero subsequential limit on an open set forces a^{n_j}→0 and b^{n_j}→0 from the diagonal entries of DT^{n_j}. Thus |a|,|b|<1. Write w*=c/(1-b) and z*=P(w*)/(1-a). Then w_n→w*, and

z_n-z*=a^n(z_0-z*)+Σ_{k=0}^{n-1}a^{n-1-k}(P(w_k)-P(w*)).

The sum tends to zero: split off finitely many k, whose weights tend to zero, and bound the remaining terms by a uniformly small error times 1/(1-|a|). Every orbit is bounded, so K⁺=C² and there is no finite component boundary. For an affine automorphism, A^{n_j}→0 implies every eigenvalue of A has modulus below one, giving the same conclusion. Polynomial conjugacy preserves bounded sets, the constant-limit property and boundaries. Together with the classical classification of plane polynomial automorphisms, this explains why the substantive unresolved case is Hénon type.

## 2. Two sufficient conditions for full convergence

**Proposition 2 (bounded gaps).** If n_{j+1}-n_j≤M eventually for a fixed integer M, then f^n|U→p locally uniformly.

Proof. Every sufficiently large n can be written n=n_j+r, 0≤r<M. For a compact K⊂U, f^{n_j}(K)→p uniformly. Each of the finitely many continuous maps f^r sends p to p. Uniform continuity on a small compact neighborhood of p now gives f^r(f^{n_j}(K))→p uniformly in those finitely many r. ∎

**Proposition 3 (all limits rank zero).** Suppose the iterates on U are relatively compact in the compact-open topology, f has finitely many fixed points, each orbit in U is bounded, and **every** subsequential limit map has rank zero. Then f^n|U→p locally uniformly.

Proof. Connectedness of U makes each rank-zero limit constant; the commuting argument in Proposition 1 makes its value fixed. Fix z∈U. Every cluster point of x_n=f^n(z) therefore belongs to the finite fixed-point set S. Also |x_{n+1}-x_n|→0. Otherwise a subsequence with jumps bounded below has, by boundedness, a further subsequence x_{n_j}→q∈S, whereas x_{n_j+1}=f(x_{n_j})→f(q)=q, a contradiction.

A bounded sequence with vanishing successive jumps and finitely many possible cluster points has exactly one cluster point. To see this, put disjoint balls about the finitely many candidate points, separated by a positive distance. Eventually all terms lie in their union (otherwise a bounded subsequence outside has another cluster point), and eventually no successive jump can pass between two balls. The tail lies in one ball; refining the balls shows that just one candidate occurs. The given subsequence identifies it as p.

Finally, if convergence of maps were not locally uniform, relative compactness would give a further limit map violating that convergence on some compact set. Every such map is constant and its value at z is p. This contradiction proves the proposition. ∎

The elementary finite-cluster argument is a detailed rendition of a classical observation explicitly used in [LP, section 8], where Jupiter and Lilov are credited. It is not a new classification theorem. The assertion that one limit has rank zero does not imply the premise that every limit has rank zero.

## 3. Why full convergence is a solved, stronger problem

[LP, Theorem 5 in the inspected December 2012 preprint] proves: for a nonrecurrent invariant Hénon Fatou component, if the full sequence converges to a finite boundary point, the multipliers are 1 and a number of modulus below one. The theorem does not require the small-Jacobian bound used in its main classification theorem. The generalized snail lemma [LP, Theorem 27] supplies equality to 1, including exclusion of irrational neutral multipliers and nontrivial roots of unity.

Propositions 2 and 3 consequently yield the requested conclusion under their extra hypotheses. In this full-convergence setting nonrecurrence is immediate, since each orbit has the single limit p outside U. Applying the theorem does not require assuming that extra hypothesis in the original question.

For perspective, with full convergence a hyperbolic saddle is impossible independently of the snail lemma. Every point converging to a saddle eventually lies in its local stable manifold. The global stable set is a countable union of backward images of a one-complex-dimensional local manifold. These have four-dimensional Lebesgue measure zero and cannot contain an open subset of C². This argument needs full forward convergence; arbitrarily close returns do not put an orbit in the stable set.

A locally holomorphically linearizable fixed point with multipliers |λ|=1>|μ| has a forward-invariant small polydisk in linearizing coordinates, and hence belongs to int K⁺. Thus it cannot be p in the target, even with only subsequential convergence. This excludes that linearizable case without excluding all irrational semi-neutral germs.

The hedgehog results [LRT, Theorem C and Corollary C.1] exclude convergence to a semi-Cremer point away from its strong stable manifold. Their local nonaccumulation assertion assumes the entire forward orbit remains in the specified neighborhood. A sequence returning near p and leaving that neighborhood infinitely often does not meet that premise. No such containment is established here.

## 4. The small-Jacobian route and its exact obstruction

[LP, Theorem 1] gives the target conclusion under 0<|δ|<d⁻², with d the degree in the Hénon normal form used there. Its classification leaves only the semi-parabolic basin in the presence of a boundary constant limit. An attracting basin has an interior constant limit. In a rotation basin the retraction onto its rotation surface has rank one, and composing it with subsequential rotation limits preserves that rank.

Here is the analytic threshold in that proof, stated separately so that its limitations can be checked.

**Proposition 4 (stable-curve obstruction).** Let f be a Hénon map of degree d≥2, with a fixed point p and a contracting one-dimensional invariant manifold W^s(p). Assume there is an entire injective parametrization ψ:C→W^s(p) with ψ(0)=p and f(ψ(ζ))=ψ(λζ), 0<|λ|<d⁻². Assume a nonconstant limit map h on U factors as h=ψ∘η for a holomorphic η:U→C, has image in W^s(p)∩K⁻, and satisfies f(h(U))=h(U). Then these assumptions contradict the classical subharmonic Wiman theorem.

Proof. The backward Green function G⁻ is continuous, nonnegative and plurisubharmonic, vanishes precisely on K⁻, and satisfies G⁻∘f⁻¹=dG⁻. Hence u=G⁻∘ψ is nonnegative subharmonic on C and

u(λ⁻¹ζ)=d u(ζ).

It is not identically zero: otherwise W^s(p)⊂K⁺∩K⁻, which is compact for a Hénon map, and the entire coordinate functions of ψ would be bounded and therefore constant. Set ρ=log(d)/log(1/|λ|). The scaling equation and a bound for u on the closed unit disk give u(ζ)≤C|ζ|^ρ for |ζ|≥1, by scaling ζ into that disk. Here ρ<1/2.

The connected set Λ=η(U)=ψ⁻¹(h(U)) contains a nonzero point and is invariant under multiplication by λ⁻¹. It is therefore unbounded. It lies in {u=0}, contradicting Wiman's theorem that the zero-set components of a nonconstant nonnegative subharmonic function with growth bounded by r^ρ, ρ<1/2, are bounded. ∎

All the geometric inputs in this proposition, and their use for mixed limit ranks, are credited to [LP, Lemmas 31–33]. Proposition 4 isolates their analytic mechanism, rather than replacing those theorems with a new proof of global dynamics. Under the target's proven inequalities, the stable multiplier satisfies |λ_s|=|δ|/|λ_c|≤|δ|, so moderate dissipation supplies the required spectral bound.

**Threshold control.** The strict inequality in that analytic mechanism is essential. Define on C

v(z)=sqrt((|z|+Re z)/2)=|Re sqrt(z)|.

The latter expression is independent of the choice of square root. Away from 0 it is locally the absolute value of a harmonic function and so is subharmonic. It extends continuously at 0; the removable-singularity theorem for locally bounded-above subharmonic functions gives subharmonicity there too. It is nonnegative, nonconstant, homogeneous of degree 1/2 under positive real scaling, and its zero set is the unbounded negative real axis. For every integer d≥2,

v(d²z)=d v(z).

Thus at λ=d⁻² the scaling law and an unbounded zero continuum coexist. This is a counterexample to extending the **abstract analytic inference** to the threshold; it is not a Hénon map, Green-function realization, or counterexample to Milnor's question.

## 5. Exact remaining gap

The historical hypothesis permits mixed rank-zero and rank-one subsequential limits and unbounded gaps between visits near p. The inspected [LP, Lemma 31] specifically treats a nonunique limit set by obtaining a rank-one limit in the strong stable manifold of a fixed point. The small-Jacobian argument rules out that configuration; nothing here rules it out at an arbitrary dissipative Jacobian. Without controlling those excursions, neither the saddle stable-manifold argument, the snail lemma, nor the hedgehog nonaccumulation theorem applies as a full resolution.

In particular, this packet does not prove even that every possible boundary rank-zero value has a unit-modulus multiplier, let alone that this multiplier is a root of unity or exactly 1. Determinant contraction alone does not imply these statements. The exact Gaussian-rational matrix controls include a neutral multiplier (3+4i)/5: it is not a root of unity, since its sum with its inverse is 6/5, whereas a rational algebraic integer must be an integer. No Fatou component realizing the forbidden situation is claimed.

Recent wandering-domain examples do not repair this gap: [BB] constructs wandering components, whereas the question already assumes an invariant component after taking its return map. The escaping rank-one examples [BBS] are transcendental and have limits at infinity. The bounded search found no general resolution of the exact subsequence target. It is not a proof of current worldwide open status.

## References and inspection scope

- [M] B. Bielefeld (editor), *Conformal Dynamics Problem List*, IMS 1990/1, section 4 (Milnor), p. 10. https://www.math.stonybrook.edu/preprints/ims90-1.pdf . Page 10 visually inspected; this is the governing statement.
- [LP] M. Lyubich and H. Peters, *Classification of invariant Fatou components for dissipative Hénon maps*, GAFA 24 (2014), 887–915, DOI https://doi.org/10.1007/s00039-014-0280-9 . Full text inspected at https://www.math.stonybrook.edu/preprints/ims12-07.pdf ; theorem numbering above is from that December 2012 preprint. Sections 1–3, 7–8 and selected proofs inspected. The journal's full PDF was not successfully obtained; its bibliographic record was verified. Imported global analytic foundations were not independently reproved.
- [LRT] M. Lyubich, R. Radu and R. Tănase, *Hedgehogs in higher dimensions and their applications*, Astérisque 416 (2020), 213–251. https://arxiv.org/abs/1611.09840 . Theorem C, Corollary C.1, Theorem D and Theorem E, with relevant proof passages, inspected in the downloaded preprint.
- [BBS] V. Beltrami, A. M. Benini and A. Saracco, *Escaping Fatou components with disjoint hyperbolic limit sets*, Math. Z. 307 (2024), article 37. https://doi.org/10.1007/s00209-024-03501-z . Introductory scope and theorem inspected in the publisher text and https://arxiv.org/abs/2308.05529 . Its introductory discussion distinguishes the remaining rank-one issue for polynomial maps; that discussion alone is not a theorem deciding this target.
- [BB] P. Berger and S. Biebler, *Emergence of wandering stable components*, https://arxiv.org/abs/2001.08649v2 , published JAMS (2023). Abstract and introductory scope checked; the long construction is not audited here.

All mathematics is AI-assisted and unrefereed. Finite regression checks verify calculations and guard scope; they do not prove the infinite-dimensional analytic assertions or certify imported theorems.
