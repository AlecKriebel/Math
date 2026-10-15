# Independent audit of the atomic triangular-lattice certificate

Audit completed: 2026-10-06, America/Los_Angeles. This review began from the original atomic manuscript and checker, without consulting the saved follow-on triage. The assigned target was an unconditional density-one infinite-configuration triangular-lattice energy inequality sufficient for hypersingular Riesz energy for every real exponent greater than two.

## Scope, provenance, and verdict

Source repository: /Users/alec/Desktop/math, verified HEAD adc7f1241b42e322a6451854ab7e4b4c146bf78a. Read the repository README, atomic README, the entire atomic build/main.tex (2473 lines), the entire verification/check_certificate.py (389 lines), verification README, CERTIFICATE metadata, and lean/docs/090.md. The source clone was not edited or built. A git archive copy of the exact atomic directory was extracted to reproducibility/atomic under this effort; checks were run there. No shared Git index or branch was mutated and no external individual was contacted.

| Pinned file | SHA-256 |
| --- | --- |
| build/main.tex | bfa619a454d49596b65f310f0bfdce3ae3f5ed6545bd9058d0c6316843ded2a6 |
| verification/check_certificate.py | 5689152e970b652a8e40c3c120eda3b45320c8745968a5cb416fa9b9dbdc5385 |
| verification/CERTIFICATE.json | 76e1ad0b480f84dc00308c76498125426090918df1ecd1630b2ab1e6da28040d |

**Verdict:** no substantive mathematical or checker defect was found in this pinned atomic proof. The exact finite checker passed twice with assertions enabled. Separate rational calculations reproduced the Fourier-wave decay, infinite-system contraction, interpolation-error and far-range sign calculations. The spectral construction, full-space interpolation, propagation from finite Bernstein tables to global signs, and density-only energy transfer were independently scrutinized. On the evidence reviewed, the atomic proof is usable as the unconditional mathematical input for the follow-on Riesz reduction.

This is an adversarial mathematical audit plus exact finite computation, not conventional human refereeing or full formal verification. I did not build Lean, inspect all real Lean declarations, check current remote corrections, or conduct the follow-on priority audit; these need separate evidence. The Lean scope document alone is not evidence of formal verification, and no formal verification claim is made here. The source repository's README explicitly warns that some unformalized results could contain issues.

## Exact supplied dependency and Riesz specialization

The theorem at source lines 68–76 uses
\[
 b=\sqrt3/2,\qquad
 A=b^{-1/2}\{m(1,0)+n(1/2,b):m,n\in\mathbb Z\}.
\]
Its basis determinant is exactly one. The competitor is a locally finite **set** \(\mathcal C\subset\mathbb R^2\) satisfying precisely
\[
 N_R=\#(\mathcal C\cap B_R),\qquad N_R/(\pi R^2)\longrightarrow1,
\]
where \(B_R\) is the closed disk centered at the origin. No uniform translated-disk count, separation or periodicity is assumed. For every smooth nonnegative completely monotone \(g:(0,\infty)\to[0,\infty)\), it proves
\[
 \liminf_{R\to\infty}\frac1{N_R}
 \sum_{\substack{x,y\in\mathcal C\cap B_R\\x\ne y}}g(|x-y|^2)
 \ge \sum_{a\in A\setminus\{0\}}g(|a|^2).
\]
Pairs are ordered, both sides may be infinite, and the lattice's own disk-energy averages have a limit equal to that series. There is no assertion of uniqueness or microscopic crystallization.

For the assigned target, \(g(t)=t^{-s/2}\), \(s>2\), is smooth, nonnegative, and completely monotone because
\[
 (-1)^jg^{(j)}(t)
 =(s/2)(s/2+1)\cdots(s/2+j-1)t^{-s/2-j}>0\quad(j\ge1).
\]
The right side is exactly \(\zeta_A(s)=\sum_{a\ne0}|a|^{-s}\), with no one-half factor or covolume correction. It converges for \(s>2\): lattice disk counts are \(O(r^2)\), so dyadic shell contributions are \(O(2^{(2-s)k})\). The possible singularity at zero is harmless for any finite distinct-point sum. This theorem is not itself the finite-square bridge or manifold asymptotic; those are separate reductions.

## Gaussian construction and Fourier consistency

The crucial Gaussian theorem/energy input constructs a real radial Schwartz minorant \(f_\alpha\) for every \(\alpha>0\), with \(f_\alpha\le e^{-\pi\alpha|x|^2}\), nonnegative Fourier transform, Gaussian contact on every nonzero lattice point, and Fourier zeros on every nonzero dual point. The Fourier kernel is \(e^{-2\pi i x\cdot\xi}\).

