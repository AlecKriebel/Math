# PR154 / 30000229: independent modern AFEM priority review

Review checkpoint: 2026-10-12 UTC. Scope: the exact endpoint implication for square Dirichlet Poisson, fixed compatible shape-regular newest-vertex-bisection (NVB) forest, continuous P1 solution approximation in energy, and arbitrary-real P0 data approximation in the global H^-1 norm. Original candidate head: `58bee8514677549ee5a7cd699028a5f3a616c5bc`. The historical original `claimed_solved2/5` is not a priority assessment.

## Decision

The asserted endpoint discovery and the proposed zero-element-mean cubic edge-bubble bridge are prior work. The endpoint failure is already the content of Kreuzer–Veeser, Lemma 21, in the March 2019 preprint and its April 2021 published version. The bridge uses their very same face bubble, up to normalization. The global conclusion follows from their localization inequality, valid for every H^-1 functional. This is exact overlap, not merely overlap with a localized estimator.

The current proof's explicit `log(N)/sqrt(N)` lower bound is more explicit than the published Lemma 21 statement. However, it follows by one additional Cauchy inequality from the old fixed-coefficient CDN construction and the old face-bubble mechanism. I do not certify a new mathematical contribution on this basis. Preserve the work as a reproducibility/expository audit or a quantitatively explicit corollary with full attribution, not as a first solution to the 2005 question.

Completion of this assigned, bounded priority audit: **100%**. Confidence that endpoint failure and the bubble bridge predate the candidate: **very high**. Earliest exact global all-P0 consequence verified here: **14 March 2019**, by the public arXiv v1 source plus its own Lemma 4(ii). This is not a claim that nothing earlier exists.

## Exact target and prior theorem

Write

