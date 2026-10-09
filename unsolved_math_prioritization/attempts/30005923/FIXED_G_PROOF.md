# Repaired fixed-variable-count proof reconstruction

This is an authored verification of the argument of Jury, van Rensburg and Roman, *Free versions of the strong Szegő limit theorem*, arXiv:2607.25980v1, Sections 2–6. Its corrections are itemized in `AUDIT_REPORT.md`. All tuple lengths and coefficient matrix sizes in this proof are finite and fixed. No claim of a new result, of an all-variable-count bound, or of journal acceptance is made.

## A. Notation and established inputs

Let `U_1,...,U_g` be independent Haar probability-distributed `N` by `N` unitaries. Put

`T_X(U)=sum_j X_j tensor U_j`, `L_X(U)=I+T_X(U)`,

`||X||_row=||sum_j X_j X_j*||^(1/2)`.

All finite-matrix traces below are unnormalized unless a factor is displayed. Let `u_j` be the canonical free Haar unitaries with trace `tau`. On `M_k tensor L(F_g)` use `tau_k=(Tr_k/k) tensor tau`.

The proof uses these established inputs:

1. **Free-group norm estimate.** If `T=sum X_j tensor u_j`, define `R_n=||sum_|w|=n X^w (X^w)*||^(1/2)` and `C_n=||sum_|w|=n (X^w)* X^w||^(1/2)`, with `R_0=C_0=1`. The Buchholz/Haagerup–Pisier estimate used in Proposition 5.3 gives

   `max(R_n,C_n) <= ||T^n|| <= (n+1) max_0<=s<=n C_s R_(n-s)`.

   The middle block at split `s` factors as the column of length-`s` products times the row of length-`n-s` products, which explains the upper product. This is a cited free-group operator norm theorem, not a new estimate of this audit.
2. **Concentration.** On `U(N)^g` with the square-sum Hilbert–Schmidt metric, a real `L sqrt(N)`-Lipschitz function `F` obeys

   `P(F-EF>t) <= exp(-t^2/(12 L^2))`.

   This is Meckes–Meckes, *Spectral measures of powers of random matrices*, Corollary 17, arXiv:1210.2681v3. The constant is independent of the number of factors; the particular value of `L` still must be controlled.
3. **Smooth trace approximation.** For a fixed-alphabet bounded-degree bounded-coefficient self-adjoint polynomial family `p_X` and a fixed bounded `C^6` function `f` with bounded derivatives,

   `| E [(kN)^(-1) Tr f(p_X(U))] - tau_k(f(p_X(u))) | <= C ||f||_(C^6) k^2 log(N)^2/N^2`, for `N>=2`,

   uniformly over that family. This is the specialization of Parraud, *On the operator norm of non-commutative polynomials in deterministic matrices and iid Haar unitary matrices*, arXiv:2005.13834v2, Theorem 1.1 and the uniformity remark after Theorem 4.1. Equivalently encode all `X_j` as bounded deterministic coefficient matrices in one fixed polynomial. No variable-count-independent constant is asserted by this specialization.
4. **Gaussian fluctuations.** Finite collections of unnormalized traces of nonempty cyclically reduced words in independent Haar unitaries converge to a centered complex Gaussian family; covariance pairs a word with inverse cyclic rotations, counting their multiplicities. This is Mingo–Śniady–Speicher, *Second order freeness and fluctuations of random matrices: II. Unitary random matrices*, arXiv:math/0405258v2, Theorem 3.13 and Corollary 3.14. We use only words containing exclusively positive letters, or exclusively inverse letters.
5. **Functional calculus.** A real scalar Lipschitz function is Lipschitz with the same constant for the Hilbert–Schmidt norm on self-adjoint matrices. Together with `|Tr M|<=sqrt(kN)||M||_HS`, this gives the trace estimates used below.

Primary links: <https://arxiv.org/pdf/2607.25980v1>, <https://arxiv.org/pdf/1210.2681v3>, <https://arxiv.org/pdf/2005.13834v2>, <https://arxiv.org/pdf/math/0405258v2>.

## B. Free spectral radius and logarithmic normalization

