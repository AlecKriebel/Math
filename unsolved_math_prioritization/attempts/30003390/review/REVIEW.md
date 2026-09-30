# Independent review: CIR observation information and the dimension-one optimizer

**Verdict: PASS_SCOPED_INFORMATION_REDUCTIONS_AND_CONDITIONAL_OPTIMIZER.** No mandatory correction. The original full-parameter convergence-rate problem remains **unsolved, 2/5**.

Reviewed artifact: `PARTIAL_RESULT.md`, SHA256 `639535768c14596e520ff546b16f5d4841055ea258a5fdaeed036705630dcb3a`. This is an independent AI mathematical/source audit, not human peer review or a priority determination.

## Exact source and quantifiers

The original [OWR 9/2017 contribution](https://ems.press/content/serial-article-files/46671), printed pp.466–469, asks about terminal mean absolute error using all Borel functions of the same Brownian motion's equidistant observations. The normalization delta=4a/sigma² is consistent with diffusion coefficient 2; the conjectured exponent is min(delta/2,1). Weak convergence and independently coupled terminal laws do not answer this question.

I independently checked the cached complete primary texts: [Hefter–Jentzen v2, Theorem 1 and Corollary 2](https://arxiv.org/abs/1702.08761), [Hefter–Herzwurm v1, Theorems 2–3](https://arxiv.org/abs/1608.00410), [dimension-one v1, Corollary 1 and Remark 7](https://arxiv.org/abs/1601.01455), [Hefter–Herzwurm–Müller-Gronbach v1, Section 7.1 and Corollary 14](https://arxiv.org/abs/1710.08707), and [Alfonsi, Theorem 2](https://arxiv.org/abs/1206.3855). The claimed baseline regimes match. In particular Corollary 14 is within its x>0 setting, including its adaptive lower bound; no x=0 extension of that cited corollary is certified here. The boundary lower-bound theorem itself does include x=0. The older dimension-one logarithmic bound is for a stronger path criterion.

The author's distinction between the two lower-bound papers is correct. The [2025 reflected-SDE paper](https://doi.org/10.1016/j.jco.2025.101959) remains a full-theorem access hold; its bibliographic/abstract evidence does not justify an exhaustive best-current-rate statement. This audit does not claim the old endpoint bounds are sharp today. The listed 2026 weak-error theorem cannot replace a same-driver strong-error bound.

## Mathematical audit

### Exact normalization

With c=sigma²T/4, the time/space/Brownian scalings give drift delta-beta Z and diffusion 2 sqrt(Z). The two observation vectors differ by an invertible deterministic scalar multiplication. Pulling any Borel estimator forward or backward proves both inequalities required for the exact minimal-error equality. No noise is added, and beta remains.

### Conditional decision and bridge copies

A regular conditional law is available for the real terminal variable and finite-dimensional observation vector. A lower median is measurable by rational-threshold approximation. The inequality m<=2 E[X|G] establishes its integrability. Integrating the difference of two absolute deviations gives the signed CDF integral, proving global median optimality even with atoms.

For conditionally independent X,X' with the common conditional law, the triangle inequality through a conditional median gives D<=2e. Optimality and conditional Jensen give e<=E|X-E[X|G]|<=D. Hence a constant-factor bound for either e or D transfers in both directions; this does not estimate either quantity.

Brownian paths conditional on finitely many endpoints decompose into independent bridges plus their linear interpolants. Resampling only these bridges preserves the Brownian law and produces conditionally independent solution functionals. CIR's strong existence and pathwise uniqueness justify using the same measurable functional. The complete paths share their endpoints and are not independent unconditionally.

### Dimension-one finite-grid formula

The Skorokhod regulator increases only at reflected height zero. Ito's formula therefore removes its finite-variation contribution after squaring and yields drift 1 and diffusion 2 sqrt(X) with the original Brownian driver. This establishes the representation, unlike simply squaring an unconstrained Gaussian path.

For each interval, reflection gives the killed/free transition-density ratio exp[-2(y_i+ell)(y_{i+1}+ell)/h_i]. Conditional independence multiplies the survival probabilities. At a barrier endpoint the survival probability vanishes; the sole possible regulator atom is at zero when all observed shifted endpoints are positive. Above the support endpoint each factor is strictly increasing and tends to one. These facts prove both the zero-median case and uniqueness of the positive median root.

The terminal shifted height is nonnegative on the entire regulator support, so squaring is monotone there and transports the median. Integrating the CDF below the median and its tail above the median, followed by the square substitution, proves the risk formula. A zero atom contributes through the CDF integral and requires no additional term. Gaussian crossing tails ensure integrability. In the single-interval, zero-start case the quadratic root is the positive branch; at endpoint zero the squared reflected height is exponential of mean T/2, with median and optimal absolute risk both T log(2)/2. This last statement uses a specified continuous conditional-law version, not a positive-probability endpoint event.

### Mean-reversion information obstruction

Ito's formula and the deterministic quadratic-variation clock validate the standard squared-Bessel time change. However, the transformed observations contain weighted Brownian integrals. Orthogonal projection of the weight onto constants leaves conditional variance

integral f² - (integral f)²/h = (1/(2h)) double-integral (f(s)-f(t))² ds dt.

For f(s)=exp(bs/2), b>0, this is strictly positive. Other grid increments are independent of the residual and cannot reveal it. Thus the exact transformed noise is not measurable from the original observations. The new grid is also nonuniform. Expanding the double integral independently gives the leading e^(bu)b²h³/48 coefficient, agreeing with the closed expression. This proves failure of an exact information reduction, not failure of all approximate transfers.

## Reproducibility and limits

The submitted checker was replayed in its own isolated directory. All **2,786** assertions passed and the receipt reproduced byte-for-byte. The independent standard-library checker passes **9,193** exact assertions: discrete conditional decision problems with atoms/zero weights, polynomial Gaussian projection residuals, an independent double-integral expansion of exponential residual variance, reflection identities, support signs and the one-bridge root branch. These finite checks support the written proof; they do not compute nontrivial CIR asymptotics or certify a convergence rate.

No general parameter-dependent bridge upper bound is established. The dimension-one optimizer is an exact finite-grid oracle in an already studied rate regime, not a new rate theorem or an efficient general algorithm. Keep the original target unresolved, the prior authors credited, and the later-source access limit visible.
