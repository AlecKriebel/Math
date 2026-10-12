Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The structural proof retains its original through-nine premise; the separately accepted through-ten application appears in BOUND_TEN_DEDUCTION.md. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Independent acceptance: transitive symmetry and the prime frontier

12 October 2026 UTC. Row 1754 / problem 3276 / OPG-1808. Fourth-pass structural partial.

## Decision

**ACCEPT the fixed structural partial. The unrestricted target remains unresolved.** No mathematical correction was required.

Author manifest: SHA-256 `[verified undistributed artifact identity]`, [verified original byte count omitted], eleven payloads. Full proof: SHA-256 `[verified undistributed artifact identity]`, [verified original byte count omitted]. The exact frozen files, implementation, verification program, examples, and claims were reviewed. Author checks were freshly replayed in normal Python, `-O`, and `-OO`; each output exactly matches its frozen receipt. The author packet was unchanged.

The target remains cyclic rainbow triangle or outgoing universal monochromatic source, with the path color allowed to vary by destination. No transitive rainbow triple or incoming sink is substituted.

## Accepted all-size conclusions

1. In any finite balanced arc-colored tournament, every vertex is an outgoing universal monochromatic source. The same holds if each actual arc lies on a monochromatic directed cycle. Any finite palette is allowed.
2. A color-preserving vertex-transitive tournament has that property for any palette. With at most three colors it has a single spanning strongly connected color. More generally, for order n>1, at most the least prime divisor of n colors suffice. No regular-action assumption is needed.
3. The palette threshold is sharp in general: the affine-line tournament on F_p^2 has p+1 colors, components of size p in every color, and no spanning color. A separate balanced three-color nine-vertex example also lacks a spanning color, ruling out replacing transitivity by balance in the stronger conclusion.
4. For every odd n>=7, the specified distance-colored circulant is cyclic-rainbow-free, colored-prime, has its whole incidence core, and has a monochromatic Hamilton cycle. For every fixed finite core bound, sufficiently large members lie outside the earlier bounded recursive quotient-core certificate criterion.
5. A hypothetical induced-minimal counterexample with a vertex-transitive group allowed to globally permute colors must have odd order divisible by nine and a strictly three-periodic obstruction-cycle word. Using the separately accepted target through nine gives order at least 27. This is a necessary condition only for the fully symmetric subclass.

The full arguments and boundary checks are in `STRUCTURAL_PROOF_REVIEW.md`. They explicitly cover singleton and unused-color cases, positive return paths versus reflexive reachability, arbitrary transitive groups, equal monochromatic SCC sizes, odd partition indices, the overlap-corrected covering inequality, the action on used colors, its kernel, and actual orbit-triangle orientation.

In particular, the unique failed-predecessor map forces every color-permuting symmetry to be a rotation; a transitive rotation subgroup is the whole rotation group. Its used-color homomorphism is nontrivial of order three. The color-preserving kernel has three vertex orbits and is not incorrectly treated as transitive on the whole tournament. At orders divisible by nine the special order-three orbit triangles are monochromatic; no further divisibility or exclusion follows from that argument.

## Classical and prior dependencies

The three-color covering argument also follows from Scorza's classical three-proper-subgroup cover theorem. The SCC block stabilizers cover the acting group, whereas a tournament automorphism group has odd order and cannot have a Klein-four quotient. The journal source inspected is Mira Bhargava, [Finiteness criteria for coverings of groups by finitely many subgroups or cosets](https://dergipark.org.tr/en/download/article-file/232921), International Electronic Journal of Algebra 2 (2007), 83–89, Theorem 1(ii). The author added this contextual attribution before its final freeze. The elementary SCC-count proof remains independent of that theorem. No dedicated standard name for this exact tournament formulation was established by the limited search, and no novelty or priority claim is made.

The obstruction-cycle premise is Shen's result as credited and reproved in Lemma 2.1 of Georgakopoulos and Sprüssel, [On 3-coloured tournaments, arXiv:0904.1967v2](https://arxiv.org/pdf/0904.1967v2). Its statement, proof, and general-minimal-counterexample setting were independently read. The local PDF and extracted text match the prior public hashes. Source byte counts, hashes, and inspection scope are recorded in `the original operational record`; no copied source document or source text is included. Web screenshot retrieval failed for the two PDFs; textual inspection succeeded, and no visual-page review is claimed.

