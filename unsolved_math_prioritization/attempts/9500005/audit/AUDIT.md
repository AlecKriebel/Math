# Independent mathematical audit

Problem 9500005 / AMR-094-0005, Burdzy Problem 5. Audit date: 8 October 2026.

## Decision

Accept the frozen packet as an accurately limited collection of partial results and obstructions. Both original questions remain unresolved in this work. The disposition remains **exhausted, 5/5 approaches**. No sixth proof-search approach was attempted. No required mathematical correction was found. Two optional precision notes appear below; neither alters a conclusion or warrants changing the original freeze.

This audit covers every proposition, argument, displayed controlled trajectory, and qualification in REPORT.md; every executable line in check_identities.py; the README; and both JSON verification/manifest files. Original bytes and modes were checked before and after fresh executions. Source bodies were consulted read-only and are absent from this audit. This is an independent mathematical review and finite computational replay, not formal proof verification.

## 1. Target, stochastic assumptions, and primary sources

The author's [Problem 5](https://sites.math.washington.edu/~burdzy/open_mathjax.php) concerns normal reflection with a shared standard planar Brownian driver, starting in the domain closure. The bounded question asks for positive-probability positive limiting superior of distance; the second specifies a closed-disk exterior. The report correctly distinguishes this event from finite-time nonmeeting or a uniformly positive distance. It also handles equal starts separately and leaves the intended nontrivial initial-pair quantifier explicit. Scaling requires simultaneous time scaling by R² and regulator scaling by R; the report has both factors correct.

