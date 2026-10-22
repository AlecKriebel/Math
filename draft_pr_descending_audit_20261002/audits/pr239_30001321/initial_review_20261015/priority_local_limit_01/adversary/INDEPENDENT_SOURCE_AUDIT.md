# Weighted local-limit and stationary-density inference audit

Author: independent adversarial subagent, 2026-10-15 UTC.

## Exact question and conclusion

The target is the following statement for one fixed i.i.d. nearest-neighbor
space-time environment law with `0<p<1` almost surely. For **every** deterministic
`M_N -> infinity`, every deterministic partition into `M_N`-site intervals,
every `epsilon>0`, and every `K>0`,

`P_env(sum_I |mu_N^omega(I)-alpha_N(I)| > epsilon) = O(N^-K)`.

This audit does not adjudicate the submitted final-segment proof. It tests whether
existing stationary-density, covariance, and weighted-local-limit statements
already supply that conclusion. They do not supply it by the direct inference
examined here. There are both model-scope gaps and quantitative gaps. Section 4
gives a rigorous obstruction to inferring the target tail from even stronger
summary estimates than the finite-moment local-limit bounds inspected here.

**Crucial limitation:** the synthetic construction in Section 4 is not generated
by the target i.i.d. space-time RWRE. It refutes an implication between abstract
estimates, not the target theorem. The transport equation and i.i.d. environment
structure can support additional arguments; this audit does not rule them out.

No parent conclusion was read during the independent derivation. The submitted
`TARGET.json` and submitted candidate `PROOF.md` were read only to fix the claim
and distinguish the argument being tested from the candidate's separate closure.

## 1. Joseph–Rassoul-Agha–Seppäläinen: what is actually proved

Full primary source: *Independent Particles in a Dynamical Random Environment*,
Springer Proceedings in Mathematics & Statistics 283 (2019), printed pp. 75–121,
DOI `10.1007/978-3-030-15338-0_4`.

URL: https://www.math.utah.edu/~firas/Papers/walkers.pdf

The source was independently fetched; its PDF hash matches the parent's pinned
copy. Proposition 3.1, printed pp. 88–89, constructs

`f_N(omega) = sum_z pi^omega_{-N,0}(z,0)`

as a nonnegative martingale. It converges almost surely and in `L2` to a density
`f`, with `E f=1`, `E f^2<infinity`, measurable with respect to the environment's
past, and satisfying the stationary transport identity (3.1). Lemma 3.2 addresses
strict positivity. This is a **column sum from all starting sites**, not the
single-origin kernel `pi^omega_{0,N}(0,x)`.

Theorem 1.2, printed p. 80, identifies its spatial covariance by a Fourier formula
and `Var f=beta^-1-1`. Corollary 1.3, p. 81, gives zero off-diagonal covariance
for a one-dimensional two-consecutive-site jump support. These are second-order
statements; zero covariance does not assert independence or exponential
concentration of nonlinear norms.

The source assumes bounded jumps, product space-time environment, nondegeneracy
(1.4), and averaged span one (1.5). Literal jumps `{-1,+1}` do not have span one:
they lie in the coset `-1+2Z`. To use this theorem on the target one must restrict
to a parity class and shear coordinates, for example `Y_t=(X_t+t)/2`, obtaining
`{0,1}` jumps and an i.i.d. environment on the reachable parity space-time lattice.

For this sheared model write `q=E p`, `a=q(1-q)`, `delta=E[p(1-p)]`. Direct
substitution into (1.11)–(1.13) gives, away from theta zero,

`(1-lambda(theta))/(1-lambdabar(theta)) = delta/a`,

so `beta=delta/a` and `Var f=a/delta-1=Var(p)/delta`; distinct spatial shifts
are uncorrelated. This verifies the natural parameter translation without
silently dropping parity.

Theorem 1.1(b) gives convergence in distribution to equilibrium for an infinite
particle system initially stationary and ergodic in space in dimensions 1 or 2.
The source does not state a quantitative single-source weighted LLT or the target
coarse-L1 environment tail. Convergence of this different process cannot simply
be substituted for such a theorem.

## 2. Dunlap–Gu: a quantitative weighted LLT, in another model

Full primary sources inspected independently:

* Author-hosted PDF dated May 27, 2021:
  https://www.math.cmu.edu/~yug2/papers/flow.pdf
