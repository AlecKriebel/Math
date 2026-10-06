# Independent adversarial audit: generic hyperfiniteness for Z wr Z

## Verdict

**ACCEPT as a complete affirmative mathematical candidate, with no required proof correction.** The audited argument establishes Borel hyperfiniteness of the orbit relation on the **entire** Cantor space for a comeager set of actions. It does not merely establish a measure-theoretic statement, a result on a comeager subset of the phase space, or a result only for free actions.

This verdict is an independent AI-assisted mathematical review, not human peer review, formal verification, or certification of novelty. The author manuscript remains immutable and appropriately labeled as a candidate. Its original statement that independent review was pending records its historical freeze; this report supplies the later review. Finite computations support only the stated finite identities and software integrity.

The reviewer read the complete proof and all distributed verifier code, independently reconstructed the critical arguments, freshly retrieved the principal primary sources, and attempted the specific failure modes below. No missing hypothesis or fatal gap was found. An independent quantitative slab argument appears in Section 4.

## 1. Frozen object and exact target

- Problem ID: 30006166; source identifier: OWR-14299082-012; catalog rank: 830.
- Original author archive: 19,189 bytes; SHA-256 `1afc6d7c39a334dc3c271dfa2944426a92589236822d8a06fb97ca4c64e71d40`.
- Original author manifest: SHA-256 `c9c1b418218bbb6f831908733d4b8a27d819cdd3abbb72a142d3f57aea3ab171`.
- Original proof: SHA-256 `74c727c159d7af1ec7be50c3766356f43a07171f3787a629627d2fce9bfe3a57`.

