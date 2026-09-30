# Independent review: Markov-limit metric and completion obstructions

**Verdict: PASS_SCOPED_PARTIAL_RESULTS_AFTER_QUALIFICATION.** The torus divergence, conditional positive-time completion theorem, and instantaneous-mixture obstruction are valid. A narrow diagonal-kernel qualification was requested and incorporated. The original topology problem remains **unsolved, 3/5**.

This separate adversarial AI review used gpt-6-astra at xhigh reasoning on 2026-09-30. It does not establish novelty and is not human peer review.

## 1. Reviewed versions and checks

- Original submitted PARTIAL.md: e9562537a7d3a874f560fe0fc5019b5281b79195315bb749c3bd8102c1317bf4
- **Corrected final PARTIAL.md:** c1e0ff8a038024044e0e67c671a644bdd0bd5b248afeb747e20ad541a4e3dfc0
- Unchanged verifier: 3b2a1e2f4fa2f151bacf161d5a3308791b40857d198d07e303113ec2f248cb0a
- Final submitted receipt: 6c299ab4638c30d4133a7de803c5a0f4d94b6f3e3e41c0ca71f356849770b92e
- **4,246 submitted exact assertions** replayed with byte-identical output
- **1,097 independent exact diagnostics** passed

The only mathematical-text change is in the theorem's array-preservation clause and its concluding proof sentence. It now explicitly conditions preservation of repeated-index/diagonal entries on the canonical diagonal values, as in diagonal Chapman–Kolmogorov. The exact change is preserved in correction.diff. No construction, estimate, or verifier changed.

## 2. Exact source scope

