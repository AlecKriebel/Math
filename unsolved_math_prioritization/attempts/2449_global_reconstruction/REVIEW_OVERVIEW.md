# EP1038 / database 2449: audit of the reconstructed finite-polynomial proof

Date: 2026-10-12 UTC.

## Disposition

The combined independent evidence supports the following scoped conclusion: for nonconstant monic real polynomials with all roots in \([-1,1]\), the infimum of \(|\{x:|f(x)|<1\}|\) is the exact number \(L=\Lambda(q_*)\) defined by the specified zero-platform one-cut family. Every individual finite polynomial has length strictly greater than \(L\), and an explicit positive-platform empirical approximation approaches it. The one-cut minimizing parameter is unique.

The enclosures are
\[
0.025715536866527<q_*<0.025715536866528,\qquad
1.834430475762661<L<1.834430475762662.
\]
Tao's Theorem 2.1 is used separately for the supremum \(2\sqrt2\) and its equality classification, \(f=(x^2-1)^m\), \(m\ge1\).

This is an independent reconstruction and audit of the proposed Wang argument and Tao construction, with no novelty claim. The work uses conventional mathematical reasoning and AI-assisted review. It is unrefereed; no external human peer review or formal proof-assistant certification has occurred or been established. The public result page still described the source as **Proposed** when rechecked on 2026-10-12. Our acceptance of the scoped evidence does not change that public status.

This edition contains authored mathematical and verification material. No publication, Git or PR operation, queue change, or release was performed by the drafting task.

## 1. What changed relative to the earlier accepted upper bound

