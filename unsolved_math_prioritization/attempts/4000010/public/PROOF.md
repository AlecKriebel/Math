# Functional inequalities for coarse Ricci curvature: five approaches and a scope boundary

**Problem:** 4000010 / AMR-039-0010, Ollivier's Problem J (May 2008).

**Verdict:** Partial results and explicit obstructions; no full resolution or novelty claim. The original item is an exploratory request for a suitable functional-inequality formulation, rather than one fully quantified conjecture. We prove precise formulations below, but do not identify them with every proposed version of that request. In particular, a nonlinear function of a Wasserstein distance is different from an optimal transportation cost with that nonlinear function inside the integral.

The source and literature checks are in [SOURCE_GATE.md](SOURCE_GATE.md). These results are elementary reconstructions and consequences of established methods. The finite checks in [verify.py](verify.py) supplement the proofs; they are not substitutes for them.

## 1. Notation and two elementary tools

Let `(X,d)` be a Polish metric space. Write `P_x=P(x,.)` for a Markov kernel with finite first moments, and assume it has an invariant probability `pi` with finite first moment. For a measurable `f`, write `Pf(x)=integral f(y) P_x(dy)`. Assume

\[
 W_1(P_x,P_y)\le qd(x,y),\qquad q=1-\kappa,\qquad 0<\kappa\le1. \tag{1}
\]

Here `W_1` is the infimum of expected distance over couplings. The Kantorovich--Rubinstein duality theorem on Polish spaces with finite first moments gives

\[
 W_1(\mu,\pi)=\sup_{\operatorname{Lip}(f)\le1}
 \left(\int f\,d\mu-\int f\,d\pi\right). \tag{2}
\]

We use this standard duality theorem explicitly. No reversibility is assumed. Equation (1) implies

\[
 \operatorname{Lip}(P^n f)\le q^n\operatorname{Lip}(f),\qquad
 |P^nf(x)-\pi f|\le q^n\operatorname{Lip}(f)\int d(x,y)\,\pi(dy). \tag{3}
\]

Indeed, integrate the Lipschitz inequality against `pi`, using invariance. This proves all convergence statements below for bounded Lipschitz functions without assuming convergence of arbitrary unbounded exponentials.

Let `H(mu|pi)` be relative entropy, with natural logarithms. The entropy variational bound is

\[
 \int g\,d\mu\le H(\mu\mid\pi)+\log\int e^g\,d\pi. \tag{4}
\]

For bounded `g`, put `d rho=e^g d pi/(pi e^g)` and expand the nonnegative quantity `H(mu|rho)`. Nonnegativity follows from `u log u-u+1>=0`. For the nonnegative unbounded functions used below, apply the bounded result to truncations and pass by monotone convergence.

Suppose, for constants `A>0` and `L>0`, that all 1-Lipschitz `f` satisfy

\[
 \log\pi e^{\lambda(f-\pi f)}\le A\lambda^2,
 \qquad 0\le\lambda\le L. \tag{5}
\]

Define the convex, increasing, quadratic-then-linear function

\[
 \alpha_{A,L}(r)=\sup_{0\le\lambda\le L}(\lambda r-A\lambda^2)
 =\begin{cases}
 r^2/(4A),&0\le r\le2AL,\\
 Lr-AL^2,&r\ge2AL.
 \end{cases} \tag{6}
\]

Its derivative is `r/(2A)` before the join and `L` afterward, so it is continuously differentiable and convex. Optimizing the concave quadratic in `lambda` proves (6).

From (4)--(5), for every finite-entropy `mu`,

\[
 \boxed{\alpha_{A,L}(W_1(\mu,\pi))\le H(\mu\mid\pi).} \tag{7}
\]

Here finite entropy actually implies finite first moment: fix `o`, set `r_N=min(d(o,.),N)`, and choose any `0<lambda<=L`. Then (4)--(5) yield

