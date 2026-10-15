# An explicit Laplace-transform law for Brownian first-visit cells

**Status:** complete candidate analytic joint-law formula; separate adversarial review pending. This is an AI-assisted research draft, not human peer reviewed. Historical priority is unestablished.

## 1. Exact problem and the format of the answer

Agelos Georgakopoulos's problem in *Enumerative Combinatorics*, Oberwolfach Report 23/2018, printed p.1452, starts independent Brownian motions at k uniform random or equidistant points on the circle and asks for the distribution of the lengths of the sets first visited by each particle. The primary page contains both choices of starting positions. It does not impose a large-k limit or require a named density.

We give an explicit, absolutely convergent joint Laplace-transform series for every finite k. Every coefficient is a finite sum of ordinary finite-dimensional integrals of specified scalar series, over specified linear inequalities. No unknown Brownian hitting probability, conditional law, integral equation solution, or cell distribution remains in those coefficients. The series has a uniform factorial truncation bound. This characterizes the full joint probability measure; it is not a claim of a simple density or an efficient numerical algorithm.

Work on T = R/Z, with Lebesgue measure of total mass one. Brownian motion has generator (1/2)d²/dx². For a circle of circumference c, multiply all the lengths below by c, or replace the Laplace variable theta by c theta. A common change of Brownian diffusivity merely rescales physical time and leaves the ownership unchanged. Walkers are independent and continue after all encounters with other walkers, starting points, and previously visited territory.

Fix starting positions p=(p_1,...,p_k). The uniform-start law is obtained by integrating over independent uniform p_i; the equidistant law uses p_i=(i-1)/k. The formula also gives the conditional law at any fixed distinct p.

For particle i put T_i(x)=inf{t>=0: W_i(t)=x}. Let I(x) be the least index attaining min_i T_i(x), and let

\[
L_i=\int_{\mathbb T}{\bf1}_{\{I(x)=i\}}\,dx.
\tag{1}
\]

The arbitrary tie convention has no effect on L almost surely.

## 2. Scalar interval kernels, including their normalization

For ell>0, 0<alpha<ell, t>0 define

\[
\begin{aligned}
f_0(t;\alpha,\ell)
 &=\frac{\pi}{\ell^2}\sum_{n=1}^{\infty}n\sin\frac{n\pi\alpha}{\ell}
           e^{-n^2\pi^2t/(2\ell^2)},\\
f_1(t;\alpha,\ell)
 &=\frac{\pi}{\ell^2}\sum_{n=1}^{\infty}(-1)^{n+1}n\sin\frac{n\pi\alpha}{\ell}
           e^{-n^2\pi^2t/(2\ell^2)}.
\end{aligned}
\tag{2}
\]

These series converge absolutely for every positive t, locally uniformly with all needed derivatives away from t=0. They are the nonnegative joint densities of the exit time from (0,ell) and exit at 0 or ell, respectively, for standard Brownian motion started at alpha. In particular,

\[
\int_0^\infty f_0\,dt=1-\alpha/\ell,
\qquad \int_0^\infty f_1\,dt=\alpha/\ell.
\tag{3}
\]

Here is a derivation that also fixes signs and the factor of two. The killed heat kernel is

\[
H(t;\alpha,\beta)=\frac2\ell\sum_{n\ge1}
\sin\frac{n\pi\alpha}{\ell}\sin\frac{n\pi\beta}{\ell}
 e^{-n^2\pi^2t/(2\ell^2)}.
\tag{4}
\]

The standard unit-interval version is, for example, Exercise 6(C) in Lalley's *Brownian Motion* notes; space-time scaling gives (4). Brownian exit from a bounded interval is almost surely finite. Optional stopping for the bounded stopped coordinate gives the two exit probabilities in (3). If tau is the exit time, the Markov property gives

\[
\mathbb P_\alpha(\tau>t, W_\tau=0)
 =\int_0^\ell H(t;\alpha,\beta)(1-\beta/\ell)\,d\beta.
\]

