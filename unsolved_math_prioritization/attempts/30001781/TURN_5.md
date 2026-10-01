# Turn 5: the exact one-row tail bottleneck and a conditional moment route

2026-10-01. Fifth substantive author turn. All original rows remain independent, centered, isotropic and log-concave. This turn gives an exact reduction for the k=1 boundary and tests the correlated-column route; it does not establish the general sharp matrix estimate. The original is unresolved after five substantive turns.

## 1. Top-m norms: a first moment is easier than the needed uniform tail

For 1<=m<=N write

    Z=||X||_(m)=sup_{y in U_m(N)} |<X,y>|,
    a=sqrt(m) log(3N/m).

Here U_m consists of m-sparse Euclidean unit vectors. Z is a norm of X and a>=1. For every centered isotropic log-concave X,

    E Z <= C a.                                              (1.1)

Indeed its individual coordinates have uniform subexponential tails. Apply the deterministic tail-count inequality and integral calculation in turn1 §1 directly to X; coordinate independence is unnecessary. This even bounds E Z^2 by C a^2.

For a matrix with independent copies of X as rows, however,

    A_(1,m)=max_{1<=i<=n} Z_i.                                (1.2)

A first-moment estimate does not itself control this maximum at a+log(en). The following proposition states the missing tail issue exactly without assigning an unstated meaning to the source's qualitative phrase 'high probability'.

## 2. Uniform maximum medians, shifted exponential tails and moments

Consider any family of nonnegative random variables Z, each equipped with a number a>=1. The following three properties are equivalent, with constants changed by universal factors:

(Q) There is C_Q independent of the family member and n such that, for every n>=1 and iid copies Z_1,...,Z_n,

    P(max_i Z_i <= C_Q[a+log(en)]) >= 1/2.

(T) There is C_T independent of the family member such that, for all t>=0,

    P(Z>C_T[a+t]) <= 2exp(-t).

(M) There is C_M independent of the family member such that, for all real p>=1,

    (E Z^p)^(1/p) <= C_M(a+p).

These are quantitative distribution properties. No log-concavity is needed for their equivalence.

Proof of Q=>T. Given t>=0, put n=floor(exp(t)); then n>=exp(t)/2. Define q=P(Z>C_Q[a+1+t]). Since log(en)<=1+t, Q implies

    (1-q)^n >= 1/2.

Therefore q<=1-2^(-1/n)<=log(2)/n<=2log(2)exp(-t). Because a>=1, a+1+t<=2(a+t). Taking C_T=2C_Q proves T (with the harmless prefactor2). This argument uses iid copies only to turn the probability of a maximum into an exact power.

Proof of T=>Q. Apply T to each of n copies with t=log(4n). The union bound gives probability at most1/2 of an exceedance above C_T[a+log(4n)]. This threshold is at most a universal constant times a+log(en). Independence is not needed in this direction.

Proof of M=>T. For p>=1, Markov gives

    P(Z>e C_M(a+p))<=exp(-p).

For t>=1 take p=t. For 0<=t<=log2 the desired upper bound2exp(-t) is at least1. For log2<t<1, apply the preceding estimate with p=1 and enlarge C_T so that C_T(a+t)>=e C_M(a+1). Then exp(-1)<=2exp(-t). Thus T holds on the entire range.

Proof of T=>M. Put W=(Z-C_T a)_+. Then P(W>C_T t)<=min(1,2exp(-t)). By the tail integral,

    E W^p <= 2 C_T^p Gamma(p+1).

The elementary bound Gamma(p+1)^(1/p)<=C p for p>=1 gives ||W||_p<=C' C_T p. Since Z<=C_T a+W, Minkowski proves M. This includes all real p>=1, not only integers.

Thus a uniform sharp median estimate for the k=1 matrix case over all sample sizes would force the one-row dimension-free bound M with a=sqrt(m)log(3N/m). Conversely that one-row bound uniformly for every allowed row law gives the sharp k=1 matrix estimate, including nonidentically distributed rows: T and a union bound yield

    P(A_(1,m)>C[a+log(2n)+t])<=exp(-t), t>=0.              (2.1)

