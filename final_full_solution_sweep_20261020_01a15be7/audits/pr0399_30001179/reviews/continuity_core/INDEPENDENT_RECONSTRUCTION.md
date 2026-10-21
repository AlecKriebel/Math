# Independent reconstruction before prior-audit comparison

Date: 21 October 2026 UTC. This record was written after reading the frozen candidate, its additive exposition and the original Skeide contribution, and before opening the two historical audit bodies in this child review. Inherited parent context already describes those bodies; analytical independence is claimed, not blind provenance independence.

## Exact target

The original source defines pointed reduced Hilbert-bimodule free products on printed529 and asks on530 whether the intersection of ordered partition tensor ranges generates the given free system. The ensuing tensor-to-free construction is a theorem about already supplied spatial tensor systems; its recovery question is separate. Nothing in the generation question restricts the ambient free system to that forward construction. Setting B=C is permitted; central unit vectors and B-bilinear unitaries are then the ordinary pointed Hilbert-space notion. B-bilinearity means compatibility with left/right coefficient actions, not that the free-product operation is a bilinear function of arbitrary vectors.

The source allows bundle regularity conditions in the usual tensor-product fashion. The candidate proves an explicit continuous field, positive-time triviality, continuous vacuum and continuous elementary multiplication; it does not assert local triviality at zero or every conceivable stronger regularity convention.

## 1. Strong projection continuity and separable field

For a fixed nonempty grade omega*n+m, each coordinate sequence converges; the closure of all its letters is a finite union of compact convergent-sequence closures and a finite set. Its supremum is attained at a coordinate or one of the finitely many block limits. Each fixed-level coordinate/limit event has measure zero, by Gaussian conditional density and the Lebesgue a-parameter. Sigma-finite other factors preserve these null sets. Hence for each fixed t>0, almost every word has supremum unequal to t, giving indicator convergence along every t_j->t. The lower endpoint0 stays fixed. Dominated convergence uses |h|², not the possibly infinite total sector measure.

At t=0, any nonempty word with all positive coordinates has at least one positive coordinate, excluding that word for sufficiently small positive t; words with a nonpositive coordinate never enter. The vacuum is fixed. Thus P_t->P_0 strongly. Countable sector sums are handled by finite-sector approximation. Standard-Borel sigma-finite sectors and their countable sum give separable H.

One can define the continuous sections directly as the norm-continuous H-valued sections x(t) with x(t) in P_tH. The sections P_th are norm continuous, pass through every fibre vector and a countable dense family h supplies a fundamental family. This is a continuous Hilbert field. It needs no norm continuity of P_t and no constant dimension near zero. The latter would be false: the zero fibre has dimension1.

## 2. Translation, dilation, full multiplication and adjoints

The sequence parameters (a,log delta,z) identify its L² space with Lebesgue in the first two variables times a Gaussian probability factor. Translation changes only a. Dilation sends (a,b) to (ra,b+log r), with the square-root factor for the a-Jacobian. Strong continuity follows on elementary compactly supported functions and extends by density. Finite products and countable sector approximation give strongly continuous T_h and D_r on H. A grade omega*n+m has scaling dimension n+m, not its ordinal length. D_r maps E_1 to E_r and supplies positive-time triviality.

For a fixed alternating pattern and fixed ordinal input grades, multiplication is a single fixed bounded concatenation unitary C applied to translated source factors. Its pointwise RN multiplier may be unbounded; that is immaterial to strong continuity because C is already a unitary between the appropriate fixed L² spaces. Each source section is norm continuous after embedding in H. Finite-grade approximation is locally uniform since ||(1-R_N)x(s)|| <= ||x(s)-x(s0)||+||(1-R_N)x(s0)||. Elementary tensors are dense in each finite tensor summand; finite patterns/grades are dense in the pointed free product. Norm bounds extend the calculation to all sections. If a centered source time tends to zero, its norm tends to zero, and every pattern containing it vanishes. Vacuum and surviving single-factor patterns give exactly the canonical zero-time identifications.

