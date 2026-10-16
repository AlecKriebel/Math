# Independent priority and attribution audit

Audit date: **2026-10-06, America/Los_Angeles** (retrievals around 2026-10-07 05:12–05:20 UTC). Internal independent research subagent. No person was contacted; no commit, push, or deposit was performed. Upstream checkout remained read only.

## Conclusion and limits

If OpenAI family 200's characteristic-zero EGH claim is valid, this project's target is an immediate consequence of previously published machinery. The mechanism and **all-ideal scope are inherited**. The possible newly available item is the unrestricted characteristic-zero consequence, with explicit scope verification. This is not an independent solution of EGH, a new EGH-to-Sperner theorem, a new arbitrary-ideal extension, or a Lefschetz theorem. This audit does not certify the central upstream proof or first priority. If that proof has a material gap, an unconditional solution claim is blocked.

## Exact published implication

Primary source: Harima–Wachi–Watanabe, [arXiv:1601.06928v1](https://arxiv.org/abs/1601.06928v1), submitted **2016-01-26 08:55:23 UTC**; *Proc. Amer. Math. Soc.* **145** (2017), no. 4, 1497–1503, [DOI 10.1090/proc/13347](https://doi.org/10.1090/proc/13347). Entire seven-page arXiv PDF inspected.

| Location | Scope |
|---|---|
| Definition 2, p. 2 | Dilworth number maximizes over **all ideals**, with generator number given by dimension modulo the maximal ideal. |
| Definition 5, Proposition 7, p. 3 | Matching property; monomial complete intersections possess it over any field. |
| Proposition 8, Sublemma 9, p. 4 | Matching, Gorenstein, and unimodality imply Sperner. Proposition 8 invokes Watanabe [17], Lemma 2.4, for the graded-ideal reduction. |
| Conjecture 10, Theorem 11, pp. 4–5 | EGH for a fixed graded complete intersection implies its Sperner property over any field. |
| Theorem 13, Remark 14, p. 6 | Prior split-linear-factor cases and the stated n−2-generator relaxation. |

The exact EGH hypothesis requires Hilbert matching for **every homogeneous overideal** of the defining sequence; it does not require Betti domination. The proof transfers matching from the pure-power quotient and applies Proposition 8.

The arXiv page lists only v1 dated January 2016, although the retrieved PDF title page displays September 19, 2018. That internal date does not override the submission record. The publisher DOI was inaccessible through the browser, so exact theorem statements were audited in arXiv v1, not an unexamined publisher version. Retrieved PDF SHA-256: `b66c69b4c9e901ddb2b9fc6e655a9d4a7c276558638014ee5bb0075fbf453172`.

Original reduction attribution: Watanabe, *The Dilworth Number of Artinian Rings and Finite Posets with Rank Function*, *Adv. Stud. Pure Math.* **11** (1987), 303–312, [DOI 10.2969/aspm/01110303](https://doi.org/10.2969/aspm/01110303). Its publisher page was located, but the body/PDF was inaccessible. **Lemma 2.4 was not directly inspected in this audit.** A self-contained filtration proof is useful verification while retaining the older attribution.

Citation-chain corroboration: Güntürkün, [*A Survey on the Eisenbud–Green–Harris Conjecture*, arXiv:2103.14106v2](https://arxiv.org/abs/2103.14106v2), April 6, 2021, §5, PDF p. 11, explicitly records this same all-ideal equality as the HWW application. Pages 4–5 distinguish full-length/general-length EGH; pp. 10–11 distinguish Betti domination. The mechanism was broadly disclosed before family 200. PDF SHA-256: `fd376c3487069e0a3b41967fb1892d39c5e23998112082d0f2053ccedb842e39`.

## Upstream scope and public provenance

Pinned commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Inspected `/Users/alec/Desktop/math` and the project source copies:

- [*Commuting Division-Coefficient Forms and the Artinian Eisenbud–Green–Harris Conjecture*](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026/paper.pdf), introduction `cor:characteristic-zero` and consequences/generality section: claims every characteristic-zero field, standard grading, regular-sequence length 1≤c≤n, ordered degrees ≥2, and one monomial pure-power overideal matching the quotient Hilbert function in **every** degree.
- [*The Artinian Lex-Plus-Powers Betti Theorem*](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026/paper.pdf), introduction `thm:main`/`cor:characteristic-zero`, section 8: claims this plus stronger Betti inequalities. HWW only needs Hilbert matching with c=n.

Both READMEs name **OpenAI** as author and September 23, 2026 as manuscript date. Use their supplied manuscript-specific BibTeX blocks. Do not invent human coauthors or attribute the base EGH claim to this project.

Primary public release evidence: OpenAI's [*Sharing AI progress in mathematics*](https://openai.com/index/sharing-ai-progress-in-mathematics/) is dated **October 6, 2026**, links GitHub, and announces release of the collection. Official GitHub API and remote-reference observations:

| Datum | Value |
|---|---|
| Repository `created_at` | 2026-10-06T21:47:02Z |
| Single initial commit author/committer time | 2026-10-06T21:58:50Z |
| Repository `pushed_at` | 2026-10-06T22:01:11Z |
| Remote HEAD/main | `adc7f1241b42e322a6451854ab7e4b4c146bf78a` |
| Releases | empty list |

The remote was queried with `git ls-remote`; no fetch or checkout mutation occurred. Observed official sources support October 6 collection release; **September 23 public priority is not established**. Repository/commit timestamps alone cannot determine when visibility changed. Earlier disclosure is not excluded. No later official correction/version appeared in the checked main history. Evidence: `sources/priority/retrieval_provenance.json`.

## More recent statements actually examined

1. Abedelfatah, [arXiv:2607.20035v1](https://arxiv.org/abs/2607.20035v1), July 22, 2026, Theorems 4.2–4.3, PDF pp. 4–6. These concern six quadratic regular-sequence forms with two extra quadrics (a cubic dimension estimate) and quadratic almost complete intersections with one extra quadric. They do not supply EGH for **every overideal** of every CI, so cannot replace family 200. The introduction describes general EGH as still open before the October release.
2. Kuzmanovski, [arXiv:2608.17281v1](https://arxiv.org/abs/2608.17281v1), August 18, 2026; [full HTML](https://arxiv.org/html/2608.17281v1). Theorems 1.4–1.5 give sufficiently-large-initial-degree Hilbert matching in bounded windows for fixed types/defects; 1.9 similarly restricts Betti comparison; 1.10–1.11 and 11.3–11.4 restrict Lefschetz assertions to asymptotic windows. They do not establish unrestricted all-ideal Sperner. The paragraph after 1.5 explicitly identifies all-degree coverage and removal of the large-degree condition as remaining EGH requirements.
3. Migliore–Miró-Roig–Murai–Nagel–Watanabe, [*On ideals with the Rees property*, arXiv:1305.2551](https://arxiv.org/abs/1305.2551), pp. 1–4 inspected. Theorem 1.1 concerns monomial almost complete intersections in three variables and separates Sperner examples from WLP. It does not solve arbitrary-codimension CIs.

The classical codimension-three CI WLP result is already cited as Harima–Migliore–Nagel–Watanabe (2003) in Kuzmanovski, Theorem 4.5. Low-codimension examples should not be presented as newly resolved. No exhaustive classification of every historical special case is claimed.

## Searches and novelty boundary

Queries on October 6, 2026: `Sperner property` + `complete intersections`, with 2024/2025/2026 variants; `EGH` + `Sperner`; `Eisenbud Green Harris` + `Sperner` + `2026`; arXiv/AMS restricted variants; exact OpenAI manuscript titles; official release searches. No examined primary source independently asserted the unrestricted characteristic-zero corollary beyond the new EGH dependency.

All pinned repository TeX/Markdown manuscripts and overview/catalog were searched for `Sperner property`, `Dilworth number`, `Harima`, `Watanabe`, and `13347`; the family 200 consequence sections were read. No direct Sperner statement was found. PDF-only material, alternate terminology, unindexed sources, or new updates can evade this bounded search. **Failure to locate a statement does not establish novelty.**

The target adds no new hypothesis-removal theorem beyond applying HWW to the characteristic-zero EGH claim. Eliminating linear generators, handling the empty/all-linear case, field descent, and the product Hilbert formula are scope verification. All-ideal filtration verification is inherited scope made explicit. A defensible note identifies the consequence and both upstream attributions; it remains conditional if central EGH validation fails. If an identical explicit consequence/proof is already public, the user’s anti-duplication instruction bars a separate preprint advertised as new.

This audit clears attribution and mathematical-scope interpretation, **not unconditional mathematical readiness or first priority**. Publication requires separate dependency verification and review of the exact final candidate. Audit-created third-party PDFs were removed after a full-disk error; their retrieval hashes/provenance remain. Do not redistribute third-party source material without rights. Estimates for this subtask: audit 90%; publication-priority clearance 40% pending central dependency and final-candidate review. Estimates are planning only, not evidence.
