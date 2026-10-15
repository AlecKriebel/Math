Editorial note: The complete authored text follows. Only references to undistributed operational artifacts, identities, byte counts, locations and replay commands are replaced by descriptive prose. Mathematical arguments, full audit findings, evidence counts and limits are retained. The original structural bound-eight application is historical and remains unchanged; the new bound-nine consequence is a separate deduction in BOUND_NINE_DEDUCTION.md. Historical candidate-review conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md.

# Independent acceptance: interval propagation and colored-module composition

Date: 12 October 2026 UTC. Row 1754 / problem 3276 / OPG-1808.

## Decision

**ACCEPT the complete fixed structural partial. The unrestricted target remains unresolved.** No author correction was necessary.

The accepted author manifest is SHA-256 `[verified undistributed artifact identity]`, [verified original byte count omitted] and 11 payloads. Its full proof is SHA-256 `[verified undistributed artifact identity]`, [verified original byte count omitted]. Exact file-set, byte-count and hash verification precedes and follows the independent checks. The candidate was not modified.

## Mathematical acceptance

The complete all-size arguments were independently reviewed, including nonempty finite tournaments, at most three colors, outgoing reachability, distinct endpoints, simple paths versus same-color walks, singleton cases, and positive return cycles versus zero-length paths. `STRUCTURAL_PROOF_REVIEW.md` records the reasoning.

Accepted results are:

1. Sound terminating mandatory-interval propagation using possible actual chords for local paths and a separate global virtual reachability closure. The result is a necessary relaxation only.
2. Exact color-by-color reachability and universal-source formulas for uniform colored substitution, including same-block paths that leave and return through a positive monochromatic quotient cycle.
3. Exact cyclic-rainbow transfer, substitution closure of the target, and colored-primeness of every induced-minimal counterexample.
4. The recursive quotient-core sufficient criterion for arbitrary finite colored-substitution trees. Its empty-quotient-core instance is computation-independent; its bound-eight application uses the separately accepted finite theorem through eight.
5. The depth-d family of order 3^d whose quotient cores are all empty but whose entire incidence cores survive for d>=3. This is an unbounded strict extension of the earlier whole-core-size criterion.

Direction and color uniformity are both necessary. Blocks are nonempty. The proof does not assume a quotient is automatically an induced subgraph for arbitrary contractions; for colored modules, keeping one representative per block gives the required induced representative. The source formula does not conflate reflexive reachability with a positive return cycle. The finite-bound core premise covers every smaller possible minimal counterexample, not merely the core itself.

## Source and dependency checks

The source is Georgakopoulos and Sprüssel, [On 3-coloured tournaments, arXiv:0904.1967v2](https://arxiv.org/pdf/0904.1967v2), dated 17 April 2009. Its recovered PDF hash is `37c70064ec08aba920ed480061d68328341e61a0ddb2738a7100fb0d75660279` ([verified original byte count omitted]); extracted text hash is `[verified undistributed artifact identity]` ([verified original byte count omitted]). Source text and the rendered page containing Lemma 2.5 were checked. Shen is credited through source Lemma 2.1; Lemma 2.5 supplies proper-interval existential-color reachability; Proposition 2.4 and Theorem 3.1 remain cited incidence dependencies. The full source proof is not newly certified here.

The prior recovered structural proof has hash `[verified undistributed artifact identity]` ([verified original byte count omitted]), and its recovery acceptance report was inspected. The separate recovered finite-search report has hash `[verified undistributed artifact identity]` ([verified original byte count omitted]), accepting the general target through eight and the separately specified periodic cases. This audit does not replay that earlier enumeration and never substitutes an unaccepted order-nine premise.

No copied source text or PDF, private source, dataset contents, or private coordination record is included in this audit packet. There is no novelty or current-literature-status claim.

## Fresh independent verification

The author checker was replayed under ordinary Python, `-O`, and `-OO`. Each output exactly equals its matching frozen receipt. The frozen integrity checker in each mode rejects five copied-packet corruptions: changed proof, changed receipt, missing payload, added payload, and self-consistently rehashed but externally unpinned manifest.

The independent checker imports neither the author test script nor its Boolean-matrix oracle. It independently decodes every six-state tournament, constructs substitutions directly from vertex/block labels, computes positive monochromatic reachability by repeated bitset path doubling, detects directed triangles by their within-triple outdegrees, and computes cores by serial one-vertex deletion. Fresh normal, `-O`, and `-OO` runs agree substantively and use explicit exception gates.

- All 74,389 quotient-order-one-to-three substitutions with every factor a singleton or colored directed edge are rechecked, plus all 2,592 two-vertex quotient substitutions with an arbitrary three-vertex factor in either position. Total: 76,981. The checks include exact expanded matrices, full color-by-color reachability, outgoing source sets, positive return colors, rainbow equivalence, and quotient reconstruction.
- All 1,728 author-scope known-model interval fixtures are independently rebuilt using the new reachability oracle. No real model is removed and no false reachability is asserted. Exactly 7,620 domain states are pruned; all returned relations are reflexive and transitive. This is not an always-accept or vacuous test family.
- The four regular recursive examples of orders 3, 9, 27, 81 are independently expanded and checked, including whole-core sizes 0, 0, 27, 81. Forty-eight further deterministic heterogeneous recursive certificates, including singletons and unequal child sizes, are independently expanded and checked, with orders up to 40.
- Twenty-six invalid matrix, block, factor, certificate, domain, endpoint and seed inputs are rejected. Additional gates reject a color-nonuniform block, a direction-nonuniform block, a cyclic rainbow quotient, and the undecomposed 27-vertex core under bound eight. Singleton boundaries are checked directly.
- Twelve actual candidate-source mutations are detected: omitting return cycles; counting reflexive paths as cycles; reversing quotient reachability; ignoring quotient-source eligibility; merging reachability colors; omitting color uniformity; omitting all cross-block uniformity; omitting global transitive closure; omitting the unique forced virtual path; admitting global virtual edges as interval witnesses; ignoring forbidden pairs; and reversing the forced path.

Finite tests verify implementations and counterfixtures. The all-size conclusions rest on the reviewed arguments and explicitly credited dependencies. No tournament-completion bound is inferred from these substitution counts, and no proof assistant is claimed.

## Reproduction, seal and frontier

Run The original full independent mathematical and implementation replay under ordinary Python., The original full independent mathematical and implementation replay under Python -O., and The original full independent mathematical and implementation replay under Python -OO. for the independent checks. `the original checker` pins the candidate and replays its frozen checks. the original pinned audit integrity and hostile-control check verifies this sealed audit and its semantic receipt scopes; it does not replace the mathematical replay. Post-freeze verification and terminal records are kept outside the sealed directory.

The unresolved cases include colored-prime tournaments with large cores and no useful accepted recursive certificate. A nonrejecting interval fixed point is not a completion. This work proves no unrestricted target, no unrestricted strict three-color-periodic exclusion, no general upper bound on minimal-counterexample order, and no new finite tournament bound. No remote repository, queue, or publication write was made, and no new substantive research pass was started.
