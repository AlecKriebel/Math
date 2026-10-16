# Independent adversarial whole-package review 02

Review date: 12 October 2026 local / 13 October 2026 UTC. Reviewed effort: PR #521, problem 30003571. Reviewer: independent AI adversarial agent package02. This is an internal AI review, not human peer review. Review completion: 100% of this bounded whole-package review.

**Verdict: no remaining actionable findings for the disclosed unrefereed theorem or corrected publication package.** The written proof supplies a counterexample for the probability-normalized defining flow on an O_E(2) weight. Fresh archive verification, strict inventory checks, original Git-blob provenance, the corrected PDF rebuild workflow, optimization refusal, and four-page visual inspection all pass. This verdict does **not** certify historical first priority. The unread 2025 Naumann habilitation remains a specific disclosed priority gap.

## Exact frozen objects reviewed

| Object | Bytes | SHA-256 |
|---|---:|---|
| Published `positivity_loss.pdf` | 72,986 | `d5c31033f40afaa8dbd1f8642d7c729dfd7a858553e1c1c0856520a10f23bedd` |
| Corrected `verification_package.zip` | 92,207 | `9f9ab38e36d4b631f5d14fc2a63325f3a8e4e9cc331f200a06f6bb8ee1bf6210` |
| Current `positivity_loss.tex` | 13,221 | `2f38b06e7243966af7afda844edc4b6672be38bb9c10759816c2cce2e4e75bfe` |
| Corrected `README.md` | 3,966 | `e969418475aba9670884b0d80606385f05a8a0fb5d709a88e22c5da1090c4237` |
| Current `PACKAGE_MANIFEST.json` | 6,258 | `89711e22adea5cc7aefde3157b0bc2998f9a3cbb37bc6cd54e1dc24b473a1b7d` |

Original PR head: `91385a9ba0d445a2fae4629cd60b70026584e24b`. The frozen original proof hash is `4deb64c3b249dcf26a87ccdd222bad837e61f107b5304ed0e3ad2c6f1e444b36`; its frozen manifest hash is `14e522b5bea40b8dc1c9a222d58048e4f667a4bc805df55dfb630d79b83a162c`.

`reviewed_publication_hashes.json` records every top-level publication file read at intake. All original authored files were compared with their actual blobs at the exact locally available Git head, not merely with a positive prior report or a newly generated manifest. All 14 match byte for byte. No branch was changed, and no candidate files, remote state, commits, or pushes were modified.

## Claim, assumptions, success criteria, and boundaries

The exact proposition is that a globally smooth, strictly positively curved metric on L = O_E(2), for E = O(1) direct-sum O(1) over P¹, can lose total-space positivity under Naumann's published defining equation (13), with both fiber measures normalized to probability. The example has X = P¹ × P¹ and L = O(2,2). It must give admissible root-metric initial data on O_E(1), genuinely follow the nonlinear equation, and exhibit negative curvature on an actual tangent vector at a finite time.

The proof meets those criteria: at (s,z) = (0,0), the horizontal Hessian is

`w(0,t) = 1/96 − (1 − exp(−2t))/24`,

and it is exactly −1/96 at t = log(2)/2. Vertical curvature stays positive. The underlying bundle already has Griffiths-positive metrics; the theorem concerns a universal preservation assertion for this chosen initial metric. It asserts neither the Griffiths conjecture nor flow construction as a new result, neither positivity loss for every initial metric nor a result for an unnormalized weight flow.

The principal imported theorem is smooth finite-time existence of the relative flow, including smooth dependence on the base. That theorem is mathematical analytic input, not an assertion established by a computer run. All subsequent symmetry, stationarity, differentiation, positivity and spectral steps were independently re-derived here.

## Global geometry and initial positivity

With the specified convention f_* O_E(1) = E and E = O(1) tensor C², the projectivization is the product and O_E(1) = O(1,1). Its square is O(2,2); the canonical relative-anticanonical identity includes the determinant inverse. The metric uses the standard two logarithmic O(2) weights plus smooth functions of p = |s|²/(1+|s|²) and x = |z|²/(1+|z|²). Those functions extend smoothly to both projective factors.

