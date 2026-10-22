# Independent mathematical audit and skew-sum reduction

The general left-weak one-step growth conjecture remains unresolved here. The conclusions below are exact auxiliary statements and finite checks, not a general solution or a claim of literature novelty.

## 1. Independent finite audit

The file `audit_pipe_dreams.py` enumerates every subset of the staircase diagram. It computes each Demazure product directly, recording row monomials and the crossing-excess sign. Reduced subsets give Schubert polynomials; all subsets give ordinary Grothendieck polynomials. This is independent of the divided-difference recurrence in `explore.py`.

Every Schubert and Grothendieck polynomial in S_5 and S_6 agrees between the two methods. Every Schubert polynomial has lexicographically smallest monomial equal to its Lehmer code, with coefficient one. Every computed Schubert expansion reconstructs the independently computed polynomial. The S_6 audit examines 32,768 crossing subsets and all 720 permutations.

The finite basis restriction is justified as follows. Every staircase pipe dream has at most n-i crosses in row i, so all its monomial exponents satisfy alpha_i <= n-i. The vector space spanned by such monomials has dimension n!. The n! Schubert polynomials indexed by S_n have distinct, unit-coefficient, lex-smallest Lehmer-code monomials and are unitriangular in this space. Consequently they form a basis of it. Thus expanding G_w for w in S_n within S_n cannot omit additional S_infinity terms.

For references to the standard pipe-dream formulas and the divided-difference definitions, see Anna Weigandt, *Changing Bases with Pipe Dream Combinatorics*, sections 2.3 and 4.1, https://arxiv.org/abs/2506.07306 .

## 2. Skew-sum factorization

Let v in S_m and z in S_n, with m,n positive. Write

v skew z = (v(1)+n, ..., v(m)+n, z(1), ..., z(n)).

For P equal to either the Schubert family S or the ordinary Grothendieck family G,

P_(v skew z)(x_1,...,x_(m+n))
= (x_1 ... x_m)^n P_v(x_1,...,x_m) P_z(x_(m+1),...,x_(m+n)).

Proof. For v=w_0^(m) and z=w_0^(n), this is the defining top monomial for w_0^(m+n). Obtain arbitrary v and z from the two block-longest permutations by a sequence of length-decreasing adjacent-position transpositions internal to their respective blocks. Apply the corresponding divided differences for Schubert polynomials, or the isobaric operators pi_i f = partial_i((1-x_(i+1))f) for Grothendieck polynomials. The rectangle monomial (x_1 ... x_m)^n is symmetric in each pair of variables on which a first-block operator acts. The opposite-block polynomial is independent of those variables. These factors therefore commute through the operator. The same reasoning applies in the second block. This proves the identity by induction on the total number of lowering steps.

The independent pipe-dream check in `audit_skew_sums.py` verifies both identities for every pair of positive block sizes with m+n <= 6. The exact proof, not that finite check, establishes the general result.

## 3. Exact product structure of the support

Let G_v = sum_a c_a S_a and G_z = sum_b d_b S_b. By the two factorization identities,

G_(v skew z) = sum_(a,b) c_a d_b S_(a skew b).

Different pairs give different permutations, so there is no cancellation. Hence

A_(v skew z) = {a skew b : a in A_v, b in A_z},

and the corresponding coefficients multiply. Furthermore,

length(a skew b) = mn + length(a) + length(b),
deg G_(v skew z) = mn + deg G_v + deg G_z.

For a left simple reflection s_k there are three cases:

- k < n: s_k(a skew b) = a skew (s_k b).
- k > n: s_k(a skew b) = (s_(k-n) a) skew b.
- k = n: this is always a descent, since the value n+1 lies in the first block and n lies in the second block.

Within S_(m+n), every left ascent from a skew sum is internal to one factor, and every upward left-weak chain starting from a skew sum remains in this skew-sum fiber. The upper-order structure is the product of the corresponding factor structures.

## 4. Exact reduction of the growth conjecture

The left-weak one-step growth conjecture holds for v skew z if and only if it holds for both v and z.