The exact question was checked in the freshly retrieved [official Oberwolfach report](https://content.ems.press/assets/public/full-texts/serials/owr/22/1/14299082/online/10.4171-owr-2025-2.pdf), printed p.115, PDF page 41 (one-based). The page was also rendered and visually inspected. The preceding contribution identifies the action space as all continuous actions on Cantor space. Its distinction between hyperfinite and measure hyperfinite confirms the stronger whole-space interpretation used in the candidate.

Independent full-dataset hashing reproduces all three dataset identities and both target fingerprints. The complete problem record, including fields beyond its statement, was used in the review fingerprint. The research-results dictionary has no entry for this source identifier, so its documented empty-object fallback was used. The catalog explicitly records rank 830; it is not inferred from a subset or a search rank. `CORPUS_VERIFICATION.json` reports only verification metadata, not dataset contents.

The restricted direct-sum wreath product is the appropriate countable discrete group. The proof does not replace it with a finite-lamp group, an unrestricted product, or a topological wreath product.

## 2. Primary-source hypothesis check

The [CJMST author manuscript](https://math.berkeley.edu/~marks/papers/polycyclic_v13.pdf) was independently downloaded and matched the author source byte for byte. The [published journal record](https://doi.org/10.1215/00127094-2022-0100) confirms the citation. The following are the precise imported consequences:

- Lemma 2.2, Lemma 3.1, and the paragraph following Definition 3.2 permit finite Borel covers with uniformly finite finite-move components.
- Corollary 5.5 applies to **any** Borel action of each fixed finite-rank free abelian group. Freeness is unnecessary.
- Theorem 7.3 allows a separate finite Borel asymptotic dimension at each stage. It requires proper Borel extended metrics and uniform control of the next metric on bounded pairs for the previous one.
- Corollary 7.5 applies to arbitrary Borel actions of a countable group whose finitely generated subgroups have polynomial growth. It applies to the full lamp group.

These statements were checked in manuscript pp.11, 13–15, 21, and 31–33; pp.21, 31, and 33 were visually inspected. In particular, neither a common dimension bound nor free actions are silently being added or omitted. The compatibility requirement is genuinely stronger than the unresolved unrestricted union principle, and the candidate verifies it.

The freshly retrieved [Iyer–Shinko v1](https://arxiv.org/abs/2409.03078) confirms the known finite-asymptotic-dimension baseline and its scope. It is background, not a necessary input to the candidate. Bounded current searches found no prior full resolution or relevant correction of the imported results. Search absence does not establish worldwide current openness or priority.

## 3. Relative lifting and Baire category

### 3.1 The finite-factor conditions really are clopen

A continuous map from Cantor space to a finite set has clopen fibers separated by a positive distance in any fixed compatible compact metric. Consequently sufficiently small uniform perturbations of the images of both generators preserve all their factor labels at once, for every point. This proves openness. A failure at a single point persists under a sufficiently small perturbation, proving closedness. The argument takes place inside the closed Polish action space, so all group relations are retained.

The countability claim is valid: every clopen set is a finite union from a countable clopen basis, and finitely many such fibers determine a finite-valued continuous map. Thus the subsequent intersection is countable.

### 3.2 The lifting is relative to the specified old factor

For a factor c modulo m and m dividing n, the pullback Y over the reduction map has exactly n/m copies of every point. The diagonal action is well-defined because the old c-label and the new finite coordinate change by the same height character. It is an exact action.

Every nonempty clopen atom P in the chosen refinement is a Cantor space; its pullback is a finite nonempty disjoint union of Cantor spaces and is again a Cantor space. The piecewise homeomorphism exists for n=m as well as for n>m. It sends P onto the entire pullback over P, so both the projection of h and the projection associated to its inverse respect P.

For a prescribed finite list of action coordinates, refining the small target partition by all its inverse images under those coordinates ensures that beta(g)x and alpha(g)x land in the same small target atom. Including inverse coordinates handles uniform convergence of inverses. This works for arbitrary finite group-element lists, rather than only a and t. Refining additionally by the old factor fibers ensures that the new factor reduces to the exact old c, not to a nearby or conjugate factor.

### 3.3 The generic factors are coherent

Each dense-open requirement is conditional: it is automatically satisfied outside the old-factor locus, and enforces an actual lift inside that locus. Starting with the unique factor modulo 1, the fixed action in the intersection therefore permits a recursive choice along the factorial tower. No limit of actions is being taken here. The compatible finite maps yield one continuous map to the inverse limit, equivariant under all of W.

No uniform choice of this map as the action varies is needed for the asserted comeager property. Surjectivity is correct but is not needed for the subsequent Borel theorem: the compact image is nonempty and invariant under the dense integer translations.

**Adversarial outcome:** no density/relative-coherence gap. Having unrelated finite factors alone would not have sufficed, but that is not the proof being given.

## 4. Slabs: independent metric reconstruction

For a fixed width m, every point has the prescribed residue r in the range 0 through m−1 and the uniquely determined base point z=t^(−r)x. This is a Borel bijection with B_m times that finite set even when lamps have stabilizers. Distinct levels cannot coincide because they have distinct residues.

In these coordinates an a-edge changes z by a_(−r), while an uncut t-edge changes only the level. The sign is forced by t^(−r) a t^r. The subgroup generated by those m abstract lamps is Z^m, although its action on B_m need not be faithful.

Here is an independent derivation of the slab's finite-dimensional control. Let d_m be the orbit word metric on B_m for these m lamp generators. If x=(z,r), y=(w,s), then

    d_m(z,w) <= rho_m(x,y).

Indeed every horizontal slab edge projects to one permitted base move, and every vertical edge projects to equality. Conversely, whenever d_m(z,w) is finite,

    rho_m(x,y) <= (2m−1) d_m(z,w) + (m−1).

To realize a single base generator a_(−j) while starting at level r, move vertically to j, perform the lamp move, and return to r. This costs at most 2(m−1)+1. Repeat for a shortest base word, then move from r to s. All these moves stay inside the slab. This proves both the inequality and equality of the finite-distance component relations in the product coordinates.

Now fix a threshold R. A monochromatic rho_m-threshold chain projects to a monochromatic d_m-threshold chain under any lifted base coloring. The base cover supplied for the fixed group Z^m has uniformly bounded monochromatic components. The upper inequality therefore bounds each lifted component's slab diameter uniformly. The number of colors depends on m but not R. This independently proves the slab lemma.

The author's original cardinality proof also works. Over one base point there are exactly m slab points; a projected component with at most C_R points lifts to at most m C_R points. A connected threshold graph on at most that many points has a simple path with at most m C_R−1 threshold steps between any two of its points. Its ambient slab diameter is at most R(m C_R−1). The connecting unit-edge paths need not be monochromatic; the proof never requires that false assertion.

The graph is Borel, loop removal is harmless, and degree is at most four. Its path metric is therefore Borel and has finite-radius finite balls. Thus it meets the source's meaning of a proper Borel extended metric.

**Adversarial outcome:** no nonfree-action, projection, coloring, or uniformity gap. The independent inequality is a clarification, not a correction.

## 5. Compatible union on the regular part

If m divides n, the only forbidden forward residue at width n reduces to the forbidden residue at width m. Therefore every previously included shift edge remains included; lamp edges never change. The graph inclusion is literal on the common vertex set, so subsequent distances are no larger than previous finite distances.

For any positive finite R, the next distance is bounded by R on pairs whose previous distance is less than R. This directly checks the hypothesis of Theorem 7.3, with no change of metric chosen separately at each point. The slab dimension may grow arbitrarily with width; the theorem permits this.

The integer subgroup in the profinite integers is countable, hence Borel. Its preimage and complement are invariant under the whole action. Restricting slab graphs to the complement neither breaks paths nor changes the above coordinate description.

The one forward edge that can be omitted at every factorial width is based at profinite height −1. After removing the full invariant preimage of the integer orbit, every remaining forward generator edge is included at some stage. An arbitrary group word uses finitely many such edges, so graph monotonicity supplies one stage containing them all. This proves equality with the union of the slab relations, not just containment or equality almost everywhere.

**Adversarial outcome:** the proof does not invoke an arbitrary increasing union of hyperfinite relations. It invokes the strictly stronger verified finite-dimensional metric theorem.

## 6. The entire exceptional preimage

The exceptional set need not be countable: its fibers may be uncountable. Its integer height h is nevertheless Borel because it has countably many Borel fibers. The normalization map q(x)=t^(−h(x))x lands in the zero-height fiber.

Conjugating a group move between normalized points gives an element with height character zero, hence a lamp-group element. Conversely any lamp relation between normalized points can be conjugated back to a W-relation. These two implications prove the claimed equivalence of orbit tests without claiming that q itself is finite-to-one.

Each finitely generated subgroup of the direct-sum lamp group lies in finitely many lamp coordinates and is finitely generated abelian. Corollary 7.5 thus provides finite Borel approximations F_j on the zero-height fiber.

For the proposed H_j, the points outside the height band are singletons. Inside the band the relation is a pullback of F_j, hence transitive as well as reflexive and symmetric. Each pair (z,k), with z in the zero-height fiber and integer k, identifies exactly one point t^k z. Therefore an H_j-class in the band has at most (2j+1)|[z]_(F_j)| points. The bound need not be uniform in z, and finiteness does not require uniformity.

The bands and base approximations both increase. Every related pair eventually lies in a common band and has normalized points in one F_j-class. This exhausts the exceptional relation in full. Finally, finite approximations on the two invariant Borel pieces can be joined stage by stage without creating cross-piece classes.

**Adversarial outcome:** no loss of exceptional fibers and no invalid infinite-to-one pullback. The whole-space conclusion follows.

## 7. Diagnostics, packaging, and limitations

The author package contains exactly twelve regular files. The original archive's complete entry inventory and every decompressed file were checked against the preserved author directory, with no symlinks, directories-as-payload, duplicate entries, or path traversal accepted. The original manifest and proof hashes match the handoff pins.

The author's verifier passes under normal and optimized Python, and its relocated replay passes in both modes. All 22 original mutation rejections reproduce. Its finite consistency counters total 97,924. The code executes source bytes after manifest verification; it does not accept a stale bytecode cache or use assertions that disappear under optimization.

The independent checker uses a different cursor-coordinate representation. Its fifteen finite slab models include trivial lamps, repeated lamp generators, and nonfaithful lamp actions. It checks full all-pairs coarse metric inequalities, projected threshold-chain components, divisor inclusions, and the persistent integer boundary. It performs 20,525 counted finite diagnostics, all reproduced normally and under optimization. These models are finite quotients used for algebraic diagnostics; they are not asserted to carry the infinite profinite factor.

The independent package adds a strict source-executing verifier and separate mutation tests. Normal, optimized, and relocated replay results are recorded in the accompanying files. All acceptance metadata preserves the distinction between mathematical review and executable finite tests.

No source PDF, extract, rendered page, dataset, private record, or coordination material is included in the safe archive. The source and corpus metadata are public titles/URLs, byte counts, hashes, and match/inspection results. Hash manifests are integrity bindings, not signatures: coordinated replacement of verifier, payload, and all externally trusted pins is outside their threat model.

## 8. Acceptance conditions and disposition

All essential dependencies have been checked: exact source target, source hypotheses, relative lifting, coherent generic factors, nonfree slabs, proper metrics, stage compatibility, regular generator exhaustion, and finite exhaustion of the full exceptional preimage.

Required mathematical corrections: **none**.

Recommended disposition: **claimed_solved / complete affirmative candidate, independently audited by AI, unrefereed**. Do not relabel this as externally verified, formally certified, historically novel, or a solution for every Borel action of Z wr Z. The broader unrestricted Borel-action question is not settled by this candidate.
