# Independent adversarial review: 30000849

## Verdict

**PASS_SCOPED_PARTIALS_AND_LITERAL_NORMALIZATION_CORRECTION.** No mandatory mathematical correction was found in the frozen five-turn packet. This is a pass of the precisely bounded results listed below, not a resolution of the general intended physical scaling problem. The appropriate campaign disposition remains **unsolved, five substantive author turns**.

Reviewed commit: `93c6f7ee463145541d359d9076546e727ac80039`, branch `dot/math-30000849`, repository [AlecKriebel/Math](https://github.com/AlecKriebel/Math/tree/93c6f7ee463145541d359d9076546e727ac80039/unsolved_math_prioritization/attempts/30000849).

The aggregate author manifest is `FINAL_FROZEN_MANIFEST.json`, SHA-256 `b1b53e1425af64b8c25bf6cf062720a9aca0f06d757c8680855f9fde70dd9d6d`. Its 52 entries match, as do the four historical author manifests and the prior first-turn reviewer manifest. There are 53 frozen files in the recovered directory including the aggregate manifest. The review was performed against unchanged author files, with new checks and this report outside that directory.

The five author scripts replay byte-for-byte, totaling 45,682 exact controls. The preserved first-turn independent checker also replays byte-for-byte, with 16,585 controls. The newly written independent checker passes 32,588 exact rational/symbolic controls. These finite checks support algebra and indexing; the analytic arguments below were reviewed separately. No test count is a proof of an infinite-system theorem.

## 1. Claims that pass, and claims that do not follow

1. The literal displayed OWR normalization is false for the specified zero-data example, separately under the printed and standard birth coefficients. The counterexample includes actual infinite solutions and does not require uniform convergence along similarity rays.
2. For prescribed locally bounded forcing in monomer time, the exact weighted transport formula and conditional off-front theorem hold for every real `p<1` and every real power exponent `r`. Physical-time conversion in that theorem requires `r>-1`.
3. For the standard physical model, positive power input, `0<p<1`, `omega>-1/2`, and `d=(omega+1)(1-p)<1/2`, the finite-cluster asymptotics, off-front profile, and weak leading-mass atom hold for zero data and for nonnegative finite-support data. The earlier constant-input `1/2<p<1` result is a valid contained case.
4. For `p=1/2` and constant positive input, the critical logarithmic asymptotics, off-front profile, weak cluster-count atom, and weak mass atom hold for the stated data classes.
5. The finite-support extension correctly proves nonuniversality of a single positive, initial-data-independent strict-regime front coefficient. It does not preclude the data-dependent similarity theorem that the packet actually proves.

The unproved nonlinear region is `d>1/2` outside the credited known cases; the remainder of `d=1/2` and general infinite initial tails also remain outside the proved physical results. In particular the conditional transport theorem does not supply their missing monomer asymptotic. A pointwise front-layer result is an additional question, not a requirement of the original off-front statement. No uniqueness, explicit formula for the strict-regime limiting count, comprehensive literature coverage, historical novelty, or human peer-review certification is established.

## 2. Source and quantifier audit

The full three-page OWR contribution was read from a freshly downloaded PDF matching the recorded hash. The equation page and conjecture page were visually inspected. The coefficient and normalization ambiguities are real and are kept separate from the physical model. The survey's equation (123) was checked in extracted text and rendered form; it supports birth coefficient `a_(j-1)`. Its later discussion does not supply a proved general variable-rate scaling theorem. Details, primary links, and bounded coverage are in `SOURCE_AUDIT.md`.

Zero data satisfy the source's decay condition irrespective of its undefined bare `r`. Finite-support data satisfy every fixed polynomial upper bound after choosing its constant. The literal counterexample therefore does not exploit inadmissible initial data. The definition of the tilded variables gives no hidden size-dependent amplitude factor. The source's positive profile is only needed on an interior compact interval. The negative conclusion covers every positive finite size constant and amplitude constant, so an unspecified numerical prefactor cannot cure it.

## 3. Turn 1: actual solutions and fixed-ray obstruction

I independently reconstructed the finite first- and second-moment balances from the coordinate equations. For standard addition, the first balance is `M_n'=J-(n+1)n^p x c_n`; for the second it is `S_n'=J+2x sum_(i<n) i^(p+1)c_i-(n^2+1)n^p x c_n`. These include the extra monomer consumed in the escaping top reaction. Dropping that extra loss would be an indexing error; the frozen formulas do not do so.

At `p=1/4`, the printed birth coefficients also make every additional first-moment interior term nonpositive. Thus both finite systems have `M_n<=t`. The coordinate derivative estimates, diagonal compactness, and uniform weighted-tail estimate pass. Splitting the monomer sum at a fixed cutoff before taking the limit gives uniform convergence of that sum; consequently the limit satisfies the actual integral equations and is componentwise classical. A bounded sequence of moments alone would not suffice for this passage, but the explicit tail estimate does.

For standard addition, the uniform second moment gives both a mass tail of order `1/L` and a disappearing top flux of order `n^(p-1)`. These are different requirements and both are verified. They justify exact mass conservation rather than only a mass inequality. No infinite telescoping identity is assumed prematurely. Positivity follows from variation of constants and induction.

The fixed-ray lemma is valid under merely pointwise convergence in the ray parameter. For each fixed integer size, change variables from the ray parameter to physical time and use Fatou on an interior interval. The resulting eventual lower bound for each size can then be summed over a dyadic size band. The common physical-time window and the first-moment budget bound its integral from above. This avoids an unjustified Riemann-sum passage or a floor-substitution in the source's fixed-ratio quantifier.

For `s=4/5`, displayed amplitude `r=2/3`, and mass-input exponent one, the lower and upper dyadic integrated exponents are `31/12` and `30/12`. Their positive gap gives the contradiction. The same constructed solution has the required moment bound for every proposed constant. The corrected-amplitude equality control `r=3/4` only removes this obstruction; it does not prove a scaling theorem. The preserved prior first-turn pass is consistent with this independent re-audit.

## 4. Turn 2: transport, concentration, and all exponent signs

In monomer time, multiplying the unweighted equation by `j^p` gives `g_j'=j^p(g_(j-1)-g_j)` with boundary `g_1=f`. The convolution must include holding rates `2^p` through `j^p`, whereas a pure-birth hitting time to level `j` ends at rate `(j-1)^p`. Both conventions in the packet are correct for their respective purposes. Independent stopped-chain Laplace identities test that distinction and arbitrary fixed starting sizes.

The centered exponential moment bound holds for both signs of its parameter. With `lambda=min(x/(2v),1/(2B))`, the two branches each give the stated exponent. For `p<0`, the maximal mean grows like `j^(-p)` but the relevant normalized deviation still has an exponent of order `j`; for `0<=p<1`, the asserted weaker exponent `j^(1-p)` is safe, including the logarithmic variance boundary at `p=1/2`. Thus every fixed polynomial amplitude is dominated by the tail bound.

On the central event, arguments of `f` stay above a fixed positive multiple of monomer time, so ordinary asymptotic equivalence supplies uniform relative control there. On the complement, local boundedness and the power-law equivalent supply a polynomial upper bound even when `r<0`. The expectation, rather than only convergence in probability, is therefore controlled. The ahead-of-front limit uses the corresponding lower-deviation event. Exact equality of the ratio is unnecessary: the proof also works for sequences converging to an off-front ratio.

The amplitude `q=p+(1-p)r` and constant `1/[C(1-p)^r]` follow from the weighted variables and the size-clock conversion. Integration of `dt/dtau=1/f` gives the stated physical-time power only for `r>-1`. The packet states this restriction explicitly and does not silently apply it at the logarithmic boundary. This is a prescribed-forcing theorem; it does not assume away the nonlinear problem.

## 5. Turns 3 and 4: existence, clock growth, barriers, bootstrap

The construction with locally integrable power input passes. Negative `omega` gives continuous locally absolutely continuous solutions at zero and classical coordinates for positive time; equicontinuity at zero follows by integrating a common integrable majorant. A uniformly bounded derivative at zero is neither available nor used. Finite initial support provides the finite initial second moment needed by the extension. The weighted sum and top-flux controls retain the strict condition `p<1`.

The nonexplosion argument is sound. In the constant-input case the divergent hitting-time mean and bounded variance suffice. For general `0<p<1`, stopped-process expectation comparison gives a uniform bound `G(v)` and hence a vanishing probability of reaching a diverging stopping level in finite time. It is legitimate to use the unstopped process only after this step. The recursive coordinate solution then gives the exact cohort representation without any assertion of uniqueness of the nonlinear infinite system. Nonnegative summation yields the cluster count identity.

A positive dimer population at one finite clock time gives a lower bound from a genuine existing cohort. Markov's inequality for the hitting time gives a positive probability of reaching a level comparable to `v^(1/(1-p))`; it supplies both the mass and rate-moment lower bounds. This is enough to show the upper clock bound. Clock divergence is proved separately: a bounded clock and the preliminary monomer bound would force total mass to grow strictly slower than its exact input law. No asymptotic clock is assumed.

For constant input and `p>1/2`, the clock barrier `K tau^(-p/(1-p))` has eventual inward crossing direction and forces entry. Its integrability proves finite positive cohort measure. For general power input, the moving barrier is more delicate. In `u=C t^omega tau^(-nu)`, substitution `tau'=u` is made only at a crossing. For nonpositive `omega`, both adverse derivative ratios vanish directly. For positive `omega`, the preliminary estimate `tau>=c t^((1+omega/2)/(nu+2))` follows from the total mass, expected cohort size, and the upper cluster count. The strict regime implies the inequality needed to make `t^omega tau^(-2nu-1)` vanish. Thus the crossing calculation is not circular.

Eventual entry is justified by a signed drift whose integral diverges. Above the barrier it forces the nonnegative monomer coordinate downward; afterwards the crossing inequalities prevent escape. The lower physical-time comparison used later is likewise entered because its positive drift cannot persist forever while the solution stays below a decaying curve.

The exponent bootstrap retains its finite initial contribution. For negative monomer exponents, integration by parts produces bounded, logarithmic, or positive-power count growth according to the sign of `a+d`; treating every case as `O(t^(a+d))` would be incorrect. The recurrence `b_new=p b+2d-1` has a negative fixed point and crosses zero in finitely many steps. At equality, an arbitrarily small positive power bounds the logarithm and permits one further strict step. I deliberately checked `p=1/2`, `beta=4/5`, where the first recurrence reaches equality exactly. Controls at `d=1/2` and `d>1/2` demonstrate that the same argument does not close there.

## 6. Moment convergence and nonlinear closure

Hitting-time concentration gives convergence in probability of the normalized birth process to one. The stopped-process Jensen bound has the sharp leading coefficient: its expected-size upper bound divided by the characteristic size tends to one. Combining this upper bound with convergence in probability gives convergence of the means and then convergence in L1 by the identity involving `min(X,1)`. This is stronger than an isolated first-moment bound and provides the uniform-integrability information later needed for mass-weighted tests. The pth-moment convergence follows from concavity and `|x^p-1|<=|x-1|^p`.

In the strict regime, the cohort measure is now finite. Uniform upper bounds on normalized first and pth moments permit dominated convergence over that measure, including its young-cohort part. The mass law and the negligible monomer coordinate then identify the physical size coefficient and rate moment. They do not differentiate a previously obtained asymptotic equivalence.

The final forced scalar equation is compared with explicit upper and lower power curves. The derivative of those curves is smaller than the signed forcing discrepancy by the power `t^(-p beta-1)`. This proves the monomer equivalent. Its exponent and all three parameter powers in its coefficient agree with the size law, the integrated clock, and the transport normalization. The independent code checks these coefficient powers in logarithmic coordinates rather than evaluating potentially ill-conditioned floating-point powers.

For weak leading-mass convergence, normalized cohort sizes converge in L1, not just in probability. Consequently bounded continuous mass-weighted tests converge, and dominated convergence over the finite cohort measure applies. The nonintegrable off-front profile is not used as an integrable density for the leading mass. The distinction between a subleading bulk profile and a leading front atom is essential and correctly preserved.

## 7. Turn 5: logarithmic critical case

The initial `f<=C/tau` estimate is valid at `p=1/2`, but is not incorrectly declared integrable. Assuming finite limiting count gives the finite-cohort rate-moment equivalent; the exact monomer equation then forces a `const/tau` monomer equivalent and contradicts that assumption. This establishes divergence of the count.

Direct integration of the upper bound shows that changing clock time by a fixed multiplicative factor changes the count by only a bounded additive amount. Together with divergence this proves the slow-variation statement used here. In the old/late cohort decomposition, the old cohort ages are uniformly large and their counts asymptotically exhaust the total count; the late counts are negligible, and the expectation bound controls their mass contribution. Thus `P~N tau/2` and `alpha t~N tau^2/4` follow without a Tauberian assumption.

The comparison curves depend on the actual count, but their derivative is estimated using the exact identity `N'=f` and the already proved upper bound. The field is strictly decreasing in the monomer variable. Signed entry drifts and crossing inequalities give `f~2alpha/(tau N)`. Only then is the exact derivative `(N^2)'=2Nf` used, so integration yields the logarithm without differentiating an asymptotic formula. The coefficient powers of two and alpha in the inverse clock, physical monomer law, count law, and size law all agree.

The explicit power-log equivalent gives uniform local ratio convergence away from zero. The same exponential holding-time concentration therefore proves the off-front limit. Its multiplier reduces to physical time by the independently derived mass relation. The weak count and mass limits use the old/late split and uniform large-age L1 concentration; a first-moment bound alone would not justify the mass-weighted tail, but the established L1 concentration does.

## 8. Finite-support extension, memory, and publication interpretation

Every initial higher-cluster component is retained as a cohort starting at its actual size. Removing finitely many holding times does not change the leading hitting-time mean or concentration bound. The resulting first moments have the same leading coefficient, and their finite sum introduces only finite constants into the clock and bootstrap arguments. In the strict regime those cohorts contribute to the limiting count; in the critical case their contribution is negligible relative to the divergent count.

For a fixed starting size, lying strictly behind the front requires an unusually late hitting time of the next level; lying strictly ahead requires an unusually early hitting time. Those estimates are stretched-exponential and dominate the actual power or power-log profile normalizations. This validates the off-front extension, not just its moment statements. No uncontrolled finite-support approximation to general infinite tails is used.

The memory obstruction uses the total limiting count being at least the initial higher-cluster count. Arbitrarily large finite-support initial count makes the actual strict-regime front coefficient arbitrarily small. A proposed fixed positive coefficient would then put a nominal interior ray strictly ahead of the actual front, contradicting its demanded positive limit. The conclusion is exactly nonuniversality of that fixed coefficient, not failure of all similarity.

The historical status and manifest files correctly remain historical; their pending-review wording should not be silently edited. A publication wrapper can identify this full review as subsequent evidence. The complete packet supports a draft of scoped partial results with the literal normalization correction prominently distinguished and the original physical task still marked unsolved 5/5. It does not support a claimed-solved promotion, a new priority claim, a front-density claim, or a sixth author research turn.

Review completed 2026-10-02. No remote file, branch, PR, queue row, release, or external communication was changed during this audit.
