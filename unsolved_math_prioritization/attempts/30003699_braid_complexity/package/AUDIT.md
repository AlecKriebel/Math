# Braid-matroid coefficient complexity: scope and algorithm audit

**Disposition: partially superseded question; explicit scoped upper bound, not a new solution of an unspecified complexity problem.**

This audit concerns problem 30003699 / OWR-15987-008. Write B_n for the graphic matroid of K_n, of rank n−1, and P_n(t) for its ordinary Kazhdan–Lusztig polynomial. The original question's top-coefficient component is resolved by prior work. Its broader complexity component does not prescribe an input encoding, computational model, coefficient regime, or desired bound. Consequently there is no single formal remaining conjecture to prove or disprove. We do not claim the entire question solved or certify its remaining wording as open.

## 1. Original question and prior resolution

Wakefield's contribution, printed pp.81–84 of the Oberwolfach report [1], ends by asking what the stated coefficient formulas imply about complexity and whether they help compute the conjectured top coefficient. Its Theorem 4 applies to n≥2 and nonnegative coefficient degree i<(n−1)/2. No runtime threshold is stated. An edited description suggesting that no complete explicit coefficient formula exists is not a reliable present-day formulation.

Ferroni–Larson [2, Theorem 1.1] identify every coefficient [t^i]P_n(t) with the number of simple quasi-series-parallel matroids on the labeled set [n−1] having rank n−1−i. This is an all-coefficient interpretation. Their equivariant refinement uses the restriction to S_(n−1); this audit makes no full S_n-equivariant claim.

Their Corollary 2.12 gives, for m>1,

[t^(m−1)]P_(2m)(t) = (2m−3)!! (2m−1)^(m−2).

This is the odd-rank case, since rank(B_(2m))=2m−1. Gao–Proudfoot–Yang–Zhang [3, Theorem 1.3] give the complementary even-rank formula, again for m>1:

[t^(m−2)]P_(2m−1)(t)
= (2m−3)!! (2m−1)^(m−2)
  − (m−2)(m−1)^(m−5)(2m−1)! / (3(m−2)!).

Negative exponents at small m are evaluated rationally, not with floating-point arithmetic. At m=2 the second term is zero and P_3=1. The separate rank-zero/one cases P_1=P_2=1 cause no exception to the algorithm below. Both displayed leading formulas are credited prior results, not discoveries of this audit.

A further relevant development is Proudfoot–Xu–Young [5], published in 2025. Theorem 1.6 gives explicit counts E_(2k−r,k) of simple connected series-parallel matroids; Proposition 1.4 obtains the simple quasi-series-parallel counts from exp(E). Thus the later literature goes beyond the two leading-coefficient formulas. Its footnote to Proposition 1.4 also corrects a sign error in the proof of Ferroni–Larson Proposition 2.14. This is a published correction, not an error first discovered here.

## 2. Explicit generating functions and normalization

Let C(x,y) enumerate connected quasi-series-parallel matroids, with exponential labeling variable x and rank variable y. Ferroni–Larson Proposition 2.3 gives

f(x,y) = y^(-1) log(1+xy) + log(1+x) − x,
C(x,y) = x(1+y) + y integral_0^x f^(-1)(u,y) du,

where f^(-1) is compositional inversion in x. The apparent y^(-1) is harmless: y^(-1)log(1+xy) has polynomial y-coefficients. Its linear x-coefficient is 1, so formal inversion exists. The integration constant is zero.

Adopt the empty-matroid-inclusive normalization

A(x,y)=exp(C(x,y)),
S_plus(x,y)=A(log(1+x),y)/(1+x).

Then A(0,y)=S_plus(0,y)=1. Ferroni–Larson's displayed S excludes the constant term, so it equals S_plus−1. For n≥1,

n![x^n]S_plus(x,y) = y^n P_(n+1)(1/y).