The base-inverted chart subtracts 2 log|s|², the fiber-inverted chart subtracts 2 log|z|², and the joint inversion subtracts both. The displayed weights have finite smooth formulas at every chart origin. Dividing all weights by two gives valid O(1,1) transitions and half the positive curvature, so the initial root metric is admissible. No restriction to metrics induced by a Hermitian metric on E is required by the original question.

I independently computed the complex Hessian through real-coordinate derivatives in all four charts. In product Fubini–Study unit frames the diagonal entries A, B and squared mixed entry Q are exactly those in equation (5). This calculation does not use grid sampling. The four chart origins give:

| Base pole | Fiber pole | A | B | Q | Determinant |
|---|---|---:|---:|---:|---:|
| finite | finite | 1/96 | 2 | 0 | 1/48 |
| finite | infinity | 25/96 | 2 | 0 | 25/48 |
| infinity | finite | 383/96 | 2 | 0 | 383/48 |
| infinity | infinity | 359/96 | 3/2 | 0 | 359/64 |

The full closed-square inequalities hold: A ≥ 1/96 + (167/48)p, B ≥ 3/2 and Q ≤ p/4. Each remainder in the manuscript has the claimed sign on 0 ≤ p,x ≤ 1. In particular the bracket in the Q remainder is nonnegative because 0 ≤ (1−p)x³(1−x) ≤ 1. The determinant comparison is valid because both lower diagonal bounds are positive; it gives AB−Q ≥ 1/64 + (159/32)p. Independently expanding the full remainder recovers `(A−A0)B + A0(B−B0) + (Q0−Q)`, so no unjustified replacement of factors enters this bound.

All edge cases are covered by the actual chart weights and the continuum bound. For a quantitative robustness check, A ≤ 4 and B ≤ 13/6 give trace ≤ 37/6; hence the smallest eigenvalue is at least 3/1184 in those unit frames. The argument therefore cannot fail through an untested limiting infinity direction or an initially vanishing eigenvalue.

## Actual nonlinear solution and exact second derivative

For Euclidean fiber area, the curvature probability density is g/(2π), where g = φ_zbarz. The anticanonical probability density is e^(−φ)/I. Their ratio gives

`φ_t = log g + φ + log I − log(2π)`.

Different fixed conventions alter only the last constant. The reaction coefficient for the O_E(2) weight is one. The integrand is a density expressed in compatible anticanonical and determinant frames, not a globally defined scalar integrated against an arbitrarily fixed background area form.

A change of determinant frame multiplies numerator and denominator by the same fiberwise constant and cancels. Adding an arbitrary base function b(s) gives I(φ+b) = exp(−b)I(φ), leaves g and both probability measures unchanged, and therefore leaves b as a stationary base contribution. Under fiber inversion, e^(−φ) gains |z|⁴ and Euclidean area loses |z|⁴, so the density is invariant. Under base inversion the metric transition and the integral contribution cancel in the scalar right-hand side. The flow is thus geometrically well-defined in the displayed frames.

Uniqueness is sufficient for the symmetry argument. For the difference v of two smooth solutions, the log-integral difference is bounded in modulus by the fiber sup norm of v. At a fiber maximum the difference of logarithmic positive Hessians is nonpositive. Applying this to v and −v gives the stated Dini bound D⁺||v|| ≤ 2||v||, then Grönwall. The metric difference is a global function, so local weight transitions do not obstruct this argument. Compactness permits global sup norms. The base circle action has a lift preserving the initial metric and the defining flow; its invariance forces φ_s = φ_bars = φ_sbarz = 0 on the entire central fiber.

That central fiber has weight 2 log(1+|z|²) + 2 − ε. Its probability measures coincide exactly, so its restriction is stationary by fiberwise uniqueness. Its metric g_F = 2/(1+|z|²)² stays positive. Because φ_s vanishes as a function of z along that fiber, g_s also vanishes there. Therefore the quadratic product term in the second derivative of log g is zero. The resulting term is exactly g_F^(-1) w_zbarz.

Differentiating the density twice gives `∂s∂bars exp(−φ) = (φ_s φ_bars − φ_sbars)exp(−φ)`. The first term vanishes on the central fiber, so I_s = 0 and I_sbars = −I times the probability mean of w. There is no omitted variance term. Smoothness on the compact fiber over each finite time interval justifies differentiation under the integral. The resulting equation

