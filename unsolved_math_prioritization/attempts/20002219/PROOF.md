# Bounded-interval minima of Schur ratios: accepted partial results

This is an AI-assisted, unrefereed mathematical edition. Acceptance means an independent internal AI audit of the stated partial results. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The full authored proof and full mathematical audit are retained in PROOF.md and AUDIT.md. Copied source documents, source text and images, executable code, raw datasets, raw search responses and private coordination material are not distributed. References to checking programs describe historical verification; those programs are not included.

Source retrieval, inspection and mathematical execution statements describe the original candidate and independent audit of October 11, 2026 UTC. Editorial preparation authenticated their sealed bytes, but performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Finite checks support exact identities only; the universal analytic and sign arguments must be read in full.

## 1. Exact scope and conventions

Fix N≥1 and ordinary partitions λ=(λ₁≥⋯≥λ_N≥0) and μ=(μ₁≥⋯≥μ_N≥0), padded with zero parts. Write |λ|=Σλᵢ, D=|λ|−|μ|, and

\[
R_{\lambda,\mu}(x)=\frac{s_\lambda(x)/s_\lambda(1^N)}{s_\mu(x)/s_\mu(1^N)}.
\tag{1}
\]

Schur polynomials are positive on the positive orthant, so the ratio is well defined. We study R≥1 on I^N. This is exactly the assertion that the unnormalized ratio has a minimum at 1^N **when 1∈I**. If 1 is in the closure but not in I, validity gives infimum value 1 for R by continuity along diagonal points approaching 1. It does not assert attainment at the absent point; in degree zero the same value may still be attained at other diagonal points. If 1 is not even in the closure, comparison with R(1)=1 is still meaningful but is not a claim that 1 is a domain minimizer.

Let a=inf I∈[0,∞), b=sup I∈(0,∞], for a nonempty interval I⊂(0,∞). A finite positive endpoint can be tested by a limit whether or not it belongs to I. Indeed, positivity and continuity imply that R≥1 on I^N is equivalent to R≥1 on its closure inside (0,∞)^N. The conventions at 0 and infinity require limits rather than evaluations.

The strict increasing exponent tuple associated with λ is

\[
n_j=\lambda_{N-j}+j,\qquad 0\le j<N.
\tag{2}
\]

Thus s_λ(x)=det(x_i^{n_j})/det(x_i^j), with a common ordering of the columns. The reversal and staircase in (2) are essential; the tuple is not the partition itself. Conversely λ_i=n_{N-i}−(N−i). The two Vandermonde denominators cancel in ratios. Normalizing by the value at 1 converts the ratio into the corresponding normalized generalized-Vandermonde ratio. Adding the same rectangle (r^N) to λ and μ leaves R and the unnormalized ratio unchanged. This permits positive-part formulations of our examples.

For decreasing vectors, weak majorization means that all initial partial sums of the first vector are at least those of the second. Majorization also requires equal total sums. When negating a tuple, rearrange it before taking initial sums. The staircase contributions in (2) cancel in comparisons of corresponding initial sums, so the standard majorization conditions translate correctly between these conventions.

For N=1, R(x)=x^D; all claims follow immediately. The detailed two-variable and higher-dimensional results below concern N≥2.

## 2. Known orthant results and what their proof does not imply

Khare and Tao, [1, Theorem 10.1], characterize weak majorization using normalized generalized Vandermonde determinants on [1,∞)^N. Their converse sends selected coordinates to infinity to recover each partial-sum inequality. [1, Corollary 10.4] applies reciprocal variables to obtain the corresponding condition on (0,1]^N. The full positive orthant gives majorization. The proof of Theorem 10.1 and its reciprocal corollary was read here, not only their statements.

Their neighborhood-of-infinity variant uses unbounded scaling as well. A fixed finite box has no such scaling sequence. Thus none of these converse arguments proves necessity of weak majorization on a fixed finite interval. The examples below show concretely why that extrapolation fails, even with equal degrees and intervals on both sides of 1.

The later strict-monotonicity theorem [2, Theorems 1.4–1.5] assumes coordinatewise domination of exponent tuples. The inspected introduction of [3] concerns Jack/Macdonald majorization questions. Neither inspected passage gives an arbitrary finite-box classification. This is a limited source comparison, not an exhaustive literature claim or a novelty claim.

