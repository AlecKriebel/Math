# Independent review: 10300054 / Calegari Question 13.1

**Verdict: PASS for the scoped smooth gauge analysis and transport diagnostics. The original foliation question remains unresolved. No mandatory mathematical correction was found.**

Reviewed on 2026-09-30 by a separate AI reviewer using gpt-6-astra with xhigh reasoning. The frozen OBSTRUCTION.md has SHA-256

dcd4ba441c5655526a20a2ddd474e6c4477fab2c74978b907125f8d797b41087.

The snapshot is preserved in [author_replay/OBSTRUCTION.md](author_replay/OBSTRUCTION.md). No author mathematical file was edited. This review certifies neither a novel discovery nor a counterexample to the original question.

## 1. Exact question and regularity

I checked the complete Question 13.1 and all four remarks on printed p.29 of [Calegari's primary problem list](https://arxiv.org/abs/math/0209081), including visual inspection. The foliation is fixed, minimal, taut and $C^2$, on an atoroidal 3-manifold, with nonzero Godbillon–Vey number. The requested representative has a weak sign: zeros are explicitly permitted.

The source itself distinguishes this from the stronger contact condition. Its remarks also rule out treating arbitrary torus splicing or nonminimal examples as counterexamples to the stated target.

The submitted calculations explicitly concern smooth, globally defined forms on a closed oriented manifold with a cooriented foliation. They do not claim a smoothing theorem for the original $C^2$ data. This limitation must be retained. The global-form formulation and the fundamental-class evaluation are not used to manufacture an obstruction from an omitted orientation convention.

The introduction and Section 3 of [Hurder–Langevin](https://homepages.math.uic.edu/~hurder/papers/59manuscript-rev2016.pdf) confirm the auxiliary form's nonuniqueness and invariance of the resulting cohomology class. Their dynamical nonvanishing theorem does not provide a pointwise one-signed representative.

## 2. The full gauge formula

The signs and all terms of (2.3) are correct.

From $d\alpha=\alpha\wedge\omega$ one obtains $\alpha\wedge d\omega=0$. For $\alpha_f=e^f\alpha$,
$$
d\alpha_f=\alpha_f\wedge(\omega-df).
$$
Every auxiliary form is therefore $\beta=\omega-df+h\alpha_f$. This is a global parametrization: a smooth transverse field $Z$ with $\alpha_f(Z)=1$ recovers the coefficient $h$ by evaluation of the difference of the two auxiliary forms. A same-coorientation defining form is a positive smooth multiple of $\alpha$, so its multiplier has a global smooth logarithm.

In the expansion of $\beta\wedge d\beta$, the two potentially troublesome undifferentiated-$h$ terms vanish:
$$
(\omega-df)\wedge d\alpha_f=0,\qquad
\alpha_f\wedge d\omega=0.
$$
The remaining mixed term satisfies
$$
(\omega-df)\wedge dh\wedge\alpha_f=dh\wedge d\alpha_f.
$$
Consequently
$$
\beta\wedge d\beta
=\omega\wedge d\omega-df\wedge d\omega+dh\wedge d\alpha_f
=\omega\wedge d\omega+d(-f\,d\omega+h\,d\alpha_f).
$$
There is no missing factor of two, sign reversal, or unrestricted exact-form freedom.

The distinction from choosing an arbitrary top-degree representative is valid. On a closed connected oriented manifold, a nonzero top-degree class has a strictly one-signed representative. The displayed transgression, however, has the prescribed special form and does not realize an arbitrary exact correction.

## 3. The fixed-gauge equation and invariant measures

For the chosen positive volume form, the identity
$$
\lambda\wedge\iota_X\nu=\lambda(X)\nu
$$
gives the scalar equation $g_f+X_fh$, with $g_f=v-Yf$, exactly as written. Both vector fields preserve $\nu$ because their contractions with it are closed forms. Both are tangent to the foliation: use $\alpha\wedge d\omega=0$ for $Y$ and $\alpha_f\wedge d\alpha_f=0$ for $X_f$.

For each fixed $f$, integration against an $X_f$-invariant probability annihilates $X_fh$. This proves the necessary inequalities. The normalized volume measure is invariant, and its integral of $g_f$ equals the total Godbillon–Vey number divided by volume; the $Yf$ term integrates to zero. A positive value for this one measure does not control all invariant measures.

The two-torus example with $X=\partial_x$ and $g=1+2\cos y$ correctly distinguishes the positive area average from the negative average on the invariant circle $y=\pi$. It is explicitly an abstract transport example.

## 4. Strict positivity and approximate nonnegativity

The strict criterion is valid for any smooth flow on a closed manifold. Its proof needs the compact set of **all** invariant probability measures, not just the generally nonclosed subset of ergodic measures; the submitted statement uses the correct set.

That set is nonempty and weakly compact. If every integral of $g$ is positive, compactness gives a positive minimum. Failure of a uniformly positive time average for every sufficiently large averaging time would produce empirical measures with nonpositive averages and an invariant weak limit, a contradiction. The boundary-term estimate establishing invariance is uniform for every fixed time shift.

The proposed function
$$
h_T(x)=\frac1T\int_0^T(T-t)g(\Phi_t x)\,dt
$$
is smooth for finite $T$. Integration by parts gives $Xh_T=-g+A_Tg$, with the sign exactly as stated. Thus it supplies strict positivity. Necessity follows by integration.

Applying this to $g+\delta$ proves the approximate criterion. Conversely, integrating $g+Xh_\delta\geq-\delta$ and letting $\delta$ decrease to zero proves the invariant-measure inequalities. There is no convergence or compactness assertion about the functions $h_\delta$, so exact attainment does not follow.

## 5. The explicit nonattainment example

All arithmetic and smoothness assertions about the Liouville flow are valid.

For $q_n=10^{n!}$, the truncation numerator $p_n$ is an integer. The first omitted term of $q_na-p_n$ is exactly $q_n^{-n}$. Ratios of successive remaining terms are at most $1/10$, so the entire positive tail is at most $(10/9)q_n^{-n}$, and in particular satisfies the submitted weaker bound $2q_n^{-n}$. The stated rational-separation argument proves irrationality.

Because $|k_n|\leq Cq_n$, every fixed derivative order $m$ is dominated by a convergent series: once $n\geq2m+2$, $q_n^{m-n/2}\leq q_n^{-1}\leq10^{-n}$. Thus the defining Fourier series and each derivative converge uniformly, giving a smooth function. Its mean is zero, and no frequencies coincide even up to sign because all second coordinates are positive and strictly increasing.

The continuous irrational linear flow has exactly one invariant probability, Haar measure. The Fourier proof in the note is correct; density of trigonometric polynomials completes the determination of the measure.

A continuous nonnegative function with zero integral against full-support Haar measure is identically zero. Hence a smooth nonnegative representative would solve $Xh=-g$. The required Fourier coefficients have magnitude at least $\frac14q_n^{n/2}$, contradicting even the boundedness of Fourier coefficients of a continuous function.

There is also a direct independent check of approximate attainment: the finite smooth sums
$$
h_N=-\sum_{n=2}^{N}
\frac{c_n}{q_na-p_n}\sin(k_n\cdot(x,y))
$$
satisfy
$$
\|g+Xh_N\|_\infty\leq\sum_{n>N}c_n\longrightarrow0.
$$
Their unbounded coefficients prevent a smooth or continuous limiting solution. Thus the claimed closure-versus-attainment distinction is genuine.

This example has zero Haar average and is a flow on a two-torus. It is not presented as a nonzero-Godbillon–Vey example, as an allowable gauge pair of the source problem, or as a minimal taut foliation on an atoroidal 3-manifold. The failure of attainment in this general transport setting does not establish failure for the source's more constrained gauge family.

## 6. The Euler-class observation and the remaining gap

If $X_f$ vanishes at a point, then $d\alpha_f$ vanishes there. Since $\alpha_f$ is nonzero, $\omega-df$ is proportional to $\alpha_f$ at that point. Wedging with $d\omega$ proves $g_f=0$, and $X_fh=0$ as well. Every auxiliary representative for that fixed gauge therefore has zero density there.

Strict positivity would force a nowhere-zero vector field tangent to the oriented plane bundle $T\mathscr F$, and hence zero Euler class. This is a necessary condition for the stronger contact requirement. It says nothing against weak-sign representatives allowed to vanish.

The manuscript leaves precisely the right unresolved tasks: selecting a gauge $f$ using the minimal/taut/atoroidal hypotheses, obtaining all necessary invariant-measure inequalities, and proving actual weak-sign attainment if zero averages remain. It neither constructs an admissible foliation for which all gauges fail nor upgrades the smooth analysis to arbitrary $C^2$ data.

## 7. Verification and disposition

All **61 submitted checks** reproduce byte for byte from the preserved replay copy. The checker hash is

6d8dea9de4cd15bd79f35e71f99799b36fcd805c793cc39633b92db3920f362c.

The [independent checker](independent_checks.py), which imports none of the submitted code, passes **209 exact assertions**. It uses non-coordinate defining forms with three varying components, verifies the full gauge density and tangent divergence-free fields, and checks transport signs and rational small-divisor/summability controls. The [receipt](independent_results.json) records their scope. SymPy 1.14.0 is used; the infinite-series, invariant-measure and nonattainment arguments were assessed mathematically above.

The primary source PDF hashes match the provenance manifest, and the frozen mathematical artifact remains unchanged. A bounded current-source search found no verified full resolution; this is not an exhaustive literature certificate.

**Required corrections: none.** The package is suitable for a draft PR labeled **unsolved, one substantive attempt, no novelty claim**, with its smooth-category and abstract-diagnostic qualifications retained. The original Question 13.1 is not solved by this work.