The accepted report in [draft PR 1310](https://github.com/AlecKriebel/Math/pull/1310), at commit 845701107993994ce9d56a93164535bcb9b33874, established only
\[
\inf |E_f|\le\Lambda(q_c)
<1.83443047576266171109075363512901884952989750747
<1.834430475762662
\]
for the exact fixed rational
\(q_c=0.02571553686652745032257637166391965344\).
It included the positive-platform and finite-polynomial recovery arguments, but did not accept global family minimization, the matching lower bound, or nonattainment.

The additional accepted evidence now consists of:

1. A complete independent reconstruction of the one-cut minimum certificate, with exact record replay.
2. A sufficient independent reconstruction of the all-parameter reference and scalar calibration certificate.
3. An independent audit of the real-enclosure kernels on the domains actually used.
4. An end-to-end mathematical audit and independent complete recomputation of both new certificates.
5. A fresh adversarial analytic challenge that did not read the end-to-end reviewer's draft before completing its own analysis.

The earlier frozen publication and its scope have not been edited by this reconstruction. It is a source of the fixed upper bridge, not an inherited acceptance of the full theorem.

## 2. The mathematical dependency chain

The authored proof exposition carries the following implications in full.

### Finite structure

The empirical root potential is exactly \(n^{-1}\log|f|\), and finite strict-sublevel boundaries belong to the finite zero set of \(f^2-1\). Simultaneous componentwise barycentric collapse raises the potential outside the old negative set, preserving a global set inclusion. The resulting components have exactly one root cluster each, including possible single-point contact between adjacent negative components.

Reflection by the mean and translation normalize a principal atom at \(-1\) with mass at least \(1/2\). The zero-boundary case is treated separately, without division by that boundary coordinate. A single atom gives length 2. All remaining configurations have a finite ratio \(k\ge1\), rational positive residual weights, and distinct residual coordinates in \([1,2]\).

### Width and support

A concavity argument gives a lower bound \(2R_i\) for each residual component, with the correct inequality reversal on division by its negative weight. An elementary mean-deficit estimate handles \(1\le k\le29/20\), proving a stronger length bound \(>2\) with explicit positive rational margins.

For the remaining cases, finite-dimensional convexity is proved term by term through positive inverse-coordinate monomials in Lagrange inversion. Common equal-mass partitions are legitimate because the finite empirical weights are rational. Passing each fixed truncation uses dominated convergence of finitely many inverse moments. Pringsheim's theorem and the analytic implicit-function theorem justify the infinite reference series and its material derivative. A target at contact is handled with an Abel parameter; the proof does not differentiate the target width at a contact or require a fixed topological class along the whole interpolation.

### Adjoint and blocks

The adjoint's numerator vanishes at the conductor's lower endpoint and increases strictly. It is finite and gives positive mass to each nonempty quantile block. Its pairing with the material potential derivative is not identically the width derivative: the exact difference is
\[
-\mathcal A(2)v(2)\left(\sigma_-/K_-+\sigma_+/K_+\right).
\]
The top target coordinate is at most 2, so \(v(2)\le0\) and this is favorable. Fourier/Poisson coefficients establish the identity first for finite expansions. Explicit logarithmic uniform-integrability estimates extend it to the discontinuous block velocities actually needed.

Mixed logarithmic energies are absolutely integrable in angular coordinates. The tangent inequality is used only on off-block differences having the same sign. The remaining scalar minimization is attained at the auxiliary radius \(R_i=p_i r_i/2\). Summing the resulting block inequalities uses the exact total adjoint mass, not a normalization of that mass to one.

### Circle inequality

The external rearrangement input is Christ–Iliopoulou, *Inequalities of Riesz-Sobolev type for compact connected Abelian groups*, Theorem 1.1 and equation (1.3). The required inequality has no strict-admissibility assumption. We use no equality or stability result. Its inspected primary PDF cites both Baernstein's 1989 paper and its 1995 correction, avoiding reliance on an unqualified citation to the first paper alone.

The density-capped even extensions have masses \(2Q,2R\). Four quadrants produce the factor \(1/(2QR)\) in the normalized physical energy. Rearrangement for the nonnegative log-sine kernel and two fixed-mass comparisons give centered arcs. Fourier integration and square completion yield precisely
\[
\log\frac{2H}{a_\pi b_\pi}+h(Q)+h(R)
+\sum_{n\ge1}\frac{(\operatorname{sinc}(nQ)-\operatorname{sinc}(nR))^2}{n}
-\frac{\pi C_{\mathrm{eff}}}{a_\pi Q}.
\]
Here \(h\) decreases to zero at \(\pi\). The numerical calibration checks this expression on every admissible mass rectangle, including arbitrarily small positive masses.

### Strictness and recovery

Each finite block has strictly positive physical and adjoint masses. A positive normalized surplus therefore gives a positive unnormalized surplus, and a finite sum proves strict length \(>L\). No degree-uniform excess is asserted.

Recovery first increases the endpoint atom slightly while keeping the conductor fixed, yielding a positive platform and exactly two simple zero crossings. Weak empirical approximation then gives \(L^1\) convergence of logarithmic potentials; the zero-set-null sign lemma controls negative-set lengths. Only afterward is the positive buffer sent to zero. Direct discretization at a zero platform is not used. This proves actual finite-polynomial recovery and, together with the strict lower bound, nonattainment.

## 3. Numerical certificate A: one-cut minimization

The accepted independent checker uses integer intervals at scale \(2^{240}\), exact log and exponential series, explicit remainder bounds, and first/second derivative propagation. Root existence comes from opposite parameter-uniform endpoint signs and strict slope signs before interval Newton contraction. The analytic branch classification distinguishes the plus nontrivial root from the permanently present root \(u=1\).

The full chart inventory is:

- Closed singular tail: \(0\le\tau\le1/50\), including the regularized \(\tau=0\) limit.
- 38 left-bulk slabs: \(1/50\le\tau\le27/100\).
- Two convex-tube slabs: \(27/100\le\tau\le28/100\).
- 75 right-bulk slabs: \(28/100\le\tau\le87/200\).
- 51 regular-soft slabs: \(1/10\le q\le6181/50000\).
- One final soft slab, applied only on the admissible subdomain through \(q_s\).

Exact endpoint and overlap checks close all joins, including the cross-coordinate overlap \(1/10<e^{-200/87}<q_s\). The final soft existence sign at \(y=0\) is supplied analytically by \(q\le q_s\); no root is asserted on the numerically oversized inadmissible portion.

The two inner derivative signs, together with strict convexity on the whole tube and strict outer derivative signs, establish exactly one stationary point and global minimality in this family. The raw \(L\)-interval is strictly below the exact comparison target used in certificate B; this has been checked with exact rational arithmetic, rather than a common rounded decimal prefix.

Frozen identities:

- Independent checker SHA-256: 604c89d60cb6640f3c965b6037249e379e56e013e1d37bf7ff17368061bfc992.
- Exact integer certificate SHA-256: 01a37c997aa6c705b7dc48995f7d731848eccabe802136097a07c31762818e9a.
- Builder normal/-O/-OO and independent auditor exact-replay output SHA-256: 2ce48fdfbc3922ec77e27200bdbe897cb523dbf2ecac70cdd70b300e4d5fcb1c.

The saved certificate replay uses no floating proposals. This fact does not imply that its program is formally verified.

## 4. Numerical certificate B: sufficient all-parameter replacement

The independent implementation uses integer intervals at scale \(2^{160}\), with directed log, exponential, integer square root, Machin \(\pi\), and trigonometric Taylor enclosures including possible interior critical points. Floats only propose brackets or reduction integers that are checked by exact tests. The full regeneration is not described as float-free.

It verifies 1,530 finite slabs and one closed singular-tail box:

| Reference | Slabs | Strict normalized surplus lower bound |
|---|---:|---:|
| Affine \(a=1153/500-k/4\) | 395 | \(0.028229353338717\) |
| Constant \(a=9/5\) | 840 | \(0.036361685512222\) |
| Simple terminal | 256 | \(0.000564594536104\) |
| Refined terminal | 39 | \(0.065630278169259\) |
| Closed singular tail | 1 | \(0.961762019209\) |

These are independently sufficient margins, not acceptance of the source author's stronger figures or exact subdivision choices.

The finite regimes test at the exact rational upper target
\(T=1.83443047576266171109075363512901884952989750747\).
Increasing the target decreases the surplus, so \(L<T\) is the necessary one-sided bridge. It follows both from the previously accepted candidate upper bound plus family minimality, and directly from the new raw \(L\)-interval.

The terminal references have \(C=0\), and certificate A supplies \(M_0\ge L\), hence \(C_{\mathrm{eff}}\le0\). The canceled scalar denominator and cap formulas are algebraically verified for every finite positive parameter. Tail positivity is established without dividing by an interval containing zero. The map \(k(q)\) decreases to cover all finite \(k\ge21/5\), with strict finite-regime overlap. The case of all mass at the principal atom was handled separately.

Frozen identities:

- Finite checker SHA-256: 48b28eb878de3d868d25ab4b23fdf34752fa0eb7b621df41e62b49f43c82e43d.
- Terminal checker SHA-256: 2020a31e3db7e7c2c4c0275660d68448d4f6a70f6916a380c2f668c2b6e9921c.
- Complete finite result SHA-256: 911f446ad8a1d9133baf6f2775dd05a6ab70a3f5ca4d1c680b54c2041177326f.
- Complete terminal result SHA-256: 7f63d1b0af640f2f64be4329a124d2c31e1dcee75f3b972aca805e4bd6f66fd1.
- Final reconstruction manifest SHA-256: d755191feb3e6a21a856302ba5ad193610cda60413f957164c36eea1a73126b9.

Builder normal/-O/-OO executions were byte-identical. The independent end-to-end auditor separately recomputed all finite and terminal slabs in normal Python and obtained the exact same complete bytes. This was not merely a check of record counts or saved PASS fields. Coverage/domain corruption controls rejected nine deliberately invalid cases.

## 5. Independent kernel and end-to-end reviews

The kernel review accepted the elementary enclosure interpretations, Taylor remainders, derivative rules, uniform brackets, and mean-value Newton contractions on the actual declared domains. Its 2,454 exact tests included 29 rejection controls; normal/-O/-OO receipts were byte-identical. It explicitly did not by itself accept certificate coverage or the finite-polynomial theorem.

The end-to-end review checked those missing interfaces and performed the complete independent certificate recomputations. Its accepted scope includes finite atomization, degenerate normalization cases, the supporting-series limit, the corrected adjoint and discontinuous velocity limit, circle normalization, all parameter joins, exact target linkage, finite strictness, and positive-platform recovery.

The separate fresh adversarial review independently challenged the analytic interfaces. It found no blocking defect and accepted their implication conditional on the explicit certificate/reference assumptions. Those assumptions are discharged by the separate numerical audit. It examined genuine finite contact, coalescing roots, endpoint roots, tiny blocks, large circle masses, material topology changes, and strict versus weak sublevels. Its six floating diagnostics were only corroborative; no floating diagnostic was treated as an exact certificate.

Verification metadata:

- End-to-end authored report SHA-256: c50eb17031106d933298deae20bfaddc60b1fbee7f742f78b32ca2f4837bed95.
- End-to-end acceptance record SHA-256: f48e610234deeca26d9b475c60da6506636ede361e67d690a560bb61d3a810c9.
- End-to-end manifest SHA-256: 19e360686444a2680d8e8ebd070fd075e00f9b895a4843f420beb73eca950b3f.
- Exact interface normal/-O/-OO receipt SHA-256: e3959d26383114617587211202205ca2785bb9d1b6f7e569256cba1c83352b3b.
- Fresh adversarial analytic report SHA-256: 4ae5be6cf18ec948c15e8f7a5e91f41585902701adc8f0de7b486358cd6689da.
- Review-status editorial clarification SHA-256: a433077a89b0b6137065d982f96fe622dc85f34adc246393e78145f41feaae37.

The last clarification records that the sealed report's phrase about ordinary human mathematical review must not be understood as evidence of external human peer review. This edition uses the corrected status language and does not modify the sealed report.

## 6. Limits and evidence availability

The accepted uniqueness is only that of \(q_*\) in the specified one-cut family. No uniqueness or classification of arbitrary relaxed minimizing probabilities is proved. No new universal lower theorem for non-empirical measures, proof-assistant theorem, external peer-review acceptance, or problem-site acceptance is claimed.

The proof depends on named standard mathematical results, the Christ–Iliopoulou circle inequality, Tao's external supremum theorem, and the pinned exact-integer implementations and their execution. No source-author numerical verifier, source-author Lean project, installer, or copied executable was run in this reconstruction.

The code and complete new certificate records remain local. They are not supplied by this proof-and-audit edition. The algorithm, exact domains, coverage obligations, remainder estimates, and evidence identities are specified, but a hash alone does not let a public reader execute an omitted record. No self-contained executable public-reproduction claim should accompany this edition unless the appropriate files are actually supplied and independently checked under a separately authorized release.

The mathematical reviews leave no identified blocking gap within the accepted finite-polynomial scope. Code/data publication permission remains a separate release boundary, not a missing step of the already performed local numerical proof.

## Public sources

- [Original EHP problem, printed page 131](https://users.renyi.hu/~p_erdos/1958-05.pdf)
- [Wang proposed manuscript](https://multiscalar.ai/results/erdos-1038/paper.pdf) and [result-page status](https://multiscalar.ai/results/erdos-1038/)
- [Tao's updated note, December 27, 2025](https://terrytao.wordpress.com/wp-content/uploads/2025/12/erdos-1038-2.pdf)
- [Christ–Iliopoulou primary theorem](https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-christ-iliop.pdf)
- [Previously accepted fixed-candidate draft PR 1310](https://github.com/AlecKriebel/Math/pull/1310)

Source hashes, sizes, inspection history, and the publicly stated manuscript status are recorded in the separate source-verification metadata. No third-party source text or source file is part of this authored edition.
