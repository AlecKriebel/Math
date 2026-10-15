# Clarifications for the fixed-parameter reconstruction

Independent audit, 8 October 2026. This addendum supplements, and does not change, the two accepted fixed-parameter conclusions in `original/FIXED_G_PROOF.md`. The original files are preserved byte-for-byte. No new proof-search turn or claim of all-variable-count uniformity is involved.

## 1. Operator-valued norm input and finite-dimensional use

The norm inequality used in A1 is the homogeneous free-group estimate in Pisier, *Introduction to Operator Space Theory*, Theorem 9.7.4, printed pp. 187–189. Its coefficient matrix at split s has entries c(vw^{-1}) when there is no cancellation. If c is supported on positive words of length n, the nonzero rows have positive v and the nonzero columns have negative w. Inverting the column index gives precisely entries X^v X^z with |v|=s and |z|=n-s. The resulting matrix is the product of the column of X^v and the row of X^z; its norm is at most C_s R_(n-s). The edge matrices give R_n and C_n. This verifies both sides and the orientation in A1.

The lower bound can also be checked directly on the free-group vacuum, once for T^n and once for (T^n)*, because distinct words give orthogonal vectors. No scalar-only norm inequality is being substituted for an operator-valued one.

In B, the equality of the two positive-map spectral radii uses finite-dimensional Hilbert–Schmidt adjointness. Reversing all words in the sum identifies Psi^n(I) with sum (X^w)*X^w. For column-vectorization, Phi is represented by sum conjugate(X_j) tensor X_j; exchanging the tensor factors gives the displayed version. Neither an assertion about spectra of adjoints on different Banach spaces nor an infinite-dimensional adjoint argument is needed.

## 2. Exact specialization of Parraud's theorem

Keep g fixed. After flipping tensor factors, write the pencil as I + sum (U_j tensor I_k)(I_N tensor X_j). Encode this using one scalar-coefficient noncommutative *-polynomial in g unitary variables and g deterministic coefficient variables, together with their adjoints. The polynomial is self-adjoint after multiplying the pencil by its adjoint. The deterministic variables are I_N tensor X_j, whose norms are at most r. Thus Parraud's polynomial L_P is evaluated on a common bounded interval independent of N and X. Its free comparison is exactly the tensor-product model with free Haar u_j commuting with M_k, and the comparison trace is tau tensor (Tr_k/k).

The theorem's matrix-amplification parameter M is k. The normalized error is O(k^2 log(N)^2/N^2); multiplying by kN gives the unnormalized error O(k^3 log(N)^2/N). This explains all trace factors in C. The theorem is applied for N>=2, and N=1 is estimated directly. This specialization is uniform only for the fixed polynomial alphabet and fixed matrix size.

## 3. A completely specified smooth majorant

Choose a smooth function theta supported away from zero with 0<=theta<=1, theta=0 on x<=a/4, and theta=1 on x>=a/2. On the positive axis, define f_0(x)=(1-theta(x)) log a + theta(x) log x; set f_0=log a on x<=0. This is smooth because it is constant on a neighborhood of zero. In the interpolation region x<a, log a>=log x, so f_0 majorizes log x. It equals log x on x>=a/2.

Choose a second smooth cutoff chi=1 on x<=K and chi=0 on x>=K+1. Set f=chi f_0+(1-chi)c with any fixed real c. Then f has bounded derivatives of every order, is bounded, equals log on [a,b], and majorizes log on (0,K]. Its behavior beyond K is irrelevant. This is the function required in C.

The Hilbert–Schmidt bound follows by factoring the pencil difference into the row [X_j tensor I_N] and column [I_k tensor (U_j-V_j)]. The row has norm <=r and the column has squared Hilbert–Schmidt norm k sum ||U_j-V_j||_HS^2. There is no missing factor of N or g. Multiplication by the bounded pencil and the trace Cauchy–Schwarz bound then give exactly L sqrt(N), with L=2kr(1+r sqrt(g)) Lip(f).