## 3. Complete two-variable answer near the reference point

Let λ=(a,b), μ=(c,d), with a≥b≥0, c≥d≥0. Set

\[
D=a+b-c-d,\qquad p=a-b+1,\qquad q=c-d+1.
\]

For T≥0, define

\[
H(T)=\begin{cases}\dfrac{q\sinh(pT)}{p\sinh(qT)},&T>0,\\1,&T=0.\end{cases}
\tag{3}
\]

### Theorem 1 (N=2 interval classification)

Assume I is nondegenerate and 1 lies in its closure.

1. If a_I:=inf I<1<sup I=:b_I, then R≥1 on I² if and only if D=0 and p≥q.
2. If a_I=1<b_I<∞, put T=(log b_I)/2. Then R≥1 if and only if D≥0 and e^{DT}H(T)≥1.
3. If a_I=1 and b_I=∞, then R≥1 if and only if D≥0 and D≥q−p.
4. If 0<a_I<b_I=1, put T=−(log a_I)/2. Then R≥1 if and only if D≤0 and e^{−DT}H(T)≥1.
5. If a_I=0 and b_I=1, then R≥1 if and only if D≤0 and −D≥q−p.

The finite endpoint inequalities include D=0: they then say exactly p≥q. No endpoint-inclusion assumption is needed for the inequality criterion. The singleton I={1} is trivial for all λ,μ.

### Proof

The bialternant formula gives

\[
s_{(a,b)}(x,y)=(xy)^b\frac{x^p-y^p}{x-y},
\]

with the continuous value at x=y. Write x=e^{u+v}, y=e^{u-v}, t=|v|. Since s_(a,b)(1,1)=p,

\[
R(e^{u+v},e^{u-v})=e^{Du}H(t).
\tag{4}
\]

For A=inf(log I) and B=sup(log I), feasibility in the closure means

\[
0\le t\le(B-A)/2,\qquad A+t\le u\le B-t.
\tag{5}
\]

Infinite endpoints and excluded finite endpoints are interpreted in the evident limiting way. Homogeneity on diagonal points gives R(z,z)=z^D. Hence D must be nonnegative on right-sided intervals, nonpositive on left-sided intervals, and zero on two-sided intervals.

Put F=log H. For t>0,

\[
F'(t)=p\coth(pt)-q\coth(qt),\qquad
F''(t)=q^2\operatorname{csch}^2(qt)-p^2\operatorname{csch}^2(pt).
\tag{6}
\]

For fixed t>0, r↦r coth(rt) is strictly increasing: its derivative has the sign of sinh(rt)cosh(rt)−rt, which is positive because its value at zero is zero and its derivative in rt is 2sinh²(rt)>0. Also r↦r/sinh(rt) is strictly decreasing: its logarithmic derivative is 1/r−t coth(rt)<0, since s coth s>1 for s>0. Therefore F is positive and increasing when p>q, zero when p=q, and negative, decreasing, and strictly concave when p<q. We also have F(0)=F'(0)=0 by the power series of sinh.

For a right-sided interval, A=0 and D≥0. For each fixed t, the minimum over u is attained or approached at u=t. Its logarithm is h(t)=Dt+F(t). If p≥q, h(t)≥0. If p<q, h is strictly concave with h(0)=0; on a finite interval [0,T] it is nonnegative everywhere exactly when h(T)≥0. Sufficiency is the chord inequality. Necessity follows by evaluating the endpoint, or by continuity if it is excluded. This proves part 2, including D=0.

For an unbounded right interval, when p<q, h'(t) decreases to D+p−q. If that limit is nonnegative, h is nondecreasing from zero and is nonnegative. If the limit is negative, the asymptotic expansion

\[
h(t)=(D+p-q)t+\log(q/p)+o(1)
\]

forces negativity for sufficiently large t. When p≥q the extra condition D≥q−p is automatic from D≥0. This proves part 3.

For a left-sided interval, B=0 and D≤0. The minimizing mean is u=−t, so the same function becomes |D|t+F(t); the previous argument proves parts 4 and 5. On a two-sided interval the diagonal test forces D=0, and (4) is ≥1 for every spread exactly when p≥q. This proves part 1. ∎