The Q property is a deliberately precise necessary benchmark. If a proposed interpretation of 'high probability' guaranteed only an unspecified restricted sample-size range, one could not use Q outside that range. The original report does not state such a restriction, but this packet does not retrofit a quantitative theorem into its wording.

## 3. A sufficient weak–strong comparison, explicitly conditional

A known general conjectural mechanism is the weak–strong moment inequality. Latała's primary survey *On some problems concerning log-concave random vectors*, §3, Conjecture12 (PDF p.7), states the relevant proposed inequality for arbitrary norms. Applied only to the top-m norm it would read

    || ||X||_(m) ||_Lp
      <= C [E||X||_(m) + sup_{y in conv U_m(N)} ||<X,y>||_Lp].    (3.1)

This application uses the correct dual unit ball. The top-m norm is the support function of the compact symmetric convex body conv U_m(N); hence the unit ball of its dual norm is exactly conv U_m(N). This body is contained in the Euclidean unit ball. Isotropy and the one-dimensional log-concave moment estimate therefore give

    sup_{y in conv U_m(N)} ||<X,y>||_Lp <= C p, p>=1.

At y=0 the assertion is trivial; for nonzero y use the variance-one projection <X,y>/|y| and |y|<=1. Combining this with (1.1) and the hypothetical (3.1) gives M and hence (2.1).

Equation (3.1) has not been proved in this attempt. The established Euclidean moment theorem does not automatically apply to the maximum of all m-coordinate Euclidean projections. Nor does the established ell_r inequality with a constant proportional to r give a dimension-free bound after an ell_infinity embedding. The same survey, Theorem14 and Remark16, explicitly retains the r and distortion factors. Its Theorem18 for coordinate maxima of an isotropic vector cannot simply be applied to all sparse linear projections: their larger joint vector need not be isotropic, or even have full-rank covariance.

We use that survey to identify the exact hypothesis, not to certify its current global open/closed status. The proof here is conditional and remains valid independently of later developments. No abstract-only recent result is used as a theorem input.

## 4. Why this is still short of the full correlated multiscale step

For general k, A_(k,m) also optimizes over every row coefficient vector u with |u|=1 and support at most k. For each fixed u, the sum Y_u=sum_i u_i X_i is centered isotropic and log-concave. Even if (3.1) were proved for each Y_u, a direct union bound over exponentially many u-net points would add a cost of order k log(en/k), rather than the desired sqrt(k)log(3n/k). Thus the preceding conditional k=1 result is not silently promoted to the full k>1 result. A uniform comparison or chaining estimate respecting the dependence between those sums is still needed.

The full author version of Adamczak–Latała–Litvak–Pajor–Tomczak-Jaegermann's published2014 paper gives much more sophisticated correlated projection estimates. Its Theorem4.3 has different regimes according to the maximal coefficient b=||u||_infinity, including a sqrt(log(e^2 b^2 m)) denominator in the large-b regime. The multiscale proof of Theorem5.1 produces the extra sqrt(loglog(3m)) in the column term. None of the elementary net or flat-vector arguments of turns3–4 removes that factor. The attempt does not improve their known full general-row theorem.

Potential artificial examples based on random permutations and signs of a fixed sparse profile cannot be admitted without checking log-concavity. A distribution on a finite union of distinct rays generally has nonconvex support, whereas every log-concave probability has convex support. Likewise, a mixture of log-concave laws is not automatically log-concave. We found no admissible stochastic counterexample. The deterministic harmonic profile from turn3 only obstructs one flat-atomic proof method.

## 5. Final disposition of the five-turn attempt

The completed positive partials are the common coisometric latent class (turn1), the asymmetric common-weight Dirichlet class (turn2), the flat-row test bound (turn3), and the full m=1 and row-dominated-regime estimates for arbitrary rows (turn4). This fifth turn gives the exact Q/T/M equivalence and the conditional weak–strong route for k=1.

The missing theorem is the sharp corrected maximal-submatrix bound for all independent isotropic log-concave row laws, without the extra known factors or a latent-representation restriction. No proof or counterexample to that original statement has been obtained. The final proposed campaign status is **unsolved, 5/5 substantive author turns**, subject to a separate full review of every retained partial. Source validation, independent review and packaging do not count as additional research turns.