## 4. Gaussian covariance, including pure powers

For positive words w,v of length n, the limiting covariance of Tr(U^w) with conjugate(Tr(U^v)) is the number of letter rotations of v equal to w. Covariances between two positive traces vanish. Theorem 3.13 and Corollary 3.14 of Mingo–Śniady–Speicher give the cyclically alternating multi-generator case after consecutive identical generators are grouped into powers. Pure powers U_j^n are covered by the same paper's Remark 3.8, equation (15): their limiting variance is n. This last input is worth stating explicitly because the displayed cyclically alternating condition in (24) is not literal for a single syllable.

For each fixed w, sum_v #{rotations of v equal to w}=n. The trace coefficient b_v is constant over the cyclic orbit. Consequently the full double covariance sum is sum_w n a_w conjugate(b_w), including periodic words. For example, w=0101 has two distinct rotations and stabilizer size two; w=0000 has one distinct rotation and stabilizer size four. Counting distinct rotations alone would be incorrect.

The use of exact finite-N centering is restricted to positive and inverse-positive words. A common Haar phase gives this centering, including the infinite series by uniform convergence at each fixed N. It does not establish exact centering of general cyclically reduced mixed words. The commutator witness in the original audit is correct: integrating U first gives (Tr V/N)Tr(V*) and hence expectation 1/N.

## 5. Full-series uniform integrability

Let delta_M be the weighted absolute coefficient mass of the omitted positive and inverse-positive words. The trace of each length-n word is n sqrt(N)-Lipschitz, so the centered tail is delta_M sqrt(N)-Lipschitz. The displayed complex sub-Gaussian tail in D follows by applying real concentration to its two components and using a union bound. When delta_M=0, the tail is identically zero and that case is handled directly.

For any fixed p>1, the same centered concentration bound gives a uniform bound on E exp(p Re G_N), and on the corresponding truncations. Thus their exponentials are uniformly integrable. Gaussian convergence for each finite truncation therefore implies convergence of its exponential expectation.

The square-tail integral in D has the correct factor eight: differentiation of (e^t-1)^2 gives 2e^t(e^t-1), and the complex concentration tail contributes four. For all sufficiently large M, delta_M<=1, so the integrand is dominated by 8e^t(e^t-1)e^(-t^2/24), an integrable function. It tends to zero for every t>0. This justifies dominated convergence and the uniform-in-N removal of the truncation. The covariance series itself is absolutely convergent, for example by the bound kl sum_n (gq^2)^n/n.

## 6. Product-domain continuation and similarity

The complex variables in E are independent A and Z, not A and B with an unannounced antiholomorphic dependence. Entrywise conjugation preserves row norm, so Z=conjugate(B) lies in the second row ball. The two second-moment bounds give compact-local boundedness by Cauchy–Schwarz.

The prospective reciprocal determinant is holomorphic on that product: row control of A-words and the dimension-l trace bound for the Z-word column give ||S^n||<=sqrt(l)(ab)^n, hence spectral radius <1. Joint normality, uniqueness on the nonempty small product neighborhood, and the identity theorem force every convergent subsequence to have the same limit. The subsequence contradiction proves convergence of the original sequence locally uniformly.

For each fixed tuple of strict outer radius, the convergent positive-map series P=sum Phi^n(I) satisfies P>=I and Phi(P)=P-I. Conjugating by P^(-1/2) gives row square I-P^(-1), with norm strictly below one in finite dimension. Independent similarities for A and B preserve the determinant integrals and the mixed tensor determinant. No uniform control of these similarities over changing parameters is asserted.

## 7. Stopping boundary

OWR Lemma 9 supplies strict row-contracting determinantal representations valid on all finite matrix tuples. Those exact representations allow the companion covariance conclusion. The supplied source does not ask for a tuple-count-uniform convergence rate. OWR Conjecture 12 displays C(r,k) over all tuple counts. The fixed-g argument establishes C(g,k,r,m), which is insufficient for that stronger literal requirement. Neither this addendum nor the test suite closes that bridge.
