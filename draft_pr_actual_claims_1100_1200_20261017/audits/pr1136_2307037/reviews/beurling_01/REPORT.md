# Independent Beurling and localization audit of PR 1136

## Verdict and scope

**PASS for the analytic Beurling/localization route. No blocking mathematical defect found.** The exact constant in the frozen proof is valid. The deduction below is universal in the pole positions, finite positive weights, and every real radius R>1; finite controls are supplementary.

This shard freshly verified the Eremenko-Hamilton input against all five pages of the primary paper, including rendered equations. It did not independently revalidate the separate Levine-Peres construction theorem. Consequently, the complete deduction is stated with that theorem's precise output as an imported hypothesis; acceptance of that construction is a separate dependency, not a conclusion of the present numerical controls. Once that output is supplied, there is no remaining gap in the analytic deduction reviewed here.

The frozen proof is `inputs/PROOF.md`, 9,263 bytes, SHA-256 `32e68249400aad782b77c74405890f9929fc8576ab8a13d59a3b8db75dea9bdc`. All twelve input files were checked byte-for-byte by digest against source commit `cbbe7826cca914588018c840ba99c6b7a59fa7f5`; see `SOURCEHEAD_VERIFICATION.json`. Current main HEAD is distinct from the source PR head, as recorded in `INPUT_PINS.json`.

### Independence disclosure

The proof was read first, followed by fresh primary-source inspection. The main analytic audit, endpoint analysis, direct finiteness observation, and optimized split derivation were obtained before any prior audit was exposed. Subsequently, an attempt to inspect path provenance printed `PR_FILES.json`, which contains embedded patches of the prior audit and other author files. The returned output exposed the prior audit introduction and assorted later metadata. This was promptly disclosed to the parent. The reviewer did not intentionally read `inputs/AUDIT.md` or any other review and did not use the exposed material as evidence, but this late exposure means strict end-to-end isolation from the previous audit is not claimed. No further prior-audit reading occurred.

## Exact claim and success criteria

Let

\[
g(z)=\sum_{j=1}^n\lambda_j(z-z_j)^{-2},\quad
\lambda_j>0,\quad\sum_j\lambda_j=1,
\]

with arbitrary finite complex pole locations, including repetitions. The claim is that one compact S, independent of R and of exact unnormalized area pi, satisfies

\[
I(R):=\int_{D_R\setminus S}|g|\,dA
\le 2\pi\log R+\pi(\log2+1/e)\qquad(R>1).
\]

This is an ordinary nonnegative Lebesgue integral. The test of success includes poles arbitrarily far from the origin, overlapping initial disks, disconnected quadrature sets, all components of the complement, the two clipping-area endpoints, and the uncountable quantifier over real R. No additive-constant optimality, historical priority, formal proof-assistant verification, or external human peer review is asserted.

## Fresh primary-source verification

