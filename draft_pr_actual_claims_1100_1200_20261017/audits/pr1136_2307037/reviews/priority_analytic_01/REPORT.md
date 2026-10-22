# Independent analytic priority audit: PR1136 / AMR-022-7037

## Verdict

**No pre-10-October-2026 primary statement covering the complete exact target was identified in this bounded analytic/quasiconformal/quadrature search. Historical prior-full status is NOT ESTABLISHED; historical novelty is UNRESOLVED.**

The affirmative theorem is a checkable consequence of established inputs available by May 2009. That fact does not establish that someone previously stated, proved, or recognized this exact consequence. The strongest verified overlap is the acknowledged pair of ingredients: Eremenko–Hamilton's sharp indicator-transform inequality (1995), and Levine–Peres's arbitrary positive finite-source quadrature construction (authenticated 2009 manuscript/arXiv v2; journal 2010). Neither source is an exact covering criterion for 7.37. The bridge below is a deduction, not a theorem found in their bodies. No evidence supporting first priority was found; none is claimed.

This review was independent of the other priority report, which I did not read. I read frozen PROOF.md, SOURCE_REVIEW.md, source metadata/hypotheses, and primary source bodies. No person was contacted; no outreach was prepared; no PR, paper, tracker, Zenodo record, Git index or ref was changed. Authored files are confined to this review folder. Copied bodies, raw API results, extractions and renders are private/ignored.

## Exact comparison standard

For every finite \(g(z)=\sum_j\lambda_j(z-z_j)^{-2}\), with arbitrary complex locations, positive real weights and \(\sum_j\lambda_j=1\), there must exist **one** measurable \(S(g)\) of area **exactly** \(\pi\), working for **all real** \(R>1\), with
\[
\int_{D_R\setminus S(g)}|g|\,dA\le2\pi\log R+C
\]
for an absolute\(C\). The submitted result strengthens measurable to compact and gives \(C=\pi(\log2+e^{-1})\). Repeated poles are allowed; integration is ordinary nonnegative area integration. No unit-disk support or separation hypothesis is allowed.

