# Independent analytic and semantic review

This is an adversarial deduction record. It is not a worldwide literature-exhaustiveness certificate and is not a final packet PASS. Primary facts are recorded only in the bounded source capsules below; the remaining sections are the reviewer's mathematical deductions and editorial judgments.

## Bounded source capsules

**O (bounded capsule).** The original is Podolskij's contribution in OWR09/2013, printed491-493. Its pure-jump paragraph gives a compound-Poisson fixed-time stable quadratic-variation limit for kernel x_+^alpha f(x), 0<alpha<1/2, exponentially decaying smooth f nonzero at zero. The statistic uses deterministic mesh tending to zero. The proposed extension asks for sufficient conditions for a substantially general pure-jump semimartingale driver. It does not state a maximal driver class, a specified characteristic condition, or a functional topology. The other parts of the contribution concern Gaussian processes and fields. Read the complete contribution, including references; visually inspected all three pages. Primary URL: https://ems.press/content/serial-article-files/46440 .

**P (bounded capsule).** Basse-O'Connor, Heinrich and Podolskij's arXiv1604.02307v2, public14October2016, model(1.2), uses (g(t-s)-g0(-s)) sigma_(s-)dL_s, with adapted cadlag sigma and symmetric pure-jump Levy L relative to the filtration. Independence of sigma and L is not required. Under(A),(B1), beta<2, p>beta, p>=1 and alpha<k-1/p, Theorem1.2(i) gives functional F-stable M1 convergence on the1/n mesh to a uniformly marked jump sum. Assumption(A) includes local power behavior, tail integrability, and eventual monotonicity of the relevant absolute derivatives. Assumption(B1) controls the remote-past random derivative integrand. Remark1.4 excludes J1 and J2. The complete part(i) proof was read, including the all-F statement after Lemma4.3. The arXiv history dates v1 to8April2016 and v2 to14October2016; later PDF compilation dates do not set public priority. The associated journal citation is Bernoulli24(4A)(2018),3117-3146. Primary URL: https://arxiv.org/pdf/1604.02307v2 .

**Q (bounded capsule).** The same authors' arXiv1806.10352v1, public27June2018, model(1.1), permits a pure-jump two-sided Levy process without imposing symmetry. Theorem2.1(i) treats regular statistic functions subject to vanishing derivatives at zero, (A), beta<2 and its auxiliary regularity exponent condition. Proposition2.3(i) gives finite-dimensional stability and M1 convergence with its sign condition. The definition of stability tests all bounded original-F variables. Read model, hypotheses, theorem, definition and proposition; visually inspected theorem/proposition pages. Associated journal article: EJP24(2019),article79. Primary URL: https://arxiv.org/pdf/1806.10352v1 .

## Exact bridge on a substantial non-Levy class

Set g(x)=x_+^alpha exp(-x), g0=0 and 0<alpha<1/2. Choose the symmetric Levy measure exp(-|z|)|z|^(-2)dz. It has small-jump index1 and total quadratic integral2. Any uniformly bounded adapted cadlag sigma yields a legitimate square-integrable stochastic integral against the associated martingale random measure; using increments avoids any nonadapted negative-time normalization of a two-sided Levy level. For a concrete non-Levy choice, deterministic sigma(s)=2+sin(s) is bounded, positive and smooth on the whole line. The instantaneous second-moment rate2sigma(s)^2 varies with time, so increments cannot be stationary. Random adapted bounded sigma adds much more than this example.

For these choices, (A) holds with theta=2. Near zero g'=O(x^(alpha-1)); at infinity g and g' decay exponentially. For x>alpha,

    d/dx log|g'(x)| = -1+(alpha-1)/x+1/(x-alpha),

which is eventually negative. For(B1), choose rho=1,beta'=3; bounded sigma makes both tail integrals finite. At k=1,p=2, p>beta and alpha<k-1/p hold. This is a genuine family of prior semimartingale sufficient conditions, not merely the source's original compound-Poisson case.

The actual jump of Y is J_T=sigma_(T-)Delta L_T. Write h(x)=x_+^alpha-(x-1)_+^alpha. For every u,

    sum_(l>=0)h(l+u)^2 = sum_(j>=1)h(j-(1-u))^2 = W_alpha(1-u).

Reflection preserves independent uniform marks and independence from original F. The g0 subtraction is time-constant and cancels from increments. Since the time-compensator has no deterministic atoms, no fixed evaluation horizon is a jump time almost surely. Evaluation at a finite list of such continuity times transfers stable M1 convergence to stable finite-dimensional convergence. This establishes the precise formula bridge on the printed mesh.

## Mesh attack and limited deduction

The source statistic allows arbitrary positive deterministic spacings tending to zero; P is printed with1/n. Rounding the frequency is an invalid proof: replacing r=1/Delta by floor(r) changes the impulse phase by s(r-floor(r)), which may remain order one. Therefore no packet may silently claim an arbitrary-mesh theorem is a literal substitution into P.

There is nonetheless no new phase phenomenon here. On the bounded-volatility finite-quadratic-rate overlap above, for each retained base-jump cutoff the ordered positive jump-time vectors have densities. If H is any bounded original-F variable, multiplying its induced time-vector measure by H produces a signed L1 density a_H. For each nonzero integer frequency vector q,

    integral a_H(s) exp(2pi i q dot s / Delta_n) ds ->0

