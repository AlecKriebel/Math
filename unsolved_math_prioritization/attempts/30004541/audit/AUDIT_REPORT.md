# Independent adversarial audit: 30004541

## Verdict and scope

**PASS for the frozen NO RESOLUTION checkpoint.** This is not a proof of either general problem and is not an endorsement of novelty. No blocking mathematical correction was found in the six retained propositions. The five-approach, 5/5 exhausted disposition is supported; neither “solved” nor “complete candidate” is supported.

The audit read all ten authored files and every retained proof, reproduced the author controls, independently derived the delicate estimates, checked cited source passages, and inspected the original question visually. The author directory and its archive were not edited. No remote write was performed.

Frozen archive: `DERRIDA_30004541_AUTHOR_SAFE_FREEZE.zip`, 24,145 bytes, SHA-256 `87523ba565a385498b3f779924373a20e3fc0b6c75d596e8d1aa91f4de33b750`.

The pass is scoped to the mathematical partial results, exact target, source-scope distinctions, and preserved artifact. A publication worker must still perform the separately required current selected-record/review-hash binding before any queue change. This audit does not certify current remote queue state or authorize a remote mutation.

## 1. Exact problem and stochastic construction

The original OWR printed page 1641 contains two distinct tasks: an initial-law characterization of zero free energy, and convergence in probability to zero under zero free energy. The initial state is a probability law on the nonnegative reals. The driving model is binary rate-one Yule branching with unit erosion, equivalently a rate-one McKean–Vlasov jump process. The process is not the fixed-binary integer recursion and is not the geometric-offspring discrete recursion.

The quantile convention agrees with HMP Definition 1.4. The two endpoint choices have no effect on a Lebesgue-intensity Poisson random measure. HMP Theorem 1.8 explicitly applies to arbitrary probability measures, not only finite-mean or smooth laws. This existence/uniqueness result remains an identified external theorem import; the audit does not claim a new independent proof of that theorem.

A Yule tree is finite almost surely on every finite time horizon, since the sum of independent exponential holding times with rates 1, 2, 3, ... diverges almost surely. Thus finite trees with almost surely finite leaf values define their roots without a moment assumption. The law at a fixed height and the path process are not being confused. The first-split decomposition and branching property yield the nonlinear semigroup. The leaf number is geometric at a fixed height; this is not a geometric-offspring rule at each generation.

## 2. Proposition-by-proposition findings

### Proposition 1: mass and energy — PASS

The root is at most the sum of its leaf amounts. Conditional expectation over the tree therefore gives `m(t) <= exp(t) m(0)` in the finite-mean case. This bound is locally integrable and validates the compensator calculation. The erosion term is `P(X_t > 0)`, not one and not a boundary-density value. Hence the locally absolutely continuous mean satisfies `m' = m - q` almost everywhere.

The rescaled mean is nonincreasing and nonnegative. Its limit and the tail integral follow without a uniform-integrability assumption at infinite time. From the tail identity, zero free energy implies `m(t) <= 1` for every time. The converse uses a bound for the entire trajectory; a bound only at time zero would be false. The finite-time positivity certificate has the correct direction.

For infinite initial mean, the no-split event alone retains an infinite expectation of `(X_0-t)_+`. This avoids illegal subtraction involving infinity. The author's explicit extended-real free-energy convention gives infinity in this case; it does not change the zero-energy class.

### Proposition 2: tails and second moments — PASS

The deterministic tree lower bound is valid. On any common edge of length `c`, erosion of an aggregate loses at most what separate erosion loses: `(sum a_i-c)_+ >= sum (a_i-c)_+`. Applying this successively gives the sum over leaves of `(X_i-s)_+` for a height-`s` tree. This reasoning does not require equal individual edge lengths; it uses equal total root-to-leaf height. Conditional averaging gives the factor `exp(s)`.

At `x=s+1`, the use of `>=` in the tail event is valid even with an atom: `(X-s)_+ >= 1_{X>=s+1}`. The resulting uniform exponential tail controls every polynomial moment and gives uniform integrability of first moments. For each fixed `theta<1`, it also controls the polynomial-exponential moments needed later. It does not control the endpoint `E[X exp(X)]` by itself.

The second-moment generator is `m_2' = m_2 - 2m + 2m^2`. After integration, the terminal term vanishes because the tail estimate has already supplied a uniform second-moment bound. There is no circular use of the desired `1/2` estimate. The retained non-strict bound is justified; no stronger claim from a source is needed.

### Proposition 3: invariant family and phase — PASS

The positive-density convolution, erosion derivative, and zero-atom flux give the stated two ODEs. In particular, the boundary atom has incoming flux `(1-p) lambda` and convolution change `p^2-p`; omitting either term would produce a different phase curve. Independent checks confirm both density coefficients, atom flux, mean equation, and invariant.

