# Approach 4: prescribe one zero first, then seek ordinary coefficients

This approach starts from analytic functions with one zero, rather than from arithmetic coefficients. It has two independent scope barriers: the asymptotic form forced by an ordinary Dirichlet expansion and the difference between analytic continuation and convergence.

## Lemma 4.1: the first nonzero coefficient controls the right-hand end

Let a nonzero ordinary Dirichlet series f(s)=sum a_n n^{-s} converge in a nonempty right half-plane, and let m be its first index with a_m!=0. There is c>0 such that, as real sigma tends to infinity,

f(s)=a_m m^{-s}(1+O(exp(-c Re(s)))),

uniformly in Im(s) for Re(s) sufficiently large. Moreover

f'(sigma)/f(sigma)=-log m+O(exp(-c' sigma))

for some c'>0.

### Proof

Convergence at one real sigma_0 implies |a_n|<=C n^{sigma_0}, so there is a real b with A=sum |a_n|n^{-b}<infinity. For Re(s)=sigma>b,

|sum_{n>m}a_n n^{-s}|/m^{-sigma}
 <= m^b sum_{n>m}|a_n|n^{-b}(m/n)^{sigma-b}
 <= m^b A (m/(m+1))^{sigma-b}.

Divide by a_m and put h(s)=f(s)/(a_m m^{-s})-1. This gives the first assertion and an exponentially small uniform bound on h. Cauchy's formula on a fixed-radius disk about a large real sigma gives the same type of bound on h'(sigma). Since 1+h stays bounded away from zero there, f'/f=-log m+h'/(1+h). QED.

## Theorem 4.2: polynomial–exponential ansatz

Suppose such an f has the exact form P(s)exp(Q(s)), with P a nonzero polynomial and Q a polynomial. Then P is constant and f(s)=a_m m^{-s}. In particular this ansatz cannot yield even one zero.

### Proof

Let d=degree(P). Along the positive real axis, P'/P=d/sigma+O(sigma^{-2}). Combining this with Lemma 4.1 gives

Q'(sigma)+log m=-d/sigma+O(sigma^{-2})+O(exp(-c' sigma)).

The polynomial on the left tends to zero, so it is identically zero. Therefore Q'=-log m. The remaining identity P'/P=O(exp(-c' sigma)), after multiplication by sigma and passage to infinity, yields d=0. The first-coefficient asymptotic then fixes the constant. QED.

This covers, for example, (s-rho)exp(as+b), all finite polynomial multiples of exponential functions, and the polynomial–exponential representation in the usual finite-zero finite-order entire factorization theorem. The latter extension depends on Hadamard's classical factorization theorem; no proof or independent verification of that external theorem is claimed here. The direct theorem above does not need it.

## Theorem 4.3: rational targets

A rational function representable by an ordinary Dirichlet series in a right half-plane must be constant.

### Proof

If a rational f is nonzero, its positive-real asymptotic is C sigma^d(1+O(1/sigma)) for an integer d. Lemma 4.1 rules out m>1, since a nonzero power cannot be asymptotic to an exponentially decaying quantity. Hence m=1 and f-a_1 is exponentially small. If that rational difference were nonzero, its own leading power asymptotic would contradict exponential smallness. Thus f=a_1. The zero rational function is already constant. QED.

In particular the tempting holomorphic one-zero half-plane function (s-rho)/(s-b), with a pole b outside the desired half-plane and rho inside, does not have an ordinary Dirichlet expansion. Being holomorphic and correctly zeroed is insufficient.

## Valid prescribed-divisor literature does not supply the missing convergence

Seip's Theorem 1.1 in arXiv:1812.11729v2 gives Helson zeta functions with prescribed signed divisors in a specified substrip of H_{1/2}. For instance a singleton at real 2/3 satisfies its conditions by choosing alpha=7/10<59/80; its counting conditions are immediate for a finite set. Crucially the symbol sigma(chi) in that paper denotes the abscissa of meromorphic continuation, not sigma_c of the ordinary series. The theorem does not assert sigma_c<2/3. Thus it provides a valid one-zero holomorphic continuation without the conclusion needed here about the original series.

Bochkov–Romanov's 2022 theorem and Bochkov's 2023 finite-value refinement likewise concern analytic continuations. The latter even permits signs +/-1 for conjugation-symmetric prescribed divisors. Neither abstract's coefficient restriction supplies a convergence theorem to the left of the prescribed zero. The finite-value refinement was checked at its publisher abstract only; its full proof was not inspected in this attempt.

## Attempt disposition

Explicit rational and polynomial–exponential single-zero recipes fail by complete proofs above. General holomorphic logarithmic factors may evade these obstructions, and valid Helson prescribed-divisor results remain promising inputs. The missing step is an ordinary coefficient expansion that actually converges in an open half-plane containing its chosen zero. No claim excludes arbitrary entire infinite-order continuations or arbitrary half-plane holomorphic factors. Estimated full-resolution progress remains 0%.
