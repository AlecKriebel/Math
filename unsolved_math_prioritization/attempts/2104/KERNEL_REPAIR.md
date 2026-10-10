# Authored replacement for the Fourier normalization step

Source audited: Cheuk Fung (Joshua) Lau, *On the Number of Prime Factors of Consecutive Integers*, arXiv:2604.15042v2 (24 June 2026), https://arxiv.org/pdf/2604.15042v2, especially §§6.1–6.3, equations (6.5)–(6.9), PDF pp.20–29. This is an authored replacement argument, not text copied from the source and not an acceptance of every assertion in the paper.

## Result and scope

The absolute-value identity printed on p.28 is false. Nevertheless, the normalization (6.9) and the divisor-probability conclusion of Lemma 6.2 can be recovered from the exact Euler product in (6.5)/(6.6) by the argument below. It retains K=floor((log x)^(1/1000)), the fixed smoothing function, and the stated 8^s bound. Crucially, it does not replace the actual Euler-product correction by an arbitrary uniformly small function.

This replacement assumes the preceding exact Euler-product formula and its truncation error (6.6), whose local factors are explicitly displayed on p.23. It independently redoes the subsequent integration, rather than invoking (6.7)'s aggregate approximation. It does not certify other sections of the manuscript.

## 1. Notation and exact positive-shift identity

Write L=log x, H=L^0.2, K=floor(L^0.001), w=0.15 L, ell_k=log R_k, h=eta-hat, and

A(t,t')=(1+it)(1+it')/(2+i(t+t')),
c0=integral_[0,infinity) f(u)^2 du,
f(u)=d/du [exp(-u) eta(u)].

The source hypotheses imply h is even, nonnegative, continuous and rapidly decreasing; f is real. In particular c0>=1. Define the right translation T_a f(u)=f(u+a), a>=0, on L2([0,infinity)). It is a contraction.

For any finite set of nonnegative shifts a_1,...,a_m, put

U(t,t')=product_r (1-exp(-a_r(1+it)))(1-exp(-a_r(1+it'))),
Delta=product_r (I-T_{a_r}).

For arbitrary alpha,beta>=0, Laplace inversion and absolutely convergent Fourier integration give

integral_R2 A(t,t') U(t,t') exp(-alpha(1+it)-beta(1+it')) h(t)h(t') dt dt'
= integral_0^infinity (T_alpha Delta f)(u) (T_beta Delta f)(u) du.

Consequently its absolute value is at most 4^m c0. When alpha=beta=0, it is exactly ||Delta f||_2^2>=0. For m=0 and alpha=beta=0, the value is c0.

These identities follow by writing 1/(2+i(t+t')) as the integral of exp(-(2+i(t+t'))u) over u>=0 and observing that the one-variable Fourier integral with factor (1+it) is -f(u). All translation lengths are nonnegative, so the contraction estimate applies. The sign disappears in the paired product.

## 2. Single-coordinate factors, before collapsing the error

For each p>w and 1<=k<=K set a_{p,k}=log p / ell_k and