Differentiate at t>0, use H_t=H_{beta beta}/2, integrate twice by parts, and use H=0 at both endpoints. The negative derivative is (1/2)H_beta(t;alpha,0)=f_0. Using beta/ell instead gives -(1/2)H_beta(t;alpha,ell)=f_1. This proves positivity, the density interpretation and (3) without integrating a possibly nonabsolutely convergent Fourier series term by term at t=0.

For an additional normalization check, for s>0 their Laplace transforms are

\[
\int_0^\infty e^{-st}f_0\,dt
 =\frac{\sinh((\ell-\alpha)\sqrt{2s})}{\sinh(\ell\sqrt{2s})},\qquad
\int_0^\infty e^{-st}f_1\,dt
 =\frac{\sinh(\alpha\sqrt{2s})}{\sinh(\ell\sqrt{2s})}.
\tag{5}
\]

Indeed these are the unique solutions of u''/2=su with the respective endpoint data (1,0) and (0,1); the stopped exponential martingale or the bounded-domain Feynman--Kac formula gives (5).

## 3. A completely specified next-target kernel on the circle

Let A be a finite nonempty set of distinct circle points and z not in A. Lift the component of T minus A containing z to an interval (a,b) in R with z represented by z_tilde in (a,b). Put ell=b-a and alpha=z_tilde-a. Define K_A(t;z,q) for q in A as follows:

- Add f_0(t;alpha,ell) if a modulo 1 equals q
- Add f_1(t;alpha,ell) if b modulo 1 equals q
- Otherwise the value is zero

Both additions are made when A has only one point: then ell=1, the two endpoints represent the same point, and K_A=f_0+f_1. This case is essential. The definition is independent of the chosen integer lift. Equation (3) gives

\[
\sum_{q\in A}\int_0^\infty K_A(t;z,q)\,dt=1.
\tag{6}
\]

K_A is the joint density of the time and place of the *next first visit to a member of A*. Only A is absorbing in this auxiliary calculation. Previously visited test points and territory belonging to any particle are not absorbing.

## 4. Finite-target joint hitting-time densities

Choose distinct auxiliary query points x=(x_1,...,x_m), none equal to a starting position. The excluded configurations have zero Lebesgue measure in all later integrals.

For a permutation pi of {1,...,m}, define

\[
A_r^\pi=\{x_{\pi(r)},...,x_{\pi(m)}\},\qquad
z_0=p_i,\quad z_{r-1}=x_{\pi(r-1)}\quad(r\ge2).
\]

For u=(u_1,...,u_m) in (0,infinity)^m put

\[
D_i^\pi(u;x,p_i)=\prod_{r=1}^m
 K_{A_r^\pi}(u_r;z_{r-1},x_{\pi(r)}).
\tag{7}
\]

**Lemma.** D_i^pi is the joint density that particle i visits the test points in order pi, with u_r the elapsed time from the previous newly visited test point to the next one. Moreover,

\[
\sum_{\pi\in S_m}\int_{(0,\infty)^m}D_i^\pi(u)\,du=1.
\tag{8}
\]

**Proof.** Stop at the first visit to the whole finite target set, remove that visited target, then stop at the next visit to the remaining targets, and so on. These are finite stopping times. At each stage the current point is outside the remaining set. The strong Markov property gives precisely the successive kernels in (7), and induction using (6) gives (8). Impossible orders simply have zero factors. Distinct targets cannot be visited simultaneously by a continuous path. All targets are eventually visited because exit from each lifted bounded interval is finite. There is no stopping or coalescence caused by any of the other k walkers. ∎

The strong Markov property used here is Theorem 2.16 in Mörters--Peres, *Brownian Motion*. This is a standard tool, not a new claim of this work.

For k permutations bold-pi=(pi_1,...,pi_k) and k increment vectors u_i define the reconstructed physical hitting times

\[
h_{ij}(u,\boldsymbol\pi)=\sum_{r=1}^{\pi_i^{-1}(j)}u_{ir}.
\tag{9}
\]

For a label vector a=(a_1,...,a_m) in {1,...,k}^m let

\[
\mathcal C_a(\boldsymbol\pi)=
\{u>0: h_{a_j,j}(u,\boldsymbol\pi)<h_{i,j}(u,\boldsymbol\pi)
\text{ for every }j\text{ and every }i\ne a_j\}.
\tag{10}
\]