The invariant rectangle and finite-time positivity of lambda are adequate. In the decreasing-lambda phase analysis, a positive limit below one is impossible because the invariant curve lies above `p=1` immediately to its right. If the initial lambda is at most one, strict decrease rules out a limit of one. For initial lambda above one, the first admissible root has the stated classification. The degenerate case `p=1` is explicitly separated.

In the pinned regime the integral defining the finite constant `K` has no interior singularity and has only an integrable logarithmic endpoint at zero. Therefore the positive free-energy formula is justified. At criticality, the quadratic expansion and integration of `(1/(lambda-1))'` imply the reported asymptotics. Stochastic domination on a common tree is valid and yields the stated comparison corollary, without a universal-envelope assertion.

### Proposition 4: pinned obstruction — PASS

For rate `5/2`, the invariant maximum is `(5/2)/e < 15/16`, using the exact strict lower bound `e>8/3`. Consequently the integral exponent is strictly less than 40, and `F > (2/5) exp(-40) > 0` follows. No numerical integration is used.

The second moment, endpoint exponential moments, and tail comparison are correct. The polynomial numerator for the whole interval `0<theta<1` is exactly `2(theta-7/8)^2+23/32`; the denominator stays positive throughout that interval. This algebraic identity is an infinite-family certificate. The 27 sampled/named author checks, or our finite controls, would not alone establish that infinite statement.

For the necessary polynomial-exponential inequality, the drift and jump identities were recomputed, including their atom terms. If the test quantity became negative, the scalar differential inequality forces an exponentially diverging negative upper bound, contradicting the already established uniform integrability bounds at this fixed `theta<1`. The integrating-factor argument works with almost-everywhere derivatives.

HMP Proposition 6.6(4) indeed supplies the endpoint integrability and moment inequality that the author imports. Its proof first uses bounded monotone comparison to exclude an infinite endpoint moment, then passes to the endpoint using dominated convergence. This is substantially stronger than merely substituting `theta=1` into the crude tail estimate. The author correctly avoids that invalid shortcut.

The independent `Exp(2)` boundary calculation gives `D'(0)=-2` when `D=E[(1-X)exp(X)]=0`; the invariant-family rate stays above one for a short interval, so the required moments really exist there. Thus sign invariance fails. The pinned example refutes only the conjunction of the listed initial tests, not the extinction conjecture.

### Proposition 5: capped-tree exponential criterion — PASS

The cap must be applied to the leaves and after every merger, as the author does. This defines bounded state-space dynamics; it is not merely truncation of a test function applied to an uncontrolled process. With `T_r(x)=(x-r)_+` and `C_K(x)=min(K,x)`, its first-split equation is

`nu_t = exp(-t) (T_t)#nu_0 + integral_0^t exp(-(t-s)) (T_(t-s))#(C_K)#(nu_s * nu_s) ds`.

This formula justifies the weak generator and local absolute continuity for the bounded exponential observable. Differentiability at a hitting time need not be classical; the integrated identity and almost-everywhere inequality suffice. The cap only decreases the exponential jump term. Replacing the atom probability by one gives exactly `(g_K-1)(g_K-theta)`.

Scalar comparison is in the correct direction, starts from `g_K(0)<=g_0`, and prevents crossing the invariant interval `[1,g_0]`. The positive gap `theta-g_0` then gives the uniform exponential decay estimate. No moment finiteness for the original uncapped process has been presumed in this step.

For each fixed horizon, couple all caps on the same finite tree with the same leaf values. The root is nondecreasing in the cap. Once the cap exceeds the total leaf mass, no cap is used anywhere. This is eventual equality on each realized finite tree, a stronger statement than convergence in distribution. Monotone convergence therefore passes the exponential estimate to the original law. Uniform integrability is neither silently assumed nor needed for this passage.

A useful negative control: bounding the root only by the leaf sum gives an exponential-moment estimate involving `E[g_0^N]`, which becomes infinite once `(1-exp(-t))g_0>=1` when `g_0>1`. That simpler argument would not justify global moment propagation. The author's capped dynamics avoids precisely this defect.

The deterministic sufficient threshold is the maximum of `log(theta)/theta`, namely `1/e`. The strict inequality and lack of an endpoint assertion are appropriate. Critical atom-exponential laws already preclude treating this exponential-decay region as a complete zero-energy characterization.

### Proposition 6: stationary law and conditional limit — PASS

The Laplace equation contains the boundary correction `-s p_t`, with the stated sign. For a finite-mean stationary law, the rescaled mean tends to zero, so the previously proved exponential tail applies. The moment-generating function is analytic in the open unit disk and has nonnegative Taylor coefficients. Independent-sum integrability validates the stationary quadratic for real parameters below one, and analytic continuation extends it to the disk.