The same equality also holds at n=0 with this normalization. These formulas give an effective all-coefficient computation, not merely a combinatorial existence statement. One must not repeat the incorrect negative exponential sign from the proof of [2, Proposition 2.14]: in the inclusive normalization the relation is A(x,y)=exp(x) S_plus(exp(x)−1,y), as [5, Proposition 1.4] states. The theorem's quotient formula above is consistent with that positive sign.

## 3. Precisely specified computational task

**Task PREFIX-KL(N).** Given an integer N≥1, output all integer coefficient lists P_1,…,P_N in binary, in ascending powers of t. The complexity parameter below is the numerical value N. It is polynomial for unary input or a size parameter N, not polynomial in the bit-length log N of a succinct binary-only input. It also supplies an upper bound for one coefficient by computing the prefix, without claiming that this is the best method for that different task.

**Scoped corollary.** The established Z-polynomial recurrence has an implementation using O(N³) integer arithmetic operations, O(N²) stored integers, O(N log(N+1)) bits per integer, O(N⁵ log²(N+1)) bit operations with schoolbook arithmetic, and O(N³ log(N+1)) storage bits.

These are conservative upper bounds for the specified implementation. They are not optimality results, lower bounds, or novelty claims. Ferroni–Larson already refer to Proudfoot–Xu–Young [4, Corollary 4.2] as the fastest known practical recurrence at the time of their article. We reconstruct that established machinery and give explicit elementary accounting.

### Recurrence and correctness

Let {n brace k} be a Stirling number of the second kind. A flat of B_n corresponds to a partition into k blocks; it has rank n−k and its contraction has the same lattice of flats as B_k. Therefore

Z_n(t) = sum_(k=1)^n {n brace k} t^(n−k) P_k(t).

The Z-polynomial is palindromic of degree n−1 by established theory [4]. Put

R_n(t)=sum_(k=1)^(n−1) {n brace k} t^(n−k) P_k(t).

Then Z_n=P_n+R_n. If 0≤i<(n−1)/2, the coefficient of degree n−1−i in P_n is zero, and palindromicity forces

[t^i]P_n = [t^(n−1−i)]R_n − [t^i]R_n.

Start with P_1=1, form R_n from previously computed polynomials, and use this identity for i=0,…,floor((n−2)/2). Correctness follows inductively from existence and uniqueness of the genuine Kazhdan–Lusztig polynomials and their Z-palindromicity. It does not depend on claiming that an arbitrary reflected low-degree array automatically satisfies every middle/high-degree constraint. In particular, when n−1 is even, its central degree is excluded from P_n.

### Arithmetic operation count

Precompute Stirling numbers by {n brace k}={n−1 brace k−1}+k{n−1 brace k}, in O(N²) integer operations. For each n, traverse k<n and the O(k) stored coefficients of P_k, multiplying by {n brace k} and accumulating into the shifted R_n array. There are O(n²) such operations for that n, hence O(N³) overall. Reflection/subtraction adds O(N²) operations. The stored Stirling and coefficient triangles use O(N²) integers.

### Integer-size bound

Let C_n be the maximum absolute coefficient of P_n. Define D_1=1 and

D_n=2 sum_(k=1)^(n−1) {n brace k}D_k.

The coefficient recurrence gives C_n≤D_n inductively, without requiring nonnegativity. Interpret D_n as the sum of 2^(number of jumps) over all strict chains from the discrete partition of [n] to the indiscrete partition. Once the first jump has k blocks, there are {n brace k} choices and the interval above it is a partition lattice on k objects, proving this interpretation.

Every strict chain extends to a maximal chain. A maximal chain is obtained by merging a pair of blocks at each step, so their number is

M_n=product_(j=2)^n binom(j,2)=n!(n−1)!/2^(n−1).

For n≥2, one fixed maximal chain has n−2 optional internal elements. Summing the weights of its endpoint-containing subchains gives

sum_(s=0)^(n−2) binom(n−2,s)2^(s+1)=2·3^(n−2).

A nonmaximal chain may be counted repeatedly, which only increases the upper bound. Thus

D_n≤2·3^(n−2)M_n.

