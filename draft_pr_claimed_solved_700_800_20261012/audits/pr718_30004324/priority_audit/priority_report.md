# Independent historical priority audit: PR 718 / problem 30004324

Audit performed on 2026-10-13 UTC (2026-10-12 in the user's America/Los_Angeles timezone). This is an AI-assisted literature audit, not external peer review. The parent reports independent mathematical verification; this report does not substitute for it. No outside individual was contacted.

## Verdict

**No earlier full resolution, or previously stated immediate consequence with the exact target assumptions, was identified in this bounded audit. No concrete priority obstacle is established. First priority is not certified.**

The claim matches the unrestricted Fulger–Murayama conjecture. The inspected later primary literature includes Chang's 2025 toric result, which still states the unrestricted assertion as conjectural. That is meaningful evidence of the literature's treatment, not proof that no earlier or later complete argument exists. [Chang, latest arXiv version](https://arxiv.org/pdf/2211.17172v2).

The mathematical tools are largely established. In particular, the numerical-generation principle behind candidate Lemma 5 must be credited as standard. The candidate's possible contribution is the complete reduction at the original specified point, with its characteristic-independent pointed compactification and application to the conjecture, rather than an invention of unsplit-family Picard-rank arguments.

## Claim audited and success criteria

Let X be a smooth integral projective n-fold over an algebraically closed field k, in arbitrary characteristic. If the relative Fulger–Murayama tangent-bundle Seshadri constant is positive at one specified closed point x, then X is isomorphic to P^n. No Fano, globally nef tangent, general-point, or characteristic-zero hypothesis is added.

A disqualifying earlier result would state this implication, or a stronger theorem whose hypotheses are supplied by directly established consequences of the positivity assumption, with an explicit earlier mapping. A Fano theorem, a general-point theorem, a toric theorem, a global tangent-positivity theorem, or a large anticanonical line-bundle Seshadri threshold is insufficient on its own.

The stronger mechanism was searched separately: a rational curve exists through x and every rational-curve normalization through x is very free; choose minimum ample degree through x; obtain a proper marked irreducible-curve family; its evaluation covers X; numerical generation gives rho(X)=1 and ampleness of -K_X; invoke the established Fano clause.

## Exact primary-source comparisons

| Source and inspected location | Earlier assumptions/result | Relation to target |
|---|---|---|
| [Fulger–Murayama, final-numbering manuscript](https://par.nsf.gov/servlets/purl/10198624), Corollary 4.6 and Proposition 4.8, p.16; Conjecture 4.9, p.17 | Rational-curve existence at the specified point; Fano case in any characteristic; general-point case in characteristic zero; surface case separately | Original conjecture and imported special cases; no full unrestricted proof. Its [2019 v2](https://arxiv.org/pdf/1903.00610v2) uses Conjecture 5.9. |
| [Fulger, OWR 53/2019](https://ems.press/content/serial-article-files/46833?nt=1), printed p.3289 | Conjecture plus low-dimensional, homogeneous, Fano, and sufficiently general-point cases | Primary contemporaneous formulation. A related author [seminar abstract archived under summer 2018](https://www.iag.uni-hannover.de/oberseminar-alt/oberseminar/abstracts/ss-2018/fulger) also asks the question (page last modified 2020-06-23); do not assert that the question first arose in 2019. |
| [Chang, arXiv 2211.17172v2](https://arxiv.org/pdf/2211.17172v2), pp.1–3 | Smooth projective toric case, any characteristic, any closed point; general statement remains Conjecture 0.1 | Genuine later special case. v1: 2022-11-30; v2: 2025-07-10; journal September 2025, DOI 10.1016/j.jpaa.2025.108046. Singular toric counterexamples explain why smoothness matters. |
| [Achinger–Witaszek–Zdanowicz](https://ems.press/content/serial-article-files/32569?nt=1), Theorem 6.1.4, printed p.2639 | Fano, general x, every curve through x free, and minimal free curves through x very free | Close Mori-type precursor. It retains assumptions absent from the target. |
| [Occhetta–Wiśniewski](https://arxiv.org/pdf/math/0105166v2), unnumbered Mori theorem in “Families of curves”, PDF p.4 | rho=1; minimal dominating family; members through a general point have ample pulled-back tangent | Picard-rank-one/general-point precursor. Does not give the missing rank-one reduction. arXiv v2 2001-05-24; journal 2002. |
| [Kebekus](https://arxiv.org/pdf/math/0107069v1), Theorems 1.1 and 2.1 | Over C, n>=3; anticanonical lower bound for every curve; construction at very general x | Established projective-space characterization. The globally quantified bound and field assumptions are stronger. |
| [Debarre, CIMPA notes](https://www.math.ens.psl.eu/~debarre/CIMPA2015i.pdf), Section 4.3, Theorem 4.12 and s=n remark, printed pp.44–45 | Characteristic zero; degree minimal among free curves; general-point deformation analysis | Useful contextual characterization, not an arbitrary-characteristic specified-point result. |
| [Li–Ou–Yang](https://arxiv.org/pdf/1801.09191v2), Theorem 1.4 and its proof | Over C; tangent globally strictly nef; first derives Fano using nef-tangent structure theory | Distinct stronger global positivity assumption. v2 2018-11-28; journal 2019. |
| [Araujo](https://arxiv.org/pdf/math/0410584v1), Theorems 1.1–1.2 and Proposition 2.2 | Complex uniruled varieties; minimal-family tangent directions at general points; global ample tangent subsheaf in the application | No specified-point/positive-characteristic resolution. v1 2004-10-27; journal 2006. |
| [Druel](https://druel.perso.math.cnrs.fr/textes/projectif.pdf), introduction theorem/corollary, printed pp.19–20 | Characteristic-zero uncountable field; a given rank-one foliation and a line bundle positive on every curve | French alternative terminology checked directly. The foliation/global positivity is extra structure. Published online 2004-08-10. |
| [Fujino–Jovinelly–Lehmann–Riedl](https://arxiv.org/pdf/2602.22192v1), Theorem 1.1/Corollary 1.3 | Over C; full negative extremal ray of anticanonical length > n, or global rational-curve degree condition | Current 2026 characterization; it does not derive its ray condition from positivity at one point. v1 2026-02-25. |

## Standard numerical-generation mechanism and attribution

[Andreatta–Occhetta, Proposition 2.20(b)](https://archive.intlpress.com/site/pub/files/_fulltext/journals/ajm/2005/0009/0004/AJM-2005-0009-0004-a005.pdf), printed p.529, states that properness of the pointed family V_x makes the numerical classes in its locus generated by the family class. The cited chain leads to [Andreatta–Chierici–Occhetta, Lemma 4.1 and Corollary 4.2](https://arxiv.org/pdf/math/0309473v1), PDF p.6, and [Chierici–Occhetta, Corollary 2.1](https://arxiv.org/pdf/math/0401429v2), PDF p.8. The latter is the renumbered current version of the result cited as Corollary 2.23 in the 2005 paper; its arXiv v2 explicitly explains the renumbering.

These statements and their immediate numerical consequence when Locus(V_x)=X are close precursors to candidate Lemma 5. The candidate supplies its own line-bundle descent proof with an actual contracted marking section, so it need not silently extend every older source's characteristic conventions. Nevertheless the principle should be described as the familiar numerical-generation argument for proper pointed families. No inspected source above states the entire arbitrary-point tangent-Seshadri synthesis as an immediate corollary.

Minimal degree, proper pointed rational-curve families, very-free evaluation, and Mori's characterization are likewise established techniques. A sound paper can be novel as an application/synthesis of these tools; it should not claim novelty for each lemma separately.

## Citation and current-literature screening

The ledger records 64 distinct executed queries across exact statements, alternate mechanisms, historical citation chains, and limited French/Japanese terminology. Primary statements, rather than snippets, support the comparisons above. OpenAlex returned 19 FM21 citing entries, including a self entry and duplicated Ulrich-bundle records. Relevant leads were followed to primary texts; other titles were screened only as leads, not treated as evidence that they cannot contain an obscure relevant remark.

[Fulger–Ray](https://arxiv.org/pdf/2303.13201v1) studies base-loci functoriality; its latest available arXiv version is 2023-03-23 despite journal publication in 2025. [Biswas–Hanumanthu–Misra](https://arxiv.org/pdf/2303.15808v2) studies constants of already ample bundles and a tangent-bundle example on already specified P^n. [Matsumura](https://afst.centre-mersenne.org/item/10.5802/afst.1712.pdf) treats pseudo-effective tangent/MRC structure. No full target resolution was identified in these inspected citing texts.

Line-bundle anticanonical thresholds, including Liu–Zhuang and Bauer–Szemberg as discussed directly by FM21 and Chang, do not match tangent-bundle positivity at one point. Secondary catalogs and AI-written web pages were excluded from priority evidence. MathDB's “open” label and absence of posted solutions are not a priority certificate.

## Limits and final recommendations

The official [CMSB DOI](https://doi.org/10.2969/aspm/03510001) redirects to a Project Euclid security check. Full CMSB was not directly inspected there; FM21's exact invocation under characteristic-zero/general-point assumptions was. The [Kollár monograph publisher page](https://link.springer.com/book/10.1007/978-3-662-03276-3) confirms bibliographic identity, but the full monograph was not independently obtained. Fulger–Murayama's *Moving Seshadri constants for vector bundles* remains an in-preparation reference in inspected public bibliographies, with no contents inspected here. Full later journal text of Fulger–Ray was not accessed. Citation indexing and multilingual coverage are incomplete.

Accordingly, this audit supports publication language presenting a proof of FM21 Conjecture 4.9 after mathematical verification, with accurate citations to prior cases and standard methods. It does not support a certified “first-ever” priority claim. No status change to already_solved is justified by the evidence found. Any useful future specialist input is recorded here only; no outreach is prepared or initiated.

The machine verdict is `verdict.json`. Search, evidence, citation-screening, and retrieval manifests make the scope reproducible. PDFs and extracted text under `retrieved/` are research reference material and should not be copied into the public preprint/verification package.