The root with value one at zero is correctly selected. The cases `p=0` and `p=1` are treated separately. For `0<p<1`, the discriminant roots are distinct, nonreal, and of modulus one. A square of an analytic function cannot have a simple zero, so their singularities cannot be removed. The Taylor radius is exactly one, while the algebraic expression has an analytic continuation near the positive point one. The author's positive-coefficient lemma proves the resulting contradiction: shifting the Taylor center to a nearby positive point and applying Tonelli would force convergence at a real point beyond the radius. It does not assume the original integral is analytic at one.

The Wasserstein estimate follows from the sum of leafwise differences and `E[N_s]=exp(s)`. A whole-trajectory weak limit under the common tail estimate is a Wasserstein limit, so the semigroup continuity argument really makes that limit stationary. A merely subsequential limit cannot be substituted. The report explicitly retains this distinction and therefore does not solve extinction by tightness.

## 3. Nonblocking precision note

In REPORT.md's weak law equation and transform displays, and the moment displays in Proposition 4, read time derivatives as almost-everywhere identities or use their equivalent integral forms. It would improve standalone readability to add: “All general-law time differential identities are understood almost everywhere; their observables are locally absolutely continuous.” This is a clarification, not a change to a theorem or proof. The proof already states the needed almost-everywhere convention in Propositions 1 and 5.

This qualification matters. Starting from `delta_a` with `a>0`, the no-jump mass reaches zero at deterministic time `a`. In the tree representation, at that time all split trees have positive residual mass, whereas the no-split tree contributes atom `exp(-a)` at zero. The probability of positivity drops from its left limit one to `1-exp(-a)`. The mean's one-sided derivatives consequently differ by `exp(-a)`. A claim of a classical derivative at every time for arbitrary initial laws would be false. None of the retained arguments needs such a claim.

Required corrections: **none**. Optional editorial clarification: the preceding sentence about almost-everywhere derivatives. If the package is edited, refreeze and rehash it; this verdict binds only the recorded frozen bytes.

## 4. Source and metadata checks

All six cached public PDFs were independently rehashed and match the author's byte counts and hashes. Their relevant model, theorem, or scope passages were inspected; the original OWR problem was also visually inspected. Source files and extracts are not included here. Current arXiv abstract/version pages and the HMP publisher page were checked independently. HMP is a published CMP article, not merely an unreviewed preprint. Li–Zhang's asymptotic-paper PDF explicitly reports its 2025 journal publication.

The scaling paper gives fixed-time/Skorokhod finite-horizon convergence; its quantitative error bound grows with time and does not justify an exchange with an infinite-time limit. The later geometric-offspring results concern restricted invariant families in a different recursion. The Brownian-CRT paper concerns a time-inhomogeneous growth-fragmentation process on `[0,1)`. These distinctions survive inspection.

An additional 2026 publication surfaced during the audit: Xinxing Chen, *Infinite Differentiability of the Free Energy for a Derrida–Retaux System*, DOI `10.1007/s10114-026-4249-z`, associated with arXiv:2405.09741. Its introduction fixes an integer offspring number and nonnegative integer initial values, and studies smoothness of discrete free energy. Inspection of its opening model and main theorem does not produce a resolution of this continuous-time arbitrary-law target. This is a source-scope cross-check, not a sixth solution approach. The bibliography remains a dated, bounded search, not a universal openness certificate.

Both complete public dataset corpora were independently rehashed. They match the stored immutable-manifest values: 68,931,837 bytes for problems and 80,334,822 bytes for research results. There is one numeric-ID match and one exact problem-code match; the exact prior-report key is absent from the full 6,701-entry dictionary. The cached catalog matches rank 754, the recorded statement hash, and the recorded review hash. This does not upgrade the cached record to a freshly read remote record. The author's prior repository-search results are historical metadata, not fresh remote searches performed by this audit.

## 5. Reproducibility and final gate

`python verify_independent.py` reproduces 54 named checks, 780 deterministic rational-tree cases, seven finite stationary-moment negative controls, and all 27 author controls. The script performs no networking, writes, or simulation. It also compares every archive member byte-for-byte with the author directory. `INDEPENDENT_CHECKS.json` records the actual run. These finite controls support the audit but do not certify its analytic arguments.

The audit bundle contains only newly authored analysis/code and verification metadata. It contains no PDF, source extract, raw dataset, credentials, or private coordination. The audit manifest enforces its exact file allowlist. The unchanged author freeze remains the authoritative object audited.

**Final disposition: PASS, scoped to an honest NO RESOLUTION / exhausted 5/5 checkpoint. Full arbitrary-law classification and zero-energy extinction remain unproved by this work.**
