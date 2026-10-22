# Fresh adversarial package audit, round 1 — PR #1108

Problem 30003439 / OWR-15219-008. Reviewed version 1.0.0 dated 2026-10-17.
Completed: 2026-10-17T17:32:17Z (authoritative UTC clock).
Assigned-scope completion estimate: 100%.

**Disposition: PASS for the exact theorem and frozen package inspected. No actionable mathematical or distribution defect found; no parent-package repair requested.** This is an adversarial AI review, not external human peer review or proof-assistant certification. The historical priority screen remains bounded. This audit does not establish novelty or worldwide priority.

## Frozen inputs and review order

The inspected parent directory is `draft_pr_actual_claims_1100_1200_20261017/audits/pr1108_30003439/publication/`. Initial and final hashes agree:

| Artifact | SHA-256 |
|---|---|
| `main.tex` | `03f685e09a10a140915acfcaa1e4fcda9197a9a8a6f8800f2a3330c9532a101b` |
| Five-page PDF | `ad9864c08642737e4459673749c1db6d2e3dafb521f323fb1071f157f8110eb0` |
| Source and verification ZIP | `d97ba7ed1057518e3bd499d88182c64767e912d589ed8574092c0ebc7a27c06e` |
| Portable upload ZIP | `0f52fdfc42cc83e4739ca5de9cabda5120565c3d48cbb4457a0da9ab7ce1bd76` |

I read the actual TeX and reconstructed its proof before reading the dedicated earlier mathematical audit reports. Initial discovery also exposed `input/SOURCE_METADATA.json` and the historical source-role summary `input/SOURCE_REVIEW.md`; this was not a fully blinded review. Those summaries were not used as mathematical evidence. The original primary problem and source definitions were then checked directly, and separately authored exact computations were completed before the dedicated mathematical reports were opened. No other shard was contacted. All writes stayed in `reviews/package_round1/`; no PR mutation, parent-package edit, commit, push, publication, or outreach occurred.

## Exact target and claim