This region is given by explicitly displayed strict linear inequalities, all with integer coefficients. Define the deterministic quantity

\[
Q_a(x;p)=\sum_{\pi_1,...,\pi_k\in S_m}
\int_{\mathcal C_a(\boldsymbol\pi)}
 \prod_{i=1}^kD_i^{\pi_i}(u_i;x,p_i)\,
 \prod_{i=1}^k\prod_{r=1}^mdu_{ir}.
\tag{11}
\]

The sum has (m!)^k terms, each a nonnegative km-dimensional integral. Equations (2), (7), (9) and (10) specify it without any remaining stochastic objects. The integral is at most one after summing all orders, by (8). Independence and the lemma show that

\[
Q_a(x;p)=\mathbb P(I(x_1)=a_1,...,I(x_m)=a_m),
\quad \sum_aQ_a(x;p)=1.
\tag{12}
\]

For justification of the last identity, each single-target hitting time has the continuous density furnished by the singleton case of Section 3. For fixed x_j the k times are independent, so ties have probability zero. Their finite union over j still has probability zero. Equivalently, the equality boundaries in (10) are finitely many proper hyperplanes and have measure zero for the product density.

## 5. The explicit joint law and its error bound

Let theta=(theta_1,...,theta_k) with theta_i>=0, and theta_* = max_i theta_i. Set M_0(theta;p)=1 and for m>=1 set

\[
M_m(\theta;p)=\int_{\mathbb T^m}
\sum_{a\in\{1,...,k\}^m}
 \left(\prod_{j=1}^m\theta_{a_j}\right)Q_a(x;p)\,dx_1\cdots dx_m.
\tag{13}
\]

The integrand may be assigned arbitrary values on the excluded zero-measure configurations. These are bounded, well-defined deterministic integrals: 0<=M_m<=theta_*^m.

**Theorem.** The conditional joint law of the first-visit cell proportions L=(L_1,...,L_k), for fixed p, has the Laplace transform

\[
\boxed{\quad
\mathcal L_p(\theta)=\mathbb E_p e^{-\sum_i\theta_iL_i}
 =\sum_{m=0}^\infty\frac{(-1)^m}{m!}M_m(\theta;p).
\quad}
\tag{14}
\]

All coefficients in (14) are explicitly given by (2), (7), and (9)--(13). The series is absolutely convergent. For every truncation degree M>=0,

\[
\left|\mathcal L_p(\theta)-\sum_{m=0}^M
  \frac{(-1)^m}{m!}M_m(\theta;p)\right|
\le \frac{\theta_*^{M+1}}{(M+1)!}.
\tag{15}
\]

The bound is uniform in starting positions. The entire joint probability measure on the simplex {l_i>=0, sum_i l_i=1} is uniquely determined by (14).

**Proof.** We first make (1) and the required applications of Fubini precise. On continuous-path space, for each fixed t the set of visited points up to t is compact. Its distance from x is the infimum over rational times in [0,t], together with t, of continuous distance functions. Thus (path,x) -> T_i(x) is jointly measurable. For each x other than the finitely many seeds, all particles hit x in finite time and their hitting times are independent and atomless. Fubini therefore shows that almost surely the exceptional x where a hitting time is infinite or the earliest visit is tied have Lebesgue measure zero. Consequently the measurable sets in (1) partition the circle up to a null set, and sum_i L_i=1.

Put Z=sum_i theta_i L_i=integral_T theta_{I(x)}dx. It lies in [0,theta_*]. Applying Tonelli to the mth power of this nonnegative integral, then (12), gives E Z^m=M_m. The exponential series is dominated in absolute value by exp(theta_*), so it may be averaged term by term. Taylor's theorem for exp(-z) on z>=0 bounds its degree-M remainder by z^(M+1)/(M+1)!, proving (15) after taking expectations.

Finally the transform determines all mixed moments, either by differentiation at zero (justified by bounded support), or by the homogeneous polynomial coefficients M_m. Polynomials are dense in continuous functions on the compact simplex by Stone--Weierstrass, and finite Borel measures are determined by their continuous-function integrals. Thus no two joint laws on that simplex can have (14). ∎