Define positive maps on `M_k` by `Phi(H)=sum X_j H X_j*` and `Psi(H)=sum X_j* H X_j`. A positive map has operator norm `||Phi(I)||`; thus `R_n^2=||Phi^n||` and `C_n^2=||Psi^n||`. With the Hilbert–Schmidt inner product, `Phi` and `Psi` are adjoints. They therefore have the same spectral radius. Vectorization identifies the matrix of `Phi`, up to an ordering of tensor factors, with `sum X_j tensor conjugate(X_j)`.

Let `s=rho(Phi)^(1/2)`. Gelfand's formula gives `R_n^(1/n), C_n^(1/n) -> s`. For each `epsilon>0`, there is an `M_epsilon` with `R_n,C_n<=M_epsilon(s+epsilon)^n` for all `n>=0`. The upper estimate in input A1 then gives

`||T_X(u)^n|| <= (n+1) M_epsilon^2 (s+epsilon)^n`.

Taking `n`th roots, and using the lower estimate in A1, proves

`rho(T_X(u)) = rho(sum X_j tensor conjugate(X_j))^(1/2)`.

If `||X||_row<=r<1`, then `rho(Phi)<=||Phi||<=r^2`, so `L_X(u)` is invertible. The closed row ball is compact in `M_k(C)^g`. Continuity of `L_X(u)` and of inversion on invertible elements gives numbers `0<a<=b<infinity`, uniform on this fixed ball, such that the spectrum of `p_X(u)=L_X(u)L_X(u)*` is in `[a,b]`.

Every strictly positive word in the free generators has trace zero. Consequently `tau_k(T_X(u)^n)=0` for `n>=1`. Since `rho(T_X(u))<1`, the norm-convergent logarithmic series has trace zero. The usual Fuglede–Kadison logarithm identity gives

`tau_k(log(L_X(u)L_X(u)*)) = 2 Re tau_k(log(I+T_X(u))) = 0`.

For completeness, the identity in this application can be verified without commuting the logarithms: along `L(t)=I+tT`, `0<=t<=1`, differentiate the trace of `log(L(t)L(t)*)`. Tracial differentiation gives `2 Re tau_k(T(I+tT)^(-1))`. The Neumann series converges uniformly on this segment, and each positive power has trace zero. Thus this derivative vanishes; its initial value is zero. In unnormalized trace form the corresponding FK identity has a factor `2k`, which does not affect the zero.

## C. Repaired positive-moment bound

Fix `g,k,r` as above. For arbitrary unitary matrices, the row-column factorization gives

`||T_X(U)|| <= ||[X_1 tensor I ... X_g tensor I]|| ||[I tensor U_1; ...; I tensor U_g]|| <= r sqrt(g)`.

Hence `0<=p_X(U)<=K I`, where `K=(1+r sqrt(g))^2`. The same norm ceiling holds for `p_X(u)`, so enlarge `[a,b]` if needed while keeping `0<a<=b<=K`.

Choose one real smooth function `f`, bounded with all derivatives bounded, which equals `log x` on `[a,b]` and majorizes `log x` for `0<x<=K`. Such a function exists: keep the logarithm above `a/2` through `K`, interpolate below `a/2` to a constant at least `log a`, and smoothly flatten after `K`. The interpolation can be a convex combination of `log x` and `log a`, supported away from zero; there the latter is the larger function. Put

`F_(N,X)(U)=Tr_(kN) f(p_X(U))`.

To verify its Lipschitz bound, first use the elementary row-operator estimate

`||T_X(U)-T_X(V)||_HS <= sqrt(k) r d(U,V)`.

Then

`||p_X(U)-p_X(V)||_HS <= 2(1+r sqrt(g)) sqrt(k) r d(U,V)`.

By A5 and the trace bound, `F_(N,X)` is `L sqrt(N)`-Lipschitz with

`L = 2 k r (1+r sqrt(g)) Lip(f|_[0,K])`,

uniform in `X,N`. Degenerate `r=0` gives determinant identically one and is handled directly.

By B, `tau_k(f(p_X(u)))=0`. The polynomial family `p_X` has degree at most two and bounded coefficients in a fixed alphabet. Input A3 consequently gives

`|E F_(N,X)| <= C ||f||_(C^6) k^3 log(N)^2/N`, for `N>=2`.

