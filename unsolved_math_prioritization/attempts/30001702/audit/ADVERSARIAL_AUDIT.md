# Independent adversarial audit: minimal simplicial-cell torus facets

## Verdict

ACCEPT the frozen packet as a rigorous partial result with the status PARTIAL_UNRESOLVED. No mathematical correction or code correction is required for its stated claims. This is not acceptance of a solution of the universal factorial lower-bound problem, nor of realizability of either three-dimensional numerical vector. Five approaches were documented; no extra approach is being counted by this audit.

The original author ZIP has SHA-256 6bc7b4cc916c38afbc1f7a6289e0dd9643f577d17778ecc79524c1f4646a538b. Its independently supplied manifest has SHA-256 9516d60833e6f198eea54faf502f70d151aafe39ed26504ae9be3af05b22bab4. Both anchors, all seven payload bytes, ZIP entry modes, and the exact inventory were checked before execution. The originals were not edited or rebuilt.

## Accepted mathematical claims

1. For every regular simplicial-cell decomposition of T^d, the exact h-double-prime formula yields f_d>=C(2d,d), with the stated vertex refinement for d>=2.
2. The factorial target is attained and minimal in dimensions one and two.
3. It is attained and minimal within the explicitly defined class of regular finite-index quotients of unimodular lattice triangulations.
4. In dimension three, a counterexample to the 24-facet target would have exactly five vertices, underlying simple graph K_5, and f-vector (5,27,44,22) or (5,28,46,23). The facet-type parity restrictions also hold.
5. The elementary staircase-product calculation and the exponential cup-product bound do not close the universal factorial gap.

EXPANDED_LEMMAS.md gives full independent arguments for the difficult category, coloring, dipole, parity, and lattice-regularity obligations. The imported h-double-prime nonnegativity/symmetry theorem and contracted crystallization theorem were checked in their primary sources with their hypotheses intact.

## Attempts to break the proof

- A one-vertex two-triangle torus is excluded by regularity. It is not an admissible counterexample.
- The Basak–Datta bound cannot be applied directly to a five-vertex poset. The report instead uses it for four vertices and supplies a valid reduction only when a proper four-coloring exists.
- A c-edge between different c-deleted graph components is a genuine 1-dipole: a second edge of another color would contradict that component separation. The represented three-manifold is PL, and cancellation preserves the regular simplicial-poset model through the colored graph construction.
- The theorem imposing even facet count when an interior h-double-prime coordinate vanishes does not invalidate either numerical candidate. The 22-facet case is even; the 23-facet vector has no vanishing interior coordinate.
- The parity argument uses the target boundary-of-simplex chain map. It does not require the two source tetrahedra around a triangle to have different missing-vertex types. The expanded proof makes this distinction explicit.
- Counting vertex residues alone would not prove regularity for arbitrary quotient complexes. Here the face-to-face geometric intersection property of the Kuhn triangulation supplies the required closed-cell embedding argument.
- Homology does not prove homeomorphism to a torus. The author supplies the necessary geometric quotient identification independently of its finite checks.
- Neither arbitrary flatness nor unimodularity is smuggled into the general problem.
- Ayzenberg's cited minimality concerns vertices of the dual simplicial decomposition, not the number of its simplicial facets. Basak's inspected mapping-torus construction does not license an identity-monodromy assumption.

No claim-breaking counterexample or missing hypothesis was found within the stated scope. The audit does not establish that either numerical candidate is realizable, impossible, or the only obstruction to stronger variants of the problem.

## Source and dataset identity

The complete catalog, complete problem corpus, and complete research-results corpus were independently read and hashed. Counts were 15,458, 15,458, and 6,701. The target is catalog rank 833, problem ID 30001702, problem number OWR-4798-027. The statement hash and the specified combined-record review hash exactly match the author's metadata. Only hashes, byte counts, matching results, and public identifiers are included in SOURCE_AUDIT.json; none of the datasets or record contents are included.

All seven cited source PDFs were independently retrieved from their public primary URLs. Every fresh PDF has the same byte count and SHA-256 digest as reported by the author. Fresh text extraction was used, and printed OWR page 398 was rendered and visually inspected. Definitions on pp. 396–397 and Problem 7 on p. 398 establish the exact category and question. The nearby Problem 6 is not silently treated as solved.

The 2026 published Avvakumov–Karasev article was checked directly on its publisher's full-text page, including its current Corollary 1.2 and proof. Its conclusion is still exponential. A bounded supplementary literature search did not identify a general resolution. This is not an exhaustive literature-absence claim. Repository prior-attempt searches asserted by the author were not independently repeated in this audit and are not certified by its acceptance verdict.

## Executable verification

The independent diagnostic implementation imports no author module. It uses a different cell-orbit normal form, polynomial expansion for h-vectors, sparse-set boundary elimination, explicit subset-incidence tests, and an actual boundary matrix for the parity kernel.

Results:

- 11,475 arithmetic checks through d=150
- 900 product-gap checks
- The two numerical candidate vectors reproduced by enumeration starting from facet counts
- All 32 parity vectors checked against the boundary matrix of the 4-simplex boundary
- Explicit regular Kuhn quotients in dimensions 1–5, including all Boolean lower-interval incidences, boundary squared zero, two facets per ridge, and mod-2 Betti numbers
- The d=5 Betti check, additional to the author's range, gives (1,5,10,10,5,1)
- Extra regular quotients (d,q)=(2,4),(3,5)
- Nonregular q=d quotients rejected for d=1,...,5
- An explicit 26-facet colored expansion and 1-dipole cancellation restoring the exact 24-facet graph
- Exact sign-pattern controls through d=10

The author verifier was exercised 78 times: four genuine positive runs (normal/optimized, original/relocated), 72 expected negative runs across 36 mutations in normal and optimized modes, and two expected positive demonstrations of its documented trust boundary. Every outcome matched its expectation. AUTHOR_CONTROL_RESULTS.json includes the diagnostics.

The trust-boundary demonstrations replace both explanatory prose and the caller-supplied manifest. The author verifier accepts such a replacement because it is an integrity/replay tool, not an independent authenticator or theorem prover. This is already accurately disclosed in the author's README. The audit runner separately pins the original manifest and archive SHA-256 values before trusting them. Arbitrarily rehashing a changed packet does not make it the accepted original.

## Acceptance boundary and disposition

The safe audit ZIP contains authored analysis, independent code, replay results, acceptance metadata, public source identifiers, and hashes only. It contains no third-party PDF, extracted source text, page image, dataset content, or private coordination file. No remote publication or other remote mutation was performed.

There is no correction patch because the audited partial result did not require one. The expanded parity explanation is an interpretive clarification, and the extra finite checks are supplementary verification rather than a modification of the original proof. The exact original status remains PARTIAL_UNRESOLVED.
