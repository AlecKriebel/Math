# Covariance without logarithmic oversampling: moment scope and a radial classification

**30001779 / OWR-5152-002. Scoped partial result; original general characterization unresolved, 3/5 approaches.** The negative answer under unrestricted one-dimensional moment assumptions is already known and credited below. No historical-priority or human peer-review claim.

## 1. Exact original question and the missing hypotheses

Vershynin's [OWR24/2011 contribution, printed p.1291](https://ems.press/content/serial-article-files/46338) uses the uncentered empirical second moment of a mean-zero vector,

$$\Sigma_N=\frac1N\sum_{i=1}^NX_iX_i^T,\qquad \Sigma=\mathbb E XX^T,$$

and asks for

$$\mathbb E\|\Sigma_N-\Sigma\|_{op}\le\varepsilon\|\Sigma\|_{op}$$

with N=O(n), at fixed accuracy. This is an expectation/operator-norm question, not merely weak spectral convergence, a lower-eigenvalue bound, or the performance of a different robust estimator. The constant implicit in O(n) must be uniform in dimension within the stated distribution class and may depend on accuracy and fixed regularity parameters.

The paragraph first recalls the O(n log n) bound for vectors supported in a ball of radius O(sqrt n), then asks for a general characterization and suggests sufficiency of 2+eta moments. It does not specify how the moment constants or the preceding norm restriction enter that last sentence. We retain both interpretations rather than silently dropping a structural hypothesis.