\[
 a_N(u)=\inf_{\#\mathcal T\le N}\inf_{v\in P_1(\mathcal T)\cap H^1_0}
              \|\nabla(u-v)\|_{L^2},\qquad
 E_N(f)=\inf_{\#\mathcal T\le N}\inf_{g\in P_0(\mathcal T)}
              \|f-g\|_{H^{-1}(\Omega)}.
\]

The rejected universal implication is `sup_N sqrt(N) a_N(u)<infinity` implies `sup_N sqrt(N) E_N(-Delta u)<infinity`. All P0 coefficients are unrestricted real numbers. The H^-1 norm is dual to the gradient norm on H^1_0. Cardinality shifts by the fixed initial mesh or fixed multiplicative completion constants do not change this claim.

Kreuzer–Veeser 2021, Lemma 21, printed pp. 66–68, equations (3.32a,b), has both infima over **all** recursively or iteratively generated NVB meshes from one initial square mesh. Its data error also minimizes over **every** P0 function. It states a solution error bounded by `N^-1/2` and a local-star data error bounded below by `L_N N^-1/2`, where `L_N -> infinity` and `L_N` is bounded above by a multiple of `log N`. It explicitly uses the CDN Section 6.4 construction. These exact quantifiers are present in arXiv v1, pp. 17–19, as well as the published article. [Publisher](https://link.springer.com/article/10.1007/s00211-021-01194-8), [2019 v1](https://arxiv.org/abs/1903.05915v1).

The paper's own Lemma 4(ii), printed p. 52, says for **any** functional `ell` (no Galerkin orthogonality assumption)

\[
 \sum_z\|\ell\|_{H^{-1}(\omega_z)}^2
       \le (d+1)\|\ell\|_{H^{-1}(\Omega)}^2.
\]

Our deduction is immediate: apply it with `ell=f-g`, `d=2`, and take the same two infima. Then `E_N(f)>=L_N/(sqrt(3 N))`. Thus the different norm in the displayed Lemma 21 cannot preserve novelty of the global endpoint counterexample. The inequality direction is essential: the local sum is at most the global norm times a fixed factor, so a lower bound on the local sum is a lower bound on the global error.

## The proposed bridge is algebraically identical

Published formula (3.19b), printed p. 58, and Lemma 7 construct a face test function biorthogonal to the volume characteristic functions and face integration functionals. In two dimensions, on either of the two triangles sharing edge `e=[A,B]`, with opposite vertex `C`, its formula simplifies to

\[
 \psi_e^{KV}=\frac6{|e|}\lambda_A\lambda_B(1-5\lambda_C).
\]

The original candidate uses

\[
 \psi_e^{candidate}=4\lambda_A\lambda_B-20\lambda_A\lambda_B\lambda_C
                   =\frac{2|e|}{3}\psi_e^{KV}.
\]

This is exact equality, not a resemblance. The zero mean on each incident triangle annihilates every element-constant volume term; the trace integrates the selected face jump. KV's Lemma 21 proof uses this exact cancellation against arbitrary `g in P0` through Lemma 7 and Theorem 15. Their local stability depends only on dimension and shape regularity. Consequently an attribution merely to the CDN hat series is insufficient: **Kreuzer–Veeser must also be credited for the claimed new bridge**. [Published PDF](https://link.springer.com/content/pdf/10.1007/s00211-021-01194-8.pdf).

The selected-edge global test in the current proof is a particularly transparent way to sum these old face tests. Its overlap bound, exact reference energies, and explicit constants supply useful verification, but do not constitute a different mathematical mechanism.

## Adversarial check of the older proof

One should not hide an apparent omission in the published Lemma 21 proof. Its last step subtracts a Galerkin energy error on an arbitrary mesh and then invokes the best-mesh upper bound (3.32a). A minimum upper bound does not by itself bound the error on every competing mesh. The same omission occurs in the 2019 v1. It is not safe to repeat the literal implication without a mesh overlay.

Here is a checkable repair using the paper's ingredients. For a competitor `T` of at most `N` elements, overlay it with one good solution-approximation mesh `R_N` having `O(N)` elements and energy error at most `C N^-1/2`. On `T*=T overlay R_N`, all constants from `P0(T)` remain constants, and the Galerkin error is at most the good-mesh error. The all-mesh lower bound for the raw CDN local data norm applies at the enlarged budget `C_0 N`; it has an unbounded multiplier there too. The local-stable face/volume separation from KV then gives

\[
 D_{T^*}(f-g)\gtrsim D_{T^*}(f)-C\|\nabla(u-U_{T^*})\|
 \gtrsim (\widetilde L_N-C)N^{-1/2}.
\]

Finally Lemma 4(ii) bounds `D_{T*}(f-g)` by `sqrt(3)||f-g||global`. This proves the all-competitor global result with changed fixed constants. No comparison between the star norms on `T` and `T*` is required. The omitted line is therefore repairable by standard NVB overlay, and provides no new route or central unsupported claim.

An even more direct reconstruction uses a finite CDN partial sum `V_n`, the overlay on which it is P1, the old KV face tests, and the energy-isometric tail estimate. This is the original candidate's route. It independently confirms that the prior statement is not resting on an irreparable gap.

## Explicit logarithmic rate: printed statement versus direct corollary

The complete CDN author preprint is dated 20 April 2011. Section 6.4, printed pp. 29–31, has **the same** hat coefficients: their `u=sum_j 2^-j psi_j`, `psi_j=2^-j sum_i phi_Qij` is exactly `sum_j 4^-j sum_i phi_Qij`. It uses the square's four-triangle master pattern and compatible NVB labels, one macro square at each scale, and `4^j` micro squares at scale `j`. Its equations (6.22)–(6.25) perform edge subdivision and allocation. [Complete author preprint](https://math.umd.edu/~rhn/papers/pdf/afemH-1.pdf).

Visual inspection of preprint p. 31 confirms that its final printed allocation sentence gives `n 4^(-n-2)`, not `n^2 4^(-n-2)`. Its explicit lower conclusion is therefore only enough for an unbounded multiplier of order `sqrt(n)` by that sentence. KV's `L_N -> infinity` with an upper logarithmic bound also does **not** literally assert `L_N >= c log N`. Do not misquote either source as explicitly printing the candidate's logarithmic lower bound.

Nevertheless, the stronger lower rate is an elementary corollary of the displayed old allocation ingredients. To avoid incidental overstrong statements about all jump edges, select just one interior spoke per micro square. After overlay let `m_ij` count its fine subedges. Same-forest linear overlay and planar edge incidence give

\[
 \sum_{j=1}^n\sum_{i=1}^{4^j}m_{ij}\le C4^n.
\]

The old constant jump and old spoke length give a fixed positive constant times

\[
 \sum_{j=1}^n\sum_{i=1}^{4^j}\frac{4^{-2j}}{m_{ij}}
 \ge \frac{\big(\sum_{j=1}^n\sum_{i=1}^{4^j}4^{-j}\big)^2}
             {\sum_{j,i}m_{ij}}
 \ge c n^2 4^{-n}.
\]

The middle numerator is exactly `n^2`. KV's already published mean-zero face tests turn this into the global all-P0 error for `S_n=-Delta V_n`, bounded below by `c n 2^-n`. The old H^1 tail is `O(2^-n)`, so subtracting it yields `(c n-C)2^-n` for `f`. Since `N=4^n`, this is `c log(N)/sqrt(N)` for large `N`. Monotonicity interpolates to every budget with a fixed factor. This deduction uses neither an additional regularity premise nor bounded P0 coefficients.

The candidate's exact tail annihilation avoids subtraction and clarifies constants. That is an exposition improvement. No matching best-P0 upper bound has been verified here; no sharp-equivalence claim is made.

## Later approximation classes and adjacent work

Bonito–Canuto–Nochetto–Veeser, *Adaptive Finite Element Methods*, Acta Numerica 33 (2024), 163–485, DOI `10.1017/S0962492924000011`, provides a modern account. Its Remark 4.15 points to KV Lemma 21. Definition 4.17 allows polynomial densities on **both volume elements and interior faces**. Definition 6.8 measures locally best approximation in that enriched functional space; Lemma 6.9, including `s=1/2` for `d=2,n=1`, transfers the solution class to this enriched load class for initially discrete coefficients. It is not a theorem about volume P0 approximation. This distinction is the modern resolution of the invariance obstacle, and is compatible with the counterexample. The relevant definitions and lemmas were checked in both arXiv versions and the author final preprint. [ArXiv](https://arxiv.org/abs/2402.07273), [author final preprint](https://people.tamu.edu/~bonito/Publications/Preprints/2024_afem_acta.pdf).

Gantumur's *Convergence Rates of Adaptive Methods, Besov Spaces, and Multilevel Approximation*, arXiv `1408.3889` v1/v2 and FoCM 17 (2017), 917–956, studies energy-plus-oscillation classes. In its elliptic section the load is expressly in L2, and oscillation uses local L2 polynomial projections. It does not assert endpoint equivalence for general H^-1 volume P0 data. This is adjacent positive approximation theory, not a loophole in the negative priority finding. [Primary preprint](https://arxiv.org/abs/1408.3889).

OWR 42/2016, printed pp. 2433–2436, already describes the bulk-plus-face residual projection and suitable face/element bubbles, but does not print the explicit all-P0 Lemma 21. Tantardini's contribution on pp. 2436–2438 distinguishes global H^-1 polynomial approximation from local norms. It is useful context, not an earlier exact certificate. Verfürth's own page lists two October 2016 reports without download links. Their complete contents were not obtained and are not needed for the decisive 2019/2021 overlap. [OWR](https://ems.press/content/serial-article-files/46646), [author report listing](https://homepages.rub.de/ruediger.verfuerth/).

The limited 2025–2026 targeted search did not identify a later paper needed to establish this priority result. A 2026 primary conference abstract on randomized polynomial projections concerns right-hand sides in L2; it is not evidence of a positive general H^-1 endpoint theorem. Absence from a bounded search is not a literature-wide nonexistence claim.

## Versions, gaps, and provenance

* KV arXiv lists only v1 (14 March 2019). The downloaded versionless and v1 PDFs are byte-identical. Published 2021 full PDF and HTML were acquired and independently checked; Lemma 21, Lemma 4(ii), and bubble formula persist. There is no acquisition gap for the decisive source.
* The CDN complete author preprint was acquired and rendered. The final 2012 publisher page/abstract was available, but a public PDF download returned purchase-page HTML. Its final typeset Section 6.4 was not acquired. Consequently I make no claim about whether the typeset version strengthens the final numerical sentence. This cannot restore the novelty of the 2019/2021 theorem or bubble.
* Acta arXiv v1 (11 February 2024), v2 (10 May 2024), and author final preprint were acquired. Relevant definitions and theorem locators persist. Gantumur v1 and final arXiv v2 were acquired; the elliptic load restriction was checked in v2.
* No sibling priority report was read. Parent's independent precise KV comparison was received only after FIRST_ASSESSMENT and the independent KV discovery. It prompted adversarial verification, not an inherited verdict.
* All created files are in the assigned `priority_modern_afem` folder. Source PDFs, extracted text, raw HTML, and renderings are private-cache files excluded by its `.gitignore`. No Git/index/ref/main/PR/publication write, release, push, or individual outreach occurred.

`SOURCE_DOWNLOADS.json` records download URLs, failures, UTC timestamps, byte counts, and SHA256. `SEARCH_PROVENANCE.json` records the bounded queries and source locators. `BYTEHASH_MANIFEST.json` inventories the exact consumed local artifacts and produced outputs, excluding its own recursively impossible self-hash; its digest is in `BYTEHASH_MANIFEST.sha256`. Original source files were never overwritten.
