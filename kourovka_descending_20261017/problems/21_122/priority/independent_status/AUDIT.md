# Independent challenge to the eligibility of 21.122

Date: 2026-10-24 UTC. Role: independent literature and scope check only.
Research completion estimate: 0%; this is preparation, not a solution attempt.
This bounded source audit is complete. No external communication occurred.

## Finding

No complete prior proof or counterexample to the arbitrary-word, arbitrary-profinite-group **set** dichotomy was located. This supports provisional eligibility; it does not prove that no solution exists. The parent is independently checking the latest official problem and solution notices. This note does not determine the top-level status.

The target is

\[
 |G_w|<2^{\aleph_0}\quad\Longrightarrow\quad |G_w|<\infty,
 \qquad G_w=\{w(g_1,\ldots,g_k):g_i\in G\}.
\]

It does not ask that the closed verbal subgroup \(w(G)\) be finite. An open-status assertion about strong conciseness alone therefore cannot certify that this weaker question is open. Likewise, countability-only, finite-generation, linearity, metrizability, or solvability restrictions must not be removed.

## The most relevant current results, with scope retained

1. **Shumyatsky, arXiv:2401.15707v2 (22 February 2024), Theorem 1.1 and Proposition 3.1.** For every word and every profinite group, the small-value hypothesis implies \(w(w(G))\) is finite. Every word is strongly concise in profinite groups whose FC-centre is dense. The proof establishes that \(w(G)\) is FC-generated and applies the latter result **inside \(w(G)\)**. This yields the iterated verbal subgroup, rather than finiteness of the original value set. Neither the theorem's conclusion nor its published proof asserts the desired set dichotomy in full generality. Applying Proposition 3.1 to the original \(G\) requires a further hypothesis. [Primary text](https://arxiv.org/html/2401.15707v2).

2. **de las Heras–Zozaya, arXiv:2502.07427v1 (11 February 2025), Theorem 1.1.** The desired set implication holds for any profinite group containing a **dense equationally Noetherian subgroup**. Corollaries cover profinite linear groups and specified pro-formation completions; Theorem 1.4 separately covers a dense virtually abelian-by-polycyclic subgroup. The hypothesis is not deleted in the article. Its Questions 1.6 and 1.7 explicitly delimit stronger-conciseness cases beyond its techniques, although these questions by themselves are not evidence that the weaker set question remains open. [Primary text](https://arxiv.org/html/2502.07427v1).

3. **Zozaya, arXiv:2608.02237v1 (3 August 2026), Theorem 1.1.** Every word is strongly concise for arbitrary profinite **metabelian** groups. The introduction distinguishes its method from the earlier dense-subgroup results. Proposition 4.1 gives a finite-or-continuum image statement for polynomial maps. Example 4.3 warns that general metabelian word maps need not be polynomial; Theorem 4.4 handles central-valued commutator maps in metabelian groups. Thus a claim that Proposition 4.1 immediately settles arbitrary word maps on arbitrary profinite groups would remove necessary hypotheses. This is a substantial current partial result, not a complete prior solution of 21.122. [Primary text](https://arxiv.org/html/2608.02237v1).

4. **Detomi–Klopsch–Shumyatsky (2020), Theorems 1.1 and 1.2.** Strong conciseness holds for every multilinear commutator on every profinite group, and for every word on nilpotent profinite groups. Specific power and Engel-type words are also treated. These are stronger conclusions on restricted words or groups. Their Proposition 2.1 is a topological image lemma for **nowhere locally constant** maps; it does not assert finite image for every continuous map between profinite spaces. [Publisher](https://doi.org/10.1112/jlms.12342), [author repository](https://www.research.unipd.it/handle/11577/3344010).

5. **Khukhro–Shumyatsky, arXiv:2108.11789v1 (25 August 2021).** The abstract explicitly restricts strong conciseness of all Engel words to **finitely generated profinite groups**. Do not silently promote this to arbitrary profinite groups. [Primary abstract](https://arxiv.org/abs/2108.11789).

6. **Conte–Petschick, Monatshefte für Mathematik 209 (2026), 215–240, current corrected version of record.** Examined as a possible general definability shortcut. Its compact-Hausdorff results concern openness and conciseness of **negative formulae** (Theorem 1.4 and Section 5); ordinary word-value formulae are existential positive formulae. This paper does not state a general finite-or-continuum theorem for word-value sets. [Version of record](https://doi.org/10.1007/s00605-025-02127-5).

## Direct weaker-open-status lead, and its access limitation

Matteo Pintonello's *On Conciseness and Profinite RAAGs*, December 2023 thesis, introduction page 2, explicitly distinguishes the conjecture that a word-value set of cardinality below continuum is finite from ordinary conciseness, and describes their combination as strong conciseness. The primary-source search index exposes this paragraph and calls the former an open problem. The university record confirms the thesis title, author, and December 2023 defence. This is more directly relevant than a bare open-status statement for strong conciseness.

However, fresh retrieval of the thesis PDF on both `.es` and `.eus` hosts returned 404; the university record also intermittently returned 503/reset. This lead was inspected through the search index, **not authenticated from a freshly downloaded full text**. Treat it as corroboration requiring fresh full-text recovery, not the sole basis of eligibility or a 2026 status certificate. The parent's current official Notebook check is the stronger contemporaneous source.

[University record](https://ekoizpen-zientifikoa.ehu.eus/documentos/6748c207f21b355a807aaeeb), [repository handle](https://hdl.handle.net/10810/66909), [indexed PDF](https://addi.ehu.es/bitstream/handle/10810/66909/Tesis_Matteo_Pintonello.pdf?isAllowed=y&sequence=1).

## Search coverage and limits

Searched exact problem number; finite/continuum, small-cardinality, countable-word-value and strong-conciseness formulations; arbitrary profinite groups versus restricted classes; current 2025–2026 preprints; and follow-up references in the current metabelian and equational-Noetherian papers. Search engines located no complete resolution of the exact target. Aggregator status labels were not used as proof. No unverified Lean or repository result was treated as a theorem.

Direct zbMATH and MathSciNet searches were inaccessible through the browser tool; domain-limited web searches returned no useful matching primary record. Thus this is not a claim to have exhaustively searched those databases. Four full primary HTML texts are locally cached with cryptographic hashes; fresh retrieval of two thesis resources failed and is recorded in the manifest. No claim of originality, solved status, publication readiness, or independent human review is made.
