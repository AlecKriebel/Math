# Audit of the strong Heegaard Floer geography counterexample

## Decision and attribution

The counterexample in Theorem 1.3 of Alper Ferudun's *A Negative Answer to the Strong Geography Question of Alfieri and Binns*, dated September 30, 2026, passes this independent mathematical and computational audit. The theorem supplies a negative answer to the precise strong geography question: the total, ungraded F₂[U]-module HF⁻ of an integral homology sphere can have torsion length 16 without a direct summand F₂[U]/(U¹⁵).

Credit for the example Σ(30,47,83), its displayed decomposition, and the computer-assisted argument belongs to Ferudun. This audit independently checks that argument and its finite certificate; it makes no discovery or priority claim. The source explicitly describes itself as an unrefereed, AI-assisted computer-assisted note. Its Zenodo record labels version 1.0 as a preprint. This audit does not change that scholarly status. [Ferudun preprint](https://eulersolve.org/papers/owr-14298580-008/) · [DOI](https://doi.org/10.5281/zenodo.23063072).

The acceptance is scoped to the counterexample and the algebraic conclusion for both orientations. It does not certify the note's exhaustive search, minimal-product claims, further-example table, or priority survey. Those claims are unnecessary for the negative answer.

## The exact question

Let Y be a connected closed oriented smooth rational homology 3-sphere and let M = HF⁻(Y;F₂), summed over every Spinᶜ structure. Write M_red for its U-torsion and let ℓ be the least nonnegative integer with U^ℓ M_red = 0. The question asks whether M has a direct summand isomorphic to the direct sum of F₂[U]/(Uʲ) for every j from 1 through ℓ. The requirement is empty when ℓ = 0.

This is the definition and question in Alfieri's report, printed pages 1952–1953, and in Alfieri–Binns, Definition 1.6 and Question 1.10. Their Section 2 explicitly uses the sum over Spinᶜ structures and identifies the reduced plus module with the torsion of the minus module. Their results about knot surgeries and large link surgeries do not supply the answer for all rational homology spheres. [Oberwolfach report](https://doi.org/10.4171/OWR/2024/34) · [Alfieri–Binns, arXiv:2404.00490v1](https://arxiv.org/abs/2404.00490v1).

The audited example is an integral homology sphere, so it has exactly one Spinᶜ structure. There is consequently no mismatch between an individual Spinᶜ calculation and the requested total module.

## Plumbing and manifold hypotheses

Use the boundary orientation of the negative definite star plumbing with central weight −1, one arm consisting of 29 vertices of weight −2, and two one-vertex arms of weights −47 and −83. There are 32 vertices. The normalized Seifert data are

(e₀; (a₁,ω₁),(a₂,ω₂),(a₃,ω₃)) = (−1; (30,29),(47,1),(83,1)).

The multiplicities are pairwise coprime, their product A is 117030, and

−117030 + 29·3901 + 2490 + 1410 = −1.

Thus the rational Euler number is −1/117030. The negative continued fraction with 29 entries all equal to 2 is 30/29. These data identify the plumbing boundary with the indicated Seifert, equivalently Brieskorn, integral homology sphere under the source's orientation convention. The normalization and homology-sphere criterion were checked against the primary Seifert calculation, not inferred from the example's name. [Can–Karakurt, Sections 1–2](https://arxiv.org/abs/1211.4934v2).

An independent exact rational elimination of the actual 32×32 intersection matrix gives pivots

−2, −3/2, −4/3, …, −30/29, −47, −83, −1/117030,

when the long arm is eliminated from its outer endpoint, followed by the two short arms and the center. Every pivot is negative and their product is 1. This verifies negative definiteness and |H₁(Y;Z)| = 1. All noncentral vertices have weight at most minus their degree. The center is the sole bad vertex.

The plumbing is a connected tree of sphere bundles. Its boundary is a connected closed oriented smooth 3-manifold. Unimodularity gives an integral homology sphere, hence the rational homology sphere required by the question. These checks also avoid assuming the topology from numerical Floer output.

## Imported theorem chain and conventions

1. Ozsváth–Szabó's Theorem 1.2 identifies HF⁺(−Y(G);Z) with their plumbing module for a negative definite graph with at most one bad vertex. Theorem 2.1 works over F₂, as specified at the beginning of its subsection. The minus sign on the boundary orientation is essential and is retained here. [Published primary paper](https://msp.org/gt/2003/7-1/gt-v7-n1-p05-s.pdf).
2. The graph is almost rational: decreasing the center to a sufficiently negative weight gives a graph with every negative weight at least its degree, which is rational. Némethi's Example 8.2(3), Theorems 8.3 and 9.3, and Proposition 4.7 therefore apply. His Sections 11.11–11.14 give the canonical Seifert sequence and the grading shift. Since H₁ is zero, the canonical class represents the unique Spinᶜ structure. [Némethi, published primary paper](https://real.mtak.hu/141378/2/23424.pdf).
3. Némethi's Proposition 3.5.2 expresses the root module as one infinite tower and finite cyclic summands whose lengths are the leaf-to-merger height differences. His Section 2.2 defines the finite module with parameter n to have rank n. Thus a height difference of 16 means U¹⁶-torsion, without an off-by-one shift. The root height corresponds to half the Floer grading; this factor of two does not double the U-exponent.
4. The integral root decomposition is free abelian in every degree. The universal coefficient theorem consequently produces the same cyclic lengths over F₂, with no additional coefficient-torsion term. Alternatively, the F₂ version of the plumbing identification is directly available. There is no substitution of a different coefficient field.

For this graph, τ(0)=0 and the canonical difference formula becomes

Δ(i) = τ(i+1)−τ(i) = 1 + floor(i/30) − ceil(i/47) − ceil(i/83).

The formula follows because i−ceil(29i/30)=floor(i/30). Both the floor/ceiling convention and the normalized Seifert signs were checked visually in the primary formulas.

## Why the computation is finite

Set N = A−3901−2490−1410 = 109229. The ceiling identity, together with Nω_l ≡ 1 modulo a_l, gives Δ(i)+Δ(N−i)=0 for every integer i. For j<0, the elementary bound ceil(x)≥x gives Δ(j)≤1+j/A<1, so integrality implies Δ(j)≤0. Hence Δ(i)≥0 whenever i>N.

It follows that τ is nondecreasing from N+1=109230 onward. Extending the path by this tail adds no new sublevel components and no new finite cyclic summands. The finite interval is exactly the 109231 samples indexed from 0 through 109230. Pairing the differences also proves τ(109230−i)=τ(i). This is a proof of the tail bound, rather than an extrapolation from a finite numerical test.

The same cutoff and semigroup description occur in Can–Karakurt, Theorem 1.3. Its exceptional triple (2,3,5) is irrelevant here. The independent arithmetic additionally checked the affine-period relation Δ(i+A)=Δ(i)+1 and the symmetry on a range spanning several periods as error-detection controls.

## Independent recomputation

The audit used newly authored Python standard-library code. No downloaded executable code, library, or checker was run. All calculations use integers, exact rational fractions, or F₂ bit operations.

Three constructions agree at every sample:

- Direct summation of the canonical ceiling formula.
- Actual generalized Laufer additions on the 32-vertex plumbing lattice, starting at zero and increasing the central coefficient once per step, then adding noncentral vertices with positive intersection until stabilized. The run performed 1,696,707 vertex additions. Each noncentral addition occurred at intersection 1. At every step the resulting cycle was checked against the explicit arm-cycle recurrence, and its value of −(x·x+K(x))/2 was evaluated directly.
- Numerical-semigroup reachability with generators 1410, 2490 and 3901, using the positive semigroup indicator minus its reflection about N.

The 109230 differences through index N consist of 17619 values −1, 73992 zeros and 17619 values 1. The range of τ is [−12755,1]. Its minimum occurs precisely on the four intervals [54390,54420], [54480,54510], [54720,54750] and [54810,54840].

The source archive contains two identically hashed copies of the certificate. The selected certificate has 21829 bytes and SHA256 6d7130dbc0ecf948286ed5d2b7e51a2cdad322da0588a97f3c9ddf7a43f72943, matching the hash printed in Appendix A. All 1707 index/value pairs agree with an independently extracted complete turning-point sequence, using the first index of a plateau at an extremum. The printed PDF list agrees pair for pair with the archived file. Every interval between successive pairs was checked for weak monotonicity.

Four routes give the same cyclic lengths:

1. Union-find on all 109231 path samples.
2. Union-find on the 1707 turning-point values.
3. Direct sublevel-interval minima counts at each of the 12757 integer height levels, followed by N_(d−1)(b)−N_d(b). Agreement holds for the entire birth/death multiplicity data, not only for total dimension.
4. Direct construction of the reduced root-function module over F₂ and exact ranks of its U-powers, without persistence pairing.

For the fourth calculation, at height q the homogeneous piece is F₂^{C_q}, where C_q is the set of sublevel components. The infinite tower is the constant vector. Quotient by that vector, and let U pull coefficients back from components at height q to their descendants at height q−1. This gives a finite module of dimension 4864. Gaussian elimination gives the ranks of Uʲ for j=0,…,17:

4864, 4011, 3250, 2579, 1996, 1499, 1086, 755, 500, 311, 178, 91, 40, 13, 2, 1, 0, 0.

Their second differences recover the individual nilpotent block multiplicities. This checks directly that the root-module convention, the barcode convention, and the F₂ module all yield the same answer.

The multiplicities of F₂[U]/(Uʲ), in ascending order j=1,…,16, are

92, 90, 88, 86, 84, 82, 76, 66, 56, 46, 36, 24, 16, 10, 0, 1.

There are 853 finite summands and their dimensions sum to 4864. Némethi's independent total-rank identity, minimum τ plus the total downward variation, gives −12755+17619=4864. As an additional exact normalization check, K²+32=−102040 and the correction-term formula gives d(Y)=0.

## From plus to minus and both orientations

For a rational homology sphere in a fixed Spinᶜ structure, HF^∞ is F₂[U,U⁻¹]. The long exact sequence for CF⁻→CF^∞→CF⁺ identifies the quotient of HF⁺ by its infinite tower with the U-torsion in HF⁻. The latter is finitely generated, has one free F₂[U] summand in each Spinᶜ structure, and its torsion splits off over the PID F₂[U]. In this example there is one Spinᶜ structure, so the full minus module is one free summand plus the finite module just calculated. [Ozsváth–Szabó, properties and applications, Theorem 10.1](https://annals.math.princeton.edu/wp-content/uploads/annals-v159-n3-p04.pdf).

Orientation reversal exchanges the plus and minus chain complexes by graded duality. It is the degreewise direct-sum dual, not the unrestricted product dual of an infinite-dimensional vector space. Finite-dimensional graded pieces and field coefficients allow homology to commute with this dual. The graded dual of F₂[U] is the infinite plus tower, while the graded dual of F₂[U]/(Uʲ) is another length-j cyclic module, up to grading shift. Proposition 2.5 of the same primary paper supplies this orientation identification. Therefore the torsion lengths for Y and −Y agree. No claim that their absolute gradings are identical is needed.

## Direct summand obstruction

Let f_M(j)=dim_F₂(ker U ∩ UʲM). This quantity is additive on direct sums. A free F₂[U] summand contributes zero. A length-k cyclic summand contributes 1 for j<k and zero otherwise. Thus m_k=f_M(k−1)−f_M(k) counts length-k summands.

The audited decomposition gives f_M(14)=f_M(15)=1, so m₁₅=0. It also gives f_M(16)=0 and m₁₆=1. If a length-15 cyclic module were an abstract direct summand, its contribution would force m₁₅≥1, since the complementary module has nonnegative successive differences. This contradiction rules out every such direct summand, even after forgetting the grading or mixing it with the free summand.

The length-16 block establishes ℓ=16. The required full staircase would itself contain a length-15 direct summand. Therefore neither orientation satisfies the strong geography restriction. A length-15 submodule inside a length-16 block does not satisfy the question; the audit does not confuse these notions.

## Adverse controls and limitations

The certificate validator rejected deletion of an endpoint, deletion of an interior extremum, reversal, duplication, a changed height, and an off-by-one terminal index. Replacing the ceilings with floors changed the sequence and was detected. The plumbing checks rejected a central-weight perturbation and a short-arm perturbation. Synthetic root examples distinguished a single length-16 block from a single length-15 block, and checked equal-birth mergers and plateaus. Both main computations were rerun with Python optimization enabled; their checks use explicit exceptions, not removable assertions.

No substantive mathematical or arithmetic gap was found in the scoped counterexample. The conclusion still relies on the published plumbing and graded-root theorems, just as other applications of those theorems do; this audit does not reconstruct their analytic foundations. It verifies a published preprint claim with independent exact code and primary-source hypothesis checks. It is not a formal proof-assistant verification or a claim of journal peer review.