\[
 \lambda\mu r_N\le H+\lambda\pi r_N+A\lambda^2
 \le H+\lambda\pi d(o,\cdot)+A\lambda^2.
\]

Let `N` tend to infinity. We can therefore apply (2); first use (4) with bounded truncations of `lambda(f-pi f)`, then take limits and the supremum over `f`, and finally optimize `lambda`. For infinite entropy, (7) is understood in the extended sense. The same optimization gives `pi(f-pi f>=r)<=exp(-alpha_{A,L}(r))` by Markov's inequality. Thus (7) permits exponential rather than purely Gaussian far tails.

## 2. Approach one: the established uniform one-step T1 theorem

Assume, in addition to (1), that for some `B>0`, every `P_x` satisfies

\[
 W_1(\rho,P_x)^2\le B H(\rho\mid P_x)\quad\hbox{for every probability }\rho. \tag{8}
\]

Then

\[
 \boxed{W_1(\mu,\pi)^2\le\frac{B}{\kappa(2-\kappa)}H(\mu\mid\pi).} \tag{9}
\]

To prove this, first take bounded 1-Lipschitz `f`. Exponential tilting gives the local Laplace bound

\[
 \log P_x e^{\lambda(f-P_x f)}\le B\lambda^2/4. \tag{10}
\]

For completeness, the tilted measure `rho` with density proportional to `e^{lambda f}` is bounded relative to `P_x` and has finite first moment. The exact entropy identity, (8), and (2) give

\[
 \log P_x e^{\lambda(f-P_x f)}
 =\lambda(\rho f-P_x f)-H(\rho\mid P_x)
 \le\lambda w-w^2/B\le B\lambda^2/4,
\]

where `w=W_1(rho,P_x)`. Scaling handles any Lipschitz constant. Apply (10) successively to `f,Pf,...,P^{n-1}f` and use (3):

\[
 P^ne^{\lambda f}(x)
 \le\exp\left(\lambda P^nf(x)+\frac{B\lambda^2}{4}
                \sum_{j=0}^{n-1}q^{2j}\right). \tag{11}
\]

For bounded `f`, both `f` and `e^{lambda f}` are Lipschitz. Equation (3) and the geometric series give

\[
 \log\pi e^{\lambda(f-\pi f)}\le\frac{B\lambda^2}{4(1-q^2)}.
\]

Clipping an arbitrary Lipschitz `f` to `[-R,R]`, using first-moment convergence for its mean and Fatou's lemma for its exponential, extends this estimate. Apply (4) and optimize over all `lambda>=0` to obtain (9).

If every transition support has diameter at most `Delta`, then (8) holds with `B=Delta^2/2`. One proof is the following bounded-variable argument. For a random variable in an interval of length `Delta`, the variance under every exponential tilt is at most `Delta^2/4`. Integrating the second derivative of its centered log-Laplace transform twice gives `log E e^{lambda(Y-EY)}<=lambda^2 Delta^2/8`. Combining this with (4), (2), and optimization gives (8). The variance bound follows from `Var(Y)<=(EY-a)(b-EY)<=(b-a)^2/4` for `Y in [a,b]`.

For a walk moving only to graph neighbors or staying put, `Delta<=2`, so (9) gives `W_1^2<=2H/[kappa(2-kappa)]`.

**Outcome.** This is established prior work, not a new result: Djellout--Guillin--Wu, Proposition 2.10, and Eldan--Lee--Lehec, Theorem 1.5 and Corollary 1.8. It settles a natural uniform-local-T1 subcase. It neither handles arbitrary non-Gaussian invariant measures nor justifies an inequality with `alpha(d)` inside an optimal-transport integral.

## 3. Approach two: retain local variance and a finite Laplace window

This approach uses the local assumptions in Ollivier's concentration argument rather than replacing actual variance by an all-parameter sub-Gaussian proxy.

Define