The original p.799 question is existential: exhibit an algebraic convex cone carrying a negative-curvature normal barrier although it is not a hyperbolicity cone. Algebraic is defined there using homogeneous polynomial inequalities, and curvature is the third-derivative matrix sign. This is distinct from the broader existence question for every regular cone. Direct source: [Tunçel, OWR14/2017, contribution pp.797–800](https://ems.press/content/serial-article-files/46677?nt=1). Its physical PDF page29, printed799, was read as text; a new screenshot request timed out, so no new visual inspection of that source page is claimed.

The manuscript's claim is exactly

\[
K=\{x,y,z\ge0:xy^2\ge z^3\},\quad
F=-25\log\bigl(z(xy^2-z^3)\bigr),\quad \nu=100,
\]

with \(D^3F(a)[h,u,u]\le0\) for every interior base point, every \(h\in K\), and every real \(u\), and with no homogeneous polynomial of any degree defining \(K\) as a hyperbolicity cone in the original \(\mathbb R^3\). Neither a lifted representation, a signed cone, nor a dual barrier is substituted for this claim.

## Independent analytic reconstruction and falsification

**Geometry and complete barrier domain.** The displayed Hessian of \(m=x^{1/3}y^{2/3}\) is a negative scalar times \((y,-x)(y,-x)^T\). Its concavity extends continuously to the closed orthant. Its nonnegative hypograph is therefore convex. Orthant containment gives pointedness; closed homogeneous inequalities and the strict point \((2,1,1)\) give the other regularity properties. A boundary point with \(z>0\) must have \(p=0\); coordinates vanishing on the other boundary strata force \(z=0\) or \(p=0\). Along *every* interior sequence converging to a finite boundary point, continuity gives \(zp\to0^+\). Thus no face, axis, vertex, or approach path is omitted from blow-up. No claim about blow-up at infinity is needed.

**Self-concordance and normality.** Differentiating \(g=z^3/y^2\) independently gives the displayed first, second, and third line derivatives. With \(\delta=x-g\), the Hessian is \(w^2+v^2+2b^2+c^2\). Its null space is trivial. The cubic polarization has exactly the factors shown, including the \(1/3\) in the mixed \(\ell v^2\) term. The dual norm of \(c-4b\) under \(2b^2+c^2\) is exactly3. Triangle and Cauchy–Schwarz bounds give the four constants \(2,3,3,2\); hence the mixed bound10 holds globally. Scaling by25 yields standard constant2 because the local norm scales by5. The scalar condition is included by setting \(h=u\). Homogeneous degree4 gives \(\nu=100\), and \(Ha=-\nabla F\) gives the exact gradient bound100. The extended function is closed and convex by positive Hessian plus finite-boundary blow-up. These properties match the definitions in [Nesterov–Tunçel, pp.3–4 and §6](https://arxiv.org/pdf/1412.1857) and the mixed convention in [Dahl–Tunçel–Vandenberghe, §2.2](https://www.math.uwaterloo.ca/~ltuncel/publications/2509.10263.pdf).

**Fixed automorphism and all directions.** The normalization obeys \(\alpha\beta^2=\gamma^3\). Its logarithmic additive shift is constant when differentiating, because the base-dependent diagonal map is held fixed. The residual invariant \(r>1\) remains; transitivity is not assumed. If \(h_y>0\), the displayed ray decomposition has nonnegative coefficients by the defining cone inequality. If \(h_y=0\), that inequality forces \(h_z=0\). This covers the facet direction \(t=0\), every curved ray, all conic combinations, the \(e_x\) endpoint, and zero.

**Universal PSD certificate.** I independently recovered the matrix from a full trivariate Taylor expansion of the logarithms, not from the printed derivative tensor. Multiplication by \(-s^3\) clears denominators. Each matrix entry has degree at most3 in each of \(s,t\), so every determinant or identity residual tested has conservative bidegree at most \((9,9)\). Agreement on ten distinct rational nodes in each variable is therefore a complete polynomial interpolation certificate. This independently verifies all entries, the leading minor, determinant, both squares, and endpoint Gram matrix. It is not a probabilistic sample argument. The separate analytic sign argument remains necessary and valid: for \(0\le t<1\), all relevant terms are nonnegative and the constant terms are positive; at1 both residual polynomials equal \(6s^2\); above1 the square remainders are positive. The shift \(t=1+v\) makes the first remainder's positivity explicit. Sylvester's criterion is used only when \(t\ne1\). At1 the lower block has determinant \((r-1)(2r+7)>0\); at \(e_x\) the two-term Gram representation is PSD. No boundary base point \(s=0\) is needed.

**All-polynomial obstruction.** Boundary continuity of the real eigenvalue roots, with fixed nonzero leading coefficient, forces any proposed defining hyperbolic \(H\) to vanish on the curved boundary patch. Substitution and clearing denominators produce a polynomial identity on an open subset of \(\mathbb R^2\). The coefficient gcd of \(y^2x-z^3\) is1, so Gauss's lemma transfers its fraction-field divisibility to \(\mathbb R[x,y,z]\). This is an actual irreducibility/divisibility argument, not a claim that excluding one proposed defining polynomial suffices. Every proposed hyperbolicity direction lies in \(\operatorname{int}K\), so \(a>b>0\). The line factorization has quadratic discriminant \(-3a^2<0\); the restricted product is nonzero because \(H(e)>0\), and multiplication cannot cancel roots. Constants, repeated factors, arbitrarily high degrees, and different interior directions offer no exception.

**Adverse controls.** The independent expansion gives, on removing \(-\log z\),

\[
-s^3D^3(-\log p)[(8,1,2)]
=\begin{pmatrix}8&-8&0\\-8&96&72\\0&72&24\end{pmatrix}
\quad\text{at }(5,1,1).
\]

Its determinant is \(-24576\), and the independently chosen rational witness \(u=(-9/11,-9/11,1)\) has quadratic value \(-384/11\). Thus the facet logarithm is substantive. Extending the ray parameter to the forbidden value \(t=-1\) also fails: at \(r=2\), \(u=(5,1,2)\) gives value \(-2\) for the purported PSD matrix. Wrong sign and corrupted coefficients are detected. The singular directions are correctly PSD rather than positive definite.

## Exact software and archive audit

`audit_distribution.py` performs104 checks. It independently enforces the exact26-member source allowlist and5-member portable-kit inventory; checks duplicate/unsafe names and every CRC; verifies every member byte count and SHA-256 against the manifest and receipt; compares the source/working copies and distributed audit bindings; binds provenance to the frozen PR snapshot and input-proof hash; and checks repository-relative versus portable deposit paths and the three equal metadata copies. The source and portable archives also repack byte-identically with their fixed timestamps and attributes. No third-party source documents, hidden files, bytecode, or unexpected member was found.

Both verifiers were run from the *unpacked distributed source*. Geometry passes all791 checks, including8 adverse controls, normally and with `-O`. Curvature passes its displayed identities,45 rational parameter cases and315 logarithm-series contractions normally, and explicitly rejects `-O` at startup. Stable results exactly match distributed expectations. Four independent code mutations generated six executions: changes to two geometry diagonal coefficients each fail in normal and optimized modes; changes to a curvature off-diagonal coefficient and square remainder each fail normally. These mutations alter real distributed checker copies; they are not merely restatements of the original negative controls.

`independent_controls.py` adds1295 exact checks via a separately authored full Taylor-jet/interpolation mechanism, and passes identically under `-O`. It includes highly anisotropic bases, distance \(10^{-9}\) from the normalized curved boundary, the fixed-diagonal tensor law in all27 components, scalar and mixed normal forms, the parameter100 identity, and independent adverse witnesses. Finite general-base self-concordance tests supplement, rather than replace, the analytic global norm estimates.

## PDF rebuild and visual QA

The distributed `main.tex` compiles successfully with cached Tectonic0.16.9 in scoped scratch, with no network retrieval. Python3.14.6 runs the standard-library checks; bundled Python3.12.14/Pillow/pypdf perform image/metadata comparison; Poppler26.08.0 renders both PDFs. No overfull box, unresolved citation/reference, or compilation error appears in the log. Text extracted with layout is byte-identical, SHA-256 `071262e4c4357dd9f34da21efe0310638bf9b5d4af9711168977360f2cbebb65`.

All five pages were rendered at110dpi and individually inspected. The theorem, formulas, square certificates, references, author identity, date, page numbers and disclosures are legible, correctly placed, and free of clipping/overlap. The two five-page render sets are pixel-identical (935×1210 each). Rebuilt PDF SHA-256 is `674c0afbbc5c84e11392a3eed9d28984caba63167d876cbf7dc47426f737b364`; PDF byte equality is not required. The recorded creation timestamp differs, while author/title/producer metadata agree. Pixel and extracted-text equality establish the substantive rebuild match.

## Attribution and research-status boundaries

The exact cone is correctly credited to [Hildebrand, Theorem3.2 family5](https://arxiv.org/pdf/1305.4814) using exponents3 and3/2 and coordinate order \((x,z,y)\). The affine-sphere use of “hyperbolic” does not supply polynomial hyperbolicity. [Roy–Xiao Theorem2](https://optimization-online.org/wp-content/uploads/2018/01/6441.pdf) directly gives the printed parameter3 self-concordant barrier on this same nonnegative power cone; that credit and the explicit nonoptimality of100 are present.

The [DTV version record](https://arxiv.org/abs/2509.10263) says June12,2026, the inspected author PDF internally says June16, and the [v2 HTML](https://arxiv.org/html/2509.10263v2) says August24. This audit checked those representations independently; the manuscript records their difference correctly. Both relevant definition and broader final question are consistent with the scope distinction. The package carries bounded primary-source priority evidence and explicit access/coverage limitations. I did not conduct a fresh worldwide literature search and do not infer present openness or first-ever priority.

The actual PDF, README and metadata disclose extensive AI assistance and unrefereed status. They distinguish adversarial AI review from external human peer review and formal certification. The abstract's affirmative existential conclusion is supported by the proof; its contribution wording is not an exhaustive priority guarantee.

## Remaining gap and reproduction

No unresolved gap was found in the assigned theorem, self-contained analytic proof, stated attribution, verifier behavior, archive bindings, metadata or PDF integrity. Worldwide novelty/priority, inaccessible/unindexed literature, broader cones/exponents, and universal barrier existence remain outside this PASS. A later fresh package round is still required by the parent's successive-review workflow; this report does not approve publication by itself.

Run from the audit root:

```sh
python3 -B reviews/package_round1/audit_distribution.py
python3 -B reviews/package_round1/independent_controls.py
python3 -B -O reviews/package_round1/independent_controls.py
```

For the PDF reproduce the commands in `REPRODUCTION.md`; the image check requires the already available bundled Pillow/pypdf runtime. Machine-readable results are in `distribution_results.json`, `independent_results.json`, and `pdf_results.json`. Logs, raw verifier outputs, independently authored scripts, source-scope ledger, hashes, rebuilt PDF and page renders are preserved within this review directory. The copied58MiB Tectonic cache was temporary and removed after the successful rebuild.
