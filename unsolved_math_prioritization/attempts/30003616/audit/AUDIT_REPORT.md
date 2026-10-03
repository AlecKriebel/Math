# Independent adversarial audit: continuum Fibonacci spectral rays

**Problem:** 30003616 / OWR-15951-003, rank 505.  
**Audit date:** 2026-10-03 UTC.  
**Verdict:** **PASS_PARTIAL**. Retain **`unsolved 5/5`** and **`full_resolution: false`**.  
**Blocking mathematical findings:** none in the frozen partial-result claims.

The packet correctly formulates the original full-plane problem, proves the displayed transfer-matrix bound, supplies two valid abstract sumset obstructions, and proves its conditional mixed-spectrum thickness criterion. It does not establish the missing thickness hypotheses for arbitrary tiles. Neither an affirmative solution nor a counterexample within the continuum Fibonacci class has been obtained. Passing this audit is not permission to relabel the problem solved or to describe the abstract Cantor examples as spectral counterexamples.

## 1. Frozen scope and independent checks

This audit covers exactly the six files recorded in `FROZEN_INPUTS.json`: `README.md`, `RESEARCH_LOG.md`, `RESULT.md`, `SOURCE_AUDIT.md`, `checks/check.py`, and `checks/results.json`. The audited `RESULT.md` has SHA-256

`f5320a2ba9eae725c000c71c3ad7825226c76c9c1d1b98b16d4676648583a2b7`.

Every input byte count and SHA-256 matched the freeze before and after the audit. No frozen file was edited. The author’s six exact-check functions were called without invoking their file-writing entry point; all passed. A separate control script verifies a stronger unrestricted commutator identity rather than reusing the author’s determinant-ideal calculation. It also checks the transfer normalization, simultaneous conjugation, residue obstruction, digit counts, and both overlap margins. There are **47 passing positive controls and six rejected negative controls**. These are symbolic or exact rational/integer checks, not spectral numerics.

The substantive analytical arguments were reviewed separately. A finite collection of digit counts does not prove Hausdorff dimension or nullity; finite matrix substitutions do not prove the transfer estimate; a finite list of spectral approximants cannot establish a spectral ray. The supplied artifacts maintain these distinctions.

## 2. Source target and literature boundary