\[
 S=\frac12\sup_x\operatorname{diam}(\operatorname{supp}P_x),\qquad
 v(x)=\sup_{\operatorname{Lip}(f)\le1}\operatorname{Var}_{P_x}f.
\]

Assume `0<S<infinity`, that `v/kappa` is `C`-Lipschitz for some finite `C>=0`, and that `pi v>0`. In Ollivier's notation, `v(x)=sigma(x)^2/n_x`. Bounded support and the preceding variance argument give `0<=v<=S^2`; in particular `v` is bounded and integrable. Put

\[
 a=1-\kappa/2,\quad
 A=\frac{\pi v}{1-a^2}=\frac{\pi v}{\kappa(1-\kappa/4)},\quad
 L=\min\left\{\frac1{3S},\frac1{2C}\right\}, \tag{12}
\]

where `1/(2C)=infinity` when `C=0`. The nontrivial case `pi v>0` keeps (6) free of division by zero; no assertion about a degenerate case is needed here.

**Theorem.** Equation (5) holds with (12), hence so does the quadratic-then-linear transport bound (7).

**Proof.** If `g` has Lipschitz constant `b<=1`, its centered value under `P_x` lies in `[-2S,2S]`. Taylor's formula implies

\[
 P_xe^{\lambda(g-P_xg)}
 \le1+\tfrac12\lambda^2e^{2S\lambda}\operatorname{Var}_{P_x}g
 \le\exp(\lambda^2b^2v(x)), \tag{13}
\]

for `0<=lambda<=1/(3S)`, because `e^{2/3}<2`.

Fix bounded 1-Lipschitz `f` and `0<=lambda<=L`. Define

\[
 f_0=f,\qquad f_{j+1}=Pf_j+\lambda a^{2j}v. \tag{14}
\]

Inductively `Lip(f_j)<=a^j`: indeed

\[
 \operatorname{Lip}(f_{j+1})
 \le q a^j+\lambda\kappa C a^{2j}
 \le(q+\kappa/2)a^j=a^{j+1}. \tag{15}
\]

All these functions are bounded because `f` and `v` are bounded. Equation (13) gives `P e^{lambda f_j}<=e^{lambda f_{j+1}}`. Positivity of `P` and iteration now yield

\[
 P^ne^{\lambda f}\le e^{\lambda f_n},\qquad
 f_n=P^nf+\lambda\sum_{j=0}^{n-1}a^{2j}P^{n-1-j}v. \tag{16}
\]

For every fixed `j`, equation (3) gives `P^{n-1-j}v(x)->pi v`; the tail of the sum is bounded uniformly by `||v||_infinity sum_{j>=J}a^{2j}`. Therefore `f_n(x)->pi f+lambda A`. Applying (3) also to the bounded Lipschitz function `e^{lambda f}` proves (5) for bounded `f`. The clipping/Fatou argument used in approach one proves it for arbitrary 1-Lipschitz `f`. Section 1 completes (7). QED.

Writing `D^2=pi v/kappa`, one has `A=D^2/(1-kappa/4)<=4D^2/3`. This recovers the restricted Laplace estimate used in the proof of Ollivier's Theorem 33, with the geometric sum retained exactly. Applying convex duality to that estimate is also within the norm-entropy framework of Gozlan--Leonard, Theorem 3.17. No historical priority is claimed.

**Outcome.** A fully proved functional inequality retaining local variance and allowing non-Gaussian tails. The nonlinear function is applied to `W_1`; it is not a proof of the stronger, different transportation-cost assertion examined next.

## 4. Approach three: test the proposed cost inside the transport integral

For a nonnegative cost function `c`, write

\[
 \mathcal T_c(\mu,\pi)=\inf_{\gamma\in\Pi(\mu,\pi)}
                         \int c(d(x,y))\,\gamma(dx,dy). \tag{17}
\]

For convex increasing `alpha`, Jensen's inequality gives

\[
 \alpha(W_1(\mu,\pi))\le\mathcal T_\alpha(\mu,\pi). \tag{18}
\]

