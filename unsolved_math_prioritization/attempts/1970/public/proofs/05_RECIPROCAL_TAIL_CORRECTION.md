# Auxiliary reciprocal-tail remainder correction

## Scope and inspected source

This authored addendum is a new 15 October 2026 reconstruction. It makes a narrow statement about one remainder estimate, not an assessment of the whole paper or a solution of EP168.

Inspected source: Nikola Veselinov, *Extremal densities for forbidden configurations in S-smooth numbers*, arXiv:2604.15515v1, dated 16 April 2026. Public version-specific PDF: https://arxiv.org/pdf/2604.15515v1 . The retrieved PDF has 484,220 bytes and SHA-256 68e3b58de8d2bf8f4e5fb48560f2c43e489d7979e7e0f8c44ed2ddf1c7adbb14. Its printed page 10 was inspected visually as well as through extracted text.

For two primes S={2,3}, Proposition 4.3 on printed page 10 asserts the specialization

T(X) = log X / [(log 2)(log 3) X] + O(1/X),

where T(X)=sum_{2^a 3^b>X} 2^(-a)3^(-b), a,b>=0. The specific O(1/X) remainder is false. The proof below establishes that

X T(X) - log X / [(log 2)(log 3)]

is unbounded in absolute value. This does not rule out a weaker asymptotic with the same leading term.

The source's exact reciprocal-tail identity in Corollary 6.1 (printed page 12), and the elementary bound T(X)=O(log X/X), remain valid and sufficient for the downstream density-series and nested-bound arguments discussed below.

## 1. Exact identity and a sufficient upper bound

Put m=floor(log_2 X) and b_a=1+floor(log_3(X/2^a)) for 0<=a<=m. Splitting the sum by a gives the exact identity

T(X) = (3/2) sum_{a=0}^m 1/(2^a 3^(b_a)) + 3/2^(m+1).       (1.1)

Indeed, for a<=m the allowed b are b>=b_a, whose geometric sum is (3/2)3^(-b_a). For a>m every b>=0 is allowed, giving the last term. The strict cutoff in T corresponds to the added one in b_a, including when X/2^a is an exact power of 3.

Since X<2^a3^(b_a)<=3X and X<2^(m+1), (1.1) implies the explicit estimate

0 < T(X) < 3(m+3)/(2X), for every X>=1.                       (1.2)

Thus T(X)=O(log X/X). No sharp remainder estimate is needed for this conclusion.

## 2. Laplace transform of the alleged bounded remainder

Write A=log 2 and B=log 3. For u>=0 define

H(u)=exp(u) T(exp(u)),
R(u)=H(u)-u/(AB),
P(s)=1/[(1-exp(-As))(1-exp(-Bs))], Re(s)>0.

The estimate in (1.2) gives H(u)=O(u+1), so these Laplace transforms converge absolutely for Re(s)>0. With lambda=aA+bB,

H(u)=sum_{a,b>=0} exp(u-lambda) 1_{0<=u<lambda}.

Absolute convergence justifies integrating this expression term by term. For s!=1,

integral_0^infinity H(u) exp(-su)du
 = sum_{a,b>=0} [exp(-s lambda)-exp(-lambda)]/(1-s)
 = [P(s)-P(1)]/(1-s).                                        (2.1)

The apparent singularity at s=1 is removable. In particular P(1)=3. Subtracting the transform of u/(AB) gives

F_R(s)=[P(s)-P(1)]/(1-s)-1/(AB s^2).                         (2.2)

If the source's O(1/X) estimate held, then R(u) would be bounded for all sufficiently large u. It is also bounded on each finite interval, so R would be bounded on all [0,infinity).

## 3. Nondecaying Abel coefficients

For n>=1 put t_n=2*pi*n/A. At s=i*t_n the first factor of P has a simple zero. The second does not vanish, because B/A is irrational: simultaneous vanishing would imply 3^n=2^k for integers n>=1 and k. The factors 1-s and s^2 are also nonzero at i*t_n. Therefore (2.2) has Abel coefficient

