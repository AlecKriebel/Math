# Exact target, literature and prior-attempt gate

Problem **30003786 / OWR-16160-016**, queue rank **440**. Checks performed on **2026-10-03 UTC**.

## Original question and scope

Alain Valette, “Diameters in box spaces,” in *Mini-Workshop: Superexpanders and Their Coarse Geometry*, Oberwolfach Report **19/2018**, printed pp.1150–1151. The target paragraph is on printed **p.1151**, PDF page **35** (zero-based page 34).

- DOI: https://doi.org/10.4171/OWR/2018/19
- Original report: https://ems.press/content/serial-article-files/46739

The report's workshop dates are **15–21 April 2018**. The imported catalogue's citation includes “(2019)”; the original report, its DOI and workshop date identify 2018.

The paragraph defines congruence subgroups for a group embedded in SL_N(Z) by intersection with ambient congruence subgroups, then asks whether that notion depends on the embedding. It does **not** require an algebraic extension, irreducibility, Zariski density in the entire ambient SL_N, or fixed connected Zariski closure. Our counterexample keeps both N = 7 and the coefficient ring Z fixed. It changes the family itself, not merely which modulus describes an unchanged subgroup.

The nearby comparison to branch-group actions and subsequent semidirect-product box-space results are different statements.

## Exact site and permitted catalogue fallback

The live URL https://www.unsolvedmath.com/problems/30003786 was attempted first and returned inaccessible through the web reader. The immutable fallback was the public ulamai/UnsolvedMath revision **37e53eabe540fb458758e198be61634bd02ee008**:

- `problems.json`, recomputed SHA-256 **04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf**
- `research_results.json`, recomputed SHA-256 **8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b**

The exact numeric-ID entry and OWR code match this question. Its August 2026 literature triage says open, but is not itself mathematical evidence. The complete research-results mapping has no key matching the numeric ID or OWR code and no value containing the numeric ID or exact title. Full corpus files are not included in this packet.

## Primary and scholarly literature checks

1. **Classical free matrix group.** The matrices A = [[1,2],[0,1]] and B = [[1,0],[2,1]] are the classical Sanov free generators. I. N. Sanov, *A property of a representation of a free group*, Doklady Akad. Nauk SSSR (N.S.) **57** (1947), 657–659. The original Russian paper was not directly inspected; its citation and the classical attribution are confirmed in the primary research paper by Chang–Jennings–Ree, *On Certain Pairs of Matrices which Generate Free Groups*, Canadian Journal of Mathematics **10** (1958), 279–284, https://doi.org/10.4153/CJM-1958-029-2 . Attempt 1 supplies its own full ping-pong proof, so it does not depend on an uninspected theorem.

2. **Algebraic-embedding invariance.** A. Lubotzky and T. N. Venkataramana, *The congruence topology, Grothendieck duality and thin groups*, https://arxiv.org/abs/1709.06179 , and the author's manuscript https://www.ma.huji.ac.il/~alexlub/PAPERS/The%20congruence%20topology%2C%20Grothendieck%20duality%20and%20thin%20groups.pdf . The setting distinguishes a fixed algebraic group and algebraic morphisms from arbitrary abstract representations. Its conclusions do not assert equality of congruence families for arbitrary abstract embeddings of a free group. This is an important scope distinction, not a contradiction of the elementary example.

3. **A specialized later positive theorem.** L. Hayez, T. Kaiser and A. Valette, *On arithmetic properties of solvable Baumslag–Solitar groups*, Journal of Group Theory **26** (2023), 623–644, https://doi.org/10.1515/jgth-2021-0069 , author manuscript https://arxiv.org/abs/2101.04999 . Theorem 1.7 proves a congruence subgroup property for embeddings of BS(1,m) into upper triangular matrices over Z[1/m]. Proposition 1.8 addresses algebraic-isomorphism realizations. These restricted positive results do not settle the unrestricted free-group question considered here.

4. **Older relevant rigidity.** R. A. Kucharczyk, *Modular embeddings and rigidity for Fuchsian groups*, Acta Arithmetica **169** (2015), 77–100, https://doi.org/10.4064/aa169-1-5 , https://arxiv.org/abs/1408.3024 . Theorem A states that a congruence-preserving abstract isomorphism between the specified semiarithmetic lattices must come from real projective conjugation. This is relevant prior literature on the dependence question. A transfer to an explicit integral example would need its hypotheses and the chosen abstract isomorphism checked; it is not used as the proof of the present certificate, and no claim is made that the general negative phenomenon is new.

5. **A 2026 scope check.** S. Mao, *Isogenies and congruence subgroups*, Journal of Algebra **691** (2026), 781–810, https://doi.org/10.1016/j.jalgebra.2025.12.001 . The accessible publisher abstract/introduction concerns isogenies and morphisms of linear algebraic groups over number fields. It does not state invariance under arbitrary abstract-group embeddings. The full paper was not inspected.

Searches included the exact question/title, “congruence topology,” embedding choice, finite quotients, direct sums, Valette, counterexamples, and 2025–2026 updates. No earlier explicit statement of the same SL_7(Z) construction was located in this bounded search. This does not establish first priority, originality, or that the broad negative answer was previously unknown.

## Alec prior-attempt gate

The live main-branch file https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md has rank 440 queued at **0/5**, blob SHA **42d850b073e3f3a5adf8303e985a0933260efa51** at the check.

The complete recursive `unsolved_math_prioritization` tree at SHA **cc37a9319691521a4c363ecf97e0d18a9ec9336f** contains **9,376 entries**, with `truncated=false`. There is no attempt folder matching this numeric ID or OWR code. Root folder inventory and complete `problems` (315 entries) and `reports` (4 entries) subtree listings have no corresponding attempt. Existing matrix-congruence test files under a different target concern a different meaning of congruence.

The main `history.jsonl` has no ID/code/congruence match. GitHub code, branch, commit and all-state PR searches for the numeric ID and the relevant title/code found no substantive prior attempt; broader “congruence” PR hits concern unrelated matrix/billiard questions. `review_v2/related_target_groups.json` contains no related group for this target. Imported catalogue entries and dated literature assessments were not treated as Alec's proof attempts.

**Gate result:** no previous substantive Alec attempt located; permitted to investigate. The self-contained explicit construction is recorded as **author attempt 1/5**, not as a novel historical discovery. Mathematical completion and publication status remain subject to the independent audit.
