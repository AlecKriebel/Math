# Cofinite zeros of high derivatives

## Theorem and attribution

There is a transcendental entire function f such that, for every nonempty open subset U of the complex plane, every sufficiently high derivative f^(n) has a zero in U. More precisely, the planar Gaussian entire series

    F(z) = sum_{k>=0} xi_k z^k / sqrt(k!)

has this property with probability one, when its coefficients are independent circular complex Gaussian variables with density pi^(-1) exp(-|w|^2).

This is a detailed reconstruction of the Gaussian route proposed by Adriano Almeida and Przemek Chojecki in April 2026, not a novelty claim. Almeida's five-page manuscript supplies the same covariance, expected-zero, hole-probability, and Borel–Cantelli architecture. The proof below establishes directly all the special-function and deviation estimates used here. Neither a Laguerre asymptotic theorem nor an Offord theorem is assumed. No bounded-coefficient theorem, explicit selected sample, formal verification, or audit of the Boas–Reddy papers is asserted.

Primary provenance: [Almeida's manuscript at the inspected commit](https://github.com/Drill23/erdos-problem-906-proposed-solution/blob/d9aefa869577e6c0135dd994046a6b59b063733f/paper/erdos_906_proposed_solution.pdf) and [the contemporaneous discussion](https://www.erdosproblems.com/forum/thread/906).

Throughout, derivative orders are nonnegative integers; restricting to positive integers changes no conclusion. Area measure dA and the real Laplacian Delta are unnormalized. Zeros of a nonzero analytic function are counted with multiplicity.

## 1 Entire samples and measurable fields

Use the countable product of the stated Gaussian laws on C^N. For k>=1,

    P(|xi_k|>k) = exp(-k^2).

The sum over k is finite, so the first Borel–Cantelli lemma gives |xi_k|<=k eventually with probability one. For each finite R, the series sum_{k>=1} k R^k/sqrt(k!) converges by its ratio test. Consequently, on this single event, the series defining F converges locally uniformly on C and defines an entire function. This event works for every R, without an uncountable probabilistic intersection: it is the one coefficient bound followed by a deterministic convergence statement.

For each k, P(xi_k=0)=0. Intersecting these countably many probability-one events yields an event Omega_* of probability one on which all coefficients are nonzero and F is entire. All such F are transcendental. In particular, no derivative is identically zero. Termwise differentiation of a locally uniformly convergent power series gives, for every n,

    F_n(z) := F^(n)(z)
            = sum_{j>=0} xi_{n+j} sqrt((n+j)!) z^j/j!.

For complete measurability bookkeeping, on the measurable null complement of Omega_* define F(z)=exp(z) and F_n(z)=exp(z). The field (omega,z) -> F_n(omega,z) is jointly measurable: on Omega_* it is a pointwise limit of jointly measurable partial sums, and elsewhere it is the specified measurable function. Every resulting sample is entire with nonzero derivatives. This modification leaves every fixed-point distribution and every almost-sure claim unchanged. In the remainder F_n denotes these versions.

For fixed n and z, the sum of the variances of the differentiated summands is

    K_n(z) = sum_{j>=0} (n+j)! |z|^(2j)/(j!)^2 < infinity.

The ratio of consecutive nonzero summands is |z|^2(n+j+1)/(j+1)^2, tending to zero. Thus the random partial sums converge in L2. Their Gaussian laws converge to a centered circular complex Gaussian of variance K_n(z). The L2 limit agrees almost surely with the already constructed almost-sure sum at this fixed point. Also K_n(z)>=n!>0. The field therefore has a nondegenerate Gaussian law at every fixed spatial point. This assertion does not say that different points or different derivative orders are independent.

## 2 Exact covariance and an elementary uniform bound

Differentiating exp(zw) n times in each of its two independent variables gives

    partial_z^n partial_w^n exp(zw)
       = n! exp(zw) sum_{j=0}^n binom(n,j) (zw)^j/j!.

For example, first differentiating in z gives w^n exp(zw); in the subsequent Leibniz expansion, take j derivatives of the exponential and n-j derivatives of w^n. Setting w=conjugate(z) proves

    K_n(z) = n! exp(|z|^2) L_n(-|z|^2),
    L_n(-r^2) := sum_{j=0}^n binom(n,j) r^(2j)/j!.

Fix numbers 0<a<b. Uniformly for a<=r<=b, we claim

    log L_n(-r^2) = 2r sqrt(n) + O_{a,b}(log n).       (1)

Here is a bound with explicit error. Put x=r sqrt(n). For all n with a sqrt(n)>=1 and b sqrt(n)<=n/2, put k=floor(x). Then 1<=k<=n/2. Since binom(n,j)<=n^j/j!,

    L_n(-r^2) <= sum_{j>=0} x^(2j)/(j!)^2
               <= (sum_{j>=0} x^j/j!)^2 = exp(2x).

For the lower bound, log(1-t)>=-2t when 0<=t<=1/2, so

    binom(n,k) >= (n^k/k!) exp(-k(k-1)/n).

The kth summand alone yields

    log L_n(-r^2) >= 2k log x - 2 log(k!) - k(k-1)/n.

There is no need to invoke Stirling. Monotonicity of log gives, for every integer k>=1,

    log(k!) <= integral_1^k log t dt + log k
             = k log k - k + 1 + log k.

Because k<=x<k+1, we have k log(x/k)>=0 and 2k>=2x-2. Also k(k-1)/n<=b^2 and k<=b sqrt(n). Consequently

    2r sqrt(n) - 4 - 2 log(b sqrt(n)) - b^2
       <= log L_n(-r^2) <= 2r sqrt(n).                (2)

This proves (1). In particular, on a<=|z|<=b,

    log K_n(z) = log(n!) + 2 sqrt(n)|z| + E_n(z),
    |E_n(z)| <= C_n := b^2 + 4 + 2 log(b sqrt(n)),     (3)

for all sufficiently large n. The constant is independent of z on the fixed annulus and C_n=O_{a,b}(log n). These are bounds on function values only. No derivative of E_n is used anywhere.

## 3 Distributional zero counting and expectation

Fix an open disk D whose closure avoids zero. Take phi in C_c^infinity(D), nonnegative and not identically zero. Let

    X_n = sum_{F_n(z)=0} m_z phi(z),
    L = integral_C |Delta phi(z)| dA(z),
    A = integral_C phi(z)/|z| dA(z).

There are only finitely many zeros on the compact support of phi, since F_n is entire and not identically zero. Thus X_n is finite and nonnegative. We have A>0, because phi is continuous, nonnegative, positive somewhere, and its support avoids zero. We also have L>0: otherwise Delta phi=0, and integration by parts gives integral |grad phi|^2=-integral phi Delta phi=0, forcing phi=0.

For any analytic function g that is not identically zero, local factorization at each zero gives g(z)=(z-z_0)^m h(z) with h nonvanishing nearby. Then log|h| is harmonic and log|z-z_0| is locally integrable. The fundamental identity Delta log|z-z_0|=2pi delta_{z_0}, obtained by integration over a small circle, therefore gives

    Delta log|g| = 2pi sum_{g(z)=0} m_z delta_z

as distributions. Pairing with phi yields, sample by sample,

    X_n = (1/(2pi)) integral_C Delta phi(z) log|F_n(z)| dA(z).    (4)

Define Z_n(z)=F_n(z)/sqrt(K_n(z)). For each fixed z this is a standard circular complex Gaussian. Its radial law is 2r exp(-r^2) dr for r>0, so

    E |log|Z_n(z)|| = E |log|Z|| < infinity.

The finiteness follows directly by integrating r|log r| near zero and r exp(-r^2) log r near infinity. On the compact support of Delta phi, log K_n is bounded for each fixed n. Since

    log|F_n(z)| = (1/2)log K_n(z) + log|Z_n(z)|,

Tonelli gives absolute integrability in the product of probability and weighted area measure. It follows that (4) defines a measurable integrable random variable and Fubini applies. The number E log|Z| is independent of z, and integral Delta phi dA=0. Therefore

    mu_n := E X_n
          = (1/(4pi)) integral_C Delta phi(z) log K_n(z) dA(z).   (5)

Choose 0<a<b such that the support of phi lies in a<|z|<b. The same is then true of the support of Delta phi. Insert (3) in (5); the constant log(n!) integrates to zero. The compact support allows integration by parts against |z|, which is smooth nearby and satisfies Delta|z|=1/|z| there. Hence

    mu_n = (sqrt(n)/(2pi)) A + R_n,
    |R_n| <= L C_n/(4pi).                                (6)

As C_n/sqrt(n) tends to zero, there is a deterministic N_phi such that

    mu_n >= A sqrt(n)/(4pi) > 0,                         (7)

for every n>=N_phi. This justifies the full expected-zero growth needed for the argument, using only the value estimate (3).

## 4 Uniform exponential deviation without independence

Subtracting (5) from (4), and using integral Delta phi=0 to remove the constant E log|Z|, gives

    X_n-mu_n = (1/(2pi)) integral_C Delta phi(z) log|Z_n(z)| dA(z).

Notice that no holomorphicity of the normalized field Z_n is required. Introduce the deterministic probability measure

    dw(z) = |Delta phi(z)| dA(z)/L.

We have almost surely

    (2pi/L)|X_n-mu_n| <= integral_C |log|Z_n(z)|| dw(z).

At each fixed z, Z_n(z) has no atom at zero. Joint measurability and Tonelli allow the logarithm to be assigned any value at zeros when forming Lebesgue integrals; for each analytic sample its zero set has area measure zero. Tonelli also shows that the displayed integral is finite almost surely. Jensen and another application of Tonelli now give

    E exp((2pi/L)|X_n-mu_n|)
       <= E exp(integral |log|Z_n(z)|| dw(z))
       <= integral E exp(|log|Z_n(z)||) dw(z)
       <= E(|Z|+|Z|^(-1))
       = sqrt(pi)/2 + sqrt(pi)
       = 3sqrt(pi)/2 < 3.                               (8)

Indeed exp(|log r|)=max(r,r^(-1))<=r+r^(-1), and the two displayed moments follow by integration against 2r exp(-r^2) dr. To avoid any possible question about unbounded Jensen, first observe by Tonelli that integral exp(|log|Z_n||) dw is finite almost surely; Jensen for truncations and monotone convergence then prove (8).

Markov's inequality yields for every n and lambda>0,

    P(|X_n-mu_n|>=lambda) <= 3 exp(-2pi lambda/L).        (9)

All constants are uniform in n. Only the standard one-point marginal law was used in (8); no independence of spatial values or derivative orders is assumed.

## 5 Hole events and the countable conclusion

Let H_n(D) be the event that F_n has no zero in D. This event is measurable. One explicit verification uses a sequence of closed concentric subdisks K_j exhausting D. On each K_j, take a countable dense set Q_j. Continuity gives

    min_{z in K_j}|F_n(z)| = inf_{q in Q_j}|F_n(q)|,

a measurable random variable. There is a zero in D exactly when this minimum is zero for some j. Thus the zero-existence event is a countable union of measurable events, and H_n(D) is its complement.

On H_n(D), X_n=0. For n>=N_phi, (7) and (9) consequently imply

    P(H_n(D)) <= 3 exp(-A sqrt(n)/(2L)).                 (10)

The right side is summable. For example, for integers m>=1, the block m^2<=n<(m+1)^2 contains 2m+1 terms, each at most exp(-c m), with c=A/(2L)>0. The sum of (2m+1)exp(-c m) is finite. The finitely many orders n<N_phi do not matter. The first Borel–Cantelli lemma therefore proves that almost surely H_n(D) occurs only finitely many times. Independence is not a hypothesis of that lemma.

Let B consist of all disks B(c,r) with c in Q+iQ, r a positive rational, and r<|c|. This is countable. Every nonempty open U contains one of these disks: take a nonzero point in U, then a sufficiently nearby rational center and a sufficiently small rational radius. This also works when zero belongs to U. Technically B is a countable pi-base for C, sufficient for hitting every open set; it is not a neighborhood base at zero.

Intersect the probability-one eventual-hitting events for all D in B with Omega_*. The resulting event still has probability one. Fix one sample f in it. For every nonempty open U, choose D in B with D subset U. There is an N(D) such that f^(n) has a zero in D for every n>=N(D), and hence it has a zero in U for those n. This proves the theorem. No uncountable intersection of probability-one events was taken.

## 6 Relation to the precise problem statement

For any entire f, write Z_n(f)={z:f^(n)(z)=0}; if a derivative is identically zero, this set is all of C. The following statements are equivalent:

1. Every nonempty open U is hit by Z_n(f) for all sufficiently large n.
2. For every infinite strictly increasing sequence (n_k), the union of Z_{n_k}(f) is dense in C.

For 1 implies 2, fix U and use that n_k tends to infinity. For the converse, if 1 fails for some U, the set of orders n for which Z_n(f) misses U is infinite. Its increasing enumeration gives a sequence whose union of zero sets misses U, contradicting 2. This is a deterministic equivalence, so the universal quantifier over infinite sequences causes no further probabilistic issue.

If the problem asks only for a nonzero entire function, every nonzero polynomial satisfies it: all derivatives above its degree are identically zero. The theorem proved here establishes the stronger transcendental interpretation without exploiting that degeneracy.

## Provenance and limits

The original problem appears in Paul Erdős, *Some of my favourite problems which recently have been solved* (1982), printed p.72, physical PDF p.14, [original PDF](https://users.renyi.hu/~p_erdos/1982-33.pdf). That page presents the every-infinite-subsequence quantifier and reports an older affirmative resolution; its note (1), printed p.79, lists four Barth–Schneider papers. This proof does not rely on that historical claim or identify which older result might settle the question.

Almeida's April 2026 manuscript is a proposed AI-assisted draft. Chojecki's contemporaneous forum contribution describes the same Gaussian route and acknowledges Almeida's earlier posting. Eric Hou's separate bounded-coefficient manuscript also credits those proposals; its latest arXiv record inspected here is [2607.20816v5](https://arxiv.org/abs/2607.20816v5), revised 25 August 2026. Hou's proof, its growth assertions, and its separate Lean development are not dependencies of the theorem proved above.

The only background used is elementary complex power-series theory, local factorization and the distributional Laplacian of log|z|, elementary integration by parts, countable product probability, Gaussian finite-sum laws and L2 convergence, Tonelli/Fubini, Jensen, Markov, and the first Borel–Cantelli lemma. The result here is a mathematical proof and audit conclusion, not a claim of journal acceptance or machine verification.
