# Independent adversarial audit: AMR-039-0010

Date: 2026-10-04 UTC  
Problem: 4000010, rank 553, Ollivier's Problem J  
Frozen candidate manifest SHA-256: `b287f898f2dafe79381e57132f8fe6f476c3b0b7d73dc6e9d9852de095dc710b`

## Verdict

**PASS as unresolved partial progress. No blocking mathematical error was found.** The candidate does not prove the whole exploratory problem and does not claim novelty. Its proposed `unsolved`, `5/5` accounting is consistent with the five explicitly described approaches, provided `5/5` is read as approach accounting rather than five independent discoveries or a completed solution.

The uniform-local-T1 theorem is established prior work. The finite-window scalar inequality, two-point obstruction, exact two-point defect, weak general defect, and tail/scaling controls are valid with the stated hypotheses. In particular, the two-point rational margin `29/1728` is a lower bound on the actual cost-minus-entropy gap, not its exact value. The minimum additive defect for the specified profile is exactly `log cosh(7/27)`.

The entire frozen candidate was left unchanged. All seven content hashes and the manifest hash agree. The recorded verification output was reproduced by calling the verifier's calculation function without its file-writing entry point. The additional checks supplied with this audit use exact rational polynomial identities and do not promote finite numerical samples to proofs.

Two nonblocking interpretation notes should accompany any summary:

1. Finite transition-support diameter already permits a global, possibly much weaker, Gaussian T1 bound. The finite-window result preserves the local-variance scale; it does not, under the same finite-diameter hypotheses, establish a class of invariant measures failing every Gaussian T1 inequality. The Poisson and polynomial-tail examples have infinite transition-support diameter and are expressly outside those hypotheses. The manuscript's references to permitting non-Gaussian tails are appropriately read as descriptions of its mixed concentration profile and of the broader problem's scale-sensitive motivation.
2. The exact two-point defect formula uses the usual normalization `c(0)=0`, as in the preceding two-point calculation. It should not be quoted for a general cost with an arbitrary nonzero diagonal. The profile actually used has zero diagonal, so no stated application is affected.

## 1. Primary question and literature boundary