`w_t = Δ_F w + w − mean(w)`

is an exact jet equation for the actual nonlinear solution, independent of higher base jets. A separate Taylor-coefficient calculation in the new verifier checks the coefficients of log(g_F + u g_w) and log(I0 − u J) at u = 0. No approximate or infinitesimal solution is substituted for the nonlinear one.

The geodesic curvature equals w because its Schur-complement mixed term vanishes. At the target point ∂/∂s is consequently an actual horizontal tangent vector with strictly negative curvature.

## Analytic existence and parameter regularity

I independently read Naumann's published §§3.1–3.3, Theorems 3–5 and their relevant proofs, and visually inspected printed pp.1519–1521. Theorem 5 explicitly concerns the defining equation (13) on O_E(r), and states smoothness on X × [0,∞). Its proof identifies the flow fiberwise with the normalized relative-anticanonical flow after a local determinant trivialization. Theorem 4 already states the total-space finite-time smoothness and cites Berman's existence result. Berman Theorem 4.1 independently states finite-time smooth existence; its stronger convergence assumptions are separate.

Here P¹ fibers are compact Fano Kähler–Einstein manifolds, the projection is a smooth proper product submersion, and the initial vertical Hessian is strictly positive everywhere. Thus the hypotheses needed for the finite-time part apply. On every compact finite-time interval, smooth positive fiber metrics supply uniform parabolicity locally in the base. The nontrivial automorphisms of P¹ cause no gap in this finite-time argument. The source separately leaves horizontal regularity of the infinite-time limit unclear; the proof uses none of it. I have not re-proved the cited analytic existence theorem from first principles, and the package correctly says so.

## Exact evolution, signs, and boundary times

The central probability measure pushes forward to dx on [0,1]. The general smooth-function chain rule gives

`Δ_F F = [x(1−x)F'' + (1−2x)F']/2`.

This is the nonpositive Laplacian convention. The mean-zero modes P1 = 2x−1 and P2 = 6x²−6x+1 have eigenvalues −1 and −3. The decomposition x² = 1/3 + P1/2 + P2/6 gives the exact solution printed in equation (9). The constant mean is ε+δ/3. The first mode is stationary under Δ_F+1 and the second decays at exp(−2t), fixing both the sign and the time scale.

The difference of two jet solutions with identical data has initially zero mean; integrating the equation keeps that mean zero. Multiplication by exp(−t) then reduces their difference to the heat equation, proving uniqueness. This identifies the explicit formula with the nonlinear solution's jet.

At t = 0 the pole curvature is ε = 1/96. At t = log(4/3)/2 it is zero, and at t = log(2)/2 it is −1/96. The zero threshold concerns this pole, not a claim of the earliest loss anywhere on the total space. At the target time the whole central-fiber function is `(x²+x)/8 − 1/96`, giving an open negative cap, rather than an isolated numerical artifact. As t tends to infinity the pole expression tends to −1/32, but this algebraic limit is not used as a theorem about horizontal smooth convergence.

## Normalization calibration and scope

The positive product weight is stationary for the defining probability-normalized equation on every fiber. Its central horizontal coefficient is 2, its mixed term and fiber Laplacian of that coefficient vanish, and (log I)_sbars = −2. A literal same-weight, same-time reading of the source's displayed r c term with r = 2 gives residual 2 instead of 0. This independently proves the convention discrepancy without depending on the proposed counterexample or on a Laplacian sign. The manuscript appropriately derives from equation (13) and does not attribute an undocumented typo or intention to the source.

For ψ = φ/r and τ = t/r, one has φ_t = ψ_τ and g_φ = r g_ψ; the transformed equation has reaction coefficient r with the matching integral exp(−rψ) and a shifted constant. Thus the root/time statement is coherent. Both curvature scaling and time reparameterization are positive, preserving the fact of positivity loss while changing its numerical coefficient and time. Omitting the fixed numerator mass adds a uniform time-dependent constant. Omitting the evolving denominator is a different flow: its initial pole derivative here is ε instead of −δ/3. The package keeps these distinctions explicit.