[Srivastava–Vershynin, *Annals of Probability*41(2013),3081–3111](https://doi.org/10.1214/12-AOP760), Theorem1.1 and Corollary1.2, give the two-sided expected operator-norm bound under **strong regularity**: after isotropic normalization, for every orthogonal projection P,

$$\Pr(\|PX\|_2^2>t)\le Ct^{-1-\eta}\quad\text{for }t>C\operatorname{rank}P,\tag{SR}$$

with C,eta independent of dimension and P. Their Theorem1.5 needs only uniformly bounded (2+eta)-moments of one-dimensional marginals, but concludes an expected **lower spectral edge** bound. It does not control the upper edge. Thus the imported description of the two-sided theorem as merely uniform marginal regularity is incomplete unless all projection dimensions and the unscaled tail bound (SR) are retained. In particular a normalized bound E(||PX||/sqrt(rank P))^(2+eta)<=C is not the displayed (SR).

Their Section1.8 already gives a counterexample, credited essentially to Aubrun: X=xi Z with xi standard Gaussian and Z uniform on the sphere of radius sqrt n, independent. It is isotropic and has uniformly subexponential one-dimensional marginals, yet the largest observed radius forces logarithmic oversampling. This settles the unrestricted-marginal-moment reading negatively, even with all finite marginal moments. It does not refute a version imposing an almost-sure O(sqrt n) norm bound. The same section explicitly discusses that distinction. We use the final journal-reprint source, not an inference from the paper's title.

## 2. A credited resolution of the bounded-radius moment subquestion

[Tikhomirov, *Sample covariance matrices of heavy-tailed distributions*, Theorem1](https://arxiv.org/abs/1606.03557) supplies a later high-probability estimate. The paper was published online21April2017 and appears in *IMRN*2018(20),6254–6289, DOI[10.1093/imrn/rnx067](https://doi.org/10.1093/imrn/rnx067). The full author preprint was checked; final typeset text was not compared line by line. In its isotropic specialization, if p>2, sup_(||u||=1) E|<X,u>|^p<=M, and N>=2n, then with probability at least1-1/n,

$$\|\Sigma_N-I\|\le\nu(p)\left[\frac1N\max_i\|X_i\|^2+M^{2/p}(n/N)^{1-2/p}\log^4(N/n)+M^{2/p}(n/N)^{1-2/\min(p,4)}\right].\tag{T}$$

The logarithm depends on the oversampling ratio N/n, not on n alone. If ||X||<=L sqrt(n) almost surely, let r=N/n>=2 and denote by

$$A(r)=\nu(p)\left[L^2/r+M^{2/p}r^{-(1-2/p)}\log^4r+M^{2/p}r^{-(1-2/\min(p,4))}\right]$$

the deterministic upper bound on the good event. Each term tends to zero as r tends to infinity. To obtain the **expectation** required by the original source, the exceptional event must still be controlled. Independence and isotropy give exactly

$$\mathbb E\|\Sigma_N-I\|_F^2=\frac{\mathbb E\|X\|^4-n}{N}\le\frac{L^2n^2}{N}.$$

Indeed E||XX^T-I||_F²=E||X||⁴-n, and the centered cross terms vanish. Cauchy–Schwarz on the exceptional event E, whose probability is at most1/n, now gives

$$\mathbb E[\|\Sigma_N-I\|_{op}\mathbf1_E]\le\sqrt{\mathbb E\|\Sigma_N-I\|_F^2\Pr(E)}\le L/\sqrt r.$$

Therefore

$$\mathbb E\|\Sigma_N-I\|_{op}\le A(r)+L/\sqrt r\longrightarrow0\quad(r\longrightarrow\infty),\tag{B}$$

uniformly in n. This proves linear sample sufficiency for the bounded-radius, uniform-p-moment subclass in the exact expectation norm of the source. It is a consequence of Tikhomirov's credited theorem, not a new proof of his probability estimate. For n=1 the Frobenius estimate alone gives the same limiting conclusion; no useful probability assertion at 1-1/n is needed.

For a nonidentity nonsingular covariance, apply this to Z=Sigma^(-1/2)X when the stated moment and radius assumptions hold after whitening, then use ||Sigma^(1/2)A Sigma^(1/2)||<=||Sigma|| ||A||. A singular covariance is treated on its range. A Euclidean radius bound on X alone is not automatically the same as the whitened bound.

## 3. A general necessary radial-maximum bound

For any isotropic vector and independent copies, positivity of each rank-one summand gives

$$\lambda_{max}(\Sigma_N)\ge\frac1N\max_{i\le N}\|X_i\|_2^2.$$

Consequently

$$\mathbb E\|\Sigma_N-I\|_{op}\ge\frac1N\mathbb E\max_{i\le N}\|X_i\|_2^2-1.\tag{1}$$

This is a necessary condition only. It does not characterize arbitrary covariance estimation: many vectors can have bounded radii and still exhibit directional/occupancy obstructions.

A precise complete classification is possible for the following restricted family. Fix a nonnegative random variable R, with a law independent of n and E R²=1. Let epsilon_1,...,epsilon_n be independent symmetric signs, independent of R, and put

$$X^{(n)}=R(\epsilon_1,\ldots,\epsilon_n).\tag{2}$$

The vectors are mean-zero and isotropic. Samples use independent copies of the entire vector, including independent radii. Coordinates within one sample are generally dependent.

**Restricted classification.** For the family (2), uniform-in-n expected operator-norm approximation with N=C_epsilon n for every fixed epsilon>0 holds if and only if R is essentially bounded.

### Necessity

Since ||X||²=nR², (1) becomes

$$\mathbb E\|\Sigma_N-I\|_{op}\ge\frac nN\mathbb E\max_{i\le N}R_i^2-1.\tag{3}$$

If R is unbounded, max_(i<=N) R_i² tends to infinity almost surely: for every M, P(max R_i²<=M)=P(R²<=M)^N tends to zero, and an infinite independent sequence realizes all levels almost surely. Monotone convergence gives divergence of its expectation. For any fixed C and n<=N(n)<=Cn, (3) therefore diverges. If N<n, rank deficiency already gives error at least1, so it cannot supply any accuracy below1. Thus no fixed linear sampling coefficient works for unbounded R. In fact along n<=N<=Cn the error diverges in probability as well, by the same maximum bound.

The dimension-independent law of R is essential. This theorem does not classify triangular arrays with dimension-dependent radial tails.

### Sufficiency, including the expectation bound

Suppose 0<=R<=B almost surely; E R²=1 implies B>=1. For every unit vector u,

$$\mathbb E e^{t\langle X,u\rangle}=\mathbb E_R\prod_j\cosh(tRu_j)\le e^{B^2t^2/2}.$$

Thus Z=<X,u> has tail P(|Z|>s)<=2 exp(-s²/(2B²)) and E Z²=1. Integrating its tail gives E|Z|^(2k)<=2(2B²)^k k!. For Y=Z²-1 and k>=2,

$$\mathbb E|Y|^k\le2^{k-1}(\mathbb E|Z|^{2k}+1)\le k!(8B^2)^k.$$

Since E Y=0, expansion of its exponential series yields

$$\mathbb E e^{tY}\le\exp(128B^4t^2)\quad\text{if }|t|\le(16B^2)^{-1}.$$

Chernoff's bound for N independent samples, optimizing in this allowed interval, gives

$$\Pr\left(\left|\frac1N\sum_iY_i\right|>s\right)\le2\exp\left[-N\min\left(\frac{s^2}{512B^4},\frac{s}{32B^2}\right)\right].\tag{4}$$

Take a Euclidean1/4-net of the unit sphere of size at most9^n. For a symmetric matrix A, approximating a maximizing unit vector by a net point proves ||A||<=2 max_net |u^TAu|. A union bound in (4) therefore gives, for t>=0, with A_0=n log9+log2,

$$\Pr\left\{\|\Sigma_N-I\|>2B^2\left[\sqrt{\frac{512(A_0+t)}N}+\frac{32(A_0+t)}N\right]\right\}\le e^{-t}.\tag{5}$$

Integrating this tail proves

$$\mathbb E\|\Sigma_N-I\|\le C_0B^2\left(\sqrt{n/N}+n/N\right),\tag{6}$$

for an absolute constant C_0. Indeed the threshold at t=0 and the integral of its derivative against e^-t are bounded by the right-hand side, since A_0 is comparable to n for n>=1. Choosing C_epsilon sufficiently large proves sufficiency. This is the standard subgaussian covering mechanism recalled in the original source, written explicitly for the restricted family.

## 4. An all-moments example requiring at least n log² n samples

The known radial obstruction can be made quantitative with a different elementary radius. Let Y be exponential of mean1 and put R=Y/sqrt2 in (2). Then E R²=1. Every fixed-order one-dimensional moment is uniformly bounded in n: for an even order2k,

$$\mathbb E|\langle X,u\rangle|^{2k}\le\frac{((2k)!)^2}{4^k k!}\quad(\|u\|_2=1).\tag{7}$$

To see this, E R^(2k)=(2k)!/2^k, while the moment of the Rademacher sum is at most the corresponding standard-Gaussian moment (2k)!/(2^k k!). The latter inequality follows coefficientwise from cosh(tu_j)<=_coeff exp(t²u_j²/2), since (2l)!>=2^l l!. Multiplication of nonnegative series preserves the coefficient inequality. Other finite orders follow by Holder.

For independent mean-one exponentials Y_i, E max_(i<=N)Y_i=H_N=sum_(j=1)^N1/j. One direct proof integrates 1-(1-e^-t)^N and uses y=e^-t followed by the finite geometric identity (1-(1-y)^N)/y=sum_(j=0)^(N-1)(1-y)^j. Jensen and (3) give

$$\mathbb E\|\Sigma_N-I\|\ge\frac{nH_N^2}{2N}-1.\tag{8}$$

Thus achieving any fixed accuracy epsilon<1 requires N>=n and

$$N\ge\frac{n\log^2(n+1)}{2(1+\varepsilon)},\tag{9}$$

because H_N>=log(N+1)>=log(n+1). This is a necessary sample-size bound, not a matching sufficiency assertion.

There is also a direct high-probability lower bound. For N>1,

$$\Pr\{\max_iY_i\ge\tfrac12\log N\}=1-(1-N^{-1/2})^N\ge1-e^{-\sqrt N}.$$

On this event,

$$\|\Sigma_N-I\|\ge\frac{n\log^2N}{8N}-1.\tag{10}$$

The law in this example is fixed across dimensions; all samples are independent. It satisfies every finite one-dimensional moment condition uniformly but violates any almost-sure bounded-radius assumption. It also fails (SR): taking P=I and t=An with fixed A>C leaves a positive dimension-independent tail probability, while C(An)^(-1-eta) tends to zero. Therefore it does not contradict Srivastava–Vershynin's theorem.

## 5. Remaining gap and outcome

Route1 was exact source recovery and separation of strong all-projection regularity from weak one-dimensional moments, including the already published radial counterexample. Route2 proved the restricted fixed-radius-law classification (2) and the explicit exponential-radius lower bounds. Route3 extracted the bounded-radius expectation conclusion (B) from the later high-probability theorem using the Frobenius identity. These use credited theorems and known maximum-radius/covering mechanisms; no novelty claim is made.

The original broad characterization of all distributions with N=O(n) remains unanswered here. The bounded-radius uniform-p>2 subclass is covered by (B), while the unrestricted-moment reading is already false. This does not yield necessary and sufficient conditions for arbitrary distribution families. The expectation upgrade uses the explicit Frobenius exceptional-event estimate; a high-probability theorem alone would not justify that step. Robust covariance estimators cannot replace the prescribed empirical covariance. Recommended status: **unsolved, 3/5**.
