# Source and prior-attempt gate

**Target:** rank 563, problem 20001587 / AIM-GEOMETRIC_GROUP_THEORY-0096. Checked 4 October 2026 UTC.

## Original question, independent of the generated title

The requested [UnsolvedMath catalogue page](https://www.unsolvedmath.com/problems/20001587) was attempted with the web reader and direct HTTP. The web reader failed; direct HTTP returned 403. The target record was located in an already available local copy of the public [UnsolvedMath dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath). Its identifier and source item match. The generated finite-gluing title, partial-progress label, and research summary were treated as untrusted discovery aids. They are not the original target or proof of a result.

The exact original was then independently retrieved from the live [AIM list, section 2, Problem 2.1](http://aimpl.org/amenablediscrete/2/#2.1). The HTTPS endpoint returned 502 and the web reader failed; the canonical HTTP source returned 200. Its problem record has identifier `ed2f7227f2b11f99ac79c437090b8479`, revision `22-adf6dea1ded8b33815f9097edb032675`, and an empty status field. No posted resolution was present in the retrieved section. The question concerns minimal full Cantor actions and nonamenability of clopen restrictions. It imposes no Hausdorff germ-groupoid hypothesis.

The precise rigid-subgroup meaning is independently explicit in Kate Juschenko's [author book draft](https://metaphor.ethz.ch/x/2017/hs/401-3370-67L/sc/Juschenko.pdf), *Amenability of discrete groups by examples*, Problem C.33, printed p.261. That page was extracted and visually inspected. It defines the restriction by preserving U and acting identically off U. PROOF.md states the intended nonempty-U question and flags the literal empty-set defect without claiming that defect solves the intended problem.

## Complete relevant arguments inspected

1. **Juschenko, book draft**, linked above: Section 2.7, complete proofs of subgroup, quotient, extension and directed-union permanence; Theorem 2.21 and its complete invariant-mean proof; and Problem C.33. These provide elementary background. Our partition-coset argument is written out explicitly, including its well-defined averaging map.

2. **Eduardo Scarparo**, [*A dichotomy for topological full groups*, arXiv:2111.13616v3](https://arxiv.org/abs/2111.13616v3), 11 September 2022; [published DOI](https://doi.org/10.4153/S000843952200056X), Canadian Mathematical Bulletin 66 (2023), 610–616. The full six-page manuscript was read. Proposition 3.1 and Lemma 3.3 already establish the measure-transfer and local-realization mechanisms used here, with a stronger alternating-group conclusion in the latter. These results are credited. Lemma 3.4, Theorem 3.5, Corollary 3.6 and their full proofs concern alternating full groups, confined subgroups, invariant random subgroups and C*-simplicity. The paper does not identify the alternating subgroup with the commutator subgroup in general. We do not import such an identification or claim that its dichotomy resolves the present unrestricted question.

3. **Vadim Alekseev and Martin Finn-Sell**, [*Representation theory of topological full groups of étale groupoids and paradoxicality*](https://doi.org/10.1007/s00233-025-10501-w), Semigroup Forum 110 (2025), 51–77. Definitions 2.7, 2.9 and 4.4, Lemma 4.5 with proof, and the complete Theorem 5.2 proof were checked in the published PDF. The amenability criterion includes amenability of every clopen rigid stabilizer. Replacing that quantifier with one corner, or with atoms of one partition, is not justified. Our proof does not depend on the paper's more technical representation or groupoid-permanence assertions.

4. **Juschenko, Nekrashevych and de la Salle**, [*Extensions of amenable groups by recurrent groupoids*, author manuscript](https://web.ma.utexas.edu/users/juschenko/files/Juschenko-Nekrashevych-Salle.pdf): Proposition 4.4 and its complete proof were read. For rooted-tree automorphisms the decisive finite level partition is invariant under the relevant generators. This is precisely the extra property not available for arbitrary full Cantor actions. We use it as a comparison of mechanisms, not as an unrestricted theorem.

No theorem from an abstract, search snippet or generated catalogue report is used as a proof dependency. The main reductions in PROOF.md have complete elementary proofs, and explicitly credit the pre-existing local/measure arguments.

## Current-source search limits

Searches covered exact question phrases, amenable clopen restrictions, full-group amenability and finite amplification, and the relevant author/publisher records. They located the sources above and no source-verified complete resolution of the unrestricted question. This is a bounded negative search statement, not a certification of worldwide current openness or priority. In particular, no novelty is asserted for Theorem 6's formulation.

A new result on distal actions appeared in current searches, but its abstract alone does not settle arbitrary minimal full actions; it is not imported. Neither general topological amenability of a germ groupoid nor an invariant probability measure is silently identified with amenability of its discrete full group.

## Actual previous-attempt checks

Repository: [AlecKriebel/Math](https://github.com/AlecKriebel/Math).

- The current queue row was read: rank 563, `queued`, `0/5`, with the requested numerical and AIM identifiers.
- All-state PR searches for `20001587`, `GEOMETRIC_GROUP_THEORY-0096`, `amenable clopen`, and `amenablediscrete` found no result. A broader `amenability` query found none. `clopen` returned PR347, a distinct Weihrauch/Ramsey investigation; its description was inspected.
- Default-branch code search for `20001587` returned no result. Because even a queue entry may be absent from code-search results, this was not treated as exhaustive evidence.
- ID-based branch search had no matching branch and no continuation cursor; ID-based commit search had no match.
- The actual root contents were read. The recursive `problems/` tree at `8f72e77ed517ba2424b4e74b324cda525e6373c3` had 652 entries, `truncated=false`, and no target-ID, amenability, clopen or gluing path.
- The actual `unsolved_math_prioritization` tree was inspected, including its attempts subtree `0270c330cecec35524db98be465ebc4d2aa12d24` (54 entries, `truncated=false`). No target attempt was found.
- The queue's actual Git blob is `59dba610d333684751e889818d21f66aba29cec9` in tree `87f87a1dee35388240c13ed30c39a43502c771bd`. The queue text itself begins with an older SHA-looking line; that literal header is not claimed to be the current Git blob.
- Repository AGENTS.md was read at blob `9744d9b0ca61394e2ff9f23a1e6d24af1129a7ff`.

The queued row alone was not used to infer no prior attempt. Successful checks found none; unindexed or untagged work cannot be ruled out. There were no remote writes during this investigation.

## Local-source integrity and publication boundary

SHA-256 hashes of the local reading copies:

- AIM section HTML: `7b9d5e2acc5df496ba9946f3c6936b97505a70fa67275bac4392e21b2ae4ae21`
- Juschenko draft PDF: `5667e2986ae0ab1671a7ece093b34bde6953a5372f93f1e9f60b90bfc763ca12`
- Scarparo v3 PDF: `bd45cdad3fa73f4d6a50918ab294738592cc75c30d920fb4360b8ede495eeb5b`
- Alekseev–Finn-Sell published PDF: `925e4a5bb1bf106378aca9548d2037bc44bb313731e956c7bd5e9ff1672e449e`
- Juschenko–Nekrashevych–de la Salle manuscript PDF: `972ebcf96dcaf14b3e874774bcc8b8bf42c3aafdd22067bc19ca64ca1ef892d2`

Only authored prose, original small code, its output, and integrity metadata are proposed for publication. No source HTML/PDF, extracted book/paper text, screenshot, corpus, raw catalogue record, unrelated repository content or private context belongs to the public packet.

**Gate:** the primary source and intended scope are established. The gate supports a partial-results packet with original disposition `unsolved`, five substantive approaches. It does not support a full-solution label. A separate fresh adversarial review must occur before any remote publication.