Thus (7) bounds the *smaller* quantity. The missing direction cannot be supplied in general.

Take `X={0,1}`, `d(0,1)=1`, `pi=(1/2,1/2)`, and `P_x=pi` at both states. This chain is reversible and has curvature `kappa=1`. For

\[
 \mu_\epsilon=(1/2+\epsilon,1/2-\epsilon),\qquad 0<\epsilon<1/2,
\]

exactly `epsilon` mass must cross between the two points. Consequently

\[
 W_1(\mu_\epsilon,\pi)=\epsilon,\qquad
 \mathcal T_c(\mu_\epsilon,\pi)=c(1)\epsilon \tag{19}
\]

whenever `c(0)=0`. On the other hand

\[
 h(\epsilon):=H(\mu_\epsilon\mid\pi)
 =(1/2+\epsilon)\log(1+2\epsilon)
 +(1/2-\epsilon)\log(1-2\epsilon)
 \le4\epsilon^2. \tag{20}
\]

The last estimate uses `log u<=u-1`, or equivalently `H(mu|pi)<=chi^2(mu|pi)`. Hence for every `c(1)>0` and every finite `K>0`, the assertion `T_c<=K H` fails for sufficiently small `epsilon`. Even perfect coarse Ricci curvature does not remove this atomic small-mass obstruction.

The obstruction applies to the *same* profile produced by (12). In this example,

\[
 S=1/2,\quad v=1/4,\quad C=0,\quad A=1/3,\quad L=2/3,
 \quad \alpha_{A,L}(1)=14/27.
\]

For `epsilon=1/16`, equations (19)--(20) give the exact certificate

\[
 \mathcal T_\alpha=7/216,
 \qquad H\le1/64,
 \qquad \mathcal T_\alpha-H\ge29/1728>0. \tag{21}
\]

Meanwhile `alpha(W_1)=3/1024`, which is fully consistent with (7).

**Outcome.** A complete counterexample to the correction-free pointwise-cost variant. It is not a counterexample to Problem J, which explicitly allows modified formulations and additive corrections. It also does not rule out costs vanishing below a discrete resolution scale, weak transport costs, or squared total costs.

## 5. Approach four: add a defect, and quantify its limitations

### 5.1 The least defect on the two-point test space

Let `c=c(1)>0` and `K>0`. For the uniform two-point measure, the least `b` such that

\[
 \mathcal T_c(\mu,\pi)\le K H(\mu\mid\pi)+b
 \quad\hbox{for all }\mu
\]

is exactly

\[
 \boxed{b_{\min}=K\log\cosh\left(\frac{c}{2K}\right).} \tag{22}
\]

To see this, symmetry reduces the supremum to `0<=epsilon<=1/2` of `c epsilon-K h(epsilon)`. Differentiation gives

\[
 h'(\epsilon)=\log\frac{1+2\epsilon}{1-2\epsilon},\qquad
 h''(\epsilon)=\frac4{1-4\epsilon^2}>0.
\]

The unique maximum is attained at `epsilon=(1/2)tanh(c/(2K))`. Substituting, using `1+-tanh z=e^{+-z}/cosh z`, yields (22); continuity includes both endpoint measures. For the profile in (21) and `K=1`, the exact least defect is `log cosh(7/27)`, not zero. Equation (21) already gives the rational lower bound `29/1728` for any admissible defect.

### 5.2 A general, explicitly defective transportation-cost bound

Assume (5). For `0<eta<=L`, use the profile `alpha_{A,eta}` of (6), whose slope is at most `eta`; in particular `0<=alpha_{A,eta}(r)<=eta r`. Fix `o in X` and write `m=pi d(o,.)`. Then

\[
 \boxed{\mathcal T_{\alpha_{A,\eta}}(\mu,\pi)
 \le H(\mu\mid\pi)+2\eta m+A\eta^2.} \tag{23}
\]