In particular, this is more than the tautological identity E exp(-theta dot L): equations (2) and (7)--(13) reduce every coefficient to explicit scalar functions, finite permutations and ordinary integration. The factorial bound controls truncation of the outer series. It does not by itself certify a particular numerical quadrature or truncation of the inner heat-kernel series; no such numerical claim is made.

## 6. The two requested starting laws and immediate checks

For equidistant starts the answer is (14) with p_i=(i-1)/k. A common random rotation changes none of the lengths and can be ignored. For independent uniform starts the answer is

\[
\boxed{\quad
\mathcal L_{\rm unif}(\theta)
 =\int_{\mathbb T^k}\mathcal L_p(\theta)\,dp
 =\sum_{m=0}^\infty\frac{(-1)^m}{m!}
      \int_{\mathbb T^k}M_m(\theta;p)\,dp.
\quad}
\tag{16}
\]

The uniform bound proves the exchange of the integral and series and gives exactly (15) for (16). Coincident seeds form a null set and cause no difficulty. If the phrase “uniformly at random” uses labels assigned after circular ordering rather than i.i.d. labels, the same fixed-p formula can instead be integrated against that ordered-start law; (16) uses the usual independent-uniform convention.

Some useful exact checks are:

1. k=1 gives L_1=1 and the transform exp(-theta_1)
2. All theta_i=t gives M_m=t^m and the transform exp(-t)
3. The uniform-start law is exchangeable in the labels, so E L_i=1/k
4. The equidistant-start law is cyclically and dihedrally symmetric, so E L_i=1/k; full permutation exchangeability is not asserted
5. For a single query point x, let g_i(t)=K_{\{x\}}(t;p_i,x) and S_i(t)=1-integral_0^t g_i(s)ds. Then (11) reduces to the familiar competing-clock identity

\[
\mathbb P(I(x)=i)=\int_0^\infty g_i(t)\prod_{j\ne i}S_j(t)\,dt.
\tag{17}
\]

The general formula preserves the dependence among all hitting times belonging to one walker. Replacing that dependence by independent clocks, stopping walkers when they enter another cell, or using spatial Voronoi cells of the seeds would not give the same model.

## 7. Attribution, source scope and remaining limitations

The source problem is a finite-k distribution question. Equations (14) and (16), with explicitly reduced coefficients and error bound, are a complete analytic-transform answer in that literal sense. They do not identify a classical named multivariate distribution, provide a compact density, or establish a fast algorithm. Those stronger refinements remain unaddressed.

All probabilistic ingredients used in the reduction are standard: killed one-dimensional heat kernels, interval exit probabilities, independence, the strong Markov property, and bounded-variable moment determinacy. They are credited below. Bounded current-literature searches did not locate a later treatment of the exact first-visit cell law, but this is not a proof of novelty or an exhaustive priority search.

The checks accompanying this note verify interval-kernel normalizations, finite-target order combinatorics and moment identities on exact finite analogues. They are diagnostics, not substitutes for the Brownian argument above. In particular, a discrete random walk simulation would not prove the circle Brownian law, and none is used as such.

## Sources

1. A. Georgakopoulos, “Voronoi-like decomposition of S1 with randomness,” in *Enumerative Combinatorics*, Oberwolfach Report 23/2018, printed p.1452. [Full primary report](https://ems.press/content/serial-article-files/46745). The original page was also inspected as a rendered image.
2. P. Mörters and Y. Peres, *Brownian Motion*, Cambridge University Press, 2010, Theorem 2.16 and its proof, printed pp.43--44: the strong Markov property. [Author-hosted full book](https://www.mi.uni-koeln.de/~moerters/book/book.pdf).
3. S. Lalley, *Brownian Motion*, course notes, Exercise 6(A)--(C): the killed unit-interval eigenfunction expansion with generator (1/2)d²/dx². [Author-hosted notes](https://galton.uchicago.edu/~lalley/Courses/312/BrownianMotion312.pdf).
