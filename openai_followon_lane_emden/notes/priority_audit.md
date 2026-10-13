# Independent priority and attribution audit

Audit started 2026-10-06 PDT; source/metadata retrieval timestamps are preserved in the accompanying manifests. This is a literature/provenance audit, independent of the upstream-proof and transfer-proof agents. It is not a validation of the unreviewed upstream theorem. No outside individual was contacted.

## Provisional verdict

The requested pure-power distance, exterior, and arbitrary zero-Dirichlet half-space conclusions are the exact established implications in Poláčik–Quittner–Souplet (PQS), not a new reduction. Fixed-domain Dirichlet bounds are likewise an established conditional transfer, explicitly stated in the later Quittner–Souplet (QS) paper. Gradient and compactness conclusions follow from ordinary elliptic estimates once those bounds hold. If the family 370 entire Liouville theorem is sound, the full exponent range becomes available immediately. The substantive upstream breakthrough must be credited to OpenAI; this effort could accurately be presented as a short consequence/exposition note documenting newly available scope and exact boundary regularity. It cannot be presented as our independent solution of the Lane–Emden conjecture, a new doubling method, or a new Dirichlet blow-up method.

There is no mathematically new mechanism identified in the core target. The newly available full-subcritical scope is a consequence of the upstream theorem and prior reductions. A standalone note is only defensible if this modest contribution is transparent throughout title, abstract, metadata, and paper, the upstream input actually survives proof validation, and later primary-source checking does not reveal the same combined consequence already explicitly public. Absence of search hits does not certify novelty. If the upstream input has a material gap, this audit supports only a conditional account, not an unconditional publication.

## Exact prior implications

Let \(n\ge3\), \(p,q>1\), \(\alpha=2(p+1)/(pq-1)\), and \(\beta=2(q+1)/(pq-1)\). Write LP for nonexistence of bounded, nontrivial, nonnegative classical entire solutions of the pure-power system.

| Requested conclusion | Primary locator and previously public mechanism | Attribution consequence |
|---|---|---|
| \(u\le C d^{-\alpha}\), \(v\le C d^{-\beta}\) on arbitrary proper domains | PQS Theorem 4.3, PDF p. 9; assumes LP and gives the exact estimates with \(C=C(n,p,q)\). | Entirely established conditional theorem. |
| Exterior decay for \(|x|\ge2R\) whenever the domain contains \(\{|x|>R\}\) | Same PQS Theorem 4.3. | Already part of the exact transfer theorem. |
| Arbitrary nonnegative zero-Dirichlet half-space solution is zero | PQS Theorem 4.2, PDF p. 9, assumes LP; solution class \(C^2(\mathbb R^n_+)\cap C(\overline{\mathbb R^n_+})\); no boundedness/growth requirement on the half-space solution. Proposition 7.1, pp. 17–18, supplies the boundary-local estimate used in the proof. | Established conditional half-space transfer. |
| Fixed bounded sufficiently smooth domain, uniform zero-Dirichlet \(L^\infty\) bounds | QS Theorem 4.1(ii), arXiv:2407.04154v1 and v2, PDF pp. 14 and 46 (v2). Assumes the pure-power entire Liouville property; allows uniformly regular \(C^2\) domains. Remark 4.1(ii) credits the pure-power \(p,q>1\) specialization to PQS. | Not a new boundary argument. Cite QS and PQS/Gidas–Spruck. |
| Asymptotically positive constant multiples of powers | PQS Theorem 7.3, pp. 18–19: continuous scalar nonlinearities with \(f(t)t^{-p}\to\ell_1>0\), \(g(t)t^{-q}\to\ell_2>0\); conclusion includes additive constants. | Already an exact conditional extension; cannot be used as a novelty claim. |
| Gradient estimates \(|\nabla u|\le C d^{-\alpha-1}\), \(|\nabla v|\le C d^{-\beta-1}\) | Interior rescaling and elliptic gradient estimates; PQS Remark 7.4 expressly notes gradient extensions. | A standard derivative consequence, requiring a written verification. |
| \(W^{2,r}\) bounds and corresponding compactness on fixed smooth bounded domains | Elliptic Dirichlet estimates after \(L^\infty\) control; additional Hölder/Schauder claims must state actual boundary regularity and target topology. | Standard functional-analytic consequence, not a new Lane–Emden theorem. |