* Latest arXiv v3, submitted December 8, 2021:
  https://arxiv.org/pdf/2105.07907v3

Title: *A quenched local limit theorem for stochastic flows*; journal reference
J. Functional Analysis 282 (2022), no. 6, 109372,
DOI `10.1016/j.jfa.2021.109372`.

Both inspected versions' Theorem 1.1 has the same one-dimensional estimate

`sup_x E|u(t,x)-G_t(x)U(t,x)|^2 <= C t^(-4/3) log t`,

with positive space-time stationary `U`, `EU=1`, and spatial covariance bound
`|Cov(U(t,x),U(t,y))| <= C(1+|x-y|)^-d`. The latest version additionally states
temporal covariance decay `(1+|t-s|)^(-(d-epsilon)/4)` in (1.11). These are
finite-moment bounds, not superpolynomial probability bounds for a coarse-L1 norm.

The dynamics use a Brownian particle, independent molecular diffusivity `nu>0`,
and a Gaussian velocity field white in time with smooth compactly supported
spatial covariance. They are not the target lattice model with arbitrary
elliptic i.i.d. transition law. The authors' comparison to discrete results is
useful context, but does not itself establish a transfer theorem.

For perspective on rates, in `d=1` the square-root of the local error bound is
`C t^(-2/3) sqrt(log t)`. Integrating over a central window of length
`R sqrt(t)` gives an **expected** L1 error at most
`C R t^(-1/6) sqrt(log t)` by Fubini and Cauchy–Schwarz. Markov gives only a
polynomial upper bound at fixed `R`. It does not turn that bound into `O(t^-K)`
for every `K`. Stronger probability or high-moment estimates with improving
exponents would be required, or a separate concentration mechanism.

Version history was checked from https://arxiv.org/abs/2105.07907:
v1 May 17, 2021; v2 May 27, 2021; v3 December 8, 2021. The unversioned PDF
fetched in this audit was byte-identical to the explicitly fetched v3 PDF.

## 3. Discrete references [12] and [17]

### [17]: primary full source obtained

Deuschel–Guo, *Quenched local central limit theorem for random walks in a
time-dependent balanced random environment*, arXiv:1710.05508v2:
https://arxiv.org/pdf/1710.05508v2

The abstract and standing assumptions (pp. 1–2) specify `d>=2`, continuous time,
balanced transition rates, uniform ellipticity, and ergodicity under space-time
shifts. Balance is pointwise zero local drift. In a one-dimensional discrete-time
nearest-neighbor model it would force `p=1/2` at every site; subtracting a mean
drift does not make a random local drift balanced.

Theorem 4 (p. 4) is an almost-sure uniform local limit for the normalized heat
kernel `q^omega=p^omega/rho^omega`. It has no stated deterministic quantitative
rate or environment tail for its convergence threshold. Theorem 7 supplies
positive and negative finite-moment heat-kernel estimates. Neither the model
scope nor the quantitative conclusions directly give the target assertion.

Current arXiv history checked at https://arxiv.org/abs/1710.05508: v1 October 16,
2017; v2 December 3, 2019, still the latest. Its internal title-page date is
December 4, 2019. This distinguishes the submission timestamp from manuscript
date.

### [12]: no full-source claim

Boldrighini–Minlos–Pellegrinotti, *Central limit theorem for a random walk in
dynamical environment: integral and local*, Theory Stochastic Processes
5(21) (1999), no. 3–4, pp. 16–28.

The original full research text was not obtained. The journal's public archive
https://tsp.imath.kiev.ua/published/index.html lists back to 2005; the institutional
record https://iris.uniroma1.it/handle/11573/28307 has no attached full text.
Those metadata and DG's account are not a substitute for reading the original.
Accordingly no theorem-level assertion about BMP1999 is promoted here. In
particular, DG's reported `|x| << t^(1/3)` restriction is recorded only as DG's
description, not independently verified BMP1999 content.

## 4. Exact obstruction to the finite-moment/qualitative-LLT inference

Let `alpha_N` be the exact endpoint mass of the ordinary symmetric nearest-
neighbor walk after `N` steps from zero. Let `B_N` be Bernoulli with
`P(B_N=1)=N^-2`, and let `S_N` be an independent symmetric sign. Set `c=1/2`,
`sgn(0)=0`, and define a random probability measure

