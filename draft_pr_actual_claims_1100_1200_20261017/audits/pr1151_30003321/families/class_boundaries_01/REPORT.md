# PR1151 / Problem 30003321 — independent class and boundary audit

Completed: 2026-10-18 UTC. Family: `class_boundaries_01`.

**Verdict: ACCEPT the full original mathematical target in NBG with global choice, including set and proper-class groups and the separately handled trivial group.** No candidate counterexample or required correction to its exponent surgery, normalization, or image construction was found. Two literal defects in the cited characterization theorem's proof presentation were found and repaired in full below; the acceptance does not assume those defective lines are valid.

The exact remaining mathematical gap identified by this audit is **none**, relative to the primary paper's earlier normal-form facts, monomial simplicity cuts (Lemma 3.1), and initial-module extension lemma (Lemma 4.1). This is an ordinary mathematical audit, not proof-assistant verification, external peer review, or a priority determination.

## Independence and scope

The original claim and an independent attack plan were sealed at **2026-10-18T00:33:35.041346+00:00**, before the candidate was first read at **2026-10-18T00:33:37.713195+00:00**. The sealed note's SHA-256 is `3af96975713f925da6c129df89a40a9e482244b416ab231542e82def8ccf83b4`.

Before candidate access, I independently identified bottom-only coefficient normalization, failure of naive arithmetic exponent translation at a limit bottom, and exponent reindexing with no new right ancestors as the central mechanism. My preliminary realization used minimum-first simplest cuts. The candidate instead supplies an explicit sign-sequence map, avoiding the prospective class-recursion issue. The independent finite cut construction agrees with that explicit map in every tested finite case.

Only `/Users/alec/Documents/Math/AGENTS.md`, the specified candidate `inputs/PROOF.md`, the two named primary originals, arXiv metadata corroboration, and this family's own artifacts were read. No old audit report, acceptance file, root/sibling verdict, PR state, or Git index was accessed. The candidate embeds prior-audit claims; they were disregarded as evidence. No other researchers or shard agents were contacted. Coordination was only with the parent task. All work and downloads remain in this assigned folder; downloaded third-party bodies/extracts are under ignored `private/`.

The candidate pin is 11,530 bytes, SHA-256 `3eb600a03878d62c9e2e6f4b6c641af169bb4551fec699c63932ca980bfedf2e`. The receipt pins all read evidence files and all own artifacts.

## Target reconstructed from the originals

Kaplan–Ehrlich's workshop contribution asks Question 1 on printed p.3356. Ehrlich–Kaplan II repeats the same question as Question 9.1. Its introduction explicitly uses NBG with global choice and uses “class” to include sets and proper classes. The claim is about an order-preserving additive bijection **onto** a subgroup of Oz whose inherited simplicity tree is initial. The source's motivating example D+Z/omega already shows why literal original containment in Oz is too strong.

The audited claim is neither the known discrete-initial-subdomain result nor an assertion about arbitrary discrete ordered groups. It assumes an initial embedding G subset No and concludes the existence of a new initial copy in Oz. It requires no multiplication and no preservation of the original simplicity order. The original paper defines discreteness for nontrivial groups by a least positive member; the candidate's identity map on {0} correctly supplies the requested additional trivial case.

Primary dependencies match their uses: normal forms and the ordered Hahn-group isomorphism in Proposition 3.3; initial real coefficient groups in Lemma 5.1; the additive subgroup characterization in Theorem 5.1; and the nonnegative-exponent/integral-constant characterization of Oz in Section 6.2. The author manuscript labels the adjacent subdomain theorem 6.2; the sealed preliminary note's mention of 6.3 was a numbering slip, corrected in the research log. The candidate cites Section 6.2 and is unaffected.

## Candidate checks and strongest attacks

| Candidate step | Adversarial pressure | Verified disposition |
|---|---|---|
| Lemma 1, lines 28–34 | Least positive could have an infinite or negative tail; exponent infimum might be absent; bottom lattice might be nondyadic | Any nonzero tail has absolute value below half the leading term and hence below g. A smaller cross-sectional exponent contradicts least positivity. The actual minimum is all minus and the coefficient group is exactly 2^{-n}Z. |
| Lemma 2, lines 43–63 | Ordinal concatenation, alpha=0, successor/limit/uncountable alpha, missing prefix at a limit | The map operates on ordered sums, not arithmetic subtraction of lengths. Its exact prefix identity lists every initial segment and treats the empty tail endpoint correctly. It works for every set ordinal. |
| Right-predecessor implication | Reindexing could silently impose new D-divisibility conditions | Away from the old minimum, proper prefixes are preserved and reflected. The only new root is least and therefore a left predecessor. No new right obligation occurs. |
| Bottom normalization, lines 67–81 | Scaling all coefficients could destroy an upper lattice's cross section; one-term coefficient groups might not control arbitrary constants | Only the bottom coordinate is scaled. Exact one-term groups are Z at zero and unchanged elsewhere. Adjacent-truncation subtraction proves every actual coefficient lies in its one-term group. |
| Supports and addition, lines 69–73 | Proper-class exponent domains might introduce proper-class supports, require completion, or lose group closure | Every input support is set-sized and is relabeled without new terms. Class replacement gives a set image of identical order type. Addition uses only the set union of two supports and fixed coordinate factors. |
| Onto and initiality, lines 73–83 | Merely finding an embedding into Oz would weaken the target | H is exactly T[G], T is injective/order preserving/additive, and the five characterization conditions hold for that exact H. The result is initial in No, hence also in Oz. |
| Class bookkeeping, line 87 | Hidden elementary transfinite recursion, proper-class cuts, inverse choices, or class quantification | f is elementary from a set parameter alpha; T uses established normal-form class maps and class replacement on sets. H and the inverse graph use elementary class comprehension. No new class recursion or choice of preimages is needed. |