This is bounded over all `N>=2`; at `N=1`, `|F_(1,X)|<=k||f||_infinity`. Let `M` be a common bound for these means. Applying A2 to both signs yields

`P(|F_(N,X)|>t) <= 2 exp(-(t-M)^2/(12L^2))`, for `t>M`.

There are therefore positive constants `C,c`, depending on the fixed parameters and chosen `f`, with `P(|F_(N,X)|>t)<=C exp(-ct^2)` for every `t>0`, every `N`, and every tuple in the ball. This extension to small `t` only enlarges `C`.

At a zero eigenvalue interpret the determinant directly as zero; otherwise functional calculus and the scalar majorant give

`|det L_X(U)|^(2m) <= exp(m F_(N,X))`, for `m>0`.

The valid tail identity is

`E exp(m|F|) = 1 + m integral_0^infinity exp(mt) P(|F|>t) dt`.

The sub-Gaussian estimate makes its right side finite, uniformly in `X,N`. Thus

`sup_(N, ||X||_row<=r) E |det L_X(U)|^(2m) <= 1+mC integral_0^infinity exp(mt-ct^2)dt < infinity`.

For `m=0` take the zeroth moment to be one. This proves the repaired fixed-`g` proposition. The substitution `X=-A` gives the minus-pencil convention of OWR. Nothing in this argument bounds the resulting constants over all `g`.

## D. Covariance on a small coefficient neighborhood

First assume `max_j ||A_j||, max_j ||B_j|| <= q<1/g`. For positive words `w` of length `n`, set

`a_w=(-1)^(n+1) Tr_k(A^w)/n`, `b_w=(-1)^(n+1) Tr_l(B^w)/n`.

Then `sum_|w|=n |a_w| n <= k(gq)^n`, and likewise for `b_w`. Thus the weighted absolute sums are finite. The random variable

`G_N = sum_(w positive, nonempty) [a_w Tr_N(U^w) + conjugate(b_w) Tr_N((U^w)*)]`

is the sum of the two appropriate trace logarithms. In particular

`exp G_N = det L_A(U) conjugate(det L_B(U))`.

Its scalar coefficients are invariant under cyclic rotation because matrix trace is cyclic. All its nonempty words are exactly centered at finite `N`: replacing every `U_j` by `exp(i theta) U_j` multiplies each positive word trace of length `n` by `exp(i n theta)`, and each inverse word by the conjugate phase. Haar invariance forces the expectations to vanish. This argument does not apply to arbitrary mixed words and no such application is made.

For a finite word-length truncation, input A4 gives a Gaussian limit `Z`. The covariance rule and orbit-stabilizer counting yield

`(1/2) E Z^2 = sum_(w positive) a_w conjugate(b_w) |w|`.

Each cyclic orbit contributes its number of words times the number of rotations fixing one word; the product is the length. Hence periodic words have the correct multiplicity as well. A centered complex Gaussian satisfies `E exp Z=exp((1/2) E Z^2)`.

The trace-monomial Lipschitz bound and weighted absolute coefficient sum make every truncation `L sqrt(N)`-Lipschitz, with one `L`. Exact centering and concentration give uniform exponential integrability, so expectations of exponentials converge for each truncation.

Here is the passage to the full series. Let `H_(N,M)` be the truncation and `R_(N,M)=G_N-H_(N,M)`. Its weighted coefficient sum `delta_M` tends to zero, and it is centered and `delta_M sqrt(N)`-Lipschitz. Applying concentration to real and imaginary parts gives

`P(|R_(N,M)|>t) <= 4 exp(-t^2/(24 delta_M^2))`.

Cauchy–Schwarz bounds `E|exp G_N-exp H_(N,M)|` by

`(E|exp(2G_N)|)^(1/2) (E|1-exp(-R_(N,M))|^2)^(1/2)`.

The first factor is uniformly bounded. For the second, `|1-exp(-z)|<=exp(|z|)-1`, so the tail formula bounds its square by

`8 integral_0^infinity exp(t)(exp(t)-1) exp(-t^2/(24 delta_M^2))dt`,

which tends to zero by dominated convergence, uniformly in `N`. The factor 8 includes the derivative of `(exp(t)-1)^2`. The limiting covariance series is absolutely convergent by the same coefficient bounds. Thus the finite-truncation calculation passes to the full pencil logarithms.