PQS primary source: [author PDF](https://www-users.cse.umn.edu/~polacik/Publications/pqs1.pdf); published as Duke Math. J. 139 (2007), 555–579, [DOI](https://doi.org/10.1215/S0012-7094-07-13935-8). The saved author PDF has theorem numbers used in the brief. The earliest preprint disclosure date of this particular PDF has not been independently established; the 2007 journal publication is sufficient to establish that the reduction predates this project.

QS primary source: [arXiv v2](https://arxiv.org/abs/2407.04154v2), *Liouville theorems and universal estimates for superlinear elliptic problems without scale invariance*, Rev. Mat. Complutense 38 (2025), 1–69. Public arXiv v1 date 2024-07-04 21:06:34 UTC; v2 2024-09-26 11:56:59 UTC. I downloaded both PDFs and verified Theorem 4.1(ii) and Remark 4.1(ii) are already present in v1. The broader regularly varying extension in this paper is also prior work. It requires its own regularity hypotheses and should not be silently identified with the weaker continuous-asymptotically-power assumptions of PQS Theorem 7.3.

QS's convention is nonnegative strong solutions: the page-2 footnote defines the local class as \(W^{2,r}_{\mathrm{loc}}\) for all \(r\in(1,\infty)\), with continuity up to the boundary when Dirichlet conditions are imposed. The classical pure-power solutions requested here fall within that class by local elliptic regularity. This broader source class does not itself authorize unspecific weak-solution assertions in the follow-on note.

## Modern half-space distinction

[Li–Souplet, arXiv:2408.17007v2](https://arxiv.org/abs/2408.17007v2), Theorem 1.1, establishes half-space nonexistence for all \(p,q>1\) provided the solution is bounded on every strip \(0<x_n<R\). The exact classical class is \(C^2(\mathbb R^n_+)\cap C(\overline{\mathbb R^n_+})\). This is not the unrestricted class requested here: continuity on the noncompact closure does not imply uniform strip boundedness. Public arXiv v1 date 2024-08-30 04:40:04 UTC, v2 2025-06-05 15:09:25 UTC. I checked the exact statement in both the v1 HTML and downloaded v2 PDF.

Their introduction, citing Chen–Lin–Zou, J. Funct. Anal. 266 (2014), 1088–1105 ([DOI](https://doi.org/10.1016/j.jfa.2013.08.021)), records that globally bounded half-space solutions were already excluded for every \(p,q>1\). That original full text was not retrieved in this pass; do not describe its proof as independently audited here. It follows from the directly checked Li–Souplet theorem that the bounded half-space limits used in ordinary Dirichlet blow-up were already unavailable, independently of subcriticality.

## Family 370 inventory and public provenance

The pinned input is repository commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The upstream clone was read only. I read its root README, family 370 entry in `CONTENTS.md` (lines 8972–8981), `lean/docs/370.md`, the manuscript-specific README and BibTeX, introduction, conclusion, and bibliography, and searched all six manuscript sections for the target conclusions. I did not validate the intervening proof. The manuscript map and Lean scope document list exactly one family 370 manuscript, *The Subcritical Hénon–Lane–Emden Conjecture*. A corpus sweep for the word Emden across manuscript TeX, bibliographies, and READMEs found this sole relevant PDE manuscript plus an unrelated Yamabe bibliography title in an Einstein four-manifold manuscript. A broader Hénon search had two irrelevant Ramsey lexical matches. No family companion states the requested full estimate suite. This is a check of the released catalogue, not a proof that no unpublished companion exists.

The manuscript states the weighted entire positive theorem and, explicitly, its unweighted entire corollary. It mentions the role of Liouville inputs in estimates in its introduction but does not state or prove the local/boundary estimate suite. The catalogue result and formalization-scope claim are evidence of what was asserted, not evidence of correctness or successful formal verification.

The manuscript's printed date is **24 September 2026**. Its independently verified public disclosure is associated with the **6 October 2026** release. The official [OpenAI release announcement](https://openai.com/index/sharing-ai-progress-in-mathematics/) is dated 6 October. The public GitHub API currently reports repository creation `2026-10-06T21:47:02Z`, initial commit `2026-10-06T21:58:50Z`, and last push `2026-10-06T22:01:11Z`. The path-specific history contains only the pinned initial commit at retrieval. A Git commit timestamp alone is not a public-disclosure timestamp; together with the dated announcement and public repository it supports 6 October as the verified release date, not 24 September. The exact moment of public visibility and any earlier private circulation have not been established.

Use the manuscript-specific citation rather than attributing the entire theorem to this follow-on note:

```bibtex
@misc{OAI:The-Subcritical-Henon-Lane-Emden-Conjecture-September-24-2026,
  author = {{OpenAI}},
  title = {{The Subcritical H{\'e}non--Lane--Emden Conjecture}},
  howpublished = {OpenAI Math Release preprint
    \href{https://github.com/openai/math/blob/main/preprints/The-Subcritical-Henon-Lane-Emden-Conjecture-September-24-2026/paper.pdf}{OAI:The-Subcritical-Henon-Lane-Emden-Conjecture-September-24-2026}},
  year = {2026}
}
```

For exact reproducibility, additionally pin the commit URL and hash in the dependency ledger. The upstream author is OpenAI as supplied; no human upstream coauthor or conventional peer-review status should be invented.

## What scope is newly available, assuming the input is valid

The full \(n\ge3\), \(p,q>1\), strict-subcritical hyperbola is available after LP is established. This must not be described as a new result at every parameter pair: the full range in dimensions three and four, both-powers-Sobolev-subcritical regions in arbitrary dimensions, Souplet's higher-dimensional \(\max(\alpha,\beta)>n-3\) region, and later sufficient regions were already known. “Complete range” is accurate; “first bounds for all dimensions” is not.

There is also an equivalence that limits novelty claims. If a universal proper-domain distance estimate holds, restricting any entire solution to a ball \(B_R(x_0)\) and sending \(R\to\infty\) forces both components to vanish. PQS supplies the converse from LP for \(p,q>1\). Thus the arbitrary-domain bound and whole-space nonexistence encode the same obstruction. The elementary strong maximum principle changes a nontrivial nonnegative pair into a positive pair and matches the upstream class; that observation is not a new theorem mechanism.

The full result is therefore a previously established conditional theorem with a newly asserted entire-space input. If valid, a consequence note can make the scope unconditional, but its discovery credit belongs to the upstream theorem. Re-proving normalization, boundary charts, and compactness improves checkability, not analytical originality.

## Search record and limitations

Queries on 2026-10-06 PDT included the exact PQS title/theorem suite; “Lane Emden conjecture a priori estimates full subcritical 2025 2026 half space Polacik Quittner Souplet”; “Lane-Emden universal 2026”; “Lane-Emden a priori 2026 subcritical”; “Lane-Emden full universal estimates”; and the OpenAI manuscript title. Citation chains inspected include family 370's bibliography, PQS's bibliography, QS Section 4/7 and its references, and Li–Souplet's introduction. A separately delegated modern-literature checker inspected current exact primary statements without receiving the proof agents' results; its report is [priority_modern_check.md](priority_modern_check.md), with source captures/hashes in `sources/priority_modern_manifest.json`.

That independent report confirms that Li–Li–Wei (public arXiv v1 on 8 October 2025) gives the smaller region \(1/(p+1)+1/(q+1)\ge1-2/n+4/n^2\), and Huang–Zou (public arXiv v1 on 18 December 2025) retains stability, exact scaling decay, or annular-energy assumptions. Neither gives arbitrary full-range solutions. Xu–Luo's checked publisher theorem preview, specialized to unweighted second-order cross-coupling, requires both powers individually at most the scalar Sobolev exponent and not both endpoint. Sciunzi–Vuono's directional-boundedness result is scalar; Bhattacharyya's estimates depend on bounds on the particular solution. Those mismatches are checkable reasons for nonduplication of the full target, not a general novelty certificate.

Two relevant subscription sources remain exact-statement access gaps: Wen Wang, DOI `10.1007/s12220-026-02487-w`, publicly published 29 May 2026, and Zhihao Lu, DOI `10.1007/s12220-025-01967-9`, publicly published 18 March 2025. Primary abstracts restrict positive-exponent coverage, but the exact theorem ranges/function spaces were inaccessible in the available previews. No access control was bypassed. They cannot be represented as fully audited. Outside input could help close the full-text gaps; none was solicited and no outreach was prepared.

Search snippets, secondary indices, and absence of indexed hits are not theorem validation or priority certification. Modern manifold and stable-solution results cannot be conflated with arbitrary classical Euclidean solutions. Current audit does not certify a “first” claim. Third-party downloaded PDFs are research-source copies, not intended deposit files; redistribution rights were not established here.

## Checkpoint estimate

Priority-audit completion: **90%** for the assigned scope. The independent modern-source pass is complete within public access; the precise remaining literature gap is the two subscription papers above, and exhaustive priority is not certified. Any mathematical input failure must also be reconciled before an unconditional result is promoted. These percentages are workflow estimates only. Mathematical resolution and publication readiness are not certified by this audit.
