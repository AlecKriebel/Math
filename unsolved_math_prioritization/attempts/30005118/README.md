# Cyclic self-sumset recognition: certificate and audit

Problem 30005118 / OWR-10252930-031 asks whether a given subset B of Z/nZ is A+A for a subset A of the same group. With ordinary self-sums, repeated summands allowed, this decision problem is NP-complete in both explicit sparse binary and dense characteristic-vector encodings. Hardness already holds for odd n and nonempty targets containing zero whose canonical representatives lie strictly below n/2.

The conclusion combines Abboud, Fischer, Safier, and Wallheimer's published integer NP-hardness theorem with the complete elementary normalization and zero-anchor transfer supplied here. The original hardness construction is theirs. This is prior-theorem applicability plus a supplied reduction, with no novelty claim for the transfer and no independent reproof of the source gadgets. A polynomial-time algorithm in either explicit encoding exists if and only if P=NP; no unconditional impossibility is asserted.

## Reading order

- [CYCLIC_SUMSET_CERTIFICATE.md](CYCLIC_SUMSET_CERTIFICATE.md): the full universal proof, including all normalization, anchor, no-wrap, exceptional-case, size and NP-membership arguments.
- [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md): the complete substantive independent check of that proof, the source dependency and both encodings.
- [ACCEPTANCE.md](ACCEPTANCE.md): the bounded accepted conclusion and exact edition identities.
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md): public primary-source links, bibliographic details, inspected locations, PDF identities and source-inspection limits.
- [PROVENANCE.md](PROVENANCE.md), [STATUS.json](STATUS.json) and [MANIFEST.json](MANIFEST.json): the editorial boundary, precise scope and exact inventory.

The original certificate's mathematical Sections 1–5, complete source-dependency introduction and final limitations are unchanged. The audit's target/source verification and every mathematical and complexity check are unchanged. Computational reproduction sections and administrative references outside this standalone edition are omitted; no argument is replaced by a computational assertion.

AI-assisted and unrefereed. The independent check is an AI-assisted mathematical audit, not external human peer review or proof-assistant verification. The original question does not specify an encoding or define efficient, so the conclusion is expressly confined to the two stated explicit models. No claim is made for compact circuit or oracle input, restricted sums, approximation, randomized algorithms or average-case recognition.
