# Independent review: braid-matroid coefficient complexity

## Verdict and scope

The palindromic recurrence below correctly computes all ordinary Kazhdan–Lusztig polynomials of braid matroids through vertex count N using O(N^3) integer arithmetic operations. A weighted-partition-chain majorant proves that all stored integers and arithmetic intermediates have O(N log(N+1)) bits. Consequently schoolbook integer arithmetic gives the conservative upper bound O(N^5 log²(N+1)) bit operations. These are upper bounds for an explicitly specified dense computation, not optimality claims, and not a claim to settle every interpretation of the original informal question.

Wakefield's original report asks what its Theorems 2–4 imply about coefficient complexity and whether they help compute the conjectured top coefficient. It specifies no computational model, target runtime, or fixed-degree versus variable-degree regime. Thus proving a uniform algorithmic upper bound answers a precisely chosen interpretation, not a literally stated complexity conjecture. In particular, polynomial time in N is not polynomial time in the binary input length log N.

Prior results must remain central:

- Ferroni–Larson Theorem 1.1 gives an interpretation of every coefficient, not merely the leading one: [t^i]P(B_n,t) counts simple quasi-series-parallel matroids of rank n−1−i on the labeled set [n−1]. Their generating-function results already give explicit computation.
- Ferroni–Larson Corollary 2.12 proves the formerly conjectured leading coefficient for B_(2m), whose rank is odd: (2m−3)!!(2m−1)^(m−2), m>1.
- Gao–Proudfoot–Yang–Zhang Theorem 1.3 gives the complementary leading coefficient for B_(2m−1), whose rank is even: (2m−1)^(m−2)(2m−3)!! − (m−2)(m−1)^(m−5)(2m−1)!/[3(m−2)!], m>1.
- Ferroni–Larson §1.3 explicitly identifies the recurrence of Proudfoot–Xu–Young, Corollary 4.2, as the fastest known computation of P and Z in that paper. The reconstruction here uses established Z-polynomial machinery. No novelty claim is justified by this review or by an absence of an inspected bit-complexity theorem.

## Derivation and indexing checks

Let P_n=P(B_n,t), so P_1=1 and rank(B_n)=n−1. For n≥2, deg P_n<(n−1)/2. A flat of B_n corresponds to a partition of [n] into k blocks, has rank n−k, and its contraction has simplification B_k. The lattice-based Kazhdan–Lusztig polynomial is unchanged by simplification. Since there are S(n,k) such partitions, the defining Z-polynomial sum gives

Z_n(t)=Σ_(k=1)^n S(n,k)t^(n−k)P_k(t).

This is palindromic of degree n−1. The k=n term is exactly P_n. Put

R_n(t)=Σ_(k=1)^(n−1) S(n,k)t^(n−k)P_k(t)=Σ_j r_(n,j)t^j.

For 0≤i<(n−1)/2, the coefficient of degree n−1−i in P_n is zero, whereas the coefficient of degree i is p_(n,i). Palindromy therefore gives

p_(n,i)=r_(n,n−1−i)−r_(n,i).

Thus compute indices i=0,…,floor((n−2)/2), inclusive, with missing coefficients interpreted as zero. The rank-zero case n=1 is a separate initialization. When n−1 is even the central coefficient is not an unknown coefficient of P_n: imposing a degree-(n−1)/2 coefficient would be an indexing error.

The correctness argument uses the existence and uniqueness theorem for the established Z-polynomial characterization. If presented as a stand-alone construction from arbitrary arrays, reflection of low coefficients alone would not prove every middle/high palindromy equation. Here induction identifies every computed low coefficient with that of the existing P_n, and the degree bound excludes all other coefficients.

## Arithmetic count

