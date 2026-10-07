Independent pinned-source upstream audit, round 2

Completed 2026-10-07 04:32 UTC. Audit completion estimate: 100% of this assigned external-input review. This percentage concerns the review task, not a new discovery or a formal verification claim.

**Verdict: no mathematical defect or missing assumption found in the central upstream input actually used by the candidate.** The main and atomic manuscripts both support the required density-one ordered Riesz lower bound. Their normalizations agree exactly with the candidate. The verdict rests on reading the analytic source and freshly recomputing the finite arithmetic, rather than treating certificate success as an analytic proof.

The candidate inspected was `/Users/alec/Documents/Math/openai_followon_riesz_surface_constants/publication/main.tex`, SHA-256 `ee210daea871f3db4f84775f40197cc2ef07bc3c286da76acfb448f57c2e03d3`. Its central import occurs at lines 75–93; its use in the gap-periodization proof occurs at lines 188–195.

The actual upstream checkout `/Users/alec/Desktop/math` was verified at HEAD `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. All 34 byte counts and SHA-256 values in the candidate's `sources/UPSTREAM_MANIFEST.json` were independently checked against that checkout and matched. The upstream working tree was clean before and after the inspection and computations. No candidate or upstream source, Git state, publication, or deposit was modified. This report is the only file written by this reviewer.

**Exact claim and conventions.** Let

\[
b=\sqrt3/2,\qquad A=b^{-1/2}\{j(1,0)+k(1/2,b):j,k\in\mathbb Z\}.
\]

For every locally finite set \(\mathcal C\subset\mathbb R^2\) satisfying \(\#(\mathcal C\cap B_R)/(\pi R^2)\to1\), and every real \(s>2\), the imported conclusion is

\[
\liminf_{R\to\infty}\frac{1}{\#(\mathcal C\cap B_R)}
\sum_{\substack{x,y\in\mathcal C\cap B_R\\x\ne y}}|x-y|^{-s}
\ \ge\ \sum_{a\in A\setminus\{0\}}|a|^{-s}.
\]

The sums are ordered, the disks are centered at zero, and the lattice has covolume one. This is exactly the specialization \(g(t)=t^{-s/2}\) of main §1, lines 10–40, Theorem `thm:universal`; the atomic manuscript states the same definitions and theorem at lines 46–76. The candidate's \(\Lambda\) is this same lattice, not a differently scaled representative. There is no factor-of-two or Fourier-normalization conversion. Complete monotonicity follows from \((-1)^r g^{(r)}(t)=(s/2)_r t^{-s/2-r}>0\). The source theorem places no separation, occupancy, translated-density, or periodicity condition on the competitor. The candidate's density-one square-periodic configurations are therefore included.

The necessary argument was read directly from the main source, all of §§1–7, the Gaussian-construction scalar part of Appendix A (lines 1–339), and the relevant finite checker source. The atomic analytic chain received a separate adversarial source review, reported below. The long-range renormalized/jellium argument and its field approximation appendix are not dependencies of this \(s>2\) import and were not promoted by this verdict. No previous audit's conclusion was used as a premise.

**Main manuscript: analytic dependencies checked.** All section-file references below are relative to `preprints/Universal-optimality-of-the-triangular-lattice-September-23-2026/build/sections/` in the pinned checkout.

1. `02-cardinal-fourier.tex`, lines 18–55, correctly uses the radial coordinate \(\tau=b|x|^2\), contains all nonzero triangular shells in the periodic set \(12\mathbb Z+\{0,1,3,4,7,9\}\), and proves \(A^*=JA\). The extra interpolation nodes are intentionally a superset. They are not silently assumed to be lattice shells. The product, coefficients, and node constants at lines 107–157 agree with that node set.

2. The cardinal measure proof at lines 170–267 constructs the genuine entire extension from a finite complex measure on \([-1,1]\). Its per-node variation estimate is independent of node location and is sufficient for arbitrary unweighted \(\ell^1\) lists. The positive-frequency real-part formula is correctly restricted to real evaluation, with the full complex integral supplying holomorphy. The Gaussian transform at lines 271–360 is genuine Fourier transformation: \(\gamma=b(h-it)\), \(\widehat{e^{-\pi\gamma|x|^2}}=\gamma^{-1}e^{-\pi|\xi|^2/\gamma}\), and the stated \(\lambda,z\) give the transformed profile after removing the positive damping factor. Uniform Gaussian domination justifies Fubini, derivatives, Schwartz seminorms, and the reverse transform. The frequency involution is not improperly substituted for a contour or function-space inverse.

3. The transformed-jet bounds at `02-cardinal-fourier.tex`, lines 397–515, correctly split the last frequency interval from the other five and include the endpoint atom at 1. Both the crude bound \(\|S\|<4000\) and the sharper output-tail bound \(U_r(w,c)\) hold uniformly over every input-node location. This uniformity is essential when a finite block is coupled to infinitely many unknown tail coefficients; it is actually proved, not inferred from a truncated matrix.

4. `03-quadrature-finite-data.tex`, lines 33–199, proves positivity and degree-383 exactness of the Fejér rule with the stated interval mass normalization. The atoms remain exact. The Cauchy estimate applies on analytic disks of radius \(1/6\), covers all input/output nodes through 168, and gives a uniform scaled-moment error below \(10^{-31}\), including arbitrary derivative order. Thus the finite certificate is connected to exact spectral integrals by an analytic error bound. The finite matrices, extra coordinates, target columns, shared reciprocal parameter, signed half-gaps, deleted quotients, Bernstein coefficients, and tail rows at lines 201–530 match the subsequently used formulas. The parameter-box minimum is a valid multilinear box minimum, not point sampling.

5. `04-exact-interpolation.tex`, lines 95–195, first inverts the paired finite block and then eliminates it. The exact finite inverse bound is below 40. The tail-output estimate is \(\delta=1.1\cdot10^{-14}\); the resulting Schur perturbation satisfies \(\|\mathcal Q-I\|<\delta(1+40\cdot4000)=1.760011\cdot10^{-9}<1\). This establishes a bounded inverse on the full pair of Banach spaces. It does not transfer the central interpolation difficulty to an unsupported invertibility statement. Lines 225–344 include the omitted target jets, finite-geometric-sum residual, quadrature errors, extras, and full tail residual, obtaining an exact-list correction below \(2\cdot10^{-8}\), exact jets at every positive node, and combined norm below 5.

6. `05-global-signs.tex`, lines 68–284, deletes the value and slope of each component before approximating its quotient. Only the exact slack uses zero jets. This prevents an approximate constant or linear residual from being divided by a vanishing square. The correction, spectral Taylor remainder, and target-support errors are retained separately; the resulting quotient margin is \(.001-.00011-.000001-.000001=.000888>0\). The target supports handle both signed half-gaps at node 1 and the unbounded parameter interval. There is no Taylor approximation with an unbounded parameter, because the target support uses the bounded left endpoint \(K\le6\).

7. `05-global-signs.tex`, lines 295–492, covers the entire unbounded radius range. Log-concavity of \(P(\tau)/(\tau-m)^2\) between a zero and an adjacent midpoint yields the continuum sine-product barrier \(P(\tau)\ge .68(\tau-m)^2\). The signed low-node rational part exceeds .002 after correction. The combined high-node/transformed/target remainder has an independently bounded second derivative below .0002 and has exact double zeros at every node from 91 onward. At the junction \(\tau=89.5\), choosing the tied nearest node 91 keeps the Taylor segment within the controlled tail. The comparison \(.68\cdot.002>.0001\) proves the tail signs. Small coefficient norms alone are not incorrectly treated as a sign theorem.

8. `06-gaussian-energy-transfer.tex`, lines 25–128, proves density-only linear programming using a positive Fourier quadratic form and area measure in a slightly larger disk. The cross-term error is uniform for all points of the disk, so clustered points and highly uneven local counts cause no gap. Lines 139–219 correctly convert the normalized theorem with \(k=\pi(\alpha/b-h)>2.36\) for \(\alpha\ge1\), use the reciprocal Gaussian complement for \(0<\alpha<1\), and apply unit-covolume Poisson summation. The equality \(\widehat f_\alpha(0)-f_\alpha(0)=\sum_{a\ne0}e^{-\pi\alpha|a|^2}\) has the correct dimension-two factor.

9. `07-shifted-mixtures.tex`, lines 21–133 and 142–232, gives a finite positive measure after a positive shift, preserves endpoint atoms, and applies Fatou along every sequence of radii. It mixes nonnegative scalar energy kernels, not the auxiliary functions. The shift is removed only on the lattice side. The lattice attainment argument separately handles finite and infinite sums. No improper interchange of a configuration lower limit, a shift limit, or an auxiliary-function infimum was found.

**Independent Riesz specialization check.** The needed hypersingular conclusion also follows directly from the already established Gaussian energy inequalities, without depending on the general moment-representation construction. Set \(p=s/2>1\). The exact positive representation is

\[
|z|^{-s}=\frac{\pi^p}{\Gamma(p)}\int_0^\infty\alpha^{p-1}e^{-\pi\alpha|z|^2}\,d\alpha\qquad(z\ne0).
\]

For any sequence \(R_j\to\infty\), apply this identity to the finite ordered-pair sum, then Fatou to the nonnegative \(\alpha\)-integrand. The pointwise Gaussian lower bound applies along that sequence. Tonelli on the lattice side gives exactly \(\sum_{a\ne0}|a|^{-s}\). Since the sequence was arbitrary, the full-radius lower bound follows. This confirms the exponent, the factor \(\pi^p/\Gamma(p)\), and the lower-limit direction independently. The condition \(s>2\) ensures convergence of the lattice sum; the proof does not require an upper bound on \(s\).

**Fresh main finite arithmetic.** The pinned source functions were imported directly with isolated Python and bytecode writing disabled, using the existing `reproducibility/checker-venv`. `numeric_balls.initialize_numerics()`, `build()`, and `check_signs()` were run in memory. This avoids all report-output writes to the read-only upstream checkout. Source hashes were independently verified separately rather than treating a manifest as formula authentication. The source-code formulas and matrix/sign-row operations were checked against the displayed recipes above.

- `verification/numeric_balls.py` SHA-256: `d5725fe0b1946e3213ae4bdfdb8e3abc99102d1564677665dd0d9e89bdcfab01`.
- Python-Flint 0.9.0; Arb precision 256 bits; exit code 0; all source assertions passed.
- All 37,310 Bernstein comparisons and ten tail comparisons were recomputed. Every power-table and column-norm comparison also passed.
- The recorded smallest Bernstein comparison was `[0.0012061126419378479840360722746555951 +/- 3.42e-38]`, at function 2, center 15, half-length .5, Bernstein index 40, parameter box [2.36,2.65]. It remains strictly above the .001 allowance.
- The recomputed \(\|D^{64}\|\) enclosure was `[0.0029563854014751250039579606457834812 +/- 2.71e-38]`; the final inverse-series norm enclosures were approximately 32.10141091408572 and 1.84377550484345. Their sum is below 36.
- Diagnostic floating-point comparisons in the checker only select reported minima; the actual inequalities are checked by strict Arb inclusion first.

`arithmetic_bounds.run_certificate()` was separately replayed in memory at 512-bit Arb precision with assertions enabled. All scalar assertions passed; the result contained 107 numeric fields and the final success-status field. Its source SHA-256 was `d6dd618f5d67f16a96c385d78f6362c6af81cd5e2b8bec003b91029f356c91e5`. Representative outward values were

\[
\begin{aligned}
\text{Cauchy quadrature majorant}&\approx1.01518\cdot10^{-32}<10^{-31},\\
U_{168}(1,0)&\approx1.066934\cdot10^{-14}<1.1\cdot10^{-14},\\
U_{168}(5,.02)&\approx8.157418\cdot10^{-14}<8.3\cdot10^{-14}-10^{-170},\\
U_{91}(5,.02)&\approx2.271066\cdot10^{-7}<2.4\cdot10^{-7},\\
\text{total exact-list correction majorant}&\approx1.368009\cdot10^{-8}<2\cdot10^{-8},\\
\text{tail second-derivative majorant}&\approx8.548407\cdot10^{-5}<.0002.
\end{aligned}
\]

These are evaluations of the analytically derived majorants, not sampled auxiliary functions. The alternate floor-rounded full-matrix procedure is conditional and was not executed; it is not needed because the exact-quadrature Arb route was independently completed.

**Atomic companion: separate adversarial audit.** A separate reviewer directly read the actual pinned file `preprints/An-atomic-certificate-for-triangular-lattice-universal-optimality-September-26-2026/build/main.tex`, scrutinized the full analytic chain, and independently ran `python3 -I -B verification/check_certificate.py`. It completed with exit code 0, no output, and no writes. A further independent child inspected continuum sign propagation. Neither found a mathematical defect. The principal source evidence is:

- Lines 828–980 establish node-independent spectral variation and convergence in every Schwartz seminorm for the full \(\ell^1\) tail. No unproved coefficient-moment condition is needed.
- Lines 1457–1535 prove the full frequency-envelope and geometric-tail bounds, including own-side repetitions of periodic columns.
- Lines 1544–1672 solve the exact Banach-space split system by Schur/Neumann inversion. The contraction uses \(\delta+340\beta N_\varepsilon<1\), with \(\delta=3\cdot10^{-8}\), \(\beta=3\cdot10^{-10}\), \(N_+=17\), and \(N_-=5\). Both finite and tail correction allowances are justified.
- Lines 1696–1717 subtract exact jets before estimating remainders. Lines 1777–1906 derive the full-tail curvature and Taylor allowances. Lines 1985–2030 give the exceptional first-node right-half-cell cubic argument over the full parameter range. Lines 2040–2134 establish the log-concave sine barrier and far signs, including junctions, nearest-node ties, and all later gaps. Lines 2139–2155 correctly normalize the Gaussian minorant.
- Lines 354–399 and 409–492 establish reciprocal Gaussian parameters, Poisson normalization, and density-only Fourier comparison. Lines 599–629 use positive-mixture/Fatou transfer along arbitrary radius sequences. These give precisely the ordered centered-disk Riesz bound required by the candidate.

The atomic source uses a different damping parameter and a different interpolation set, omitting the artificial node 24. These differences do not alter its energy theorem and create no normalization mismatch with the candidate. The two auxiliary-function constructions are not assumed identical or treated as each other's premise.

**Strongest verified result and remaining scope.** Both independently audited analytic chains, together with freshly recomputed finite arithmetic, establish the exact external theorem needed by the candidate's finite-square lower bound. No mathematical gap requiring a candidate revision was identified in that input. This is a source-level adversarial analytic review and reproducible arithmetic verification. It is not a formal kernel verification, priority determination, or validation of the unused long-range field-energy claims. No outreach was prepared or initiated.