## Original source question and priority distinctions

The [2017 Oberwolfach contribution](https://doi.org/10.4171/OWR/2017/39), printed pp.2440–2443, defines the flow before raising positivity preservation. At p.2441 it drops the earlier induced-metric restriction and allows a positive metric on O_E(1). At p.2443 it runs the r-th power of that metric and leaves total-space positivity open. The [published article](https://doi.org/10.4310/MRL.2021.v28.n5.a10), §3.3, explicitly poses the same preservation question for its evolving probability-normalized equation (13). The catalogue's narrower construction request was already fulfilled by those sources; the manuscript correctly targets the source's substantive remaining question. I do not infer a current catalogue status from an inaccessible catalogue page.

I independently read the relevant primary clauses establishing these priority boundaries:

* [Berman 2013](https://doi.org/10.2140/apde.2013.6.131), Corollary 4.9, proves preservation for the **nonnormalized** weight flow. Section 4 distinguishes probability-normalized from nonnormalized weights even though their fiber curvature flows agree. Remark 4.11 identifies negative normalized anticanonical Kähler–Einstein curvature for effectively parametrized Fano families. This prior fact prevents broad priority claims about normalized relative negativity. It does not itself identify the present gauge, finite time, initial metric or locally isotrivial projective-bundle example.
* [Wan 2018](https://arxiv.org/abs/1801.09886) uses `∂t log G = Δ_Ω log G`, with Ω including a horizontal base metric, and proves a preservation theorem on curves for that different flow. Its equation, not just its title, distinguishes it from the fiberwise logarithmic measure-ratio flow here.
* [Demailly's later manuscript](https://arxiv.org/abs/2002.02677) records uncertainty about positivity of Naumann's method. That is dated supporting context, not proof that the question is still open in 2026.
* [Cao–Guenancia–Păun](https://arxiv.org/abs/1908.08087), Theorem D and §3, give a relative Ricci-flat positivity failure from an elliptic K3 setting. It is prior related negativity, but has Calabi–Yau fibers and a different canonical-metric question.

I verified the recorded 76 sequentially numbered queries and the sizes/hashes of all 19 retrieved primary PDFs. This verifies the retained audit records and their source inventory; it is not a new exhaustive replication of all literature searching or all theorems in those 19 papers. The source audit states its own limited reading coverage and index/access limitations.

The [University of Bayreuth listing](https://www.maphin.uni-bayreuth.de/de/forschung/schriften/alle/index.html) was freshly opened independently and confirms Naumann's relevant habilitation dated 4 June 2025. Its full text was not obtained or read here. The manuscript, README, deposit description and archived source audit all disclose that precise gap. No absence of search hits is promoted to priority certification; no outside contact or outreach was prepared.

## Metadata, license, and disclosure

The title, mathematical description, rank-two bundle, line bundle, target time/value, four-page count and exact source question agree with the proof and archive. The deposit is consistently a publication/preprint, version 1.0, dated 12 October 2026. The local review and PDF creation date are that day even though UTC is 13 October. Alec Kriebel and the independent-researcher affiliation agree with the project instructions; the ORCID `0009-0001-9320-500X` agrees and has a valid checksum. README licensing and deposit `cc-by-4.0` agree with CC BY 4.0. The two named deposit files exist with the stated bytes and hashes; the three DOI relations agree with the primary source bibliographies. No DOI or remote-publication receipt is invented by this review.

The visible page-4 disclosure, README and deposit description consistently state extensive AI assistance, internal AI adversarial reviews, unrefereed status and absence of human peer review. They distinguish algebraic reproduction from analytic existence and mathematical validity from historical-first priority. The Griffiths-positive keyword is contextual, not a contradictory claim that the Griffiths conjecture is solved. The historical originals retain their earlier frozen wording and notation defect, while CORRECTIONS.md identifies the current manuscript and the fixed u/nu inconsistency. Preserving those bytes as provenance is appropriate.

## Archive inventory, execution, and corrected rebuild

The ZIP has one root and 40 distinct safe file entries, including MANIFEST.json. Its 39 listed payloads comprise 14 original files, 3 paper files, 5 flow-review files, 5 geometry-review files, 4 source-review files, 4 reproduction records, 2 root assessment/source-receipt files, and the wrapper plus requirements. All sizes and hashes match, and the outer manifest is byte-identical to the extracted manifest. The ZIP CRC test passes. No downloaded PDF, source-text extraction, source/record cache, credentials or private coordination file occurs in that inventory. The archived authored reports were checked for scope and disclosure; their prior positive verdicts were not used as mathematical evidence.

All three historical original manifests validate their actual preserved files. The exact Git-head comparison independently authenticates the original subtree. The manifest excludes itself, which is disclosed; the externally supplied ZIP/PDF hashes anchor that convention. The current `PACKAGE_BUILD.json`, `zenodo_check.json` and PDF QA record agree with the exact frozen artifacts. These local preflight records are not treated as evidence of a completed remote Zenodo publication.

I exercised both the supplied effort-local pinned environment and the literal README setup: fresh `python3 -m venv .venv`, pinned dependency installation, and `.venv/bin/python run_all.py`. Python 3.14.6, SymPy 1.14.0 and mpmath 1.3.0 were used. The wrapper reports 40 original identities, 43 original-audit identities, 57 geometry checks and 17 flow checks, then verifies 39 manifest payloads. Normal, repeat and post-rebuild runs all pass, and a full before/after hash inventory shows unchanged frozen extraction bytes. The two scripts that write beside themselves are correctly copied to temporary scratch before execution. The dependency/cache exceptions allow the documented environment setup. Python 3.9 compatibility was inspected at source level; only 3.14.6 was executed in this review.

Both `-O` and `PYTHONOPTIMIZE=1` runs fail before checks, which protects the assertion-based archived programs. Separate derived fixture extractions prove that added files, a removed file and a changed file are rejected. Fixtures were removed afterward; they never touched the candidate.

The corrected rebuild instructions were exercised from the extracted root, including the documented mkdir and `tectonic --outdir ../positivity-loss-rebuilt paper/positivity_loss.tex`. The output sibling is outside the verified extraction and still inside this review's isolated folder. Compilation succeeds. A subsequent wrapper run succeeds. The rebuilt PDF has four pages, text identical to the frozen PDF, and byte-identical 120-DPI PNG renders on **all four pages**. Its binary hash is `9cf31cd618568f7f382b9c5663d2ccdc145e06b33ce669628d4e87e1cb8489fa`; the creation timestamp differs, as the README permits. The original published PDF and ZIP hashes remain unchanged.

## Visual inspection

All four frozen PDF pages were independently rendered and viewed. Page 1 has readable title, author/ORCID/date, abstract, question and defining equation. Page 2 has the theorem, analytic input, charts and positivity certificates; page 3 continues the certificate, exact jet derivation and spectral solution; page 4 has normalization, scope, priority limitation, AI disclosure and references. I found no clipped text or mathematics, overlaps, unresolved references, missing glyphs, inaccessible equations or unreadable text. Page 2's final certificate is close to the footer but is fully visible and separated. The identical rebuilt renders independently confirm source/PDF consistency.

## Checkable artifacts and exact remaining gaps

`independent_verify.py` and `independent_results.json` supply 153 new combined exact algebra, source-inventory and provenance/custody checks, including real-coordinate Hessians in every chart and generic jet/Laplacian calculations. `execution_receipt.json`, `after_rebuild_receipt.json`, `operational_guard_receipt.json`, `visual_rebuild_check.json`, `zip_inventory.json`, `metadata_check.json` and `source_count_check.json` preserve the operational evidence. The research log includes timestamped completion estimates. Scratch extraction/environment and renders are local and ignored; full copyrighted source-text extractions used during reading were deleted.

There are **no actionable mathematical, source-scope, metadata, inventory or rebuild findings remaining** for the exact disclosed package. The proof still imports the cited finite-time analytic existence theorem; verification checks its applicability and the source statement, rather than reconstructing that theorem from first principles. Historical-first priority remains uncertified, specifically because the 2025 habilitation is unread and literature searching is bounded. Those are accurately disclosed limitations, not hidden proof gaps or a claim to have settled the wider conjecture. Any proposed future historical-first claim requires a materially additional priority investigation.