For the determinant-one basis matrix \(M\), the identity \(M^{-\mathsf T}=JMJ^{-1}\), \(J\) a quarter turn, gives \(A^*=JA\). Thus the contact sets have exactly the same radii, and Poisson summation has covolume multiplier one. It yields
\[
 \widehat f_\alpha(0)-f_\alpha(0)
 =\sum_{a\ne0}e^{-\pi\alpha|a|^2}.
\]
The reciprocal construction \(f_\alpha=k_\alpha-\alpha^{-1}\widehat f_{1/\alpha}\) for \(\alpha<1\) has the correct dimension-two coefficient; contact and Fourier-zero conditions exchange correctly by radiality and \(A^*=JA\).

For \(\alpha\ge1\), the construction uses \(s=b|x|^2\), \(h=17/50\), \(H=27/50\), \(B=b^{-2}=4/3\), and \(\eta=1/5\). The displayed residue list
\[
 I=\{0,1,3,4,7,9,12,13,16,19,21,25,27,28,31\}
\]
contains every \(m^2+mn+n^2\) modulo 36; a separate finite enumeration confirmed it. The nodes are deliberately a superset of actual shells, and the argument does not identify every node with an actual lattice point.

The squared sine product \(P\) has precisely double zeros on these residue classes. Its periodic \(\csc^2\) and \(\cot\) columns are trigonometric polynomials because the apparent poles are removed by the zeros of \(P\). Their spectral formulas at source lines 785–823 follow by Laurent expansion at infinity in \(Y=e^{2i\kappa(s-n)}\). The zero-frequency atom is real and **not doubled**; positive nonzero atoms are doubled on folding. Both \(P(n)=0\) and \(P'(n)=0\) are used to justify zero-frequency reality.

The rational tail columns' continuous spectral measures follow from the two oriented integral identities at lines 845–851. The orientation has the correct signs at negative frequencies, the reflected density is conjugate symmetric, and no zero-frequency atom is missing. The integrated variation matrix \(W\) is uniform in the tail node: the node-dependent phase has modulus one. Thus an **unweighted** \(\ell^1\) coefficient list suffices; no unmentioned coefficient moments are needed.

For fixed positive damping \(k\), the waves \(e^{-\pi b(k-it)|x|^2}\) have uniformly bounded Schwartz seminorms on \(|t|\le5/6\). Integration against a finite measure and absolutely summable tails therefore converge in every Schwartz seminorm. This justifies derivatives, removable values, Fourier transforms, and summation. The complex Gaussian transform has the correct prefactor \(1/(b(k-it))\) and exponent \(-\pi|\xi|^2/(b(k-it))\). Conjugate-symmetric folding is compatible with the radial transform, and Fourier inversion gives \(\widehat F_1=F_2\) exactly.

Independent rational evaluation verified the four positive divided Fourier-wave exponents, before multiplication by \(\pi\):
\[
100079/455650,\quad8949/455650,\quad216419/554650,\quad105489/554650.
\]
This prevents a decay sign from being inferred solely from numerical evaluations.

## Reproduced finite checker and its exact scope

Ran Python with -I -B and assertions enabled in the pinned copied atomic directory twice. Both runs exited zero with empty stdout/stderr. The retained receipt is reproducibility/atomic/checker_execution_receipt.json. Its explicitly captured run started at 2026-10-06T21:13:35.338186-07:00 and finished at 2026-10-06T21:13:39.375630-07:00, using Python 3.14.6 on macOS 26.6.2 arm64. It includes input hashes and byte counts. CERTIFICATE.json is static metadata and was not treated as an execution record.

The checker uses scaled integer intervals with denominator \(10^{60}\) and rectangular complex intervals. Its certificate arithmetic contains no floating-point operations. Every interval implementation routine was inspected. Addition, endpoint multiplication, zero-excluding reciprocals, outward integer division, integer-square-root enclosure, and absolute values have sound containment properties. Setting algebraically known zeros and ones in Gauss–Jordan elimination is justified by exact elimination identities. Every pivot is enclosed and asserted to exclude zero. The Machin enclosure of \(\pi\) and its alternating-series tail are sound. Exponentiation divides by 1024, checks the modulus, encloses the degree-60 series with \(2/61!<10^{-60}\), then squares ten times. -I ignores potentially interfering environment variables, and no -O or -OO disables assertions.

The implementation agrees with the article's recipes: Laurent convolution orientation; \(Q_n,D_n\) folding factors; atomic masses; opposite-side jet signs; fixed column and target row order; \(I-R\) and \(I+R\) inverses; the affine parameter polytope; curvature, tail and Taylor formulas; power-to-Bernstein conversion; and exceptional cubic row shifts/padding. The exact row minimum on the polytope correctly uses its independent scalar coordinates and the three vertices of \(0\le a\le Zu\).

The checker verifies two 20-by-20 inverse and coefficient bounds; residue-node and midpoint estimates; finite and geometric envelope sums; a containing Gaussian-data polytope; endpoint expressions used for curvature/Taylor envelopes; and 659 Bernstein row minima over that entire polytope. No spatial sampling or parameter sampling substitutes for these interval and polytope inequalities.

It **does not** prove the existence of the infinite coefficient solution; justify all continuous frequency extrema, differentiation and summation; prove global signs from finite tables; prove the density-only energy transfer; or prove the follow-on manifold theorem. Those analytic arguments were reviewed separately. In particular a successful finite checker is not, alone, universal optimality or the Riesz constant.

## Full infinite interpolation audit

Direct jet coordinates are consistent: removing local damping gives \(Q_n(c_n,d_n+D_nc_n)\). Canceling an extra function \(Z\) requires \(Q_n^{-1}(-Z(n),D_nZ(n)-Z'(n))\), exactly the sign used in the Fourier map. The finite periodic columns have repeated poles at later nodes, and their stronger damping gives the tail contribution \(e^{-\pi\eta m}(c_n,d_n-\pi\eta c_n)\). The proof subtracts this **own-side** repetition map, including the fixed zero column. The sign remains unchanged when forming sum and difference systems. This potentially material issue was handled correctly.

The continuous-frequency jet envelope is analytic rather than sampled. The logarithmic derivative of \((1+|D_n|+d_b)\sqrt X\) is at most \(1/X\), and the exponential contributes \(-\pi kn\). For both \(k=h,H\) and \(n\ge1\),
\[
 (k^2+25/36)/B<3k<\pi kn.
\]
Thus the right frequency endpoint bounds every tail spectral interval. The initial tail period is the complete \(T\cap[25,61)\); geometric summation includes every tail node with no splice omission.

The operator bounds are \(\|\mathcal B\|<340\), \(\|\mathcal D\|<3\cdot10^{-8}\), and \(\|\mathcal C\|+\|\mathcal A\|<3\cdot10^{-10}\). Uniform absolute column sums define bounded operators on all of \(\ell^1\), with Tonelli justifying the absolute summations. Finite inverse norms 17 and 5 yield a Schur contraction
\[
 3\cdot10^{-8}+340(3\cdot10^{-10})N_\varepsilon<1.
\]
The Neumann inverse is on the full Banach space, not a finite truncation extrapolation. Targets and fixed-column effects are summable, so the solution imposes every desired node jet exactly. The route does not replace the central issue by an unsupported infinite inverse claim.

The correction estimates include omitted targets at nodes 9–21, all tail targets, finite repetitions and the transformed constant. Constants cancel in the plus system only; their difference coefficient is 0.012. Independent Fraction arithmetic reproduced individual tail errors below \(3\cdot10^{-9}\) and individual finite errors below \(10^{-5}\). These are obtained by averaging the plus/minus bounds, so each separate plus/minus finite bound need not be below the individual threshold. No lost factor of two was found.

## Global signs and limiting cases

The deleted-jet identity
\[
 U_m[\varphi](v)=\int_0^1(1-t)\varphi''(m+tv)\,dt
\]
works for negative and positive \(v\) and at zero by continuity. Exact jets are removed before bounding errors, preserving contact even at arbitrarily small displacements. Degree-twenty divided Taylor truncation begins at derivative order 23 with denominator \(23!\), and its next ratio is bounded by \(|y|d/24\); the checker matches these indices.

For tail curvature, the transformed factor's logarithmic derivative is at most \(3/(2X)-\pi hs\). The rational inequality \(3(h^2+25/36)/(2B)<3h<\pi h\) validates the right-frequency maximum for \(s\ge1\), while the other endpoint is correctly maximal at zero. Uniform measure variation justifies differentiation of the entire tail. The deleted-jet error bounds are 0.018 for the first left half-cell, 0.003 for the first right half-cell, and 0.00016 afterward.

The Gaussian divided-remainder lower bound follows from \(q(0)=q'(0)=0\) and \(q''(x)=x^2e^{-x}\ge0\) for \(q(x)=e^{-x}(6+4x+x^2)-6+2x\). For negative displacement, the exponential derivative is bounded below by its value at the node. The comparison at node 3 uses the correct monotonicity and \(r(Z,1/2)=836500/974643>0.8\).

The exceptional right half-cell at node 1 uses four cubic Bernstein coefficients in \(z/Z\). On a segment of the containing polytope, only its independent first coordinate \(z\) varies. The proof does **not** falsely treat the physical exponential coordinates as affine functions of \(z\). Multiplication by the positive Gaussian denominator gives exactly the stated coefficients. Its first coefficient has a factor \(v\) and may vanish at \(v=0\), but actual \(z>0\) gives positive weight to other coefficients there. The denominator is positive, and its maximum is below 3.5, so decreasing by the 0.003 error preserves the stated margins. The origin \(s=0\), the zero-displacement limit, half-cell endpoints and ties are included.

The quotient \(P(s)/(s-m)^2\) is log-concave on each half-gap. Removing the zero contributes a nonpositive logarithmic second derivative by \(|\sin x|\le|x|\), and all other factors contribute nonpositive derivatives. Concavity bounds the quotient **below** by its smaller endpoint; this is the correct direction. The finite residue/midpoint bounds give the global quadratic barrier 0.054 and intermediate barrier 3.

For \(s\in[14.5,23]\), chosen nearest nodes 16,19,21 keep the full joining segment within that interval. Above 23 all nearest nodes are at least 25 and the joining segment stays above 23. Removing the direct constant \(C_iP\) preserves positive-node jets; the transformed constant remains and is bounded separately. Independent rational checks reproduce
\[
 K=0.0140109<0.018,\qquad K=0.00008363<0.000324.
\]
The fixed terms \(\pm0.006P\) therefore dominate all remainder curvature including the infinite correction, on every later gap. At nodes the exact jets supply the inequality. Positive normalization \(Q_1ze^{1/z}\) gives precisely \(e^{-\pi\alpha|x|^2}\), contact, and nonnegative Fourier transform.

## Density-only energy transfer

The low-frequency cutoff equals one on the unit disk and is supported in a slightly larger disk. Fourier inversion gives \(N_R\), and its omitted frequency tail is bounded by \(N_R\int_{|u|>\varepsilon R}|\widehat\phi(u)|\,du=o(N_R)\), independent of all translated small-disk counts. Cauchy–Schwarz and Plancherel give the normalized lower limit \((1+d)^{-2}\), then \(d\downarrow0\) gives one with \(N_R\sim\pi R^2\). The sign in the Fourier inversion matches the exponential sum.

The diagonal-included Fourier identity is exact for the finite set. Nonnegative Fourier transform allows restriction near zero, and removal of exactly \(N_R f(0)\) gives \(\widehat f(0)-f(0)\). Target comparison is needed only off the diagonal, so singularities at zero do not enter.

The manuscript's Bernstein–Widder proof allows infinite total representing mass and preserves an atom at zero. Approximation measures are locally finite; compact masses are uniformly bounded by a finite Laplace transform; compact-test convergence extends to Laplace transforms by a uniform \(e^{-sT/2}\) tail bound. Its subsequence is selected independently of the transform parameter. Energy mixing uses nonnegative finite Gaussian sums, Fatou along **every** radius sequence, then Tonelli. The atom at zero has infinite lattice and configuration energies and is explicitly treated. There is no invalid exchange of a liminf or minimizing sequence with the Gaussian parameter.

Fixed lattice-displacement pair counts are asymptotic to full disk counts. Finite displacement truncation yields the series as a lower bound, while the full nonnegative per-site lattice sum bounds disk averages above when finite. This proves lattice attainment and the exact liminf convention without an unsupported boundary-energy interchange.

## Independent artifacts, remaining scope, and completion

The separate reproducibility/atomic/audit_checks.py uses Fraction arithmetic to reproduce the four Fourier decay endpoints, both continuous-frequency inequalities using only \(\pi>3\), residue set, Schur contractions/errors, and final sign margins. It independently reconstructs Laurent coefficients in double precision and makes 96 diagnostic comparisons of the spectral atomic formulas to direct sine-product columns at off-node radii and different centers. The maximal normalized absolute error was 5.106549150887985e-10. These numerical diagnostics do not establish global signs or the Riesz constant. Results are in audit_checks_result.json.

The strongest result verified here is that the pinned atomic theorem withstands this full source/checker audit and its exact finite certificate is reproduced. No exact unresolved gap was identified in the reviewed proof. Outside this audit, the finite-square lower bridge, lattice upper bound, corrected manifold universality hypotheses, priority/attribution audit and fully reviewed publication package still need their own checks. This report does not advertise those tasks as completed.

Assigned dependency-audit completion estimate: mathematical audit 100%; this audit's reproducibility/report package 100%. These percentages refer only to the assigned audit, not to resolution or publication of the overall surface-constant project.

