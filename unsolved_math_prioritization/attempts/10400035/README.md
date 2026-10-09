# Milnor invariants and free-exterior string links

Three scoped results for Stanford Question 2.13, problem 10400035 (AMR-103-0035), with complete authored proofs, supporting lemmas, independent AI mathematical audits, and bounded literature context.

## Accepted mathematical scope

All statements concern rational-valued ordinary unframed Vassiliev invariants of smooth ordered string links with fixed matching endpoints and product endpoint collars. Each component is oriented from bottom to top; its height need not be monotone. The free-exterior condition means the **actual three-dimensional exterior group is abstractly free of the appropriate rank**. It imposes no meridian-basis condition.

Write \(V_n(k)\) for invariants of order at most \(n\), including constants; \(N_n(k)\) for the subspace vanishing on every such free \(k\)-string exterior; and \(M_n(k)\) for the intersection of \(V_n(k)\) with the entire unital algebra of based Milnor invariants, allowing all lengths and repeated indices.

1. **The proposed Milnor/free-exterior span fails at \((k,n)=(2,2)\).** In fact \(M_2(2)=\operatorname{span}_{\mathbb Q}\{1,\ell,\ell^2\}\), and the first component's Conway coefficient \(a_1\) does not belong to \(M_2(2)+N_2(2)\).
2. **The low-order vanishing kernel is zero:** \(N_n(k)=0\) for every \(k\ge2\) and \(0\le n\le2\).
3. **There is a nonzero kernel element of exact order seven on two strands.** Thus \(N_7(2)\ne0\), and the same invariant lies in \(N_n(2)\) for every \(n\ge7\). The complete marked geometric lemma proves that every free-exterior two-string link is fixed by the specified label-preserving simultaneous reversal. Antisymmetrizing a rational integrated Duzhin–Karev odd weight system gives the invariant.

Orders three through six for two strands remain unresolved here. There is no least-order claim, higher-strand higher-order kernel theorem, general classification of \(N_n(k)\), or extension of the spanning counterexample to every larger order. The existence construction in degree seven does not supply a numerical value on a named nonsingular string link. The familiar one-strand case is separate.

## Complete written arguments

- [PROOF_SPAN_ORDER_TWO.md](PROOF_SPAN_ORDER_TWO.md): the complete first proof.
- [FILTERED_MILNOR_ORDER_TWO_LEMMA.md](FILTERED_MILNOR_ORDER_TWO_LEMMA.md): the full all-length Milnor-algebra argument, preserved byte-for-byte.
- [GEOMETRIC_EXISTENCE.md](GEOMETRIC_EXISTENCE.md): the full source-backed free-exterior trefoil-strand construction and marked-category conversion.
- [PROOF_KERNEL_ORDER_TWO.md](PROOF_KERNEL_ORDER_TWO.md): the complete all-\(k\) low-order kernel proof, including the Artin/Magnus calculation, every coordinate, split inclusion, and coefficient elimination.
- [RATIONAL_FREE_WITNESS.md](RATIONAL_FREE_WITNESS.md): the full rational-tangle witness with its cap-preserving marking.
- [PROOF_KERNEL_ORDER_SEVEN.md](PROOF_KERNEL_ORDER_SEVEN.md): the complete exact-order-seven existence proof and its already-authored supplementary trace calculation.
- [MARKED_FREE_REVERSAL_LEMMA.md](MARKED_FREE_REVERSAL_LEMMA.md): the complete marked free-reversal proof, preserved byte-for-byte. It includes the precise boundary map, hyperelliptic extension, collar correction, tube filling, and relative-ball isotopy.

## Independent written audits and context

- [AUDIT_SPAN_ORDER_TWO.md](AUDIT_SPAN_ORDER_TWO.md), [AUDIT_KERNEL_ORDER_TWO.md](AUDIT_KERNEL_ORDER_TWO.md), and [AUDIT_KERNEL_ORDER_SEVEN.md](AUDIT_KERNEL_ORDER_SEVEN.md): the complete independent mathematical audit reports, with only documented provenance/privacy and unavailable-artifact edits.
- [AUDIT_ORDER_TWO_ALGEBRA.md](AUDIT_ORDER_TWO_ALGEBRA.md): the complete authored algebra-audit exposition, with its unavailable reproduction commands replaced by an explicit artifact-boundary notice.
- [PRIORITY_SPAN_ORDER_TWO.md](PRIORITY_SPAN_ORDER_TWO.md) and [PRIORITY_REVERSAL_ORDER_SEVEN.md](PRIORITY_REVERSAL_ORDER_SEVEN.md): the bounded literature/context checks. They do not establish novelty or earliest priority.
- [ACCEPTANCE.md](ACCEPTANCE.md): aggregate acceptance, dependencies, and limits.
- [SOURCES.json](SOURCES.json): public bibliographic metadata, sixteen distinct PDF identities recomputed for this edition, and clearly attributed historical retrieval/inspection records. Additional context-only citations have no new PDF-identity claim.
- [STATUS.json](STATUS.json): aggregate mathematical status.
- [PROVENANCE.md](PROVENANCE.md): the exact categories and per-document account of edition-only edits.
- [MANIFEST.json](MANIFEST.json): the exact nineteen-file publication set, with SHA-256 and byte counts for all other eighteen files. It does not hash itself.

## Written proof versus supplementary computation

This is a theoretical edition. It includes no executable scripts, fixtures, machine-readable computational results, or execution logs. The historical audits report additional exact arithmetic and mutation checks; those statements describe the checks performed for the original audits, not computations rerun in preparing this edition. The written mathematics and the sources on which it depends remain available in full. The degree-seven manuscript's displayed matrix/trace calculation was already present in its audited mathematical exposition and is explicitly supplementary to the cited nonzero-symbol theorem. No executable check has been converted into new prose to replace an omitted script.

The source-dependent geometry, ordinary unframed survival of the symbol, and rational integration are mathematical obligations separate from finite calculations. Hash matching establishes byte identity, not mathematical truth. The audits are AI mathematical reviews, not human peer review or formal proof-assistant verification.

No copied third-party PDFs, extracted source text, source artwork, dataset contents, private sources, or private coordination material are included. The original mixed source/computation inventories and their digests are excluded. Only this public edition has an included exact-file manifest.

## Chronology and stopping boundary

The three original reports are retained chronologically. Their dispositions such as “audit requested” and their residual-scope descriptions refer to the time each report was written. The first proof did not settle \(N_2\); the second subsequently settled it. The second did not settle any higher-order case; the third subsequently established the degree-seven two-strand result. The current combined status is the three-item scope above and ACCEPTANCE.md.

The campaign stopped after three substantive approaches out of a maximum of five. The two remaining approaches were not used. Audit, source inspection, and preparation of this edition add no proof-search approach. No historical novelty or priority is claimed. This addition changes no QUEUE.md or unrelated repository file.