### Equality and thresholds

If D=0 and p>q, exactly the diagonal points are minimizers. If D=0 and p=q, the ratio is identically 1. If D≠0 and a finite one-sided endpoint test is strict, the only minimum at value 1 is (1,1), provided 1 belongs to I. If the endpoint test is an equality, strict concavity gives two additional equality configurations at opposite endpoints, provided both endpoints belong to I. If 1 is excluded, all configurations needing that endpoint are absent. For valid infinite one-sided intervals and D≠0, the only equality configuration is (1,1), when present.

More explicitly, if p<q and 0<|D|<q−p, the function |D|+F(t)/t strictly decreases from |D| to |D|+p−q. This follows from strict concavity of F and F(0)=0. It therefore has a unique zero T_*>0. The valid one-sided logarithmic width is exactly at most 2T_*. If |D|≥q−p there is no finite cutoff. These statements need no numerical optimization.

The unbounded right conditions are a≥c and a+b≥c+d. The unbounded left conditions are b≤d and a+b≤c+d, as follows by substituting p−q=(a−b)−(c−d). They agree with the known weak-majorization criteria.

### An audited imported example

Take λ=(3,3), μ=(4,1). These already have positive parts. Then

\[
R(x,y)=\frac{4x^2y^2}{x^3+x^2y+xy^2+y^3}.
\]

Theorem 1 says that on [1,B]², with B>1, validity is equivalent to R(1,B)≥1. Its numerator difference is

\[
4B^2-(1+B+B^2+B^3)=-(B-1)(B^2-2B-1).
\]

Thus validity is exactly B≤1+√2, although λ does not weakly majorize μ. This example and the N=2 reduction were present in the imported report; they are independently proved here and are not claimed as new contributions.

## 4. An exact three-variable transition without majorization

### Theorem 2

Let λ=(5,1,1), μ=(4,3,0), and let ρ be the unique root in (4/3,27/20) of

\[
5\rho^3-6\rho-4=0.
\tag{7}
\]

For any nonempty interval I⊂(0,∞),

\[
R_{\lambda,\mu}(x)\ge1\quad\hbox{for every }x\in I^3
\quad\Longleftrightarrow\quad
\frac{\sup I}{\inf I}\le\rho.
\tag{8}
\]

The endpoint quotient is +∞ if inf I=0 or sup I=∞. In particular, for intervals containing 1, (8) exactly determines whether the minimum is attained at 1³. If the endpoint quotient equals ρ, all diagonal triples are equality configurations, and the only possible additional ones are permutations of (b,b,a), with a=inf I, b=sup I; these additional triples occur only when both endpoints belong to I. If the endpoint quotient is less than ρ, only diagonal triples give equality.

The same theorem holds for positive partitions (6,2,2) and (5,4,1), because adding (1,1,1) leaves the ratio unchanged. Both pairs have crossing partial sums, hence neither partition majorizes the other.

### Proof: polynomial reduction

Let h_j(x,y,z)=Σ_{r+s+t=j}x^r y^s z^t be the complete homogeneous symmetric polynomial. Factoring the common determinant character and using the two-row Jacobi–Trudi determinant give

\[
s_{(5,1,1)}=xyz\,h_4,\qquad
s_{(4,3,0)}=h_4h_3-h_5h_2.
\tag{9}
\]

At (1,1,1), h_j=\binom{j+2}{2}, so the two dimensions are 15 and 24. Consequently, R≥1 is equivalent to P≥0, where

\[
P(x,y,z)=24xyz\,h_4-15(h_4h_3-h_5h_2).
\tag{10}
\]

This is symmetric and homogeneous of degree 7. A positive triple may be sorted and scaled to (1+d,1+td,1), where d≥0 and 0≤t≤1. The case d=0 is diagonal and has P=0. For d>0, direct finite polynomial expansion gives the identity

\[
\frac{P(1+d,1+td,1)}{d^2}
=\sum_{k=0}^{5} B_k(d)\binom{5}{k}t^k(1-t)^{5-k},
\tag{11}
\]

where