Finally put `S=sum_j A_j tensor conjugate(B_j)`. Expansion of `S^n` gives

`sum_(w positive) a_w conjugate(b_w)|w| = sum_(n>=1) Tr_(kl)(S^n)/n = -Tr_(kl) log(I-S)`.

The norm of `S` is below one on this small neighborhood, so these series are norm-convergent. We obtain the covariance limit `det(I-S)^(-1)` there.

## E. Exact Montel continuation on the product row ball

Let `Omega_(g,k)={A in M_k(C)^g: ||A||_row<1}` and define `Omega_(g,l)` similarly. These are open convex domains in finite-dimensional complex vector spaces. Introduce independent holomorphic variables `A,Z` and the polynomials

`H_N(A,Z) = E [det(I+sum A_j tensor U_j) det(I+sum Z_j tensor conjugate(U_j))]`.

At `Z=conjugate(B)` this is exactly the desired covariance. For every compact subset of `Omega_(g,k) x Omega_(g,l)`, its two projections lie in closed row balls of radii `r_A,r_Z<1`. Cauchy–Schwarz and C with `m=1` give a common bound for `|H_N|` on that compact subset. Thus this family is locally bounded and normal on the product domain.

We also need the prospective limit to be holomorphic throughout this domain, not just near zero. Write `S(A,Z)=sum A_j tensor Z_j`. If the two row norms are `a,b<1`, then

`sum_|w|=n A^w(A^w)* <= a^(2n) I_k`.

For `Z`, the trace of the analogous row sum equals the trace of its column sum, so

`||sum_|w|=n (Z^w)* Z^w|| <= l b^(2n)`.

The operator row-column Cauchy–Schwarz inequality yields

`||S(A,Z)^n|| <= sqrt(l) (ab)^n`.

It follows that `rho(S(A,Z))<=ab<1`. Hence `H(A,Z)=det(I-S(A,Z))^(-1)` is holomorphic on the entire product domain.

Now take any subsequence of `H_N`. Normality supplies a further subsequence converging uniformly on compact subsets to a holomorphic function `h`. Section D proves pointwise convergence of the original sequence to `H` on a nonempty open neighborhood of `(0,0)` in the product domain. Therefore `h=H` there. The identity theorem on the connected product domain implies `h=H` everywhere.

This proves convergence of the entire sequence, not just a subsequence: if locally uniform convergence failed, there would be a compact set, an `epsilon>0`, and a subsequence whose supremum distance from `H` on that compact set is at least `epsilon`. A normally convergent further subsequence would have limit `H`, a contradiction. This supplies both missing uniqueness and continuation details from the printed proof. Substituting `Z=conjugate(B)` finishes the identity for strict row contractions.

## F. Outer-radius extension and the stable-polynomial companion

Suppose `rho(Phi_A)<1`, with `Phi_A(Q)=sum A_j Q A_j*`. The convergent operator series

`P=sum_(n>=0) Phi_A^n(I)`

is positive definite and satisfies `Phi_A(P)=P-I`. For `Y_j=P^(-1/2) A_j P^(1/2)`,

`sum Y_j Y_j* = I-P^(-1)<I`.

Thus the tuple is simultaneously similar to a strict row contraction. Do this separately for `A` and `B`. Similarity preserves each pencil determinant and conjugates the mixed tensor sum by the corresponding tensor-product similarity. Section E therefore proves the limit on the full strict outer-radius domain stated in the intended Theorem 1.6. No assertion about limits uniform over varying similarity constants is necessary.

In OWR Conjecture 10 the supplied determinantal representations have strict row-contraction coefficients by the immediately preceding definition. Replacing both tuples by their negatives matches the plus convention here; their mixed tensor product is unchanged. Evaluating the given determinantal identities at the independent unitaries, which is valid because those identities hold at all matrix tuples, proves exactly

`lim_N integral det p(U) conjugate(det q(U)) dU = det(I-sum A_j tensor conjugate(B_j))^(-1)`.

This conclusion is for each fixed finite-variable polynomial pair and its finite-dimensional representations. It does not answer the constant-uniform-in-variable-count question of Conjecture 12, nor its optional optimal-constant and monotonicity suggestions.