b_{p,k}(t_k,t'_k)
= [exp(-a_{p,k}(1+it_k))+exp(-a_{p,k}(1+it'_k))
   -exp(-a_{p,k}(2+i(t_k+t'_k)))]/p.

Define the exact, single-coordinate Euler product

g_k(t,t')=product_{p>w}(1-b_{p,k}(t,t')),
C_k=(W/phi(W))/ell_k.

Uniformly for |t|,|t'|<=H,

g_k(t,t')=C_k A(t,t') (1+O(L^(-0.7))).                 (R1)

Here and below implied constants can be fixed independently of k, K, j, s and A (the parameter called A in the manuscript).

For completeness, (R1) can be proved in one coordinate. Put z=(1+it)/ell_k and z'=(1+it')/ell_k. Since ell_k>=L^0.95/100, |z|+|z'|=O(L^(-0.75)). The product over all primes of

(1-p^(-1-z))(1-p^(-1-z'))/(1-p^(-1-z-z'))

is zeta(1+z+z')/[zeta(1+z)zeta(1+z')], which equals A(t,t')/ell_k times 1+O(L^(-0.75)). For each p>w the ratio of (1-b_{p,k}) to that local factor is 1+O(p^(-2)); their product is 1+O(1/w). Removing p<=w produces W/phi(W), times 1+O(L^(-0.75)(log w)^2), by the mean-value estimate for the logarithms of the three local factors and the elementary bound sum_{n<=w} (log n)/n=O((log w)^2). These errors are O(L^(-0.7)) for sufficiently large x. No many-coordinate absolute-value integral is involved.

Let D=integral_R2 |A| h h<infinity, and let tau_H be the same integral over the complement of [-H,H]^2. The Gevrey Fourier decay gives tau_H=O(exp(-c sqrt(H))) after decreasing c>0. For every alpha,beta>=0 and U consisting of m paired factors as in §1, (R1) and §1 give

|integral_[-H,H]^2 g_k U exp(-alpha(1+it)-beta(1+it')) h h|
<= C_k 4^m [c0+O(L^(-0.7))D+tau_H].                 (R2)

The estimate is uniform in all translation lengths. Indeed |U|<=4^m, while the extra exponential factors have modulus at most one. For U=1 and alpha=beta=0 the integral is C_k[c0+O(L^(-0.7))D+O(tau_H)]. The bracket divided by c0 is 1+O(L^(-0.7))+O(tau_H), and raising it to K still gives 1+o(1).

## 3. Coefficient norm for the coupling correction

Use the Banach algebra of absolutely summable combinations of monomials

exp(-sum_k alpha_k(1+it_k)-sum_k beta_k(1+it'_k)), alpha_k,beta_k>=0,

with norm bounded by the sum of absolute coefficients. It is enough to work with formal products and their absolutely convergent expansions; merging equal monomials can only reduce this norm. Each monomial has modulus at most one. The norm is submultiplicative, and ||b_{p,k}||<=3/p.

For p>w define

Q_p=(1-sum_{k=1}^K b_{p,k}) / product_{k=1}^K (1-b_{p,k}).

The numerator of Q_p-1 has no terms of degree zero or one. Expanding each inverse factor geometrically gives, with b=3/p,

||Q_p-1|| <= [(1+b)^K-1-Kb](1-b)^(-K) <= C K^2/p^2,

because K/p tends uniformly to zero for p>w. Hence

||product_{p>w} Q_p -1|| <= exp(C K^2/w)-1=o(1).       (R3)

This is the crucial support-sensitive correction estimate. Its coefficient norm is small before any integration; there is no D^K factor.

Let d=p_1...p_j be as in Lemma 6.2. For each p|d, let U_p be the paired factor in §1 on the unique coordinate k_{*,p}, if such a coordinate exists, and set U_p=1 otherwise. The uniqueness is the source's p>w>K observation. Set U_d=product_{p|d} U_p and

H_d=product_{p>w,p not dividing d} Q_p
    * product_{p|d} product_{k=1}^K (1-b_{p,k})^(-1).

Then the exact Euler product is

F_d=(1/d) (product_k g_k) U_d H_d.                    (R4)

This follows directly from the local factors on p.23: a nondivisor prime has local factor 1-sum_k b_{p,k}; a divisor prime has local factor U_p/p.

The same coefficient norm gives

||H_d|| <= exp(CK^2/w+CjK/w) <= (1+o(1)) 2^j          (R5)

for all sufficiently large x, uniformly in j, because exp(CK/w)<=2. This does not assert that jK/w=o(1); it permits the essential 2^j factor. For d=1, (R3) instead gives ||H_1-1||=O(K^2/w)=o(1).

## 4. Integration and the two conclusions of Lemma 6.2

Expand H_d in its absolutely summable translation monomials. For any one monomial, group U_d's paired factors by their coordinate; if coordinate k receives m_k factors, sum_k m_k<=j. Fubini and (R2) bound its integral against product_k g_k h(t_k)h(t'_k) by

(1+o(1)) 4^j c0^K product_k C_k,

uniformly in the monomial and in the divisor shifts. Applying (R5) in (R4), the truncated exact integral is at most

(1+o(1)) (8^j/d) c0^K product_k C_k.                 (R6)

For d=1, first integrate product_k g_k alone. Its integral is (1+o(1))c0^K product_k C_k by (R1). The H_1-1 correction is o(c0^K product_k C_k) by (R2)/(R3). Thus the exact integral is

(1+o(1)) c0^K product_k C_k.                         (R7)

Multiplication by x/W gives the main terms in (6.6). Its error is negligible at the stated scales: product_k ell_k<=exp(O(K log L)), while exp(-c L^0.1) dominates that loss; c0>=1 and W/phi(W)>=1. The numerator error carries 4^s/d and is absorbed by the required 8^s/d bound. Consequently

P_{k_*}(1)=(1+o(1)) (x/W) c0^K product_k C_k,
P_{k_*}(d)/P_{k_*}(1) << 8^s/d.

These are (6.9) and Lemma 6.2's conclusion. The argument actually bounds the main numerator by 8^j/d, and uses j<=s for the manuscript's stated form.

## Verification boundaries

The construction above supplies the corrected kernel integration step, including the structured Euler-product remainder that the printed proof does not control after its false identity. This argument has been independently checked. Its exact CRT/Fourier antecedent is verified in DISTINCT_OMEGA_RECONSTRUCTION.md §2. The remaining reductions and the separate high-moment issue on p.16 are handled in the companion reconstruction and MULTIPLICITY_REPAIR.md; this kernel note alone does not certify those parts.