\[
\begin{aligned}
B_0(d)&=6(4d^3+18d^2+24d+5),\\
B_1(d)&=\frac35(8d^4+74d^3+204d^2+193d+40),\\
B_2(d)&=\frac32(4d^4+26d^3+56d^2+49d+14),\\
B_3(d)&=-\frac32(d+1)(d^4+5d^3+7d^2-7d-14),\\
B_4(d)&=-\frac35(d+1)(15d^4+85d^3+135d^2+33d-40),\\
B_5(d)&=-6(d+1)^2(5d^3+15d^2+9d-5).
\end{aligned}
\tag{12}
\]

For a fully elementary way to reproduce (11), expand each h_j from its displayed finite sum, substitute x=1+d,y=1+td,z=1, divide the resulting polynomial by d², and change t^j into

\[
t^j=\sum_{k=j}^{5}\frac{\binom{k}{j}}{\binom{5}{j}}
\binom{5}{k}t^k(1-t)^{5-k}.
\]

This basis identity follows by factoring t^j and applying the binomial theorem to (t+(1−t))^{5−j}. The standard-library checker independently performs both expansions and verifies every coefficient of (11); the written identity itself is a finite certificate and does not depend on a numerical search.

### Proof: positivity of the certificate

Put p(d)=5d³+15d²+9d−5. Its derivative 15d²+30d+9 is positive for d≥0. Also p(1/3)=−4/27<0 and p(7/20)>0. Hence its unique nonnegative zero d_*=ρ−1 lies in (1/3,7/20).

For 0≤d≤d_*, B₀,B₁,B₂ are strictly positive by their coefficients. To handle B₃, use d≤7/20 and discard its negative linear term:

\[
d^4+5d^3+7d^2-7d-14
\le (7/20)^4+5(7/20)^3+7(7/20)^2-14
=-\frac{2066099}{160000}<0.
\]

For B₄, its inner polynomial is increasing on [0,∞), and

\[
15(7/20)^4+85(7/20)^3+135(7/20)^2+33(7/20)-40
=-\frac{257377}{32000}<0.
\]

Thus B₃,B₄ are strictly positive too. Finally, B₅≥0 is exactly p(d)≤0, and is strict unless d=d_*. Since every Bernstein basis element in (11) is nonnegative on [0,1], P≥0 whenever d≤d_*.

For sharpness, t=1 in (11) gives

\[
P(r,r,1)=-6r^2(r-1)^2(5r^3-6r-4).
\tag{13}
\]

For r>ρ this is strictly negative, since 5r³−6r−4 is strictly increasing for r≥1. Therefore no larger coordinate ratio is permissible for every triple.

