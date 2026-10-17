# EH1995 correction-dependence check

## Verdict

**The reported 2002 correction does not affect the exact Beurling indicator inequality imported by PR 1136 or its localization proof. No mathematical revision of the accepted analytic route is required on this ground.**

The indicator estimate follows from EH1995 Theorem 1(i), the case where the deformation is conformal on E. The correction concerns its combined general-distortion statement 1(iii) and the scope of a sharpness remark. The publisher preview retains the conformal-on-E theorem with the same constant. This check independently reproduces the relevant infinitesimal argument below.

The audited sourcehead remains `cbbe7826cca914588018c840ba99c6b7a59fa7f5`. The frozen `PROOF.md` has SHA-256 `32e68249400aad782b77c74405890f9929fc8576ab8a13d59a3b8db75dea9bdc`. The earlier `beurling_01` audit remains sealed: its ten public files, exact inventory, and external receipt hash were verified unchanged. This new check resides in the sibling `eh_correction_01` folder and has a separate inventory.

## Primary evidence and access limits

The 2002 [publisher chapter preview](https://www.sciencedirect.com/science/article/abs/pii/S1874570902800075), *Area Distortion of Quasiconformal Mappings*, [DOI](https://doi.org/10.1016/S1874-5709(02)80007-5), was available through fresh web search. It identifies the combined general bound as

\[
|f(E)|\le K^{1/K}\pi^{1-1/K}|E|^{1/K},
\]

and identifies the missing exponent in the earlier coefficient and the overbroad sharpness wording. Its Theorem 5 retains, under its normalized compact-ambient setup and the condition that f is conformal on E,

\[
|f(E)|\le\pi^{1-1/K}|E|^{1/K}.
\]

Theorem 6 retains the complementary K|E| bound. The preview limits the sharpness assertion to these two special cases.

Direct publisher access failed: web open returned an internal error, and curl received HTTP 403. No full chapter PDF was obtained; the indexed publisher preview exposes the relevant statements and correction paragraph but truncates proofs. A full chapter audit is not claimed. Its terminology for the compact ambient set was not independently identified with every capacity convention; the exact unit-disk convention needed here is fixed directly by EH1995.

The [EH1995 author PDF](https://www.math.purdue.edu/~eremenko/dvi/hamilt.pdf) was freshly retrieved again: 127,015 bytes, SHA-256 `f6723abba8783a7b2294ce6e2b5b6de5672cf52cb2804f20d447e7fdcc0f8f83`. Printed pages 2796-2797 were rendered and reread. The concluding indicator argument explicitly invokes part (i), following a separate paragraph about part (iii). Source identities and access outcomes are recorded in `SOURCE_PINS.json`; all third-party bodies and renders remain ignored.

## Exact dependency under examination

Let Delta be the closed unit disk, let E be measurable with area a, and use

\[
Tf(z)=-\frac1\pi\operatorname{pv}\int_\mathbb C
\frac{f(w)}{(w-z)^2}\,dA(w).
\]

The imported assertion is

\[
\int_{\Delta\setminus E}|T1_E|\,dA
\le a\log(\pi/a). \tag{1}
\]

The continuous endpoint value is zero at a=0. The localization argument subsequently uses only (1), its scaled disk version, elementary kernel integration, and the separate quadrature construction. It never imports the numerical coefficient in the general quasiconformal-distortion theorem or a claim that that coefficient is sharp.

The dependency chain is therefore

\[
\text{conformal-on-E area estimate (i)}
\Longrightarrow\text{infinitesimal bounded-test estimate}
\Longrightarrow\text{indicator estimate (1)}
\Longrightarrow\text{localization bound}.
\]

The combined general case (iii) is absent from this chain. Neither its validity nor its optimality is used to justify (1).

## Independent infinitesimal verification

Assume first 0<a<pi. Let mu be any measurable bounded function supported in Delta minus E, with norm at most one. For |lambda|<1, let f_lambda be the normalized quasiconformal solution with complex dilatation lambda mu. Write r=|lambda| and

\[
K_r=(1+r)/(1-r),\qquad
K_r^{-1}=(1-r)/(1+r)=1-2r+O(r^2).
\]

Because mu vanishes almost everywhere on E, f_lambda is conformal on E in exactly the sense required by part (i). The standard normalized Beltrami solution and the L2-boundedness of T give

\[
\partial f_\lambda
=1+\lambda T\mu+O_{L^2}(r^2).
\]

For completeness, the derivative perturbation satisfies the Neumann equation obtained from

\[
\bar\partial f_\lambda=\lambda\mu\,\partial f_\lambda.
\]

Multiplication by mu has L2 norm at most one, T has L2 norm one, and mu has finite-area support. The Neumann remainder after its linear term is therefore O(r^2) in L2 for fixed mu. On E, the antiholomorphic derivative vanishes, so the area formula and Cauchy-Schwarz give

\[
|f_\lambda(E)|
=a+2\operatorname{Re}\left(\lambda\int_E T\mu\,dA\right)+O(r^2). \tag{2}
\]

Apply the conformal-on-E estimate (i):

\[
\begin{split}
|f_\lambda(E)|
&\le\pi^{1-K_r^{-1}}a^{K_r^{-1}}\\
&=a\exp\{(1-K_r^{-1})\log(\pi/a)\}\\
&=a+2r\,a\log(\pi/a)+O(r^2). \tag{3}
\end{split}
\]

Let A=integral_E T mu. If A is nonzero, choose lambda=r times exp(-i arg A); if A is zero, the desired conclusion is immediate. Comparing (2) and (3), dividing by 2r and sending r to zero proves

\[
\left|\int_E T\mu\,dA\right|\le a\log(\pi/a). \tag{4}
\]

The mu norm may equal one because the actual dilatation is lambda mu with norm below one. Equivalently, one can first use strictly smaller norms and pass to a limit. No smoothness of E is needed. The normalized Beltrami and L2 facts are the standard analytic framework of this source argument; the correction changes none of them.

### Duality and the exact indicator norm

The Beurling kernel is even. Its associated bilinear pairing is symmetric:

\[
\int u\,Tv\,dA=\int v\,Tu\,dA
\]

for compactly supported L2 functions. This follows first for smooth test functions from the distributional even kernel and then by L2 continuity. The pairing here is bilinear; no assertion of Hermitian self-adjointness is required.

Apply this identity with u=1_E and v=mu. Since mu is supported in Delta minus E,

\[
\int_E T\mu\,dA
=\int_{\Delta\setminus E}\mu\,T1_E\,dA.
\]

The latter density is integrable: T1_E is L2 and Delta has finite area. Choose mu equal to the conjugate phase of T1_E on Delta minus E, and zero when the transform vanishes. Then the right side equals the left side of (1), so (4) proves (1) exactly.

At a=0, the indicator and its L2 transform are zero almost everywhere. At a=pi, Delta minus E is null, so the left side of (1) is zero. Lebesgue-measurable E is covered either directly by the L2 formulation or by approximation from compact subsets and Fatou, as already documented in the sealed analytic audit. These endpoint and measurability arguments use no general-distortion coefficient.

## Falsification guard: the general theorem would give a different first-order bound

The dependence on part (i) is numerically and algebraically material. Suppose one instead tried to deduce (1) by applying the combined general-distortion estimate. Both the original K coefficient and the corrected K^(1/K) coefficient have the same first-order logarithm at r=0:

\[
\log K_r=2r+O(r^3),\qquad
K_r^{-1}\log K_r=2r+O(r^2).
\]

Consequently, either combined estimate yields only the expansion

\[
|f_\lambda(E)|
\le a+2r\,a\{1+\log(\pi/a)\}+O(r^2),
\]

which would imply the weaker bounded-test estimate a times {1+log(pi/a)}. The extra a cannot be silently discarded. This independently rejects a wrong proof that differentiates (iii) and then claims the exact constant in (1). The actual source argument and the audited proof use the special conformal-on-E estimate, whose coefficient has no K factor, so the extra term never appears.

For K>=1, K^(1/K)<=K. Thus the stated correction strengthens the displayed combined bound; the original larger bound remains an upper bound if the stronger one holds. The refinement and corrected sharpness scope provide no counterexample to part (i) or to (1). No assertion of sharpness for the general combined coefficient is needed here.

## Consequences for this audit

The exact inequality (1), its disk scaling, and the claimed additive constant remain supported. The manuscript attributes its transform input to the displayed indicator inequality, rather than asserting the combined general bound or its sharpness. The sealed audit's only sharper-constant observation concerns its own elementary localization optimization and is unrelated to the corrected general quasiconformal coefficient.

There is no correction-dependent mathematical gap to repair. It is useful scholarly context to distinguish EH1995 (i) from the corrected combined statement when documenting dependencies. No paper, PR, publication, tracker, Git index, branch, or reference was edited, and no human or other shard was contacted. Only the root agent received internal progress reports.

No numerical program was used to establish this conclusion. The checkable artifacts are the exact first-order expansions, phase selection, and L2 duality derivation above. Metadata scripts only pinned file identities and the untouched sealed inventory. `END_PINS.json` and `MANIFEST.json` record the final state and authored-content inventory. `ARTIFACT_RECEIPT.json` additionally seals the manifest and every public member, with its own digest supplied externally.