Indeed, (5) for the distance function gives `log pi exp(eta d(o,.))<=eta m+A eta^2`. Formula (4), applied by truncation, implies

\[
 \eta\int d(o,x)\,\mu(dx)\le H(\mu\mid\pi)+\eta m+A\eta^2.
\]

Use the product coupling `mu x pi`, the triangle inequality, and the upper bound `alpha_{A,eta}(r)<=eta r`. This proves (23). Under (1), one may replace `m` by `J(o)/kappa`, where `J(o)=integral d(o,y)P_o(dy)`: by the triangle inequality and contraction,

\[
 m=W_1(\delta_o,\pi)\le J(o)+W_1(P_o,\pi)\le J(o)+q m.
\]

Therefore a version depending only on explicitly available local data is

\[
 \mathcal T_{\alpha_{A,\eta}}(\mu,\pi)
 \le H(\mu\mid\pi)+\frac{2\eta J(o)}\kappa+A\eta^2. \tag{24}
\]

**Outcome.** This is a genuine quadratic-then-linear transportation cost with an additive term, under stated local hypotheses. It gives one literal coarse formulation, but the proof uses an independent coupling and bounds the cost linearly; it does not recover the sharper Gaussian small-deviation estimate of (7). Its defect can be much larger than the optimal one in (22), depends on a global radius or a base-point jump, and no optimality or dimension-free sharpness is asserted. The scalar inequality (7), the correction-free assertion refuted in (21), and the deliberately weak defective estimate (23) must not be conflated.

## 6. Approach five: test tail assumptions and the continuous-time scale

### 6.1 Curvature and bounded local variance alone allow polynomial tails

Let `X=N_0` with the usual distance, let

\[
 Z=\sum_{n\ge0}(n+1)^{-4},\qquad \pi(n)=Z^{-1}(n+1)^{-4},
 \qquad P_x=\pi \quad\hbox{for all }x.
\]

Then `kappa=1`, `pi` is invariant, and its first and second moments are finite. The local variance function is constant and bounded: for independent `Y,Y'` of law `pi`,