For a general triple, sorting and scaling identify 1+d=max(x_i)/min(x_i). If b/a≤ρ, all triples in I³ have coordinate ratio at most ρ and are covered by the positivity proof. If b/a>ρ, including an infinite endpoint quotient, there exist positive a',b' in I with b'/a'>ρ; otherwise every pair of points in I would have quotient at most ρ, forcing the supremum quotient to be at most ρ. Equation (13) then makes (b',b',a') a counterexample after scaling. This proves (8), including open and infinite endpoints.

For equality, when d>0 and t<1 the k=0 summand of (11) is strictly positive. At t=1 only B₅ contributes, and it vanishes precisely at d=d_*. Scaling back gives exactly the off-diagonal pattern (ρc,ρc,c). When b/a≤ρ, this pattern can fit in I only if b/a=ρ and c=a, ρc=b. This proves the endpoint and equality assertions. ∎

### Consequences and exact checks

The partitions have total size 7, but their first partial sums are 5>4 and their first two partial sums are 6<7. Thus the majorization order crosses. Their increasing exponent tuples are (1,2,7) and (0,4,6), respectively. Adding one to all parts gives positive partitions (6,2,2),(5,4,1) and positive exponent tuples (2,3,8),(1,5,7).

For example I=[1,4/3] satisfies the criterion, as does the genuinely two-sided interval [9/10,11/10], whose endpoint quotient is 11/9<4/3<ρ. On either interval 1³ is a minimum despite failure of majorization. Conversely I=[1,3/2] fails at (3/2,3/2,1). These conclusions are exact rational comparisons, not deductions from the decimal approximation ρ=1.34045265506422… .

This is one fully classified N=3 pair, not a classification of all N=3 partition pairs. In particular, the proof does not justify reducing arbitrary higher-dimensional Schur-ratio comparisons to vertices or to two-valued vectors.

## 5. General-dimensional local criteria

These statements are useful even when a global bounded-box classification is unavailable. Their proofs use only nonnegative coefficients, homogeneity, and symmetry.

### Weight-distribution notation

Write s_ν(x)=Σ_α c_α x^α, where c_α are nonnegative integers and |α|=|ν|. The coefficient positivity follows directly from the semistandard-tableau definition of Schur polynomials. Give α the probability c_α/s_ν(1^N), and call the resulting random vector A_ν. This is a finite probability distribution. Symmetry gives E A_ν=(|ν|/N)1. Define

\[
f_\nu(y)=\log\frac{s_\nu(e^{y_1},\ldots,e^{y_N})}{s_\nu(1^N)}
=\log E\exp(A_\nu\cdot y).
\tag{14}
\]

All differentiation below is justified by finite sums. The first derivative of a log moment-generating function is its tilted mean, and its second directional derivative is the tilted variance; both identities follow by the quotient rule.

### Proposition 3 (explicit one-sided radius)

Let k=|λ|, l=|μ| and D=k−l. For every y∈R^N,

\[
\log R(e^y)\ge D\bar y-\frac{l^2}{8}
(\max_i y_i-\min_i y_i)^2,
\qquad \bar y=\frac1N\sum_i y_i.
\tag{15}
\]

If l>0 and D>0, R>1 away from 1^N on [1,e^B]^N whenever 0<B<8D/(Nl²). If D<0, R>1 away from 1^N on [e^{−B},1]^N whenever 0<B<8|D|/(Nl²). If l=0 and D>0, R>1 away from 1^N throughout [1,∞)^N. The opposite degree signs are impossible on any nondegenerate interval starting at 1; on any interval containing points on both sides of 1, D=0 is necessary.

#### Proof

For a random variable X supported in [m,M], Var(X)≤(M−m)²/4. To see this without an external inequality, E[(X−m)(M−X)]≥0 implies Var(X)≤(EX−m)(M−EX), and the latter product is at most (M−m)²/4.

Apply this under every exponential tilt to X=A_μ·y. Because A_μ has nonnegative coordinates summing to l, X is supported in [l min y,l max y]. If h(t)=f_μ(ty), then h(0)=0, h'(0)=l\bar y, and h''(t)≤l²(range y)²/4. Taylor's integral formula between 0 and 1 yields

f_μ(y)≤l\bar y+l²(range y)²/8.

Jensen's inequality gives f_λ(y)≥k\bar y. Subtracting proves (15). For y in a right box and r=max y_i>0, \bar y≥r/N and range y≤r≤B; (15) is at least r(D/N−l²B/8)>0. On a left box take r=max(−y_i), so D\bar y≥|D|r/N, and the same argument applies. If l=0, f_μ=0 and Jensen gives f_λ(y)≥k\bar y>0 for nonzero y≥0. The sign obstructions follow from R(t1)=t^D. ∎

This quantitative bound is sufficient only; it is not asserted to be the sharp allowable radius.

### Proposition 4 (equal-degree covariance test)

Suppose |λ|=|μ|=k and N≥2. Put

\[
c_\nu=\frac{E\|A_\nu-(k/N)1\|^2}{N-1},\qquad c=c_\lambda-c_\mu.
\tag{16}
\]

If c>0, there is ε>0 such that R(e^y)>1 whenever ||y−\bar y1||<ε and y is not constant. Hence every sufficiently small multiplicative-width box, including a two-sided neighborhood of 1, satisfies the comparison. If c<0, R(e^y)<1 for all sufficiently small nonzero centered y, and no nondegenerate interval with 1 in its closure can satisfy the comparison on its N-fold power. When c=0 this second-order test gives no conclusion.

#### Proof

The covariance matrix of A_ν is permutation invariant. Since Σ_i A_ν,i=k is constant, it annihilates 1. Therefore it has the form c_ν(I−11ᵀ/N), with c_ν determined by its trace as in (16). The Hessian at zero of f_ν is that covariance matrix. The degree equality makes g(y):=log R(e^y) invariant under y↦y+t1. Its gradient at zero is zero, and for z⊥1 its Taylor expansion is

\[
g(z)=\frac c2\|z\|^2+O(\|z\|^3).
\tag{17}
\]

The finite exponential sums are analytic near zero, so the remainder estimate is uniform over centered directions. If c>0, choose a ball where the remainder's absolute value is at most c||z||²/4. This gives strict positivity except at z=0; negative c gives the reversed conclusion. A box of sufficiently small log-width has small centered norm, since ||y−\bar y1||≤√N(range y). For the negative case, choose nonconstant points of any interval arbitrarily near 1. Their centered log vectors are nonzero and arbitrarily small; invariance under scalar shifts makes (17) applicable also on a one-sided interval. ∎

For Theorem 2, exact coefficient sums give c_λ=7/3 and c_μ=25/12, hence c=1/4. In particular, the quadratic term of log R on the centered plane is ||z||²/8. This independently explains the local direction of the exact finite-width theorem. These moment values are checked by the finite coefficient script; the entire sharp theorem rests on the explicit polynomial certificate rather than a truncated Taylor expansion.

## 6. Computational scope and limits

An exploratory installed SymPy session expanded (10), factored the two-valued specialization, and converted the degree-five middle-coordinate polynomial to its Bernstein basis. No source-author code was run. The final checker uses only Python's standard library (integer/Fraction polynomial arithmetic and exact binomial coefficients). It independently constructs the complete homogeneous polynomials and both Schur polynomials, confirms their positive coefficients, dimensions and homogeneity, verifies (11)–(13) coefficientwise, checks all rational positivity bounds and moment values, and verifies the N=2 threshold factorization. It also checks selected exact rational valid/invalid sample points as diagnostics.

The checker is a finite certificate checker, not a test of all partitions or all boxes. It does not prove the analytic hyperbolic shape lemma, the general Taylor statements, or source theorems. Those are supplied as written arguments above. No random grid, floating-point sign decision, numerical optimizer, source-author program, or quantifier-elimination routine is used as proof. The displayed decimal root is only descriptive; rational brackets and monotonicity prove its existence and location.

The full arbitrary-N bounded-interval problem is not solved here. Even arbitrary pairs in N=3 are not classified. Intervals not having 1 in their closure are not covered by Theorem 1's minimizer-at-1 formulation; Theorem 2's special-pair comparison is nevertheless valid for every interval. The original imported results are identified as such. None of the results is claimed to be novel, and a limited literature check cannot establish priority.

## References

[1] A. Khare and T. Tao, *On the sign patterns of entrywise positivity preservers in fixed dimension*, American Journal of Mathematics 143 (2021), 1863–1929. https://arxiv.org/abs/1708.05197v6 ; https://doi.org/10.1353/ajm.2021.0049 . The proof discussion here uses Theorem 10.1, its proof, Remark 10.2, and Corollary 10.4, on PDF pages 51–54. Equation (5.1), PDF page 23, was inspected for the generalized-Vandermonde context; our new certificate and covariance proof do not require that integral identity.

[2] A. Belton, D. Guillot, A. Khare and M. Putinar, *Matrix positivity preservers in fixed dimension. II: positive definiteness and strict monotonicity of Schur function ratios*, arXiv:2310.18020v1. https://arxiv.org/abs/2310.18020 . Theorems 1.4–1.5 and surrounding statements inspected; their full proofs were not audited here.

[3] H. Chen, A. Khare and S. Sahi, *Majorization via positivity of Jack and Macdonald polynomial differences*, arXiv:2509.19649v2, revised February 2026. https://arxiv.org/abs/2509.19649 . Introductory scope and current public metadata inspected; the paper was not fully proof-audited here.

[4] AIM Problem Lists, *Theory and applications of total positivity*, Problem 1.45. http://aimpl.org/totalpos/1/ . The retained archived problem statement was inspected in the source-screen input. A fresh direct request during this attempt returned a 502 error; that failure does not affect the retained problem wording.