Forward direction from factors: If a skew b is below the top supported length, then at least one of a or b is below its own top supported length. Apply growth in that factor and take the corresponding block-internal left reflection.

Reverse direction: Fix b in A_z of maximum supported length. For any non-top a in A_v, the element a skew b is non-top in A_(v skew z). Its promised supported ascent cannot occur in the second factor, since b has top supported length, and it cannot occur across the block boundary, since that reflection is a descent. It therefore supplies a supported left ascent of a. Interchanging the factors gives the assertion for z.

In particular, every size-minimal counterexample would be skew-indecomposable. Iterated skew sums of known families inherit growth, with those input cases credited to Chiang and Weigandt's Oberwolfach announcement. This reduction does not prove the skew-indecomposable case, nor establish that the resulting closure class is new in the literature.

The same product structure also gives equivalence of left-weak interval convexity for the skew-sum support and its two factor supports. Indeed every interval above a skew sum remains within the fiber and is the Cartesian product of the two factor intervals.

## 5. Obstructions and orientation checks

Monomial-support transfer fails in general. The polynomial

P = S_213 - S_231 = x_1 - x_1 x_2

has alternating Schubert signs and monomial support consisting of two consecutive comparable exponent vectors. It has monomial augmentation and interval convexity. However 213 has no left ascent within its Schubert support: s_1 213 = 123 is a descent, s_2 213 = 312 is absent, and all higher simple reflections are absent. This is an obstruction to an implication for arbitrary polynomials, not a Grothendieck counterexample.

The independent computation verifies that G_12543 has coefficient +3 at S_23541, with unique supported left ascent S_24531 of coefficient -2. Its next unique supported left ascent is S_34521, of coefficient +1. Consequently a coefficient-nondecreasing ascent rule, including a fiberwise injection into all immediate successor objects, cannot prove the unweighted support conjecture.

The support of G_12543 also contains 14523, with coefficient -1, but 12543 is not below 14523 in left weak order: the position inversion (4,5) is present in 12543 and absent in 14523. Thus the support need not be a single upward-rooted interval based at the lowest-degree index w.

With inversion sets defined as pairs of positions (i,j), i<j and w(i)>w(j), inclusion is the correct orientation for LEFT weak order. Swapping two adjacent values by a left ascent adds exactly the inversion pair at their positions. Therefore the missing-neighbor convexity test in `check_posets.py` is sound: an interval gap has a first missing vertex on some saturated chain, which is precisely a missing immediate successor below a supported endpoint.

In Weigandt's reduced-path expansion with support index u=w_0 q, the requested ascent u'=s_k u corresponds exactly to q'=s_(n-k)q with length(q')=length(q)-1. Both path admissibility in the specified graph and reducedness of its word must be retained; an arbitrary shorter word or arbitrary path is insufficient.


## 6. Adversarial review verdict

Reviewed `RESEARCH_REPORT.md` as present on 2026-10-21. Verdict: PASS as a bounded research report, not as a solution of the general conjecture.

- The skew-sum proof is correct for ordinary Schubert and Grothendieck polynomials. The iff growth reduction is correct. Its quantitative cross-check has 465 skew-sum instances, 930 polynomial comparisons, and no failures for total size at most six.
- The path-shortening equivalence has the correct left/right orientation, index reversal n-k, and reversed length inequality. Admissibility and reducedness remain genuine unproved constraints, correctly identified in the report.
- The displayed G_12543 expansion and all three obstructions are correct. The coefficient example defeats even an injection into the union of immediate supported successor fibers.
- The position-inversion encoding is correctly oriented for left weak order, and the first-missing-neighbor convexity criterion is exhaustive.
- The S_8 statistics quoted in the report agree with `exact_n8.json`. The independent polynomial check reaches S_6 only, as the report discloses. No independent S_8 computation was performed by this reviewer.
- The general-solution and novelty disclaimers are necessary and are present.

Minor precision point: when claiming that every left ascent from a skew sum stays in its two-block fiber, the ambient group is S_(m+n). In S_infinity an additional reflection can leave that finite group, but such an index cannot lie in its Schubert support, by the finite-basis argument. This does not affect the report's support-growth proof.