The inspected [BCJ arXiv version](https://arxiv.org/abs/math/0501486) has boundedness, C4 regularity, a uniform finite bound on the number of points with a specified normal, and its stated nondegeneracy at curvature zeros. Theorem 1.1 treats at most one hole; Theorem 1.2 requires positive Λ. Negative Λ implying positive limsup is Conjecture 2.2. Proposition 2.3 gives the circular exterior value zero, while Problem 2.6 asks its asymptotic question. Lemma 3.1 gives arbitrarily close approach under the paper's setting. These distinctions in the report are accurate. The closure bars in the main theorem's initial states were visually verified. No theorem in the reviewed packet extends the bounded positive-exponent result to infinite area or removes the source's technical hypotheses.

The inspected [BC author manuscript](https://digital.lib.washington.edu/bitstreams/730b9465-55ca-42cf-9ebd-9acf1aad56cf/download) proves convergence for bounded polygonal and lip domains in Theorem 1.1. Its introductory announcement about future smooth-domain nonconvergence is not such a proof. The report correctly refuses to use that announcement or a polygonal approximation as a resolution.

The five available primary-source files match the recorded byte counts and hashes. The two public-dataset files were independently rehashed and match the packet's metadata, without publishing their contents. Live access reconfirmed the author problem page and BCJ arXiv PDF; this audit's live BC manuscript request failed, so its inspection used the already available hash-matching manuscript. Author publication pages were checked at the relevant bibliographic entries. No full audit of either lengthy published proof, no worldwide literature search, and no claim of present worldwide openness is made.

## 2. Boundary identity, upper-growth bound, and controls

For two continuous reflected solutions, cancellation of their common driver makes Z=X−Y continuous and locally of finite variation. Thus its quadratic variation is zero and the finite-variation chain rule gives exactly

    d|Z|² = 2 Z·n(X) dL^X − 2 Z·n(Y) dL^Y.

This does not require stochastic differentiability of the common driver. The regulators must remain finite on compact time intervals, as in the stated reflected solutions. There is no missing Brownian dt term.

For an exterior ball at u, expanding |v−u+r n(u)|²≥r² gives (u−v)·n(u)≤|u−v|²/(2r). Applying this at X and Y gives d|Z|²≤|Z|²d(L^X+L^Y)/r. Continuous Stieltjes Gronwall yields precisely the report's factor exp((L^X+L^Y)/r) for squared distance. It includes the initial squared distance and regulator increments when started later. It is an upper-growth estimate, never a positive lower-distance estimate. Convexity reverses neither sign: inward normal pushes have the nonpositive distance contributions described in the report.

The two circular holes are disjoint, contained strictly within the outer disk, and leave a connected smooth domain. For b(t)=(-t,0), X=(1,0), L^X=t is an exact reflected path. The expanding Y=(-2−t,0), with zero regulator, stays off all boundaries for 0≤t≤1; its distance is 3+t. The contracting Y=(max(1,3/2−t),0) has regulator (t−1/2)^+ and distance (1/2−t)^+. Boundary support and the common driving equation remain valid after meeting. The reflection normal on the inner circle points away from the obstacle, so its sign is correct.

These controls are deterministic finite-time examples. Neither their existence nor a Brownian support argument supplies a positive-probability infinite-time recurrence of expansion. The report makes no such implication.

## 3. Radial logarithmic correction and precise localization

On the disk exterior the inward normal at a reflecting point x is x/R. Polarization gives

    (x−y)·n(x) = (|x−y|²+R²−|y|²)/(2R).

The logarithm of separation has no quadratic-variation correction because Z has finite variation. In two dimensions, the trace of the Hessian of log|x| is 2/|x|²−2|x|²/|x|⁴=0. Its radial boundary derivative equals 1/R in the report's regulator normalization. Consequently the martingale vector and both coefficients in (3.1) are exactly correct.

For a≥1/2 each numerator is nonpositive. For distinct x,y on the circle the coefficient is (1−2a)/(2R), which is strictly positive when a<1/2. This establishes the stated sharp threshold for **individual boundary derivatives**. It is not a necessary-and-sufficient characterization of every possible stochastic supermartingale property under every initial law.

For complete explicit localization, let τ_n stop by time n, by |X|+|Y| reaching n, by separation falling to 1/n, and by L^X+L^Y reaching n, with n initially large enough for the starting pair. On these stops the stochastic integral is square-integrable and the total variation term is integrable. For a≥1/2 the stopped process is a supermartingale. This is a concrete implementation of the report's stated standard localization. The assertion applies on the stochastic interval before collision, without asserting a global extension through a logarithmic singularity.

At x=(r,0), y=(r+1,0), Euclidean separation remains one while F_(1/2) tends to minus infinity. Thus coercivity fails. Neither the local decomposition nor a stopped expectation inequality settles large-radius excursions, singular near-diagonal behavior, or convergence in original time. No global conclusion has been smuggled into Proposition 2.

## 4. Conformal inversion obstruction

For φ(z)=R²/z the componentwise Laplacian vanishes. On the reflecting circle, φ'(x)n(x)=−φ(x)/R, which is the unit inward normal of the image disk. These facts verify every coefficient in (4.1).

The difference martingale multiplier is h=R²(1/Y²−1/X²). Multiplication by h is a real two-by-two matrix with product against its transpose equal to |h|²I. Factoring Y⁻²−X⁻² therefore gives

    |h|² = R⁴ |X−Y|² |X+Y|² / (|X|⁴ |Y|⁴).

Each Cartesian quadratic variation is its time integral and the cross bracket vanishes. This is a genuine obstruction: for R=1, x=2 and y=3 the integrand is 25/1296>0. The separate instantaneous clock rates are 1/16 and 1/81. A synchronous difference would instead be finite variation. Exceptional zeros when X=Y or X=−Y do not produce synchrony for a general initial pair. Separate time changes destroy the original simultaneous comparison. The report correctly makes no transfer of convex-disk contraction to the original exterior coupling.

## 5. Stationary criterion and product-measure rejection

The assumptions of Proposition 4 include compactness, a Feller pair semigroup, a bounded continuous observable g, and an underlying Markov process. In part (a), applying Fatou to M−g(Z_n) proves the reverse-Fatou inequality E limsup g(Z_n)≥∫g dμ. A strictly positive expectation of a nonnegative bounded variable forces positive probability of positivity. Disintegration then gives at least one deterministic starting state. For the reflected pair the diagonal is absorbing, so a successful state is off the diagonal. Integer-time positive limsup implies all-time positive limsup. No unjustified ergodicity assumption is needed.

In part (b), the difference between μ_T P_u and μ_T is the difference of two time intervals of length u divided by T. Its action on f is bounded by 2u||f||∞/T. Compactness gives a subsequential weak limit; Feller continuity permits passing P_u f to that limit. The continuous g carries the positive lower bound into the limit. Both hypotheses are essential to the stated proof; it is not being applied to the noncompact exterior.

For u(x)=x_1(3−|x|²), the radial derivative is 3x_1(1−|x|²), so the normal derivative vanishes on the disk. Independent polynomial differentiation and exact uniform-disk moments give E u=0 and E∇u=(2,0). The synchronous cross covariance contributes Σ_i ∂_(x_i)∂_(y_i) with coefficient one. Hence ∫Af=4 under independent uniform marginals. A stationary law would give zero by Itô's formula for this bounded smooth Neumann test function. The candidate product law is therefore correctly rejected.

Positive limsup alone supplies no positive average occupation: the displayed triangular peaks have total squared integral at most 1/12 when indexed from n=1, yet limsup one. This is a logical counterexample to the scalar implication, not a proposed Brownian path. The report appropriately leaves (5.1) unproved.

## 6. Circular moments and auxiliary process

An independent check can avoid differentiating the p-integral. Folding the circle and substituting t=tan θ gives

    ∫h dν = −(1/π) ∫_0^∞ log(1+t²)/t² dt,
    ∫h² dν = (1/(2π)) ∫_0^∞ log²(1+t²)/t² dt.

The integrands have finite improper integrals at zero and infinity. Integration by parts in the first integral reduces it to 2∫_0^∞(1+t²)⁻¹dt=π. For the second it gives 4∫_0^∞log(1+t²)/(1+t²)dt. Substituting t=tan θ reduces the latter integral to −2∫_0^(π/2)log cos θ dθ=π log 2. The stated values −1 and 2 log 2 follow with exactly the packet's normalization.

The more general J(p) proof also works for the full range p>−1. At a zero of cosine its integrability condition is p>−1. At θ=0 the numerator vanishes quadratically. At the integration-by-parts upper endpoint the potentially singular term is of order (π/2−θ)^(p+1), which tends to zero. Differentiation near p=0 admits an integrable local majorant such as u^(−δ)(1+|log u|²) for any fixed 0<δ<1 near the cosine zero. There is no unjustified endpoint cancellation.

For the explicitly defined Poisson measure, −h is nonnegative and in L¹(ν)∩L²(ν). Its noncompensated integral has finite expectation on finite time intervals, hence is finite almost surely there. Centering and L² convergence of truncations establish expectation zero and variance 2ℓ log 2 for M_ℓ. Infinite total mass of ν is not an obstacle to these integrable jump sums.

These statements concern the auxiliary process alone. Its clock, independence structure, and finite-separation interpretation have not been identified with those of the reflected pair. Circular zero balance gives no conclusion about convergence or nonconvergence. In particular exp(−√t) and 1 have identical zero logarithmic rates and different limits. Negative geometric exponent nonconvergence remains a conjectural source implication. The report preserves all these boundaries.

## 7. Independent executions and semantic negative controls

Fresh runs use actual UID 1000 and modes 0555 on directories, 0444 on files. Denied-write probes test both new-file creation and opening an existing checker for append, without truncating data. Original manifest hashes and complete snapshots agree before and after execution.

In each of normal, -O, and -OO mode:

- The original checker passes all 26832 boundary identities, 8944 inversion identities, 12 threshold witnesses, 21 controlled times, 64 even-power identities, 61 Neumann checks, and 7 guard rejections.
- The separately implemented checker passes 1272 boundary pairs, 7632 radial coefficients, 1272 full covariance matrices, 2544 harmonic-log traces, 101 controlled times, 128 even-power moment identities, 64 finite-state occupation telescoping checks, and 6 logical counter-witness groups.
- Seven in-memory semantic mutants are rejected by the intended RuntimeError, without printing PASS: reversed reflection normal; halved radial regulator correction; reversed boundary sign; wrong inversion radius power; premature contracting regulator; halved circular moment; and treating the product-law generator integral as zero.

The receipt records all six positive subprocesses and twenty-one negative subprocesses, including complete stdout/stderr and each mutant's hash. Checks use explicit exceptions rather than Python assert, so optimization does not remove them. The finite-state occupation example checks its algebra only; it does not prove the stochastic stationary criterion. Finite rational sampling similarly does not replace the analytic arguments or resolve the original questions.

## 8. Corrections and acceptance boundary

Required corrections: **none**.

Optional precision notes, already respected by the packet's conclusions:

1. One may spell out the regulator/time cutoffs in Proposition 2 as above when interpreting its local-supermartingale assertion. Its existing standard-localization language is sufficient and is not a global integrability claim.
2. In comparisons with BCJ Lemma 3.8, the source's ρ is normalized by initial distance. The packet's ρ is the unnormalized distance and its (2.2) correctly retains |Z_0|². There is no missing initial factor to patch.

Accepted: the written identities, elementary deterministic examples, local/stopped radial assertion, inversion obstruction, abstract sufficient stationary criterion, exact rejection of product uniformity, and circular auxiliary moments.

Not accepted as established: either requested positive-probability nonconvergence event, convergence in the disk exterior, an off-diagonal invariant measure for a target domain, a negative-exponent implication, a Brownian identification of the auxiliary jump process, an infinite-horizon event from finite controls, or any novelty claim. No such stronger result is asserted by the frozen packet. Preserve the original freeze and unresolved 5/5 disposition.