The original [May 2008 problem list](https://www.yann-ollivier.org/rech/publs/problems_curvmarkov.pdf), including printed page 3 visually and in extracted text, was read. Problem J asks for functional-inequality formulations of concentration with room for small-scale or small-mass corrections and suggests a quadratic-then-linear transportation cost. It does not specify one unique cost, exact defect, or universal quantifier set. Adjacent Problem I concerns weakening local assumptions while retaining variance-sensitive continuous-time scaling. The candidate distinguishes these concerns rather than treating a finite test of lazification as a continuous-time theorem.

Relevant statements and complete arguments were checked in the following primary sources:

- [Ollivier, JFA 2009](https://doi.org/10.1016/j.jfa.2008.11.001): Definition 18; Theorem 33, Lemma 38 and the full finite-Laplace iteration; Remarks 35–37; reset-kernel warnings and the binomial/Poisson discussion. The candidate's `S` is the source's half support diameter. Its `v` is the maximal variance of a 1-Lipschitz function, namely `sigma(x)^2/n_x`. Lipschitz functions on a support extend to the ambient metric space with the same constant, so the two definitions agree. The candidate assumes the variance function itself is Lipschitz. This is a sufficient subcase; the source also allows a Lipschitz majorant.
- [Djellout–Guillin–Wu, Proposition 2.10](https://arxiv.org/abs/math/0410172): both assumptions, the fixed-point argument and the full invariant-measure T1 proof. Their normalization is `W1^2 <= 2 C H`. Thus the candidate's constant `B/[kappa(2-kappa)]` agrees after setting `B=2C` and `r=1-kappa`.
- [Eldan–Lee–Lehec, v2](https://arxiv.org/abs/1604.06859v2): Theorem 1.5, Corollary 1.8, the duality proof and the complete coupling/drift proof through Section 2.3, as well as the acknowledgment of Djellout–Guillin–Wu. The reading copy identifies itself as the 27 December 2016 revision. Uniform one-step T1 is essential in its general theorem. The graph specialization uses support diameter at most two. Neither provides arbitrary-tail Gaussian concentration from curvature alone. The candidate correctly credits the 2004 antecedent, rather than assigning first priority to the later 2016/2017 work.
- [Fathi–Shu, Bernoulli 2018](https://doi.org/10.3150/16-BEJ892): the reversible, normalized-rate graph setup; Theorem 1.13; and all of Section 5, including Lemma 5.1. Their discussion expressly excludes T1 in the unrestricted setting of Ollivier's examples. The weak-quadratic-transport conclusions use an exponential curvature-dimension hypothesis elsewhere in the paper; they cannot simply be substituted for a coarse-Ricci assumption.
- [Gozlan–Léonard](https://doi.org/10.1007/s00440-006-0045-y): the transportation-cost and norm-entropy definitions, complete proof of Theorem 3.7, Corollary 3.14, and Theorems 3.15 and 3.17. For the candidate profile the monotone conjugate equals `A lambda^2` on `[0,L]` and is infinite beyond `L`. A finite Laplace window therefore fits the scalar norm-entropy framework. This says nothing by itself about putting the nonlinear profile inside the coupling integral.

The available source reading-copy hashes agree with the source gate's hashes. Identity and theorem scope check out. This audit did not repeat remote repository searches, re-query a catalogue, or conduct a new exhaustive current-literature search. The earlier repository-search narrative in the source gate is consequently not independently certified here. The appropriate conclusion is that this package remains partial, not that every possible later solution has been excluded.

## 2. Stationarity, support, entropy and constants

The candidate expressly assumes a Polish metric space, a Markov kernel with finite first moments, and an invariant probability with finite first moment. No reversibility or irreducibility is needed in its positive semigroup arguments. Integrating the pointwise Lipschitz contraction against the invariant measure gives

`|P^n f(x)-pi f| <= (1-kappa)^n Lip(f) integral d(x,y) pi(dy)`.

This suffices for the bounded Lipschitz limits actually used. In particular, the candidate does not silently infer convergence of unbounded exponentials from W1 convergence: it first works with bounded `f`, for which `exp(lambda f)` is bounded Lipschitz, and then applies clipping and Fatou's lemma.

The entropy orientation is consistently `H(mu|pi)`. The variational bound follows from a tilt of `pi`, and finite entropy plus a positive distance-function Laplace parameter implies a finite first moment for `mu` by monotone truncation. For a signed Lipschitz function, once this first moment is known, clipped integrals converge; the exponential passage can use domination by `1+exp(lambda(f-pi f))`. Thus the duality and limiting steps are valid. Infinite-entropy statements are extended-value inequalities only.

The local T1-to-Laplace argument has the right normalization: `lambda w-w^2/B <= B lambda^2/4`. Summing `(1-kappa)^(2j)` gives `1/[kappa(2-kappa)]`. A variable of range `Delta` has tilted variance at most `Delta^2/4`, hence log-Laplace constant `Delta^2/8` and local T1 constant `B=Delta^2/2`. The neighbor-walk specialization `B=2` is correct; it requires graph-distance jumps of at most one.

There is no hidden dimension-free claim. The dimension dependence sits in maximal Lipschitz variance and in the curvature/metric scale. Under metric multiplication by `r>0`, the constants transform as `v -> r^2 v`, `S -> r S`, `C -> r C`, `A -> r^2 A`, `L -> L/r`. Consequently `alpha_{r^2 A,L/r}(r W1)=alpha_{A,L}(W1)`, as required.

## 3. Restricted Laplace estimate and scalar transport

For `b`-Lipschitz `g`, `b<=1`, a transition support of diameter `2S` makes the centered value lie in `[-2S,2S]`. Taylor's remainder is therefore bounded by

`(lambda^2/2) exp(2S lambda) Var(g)`.

The coefficient is at most `lambda^2 b^2 v` for `lambda<=1/(3S)`. This analytic estimate was independently checked: a Taylor series through degree five and the geometric tail starting at degree six give

`exp(2/3) <= 404671/207765 < 2`.

Put `a=1-kappa/2`. In the nonlinear iteration, the added variance term has Lipschitz constant at most `lambda kappa C a^(2j)`. Since `lambda C<=1/2` and `a^(2j)<=a^j`, this combines with `q a^j` to give `a^(j+1)`. The induction is valid also for `kappa=1` and for `C=0` under the stated reciprocal convention.

Bounded support gives `0<=v<=S^2`, so every iterate is bounded. For the series in the iterate formula, fixed terms converge by the Lipschitz estimate and the remaining terms are uniformly bounded by a geometric tail. Its limit is exactly

`pi f + lambda pi v/[kappa(1-kappa/4)]`.

The resulting `A` is positive by the explicit nondegeneracy assumption. Optimization over the closed interval `[0,L]` gives the stated quadratic branch, linear branch and join `2AL`. This establishes `alpha(W1)<=H` and the associated mixed concentration bound. It does not establish `T_alpha<=H`.

## 4. Nonlinear cost and the atomic obstruction

For each coupling, Jensen's inequality gives `alpha(integral d)<=integral alpha(d)`. Taking the optimal distance and then the infimum of the right side yields `alpha(W1)<=T_alpha`. The direction in the candidate is correct.

On the uniform two-point reset chain, both transition laws equal the invariant law, so curvature is exactly one and the chain is reversible. Perturbation by `epsilon` moves exactly `epsilon` units of mass. With zero diagonal cost this yields `T_c=c(1)|epsilon|`, whereas entropy is quadratic to first order. More concretely, `log u<=u-1` gives `H<=4 epsilon^2`. For any finite `K>0`, choosing `epsilon<c(1)/(4K)` (and below one half) disproves `T_c<=K H`.

Independently substituting `S=1/2`, `v=1/4`, `C=0`, `kappa=1` gives `A=1/3`, `L=2/3`, and cost at distance one `14/27`. At `epsilon=1/16`, the transportation cost is `7/216`, the chi-squared entropy upper bound is `1/64`, and their difference is `29/1728`. The scalar profile at the same W1 is `3/1024`, so there is no contradiction to the scalar theorem.

For the optimal additive defect, write `z=c/(2K)` and `t=2 epsilon`. Then

`h(epsilon) = ((1+t)/2) log(1+t) + ((1-t)/2) log(1-t)`.

The derivative of `c epsilon-K h(epsilon)` vanishes only at `t=tanh z`; its second derivative is strictly negative inside the interval. At this point `h=z tanh z-log cosh z`, so the objective is exactly `K log cosh z`. The endpoint values are covered by continuity and cannot exceed this interior maximum. This proves the formula over all two-point probability measures, without a numerical fit.

## 5. General defective cost

The distance function's Laplace bound gives

`eta mu d(o,.) <= H(mu|pi)+eta pi d(o,.)+A eta^2`.

The product coupling and `alpha_{A,eta}(r)<=eta r` add one further `eta pi d(o,.)`. This proves the stated defect. The radius estimate follows from

`m=W1(delta_o,pi)<=J(o)+W1(P_o,pi)<=J(o)+(1-kappa)m`.

The last inequality is valid by the kernel contraction integrated against `pi`, using invariance and the assumed first moment. Thus `m<=J(o)/kappa` has the correct coefficient and orientation.

This is a valid but weak estimate. Since it uses only the linear upper bound on the cost, it supplies no sharp Gaussian small-deviation conclusion, and its radius term can carry substantial dimension dependence. The candidate expressly acknowledges these limits. It is not justified to call it an optimal correction or a resolution of the broader requested formulation.

## 6. Tail and lazification stress tests

For the reset law proportional to `(n+1)^(-4)`, the first and second moments are finite. The independent-copy identity bounds every Lipschitz variance by the identity function's variance, with equality for that function. Curvature is one, yet `S` is infinite. A point mass at `N` has distance at least `N-E n` and entropy `log Z+4 log(N+1)`. Every fixed positive eventual slope therefore defeats any finite entropy coefficient and additive defect. Jensen transfers this obstruction to the integral cost.

For binomial thinning plus an independent Poisson immigration variable, generating functions prove Poisson stationarity. A monotone coupling gives `W1<=q|m-n|`; the difference of means gives equality. The local variance is exactly `(1-q)(qn+theta)`, so `v/kappa=qn+theta`. Transition supports are unbounded. At a point mass, entropy is at most `theta+N log(N/theta)` while squared distance is at least `(N-theta)^2` for large `N`. Their ratio diverges. This disproves global Gaussian T1 for this example without assuming a continuous-time limit or omitting a jump-size hypothesis.

The lazified three-state example was recomputed symbolically for every `0<h<=1`. The adjacent cumulative differences are `1-3h/8` and `h/8`, in either order, and both are nonnegative throughout this interval. The endpoint pair has two differences `1-h/4`. Thus every pair gives curvature `h/4`. Direct first and second moments yield endpoint variance `h/4-h^2/16` and middle variance `h/4`. Dividing by curvature gives endpoint value `1-h/4` and middle value one, hence `C_h=h/4`.

The support diameter remains two, so `S_h=1`, `L_h=1/3`, and

`A_h=(1-h/8)/(1-h/16) -> 1`.

The diameter-only coefficient is asymptotic to `4/h` and diverges. These are exact identities and limits, not values extrapolated from the original sampled `h` values. They verify this example's scale, not an interchange-of-limits theorem for arbitrary generators.

## 7. Reproducibility and disposition

Run `python3 independent_verify.py` from this audit directory. It uses only the standard library, checks the frozen manifest, reproduces the candidate calculation without writing into it, and writes `independent_results.json` in this directory. Its lazy-chain controls are exact polynomial identities for the whole stated parameter interval. The analytic justifications above remain essential for the universal and infinite-state conclusions.

The audit adds only authored review, source metadata, original verification code/results and its own manifest. It contains no redistributed papers, extracted source texts, dataset rows, screenshots, private workspace paths or unrelated material. No remote state was changed.

**Disposition:** acceptable as a carefully delimited partial-results package. Preserve the unsolved status, no-novelty statement, precise local hypotheses, distinction between scalar and integral costs, and explicit remaining gap.