I visually reread [HL v2, PDF pp.172–173 / printed pp.171–172](https://arxiv.org/pdf/1809.07200v2). It separately records 7.36 as solved and reports no progress communicated to its editors on 7.37. The latter is not a global openness certificate. The [2019 final chapter](https://link.springer.com/chapter/10.1007/978-3-030-25165-9_7) was accessible only as a subscription preview; its full target text and final-edition differences were not inspected. Third-party search excerpts were not promoted to primary evidence.

## Primary-source findings

| Family / source | Inspected result | Exact gap |
|---|---|---|
| [EH1995](https://www.math.purdue.edu/~eremenko/dvi/hamilt.pdf), all 5 pages read; formula p.2794 visually checked | For \(E\subset D_1\), \(\int_{D_1\setminus E}\lvert T1_E\rvert\le\lvert E\rvert\log(\pi/\lvert E\rvert)\), with \(T=-\pi^{-1}\operatorname{pv}\int(\cdot)/(w-z)^2\). | Indicator input, not an atomic sum. No quadrature-set or all-radii pole conclusion. |
| [LP2009 author manuscript](https://lionellevine.github.io/scalinglimit.pdf), [arXivv2](https://arxiv.org/abs/0712.3378v2) | Definition(4), Props.2.12/6.6, Cor.2.13, Lemmas2.15/6.1 give the bounded finite-source smash sum, null boundary, additive area, harmonic quadrature. Relevant pp.6,12–17,54–55,58–59 read;16,17,58,59 visually checked. | Supplies the exterior-field representation, but states no Beurling logarithmic/Problem7.37 estimate. |
| [Sakai1982](https://link.springer.com/book/10.1007/BFb0095892), Sakai1983/1984, Gustafsson–Sakai1994 | Publisher metadata and LP ancestral references inspected. LP attributes Theorem 6.7 to Sakai1984/85, Theorem 7.5. | Original fullbodies unavailable; I do not date the complete bridge to1982/1983/1995 by indirect citation. |
| [Sjödin2007](https://www.sciencedirect.com/science/article/pii/S0362546X06002501) | Publisher abstract/introduction discusses positive-measure partial balayage and the structure formula. | Generic ingredient; fullbody not obtained. |
| [Fuchs–Macintyre1940 publisher record](https://doi.org/10.1112/jlms/s1-15.3.162); [Bergweiler2011v1](https://arxiv.org/abs/1101.3479v1), Lemma 2.2 | Original PDF blocked. Later author preprint pp.4–5 restate bounds for sums \(1/\lvert z-z_j\rvert\) outside disks with radius/squared-radius control; both pages read/rendered. | First-order pointwise control, not the sharp second-order area integral. It cannot be differentiated into the target. Exclusion of the entire1940 body is not certified. |
| [Osękowski radial logarithmic bounds](https://www.mimuw.edu.pl/~ados/publications/papers/log_BA_radial.pdf),pp.1–3 | Theorem 1.2 uses radial\(F\), a density \(L\log L\) functional, and a disk average; p.3 rendered. | Arbitrary configurations are nonradial; point masses have no finite area-density \(L\log L\) norm. No exact exceptional set. |
| [Osękowski multiplier \(L\log L\)](https://www.mimuw.edu.pl/~ados/publications/papers/LlogL_multipliers.pdf),pp.1–3 | Symbol class and Theorem 1.2 inspected; sharp applicability includes real/imaginary Beurling parts. | No target modulus estimate for arbitrary complex squared-pole fields, nor area-\(\pi\) set. |
| [Baernstein–Montgomery-Smith1997v1](https://arxiv.org/abs/math/9709215v1),pp.1–5; [Dragičević2021v1](https://arxiv.org/abs/2109.04555v1), selected pp.20–22,29–31,59–61 | EH citation context, operator norm/weak-type passages read; fulltext keyword screening used for triage. | No exact target in inspected passages. Whole papers/final editions not exhaustively read. Dragičević's file retains the mistaken retrieval basename volberg2021; authorship here is corrected. |

The EH 2002 follow-up publisher excerpt notes corrections to the general area-distortion combination in EH Theorem 1(iii). This is not the indicator inequality used here, which is derived from part(i). The complete 2002 chapter was not obtained; its excerpt is not used as a replacement proof.

An OpenAlex query returned 80 EH-citing records. All 80 titles were screened; the relevant operator/area-distortion leads above were pursued. This is title screening, not 80 fullbody readings or exhaustive citation coverage.

## Recent analytic overlap and cautious chronology

[Guerra, arXiv:2608.23388v1](https://arxiv.org/abs/2608.23388v1), submitted 24 August 2026, states the sharp real-input Beurling weak-type constant 2 in Corollary 1.2. The retrieved version's pp.1–3 and §6 corollary proofs were inspected; p.2 visually checked. Thus saying the general real-input weak constant is still unknown based on older papers would be incorrect. This audit does not independently referee Guerra's full Morse-theoretic proof.

A search also found Lin's [Two partial balayage principles for weak-type estimates](https://coolrmal.github.io/articles/two-partial-balayage-principles/). It combines partial balayage/locality with singular-transform estimates and gives Beurling weak constant 2, including complex inputs. Current and commit-addressed historical PDFs were retrieved. The public path-history query lists commit b9c28f7af5694bd44d0f19cb4f14b5f66225174e with author/committer metadata 2026-10-05T10:49:12Z; its PDF SHA256 matches the current PDF. These timestamps and bodies are metadata evidence, not proof of first publication, independent discovery, causal influence or priority. Current HTML and PDF differ in an unrelated maximal-square table entry and are not asserted identical.

Relevant Lin PDF pp.1–4 were read, p.4 visually checked, and all extracted text keyword-screened. Its input is \(L^1\cap L^2\); its conclusion is weak-type. No exact-area single exceptional set or all-\(R\) pole logarithm is stated in the inspected results. This is a concrete antecedent for the broad *balayage plus singular-transform* mechanism; that mechanism should not be presented as novel here.

Even granting an atomic-limit weak estimate
\[
|\{|g|>t\}|\le\pi W/t,
\]
the fixed superlevel set at height\(W\) has area at most\(\pi\) and can be enlarged. Layer cake gives only
\[
\int_{D_R\setminus S}|g|\le\int_0^W\min\{\pi R^2,\pi W/t\}\,dt
=\pi W(1+2\log R).
\]
Thus\(W=2\) yields coefficient\(4\pi\), not\(2\pi\). This rejects a direct weak-type substitution, not every possible deduction from Guerra/Lin.

## Complete independent bridge from authenticated older inputs

This verifies **older-input deducibility**, not a prior exact-answer publication.

For the positive masses, take disks of areas\(\pi\lambda_j\) and their LP smash sum\(\Omega\). The cited boundedness, boundary, mass and quadrature statements give
\[
|\Omega|=|\overline\Omega|=\pi,\quad z_j\in\Omega,\quad
\int_\Omega h\,dA=\pi\sum_j\lambda_jh(z_j)
\]
for integrable harmonic\(h\). The finite disk-indicator densities meet LP's density-gap and almost-everywhere continuity hypotheses; iteration is legitimate. For \(z\notin S:=\overline\Omega\), test with real/imaginary parts of\((w-z)^{-2}\) to obtain \(T1_\Omega(z)=-g(z)\). The kernel is bounded on the compact support for every such\(z\), so this holds on every complementary component. Fix\(S\) now.

For any\(R>1\), put \(E=\Omega\cap D_{\sqrt2R}\), \(F=\Omega\setminus D_{\sqrt2R}\), \(a=|E|\). Scaled EH bounds the\(E\) contribution on\(D_R\setminus S\) by \(a\log(2\pi R^2/a)\). For \(w\in F\), direct polar integration gives
\[
\pi^{-1}\int_{D_R}|z-w|^{-2}\,dA(z)
=\log\frac{|w|^2}{|w|^2-R^2}\le\log2.
\]
Tonelli and the triangle inequality bound the\(F\) contribution by\((\pi-a)\log2\). Consequently
\[
\int_{D_R\setminus S}|g|
\le2a\log R+\pi\log2+a\log(\pi/a)
\le2\pi\log R+\pi\log2+\pi/e.
\]
Use the continuous value at\(a=0\), \(a\le\pi\), \(R>1\), and \(\max_{[0,1]}t\log(1/t)=1/e\).

All exact quantifiers survive: only auxiliary\(E,F\) depend on\(R\); exceptional\(S\) is fixed. Remote poles require the distant-piece estimate. Merely applying EH in a disk containing all poles would introduce a configuration-dependent radius and would not supply an absolute constant.

The verified older source version is available by2May 2009. Sakai's ancestry is older, but original-body gaps prevent dating this complete authenticated route earlier here. Neither inspected source states this bridge; it remains a target-specific application of generic established theorems.

## Adversarial checks and exact remaining gap

Single/repeated/nearby poles, arbitrary translations, disconnected smash sums, bounded complementary components, \(R\downarrow1\), and \(a=0\) are consistent with this argument. Null boundary supplies exact compact area; area-at-most\(\pi\) is not silently substituted. No differentiation of first-order or endpoint estimates occurs. Positivity and normalization are used in the quadrature construction; no signed/complex-weight extension is asserted.

The exact unresolved historical question is whether this quadrature/indicator/localization combination was previously stated or recognized elsewhere. No old exact-answer primary source was found. No new quadrature existence or new sharp Beurling theorem is established here.

Material limits: original Fuchs–Macintyre1940, Sakai1982/1983/1984, Gustafsson–Sakai1994, EH2002 full chapter, LP journal final, HL2019 final chapter, later Baernstein–Montgomery-Smith versions, and all 80 EH citation fullbodies were not completely inspected. Unindexed work, other languages, books, theses and uncited applications remain possible. These gaps prevent a global novelty certificate.

The justified wording is the manuscript's present posture: **a complete affirmative deduction from established theorems, with no priority/novelty claim**. Query strings, retrieval failures, body hashes/read scopes, historical pins, unchanged-input checks and authored artifact hashes accompany this report. Audit completion 100% refers to the assigned bounded audit, not certainty about global literature.

