# Independent full-source content cross-review: prior Yang–Baxter edition 21971507

**PASS. No blocking content issue.** Full twelve-page exact deposited PDF extraction read independently, including all definitions, theorem/proposition statements, derivations, minimality argument, generalized operator comparison, computational boundaries, priority qualification, AI declarations and references. Completion estimate: 100% of assigned metadata-content cross-review. Checkpoint: 2026-10-10 14:28 PDT.

The source is `papers/21971507/exceptional-ybe-d4-v1.1.3.pdf` and matching `.txt`. Independent MD5 and SHA-256 checks agree with the public source catalog: MD5 `3f65c5978bb5b4719224e6463e8a5abb`; SHA-256 `f119f7a33285f37017ed4c76a964ae6d6d17415e03c7503e9bc079f7a96a93bb`. The reviewed baseline is `receipts/21971507/before.json` and proposal is `patches/21971507.json`. No patch or remote record was modified by this reviewer.

## Version-specific mathematical evidence

The older edition itself already has the five-word real Pauli–Clifford reflection expansion. Sections 2–4 define the real Pauli basis, the four commuting involutions and fifth anticommuting involution, and the eighteen-word cubic certificate on a reflection circle. Thus `Pauli-Clifford expansion` is supported by this edition, independently of the later title's “five-word normal form” wording.

Theorem 1.1 constructs a 16×16 unitary Yang–Baxter operator on local dimension four in `[exp(iπ/3),1/2,4]`, with both braid eigenvalues having multiplicity eight. Its spectral projection has both unnormalized partial traces equal to twice the identity. Proposition 5.1 proves the Markov-trace parameter 1/2, identifies the representation kernel with the trace annihilator, and obtains faithful quotient-tower embeddings of Hn(3,6). The paper identifies this tower with the C(sl3,6) Jones–Wenzl sequence. Those statements directly support `Yang-Baxter equation`, `unitary R-matrices`, `Jones-Wenzl representations`, `Markov trace`, `C(sl3,6)`, `H_n(3,6)` and `partial trace`.

Corollaries 1.2 and 5.3 and §6 supply dimension-four minimality and confirmation of the Rowell–Wang conjecture **for this specific simple tensor generator**, using the known dimension-two obstruction and a separate dimension-three argument. `Rowell-Wang localization conjecture` is a precise named-problem subject tag, not an assertion that every case of the conjecture is solved. The unchanged description remains focused on this Jones–Wenzl sequence. `Minimal local dimension` accurately describes the actual minimality result, which is not a minimum matrix-entry count or global classification theorem.

Section 7 proves a `(3,2)` generalized Yang–Baxter operator after a sitewise qubit swap and spectator factorization, including braid-tower compatibility. It contrasts this tensor placement with the earlier GHR `(3,1)` operator and another `(3,2)` spectrum. Therefore `generalized Yang-Baxter equation` is independently supported by the older edition. This comparison is not the later exact local-unitary comparison to the opposite of a literal Family III quaternionic operator.

Section 8 supplies three exact verification routes: hardened SymPy, independent sparse standard-library exact arithmetic, and a matrix-free Pauli-word route, with deliberate negative mutations. `Exact symbolic verification` accurately names these finite checks. The paper explicitly separates them from the all-strand tower-faithfulness argument, Lechner's classification input and historical literature search. The proposed tag does not claim a complete proof-assistant formalization.

## Scope and contamination checks

The proposal is **keywords only**, with seventeen entries; it retains all five existing keywords exactly and adds twelve supported expert-search terms. English already exists and is untouched. The description, creator/ORCID, title, DOI/prereservation, publication date, version, license, access and submitted-date metadata are absent from the patch.

No later-edition HOMFLYPT, Turaev-enhancement, quaternionic-factorization, Family III equivalence, finite-braid-image, branched-cover or polynomial-time-invariant term appears in the keyword proposal. The old paper mentions quaternionic work only as prior art and expressly does **not** identify an intertwiner to the known quaternionic `(3,1)` model. The broader even-dimensional exceptional-family classification and uniqueness remain unclaimed. Its amplification construction gives local dimensions divisible by four and explicitly leaves 6,10,14,… unresolved.

Priority is also edition-specific: §9 reports only a focused search through 16 August 2026 and excludes absolute-priority guarantees, concurrent/unindexed/private work, uniqueness and a full exceptional-family classification. The AI-assisted numerical discovery search was not retained and is explicitly neither reproducible nor exhaustive; the exact derivation and verifiers support the theorem independently. No metadata prose was rewritten, and these source caveats are neither contradicted nor upgraded by the added subject tags.

## Handoff and exact binding

`CROSS_REVIEW_OLDER_YANG_BAXTER_QA.json` records the proposal, baseline and source hashes. The reviewed proposal SHA-256 is `5523c65426a5692c6394d2981e49394e64e69afaa5ee47c7eb90ba15ad1f2a1f`.

This is a metadata-fidelity cross-review, not a new independent certification of every mathematical theorem. No content gap remains for the proposed tags. Root must preserve the older record's existing DOI and its two-record version history through the separate native metadata-only workflow; this reviewer performed no remote mutation, version creation or external communication.