`CLASS_BOUNDARY_DERIVATIONS.md` provides complete derivations, including an explicit inverse for f on the whole ray [-alpha,infinity). It proves that the most expansive legal proper-class group, with exponents that entire ray, bottom coefficients 2^{-n}Z and all upper coefficients R, maps onto **all of Oz**. It also verifies non-full proper-class finite-support groups, selected infinite-support groups, discrete upper coefficient groups, alpha=0, and arbitrary limit/successor ordinals. Thus no assumption of Hahn completion is hidden in the general argument.

A direct scalar normalization and arithmetic exponent translation were independently falsified as proof routes: with minimum -omega, translating {-beta:beta<=omega} by omega gives a noninitial exponent set containing omega while omitting 1. The candidate's sign map avoids that failure. Scaling every coefficient can destroy cross sectionality in Z omega+2^{-n}Z; the candidate correctly scales only the constant coordinate.

## Characterization dependency: detected defects and complete repair

This matters because treating the source theorem as an unexplained black box would leave a misleading impression of what was independently checked. The defects concern the proof presentation; they do not supply a counterexample to the theorem's statement.

1. **Displayed exhaustion loses cofinal supports.** For Gamma={0} union {2^{-n}:n<omega}, R_0=Z and R_{2^{-n}}=D, take the full series group with those coordinate groups. In its birthday-respecting exponent enumeration, beta=omega and each earlier exponent segment is finite. The legal series sum_n omega^{2^{-n}} lies in no displayed A_i, so the source's equality A=union_{i<beta}A_i is literally false.
2. **Dyadic cut options need not be in the group.** Let q_n have signs + -^n and let the leaf p_n have signs + -^n +. Take the initial exponent set {0} union {q_n,p_n:n<omega}, with R_0=Z, R_{q_n}=D and R_{p_n}=Z. Leaves are prefix-incomparable, so these coefficient groups satisfy all right-predecessor conditions. The legal limit-support series b=sum_n omega^{p_n} has a published dyadic cut option (1/2)omega^2, absent from the group because p_0=2 is a leaf with integer coefficients.

`DEPENDENCY_REFORMULATION.md` repairs both points rigorously:

- Build the initial finite-support subgroup by processing exponents in birthday order and coefficients in real birthday order. Every needed monomial cut option is present by the stated right condition and primary Lemma 3.1. The exact whole-subgroup partition cut is then checked before applying Lemma 4.1.
- Add a **terminal stage containing every existing normalized infinite-limit-support generator**, ordered by support length. All of its proper truncations were generated earlier. This includes cofinal supports, and the generator argument proves the final group equals the original A, without adding a missing series.
- Use perturbations r_mu±1. They are in the coordinate group. Later support positions put these unit options strictly inside any given dyadic perturbation, while dyadic options at the same position lie inside unit options. Thus the left families are mutually cofinal and the right families mutually coinitial, and the same simplest surreal is defined. This proves both option membership and the exact partition-cut hypothesis of Lemma 4.1.
- For an arbitrary proper-class instance and a single actual support S, take its set-sized initial prefix closure I. The *actual restricted subgroup* A_I is a set subgroup of the set Hahn group over I, inherits truncation closure, all cross sections, the exact coefficient groups, and every right-predecessor constraint. The repaired set theorem makes A_I initial. Since it contains the chosen element, every prefix of that element is in A. This proves class initiality without any class-valued recursion.

The characterization used by the candidate is therefore supported by a complete set/class repair from strictly earlier primary inputs. It is not replaced by an equivalent or stronger unsupported assertion. These repairs do not require a change to the candidate's new mathematical construction.

## Reproducible finite falsification evidence

`finite_boundary_check.py` and its JSON result check all finite sign sequences through birthday 8 for each minimum length 0–8. Results:

- 4,097 domain nodes across nine cases;
- 1,923,413 ordered node pairs, with order and right-predecessor checks;
- every proper-prefix set and inverse;
- all 4,097 images match the independently conceived minimum-first simplest-cut realization;
- 2,700 reproducible dyadic coefficient trials check addition, sign, and inverse normalization.

All pass. This computation is evidence only for the finite instances; the proofs of transfinite and class statements are in the derivation notes.

## Reading and source authentication limits

The two primary PDFs were retrieved directly from the specified public URLs at 2026-10-18T00:32:50Z. The workshop PDF is 549,068 bytes, SHA-256 `9ea0da30509d91cbc92467f7eb7d9c82d64b24320c52effd2f49be31fde9af4f`. The author manuscript is 351,864 bytes, SHA-256 `c6d91a1850514736d88c576cafe1f4cedf1e3dcb84a2a96418648cd4fc1a5160`. Extract hashes and retrieval metadata are pinned separately.

Reading scope: workshop Kaplan–Ehrlich contribution and relevant question/normal-form excerpts; author manuscript's NBG convention, tree/sign and normal-form preliminaries, Lemmas 3.1, 4.1 and 5.1, the complete Theorem 5.1 proof, Proposition 5.2, Section 6.2 and Question 9.1, plus displayed surrounding text. arXiv metadata corroborates the title/authors and 2015 submission. No publisher PDF was separately authenticated, and no priority search was performed. This audit does not certify the candidate's historical search claim or prior-review assertions.

## Final completion checkpoint

**100% of this assigned adversarial audit completed.** The strongest verified result is the complete original target, with no known remaining mathematical gap under the stated primary inputs and NBG/global-choice theory. No PR, Git, publication, release, or outside communication action was taken by this shard.
