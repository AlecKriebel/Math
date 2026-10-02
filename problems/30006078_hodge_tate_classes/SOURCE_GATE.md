# Source and prior-attempt gate: 30006078

Source gate completed 2026-10-02. Substantive author turns before this gate: **0/5**.

## Exact question

The authority is Alexander Petrov, *Characteristic classes of étale local systems* (joint work with Lue Pan), in *Anabelian Geometry and Representations of Fundamental Groups*, Oberwolfach Report 45/2024, printed pp. 2656–2658, DOI [10.4171/OWR/2024/45](https://doi.org/10.4171/OWR/2024/45). The final question is on p. 2658, physical PDF page 38. All three contribution pages were read and visually inspected.

For a smooth algebraic variety X over a finite extension K/Q_p and a Hodge–Tate étale Z_p-local system L, the question asks whether

    alpha_X(ell_i(L)) = (i−1)! sum_m m ch_{i−1}(gr^m D_HT(L))

in H_dR^{2i−2}(X/K). The source defines the odd classes by pulling back the continuous-cohomology generators of GL_r(Z_p); deg ell_i=2i−1. The degree-one class is log_p det rho_L. The source's map is

    H_et^n(X,Q_p) -> H^1(G_K,H_et^{n−1}(X_Kbar,Q_p) tensor B_dR)
                  ~= H_dR^{n−1}(X/K).

This is arithmetic étale cohomology with **untwisted Q_p coefficients** on the left. It is not a question about the usual even Chern classes of a flat bundle. Properness and good reduction are not hypotheses of the question. The report says alpha is an isomorphism under good reduction for n>1; this ancillary statement is not assumed outside that setting. The grading convention is the one in the report: for relative cohomology R^j f_* Z_p the degree m term is R^{j−m} f_* Omega^m.

The report does not give a cocycle-level construction or a sign-normalization formula for alpha. Any degree-one calculation must check that convention; an arbitrary identification of H^1(G_K,B_dR) with K is insufficient to manufacture a counterexample. For higher generators we use the stable primitive Borel/regulator convention of the cited Pappas and Huber–Kings constructions, not an arbitrary change of exterior-algebra generators by decomposable terms. In arguments where the rank is smaller than i, the stable primitive class is understood by adding trivial summands and restricting.

## Credited existing results and boundaries

The same report's Theorem 1 gives the top-degree formula for a smooth proper geometrically connected variety over **Q_p**. It does not prove the entire displayed question for arbitrary K, X, and i. Its proof description uses c_i(L tensor O_hat_X)=ell_i(L) cup kappa_i and explicitly explains that this product loses information in general. We do not cancel kappa_i without an injectivity argument. The dimension-zero assertion H^1(G_Qp,Q_p)~=Q_p printed in the theorem's chain cannot be used literally; our uses of that top-degree theorem will have positive dimension.

Theorem 2 concerns geometric varieties over algebraically closed characteristic-zero fields, with a rank-dependent large-p hypothesis. It does not give arithmetic vanishing for the target.

Pappas, [arXiv:2006.03668v3](https://arxiv.org/abs/2006.03668), §4.4.2, defines stable higher regulator classes and their top-degree pushdowns. Huber–Kings, [arXiv:math/0612611](https://arxiv.org/abs/math/0612611), Definition 0.4.5, Remark 0.4.6, Definition 1.2.3 and Theorem 1.3.2, pin down the alternating-trace primitive and its Lazard/regulator comparison. Their normalization and theory are credited inputs, not new results.

Petrov, [arXiv:2012.13372v3](https://arxiv.org/abs/2012.13372), §2, Theorem 2.4, Proposition 3.5, Lemma 3.6, Proposition 5.1, Theorem 5.2 and Proposition 7.2/Corollary 7.3, supplies the relative Hodge–Tate and Riemann–Hilbert framework. In particular this is not permission to identify every Hodge–Tate local system with a de Rham one.

The imported suggestion to split D_HT(L) on an ordinary flag bundle does not split the étale local system L or calculate its odd classes. A splitting argument needs an actual compatible comparison theorem.

## Retrieval and literature reconciliation

- Requested [unsolvedmath page](https://www.unsolvedmath.com/problems/30006078) was attempted but not accessible through the web tool; the pinned imported record was used and checked against the primary source.
- The [publisher page](https://ems.press/journals/owr/articles/14298795) links the [full official PDF](https://ems.press/content/serial-article-files/50758), successfully downloaded and rendered.
- The old MIT author-PDF URL returned an HTML relocation page to direct download. The current [author homepage](https://sasha-pt.github.io/) links a working [three-page author excerpt](https://sasha-pt.github.io/papers/pdf/ow_2024.pdf), which agrees on the target. Its reporter footer names Qi Ge; the mathematical contribution is attributed to Petrov with Pan. This explains the imported Ge attribution without adopting it as the contribution's author.
- Both current author publication lists, [Petrov](https://sasha-pt.github.io/) and [Pan](https://sites.google.com/view/luepan/home), were checked. No later full paper proving the general formula was found. This is a bounded search result, not a claim that no such work exists.
- The 2024 IAS/Stanford and 2025 Pittsburgh primary seminar announcements describe partial relations. The newer Petrov survey on arithmetic local systems supplies background, not a resolution of this formula. Heng Du's 2026 preprint 2604.03220 concerns Newton polygons and relative monodromy, a different target.

Raw PDFs, page images, and imported records are retained locally only; SOURCE_MANIFEST.json binds their provenance without redistributing them.

## Repository/prior-attempt gate

Live main was 198b8acb0a560f2dc0cef1e57b557fadb65eaaa3 when checked. QUEUE row 375 was queued, 0/5. Exact-ID all-state PR, branch, and commit searches returned no result. Main code search found only catalog assignment metadata. Alias PR searches for Hodge, characteristic classes, and Pan/Petrov found no overlapping attempt (the Airy wild-Hodge and Ricci-expander results are unrelated). A read-only recovered clone had 443 refs: all-ref commit-subject and per-ref tree-path searches for the ID/Hodge–Tate/Pan–Petrov aliases found no attempt. This gate does not certify absence of unindexed prose in every historical blob.

The pinned source dataset revision is 37e53eabe540fb458758e198be61634bd02ee008. Its problems.json SHA-256 is 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf; research_results.json SHA-256 is 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b. The catalog's statement hash is ca52166059be1797a021dabb2f6b9049391cd743543abe7ab980bffb5a39ac13; the imported prior report is null.

**Gate outcome:** distinct target, available primary statement, ready for substantive research. No author turn is consumed by this gate.