Source: A. Eremenko and D. H. Hamilton, *On the area distortion by quasiconformal mappings*, Proc. Amer. Math. Soc. 123 (1995), 2793-2797, [author PDF](https://www.math.purdue.edu/~eremenko/dvi/hamilt.pdf), [DOI](https://doi.org/10.1090/S0002-9939-1995-1283548-8).

The fresh PDF is 127,015 bytes, SHA-256 `f6723abba8783a7b2294ce6e2b5b6de5672cf52cb2804f20d447e7fdcc0f8f83`. All five pages were read in extracted text and rendered form because extraction drops equations. Printed page 2793 permits a compact ambient set Delta of transfinite diameter one, in particular the closed unit disk. This is the conventional logarithmic-capacity normalization. It restricts ambient geometry; area pi for Omega alone would not provide it. Printed page 2794 defines

\[
Tf(\zeta)=-\frac1\pi\operatorname{pv}\int
\frac{f(w)}{(w-\zeta)^2}\,dA(w)
\]

and states, for measurable E contained in Delta,

\[
\int_{\Delta\setminus E}|T1_E|\,dA
\le |E|\log\frac\pi{|E|}. \tag{EH}
\]

There is no additive term. Pages 2796-2797 derive the corresponding bounded-test-function inequality by infinitesimal quasiconformal deformation and duality. E is not required to be compact. The endpoint |E|=0 is interpreted by continuity. The ambient compactness hypothesis is distinct from measurability of E. Private source files and renders are ignored; public retrieval metadata are in `SOURCE_RECEIPT.json`.

### Measurability and the transform realization

For bounded E, its indicator belongs to L2. The Beurling transform is therefore a defined L2 equivalence class, with the usual principal-value realization almost everywhere. On an open set separated from the closure of E, that realization equals the absolutely convergent kernel integral almost everywhere. Changing representatives on a null set cannot change the nonnegative integrals in (EH).

There is also a robust fallback if one elects to use (EH) only for compact E. Choose increasing compact K_m contained in measurable E, with |E minus K_m| tending to zero. Then T1_{K_m} tends to T1_E in L2, so some subsequence converges almost everywhere. On Delta minus E, Fatou gives

\[
\int_{\Delta\setminus E}|T1_E|
\le\liminf_m\int_{\Delta\setminus K_m}|T1_{K_m}|
\le\lim_m |K_m|\log(\pi/|K_m|).
\]

Continuity of a log(pi/a), including a=0 and a=pi, gives (EH) for every measurable E. This argument neither assumes ordinary absolute convergence of the kernel at all points of Delta minus E nor needs it. Applying the source result to the closed unit disk and discarding its null boundary gives the open-disk version used in the proof.

## Universal analytic deduction

### 1. Precise construction output required

Combine repeated poles, adding their positive weights. The separate quadrature construction must provide a bounded open set Omega with all of the following properties:

1. Each open disk B_j centered at z_j with radius sqrt(lambda_j) is contained in Omega.
2. The area of Omega is pi and its boundary has area zero.
3. For every real integrable harmonic h on Omega,

\[
\int_\Omega h\,dA=\pi\sum_j\lambda_j h(z_j).
\]

Set S equal to the closure of Omega. Boundedness makes S compact; the null-boundary property gives |S|=pi exactly. This construction takes place before R is chosen. Connectedness, simple connectedness, disk containment about the origin, and pole separation are absent from the required output.

Fix any z outside S. Its distance to S is positive. The function w maps to (w-z)^(-2) is holomorphic on a neighborhood of S and is bounded on Omega. Its real and imaginary parts are integrable harmonic functions there, so the quadrature identity gives

\[
\int_\Omega\frac{dA(w)}{(w-z)^2}
=\pi\sum_j\frac{\lambda_j}{(z_j-z)^2}
=\pi g(z).
\]

Thus

\[
T1_\Omega(z)=-g(z)\quad(z\notin S). \tag{A}
\]

Both the minus sign and the factor pi are accounted for. Squaring removes the sign in z_j minus z. This is a direct pointwise quadrature application in every component of the complement; it is not analytic continuation from the unbounded component. In particular, a point in a bounded hole is equally separated from S, and the same harmonic test is permitted.

There is a useful independent finiteness check. Since S contains B_j, every z outside S satisfies |z-z_j| at least sqrt(lambda_j), whence

\[
|g(z)|\le\sum_j\lambda_j/|z-z_j|^2\le n.
\]

Therefore I(R) is an ordinary finite integral for every finite R even before any sharp estimate is used. The kernel integrals for Omega and its subsets are also absolutely convergent at each such z. This observation does not substitute for the uniform logarithmic bound, but excludes a hidden principal-value interpretation of g.

### 2. Scaling of the source estimate

For L>0 and measurable E contained in D_L, let a=|E|. Substituting z=L zeta and w=L eta gives

\[
T1_E(L\zeta)=T1_{E/L}(\zeta).
\]

The area factor L^2 in the kernel integral cancels its denominator factor L^2. Applying (EH) at unit scale and then changing variables in the outer integral yields

\[
\int_{D_L\setminus E}|T1_E|\,dA
\le a\log\frac{\pi L^2}{a}. \tag{B}
\]

The outer integral contributes the remaining L^2, while |E/L|=a/L^2. A spurious L^2 or L^(-2) factor in the transformed field would be wrong. Formula (B) holds with value zero at a=0.

### 3. Localization and the remote part

Fix an arbitrary real R>1 and set L=sqrt(2)R, E=Omega intersect D_L, F=Omega minus D_L, and a=|E|. Then 0<=a<=pi and |F|=pi-a. The two sets are a disjoint measurable partition, including the circle of radius L in F. On D_R minus S, (A), linearity of the absolutely convergent integrals, and the triangle inequality imply

\[
I(R)\le\int_{D_R\setminus S}|T1_E|
+\int_{D_R\setminus S}|T1_F|. \tag{C}
\]

Because D_R minus S is contained in D_L minus E, (B) bounds the first term by a log(2 pi R^2/a). The source estimate is used as an almost-everywhere singular-integral inequality on the larger region; no absolute-convergence claim is made throughout that larger region.

For the second term, fix w with rho=|w|>R. The elementary Poisson-kernel identity, or its absolutely convergent Fourier series for r/rho<1, gives

\[
\int_0^{2\pi}\frac{d\theta}{\rho^2+r^2-2\rho r\cos\theta}
=\frac{2\pi}{\rho^2-r^2}.
\]

Consequently

\[
\int_{D_R}\frac{dA(z)}{|z-w|^2}
=2\pi\int_0^R\frac{r\,dr}{\rho^2-r^2}
=\pi\log\frac{\rho^2}{\rho^2-R^2}. \tag{D}
\]

The final expression decreases with rho. For w in F one has rho>=L>R, so it is at most pi log2. The kernel is nonnegative and measurable. Tonelli therefore applies before finiteness is known; the calculation proves finiteness:

\[
\begin{split}
\int_{D_R\setminus S}|T1_F|\,dA
&\le\frac1\pi\int_F\int_{D_R}|z-w|^{-2}\,dA(z)\,dA(w)\\
&\le(\pi-a)\log2. \tag{E}
\end{split}
\]

The factor 1/pi cancels the pi in (D). The separation L-R>0 additionally gives ordinary absolute convergence of T1_F everywhere on D_R. There is no assumption that the pole locations, or Omega, lie in D_L.

### 4. Scalar bound, endpoints, and all real radii

Combining (B)-(E),

\[
\begin{split}
I(R)&\le a\log\frac{2\pi R^2}{a}+(\pi-a)\log2\\
&=2a\log R+\pi\log2+a\log(\pi/a)\\
&\le2\pi\log R+\pi\log2+\pi/e.
\end{split}
\]

The last step uses a<=pi and log R>0, followed by the elementary maximum of -x log x at x=1/e on [0,1]. At a=0 the first term is zero by continuity and the remote bound remains pi log2. At a=pi the remote term is zero and the near estimate is pi log(2R^2). These endpoints require neither division by zero nor an assertion that the remote field vanishes when a=0.

R was an arbitrary real number, and S was fixed before this argument. Only the measurable partition E,F changes with R. A separate inequality for each R does not require taking an uncountable union of almost-everywhere exceptional sets. Thus the same S works simultaneously for every real R>1, including R arbitrarily near 1 and arbitrarily large R. This completes the claimed universal deduction from the stated construction output and (EH).

## Distinct adversarial routes and sharper cross-check

### Exact distant-pole counterexample to dropping localization

Take g(z)=(z-A)^(-2) with A=5/2 and S the closed unit disk about A. At R=1, S lies outside D_{sqrt(2)}, so E is empty. Nevertheless, by (D),

\[
\int_{D_1}|g(z)|\,dA(z)
=\pi\log\frac{25}{21}>0.
\]

This also persists for real R>1 sufficiently close to 1. It falsifies the tempting alternatives of applying the near estimate to all of Omega without its containment hypothesis, or discarding the far field when a=0. The manuscript explicitly retains this field. This test uses an exact rational function and an elementary area integral rather than the quadrature-domain existence theory.

### Optimizing the split gives a stronger bound

To independently challenge the additive constant, repeat the localization with L=sqrt(t)R for any t>1. Write x=a/pi and q=R^2. The same argument gives

\[
I(R)/\pi\le\log\frac{t}{t-1}
+x\log\frac{q(t-1)}x. \tag{F}
\]

Let u=t-1 with 0<u<e. Since q>1 and x<=1,

\[
I(R)/\pi-\log q
\le\log(1+1/u)+x\log(u/x)
\le\log(1+1/u)+u/e.
\]

The last maximum is attained at x=u/e. Differentiating the right side in u gives 1/e minus 1/[u(u+1)]. Choosing

\[
u_*=(\sqrt{1+4e}-1)/2
\]

therefore supplies the verified, stronger constant

\[
C_*=\pi\{\log(1+1/u_*)+u_*/e\},\qquad
C_*/\pi\simeq1.0474673309
<\log2+1/e\simeq1.0610266217.
\]

The construction of S is unchanged, and the argument is analytic for all R. This sharper cross-check supports the original constant and confirms that additive-constant sharpness must not be inferred from it. No historical novelty claim is made for this elementary optimization, and no manuscript or PR has been modified.

### Route that loses the central difficulty

A direct triangle estimate on the original point-pole sum after deleting the individual disks introduces terms proportional to sum_j lambda_j log(1/lambda_j), as seen from integrating each inverse square down to radius sqrt(lambda_j). This entropy can grow like log n. Controlling it uniformly by merely asserting cancellation would transfer the central problem to an unsupported claim. That route is blocked as a proof of the universal n-independent constant; it does not supply a counterexample to the actual field, whose complex summands may cancel. No attempt was made to promote this route using finite samples.

## Leading-coefficient boundary test

For g(z)=z^(-2), let S be any measurable set of area pi and A=D_R minus D_1. On D_1 the density |z|^(-2) is at least 1; on A it is at most 1. Also,

\[
|S\cap A|\le\pi-|S\cap D_1|=|D_1\setminus S|.
\]

Thus the integral on D_1 minus S is at least the finite integral lost on S intersect A. Adding the annular integral gives I(R)>=2 pi log R. The reasoning remains valid with an infinite first integral because only a finite annular quantity is subtracted. Therefore no logarithmic coefficient smaller than 2 pi works with any finite additive constant as R tends to infinity. For this example the unit disk attains equality. This independently checks the correct growth scale of the localization result.

## Supplementary reproducibility and wrong-alternative guards

`verify_controls.py` is authored for this audit and has no external package dependency. Four direct nonsingular disk-kernel quadratures check translation, sign, normalization, and scaling; another direct disk-area quadrature checks the distant-pole formula. Scalar witnesses check the entropy endpoints, its interior maximum, and the optimized split equation. Seven explicit guards reject opposite sign, missing 1/pi, either spurious scale factor, discarded far field at a=0, dropped positive entropy, and a smaller proposed leading coefficient. The last guard is a finite witness only; the asymptotic proof above establishes sharpness.

The controls use explicit exceptions rather than Python assertions. Normal and -O runs both passed with byte-identical output while launched from `/`. Input lookup anchors at the checker's audit folder and strips the recorded audit prefix, preserving the original path strings and digests. A portable audit mirror containing the unchanged checker, pins, and twelve inputs also passed in normal and -O modes from `/`, with the identical output. `CONTROLS_RECEIPT.json` pins the program, interpreter, commands, output identity and guard inventory. Raw outputs remain under ignored `tmp/`. The controls do not prove the imported source theorems, exact area of an arbitrary quadrature set, or any universal quantifier. Those are addressed by the analytic reasoning and the separately scoped construction dependency.

## Remaining gap, handling, and release status

There is no remaining analytic gap in the Beurling/localization deduction under the exact construction output enumerated above. The independent verification of that output against Levine-Peres remains outside this shard's scope and must be supplied by the construction reviewer before an overall complete-proof acceptance is issued. The late prior-audit exposure is an audit-process limitation explicitly retained here.

All authored files are confined to `reviews/beurling_01/`. The ignore rules were written before any third-party retrieval. Third-party bodies, extracted text, rendered images, and raw control outputs are only in ignored directories. This shard changed no input file, Git index, branch or reference, PR, paper, tracker, or publication status, and contacted no human or other shard. It reported only to the root agent. The final pin and artifact inventories are in `END_PINS.json` and `ARTIFACT_RECEIPT.json`.