For the full field, put J=H*H, A_t=P_t-P_vac, and let Q(s,t) be the direct-sum source projection formed from tensor products of A_s,A_t on each alternating summand, with vacuum fixed. Q is strongly continuous. V(s,t)=u_(s,t)Q(s,t) is strongly continuous by the preceding calculation. Its final projection is exactly P_(s+t). This last surjectivity is an essential algebraic prerequisite supplied by the run charts.

For any fixed h, ||V(p)*h-V(p0)*h||² equals ||P_sum(p)h||²+||P_sum(p0)h||²-2 Re<h,V(p)V(p0)*h>. All three terms have their required limits. Thus V* is strongly continuous. Strong continuity of V alone would not suffice: the rank-one maps e_n->e_0 converge strongly to0 while their adjoints do not. Here the final projections converge to the actual limiting final projection, excluding that pathology.

## 3. Exact tensor core

For a fixed ordered interval partition, its tensor range consists of words whose cell labels never increase along the ordinal order; each cell supplies at most one nonvacuum run, and every such run vector is available. Positive RN multipliers preserve support ranges.

Every violation of nonincreasing real labels has two countable ordinal positions with first value smaller than the second. A rational cut strictly between them detects the violation in a two-cell tensor range. Countably many rational cuts therefore give exactly the multiplication support M of globally nonincreasing words, without taking an uncountable intersection of chosen conull sets. Every infinite block has infinitely many rises almost surely, so M is null on every grade with an infinite block. The remaining finite grades give the ordered simplexes, with equality sets Lebesgue null. This proves the rational-cut intersection is F.

For each arbitrary fixed finite partition, all finite strictly decreasing tuples belong to its ordered tensor support except cut-boundary coordinate null sets. Thus F is contained in each range as a subspace of L², even though exceptional sets can depend on the partition. Consequently the full partition intersection is F. Any actual tensor subsystem must be contained in each partition range. The calculation establishes maximality without an unsupported Hilbert-module intersection theorem.

Splitting a decreasing tuple at a fixed cut gives a unique later tuple followed by an earlier tuple; ordinary Lebesgue measures and countable sums establish that F_s tensor F_t maps unitarily onto F_(s+t). Its projections are restrictions of the fixed global decreasing-finite-word projection, commuting with P_t, so F is a continuous subfield as well.

## 4. Free hull and properness

The finite-grade support projection R_K is fixed, commutes with P_t and defines a continuous subfield K. Fixed-cut run factorization maps finite words to finite words in both directions, so K is a closed free subsystem and contains F. Every generated partition word in F is finite, proving the generated hull is contained in K even after closure.

For a finite tuple of pairwise distinct coordinates, there is a finite rational partition separating all its coordinate values. Each maximal cell-color run is then a singleton, and its one-letter factor belongs to F for that cell. On the whole relevant product rectangle, the embedded free product of F contains the entire L² support, not just an individual point or a tensor of delta functions. Countably many rational partitions cover almost every finite tuple. The join of these multiplication-support ranges is the whole finite-grade sector: disjointize the countable cover, or approximate by its increasing finite unions. Closed span therefore equals K. An arbitrary closed free subsystem containing F includes all those ranges, proving minimality.

For an explicit properness bound, restrict a in [t/3,2t/3], delta in [t/100,t/50], whose parameter measure is (t/3)log2. For every such delta, success |Z_j| < (t/(3delta))*2^j for all j puts all letters in(0,t). Since t/(3delta)>=50/3, Chebyshev and the union bound give total failure probability at most sum_j 9/(2500*4^j)=3/625. Thus the successful parameter set has measure at least (622/625)*(t/3)log2>0, and at most(t/3)log2<infinity. Intersecting with Gamma removes a null set. Its indicator is a nonzero grade-omega vector orthogonal to closed K. Independence and delicate infinite-product estimates are unnecessary for this lower bound.

## Initial verdict and remaining checks

No defect found in the assigned analytic obligations. The measure/ordinal run-chart equivalence is an essential prerequisite; its direction, fixed-grade injectivity and ordinal boundary behavior have been cross-checked but receive a separate family audit. Finite controls will test the support characterization, generation combinatorics, an exact partial-isometry identity and the explicit properness bound. They will not be described as proving the infinite-dimensional result. Historical priority is outside this family verdict.