Consequently log_2(D_n+1)=O(n log(n+1)). Every product and absolute partial accumulation in R_n is bounded by sum_(k<n){n brace k}D_k=D_n/2. Stirling entries are at most n^n; their positive construction intermediates satisfy the same asymptotic bit bound. Subtraction and storage preserve it. Schoolbook multiplication of O(N log(N+1))-bit integers costs O(N² log²(N+1)); combining with the operation count proves the stated bit upper bound. This reasoning concerns the Z algorithm, not the slower independent checker.

## 4. Exact checks and adversarial review

The accompanying standard-library-only script uses explicit exceptions rather than removable Python assertions. It checks:

- All coefficients for 1≤n≤18 by both the Z recurrence and the independent characteristic-polynomial KL identity, aggregated by integer partition type.
- All coefficients for 1≤n≤18 by the separate published enumeration formula [5, Theorem 1.6], followed by the exponential formula S_plus=exp(E).
- Both published leading formulas and Z-palindromicity/nonnegativity through n=60.
- Identical successful output under ordinary Python and Python's optimization flag.

For the characteristic method, a block of size a contributes product_(j=1)^(a−1)(t−j); a type with m_a blocks of size a has multiplicity n!/product_a((a!)^(m_a)m_a!). Summing its contribution times P_k gives the defining characteristic-polynomial recurrence. The script checks the entire identity, not only the coefficients used to construct P_n.

Illustrative values are P_6=1+16t+15t², P_7=1+42t+175t², and P_8=1+99t+1225t²+735t³. The independent review addresses indexing, chain overcounting, arithmetic/bit-model separation, and prior-work attribution. These finite checks detect transcription and implementation errors; they do not substitute for the general proof or a complete re-proof of the cited literature.

## 5. What is and is not established

The original top-coefficient conjecture is resolved by prior literature. All coefficients have both a published combinatorial interpretation and effective explicit formulas. A clearly specified full-prefix computation has the polynomial upper bounds proved above. No claim of a new algorithm or newly resolved original conjecture is made.

The informal original complexity wording is not equivalent to a question about optimal bit complexity, a uniform fixed-degree formula, binary-input runtime, or a shortest closed form. Each would require its own precise target and comparison criterion. No such unprovided target is manufactured here. The audit separates the original question, established solutions, a specified algorithm, a proved complexity bound, and independent verification. This is not an exhaustive literature search or an openness certificate.

## References

1. Max Wakefield, *Braid matroid Kazhdan–Lusztig polynomials*, pp.81–84 in *Topology of Arrangements and Representation Stability*, Oberwolfach Reports 2/2018. [Official report](https://ems.press/journals/owr/articles/15987), DOI 10.4171/OWR/2018/2.
2. Luis Ferroni and Matt Larson, *Kazhdan–Lusztig polynomials of braid matroids*, Communications of the American Mathematical Society 4 (2024), 64–79. [DOI](https://doi.org/10.1090/cams/28); [inspected preprint v2](https://arxiv.org/abs/2303.02253v2).
3. Alice L. L. Gao, Nicholas Proudfoot, Arthur L. B. Yang, and Zhong-Xue Zhang, *The combinatorics behind the leading Kazhdan–Lusztig coefficients of braid matroids*, Electronic Journal of Combinatorics 31(3) (2024), P3.21. [DOI](https://doi.org/10.37236/12778); [author PDF](https://pages.uoregon.edu/njp/SQSP.pdf).
4. Nicholas Proudfoot, Yuan Xu, and Ben Young, *The Z-polynomial of a matroid*, Electronic Journal of Combinatorics 25(1) (2018), P1.26. [Article](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v25i1p26); [author PDF](https://pages.uoregon.edu/njp/z.pdf).
5. Nicholas Proudfoot, Yuan Xu, and Benjamin Young, *On the enumeration of series-parallel matroids*, Advances in Applied Mathematics 163, Part B (2025), 102801. [DOI](https://doi.org/10.1016/j.aam.2024.102801); [author PDF](https://pages.uoregon.edu/njp/z2-revised.pdf); [preprint](https://arxiv.org/abs/2406.04502).
