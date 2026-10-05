# Independent adversarial audit: AIM Problem 25

Problem 20000826 · queue rank 761 · audit date 2026-10-05 UTC

## Verdict

**PASS, strictly scoped to the stated partial results and literature update.**

The general three-variable connectedness question is not solved. All five routes remain correctly classified as partial approaches. No novelty claim, minimum-variable theorem, arbitrary-grading conclusion, or general connectedness conclusion may be inferred from this audit.

**Mandatory mathematical corrections: none.** One optional wording clarification appears below. The original author directory and ZIP were not edited. The author ZIP has 24,231 bytes and SHA-256 `3ac3fb42d81b47b6982d529d43882ee6721af7dadfd52b5137e19dd3f2a3ff25`.

## 1. Scope and provenance

The audit read all ten authored files, the complete imported public research record, every authored proof, and the verifier. It independently inspected the primary problem and the relevant literature hypotheses and transfer statements. It did not reconstruct the entire published rank-two or Santos constructions from first principles.

The controlling question is Problem 25 on page 3 of the [AIM workshop problem list](https://aimath.org/WWN/hilbertschemes/hilbertschemes.pdf). Neither the displayed question nor its adjacent variable-count remark permits replacing arbitrary Hilbert functions by the toric function. The imported title is not the primary problem statement.

The author manifest matches all nine files it covers. All ten ZIP members match the author directory byte-for-byte. Both complete public-corpus byte counts and SHA-256 values were independently recomputed, and both target canonical-record hashes match. The canonical problem statement agrees with the imported report's original and clean statement fields. All ten inspected-source PDF byte counts and hashes match the author metadata. These checks establish byte identity; they do not certify every theorem in those sources.

The audit output contains authored analysis, programs, results, and public verification metadata. It contains no PDFs, source extracts, imported records, screenshots, raw datasets, or private coordination material. There were no remote writes.

## 2. Theorem 1: positive weights through two

**PASS.** The classification is an isomorphism of functors, including nonreduced bases.

Positivity is used essentially. If the variables have positive integer weights under the given homomorphism, every fixed-weight monomial space is finite-dimensional. The degree-zero piece is exactly the ground ring. Torsion in the original grading group does not defeat this conclusion: a nonconstant monomial has strictly positive integer weight.

For a locally free degree-one quotient, its kernel is locally a direct summand. The symmetric algebra quotient identity identifies the weight-two space after imposing products of the linear relations. It holds over any commutative base and requires neither division by two nor exactness of symmetric powers on arbitrary short exact sequences. Local splitting supplies the required constant ranks and compatibility with base change.

The degree decomposition of the resulting vector bundle is correct, including unequal pairs whose sums coincide and equal pairs with the same doubled degree in a group with torsion. Weight-two variables contribute a separate trivial summand even when their degrees coincide with products. Omitting this summand would be wrong.

Every remaining positive multiplication lands in a piece already killed by the Hilbert function. Thus there is no hidden third-degree compatibility equation. The rank bounds are necessary and sufficient; rank-zero quotients, no weight-one variables, and variables of weight greater than two are handled correctly. A positive prescribed rank in an unattained degree makes the scheme empty. The dimension is the sum of the base Grassmannian and relative Grassmannian dimensions. The smoothness and geometric irreducibility conclusions follow from these actual vector bundles, not from counting rational points.

Independent computations enumerate subspaces as sets of vectors, without using the author's RREF routine. They include all possible ranks for weights (1,1,1), (1,1,2), and (2,2,3) over F₂. An additional four-variable control uses degrees (1,0), (1,0), (1,1), (2,0) in Z × Z/2. It checks the collision of two kinds of squares in degree (2,0), together with all admissible and inadmissible quotient ranks.

The quotient identity was also checked over F₂[ε]/(ε²) and F₃[ε]/(ε²), using the nonconstant quotient y = εx and all parameters in the relation z = t x². The generated relation module equals the actual kernel, not merely its reduction modulo ε.

## 3. Theorem 2: standard grading and cubic top rank one

**PASS.** The contraction argument is valid in characteristics two and three and proves geometric connectedness, without claiming irreducibility.

The functional lies in the dual of Sym³(V). Its contraction is the transpose of multiplication. This dual may be viewed through divided powers; identifying it with ordinary polynomial differentiation without the characteristic restrictions would be an error.

If a subspace W lies in the contraction kernel, the functional kills W·Sym²(V). The identity Sym³(V)/(W·Sym²(V)) = Sym³(V/W) is characteristic-free. For 1 ≤ s < r, the projective bundle over the Grassmannian of (r-s)-planes therefore maps onto the underlying determinantal rank locus. This proves geometric irreducibility of its support. It does not require that the determinantal scheme be reduced or that its universal kernel be a vector bundle.

At a geometric point of contraction rank ℓ ≤ s, the incidence fiber is the Grassmannian of (s-ℓ)-planes in an (N-ℓ)-space. It is nonempty because s ≤ N. For ℓ > s the fiber is empty and the point is outside the determinantal base. For s ≥ r the base is the whole projective space. Rank-one evaluation functionals establish nonemptiness throughout the stated range, including the boundary cases.

The incidence relation is also the correct functorial one over nonreduced rings: a locally free quadratic quotient dualizes to a subbundle, and requiring contraction into that subbundle is equivalent to requiring the cubic quotient to annihilate all products of the quadratic kernel. A cubic relation multiplied by a variable lands in degree four, which is already killed. Over a varying degree-one quotient, these constructions glue on the universal quotient bundle. A nontrivial universal cubic line bundle merely twists the contraction map; it does not change the incidence condition.

The proper-map argument is sufficient. The images of two hypothetical nonempty clopen pieces would be closed, cover the base, and be disjoint because every geometric fiber is connected. This would disconnect the base. Applying the argument after algebraic closure gives exactly the claimed geometric connectedness. No flatness of the contraction-rank stratification or constancy of its kernel rank is needed.

Independent enumeration recovers all 1,023 projective cubic functionals over F₂ and all 29,524 over F₃, with rank distributions (7,84,932) and (13,468,29043). All binary quadratic incidence counts were directly enumerated, including 301 for h=(1,3,2,1). Negative controls show that ordinary differentiation drops rank for x²y in characteristic two and annihilates x³ in characteristic three.

The two-component comparison is properly limited to the characteristic range in [Cartwright–Erman–Velasco–Viray, Theorem 3.5](https://arxiv.org/html/0803.0341v2): their standing restriction excludes characteristics two and three. Their component description is not being imported into those characteristics.

## 4. Remaining authored controls

**Haiman–Sturmfels family: PASS.** The two relevant relations, their multiplication, and the equation a₁b₁ = 0 recover the stated union of two projective lines. The fourteen degree blocks examined by the author suffice because the forced monomial relations bound every surviving exponent. This agrees with [Example 1.4](https://arxiv.org/html/math/0201271v1). Independent nonreduced-base checks distinguish a = b = ε, which satisfies ab = 0, from a = ε, b = 1, whose degree-(2,2) quotient is not locally free of rank one. Therefore field-point counting has not silently replaced the flat-family condition.

**Rank jump: PASS.** Independent monomial-set multiplication gives dimensions nine and six for the two quadratic kernels. Their common dimension in degree two does not justify a fixed-rank next-stage vector bundle.

**Positive rank-one toric classification: PASS.** A mixed-sign lattice generator gives a finite consecutive chain in every attained degree. Consecutive monomials share a common factor and differ by precisely the specified generator, even when it is not primitive in its saturation. On each projective chart the monic chain relations leave a free rank-one quotient. A surjection between locally free rank-one modules is an isomorphism, so no additional ideal pieces remain. The independent controls check 256 complete degree fibers for four lattice generators, including nonsaturated lattices, and 40 chart families over dual numbers.

The rank-two input is quoted with its actual scope. [Maclagan–Thomas, Theorem 1.1](https://arxiv.org/pdf/math/0208031) treats arbitrary lattices of rank two over an arbitrary infinite field. Applying it over an algebraic closure and descending smoothness justifies the stated geometric conclusion over any field. The argument excluding a full-rank positive lattice in Z³ is valid. None of this replaces a general Hilbert function with the toric one.

## 5. Five-variable update and the polynomial-to-function transfer

**PASS.** [Cid-Ruiz, arXiv:2608.07704v1](https://arxiv.org/html/2608.07704v1) proves the biprojective disconnectedness result and states the fixed-function consequence in Corollary 2.8. The inspected current record lists the August 7, 2026 v1 submission and no journal reference. The report properly treats it as a preprint. It improves the ancillary 26-variable remark, gives no three-variable counterexample, and establishes no minimum variable count.

The critical transfer is accurately described. [Maclagan–Smith, Theorem 6.2 and its proof](https://arxiv.org/html/math/0305215) identify the sheaf Hilbert functor with the ideal data on a uniformly sufficiently positive degree region. In this standard bigrading the region is an upper orthant C. Extend a truncated ideal by zero outside C. Since C is stable under adding monomial degrees, it is an ordinary homogeneous ideal. The resulting full quotient Hilbert function is the polynomial on C and dim(S_b) outside C. Conversely, that full function forces the ideal to be zero outside C. This explains the fixed-function realization without falsely asserting equality of the original saturated ideals' low-degree functions. The uniform cutoff is for the entire parameter scheme, not merely for two chosen points.

Independently derived piecewise monomial counts agree with direct enumeration in 934 bidegrees for a=2 through 7. Both displayed ideals agree with the polynomial when u,v ≥ 2a-1; this bound is only for those two ideals. Another 10,296 monomial membership tests confirm the intersection. The degree-(1,0) mismatch is 2 versus 3 before dehomogenization and 1 versus 2 afterward. The proposed substitution also fails to preserve the original grading. Thus the stated negative control is sound and is not an impossibility theorem for all reductions.

## 6. Literature boundaries and general grading

**PASS.** The standard-grading route is correctly marked classical. The inspected [Peeva exposition, §9](https://pi.math.cornell.edu/~irena/papers/syz.pdf) discusses fixed-function deformations to lex under a standing complex ground field. The report does not claim to have inspected the blocked original Pardue PDF and does not extrapolate its field hypothesis. General coordinate changes need not preserve a finer grading; connectedness of the larger parameter scheme gives no connectedness theorem for a closed finer-graded locus.

[Hering–Maclagan, Theorem 1.1 and §2.3](https://arxiv.org/html/1110.1861v1) give the equivariant finite-support reduction for positive gradings over arbitrary base rings. The stated graph criterion retains its positive/complex hypotheses. The reduction does not impose a cutoff of two or three. The two-variable theorem is also correctly bounded by the number of variables in [Maclagan–Smith, Theorem 1.1](https://arxiv.org/html/0811.3594v2).

For a general abelian grading, the ambient S_a can be infinite-dimensional. The finite-rank requirement is on the quotient pieces. The package does not silently impose finite-dimensional ambient pieces on the full question. Such finiteness is available exactly where its positive-weight constructions need it. Nonpositive gradings remain outside the new classifications.

## 7. Computational reproducibility and adversarial checks

The author verifier completed from /tmp and produced byte-identical output. The independent verifier imports no author functions and uses vector-set closure, direct incidence containment, explicit dual-number arithmetic, and independent piecewise monomial formulas. It passes both ordinary and optimized Python, with identical results; its checks do not rely on assert statements.

Five temporary mutations of the author verifier were all rejected: dropping weight-two variables, substituting ordinary derivatives, changing the Haiman incidence equation, pretending the two full Hilbert functions agree, and pretending the third-layer multiplication rank is constant. These temporary copies were not retained or packaged.

These computations test the displayed statements and dangerous substitutions. They do not prove universal connectedness, geometric irreducibility from finite counts, or the absence of a three-variable counterexample.

## 8. Optional clarification and final disposition

In Theorem 1, the sentence beginning “In particular” about unattained degrees would read more precisely as an explicit additional condition, or could be omitted because the theorem subsequently handles that condition and the empty case. Weight support alone does not imply vanishing at unattained degrees of weights one or two. This wording does not invalidate the displayed classification, whose nonempty criterion explicitly includes the missing condition.

No mandatory mathematical changes were found. Keep the original partial-progress status, the arbitrary-grading gap, the no-novelty statement, the characteristic boundaries, and the fixed-polynomial versus fixed-function distinction. This audit approves the scoped claims only.