Compute S(n,k) by S(n,k)=kS(n−1,k)+S(n−1,k−1), with S(0,0)=1 and the usual zero boundary values. This costs O(N²) integer operations. For each n, accumulate R_n by scaling and shifting each previously computed P_k, k<n. Each P_k has O(k) stored coefficients, so this costs O(n²) integer additions and multiplications per n and O(N³) through N. Extracting coefficients costs O(N²) overall. This bound does not enumerate individual set partitions or individual chains.

## Rigorous bit bound: weighted chains

A loose induction C_n≤2N^N max_(k<n) C_k does not prove O(N log N) bits: iterating it permits O(N² log N) bits. That proof route must not be used to claim the sharper bound.

Instead let C_n be the maximum absolute coefficient of P_n and define positive integers

D_1=1,   D_n=2Σ_(k=1)^(n−1)S(n,k)D_k  (n≥2).

The reflection formula and triangle inequality give C_n≤2Σ_(k<n)S(n,k)C_k, so induction gives C_n≤D_n.

Interpret D_n as the total weight of all strict chains from the discrete partition to the indiscrete partition of [n], with weight 2^j for a chain having j strict jumps. The first jump selects a partition with k<n blocks, with S(n,k) choices, and the interval above it is the partition lattice on k blocks. This proves the interpretation, including D_1=1 for the empty chain.

Every such strict chain extends to a maximal chain. A maximal chain has n−1 jumps and n−2 intermediate partitions. Summing the weights of all its subchains that retain both endpoints gives

Σ_(a=0)^(n−2) binom(n−2,a)2^(a+1)=2·3^(n−2).

There are M_n=∏_(j=2)^n binom(j,2)=n!(n−1)!/2^(n−1) maximal chains: at a state with j blocks, choose the next merged pair. A strict chain may extend to several maximal chains, which only increases the following upper bound:

D_n≤2·3^(n−2)M_n,  n≥2.

Taking logarithms gives log₂(D_n+1)=O(n log(n+1)). This proof uses no coefficient positivity theorem and no enumerative interpretation of Ferroni–Larson.

Each scaled coefficient contributing to R_n, and each partial sum of such contributions, has absolute value at most Σ_(k<n)S(n,k)D_k=D_n/2. Each final reflection subtraction has absolute value at most D_n. The Stirling table also has O(N log(N+1))-bit entries since S(n,k)≤n^n. Its multiplication and addition intermediates satisfy the same asymptotic bound. Hence every operation can use b=O(N log(N+1)) bits, including temporary products; schoolbook multiplication costs O(b²), addition/subtraction O(b). Multiplying this conservative cost by O(N³) operations proves O(N^5 log²(N+1)) bit time. Dense coefficient and Stirling storage uses O(N²) integers, hence O(N³ log(N+1)) bits.

## Acceptance conditions

Accept the mathematical upper bound with the stated conventions and established Z-polynomial characterization. Do not label the original broad question fully solved, do not present the recurrence as new, and do not infer a literature-wide novelty or openness statement from a bounded source review. Benchmark agreement is useful implementation evidence, not a replacement for the proof. Any reported computation must separately specify which coefficients and range were checked.

## Additional enumeration source and implementation review

Proudfoot–Xu–Young, *On the enumeration of series-parallel matroids*, gives a further all-coefficient route. Theorem 1.6 explicitly computes the numbers E_(2k−r,k) of simple connected series-parallel matroids for 0≤r≤k using unsigned associated Stirling numbers of the first kind. Proposition 1.4 then gives S(x,y)=exp(E(x,y)), and Ferroni–Larson's interpretation extracts every coefficient of P_n from S_(n−1,n−1−i). This strengthens the conclusion that a blanket claim of no explicit all-coefficient formula is untenable.

Normalization matters: E and C start at positive cardinality; S and A include the empty matroid, with constant term 1. Proposition 1.4's footnote explicitly identifies and corrects a sign error in an equation in the proof of Ferroni–Larson Proposition 2.14. The corrected relation is A(x,y)=S(exp(x)−1,y)exp(x). The tested enumeration route uses S=exp(E), not that corrected fourth relation, and does not silently transport incompatible constant-term conventions.

