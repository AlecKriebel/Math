# Preliminary screen: simple, almost simple, and direct-product scope

Cutoff: 24 October 2026. This is a bounded literature screen, not original research or an independent verification of any cited proof. No mathematical computations were performed. Read the repository AGENTS.md. All work from this screen stays in this folder; raw retrieved material is in `sources/`. No outreach, publication, Git operation, or queue change was performed.

## Target and invariant discipline

The target is Kourovka 21.135: for arbitrary finite groups G,H, equality of the **multisets** of ordinary complex irreducible character degrees, with R(G)=1, should force R(H)=1. Success for a full-solution screen requires a proof or counterexample with precisely these hypotheses; identifying special cases is insufficient.

- A degree **set** forgets multiplicity. Huppert's conjecture concerns that set for a nonabelian simple reference group S, and predicts a comparison group S×A with A abelian. It is not the multiset question as stated.
- A degree **multiset** is the first column of the ordinary character table and is equivalent to the complex group algebra as a complex associative algebra. It is not the full character table. This equivalence is explicitly explained in the introduction of [Bessenrodt–Nguyen–Olsson–Tong-Viet, 2015](https://msp.org/ant/2015/9-3/ant-v9-n3-p.pdf).
- Character **codegrees**, defined using character kernels as well as degrees, are a separate invariant. A codegree recognition theorem must not be promoted to a degree recognition theorem.
- “Semisimple” as a finite group with trivial solvable radical is distinct from semisimplicity of its complex group algebra.

## Established coverage located

| Reference class | Precisely located result | Scope for 21.135 |
|---|---|---|
| Nonabelian simple groups | All such groups are determined among all finite groups by their degree multisets. The classical case is Tong-Viet, J. Algebra 357 (2012), 61–68, [arXiv:1105.4260v2](https://arxiv.org/abs/1105.4260v2); its introduction lists the earlier alternating/sporadic and exceptional cases. | The simple reference cases are already covered, with the stronger conclusion H≅G. Do not present these as new. |
| Quasisimple groups | [Bessenrodt et al., Algebra & Number Theory 9 (2015), 601–628](https://msp.org/ant/2015/9-3/ant-v9-n3-p.pdf), abstract and introduction, complete multiset/complex-algebra recognition of all finite quasisimple groups. | Broader recognition theorem, but a quasisimple group with nontrivial center is outside the radical-free reference hypothesis. |
| Almost simple groups | Complete recognition was **not** located. The Sep. 2026 proposer survey explicitly describes only partial results: symmetric groups; socle PSL2(q); PGU3(q); PSLn(q)<G≤PGLn(q); and certain PSUn(q)<G≤PGUn(q) with the stated restriction on q+1. [Vasil'ev, §3](https://arxiv.org/html/2608.12783v2). | These are established special cases; the general almost-simple recognition question must not be declared solved. |
| All almost simple groups with socle PSL2(p^n) | Heydari–Ahanjideh, Publ. Math. Debrecen 91 (2017), 467–487, Theorem 1.2 and Corollary 1.3: [primary PDF](https://publi.math.unideb.hu/paper/2188/download/10_5486_PMD_2017_7797.pdf). Hypothesis is equality of X1, explicitly degrees counting multiplicities. | Full isomorphism recognition in this family, not merely equality of degree sets. |
| Selected direct powers | Azad–Khosravi, Math. Reports 22(72) (2020), 1–10, Corollary 15: A5^n (n≤5), PSL2(7)^n (n≤7), PSL3(3)^n (n≤13), PSL2(17)^n (n≤17). [Primary PDF](https://imar.ro/journals/Mathematical_Reports/Pdfs/2020/1/1.pdf). | These direct-product reference cases are already recognized by the complex algebra. The exponent restrictions matter. |

The 2020 paper's introduction and references also identify recognition of PSL2(p)×PSL2(p), p≥5 prime (Khosravi et al., J. Algebra Appl. 16 (2017), 1750036), and products of pairwise nonisomorphic Suzuki groups (Azad–Khosravi, J. Algebra Appl. 19 (2020), 2050036, DOI [10.1142/S021949882050036X](https://doi.org/10.1142/S021949882050036X)). These are useful primary bibliography leads; the original proofs were not audited here. It also cites the simple-K3 square result, Mathematics 6 (2018), 107, DOI [10.3390/math6070107](https://doi.org/10.3390/math6070107).

Rashidi–Oftadeh, J. Mahani Math. Res. Cent. 12(1) (2023), 127–135, DOI [10.22103/jmmr.2022.19218.1226](https://doi.org/10.22103/jmmr.2022.19218.1226), advertises recognition of bounded direct powers of a Suzuki group, with a primitive-prime-divisor bound on the exponent. The author-uploaded article was visible via ResearchGate search results; the publisher endpoint was inaccessible here. Treat the exact bound as requiring the original article before reliance. No theorem covering arbitrary direct products of nonabelian simple groups, or arbitrary finite radical-free groups, was located.

## Huppert and recent full-solution false positives

Tong-Viet, [“Huppert's conjecture for finite simple exceptional groups of Lie type”](https://www.sciencedirect.com/science/article/abs/pii/S0021869324006021), J. Algebra 665 (1 March 2025), 48–71, DOI 10.1016/j.jalgebra.2024.10.042, proves the **set** conjecture for every finite simple exceptional group of Lie type. The publisher introduction explicitly says the high-rank classical case remains open. This 2025 completion of the exceptional family is not a complete proof of Huppert's conjecture and is not a full solution of 21.135.

[Alavi–Daneshkhah–Jafari, Rend. Sem. Mat. Univ. Padova 138 (2017), 115–127](https://ems.press/content/serial-article-files/43954), treats **degree sets** of almost simple groups with Mathieu socle. Its result gives an abelian subgroup A with the appropriate quotient, and its examples show that a direct-product version of Huppert's conclusion does not extend to almost simple groups. These examples are not thereby multiset counterexamples to 21.135.

Yong Yang's [arXiv:2609.04702v2](https://arxiv.org/html/2609.04702v2), revised 19 September 2026, claims a full proof of the **codegree-set** isomorphism conjecture for nonabelian finite simple groups (Theorem 1.1). That is a different invariant and a simple reference class. This screen records the claim and its scope; it does not certify the proof or infer any answer to 21.135.

Vasil'ev's [arXiv:2608.12783v2](https://arxiv.org/html/2608.12783v2), 9 September 2026, §3, still explicitly poses the exact multiset/trivial-radical question as Problem 3.9(ii). Its separate Problem 3.9(i) concerns preservation of solvability. This is strong recent status evidence, but not a guarantee that no later solution exists. Targeted searches through the stated cutoff found no later full solution.

## Checkpoint and limits

2026-10-24 17:46 UTC — Bounded assigned screen complete (best guess **100% of this screening subtask**; no percentage claim about solving 21.135). The strongest screen-supported outcome is: simple reference cases and selected almost-simple/direct-product cases are known; general radical preservation was explicitly open in a September 2026 proposer source; no exact later solution was located. Remaining gap: exhaustive literature coverage and proof verification are not supplied by this preliminary screen. All potential outreach remains forbidden and was not prepared.

Search families included exact `21.135`; `solvable radical` with `character degrees`/`group algebra`; `character degree multiset`; `almost simple groups` with `complex group algebras`; `characteristically simple groups` with 2025/2026; `direct powers`, `direct products`, and `semisimple groups` with degree/algebra recognition; and Huppert 2025/2026. Negative search results are search outcomes, not mathematical evidence of nonexistence.

`huppert_scope_source_receipts.json` records retrieval URLs, timestamps, failures, file sizes, and SHA-256 hashes. `sources/huppert_primary_search_receipt.json` is a raw web-tool result rather than an HTTP body, and preserves publisher metadata where direct archival requests failed.
