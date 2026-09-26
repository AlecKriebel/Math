# Fresh primary-source, convention, and novelty audit

Checkpoint: **2026-09-26 04:09 UTC / 2026-09-25 21:09 PDT**. Bounded audit completion: **100%**. This is an estimate of completion of the assigned source audit, not a probability of mathematical correctness, priority, or journal acceptance. The initial investigation was independent of earlier local reviews; the 21 September source report was read only afterward, to check for missed leads.

## Verdict

**No novelty blocker or mismatch with Problem 16.45 was found.** The September 2026 official notebook still presents the question without a solution comment. Cameron's 2024 published discussion explicitly leaves the normal-bottom question open. The paper uses the intended all-actions invariant, including nonfaithful and intransitive actions. The claimed strict inequality therefore addresses the stated problem, conditional on the independently reviewed mathematics.

The bounded search did not identify a preceding resolution or an equivalent counterexample. This does not certify absence from all literature, unindexed preprints, private work, or forthcoming publications. Do not claim that the search proves priority. The dates and exact sources provide a defensible statement of the checked record.

## Primary-source findings

### Official problem and status

The [official notebook homepage](https://kourovkanotebookorg.wordpress.com/) links its **1 September 2026** update as the current version. The [21st-edition full PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21tkt.pdf), printed **p.100**, contains Problem **16.45**, attributed to **P. J. Cameron**, in the **16th Issue (2006)** section. The problem maximizes inclusion-minimal base size over every permutation representation and compares it with the largest independent subset. Its equivalent formulation asks whether a largest Boolean meet-semilattice embedding can have normal bottom. There is no solution note attached. The [separate September update](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/21upd.pdf) contains no occurrence of `16.45`.

The notebook's brief first definition alone could tempt an identity-versus-kernel misunderstanding. The equivalent normal-bottom formulation and Cameron's explicit explanations below settle the intended convention. There is no license to restrict to faithful, transitive, primitive, maximal-subgroup, or conjugate-subgroup actions.

### Cameron 2014: exact attribution

[Peter J. Cameron, *Some measures of finite groups related to permutation bases*, arXiv:1408.0968v1](https://arxiv.org/abs/1408.0968), submitted **5 August 2014**, is an unpublished preprint. [Primary full text](https://arxiv.org/html/1408.0968v1).

Section 2 expressly permits nonfaithful representations. Propositions **3.1–3.2** establish the Boolean semilattice descriptions; Proposition **3.2(b)** identifies the bottom with the representation kernel. Corollary **3.3** is the inequality, followed by the unresolved strict-inequality question. Its notation is **b₂** and **μ′**. The manuscript's attribution of these foundational statements is correct. The paper describes itself as already over ten years old when posted: 2014 should not be presented as the first proposal date. Notebook appearance in 2006 is directly supported.

### Cameron 2024: strongest published context

[Peter J. Cameron, *Independence and bases: theme and variations*, **Model Theory 3** (2024), no.2, 417–431](https://doi.org/10.2140/mt.2024.3.417); [publisher PDF](https://msp.org/mt/2024/3-2/mt-v3-n2-p08-s.pdf).

The relevant section is **Section 6 (Finite group parameters)**, printed **pp.428–429**, **Proposition 2(a)–(c)** and the paragraph after its proof. The conventions again allow nonfaithful representations. The independent-set invariant is **μ↑**. The published text leaves necessity of the normal-bottom condition unknown. The existing bibliographic entry is correct. The earlier local audit mistakenly calls this Section 7; the publisher PDF heading is Section 6. Cite the publisher DOI exactly as **10.2140/mt.2024.3.417**. This is a later published account with a different title, not a journal publication of the 2014 title.

### Author's expositions and original question page

[The symmetric group, 7](https://cameroncounts.wordpress.com/2010/07/22/the-symmetric-group-7/), **22 July 2010**, explicitly allows actions that are nonfaithful and nontransitive, using **b₂** and **μ***. [Groups, lattices and bases](https://cameroncounts.wordpress.com/2014/08/06/groups-lattices-and-bases/), **6 August 2014**, restates the normal-bottom question and suggests systematic counterexample search. The visible comments do not announce a solution. [Cameron's archived problem page, Problem 37](https://cameroncounts.github.io/web/QM/oldprob.html), gives the same normal-bottom question. These support the conventions and history, but the notebook and 2024 published account are better principal citations for a compact journal article. The two blogs need not remain in the final bibliography unless cited for a specific historical point.

### Recent base literature: a genuine notation trap

[Marina Anagnostopoulou-Merkouri and Timothy C. Burness, *On the regularity number of a finite group and other base-related invariants*, **J. Lond. Math. Soc. 110** (2024), no.6, e70035](https://doi.org/10.1112/jlms.70035); [author preprint](https://arxiv.org/html/2405.15300v2); [institutional bibliographic record](https://research-information.bris.ac.uk/en/publications/on-the-regularity-number-of-a-finite-group-and-other-base-related/).

Remark **1(c)** defines **b₂** using **faithful** representations; it corresponds to this manuscript's **b_f**, not its **b**. Proposition **2.3** gives a direct witness argument bounding minimal bases by the independence number **σ**. Their regularity number concerns conjugating prescribed core-free subgroups until the intersection is trivial. It does not establish the all-actions equality or give an earlier counterexample found here. The manuscript's distinction is useful, and a short contextual citation would prevent readers from silently importing the newer faithful-only notation. Use the journal's 2024 volume year despite some discovery services showing 2025 indexing dates.

## Related approach families screened

| Family and primary reference | Mechanism and comparison | Status for this result |
| --- | --- | --- |
| [Detomi–Lucchini, *Maximal subgroups of finite soluble groups in general position*, arXiv:1502.06840](https://arxiv.org/html/1502.06840v1) | Compares **MaxDim**, restricted to maximal subgroups, with **m(G)**, restricted to irredundant generating sets of the whole group. Constructs large gaps in that comparison. | Different quantities and restrictions; does not supply the normal-bottom all-subgroup counterexample. |
| [Fernando, *On an Inequality of Dimension-like Invariants for Finite Groups*, arXiv:1502.00360](https://arxiv.org/html/1502.00360v1) | Studies **m(G) ≤ MaxDim(G)** and strict examples. | A gap here does not imply **b(G) < μ′(G)**; no equivalent result identified. |
| [Burness–Garonzi–Lucchini, *Finite groups, minimal bases and the intersection number*, Trans. Lond. Math. Soc.9 (2022),20–55](https://doi.org/10.1112/tlm3.12040) | Intersection number minimizes a maximal-subgroup family reaching the Frattini subgroup; related base number uses minimum base sizes in faithful primitive actions. | Title sounds close; quantifiers and maximal/primitive restrictions differ. No resolution identified. |
| [Lucchini–Moscatiello–Palcoux–Spiga, *Boolean lattices in finite alternating and symmetric groups*, Forum Math. Sigma8 (2020),e55](https://arxiv.org/abs/1911.04516) | Classifies complete Boolean overgroup intervals in symmetric/alternating groups. | Full lattice intervals differ from arbitrary Boolean meet-semilattice embeddings; does not supersede the result. |
| [Lucchini–Stanojkovski, *Independence and strong independence complexes of finite groups*, J. Lond. Math. Soc.113 (2026),no.6,e70605](https://doi.org/10.1112/jlms.70605), [29 May 2026 preprint](https://arxiv.org/html/2503.19778v2) | Resolves a different Cameron question: when independence coincides with strong independence, defined through numbers of generators of overgroups. | Current potentially confusable result checked. Its full text contains no permutation-base treatment or Kourovka16.45 resolution. |

These contextual references should not all be inserted merely to lengthen the bibliography. The paper has a focused, independently readable contribution. Cameron2014/Cameron2024, the official notebook, and optionally Anagnostopoulou-Merkouri–Burness are sufficient to establish the principal setting.

## Independent convention check

This paragraph records our deduction, not a sourced assertion. For an action of X, a base for the permutation image pulls back to common stabilizer ker(ρ) in X. A subgroup family with normal total intersection N gives the required action on the disjoint union of coset spaces, because its kernel is Core_X(N)=N. Conversely, a minimal base yields exactly such an irredundant family. Hence the all-actions invariant is max over normal N of the faithful invariant of X/N. Normality cannot be discarded or repaired by taking individual cores while retaining irredundancy. The proposed counterexample explicitly handles both parts: the faithful bound, and all quotients via the unique minimal normal translation subgroup. This is the actual question's quantifier structure.

## Bounded search trail

Primary-source opens and reads were followed by exact-title, invariant, and explicit-group queries. Representative exact query strings used during this audit were:

- `"Kourovka" "16.45"`; `"Kourovka" "16.45" Cameron`; `Kourovka Notebook Problem 16.45`; `"16.45" "counterexample" "Kourovka"`.
- `"Independence and bases: theme and variations"`; `Some measures finite groups related permutation bases counterexample`.
- `"Boolean" "normal" "Cameron" "base" counterexample`; `"Cameron" "minimal base" "independent subset"`; `"b_2(G)" "mu" "strict" Cameron`.
- `"On the regularity number of a finite group"`; `"Independence and strong independence complexes of finite groups"`.
- `"maximal dimension" "independence" finite groups`; `"MaxDim" "Lucchini" "nilpotent"`; `"On an Inequality of Dimension-like Invariants for Finite Groups"`; `"Boolean lattices in finite alternating and symmetric groups"`.
- `"100920" "base" group`; `"29" "SL(2,5)" "independent"`; `"group" "maximal dimension" "independent" "SL(2,5)"`; `"irredundant" "bases" "Cameron" "Frobenius"`.

Exact problem-number and group-order searches had sparse relevant coverage and many irrelevant results. Domain-constrained problem-number searches of arXiv and Cameron's blog were not stronger evidence. Search snippets were used for discovery only; substantive conclusions above rely on primary documents. No complete citation-index export, subscription MathSciNet search, or exhaustive multilingual review was performed. Some publisher pages were inaccessible or poorly parsed in the browser; the Cameron2024 publisher PDF and official notebook PDFs were downloaded directly and inspected as extracted text. The archived full texts are inspection material, not redistribution material.

## Submission-facing recommendations

1. Preserve the clear **all-actions** definition, with bases taken in the permutation image, and the separate **b_f** notation.
2. Attribute the subgroup/Boolean characterizations directly to Cameron2014, Props.3.1–3.2, and/or Cameron2024, Prop.2.
3. Prefer a compact historical sentence: “Cameron's 2024 account still poses this question, and Problem16.45 remains listed without a solution comment in the September2026 Kourovka Notebook.” This is a dated, checkable statement.
4. If recent context is desired, cite Anagnostopoulou-Merkouri–Burness with its faithful-action convention explicitly identified.
5. Remove an uncited blog2014 bibliography item if the final article no longer uses it. No other factual bibliographic correction to the existing five entries is required.
6. Keep this audit and all full downloaded sources out of the journal's mathematical supplement. The supplement should contain the author's verification artifacts and reproducibility instructions.

No external researcher was contacted, and no outreach was prepared. Ordinary journal peer review remains valuable independent validation; this audit is AI-assisted source checking, not external peer review.

## Source integrity

Local inspection files live only in `sources/novelty/`. Their sizes and SHA-256 hashes are recorded in `sources/novelty/inspection_manifest.json`. Full PDFs, extracted text, and downloaded HTML are ignored by Git in that directory and must not enter the upload archives. Repeated retrieval of the four central PDFs matched the hashes recorded in the earlier source audit, independently confirming that the referenced primary documents had not changed between those inspections.