I inspected the complete Python checker and reran it both normally and with optimization enabled. Both runs returned PASS and produced byte-identical JSON. All three computational routes agree on every coefficient for 1≤n≤18: the palindromic Z recurrence, the original characteristic-polynomial recurrence grouped by block sizes, and the associated-Stirling enumeration formula followed by labeled exponentiation. Leading-coefficient formulas, nonnegativity, and complete Z palindromy were checked for 1≤n≤60. The characteristic-polynomial route checks its full identity, not just the coefficients used for extraction. Validation uses explicit exceptions rather than assertions, so optimization does not disable it.

Specific enumeration checks: the associated-Stirling table initializes d_(0,0)=1 and uses d_(m,k)=(m−1)(d_(m−2,k−1)+d_(m−1,k)); the signs and bounds in Theorem 1.6 match the implementation; the singleton E_(1,1)=1 is recovered correctly; the empty object S_(0,0)=1 is present; and the factor binom(n−1,j−1) correctly chooses the component containing a distinguished label in the exponential recurrence. Fraction arithmetic handles negative exponents at boundary cases exactly. The characteristic route correctly includes both block-factorial and repeated-block-multiplicity factors. I found no implementation error affecting the claimed tests.

The numerical checks do not prove agreement beyond the stated finite range, nor do they establish a complexity bound for the slower verification algorithms. The O(N³) arithmetic and O(N⁵ log²(N+1)) bit bounds apply to the Z-based algorithm analyzed above. Independence here means distinct computational formulas; it does not mean that the enumerative route is logically independent of Ferroni–Larson's theorem.

## Public sources

- Max Wakefield, “Braid matroid Kazhdan–Lusztig polynomials,” pp. 81–84 in *Topology of Arrangements and Representation Stability*, Oberwolfach Reports 2/2018. https://ems.press/journals/owr/articles/15987
- Luis Ferroni and Matt Larson, *Kazhdan–Lusztig polynomials of braid matroids*, Communications of the American Mathematical Society 4 (2024), 64–79. https://doi.org/10.1090/cams/28 ; inspected author version: https://arxiv.org/abs/2303.02253v2
- Alice L. L. Gao, Nicholas Proudfoot, Arthur L. B. Yang, Zhong-Xue Zhang, *The combinatorics behind the leading Kazhdan–Lusztig coefficients of braid matroids*, Electronic Journal of Combinatorics 31(3) (2024), P3.21. https://doi.org/10.37236/12778 ; author PDF: https://pages.uoregon.edu/njp/SQSP.pdf
- Nicholas Proudfoot, Yuan Xu, Ben Young, *The Z-polynomial of a matroid*, Electronic Journal of Combinatorics 25(1) (2018), P1.26. https://arxiv.org/abs/1706.05575 . Attribution here is confirmed through Ferroni–Larson; this review did not independently inspect that paper's Corollary 4.2.
- Nicholas Proudfoot, Yuan Xu, Benjamin Young, *On the enumeration of series-parallel matroids*, Advances in Applied Mathematics 163, Part B (February 2025), 102801. https://doi.org/10.1016/j.aam.2024.102801 ; inspected author PDF: https://pages.uoregon.edu/njp/z2-revised.pdf ; preprint: https://arxiv.org/abs/2406.04502 .

## Final-document acceptance

I reviewed the completed accompanying audit, including its additional generating-function section, against the inspected sources and the derivation above. The formal inverse has linear coefficient 1, the integration constant and empty-object normalization are correct, and the positive exponential correction agrees with the later source. The scoped complexity claim and weighted-chain proof are sound. Its leading-rank parity, base cases, and coefficient-reflection range are correct. The final document expressly disclaims a new algorithm, a newly resolved original conjecture, optimality, and an exhaustive openness certificate. I found no mathematical or scope defect requiring rejection. Acceptance is confined to this authored audit and its specified finite verification ranges, not a new proof of every cited result.