by the Riemann-Lebesgue lemma. This works for every Delta_n->0 without monotonicity. Continuous torus approximation gives the independent uniforms while preserving all-F stability. Deterministic impulse energy bounds depend on Delta>0, not on integrality of1/Delta. A uniformly bounded sigma multiplies the small-base-jump isometry bound by at most its squared bound, so the omitted energy tends to zero with int_(|z|<=epsilon)z^2nu_L(dz). Gamma-kernel prehistory has the weighted derivative integral finite, and bounded drift is negligible. Thus the usual finite-impulse/truncation reasoning can be rerun for arbitrary meshes on this substantial overlap. This is an independent present-day deduction; it must not be retroactively attributed as the printed prior theorem. The proposed packet can safely retain the literal reciprocal-mesh qualification instead.

The all-F step never assumes a density conditional on the whole field: that conditional law would be atomic because the times are F-measurable. It uses domination of the unconditional time-vector law, followed by weighting and Fourier decay. This distinction is correct in the candidate and root mathematical acceptance.

## What the positive prior result cannot imply

Use the symmetric measure

    nu(dz)=1_(0<|z|<exp(-1)) |z|^(-3)log(1/|z|)^(-2)dz.

Substitution z=exp(-v) gives quadratic rate2int_1^infinity v^(-2)dv=2. Every power r<2 has integral2int_1^infinity exp((2-r)v)v^(-2)dv=infinity. Thus candidate membership does not imply beta<2. No scalar rescaling of a fixed base measure with smaller index reaches this index-two measure; nonzero dilation preserves the index. This refutes full containment in P. It supplies no theorem about the rest of the literature.

A deterministic compensator switching from delta_1+delta_-1 to delta_1+delta_-1+delta_2+delta_-2 has bounded quadratic rate10 and provides a second separator. Nonzero dilation preserves the number of nonzero support points; zero dilation gives no jumps. It cannot be a scalar pushforward of one base Levy measure relative to the supplied filtration. Its easy finite-noise embedding does not change the scalar theorem's hypotheses. An arbitrary mark-dependent Poisson embedding likewise does not factor its coefficient into sigma_s kappa(z); invoking a broader noise space without an appropriate theorem transfers the central difficulty to an unsupported assertion.

Conversely, a symmetric beta-stable driver with beta<2 and sigma=1 satisfies P with the gamma kernel but has infinite large-jump quadratic moment, violating the candidate's global K. The classes are nonnested. Statements calling the candidate a strict generalization of the whole predecessor or saying that predecessor includes the whole candidate would both be false.

For Q, apply F(x)=x^2 with an auxiliary q satisfying max(beta,1/(1-alpha))<q<2. Only F(0)=F'(0)=0 is then required, and the sign condition holds. The normalization is sumF(n^alpha DeltaX)=n^(2alpha)sum|DeltaX|^2. Choosing q=2 would incorrectly require F''(0)=0; distinguishing auxiliary regularity from the power is essential. This bridge validates earlier nonsymmetric Levy coverage without extending beta<2 to its excluded endpoint.

Root's kernel-perturbation deduction is also valid on its explicitly stated bounded-rate intersection: r=g-f(0)x_+^alpha exp(-x) satisfies r(0)=0, r'=O(x^alpha) at zero and r' inL1 cap L2 globally. The convolution derivative has expected L2 energy at most KT||r'||_2^2, with bounded-drift derivative at most B||r'||_1. Its normalized increment energy is bounded by Delta^(1-2alpha) times that energy. This removes an artificial tail-monotonicity distinction without manufacturing arbitrary-compensator or index-two coverage.

## Disposition semantics and lane reconciliation

The strongest attack on already_solved is semantic: the source's adjective of generality is qualitative, so no theorem proves that a particular proper subclass is the unique intended answer. A tiny extra subclass would be inadequate. But P permits broad infinite-activity non-Levy adapted-volatility families, giving a substantive advance beyond the source baseline. Under the supplied user definition concerning whether the original open problem was actually still open and credit, a qualified historical prior-answer catalog judgment is defensible. Its justification is positive prior mathematics, not search failure.

This is not equivalent to complete exact-candidate anticipation. No inspected theorem settles that, and inaccessible primary leads remain material for any novelty certification. Nor does C outside P imply C is new. Requiring the source to mean exactly the candidate after the candidate has been written would add a new quantifier retrospectively; claiming P exhausts every possible intended interpretation would also exceed the source. The editorial judgment must stay visibly qualified.

All five lanes agree on the operative mathematical boundary. General-Volterra and boundary-class lanes report exact-class priority unresolved; history and novelty lanes support a substantial historical prior answer; classical coverage identifies established proof mechanisms and explicit scope separators. These are compatible answers to distinct questions, not contradictory verdicts. Whole-source access limitations in neighboring fractional-integral papers and the2018 book chapter prevent a blanket literature-exclusion claim; they do not erase the authenticated positive theorem P. The prior2014 announcement and early versions support chronology only; this review relies on the corrected2016v2 source for a valid M1 statement.

No required mathematical or semantic repair to PROPOSED_CREDIT_DISPOSITION.md has been found at this stage. All its reciprocal-mesh, nonnested-class, exact-novelty and no-promotion qualifications must survive in the current packet. Final disposition and native-application clearance are withheld until every proposed current file, archive byte and manifest has been checked.
