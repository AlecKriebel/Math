# Independent adversarial audit: amenable clopen restrictions

Problem 20001587 / AIM-GEOMETRIC_GROUP_THEORY-0096, rank 563. Reviewed 4 October 2026 UTC.

## Verdict

**PASS AS AN UNSOLVED PARTIAL-RESULTS PACKET.** No blocking mathematical error was found in the frozen proof. The original question remains unresolved by this investigation. The documented five approaches support the proposed disposition **unsolved, 5/5**, not a complete solution or a counterexample under the original hypotheses.

The strongest result is an exact equivalence between the universal clopen-restriction question and amenability preservation by binary finite amplification. That equivalence is proved; binary stability itself is not. The local transport, measure extension, amenable partition stabilizers, and countable reduction are valid at the stated scope. The two boundary examples each omit a different original hypothesis and are correctly labeled.

This is a separate AI-assisted mathematical review, not human peer review or formal proof certification. It does not certify worldwide openness, historical novelty, publication, or any remote repository state. No change to the frozen eight-file packet was necessary or made.

## 1. Identity, freeze, and source scope

The review is bound to these SHA-256 anchors:

- FROZEN_MANIFEST.json: `e16f3738e152a328cb77dfb8fefdf59edfc96c87f0bfcd2268867d5835a24cc7`
- PROOF.md: `089a1cc0d5ac99fd7d66a9148b38cfb3cf2a727daf9a7742794368d52dd796cf`

All seven entries in the frozen manifest match their recorded byte counts and hashes. The manifest itself is the eighth file. The six checks in SHA256SUMS also pass. The executable verifier was inspected before replay.

