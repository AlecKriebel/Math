# Independent acceptance of the Ohtsuki 12.6 existence-proof audit

Review date: 2026-10-21 (UTC).

## Bound artifact and verdict

- Artifact: `recovery_ktg_1885_20261021/existence_proof_audit.md`
- SHA-256: `c908aa32b3e1461462f0619a8bb5d6c1b6eb60becf8a781d05e5b34f3d0a49b7`
- Verdict: ACCEPT the accuracy of this artifact as a literature-sensitive dependency audit and a conditional residual proof criterion. This is not acceptance of a solution to Ohtsuki Problem 12.6, a new universal invariant, an original impossibility theorem, or an exhaustive determination of the problem's current status.

This report binds only the exact bytes identified above. A subsequent audit revision requires another review or an explicit statement of what changed. The reviewed audit was not edited by this reviewer.

## Scope and primary-source checks

The reviewer independently inspected Ohtsuki's original paragraph and Problem 12.6, Dancso's construction and universality discussion, and Bar-Natan–Dancso's definitions, anomaly formula, dotted construction, associator dependency, and no-go appendix. The historical generators/relations/syzygies discussion in Bar-Natan–Thurston (2001), sections 1.2–1.3, was also checked against the public author-hosted text.

Acceptance covers the following distinctions.

1. **Different theories must not be silently identified.** Ohtsuki's paragraph allows half-integer framing and nonorientable ribbon neighborhoods and lists connected sum, unzip, bubbling, and unknot creation. Bar-Natan–Dancso's oriented thickening and original operation package are different; its dotted repair changes the objects and operations again. A construction on a suitable orientable subtheory could suffice for a knot conclusion, but only after the required generation, descent, and convention checks. The audit correctly leaves these checks open.

2. **The strict ordinary obstruction is real and narrowly scoped.** The published chain from an idempotent unknot value to the contradictory degree-two dumbbell value is accurately summarized. Orientation reversal, unzip, and connected sum visibly occur in the appendix. Dropping edge deletion alone has not been justified as an escape. This review does not assert a new minimal-hypotheses version of the published theorem. Neither reviewer nor audit independently reimplemented the source's omitted degree-two diagram calculation; acceptance here is of the accurately attributed published result and its dependency chain.

3. **Dotted repair imports existence.** Theorem 3.3 explicitly starts with an existing expansion and the unknot series. Its proof of universality uses that prior expansion. The audit correctly distinguishes this dependence from circular use of an invariant not yet constructed, and does not confuse valid reuse of a theorem with a logically invalid argument.

4. **The integral construction is genuine, but does not supply the missing presentation certificate automatically.** Dancso's Proposition 6.7 and section 6.5 establish a universal graph invariant and a corrected target unzip. Calling the analytic construction circular merely because it uses Kontsevich-integral methods would be wrong. Conversely, reproducing that established construction is not new mathematics and does not alone verify the exact original half-framed presentation.

5. **Associator existence and KTG descent are separate.** An independently established associator can be legitimate input. Extracting it from an old expansion does not establish existence independently of that expansion. The audit correctly requires a complete operation/framing dictionary and relation verification, rather than treating pentagon and hexagons as an unexamined complete certificate. Bar-Natan–Dancso's finite-generation discussion does not provide that certificate; its page 6 footnote expressly leaves finite presentation unpursued.

## Associated-graded circularity

The audit correctly preserves the distinction between the diagram quotient and the abstract topological associated graded. Bar-Natan–Dancso, section 2, page 5, supplies a surjection from diagrams modulo the stated relations and explains that proving the absence of further relations uses an existing universal invariant. Equality of topological filtrations alone cannot prove that surjection injective.

For a surjection q:D_n -> gr_n V and an independently constructed filtered linear extension E:V -> completed D, the equation gr_n(E) composed with q = id on D_n does imply injectivity: q(d)=0 forces d=0. Together with surjectivity it gives the required graded identification. The audit uses this as an obligation to prove, not as an assumed identification. A vector-space splitting into the abstract associated graded does not substitute for this diagram-valued conclusion.

## Conditional lifting lemma

No material mathematical defect was found under the stated hypotheses, with the usual nonnegative degree filtration of diagram spaces understood.

For h_i in F^(n+1), n>=0, every term containing at least two corrections belongs to F^(2n+2), which is contained in F^(n+2). Additive filtration compatibility of all multilinear operations is essential here. The next-degree relation error is therefore exactly e+Lh, so a lift exists precisely when -e belongs to im L. This argument does not require surjectivity of L and supplies no such surjectivity claim.

For inverse operations the asserted extension is correct in a complete unital filtered algebra on constant-one inputs: the first correction is -x^(-1) h x^(-1), and terms with at least two h factors have the same degree bound. Completeness supplies the inverse-limit assignment from a compatible sequence; continuity and separatedness force its relation defects to vanish. The audit properly does not replace a compatible sequence by unrelated solutions at each finite degree.

The syzygy discussion is also correct: membership in ker M, with ML=0, is weaker than membership in im L. The missing all-degree obstruction vanishing or compatible explicit construction remains missing.

## Conditional universality mechanism

The stated mechanism is sufficient, with its explicit qualifications retained. Here compatible local presentations must mean a common admissible template with independent local crossing slots, so the entire alternating crossing resolution can be evaluated multilinearly. Each local over-minus-under value must begin with exactly its corresponding chord, with coefficient one; the surrounding operations must preserve the relevant filtration and induce the asserted diagram operations. Under those conditions the n-fold difference has the required degree-n diagram and no lower terms.

Proving only the one-crossing identity in unrelated presentations would not suffice. The audit explicitly requires the simultaneous arbitrary-singular-knot presentation argument and does not claim to have supplied it. Knot framing, diagram relations, and symbol conventions must remain consistent throughout any future implementation.

## Sources and limitations

- Ohtsuki (ed.), 2002, section 12.4, pages 533–534: https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf
- Dancso, 2010, section 3.5, Proposition 6.7, and sections 6.5–6.6: https://msp.org/agt/2010/10-3/agt-v10-n3-p04-p.pdf
- Bar-Natan–Dancso, 2013, sections 2–4 and Appendix: https://www.math.toronto.edu/drorbn/papers/ktgs/ktgs.pdf
- Bar-Natan–Thurston, 2001, sections 1.2–1.3: https://www.math.toronto.edu/drorbn/papers/AlgebraicStructures/LongAlgebraicStructures.html

This is an acceptance of the bounded audit, not of original-problem closure. No source documents or source passages are reproduced. No publication, repository changes, or queue edits were performed by this reviewer.
