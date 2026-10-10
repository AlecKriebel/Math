# Bounded-polynomial truncations: scope, five approaches, and remaining obstruction

## Disposition

**Partial progress; the full term-count extremal question is not solved.** Five mathematical approaches were completed. Literature retrieval, numerical discovery, implementation, and packaging are not counted as mathematical approaches. No novelty claim is made for elementary bounds or the special-case identities below.

The main useful correction to the old literature baseline is a published 2026 paper by Marc Technau, DOI [10.1017/fms.2026.10213](https://doi.org/10.1017/fms.2026.10213). It studies the degree-bounded version. Its Theorem 2.1 gives a relative error bounded by a constant times n^3 exp(-d/(5n)) when approximating the Landau constant for the first n+1 coefficients. Its introduction records Newman's exact middle-cut formula, with a 1979 erratum. These results do not supply an arbitrary-support, term-count theorem. General exact degree-bounded constants also remain undetermined there. The primary source [Hayman and Lingham, Problem 4.3](https://arxiv.org/abs/1809.07200) provides no explicit degree convention or further quantifiers. The original Newman paper and erratum were bibliographically verified through Technau; their full texts were not retrieved. Source search is bounded evidence, not a proof of absence of other literature.

## 1. Three quantities that must not be identified

Write T={z:|z|=1}, and use the supremum norm on T. Complex coefficients are permitted throughout. An analytic polynomial has the same supremum over T and the closed unit disk, by the maximum principle.

For d>=1 and 1<=k<=d, define

    A(d,k) = max { ||sum_{j=0}^{k-1} a_j z^j||_T :
                    P(z)=sum_{j=0}^{d-1} a_j z^j, ||P||_T<=1 }.

Zero coefficients are allowed. Thus d counts coefficient slots, the degree is at most d-1, and k counts slots in the truncation. In Technau's notation, A(d,k)=M_{k-1,d}. Rotation in z and multiplication by a scalar of modulus one reduce this norm maximization to maximizing the real part of sum_{j<k}a_j at z=1. Compactness gives a maximum.

For the term-count interpretation, take N distinct nonnegative integer exponents

    e_1 < ... < e_N,
    P(z)=sum_{j=1}^N a_j z^{e_j}.

Let C(N,k) be the supremum of the norm of the first k terms, over these exponents and nonzero coefficients, subject to ||P||_T<=1. The exponent e_N is unbounded. Put C_N=max_{1<=k<=N} C(N,k). Replacing nonzero coefficients by coefficients that may vanish does not change a fixed-support supremum: arbitrarily small perturbations, followed by normalization, fill the zeros. When discussing a fixed k, the coefficient slots on each side of the cut must be preserved during this approximation.

Finally, U_N allows an arbitrary subset of the N nonzero terms. Reordering terms before taking a partial sum leads to this quantity. It is a different extremal problem.

No assertion in the source justifies substituting d=N for an arbitrary N-term polynomial. Our strongest degree-bounded result below is therefore explicitly a specialization, not a solution of C_N.

For any fixed support and cut, real coefficients give the same supremum as complex coefficients for the full-circle norm. First rotate the variable to move the chosen point to 1 and rotate the value to the positive real axis. Then replace P(z) by (P(z)+conjugate(P(conjugate(z))))/2. Its coefficients are real, its norm cannot increase, and the target value is unchanged. This does not replace the circle norm by the interval norm on [-1,1], which is a different problem.

If evaluation outside the disk were allowed with no bound on exponents, even z^M has unbounded values at any fixed radius greater than one. The results here concern the circle and disk only. Empty and complete truncations have norms 0 and at most 1 respectively.

## 2. Approach 1: coefficient-energy geometry, valid for arbitrary support

Let 1<=k<N, l=N-k, and fix z on T. Write A for the retained sum, B for its complement, and x=|A|. Parseval and Cauchy-Schwarz give

    |A|^2/k + |B|^2/l <= sum_j |a_j|^2 <= 1.

Also |A+B|<=1, so |B|>=max(x-1,0). If x>=1, these inequalities imply

    x^2/k + (x-1)^2/l <= 1,
    N x^2 - 2 k x + k(1-l) <= 0.

The larger root is

    R(N,k) = [k + sqrt(k(N-k)(N-1))]/N.

For k>=1, l>=1 one has R(N,k)>=1, so the same bound also covers x<1. Consequently

    C(N,k) <= R(N,k),
    C_N <= (1+sqrt(N))/2.

For the second inequality, put t=k/N. Then R=t+sqrt((N-1)t(1-t)); writing u=2t-1 and applying Cauchy-Schwarz in R^2 gives R<=(1+sqrt(N))/2. Complete truncations also satisfy this bound. This argument works for arbitrary subsets, not only initial exponents.

**Obstruction:** the estimate uses only total coefficient energy and one-point cancellation. It does not exploit the ordering of exponents. It cannot bridge the logarithmic lower bound below and its square-root upper bound. We do not claim it is the optimal bound.

## 3. Approach 2: analytic kernel factorization and the finite-degree gap

For r>=0 put c_j=binom(2j,j)/4^j and Q_r(z)=sum_{j=0}^r c_j z^j. The power series identity (1-z)^(-1/2)^2=(1-z)^(-1) shows that every coefficient of Q_r^2 through degree r equals 1. With normalized arc measure dm,

    sum_{j=0}^r a_j = integral_T P(z) z^(-r) Q_r(z)^2 dm(z).

There are no negative exponents in P, so only coefficients of Q_r^2 through degree r contribute to this constant term. It follows that

    |sum_{j=0}^r a_j| <= integral_T |Q_r(z)|^2 dm(z)
                         = G_r := sum_{j=0}^r c_j^2.

Thus A(d,k)<=G_{k-1}. Stirling's estimate gives c_j^2=1/(pi j)+O(j^-2), hence G_r=(1/pi)log(r+1)+O(1), with an absolute constant.

If r>=1 and P is a finite polynomial, equality in the integral bound would imply |P|=1 on T except possibly at the finitely many zeros of Q_r, and hence everywhere by continuity. Such a polynomial is a monomial: if its lowest and highest nonzero powers differ, the corresponding outermost Fourier coefficient of |P|^2 is nonzero. A monomial has truncation value at most 1, whereas G_r>1. Compactness therefore yields the strict inequality A(d,k)<G_{k-1} for k>=2. This strictness is not an explicit uniform gap in d.

Reverse the coefficients of P and apply the same argument to its last l=d-k slots. Since the retained sum equals the full sum minus that tail,

    A(d,k) <= min(G_{k-1}, 1+G_{d-k-1})       (1<=k<d).

For a sparse polynomial this argument involves the exponent cutoff, after any initial monomial factor has been removed. The number of retained nonzero terms is not the cutoff exponent. Replacing that exponent by k-1 would be invalid.

**Obstruction:** the sharp analytic-function bound has a rational, rather than polynomial, extremizer in nontrivial cases. Kernel factorization gives a bound and finite-degree strictness, but not the general exact A(d,k), and not a logarithmic term-count upper bound.

## 4. Approach 3: positive-kernel construction and uniform dense growth

This construction supplies actual bounded polynomials, avoiding numerical norm sampling. Let h(t)=sign(sin t), with any values of magnitude at most one at its discontinuities. Its Fourier sine coefficients are obtained by integrating on (0,pi) and (pi,2pi): the coefficient is 4/(pi j) for odd j and zero for even j.

The Fejer kernel

    K_s(t) = |sum_{r=0}^s exp(i r t)|^2/(s+1)

is nonnegative and has normalized integral 1. Its Fourier multiplier at j is 1-|j|/(s+1) for |j|<=s. Consequently its convolution with h has magnitude at most 1 everywhere. Multiplying this convolution by i z^s, z=exp(it), gives the polynomial

    F_s(z) = (2/pi) sum_{1<=j<=s, j odd}
                 (1-j/(s+1)) (z^(s+j)-z^(s-j))/j,

of degree at most 2s, with real coefficients and ||F_s||_T<=1. For s>=1, the sum of coefficients at powers below s (or at powers at most s, since the central coefficient is zero) is

    -B_s,  B_s=(2/pi) sum_{1<=j<=s, j odd} (1-j/(s+1))/j.

The odd reciprocal sum equals H_s-(1/2)H_floor(s/2), while the correction term equals ceil(s/2)/(s+1). Therefore

    B_s=(1/pi) log(s+1)+O(1)

with an absolute error bound. This is an existence proof on the entire circle, not a grid test.

Now let 1<=k<d, m=min(k,d-k), and s=m-1. For s>=1 use z^(k-m)F_s(z). Its exponents are nonnegative and at most k+m-2<=d-2. Its first k coefficient slots include precisely the negative half of the construction. Hence A(d,k)>=B_{m-1}. The constant polynomial separately gives A(d,k)>=1. Combining with Approach 2 yields

    A(d,k) = (1/pi) log(min(k,d-k)) + O(1),    1<=k<d,

uniformly in both integers, with an absolute O(1). Also A(d,d)=1. In particular max_k A(d,k)=(1/pi)log d+O(1) as d tends to infinity. These are growth statements, not exact finite-parameter formulas or a novelty claim. A similar lower bound also follows by embedding and shifting the known middle-cut family, but the proof here is independent of that family's sharp formula.

For even N, choose s=N-1. There are exactly N nonzero terms in F_s, with N/2 in each half. Thus C_N>=B_{N-1}. Odd N follow in the supremum by adding one arbitrarily small higher-degree term and rescaling. We obtain the rigorously justified range

    (1/pi)log N - O(1) <= C_N <= (1+sqrt(N))/2.

**Obstruction:** the construction proves a lower bound, not optimality among arbitrary sparse supports. The matching dense upper bound relies on degree, not term count. The report leaves the gap above open.

## 5. Approach 4: exact two-node duality and a special-case certificate

For a polynomial of degree at most two, the sharp value for its first two coefficients is

    A(3,2)=2/sqrt(3).

Here is a full complex-coefficient proof. Let omega=(1+i sqrt(3))/2 and u=1/2-i sqrt(3)/6. Direct algebra gives

    u + conjugate(u)=1,
    u omega + conjugate(u) conjugate(omega)=1,
    u omega^2 + conjugate(u) conjugate(omega)^2=0.

Therefore a_0+a_1=u P(omega)+conjugate(u)P(conjugate(omega)), and its modulus is at most 2|u|=2/sqrt(3).

For the lower bound take

    P_*(z)=(2+4z-z^2)/(3 sqrt(3)).

Writing x=cos t, exact expansion gives

    27-|2+4exp(it)-exp(2it)|^2 = 8(x-1/2)^2 >=0.

Thus ||P_*||_T=1 and a_0+a_1=2/sqrt(3). The same value applies to a fixed arithmetic-progression triple of exponents, by removing its initial monomial and substituting z^q. No claim is made for all possible three-term supports. The identity can be checked over rational arithmetic plus the formal element i sqrt(3); the verifier does so exactly.

More generally, any fixed support has a finite-dimensional convex norm problem. Point-evaluation dual certificates with coefficients reproducing the selected-coefficient functional certify upper bounds. Feasible polynomials with exact nonnegative trigonometric slack certify lower bounds. This perspective motivated the quadratic computation, whose proof above no longer depends on numerical optimization.

**Obstruction:** for arbitrary d,k one must find appropriate contact points and a globally bounded extremizing polynomial with matching dual value. Solving finitely many such problems cannot control unbounded support exponents in C_N.

## 6. Approach 5: complementary-polynomial recursion and the ordering barrier

To test whether square-root growth might come merely from selecting favorable signs, define R_0=S_0=1 and recursively

    R_{r+1}=R_r+z^(2^r) S_r,
    S_{r+1}=R_r-z^(2^r) S_r.

The two blocks do not overlap; both polynomials have N=2^r coefficients in {+1,-1}. On T,

    |R_r|^2+|S_r|^2=2N.

The equality follows inductively from |a+b|^2+|a-b|^2=2(|a|^2+|b|^2). Normalize R_r by sqrt(2N). Its circle norm is at most one. The recurrence at z=1 gives R_r(1)>=0 (successive pairs are (2^h,2^h) and (2^(h+1),0)). At least N/2 coefficients are positive. Selecting exactly those terms and evaluating at 1 gives a value at least sqrt(N)/(2sqrt(2)).

Together with Approach 1, this proves U_N has square-root order, first for powers of two and then for all N by choosing the preceding power of two, perturbing with additional nonzero terms, and rescaling. The constants remain absolute.

However, the selected positive coefficients are generally scattered among the exponents. They are not an initial segment in increasing exponent order. Reordering them would change the problem. This construction cannot be used as a square-root lower bound for C_N.

**Obstruction:** favorable signs alone do not produce a large naturally ordered truncation. No argument here converts this subset witness into an initial-exponent witness while preserving its norm and number of terms.

## 7. Exact remaining questions

1. Under the increasing-exponent, nonzero-term interpretation, determine the sharp growth of C_N, or C(N,k). This packet provides a logarithmic lower bound and a square-root upper bound but does not show these exhaust the literature or close the gap.
2. Under the dense coefficient-slot interpretation, the leading logarithmic growth is established, but the general exact two-parameter A(d,k) is not determined here. Endpoint cases and A(3,2) are proved; known central-case formulas are attributed to the literature.
3. The source's short formulation does not resolve these conventions. A correct status update must preserve that uncertainty rather than silently strengthen the hypotheses or replace the requested extremum.

## 8. Verification boundary

The frozen verifier uses Python's standard library and exact rational/integer arithmetic. It checks the kernel convolution identities, the explicit Fejer coefficient/support/cut identities, the coefficient-energy discriminant identity, the full quadratic primal/dual certificate, and complementary-polynomial autocorrelation identities. Every input integer is required to have exact Python type int; booleans and floating-point numbers are rejected. JSON duplicate keys and non-finite constants are rejected.

The program is not a proof assistant and does not mechanically establish the analytic integral arguments, uniform asymptotics, or the unresolved conclusion. Those depend on the explicit proofs and scope qualifications above. Finite identity checks are not evidence that the original problem is solved. External file hashes authenticate a chosen snapshot only when their pins are independently trusted; they do not establish truth or novelty.