The previously accepted module-composition argument supplies the precise recursive-certificate comparison. The separately accepted third-pass interval-pruning result supplies general target validity through nine, used only for the last order-at-least-27 conclusion. Both reports and the module proof review were inspected at their recorded hashes. This audit does not rerun the through-nine search and does not use a provisional order-ten result.

## Fresh independent verification

The audit reference imports no author oracle. It uses positive-length bit-path doubling, independently forms SCCs and outgoing-source sets, detects cyclic triples by their within-triple outdegrees, peels the incidence core one vertex at a time, and checks colored modules directly. Its group tests enumerate generated permutations or literal centralizers. Normal, `-O`, and `-OO` runs agree substantively and retain all explicit exception gates.

- All 46,879 labeled oriented three-colored tournaments through order four are independently decoded. Exact colorwise reachability, balance, arc reversal, source sets, spanning colors, and cyclic-rainbow detection match. There are 72 cycle-covered order-four cases despite none being balanced, a nonvacuous boundary for the converse.
- All 9,331 six-state oriented colored circulants at orders 1, 3, 5, 7, 9, and 11, plus all 1,296 three-color mergers/reversals of the four affine-line classes on F_3^2, are freshly tested. Every relevant transitive case has a spanning monochromatic color.
- All six frozen explicit examples are independently checked. The balanced nine-vertex example has SCC sizes five and four for each color and 11 cyclic rainbow triangles; it is not misrepresented as rainbow-free. The affine four-color nine-vertex example has three components of size three for each color.
- The eight prime full-core family examples of orders 7, 9, 11, 13, 17, 27, 51, and 101 are independently rebuilt and tested. All 10,832 proper nonsingleton subsets at the first four orders are independently checked against colored-module membership. Larger primeness follows from the reviewed all-size proof.
- The sharp-palette examples for p=3,5,7 are independently built by explicit line steps and match the candidate matrices exactly.
- The entire nonregular group generated by the nine-vertex fixture is independently enumerated: order 27, vertex-zero stabilizer order three, every element preserving colors and directions. This exercises genuine transitive action with nontrivial stabilizers and a missing third color.
- All 192 rotations of the eight twisted examples are checked with their exact color homomorphisms. All 64 order-three orbit triangles have the predicted rainbow/nonrainbow boundary. Every permutation through degree eight is tested for commuting with a full cycle, yielding exactly its rotations, over 46,233 permutations.
- A nine-vertex control retains a strict three-periodic cycle word after a chord recoloring, but the shift admits none of the six possible global color permutations. Thus periodic word alone is not promoted to full-tournament symmetry.
- Twenty-four invalid-input/certificate gates and ten actual candidate-source mutations are detected by explicit failures. Mutations cover ignored colors or transitivity, reversed source direction, merged reachability colors, uncolored balance, false arc reversal, nonreflexive singleton reachability, extra cycle-color arcs, multiple cycles, and treating transitive rainbow triples as cyclic. No timeout counts as detection.

These finite checks test implementations and examples; they do not constitute a new general tournament completion bound or replace the all-size arguments.

## Integrity, reproduction, and residual scope

`STRUCTURAL_AUDIT_REPRODUCTION.md` preserves the replay and verification description; executable commands and programs are not distributed. The author integrity checker rejects five copied-packet corruptions in every Python mode. The independent audit has a separate externally pinned exact-file-set manifest, semantic result gates, actual copied-packet corruption tests, and post-freeze checks in normal, `-O`, and `-OO` modes. Post-freeze receipts are stored outside the frozen directory.

The unrestricted target, general asymmetric colored-prime full-core cases, the fully symmetric class at order 27 and above, and arbitrary strict three-periodic obstruction cycles at unexcluded lengths remain unresolved by this work. No actual counterexample is supplied. There is no new general finite conjecture bound, no unrestricted periodic exclusion, and no formal proof-assistant claim.

No remote repository write, queue change, publication action, or further substantive pass was performed by this audit.