\[
 \operatorname{Var}(f(Y))=\tfrac12 E(f(Y)-f(Y'))^2
 \le\tfrac12 E(Y-Y')^2=\operatorname{Var}(Y),
\]

with equality for `f(n)=n`. However `S=infinity`. For `mu=delta_N`,

\[
 W_1(\delta_N,\pi)\ge N-\pi n,\qquad
 H(\delta_N\mid\pi)=\log Z+4\log(N+1). \tag{25}
\]

A nontrivial quadratic-then-linear function grows linearly at infinity. Thus neither `alpha(W_1)<=K H+b` nor `T_alpha<=K H+b` can hold for fixed finite `K,b` and a profile with positive eventual slope. For the second statement, apply (18). This proves that no such theorem can follow from positive curvature and bounded local variance alone. The reset-kernel obstruction is already noted in Ollivier's discussion before Theorem 33.

### 6.2 A Poisson invariant measure also prevents a global Gaussian claim

Fix `theta>0` and `0<q<1`. On `N_0`, define a single transition from `n` as the sum of independent variables

\[
 \operatorname{Binomial}(n,q)+\operatorname{Poisson}(\theta(1-q)). \tag{26}
\]

Poisson thinning proves that `pi=Poisson(theta)` is invariant: the probability generating function of the output from a Poisson input is

\[
 \exp(\theta((1-q+qz)-1))\exp(\theta(1-q)(z-1))
 =\exp(\theta(z-1)).
\]

Couple transitions from `n<=m` by retaining the same first `n` Bernoulli trials and the same Poisson variable, and use `m-n` additional Bernoulli trials for the second transition. The expected difference is `q(m-n)`. The difference of the means gives the reverse `W_1` bound, so the curvature is exactly `1-q`. The local variance is

\[
 v(n)=nq(1-q)+\theta(1-q),\qquad v(n)/\kappa=qn+\theta. \tag{27}
\]

The variance identity follows from the independent-copy Lipschitz argument above, with equality for the identity function. Here `v/kappa` is Lipschitz but `S=infinity`.

For `delta_N`, `W_1>=N-theta` while

\[
 H(\delta_N\mid\pi)=\theta-N\log\theta+\log(N!)
 \le\theta+N\log(N/\theta).
\]

Consequently `W_1^2/H` is unbounded. This is a fully explicit positive-curvature example excluding a global finite-constant Gaussian T1 inequality, without invoking a limiting continuous-time construction.

### 6.3 A variance-sensitive bound remains finite under lazification

A separate exact sanity test shows why approach two is useful even on a finite state space. On `{0,1,2}` with line distance, take

\[
 P=\begin{pmatrix}3/4&1/4&0\\1/8&3/4&1/8\\0&1/4&3/4\end{pmatrix},
 \qquad \pi=(1/4,1/2,1/4).
\]

Detailed balance gives invariance. On the line, `W_1` is the sum of absolute differences of cumulative probabilities. The adjacent transition distances are `3/4`, and the distance between the endpoint transitions is `3/2`. Thus `kappa=1/4`. The local variances are `(3/16,1/4,3/16)`; equality is achieved by `f(i)=i`, and the independent-copy argument supplies the upper bound. Hence `S=1`, `C=1/4`, `A=14/15`, and `L=1/3`.

For `P_h=(1-h)I+hP`, `0<h<=1`, the same calculation gives

\[
 \kappa_h=h/4,\qquad
 v_h=(h/4-h^2/16,\;h/4,\;h/4-h^2/16),
\]

\[
 C_h=h/4,\quad S_h=1,\quad
 A_h=\frac{1-h/8}{1-h/16},\qquad L_h=1/3. \tag{28}
\]

For example the two adjacent cumulative differences for the first pair are `1-3h/8` and `h/8`, giving `W_1=1-h/4`. The other pair is symmetric; the endpoint distance follows by summing. The conditional variance formula follows by expanding the first two moments of the lazy transition. As `h` decreases to zero, `A_h->1` and `L_h` stays fixed. The simpler diameter-based constant from approach one is `2/[kappa_h(2-kappa_h)]`, which diverges. Thus this nontrivial test verifies that the restricted-Laplace method need not lose the local-variance scale under small time steps. It is not a proof of a general continuous-time limiting theorem.

## 7. What is established, and what is not

The preceding sections give five completed mathematical approaches, including two positive transport formulations and exact negative controls. Specifically:

1. The uniform-local-T1 regime was settled in earlier literature.
2. Ollivier's bounded-granularity/Lipschitz-variance argument gives an explicit quadratic-then-linear function of `W_1`, with complete proof here.
3. Replacing that function of `W_1` by its pointwise transportation cost, without a defect, is false even for a two-point curvature-one chain.
4. A defective pointwise-cost inequality is available, and its least defect is determined exactly on the two-point test. The general defect proved here is weak.
5. Curvature alone does not control tails; explicit reset and Poisson kernels prevent erroneous extensions. A finite-chain lazification test confirms the variance-sensitive scaling of the positive result.

**The remaining gap in this investigation is the stronger coarse transportation formulation suggested by the source:** a useful pointwise or appropriately modified transport cost, with a quantitatively controlled small-scale correction that recovers the intended concentration strength in the relevant generality. Equation (23) supplies a weak version, not that stronger claim. The original item does not fix an optimal defect, a universal quantifier over all local assumptions, or one mandatory notion of modified transport; we do not invent such a theorem and claim it settled.

No counterexample here refutes all versions allowed by Problem J. No cited result was verified to settle the entire exploratory program. Accordingly this package records **unresolved/partial progress after five substantive approaches**, not a new solution and not an assertion that all possible later resolutions have been excluded by an exhaustive literature review.