`mu_N(x)=alpha_N(x)[1+c B_N S_N sgn(x)]`.

These measures preserve positivity on every reachable site. Symmetry gives
`sum_x alpha_N(x)sgn(x)=0`, so their total mass is exactly one and
`E mu_N(x)=alpha_N(x)`.

Take the stationary corrector `U(t,x)=1` identically. Its mean is one and all
spatial and temporal covariances vanish. The local error satisfies

`E|mu_N(x)-alpha_N(x)U(N,x)|^2
 = c^2 N^-2 alpha_N(x)^2 sgn(x)^2 <= C N^-3`,

using the standard binomial maximum-mass estimate. This is stronger than the
one-dimensional DG error exponent at the level of these abstract estimates.
Also `sum_N P(B_N=1)<infinity`, hence by the first Borel–Cantelli lemma
`mu_N=alpha_N` for all sufficiently large `N`, almost surely. This is stronger
than a bare almost-sure local-limit conclusion.

Nevertheless choose any integer `M_N -> infinity`, for example
`ceil(log(N+1))`, and the deterministic interval partition
`Q_k=[kM_N,(k+1)M_N) intersect Z`, `k in Z`. No cell contains both a negative
and a positive integer. Therefore exactly

`sum_k |mu_N(Q_k)-alpha_N(Q_k)|
 = c B_N sum_{x!=0}alpha_N(x)
 = c B_N[1-alpha_N(0)]`.

Since `alpha_N(0)->0`, for every fixed `epsilon<c`, eventually

`P(sum_k |mu_N(Q_k)-alpha_N(Q_k)|>epsilon) = N^-2`.

This is not `O(N^-K)` for `K>2`. The example simultaneously has the exact
binomial annealed law, exact probability normalization, a constant stationary
corrector with stronger than required covariance control, a very strong local
L2 error rate, and eventual almost-sure exact equality. Even these properties
together do not imply the desired probability rate. **It is not a target-model
counterexample:** no claim is made that its measures arise from one fixed i.i.d.
space-time nearest-neighbor environment. It isolates precisely the extra
information that an inference based on those summaries loses.

`check_rare_event_obstruction.py` verifies the finite-N normalization, exact
annealed law, binomial local-error identity, and exact coarse norm with rational
arithmetic; the proof above handles asymptotics without numerical assumptions.

## 5. Second-order stationary information and the remaining bridge

For a stationary field `f_x` with mean one and zero off-diagonal covariance,
`Var(sum_{x in I}(f_x-1))=|I| Var(f_0)`. Applied to deterministic diffusive weights,
this gives qualitative coarse averaging in expectation when block lengths diverge.
It does not give an arbitrary-power tail. Even an **independent** positive mean-one
Pareto field with tail exponent `r>2` has finite variance and zero off-diagonal
covariance, while

`P(n^-1 sum_{j=1}^n f_j > 2)
 >= P(max_{j<=n} f_j > 2n) >= c_r n^(1-r)`

for sufficiently large `n`. Thus the asserted covariance data alone cannot supply
strong concentration. This field need not satisfy JRS's stationary transport
identity and is not claimed to arise as their `f`.

The strongest supported bridge is qualitative: a suitable single-source
weighted approximation plus covariance averaging can explain why expected
coarse-L1 distance vanishes at every diverging scale. To recover the target's
superpolynomial probability statement one must additionally prove concentration
or arbitrary-order moments for the full norm, with estimates that remain useful
when `M_N` diverges arbitrarily slowly. Merely replacing the missing statement by
one about concentration of the stationary field transfers the central difficulty.

Status of this route: **blocked as a direct inference from the inspected
stationary/covariance/local-LLT summaries**. It can reopen with a concrete
quantitative mechanism exploiting the target's independent space-time dynamics.
This is compatible with the submitted proof having such an additional mechanism;
the independent final-segment argument is outside this source-inference audit.

## Reproducibility and scope

`PRIMARY_RETRIEVAL.json` records URLs, retrieval UTC timestamps, bytes, PDF and
extracted-text SHA256 values. `METADATA_RETRIEVAL.json` separates metadata and
failed retrievals. Full third-party PDFs, text extractions, and HTML are private
reading objects under ignored `private_reading/`; none is in the authored
manifest. No communication outside this research team, Git/index/ref operations,
or provider mutations were performed.