c_n = lim_{sigma down to 0} sigma F_R(sigma+i*t_n)
    = 1/[A(1-i*t_n)(1-exp(-i*t_n B))].                       (3.1)

Let theta=B/A. Infinitely many continued-fraction denominators n of theta satisfy ||n theta||<1/n. For these n,

|1-exp(-i*t_n B)| = |1-exp(-2*pi*i*n theta)| <= 2*pi/n.

Moreover

A |1-i*t_n| = sqrt(A^2+4*pi^2*n^2)
             <= n sqrt(A^2+4*pi^2).

It follows that infinitely many distinct c_n satisfy the fixed positive lower bound

|c_n| >= 1/[2*pi*sqrt(A^2+4*pi^2)].                           (3.2)

## 4. Boundedness would contradict the Abel-Bessel inequality

For completeness, the required elementary lemma is stated and proved here.

Suppose g is a bounded complex function on [0,infinity), |g|<=K, and distinct real frequencies t_j have Abel coefficients

a_j=lim_{sigma down to 0} integral_0^infinity g(u)exp(-i*t_j*u)
                                      sigma exp(-sigma*u)du.

For any finite set of these frequencies, let Q(u)=sum_j a_j exp(i*t_j*u). With the probability measure dmu_sigma=sigma exp(-sigma*u)du, distinct exponential frequencies become orthogonal in the limit, because

integral exp(i*(t_j-t_k)*u)dmu_sigma
 = sigma/[sigma-i*(t_j-t_k)]
 -> 1 if j=k, and 0 otherwise.

Expanding integral |g-Q|^2 dmu_sigma>=0 gives, after taking limits in the Q and mixed terms and using integral |g|^2 dmu_sigma<=K^2,

sum_j |a_j|^2 <= K^2.                                       (4.1)

The g-norm itself need not have a limit. Its uniform bound suffices.

Applying this lemma to a hypothetically bounded R, formula (3.1) supplies its Abel coefficients, while (3.2) gives infinitely many coefficients bounded away from zero. A sufficiently large finite subset contradicts (4.1). Hence R is unbounded and the claimed O(1/X) remainder in Proposition 4.3 fails for S={2,3}.

## 5. Narrow impact on the density checkpoint

The source's partial-summation proof on page 10 carries an error of order (log X)^(r-1)/X before its final cancellation. Canceling the explicitly displayed leading polynomial terms does not, on its own, reduce that existing error to order (log X)^(r-2)/X. For r=2, the obstruction above shows the sharper stated error is genuinely false, not merely unsupported by that calculation.

The following statements are not affected by this correction:

1. The exact recursion in Proposition 4.2 and its two-prime specialization (1.1), reproduced in Corollary 6.1.
2. Absolute convergence of the reciprocal sum: sum_{a,b>=0}2^(-a)3^(-b)=3.
3. The finite-component decomposition and alpha=(1/3)sum_k delta_f(d_k)/d_k.
4. Exact nested bounds L_k<=alpha<=L_k+(1/3)T(d_k), and their exact computable widths.
5. The weaker estimate N*T(N)=O(log N). Together with the O(Psi(N))=O((log N)^2) component-count error, it still supplies F(N)=alpha*N+O((log N)^2) in the two-prime case.

Thus this auxiliary remainder correction does not invalidate the density series or the reconstructed arithmetic checkpoint. No claim is made here about rationality of alpha, candidate optimality, the actual optimizer's binary output, or other propositions outside this stated scope.

## 6. Verification artifacts

`checks/check_tail.py` compares (1.1), in exact Fraction arithmetic, with the independent identity T(X)=3-sum_{d<=X}1/d at fixed small cutoffs and their one-sided rational neighbors. It checks (1.2) at those same points. These finite tests verify implementation and strict-cutoff conventions; the failure of the O(1/X) remainder is proved analytically in Sections 2-4 and is not inferred from a finite experiment.