The source is Fillman’s contribution to [Oberwolfach Report 46/2017](https://publications.mfo.de/handle/mfo/3610), report-local pp. 17–18, equations (1)–(2) and the final question. It concerns a one-dimensional continuum operator on the entire real line, then the separable two-dimensional operator on the entire plane. The tile pair consists of arbitrary real square-integrable functions on a unit interval. The final quantifier is every pair of positive couplings. “Half-line” refers to a spectral energy interval, not a spatial domain or a boundary condition.

The floor-difference coding in `RESULT.md` is consistent with the usual indicator coding and with equations (1.1)–(1.2) in the [2026 Damanik–Embree–Fillman–Gorodetski–Mei paper](https://arxiv.org/html/2603.24462v1). Its Theorem 1.1 is a fixed-energy, large-coupling dimension counterexample. Its Theorem 1.3 assumes one zero tile and a continuous nonnegative other tile with nowhere-dense zero set. Neither result is a negative answer to the fixed-coupling, arbitrarily-high-energy ray question. No interchange of these limiting regimes is allowed.

[Fillman–Mei](https://arxiv.org/abs/1702.04337), Theorem 1.1 and the standing assumptions preceding Theorem 1.3, distinguish aperiodic potentials from periodic degeneracies. Proposition 2.2 gives nonnegative invariant at spectral energies. Theorem 2.3 gives the universal local-dimension function and its square-root deficit near zero. The theorem page was checked visually to disambiguate the extracted radical. These inputs require the stated aperiodic continuum Fibonacci setting; the elementary transfer estimate itself needs only integrable real pieces. The frozen packet does not silently extend the dimension theorem to arbitrary integrable potentials or to periodic degeneracies.

[Damanik–Fillman–Gorodetski](https://arxiv.org/abs/2001.03875), Theorem 3.4, concerns the two constant unit tiles and a self-sum. Lemma 2.1 supplies the exact gap-lemma consequence used by the packet. Proposition 4.2 requires curve convergence, positive invariant, a uniform absolute logarithmic-derivative bound, and specified iterated Markov-rectangle crossings. The absolute-value bars in condition (3) were checked on the PDF. Remark 4.25 identifies the derivative bound as a key difficulty for general tiles, and Section 6, Question 1 retains the general-tile self-sum question. The frozen result correctly preserves this boundary.

[Fillman–Tidwell](https://arxiv.org/abs/2206.00556), Theorems 1.6, 1.7 and 1.10, assumes controlled thickness and growth. Corollary 1.9 concerns powers of the spectrum from the constant-piece model. It does not manufacture the missing arbitrary-shape spectral blocks.

This is a check of the cited primary results and a bounded literature review. It is not an exhaustive novelty or current-literature certificate. The prior-attempt inventory in `SOURCE_AUDIT.md` is expressly bounded, including its failed recursive-tree request; this audit does not upgrade that administrative statement to exhaustive repository coverage.

## 3. Approach 1: realization, tensor sum, and perfectness

**Pass as an exact reduction.** A finite family of unit-interval real square-integrable tiles has uniformly bounded local integrable norms. The unit-interval Sobolev estimate, followed by summation, makes the potential infinitesimally form-bounded relative to the kinetic form. Fubini gives the corresponding separate-coordinate estimates in two dimensions. The lower-semibounded form realizations used in the packet are therefore legitimate even when tiles are unbounded or sign-changing.

The joint spectral theorem gives the closure of the sum of the two one-dimensional spectra. Lower bounds make that sum closed: if sums converge, neither summand can escape upward while the other escapes downward. After extracting one convergent subsequence, the other converges as well, and the limits remain in their closed spectra. Tensor products of approximate eigenvectors give the reverse spectral inclusion. Thus the stated equality is valid for the canonical form sum.

The aperiodic Cantor-spectrum theorem and periodic band theory imply perfectness in their respective cases. Fixing one summand while approaching the other by distinct points proves that a closed sum with a nonempty perfect summand is perfect. Hence there are no isolated spectral points, and the usual essential spectrum equals the full spectrum. This observation alone says nothing about absolute continuity or embedded eigenvalues; the packet explicitly avoids those conclusions.

The equal-constant computation is correct. Unequal constant tiles with equal couplings reduce by an energy shift to the previously established constant-tile theorem. None of these arguments forces a ray for arbitrary tiles.

## 4. Approach 2: transfer estimate, sign, constants, and dimensions

**Pass.** Write \(k=\sqrt E>0\), use the state \((u,u'/k)^t\), and conjugate both tile matrices by the same \(S=\operatorname{diag}(1,1/k)\). Direct calculation yields

\[
S\begin{pmatrix}0&1\\q-k^2&0\end{pmatrix}S^{-1}
=k\begin{pmatrix}0&1\\-1&0\end{pmatrix}
+\frac qk\begin{pmatrix}0&0\\1&0\end{pmatrix}.
\]

The unperturbed propagator is an orthogonal rotation. The perturbation matrix has Euclidean operator norm \(|q|/k\). For integrable \(q\), the Volterra equation and Grönwall therefore give, over every initial subinterval,

\[
\|U(t)\|\le e^{k^{-1}\int_0^t|q|},\qquad
\|U(t)-R(kt)\|\le e^{k^{-1}\int_0^t|q|}-1.
\]

There is no uncontrolled factor of \(k\), no need for pointwise boundedness of the tile, and no need for equal tile lengths. The same conjugation preserves the traces of each tile and their product. The trace-zero generator and Liouville’s formula give determinant one.

Put \(\delta_j=e^{\|q_j\|_1/k}-1\). The two free endpoint rotations commute, and expanding the additive commutator gives

\[
\|A_0A_1-A_1A_0\|
\le2\delta_0+2\delta_1+2\delta_0\delta_1
=2(e^{M/k}-1),\quad M=\|q_0\|_1+\|q_1\|_1.
\]

An independent sign calculation is provided by the unrestricted identity

\[
\det(AB-BA)+\det(B)(\operatorname{tr}A)^2
+\det(A)(\operatorname{tr}B)^2+(\operatorname{tr}AB)^2
-(\operatorname{tr}A)(\operatorname{tr}B)(\operatorname{tr}AB)
-4\det(A)\det(B)=0.
\]

At determinant one it is exactly \(4I=-\det(AB-BA)\). The two unipotent matrices with respective upper and lower off-diagonal entry one give \(I=1/4\) and commutator determinant \(-1\), rejecting both the opposite sign and a missing factor of four. Since the product of singular values is bounded by the square of the largest singular value,

\[
|I(E)|\le(e^{M/\sqrt E}-1)^2.
\]

This is valid for every positive real energy, including energies outside the spectrum. It does not claim that the invariant is positive there. For example, for \(E\ge\max(1,M^2)\), the elementary bound \(e^t-1\le et\) for \(0\le t\le1\) gives the explicit estimate \(|I(E)|\le e^2M^2/E\). Thus the asserted order is justified with controlled constants.

For aperiodic square-integrable Fibonacci tiles, the cited dimension theorem can now be applied at spectral energies, where \(I\ge0\). Choose the universal small-invariant threshold \(I_0\) from that theorem and then increase the energy threshold until \((e^{M/\sqrt E}-1)^2\le I_0\). Its upper bound \(1-D(I)\le C\sqrt I\), together with the transfer estimate, gives

\[
\dim_H^{\rm loc}(\Sigma;E)\ge1-C(e^{M/\sqrt E}-1)
\ge1-C_qE^{-1/2}.
\]

The zero-invariant endpoint is covered by \(D(0)=1\). For \(q_j=\lambda f_j\), \(M\le\Lambda(\|f_0\|_1+\|f_1\|_1)\) on \(0<\lambda\le\Lambda\), so a common threshold and constant work on bounded coupling ranges. There is no uniform assertion as \(\lambda\to\infty\), and phase independence is legitimate. Periodic cases use band structure instead.

The missing step is correctly identified. A small absolute invariant neither excludes high zeros nor controls a logarithmic derivative. The illustrative function \(k^{-2}\sin^2 k\) has the claimed size and an unbounded logarithmic derivative near its positive zeros. This is an obstruction to an inference, not evidence of an actual Fibonacci counterexample. An application of the trace-map thickness proposition must still establish all its geometric and relative-variation conditions on suitable windows.

## 5. Approach 3: full local dimension with a null self-sum

**Pass, including the infinite-set proof.** In the stated mixed-radix construction, \(b_j=2(j+1)\), \(Q_n=2^n(n+1)!\), and the number of prefixes is \(N_n=(n+1)!\). Prefix endpoints are distinct points of \(Q_n^{-1}\mathbb Z\). The telescoping full-radix tail and the digit restriction give a tail at most \(1/(2Q_n)\). Compactness follows from the convergent expansion, and arbitrarily late digit changes prove perfectness.

An interval of length \(r\), with \(Q_n^{-1}\le r<Q_{n-1}^{-1}\), can meet at most \(rQ_n+2\le3rQ_n\) cylinders. The equal-digit product measure consequently satisfies \(\mu(J)\le3\,2^nr\). For every \(s<1\), the factor

\[
2^nr^{1-s}\le2^nQ_{n-1}^{-(1-s)}
\]

tends to zero. This is a genuine factorial-versus-exponential estimate, not an inference from sample values. For an independent check, take \(s=1-1/m\). The consecutive ratio of the \(m\)-th powers of the right-hand side is \(2^{m-1}/(n+1)\), eventually at most \(1/2\). Letting integer \(m\to\infty\) already proves dimension one. Enlarging constants at finitely many scales supplies the Frostman bound. Conditional product measures with any finite prefix fixed obey the same argument. Every neighborhood of every point contains a sufficiently small such cylinder, proving local dimension one everywhere, including endpoints.

Adding two allowed expansions produces digits \(0,\ldots,2j=b_j-2\), with no carries. The self-sum has covers of total length

\[
\prod_{j=1}^n\frac{2j+1}{2j+2}.
\]

Taking logarithms and using \(\log(1-t)\le-t\) bounds this by an exponential whose exponent tends to negative infinity, since \(\sum_j1/(2j+2)\) diverges. Thus the self-sum is null. Monotonicity of a finite cover sequence alone would not have established this limit; the written proof uses the divergence correctly.

The translates defining \(S=\mathbb Z_{\ge0}+K\) are locally finite, so \(S\) is closed and perfect. It contains the nonnegative integers, bounding every bounded complementary gap by one. It retains full local dimension at each point, while \(S+S\) is a countable union of null sets. It therefore contains no nondegenerate interval. This rigorously defeats the dimension-only mechanism, even with bounded gaps and null perfect sets. It says nothing against additional restrictions imposed by Fibonacci dynamics.

## 6. Approach 4: mixed paired blocks and squaring

**Pass as a sufficient criterion only.** The imported gap-lemma consequence has exactly the hypotheses used: thickness product greater than one and the largest gap of each compact Cantor set no larger than the other diameter. It makes each stated paired sum a full interval.

The first overlap condition is precisely

\[
a_n+c_{n+1}\le b_n+d_n,
\]

and the second is precisely

\[
a_{n+1}+c_{n+1}\le b_n+d_{n+1}.
\]

These link \(I_n\), \(J_n\), and \(I_{n+1}\) in the claimed order. Ordered hulls and endpoints tending to infinity ensure their union from any sufficiently large index is an entire ray. No equal-coupling assumption or equality of the two spectra is hidden here.

In the square-energy corollary, large blocks lie in positive \(k\). On a hull \([l,u]\), the map \(k\mapsto k^2\) changes every interval length by a factor between \(2l\) and \(2u\). Transporting an arbitrary gap presentation therefore gives \(\tau(K^2)\ge(l/u)\tau(K)\). The ratio tends to one for bounded-width hulls translated to infinity.

Squaring the two endpoint expansions gives energy widths \(2nPW_j+o(n)\) and consecutive gaps \(2nP(P-W_j)+o(n)\). Both required overlap differences have the same leading coefficient

\[
2P(W_1+W_2-P)>0.
\]

The shifts between the two families affect only lower-order terms. The script independently expands both polynomials and rejects a deliberately too-narrow pair of windows.

The largest-gap estimate is also valid with the supremum-over-presentations definition of thickness. If a gap has length \(g\) in a hull of diameter \(D\), its two presentation bridges have total length at most \(D-g\). A presentation with all bridge/gap ratios at least \(t\) implies \(2tg\le D-g\). Taking \(t\uparrow\tau\) gives \(g\le D/(1+2\tau)\). Adjacent squared block diameters have finite positive limiting ratios, and thicknesses diverge, so the mutual largest-gap conditions follow.

The packet does not produce the required block families for general tiles. The corollary is a correct separation of the elementary assembly step from the unsolved spectral geometry, not a solution disguised as a hypothesis.

## 7. Approach 5: self-sum transfer and approximation

**Pass.** If \(C\) is half the middle-thirds Cantor set, the standard balanced-ternary argument yields \(C+C=[0,1]\). The specified residue sets satisfy \(B_0=-A_0\pmod {12}\). Actual integer sums from \(A_0+A_0\) cover \(0,\ldots,11\), yielding \(A+A=[0,\infty)\). The \(B_0+B_0\) sums cover each residue with a representative at most \(r+12\), yielding the claimed ray beginning at 12.

The mixed residues miss 6. An interval from the mixed sum has integer left endpoint and length one; therefore it cannot enter the open unit interval from \(12m+6\) to \(12m+7\) without having exactly the missing left-endpoint residue. The gaps persist at arbitrarily large heights. Local finiteness and the Cantor pieces supply closedness, perfectness, nowhere density, and nullity of \(A\) and \(B\). This is a valid obstruction to transferring two self-sum conclusions to a mixed sum without additional shared geometry.

The approximation cautions are valid as well. The scaled sets \(j^{-1}S\) contain a mesh of size \(1/j\) and lie in the nonnegative ray, giving the stated Hausdorff-distance bound, while their self-sums remain null. The sets \((S\cap[0,n])\cup[n,\infty)\) agree locally with \(S\) once \(n\) is large enough and possess rays. In fact their self-sums contain \([n,\infty)\), since \(0\in S\), while their parts below \(n\) remain null. Their ray thresholds genuinely escape to infinity. Thus no continuity argument from approximants works without the appropriate uniform threshold and justified spectral limit.

## 8. Release recommendation and limits

The frozen mathematical package can be retained as an **audited five-approach unsuccessful investigation with rigorous partial deductions**. Preserve all of the following qualifications:

- The exact target remains the arbitrary real square-integrable-tile, full-plane continuum problem for every positive coupling pair.
- The improved invariant and local-dimension bounds do not establish thickness or a spectral ray.
- The paired-block result is conditional; the hypotheses have not been constructed for the general target.
- The abstract sumset examples are not Fibonacci spectra and do not refute the target.
- The 2020/2021 constant-tile theorem remains credited as prior work.
- There is no claim of priority, exhaustive literature coverage, or full resolution.

No correction is required to the frozen mathematical statements for that restricted disposition. The nonmathematical progress percentages in the research log are clearly labeled estimates and must not be promoted to proof confidence.

The portable audit consists only of this report, `audit_controls.py`, `audit_controls.json`, `author_rerun.json`, `FROZEN_INPUTS.json`, and `AUDIT_MANIFEST.json`. It contains no downloaded paper, full source extract, source screenshot, private catalog material, or research corpus. No remote mutation was performed.