I read the [maintained Aldous problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/compact.html), the complete seven-page [original note](https://www.stat.berkeley.edu/~aldous/Talks/MCcompact.pdf), and all five [2018 slides](https://www.stat.berkeley.edu/~aldous/Research/OP/talk_towsner_2018.pdf). The last slide was visually inspected: its weight is $e^{-t}$. It gives the integrated row distance as an example and asks for a natural complete separable state topology with the Feller property. It does not require that particular distance or require the resulting state space itself to be compact.

The finite objects use transition densities relative to their stationary measure; for uniform measure on $N$ states this is $N$ times the transition probability. The trace normalization and positive-time trace bounds are retained. The convergence is that of finite stationary-sampled density arrays, including diagonal entries, rather than a previously given state topology or path-space convergence.

[Towsner's Definition 2.6](https://arxiv.org/abs/1404.3815v3) separately imposes ordinary and diagonal Chapman–Kolmogorov, trace bounds, and positive-time $L^2$ continuity. It does not silently supply the strongly continuous $L^2$ semigroup at time zero assumed in Section 3 of the artifact. That stronger hypothesis is expressly stated, and the examples satisfy it. Landim's work on path-space topologies is correctly kept separate from this state-space realization question.

Thus failure of the displayed distance or of a particular completion cannot by itself refute the original existential topology problem. The artifact consistently retains that distinction.

## 3. Torus divergence and the actual finite-chain approximation

For the two-dimensional heat semigroup, Fourier orthogonality gives a row-difference coefficient $4$ on odd first-coordinate frequencies for the pair $0$ and $(1/2,0)$. Squaring the heat coefficient doubles its exponent; integrating against $e^{-t}$ therefore gives
\[
4\sum_{\substack{k_1\ {\rm odd}\\ k_2\in\mathbb Z}}
\frac1{1+8\pi^2a(k_1^2+k_2^2)}.
\]
All terms are nonnegative, so Tonelli is legitimate even though the final sum is infinite. For each positive odd $k_1=m$, retaining $|k_2|\le m$ gives a constant multiple of $1/m$ from that row. The odd harmonic sum diverges. This proves that the displayed formula is not a finite metric.

The normalization $G(1)=2$ is available and unique: the heat trace decreases continuously and strictly from infinity to one as its positive time factor increases. The torus already has its usual compact Feller realization, so this example is specifically a failure of the formula.

The finite-grid link to the source is rigorous. For centered frequencies with $|k_i|\le n/2$, the inequalities $2|k_i|/n\le|\sin(\pi k_i/n)|\le\pi|k_i|/n$ give the displayed two-sided eigenvalue bounds. There are four distinct first nonzero modes for every $n\ge3$. Trace normalization consequently gives the uniform lower bound $\log4/(4\pi^2)$ for the time factors. At time factor one, the full Gaussian majorant is less than two, giving the stated finite upper bound.

Every convergent subsequence of the time factors has a limit whose torus heat trace equals two, by dominated convergence over centered lattice frequencies. Uniqueness identifies that limit, hence gives convergence of the entire sequence. The same Gaussian majorant uniformly controls the Fourier tails on compact positive-time intervals; the finite parts converge uniformly. The density normalization has no erroneous $1/n^2$ factor.

Coupling each stationary grid point by coordinatewise rounding of a uniform torus point then gives convergence of every finite sampled density array. The diagonal converges as well. The trace majorant holds uniformly in the grid size at each positive time. This is therefore an example within the normalized bounded finite-grid limit setting, not merely a separate diffusion.

## 4. The positive-time Hilbert completion

The stated symmetric strongly continuous $L^2$ semigroup has a nonnegative self-adjoint generator. Trace-class heat operators yield the discrete spectral representation used in the text. A common conull set at positive rational times suffices: spectral monotonicity gives finite rows at all later positive times, while the semigroup identity transports nonnegativity and total mass one from rational times.

The trace-adapted weight is positive and integrable, and
\[
\int\|j(x)\|^2\,d\pi(x)
=\int_0^\infty w(t)G(2t)\,dt\le1.
\]
This gives a measurable Hilbert-valued map almost everywhere. Since the probability space is standard, the relevant $L^2$ spaces are separable. The support of the pushed-forward probability is closed in the separable Hilbert space, and a conull original image is dense in that support. It is therefore complete and separable. This step correctly permits identification of density-invisible twins and does not assert preservation of arbitrary point labels.

The row inequality (5) is valid: for $0<s<t$, semigroup contractivity gives
$\|K_t(x)-K_t(y)\|_2\le\|K_s(x)-K_s(y)\|_2$; integration over $s\in(0,t)$ bounds the later row difference by the Hilbert distance divided by $\sqrt{W_t}$. Each row map is well defined on the image quotient and extends uniquely to its closure.

The nonnegative cone and the integral-one affine hyperplane are closed in $L^2$ on a probability space. Thus extension does not lose stochasticity. Taking inner products of the extended half-time rows produces symmetric, nonnegative, jointly continuous pair kernels.

For completeness, identifying their pullbacks with $K_t(z)$ in $L^2(\pi)$ is legitimate. The map sending a half-time row $h$ to the function $\langle h,K_{t/2}(y)\rangle$ is the bounded operator $P_{t/2}$; it is not an unbounded pointwise evaluation operation. This proves the pullback identity first on the original image and then by $L^2$ continuity. The integral-one condition, bounded-function continuity, and the everywhere Chapman–Kolmogorov identity follow. Positive-time joint continuity also follows by combining the row Lipschitz bound near a fixed positive time with strong continuity of the semigroup.

The stationary increment identity is a valid trace calculation. Expanding the squared Hilbert distance gives $G(2s)$ for either marginal and $G(2s+t)$ for the cross term. Its integrand is bounded by the integrable $e^{-s}$ envelope. Dominated convergence proves the averaged limit. It does not establish a limit at every exceptional state.

### The diagonal qualification

An abstract $L^2$ integral operator does not determine arbitrary values of a transition-density version on a nonatomic diagonal. Changing those values leaves the operator unchanged but changes $p_t(X_i,X_i)$ in a sampled array. Thus the original unqualified claim about all array entries was too broad under the abstract semigroup hypotheses alone.

The author corrected exactly that clause. Off-diagonal sampled entries are preserved; repeated-index entries are preserved under
\[
p_t(x,x)=\|K_{t/2}(x)\|_2^2,
\]
which is the canonical convention and is imposed by diagonal Chapman–Kolmogorov in Towsner's source setting. This resolves the issue without altering the positive-time construction or either example.

## 5. Infinite fast-leaf chain and trace control

The leaf masses sum to $1/15$ and the two hub masses to $14/15$. Detailed balance holds exactly:
\[
16^{-n}2^{n-1}=\frac7{15}\frac{15}{14}8^{-n}.
\]
The total hub exit rate is $113/98$. The chain is nonexplosive because an infinite sequence of jumps must include infinitely many hub holding times, each with the same positive exponential mean. Their sum diverges almost surely.

After conjugation to counting-measure $\ell^2$, the diagonal grows like $2^n$ on the leaves, and the off-diagonal part has finite rank. The squared coupling-vector norm is $5/28$ as stated. Combining the two equal hub-to-leaf vectors with the bounded hub block gives norm less than two. The diagonal operator has compact resolvent; bounded perturbation preserves that property. The eigenvalue comparison gives the claimed finite heat-trace bound. Connectedness gives a one-dimensional zero eigenspace, and trace summability implies convergence of the trace to one at large time.

The first-exit formula (9) is exact. At a fixed positive time the exponential convolution is an approximate identity applied to a bounded, strongly $L^2$-continuous mean hub row. Its error tends to zero. This part of the argument requires no claim of uniform pointwise kernel convergence over all leaves.

## 6. The midpoint obstruction

The disjoint star/torus semigroup with a rate-one reset is a conservative symmetric strongly continuous semigroup. The projection onto constants commutes with the block semigroup, giving formula (10) and its trace. The half-mass normalization of the two components contributes the stated $\sqrt2$ factor when comparing row differences. Reset terms cancel in the leaf-versus-hub-mean difference.

The eight-dimensional torus trace has the required $t^{-4}$ lower bound by retaining a box of Fourier frequencies of size proportional to $t^{-1/2}$. Thus the trace-adapted weight is at most a constant times $t^4$ near zero, and that estimate extends to all positive times after enlarging the constant.

Since $\pi_S(n)=r_n^{-4}$, the squared spike integral is exactly bounded by a constant times
\[
r_n^4\int_0^\infty t^4e^{-2r_nt}\,dt
=\frac{3}{4r_n}.
\]
It tends to zero. The bounded convolution error tends pointwise to zero and is dominated against the integrable weight. Therefore the Hilbert images of the leaves converge to the arithmetic mean of the two hub images.

Every leaf image has positive pushed-forward mass, so the limit belongs to the closed support. The hub images are distinct: their antisymmetric eigenfunction has decay rate $211/98$ before reset and $309/98$ afterward. The midpoint has half their positive mutual distance from either hub. It is genuinely absent from the original images: it cannot equal a fixed leaf image, whose time-zero law is concentrated at that leaf, and it cannot equal a torus image because the block-indicator mode distinguishes star and torus initial states.

Lipschitz extension of rows makes the transition law from that midpoint the mean of the two hub laws at every positive time. A hub remains in place until a jump or reset with probability at least $e^{-(c+1)t}$, so its law converges to the hub point mass. A bounded continuous distance-based test function that is zero at the midpoint and one at each hub consequently has limiting expectation one when started at the midpoint.

This disproves stochastic continuity at that state. In particular, a right-continuous process started there cannot have those transition probabilities. The argument uses this necessary time-zero property directly and does not depend on a potentially ambiguous Feller convention on a non-locally-compact space.

The example is asserted only within the stated reversible trace-class semigroup class. No separate finite-uniform-grid realization of this mixed space is claimed or supplied. Its time normalization can be adjusted because the reset heat trace decreases from infinity to one; this only rescales constants and does not remove the midpoint failure.

## 7. Remaining problem and reproduction

Neither obstruction excludes all possible topologies, null-state choices, or measurable representations. The positive theorem is conditional and only concerns positive-time kernels. The missing task remains a suitable realization with the required time-zero and path behavior at every retained state. The original target is therefore **unsolved, 3/5**.

The independent controls use complete-graph spectral identities and an exact tail-aggregated star model that retains the infinite example's hub masses, exit rate, and antisymmetric eigenvalue. They also verify symbolic Dirichlet identities, the dimension-sensitive spike integral, and midpoint test-function values. These computations support, but do not replace, the analytic arguments above.

From this review directory:

    python3 independent_checks.py
    python3 author_replay/verify.py > author_replay/replayed_verification.json
    cmp author_replay/verification.json author_replay/replayed_verification.json

The independent checker uses SymPy; the submitted checker uses standard-library Python. The corrected frozen snapshot is included for self-contained replay. All requested corrections are resolved, and no further mandatory change is required.