The [AIM primary section](http://aimpl.org/amenablediscrete/2/#2.1) was freshly retrieved by HTTP with status 200. Its bytes match the recorded source hash. The target record remains `ed2f7227f2b11f99ac79c437090b8479`, revision `22-adf6dea1ded8b33815f9097edb032675`, with an empty status field. An empty field does not certify current openness. The question concerns a minimal Cantor action whose acting homeomorphism group equals its topological full group.

The precise meaning of restriction was checked in [Juschenko's author draft](https://metaphor.ethz.ch/x/2017/hs/401-3370-67L/sc/Juschenko.pdf), Problem C.33, printed page 261, including visual inspection. It is the subgroup supported inside U, rather than arbitrary restrictions of elements that might move U out of itself. The faithful restriction to U is equivalent to that rigid subgroup. The draft's complete elementary permanence arguments in Section 2.7 and invariant-mean argument in Theorem 2.21 were also read.

The intended exclusion of the empty clopen set is explicit in the packet. The literal empty-set defect is not presented as a solution. U equal to the whole Cantor space is the tautological case. No countability, freeness, topological freeness, or Hausdorff germ-groupoid assumption is silently inserted into the original universal assertion.

The generated catalogue title and research summary play no role in the proof. The reported prior-attempt search remains a bounded search, not an exhaustive claim that no unindexed work exists. Recorded repository-search evidence and the proposed two-cell queue change were inspected; this audit did not repeat or modify remote repository operations.

## 2. Claim-by-claim adversarial review

### Lemma 1: local realization, including isotropy

The moving-point case is a valid transposition supported on V union gV after shrinking to make these sets disjoint. Each local label is an element of G, and fullness places the resulting homeomorphism in the rigid subgroup.

The fixed-point case is essential and is correctly covered. Minimality provides a point kx in U distinct from x. Because kx differs from both x and gx, the neighborhood V can be shrunk so that kV is disjoint from V union gV. The first swap sends V to kV; the second sends kV to gV by gk inverse. Their composition equals g on V, even when V and gV overlap and even when the germ of g at x is nontrivial. Neither swap requires V and gV themselves to be disjoint.

A partial map with endpoints inside U can therefore be refined into finitely many local rigid-subgroup labels. Compactness and zero-dimensionality justify the finite clopen refinement. This is a local realization statement, not an unsupported extension of an arbitrary partial map as one globally defined group element. The proofs that the restricted action is minimal and full then follow exactly as stated.

### Lemma 2 and the partial-compression observation

Minimality produces local transports into U, and compactness of its complement produces finitely many of them. Disjointifying a finite clopen cover keeps each atom inside an original transport domain. Adjoining U with identity transport is legitimate, including when the complement is empty.

Conjugation by a transport embeds each atom's rigid subgroup in the U-corner. Passing to smaller clopen subsets gives the claimed neighborhood basis. For a partial compression, the conjugated transformation preserves the image clopen set, so identity extension is a homeomorphism; its local labels belong to G by composition and inversion. This does not require a global extension of the compression itself.

The transport images can overlap. The packet never asserts that they are disjoint inside U, and it does not conclude that all of G embeds into G_U by these transports alone.

### Proposition 3: invariant measures

A left-invariant mean on the discrete amenable group H gives a positive, unital functional on C(U) by averaging an orbit, hence a Borel probability by Riesz representation. This step needs no countability assumption.

The passage from H-invariance to invariance under the restricted local pseudogroup uses Lemma 1 and finite clopen additivity. The argument also works on Borel subsets of the partition pieces. It is therefore valid when U is not G-invariant.

The extension formula defines a finite measure on X despite overlapping transported ranges: the summands are assigned to disjoint source atoms. For invariance under g, the two-index partition A_i intersection g inverse A_j is the correct refinement. Its transport comparison t_j g t_i inverse lies entirely inside U at both ends. Summing the partial-invariance equalities proves G-invariance without assuming it in advance.

The distinguished U atom gives restriction exactly equal to the prescribed probability and total mass between 1 and m. Uniqueness follows by transporting each source atom into U. Normalized restriction is consequently a bijection, with normalization depending on the measure; no affine property is used. Minimality yields full support, and infinite orbits rule out atoms.

An invariant probability on X is not promoted to a left-invariant mean on G. The packet preserves this crucial distinction.

### Proposition 4: partition stabilizers and coamenability

The product decomposition of the atomwise stabilizer uses fullness in a valid way: each restriction of an element preserving an atom can be extended by identity outside that atom. Conversely, products of rigid elements have disjoint supports and yield a faithful product map. The setwise stabilizer has finite permutation quotient, so amenability follows from subgroup, product, and extension permanence.

The stabilizer of the unordered partition is L_P, and its orbit is G/L_P. In the averaging formula, replacing representative g by g l_0 replaces the function on L_P by left translation of its argument; a left-invariant mean therefore gives the same value. The construction is equivariant under left translation by G, positive, and unital. Composing it with an invariant mean on G/L_P correctly proves G amenable.

This proves an equivalence conditional on an invariant mean on the partition orbit. Such a mean is not constructed from the invariant probability on X. Nor is L_P asserted to have finite index in G: only L_P/K_P is finite. A partition giving finitely many local descriptions of generators need not be invariant under those generators. The conditional invariant-partition criterion is sound, and the obstruction to applying it universally remains exposed.

### Proposition 5: the finite-amplification embedding

Each transported atom receives its own layer. This makes the map from X into the union Z of labeled image atoms injective even if their projections onto U overlap. Z is clopen, and conjugation on Z followed by identity off Z defines an injective homomorphism on the entire group, rather than unrelated choices for generators.

On a transition from source atom i to target atom j, the base-coordinate map t_j g t_i inverse is a partial G-map inside U. Lemma 1 supplies local H-labels; arbitrary changes of the finite layer index are available from the symmetric group. Thus the resulting map belongs to Amp_m(H).

The proof establishes membership in the topological full closure of the product action. It does not incorrectly establish membership in the product acting group itself, an abstract finite wreath product, or H alone.

### Theorem 6: exact binary equivalence

The amplification is a full minimal group on a Cantor space. Its rigid subgroup supported on the first layer is exactly H: one inclusion follows from the fullness of H, and the other from identity extension on the other layers. This proves Q implies B with the original hypotheses intact.

The associativity identity is correct after the indicated coordinate identification. In one direction, local maps supplied by Amp_a(H) are further refined into local H-maps. Compactness keeps the resulting labeling finite. In the other direction, a prescribed inner-layer transition is realized by an element of H times Sym(a), and the outer transition by Sym(b). The identity concerns full closures on the same layered space.

Repeated binary amplification is allowed because fullness and minimality are preserved at every stage. Extension by identity on surplus layers embeds the n-layer group into a sufficiently large power-of-two-layer group. Consequently B implies F. Proposition 5 and subgroup permanence give F implies Q. No amenability-preservation statement about arbitrary topological full closure is smuggled into these implications.

Theorem 6 is therefore an exact reformulation. A proof of B, or an amenable full minimal H with nonamenable Amp_2(H), is still needed to answer the original problem.

### Proposition 7: countable reduction

The nonamenability witness can be chosen finitely generated because amenability is preserved under directed unions. Finite translate covers of a countable clopen basis then add only countably many elements. Their inverses ensure that every point's orbit meets every basis member, proving minimality of the generated subgroup L.

A compact metrizable zero-dimensional space has countably many clopen sets: each is a finite union from a countable basis. There are consequently only countably many finite clopen partitions and L-labelings, so [[L]] is countable. Idempotence of local closure makes it full, containment in G follows from fullness of G, and its U-corner is a subgroup of the original amenable corner. The finite nonamenable witness survives. No conclusion about Hausdorffness of the resulting germ groupoid follows or is claimed.

### Boundary examples

For each finite free-group ball, completion of the generator partial bijections to permutations is possible because unused domain and range have equal cardinality. Their inverses also agree with the corresponding inverse letters whenever both endpoints remain in the ball. Evaluation of a reduced word at the empty word follows suffixes of length at most the radius. Thus every nontrivial word is separated in some finite coordinate, yielding the faithful dense embedding used in the construction.

The closure is an infinite compact metrizable zero-dimensional group. An isolated point would make the group discrete and compact, hence finite, a contradiction. Dense left translations are minimal and free, so proper rigid stabilizers of that acting F_2 are trivial. A nontrivial local swap with a nonempty fixed complement proves that the acting group is not full. The defect is explicitly acknowledged.

In the second example, local G-maps cannot cross the invariant components and fix the second component pointwise. Fullness on the first component therefore proves fullness of their disjoint-union action. The first component retains the nonamenable free subgroup and the second has a trivial rigid subgroup, but the action is not minimal. Neither example contradicts the original assertion.

## 3. Literature comparison and unimported hypotheses

The complete six-page [Scarparo v3 manuscript](https://arxiv.org/abs/2111.13616v3) was read, including Proposition 3.1, Lemmas 3.3 and 3.4, Theorem 3.5, and Corollary 3.6 with proofs. Fresh PDF retrieval matches the recorded hash. The packet properly credits the measure-transfer mechanism and the stronger alternating-group local-realization lemma. Scarparo's dichotomy uses the alternating full group and C*-simplicity; its general conclusion does not identify that alternating group with the whole derived subgroup. The additional equality in the corollary is conditional. Those distinctions prevent a direct completion of Q from this source.

Definitions 2.7, 2.9 and 4.4, Lemma 4.5 and its proof, and the complete Theorem 5.2 proof in [Alekseev and Finn-Sell](https://doi.org/10.1007/s00233-025-10501-w) were inspected. The amenability criterion requires every relevant clopen rigid stabilizer to be amenable, alongside its other hypotheses. A single corner or the atoms of one finite partition do not supply that quantifier. The packet does not depend on technical groupoid or representation-theoretic assertions from this paper.

The complete proof of Proposition 4.4 in [Juschenko, Nekrashevych and de la Salle](https://web.ma.utexas.edu/users/juschenko/files/Juschenko-Nekrashevych-Salle.pdf) was read. Rooted-tree automorphisms preserve a common finite level partition after the local descriptions are sufficiently refined. That structural property is the decisive extra ingredient in its finite-extension argument and is not available for arbitrary Cantor homeomorphisms.

Targeted fresh searches found no source-verified complete resolution of the unrestricted question. The distal-action result encountered in current searches has additional dynamical assumptions. This limited search does not establish a global current-open status or novelty for the reformulation.

## 4. Independent finite replay and its limits

Running the frozen verify.py independently produces a file byte-identical to verification.json, with SHA-256 `7e3d27b0b02106a4d51ef6a38bf77d6424b6cefa25a692f621d89b96acade21e`. The reproduced output is included as replay_verification.json.

The indexed counts are:

- One-swap restrictions: 950
- Two-swap restrictions: 1,442
- Partition normalizers: 75
- Matrix-embedding elements: 4,129
- Matrix-embedding products: 455,305
- Measure-atom equalities: 243
- Measure-invariance equalities: 125,162
- Layer-flattening pairs: 19,600
- Free-word separations: 2,172
- Total: 609,078

The code uses exact permutations and rational arithmetic. The permutation and measure models have at most five base points; the two-swap loop has at most four; layer parameters run through seven; free-word separation runs through radius six. The measure model is a uniform finite model, not an exhaustive test of arbitrary invariant measures. Layer flattening is a coordinate-bookkeeping check, not an amenability check. All finite permutation groups in these tests are amenable, so they cannot expose or eliminate the infinite coamenability obstruction. The infinite claims stand on the written arguments, not the successful replay.

Reproduction from the frozen packet uses `python verify.py`, byte comparison against verification.json, and `sha256sum -c SHA256SUMS`. The independently recorded integrity results are in AUDIT_CHECKS.json. AUDIT_MANIFEST.json and AUDIT_SHA256SUMS cover the audit outputs without altering the author freeze.

## 5. Publication and disposition boundary

No blocking correction is requested. The author-frozen statement that review was pending is a historical statement at freeze and should not be rewritten in place; this separate audit supplies the subsequent verdict.

The audit outputs contain authored review prose, integrity metadata, and the finite replay output. They contain no source PDFs, screenshots, extracted source text, raw catalogue records, raw repository-search responses, private filesystem paths, or coordination records. Their manifest is an explicit allowlist. The original eight-file packet remains byte-for-byte unchanged, and no remote writes were performed in this audit.

Any later presentation should continue to say that this is an unrefereed partial-results investigation with the original problem unsolved. It may accurately report a separately reviewed binary-amplification equivalence, credited local and measure arguments, other elementary reductions, and two missing-hypothesis controls. It must not label the finite checks an infinite proof, either boundary example an original-hypothesis counterexample, the equivalent binary question a solved theorem of amenability preservation, or the search results a novelty certificate.
