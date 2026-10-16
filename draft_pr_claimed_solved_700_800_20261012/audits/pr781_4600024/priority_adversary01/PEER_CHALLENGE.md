# Fresh adversarial challenge of the first priority audit

The independent report and verdict were copied byte-for-byte and hashed in INDEPENDENCE_FREEZE.json before opening the peer packet. The immutable copies are INDEPENDENT_REPORT.md and INDEPENDENT_VERDICT.json. No peer conclusion was used to produce that independent position.

Peer target: priority_audit, root-supplied FROZEN_MANIFEST.json SHA256
6223de076929683e0cffef1ce5a222bd7cd278c718718f686d5958bc87a56163.
The manifest was independently hashed before use, and its verifier digest was independently matched to the pinned manifest. Fresh ordinary and optimized verifier replays both passed: 15 artifact files and 10 input receipts. No peer files were changed. PEER_REPLAY.json records exact outcomes.

**Challenge outcome: no error found that overturns the peer's bounded, explicitly non-novelty conclusion.** Several exclusions can be strengthened with checkable distinctions below. None of these checks certifies firstness or excludes uninspected publications.

## Actual sources and hypotheses

I freshly fetched and hashed the five primary bodies in PEER_SOURCE_RETRIEVALS.json; all hashes match the peer's corresponding source receipts. I read Dykstra's printed pp. 47–48, Salo–Törmä v2 pp. 17–19, Jung pp. 13 and 18, Dastjerdi–Shaldehi v1 p. 11, and Salo's regularity paper pp. 4–5. These checks establish actual statement scope, not full proof validation.

- Dykstra's Problem 3.6.8 explicitly asks for necessary and sufficient conditions for steadiness of a homomorphism on a sofic shift. The peer correctly treats it as an earlier formulation. Its scope is more general than the candidate's irreducible setting. An aggregated report must not announce a solution of the entire unrestricted Dykstra problem. The read thesis is a distinct source from the inaccessible Barth–Dykstra article; the peer preserves that distinction.
- Jung's Theorems 4.5 and 5.5 really do require an SFT target, entropy inequality, a proper source subshift and other ambient conditions. An SFT target assumption prevents applying these statements directly to arbitrary strictly sofic T. In the selected self-map problem the SFT case is already positive by the non-strict witness T'=T. No hidden general solution follows by silently dropping the target hypothesis.
- Dastjerdi–Shaldehi Theorem 4.15 requires an irreducible SFT range and a retract. Theorem 4.16 supplies a.e. continuation from synchronized/semi-open hypotheses, without turning it into a general SFT-neighborhood extension. The peer does not conflate these properties with Ballier's condition on the ambient extension.
- Salo–Törmä Theorem 1 really decides split epicness for a specified map between sofic shifts. It is a particularly relevant algorithm, not a source to dismiss solely by title. The two counterexamples below establish that split epicness and steadiness are not equivalent even for onto self-codes of mixing sofic shifts.
- Salo Theorem 5 has a mixing SFT domain and characterizes regularity by a section onto the image. Theorem 7 restates the split-epicness decision theorem. Those are actual strong results; the XOR example below shows regularity is not necessary for the selected steadiness property.

## Two-way separation of the nearby properties

Let E be the binary even shift, with each two successive 0s separated by an even run of 1s. It is mixing sofic and is not SFT.

**Split epic but not steady.** The identity id_E has the identity block-map section. If an extension of id_E existed on an SFT neighborhood, its finite window agrees with identity on every sufficiently accurate canonical E[n]. It would then force E[n] into E. But for every n a periodic point with a 0 followed by a sufficiently long odd run of 1s is n-locally E-admissible and is not in E. Thus id_E is not steady. Dykstra's nonsteady-map discussion is consistent with this obstruction.

**Steady but not split epic.** On the full binary shift X, set f(x)_i=x_i+x_(i+1) mod 2. Every bi-infinite y has an f-preimage: choose x_0 and solve the recurrence in both directions. Thus f is an onto self-code, and is steady with witness X itself. If it had a shift-commuting section g, the fixed point 1^Z would have a fixed-point preimage g(1^Z). Both fixed points of X, 0^Z and 1^Z, map to 0^Z, a contradiction. Hence f has no section and, by the inspected regularity equivalence, is not regular.

These examples refute a direct equivalence. They do not rule out a different, nontrivial algorithmic reduction from steadiness to split epicness of some constructed map. No such reduction was located in the inspected sources; that is the precise remaining historical gap. verify_comparison.py checks finite word controls and the fixed-point obstruction, while the universal claims follow from the explicit arguments here.

## Chronology and search-claim challenge

The peer's 52-query / 14-batch claim matches the actual ledger count. Its result statements are batch-level discovery descriptions and retain negative-search limitations. The two Ballier citing records are explicitly catalog outputs, not an exhaustive citation claim. The metadata-only/unread leads are not used for a title-only exclusion.

The peer correctly separates Ballier's January 2013 arXiv record, October 2013 online publication and May 2015 issue from an inconsistent 2018 template received line. Salo–Törmä's actual fetched v2 is dated June 2018; its 2015 journal citation is not a certification that every v2 statement appeared identically then. This distinction is retained. The peer's journal/manuscript and inaccessible-body gaps remain open.

The peer also correctly credits PRZ's old general LT bound and avoids treating mathematical PASS as originality evidence. My independent automata-family pass additionally checks the 2013 v1 product bound, Costa's earlier membership/pointlike bridges, later profinite block-code work, presentation algorithms, and 2025/2026 application leads. Those add bounded coverage; they do not turn either search into an exhaustive historical exclusion.

## Remaining challenge boundary

The sealed peer packet is defensible only with its current bounded wording. Its phrase 'authored reduction' identifies the audited proof's location, not historical novelty. Published Barth–Dykstra, Ballier VOR, other source versions and unread leads remain unresolved. My own additional unread gaps are listed separately. No claim that the full criterion already exists has been proved, and no claim that it is original has been proved. The parent must retain that distinction in any public synthesis.

No sourceproof, peer artifact, Git state or external account was changed; no individual or peer agent was messaged.
