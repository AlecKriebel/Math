Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The final structural theorem is independent of a finite computer bound. Earlier through-nine and through-ten results retain their historical scope in unchanged companion editions. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Independent acceptance report: final tournament structure

12 October 2026 UTC. Queue row 1754 / problem 3276 / OPG-1808.

## Verdict and exact scope

ACCEPT STRUCTURAL PARTIAL, at the fixed author manifest identified in the original operational record and the original operational record. The unrestricted source-or-cyclic-rainbow target remains unresolved here. This is the audit of the fifth/final structural pass, not a sixth pass.

Accepted mathematical claims:

1. The stated three-fiber hypotheses force every offmatching backward-class pair to be an actual arc in the third selected color, and force the actual cyclic rainbow triangle 0-to-2-to-4-to-0.
2. Under those hypotheses all internal arcs in a residue class use its selected strong color.
3. A hypothetical induced-minimal counterexample cannot have a transitive direction-preserving vertex automorphism group even when every automorphism may globally permute the colors.
4. The full such group is a proper odd-order cyclic subgroup of the failed-predecessor cycle's rotations. It has at least as many orbits as the least prime divisor of the order; at prime order it is trivial.
5. The explicit all-order family F_m for odd positive m has the exact failed-predecessor structure and full twisted symmetry but contains a cyclic rainbow. It is a nonvacuous test family, not a counterexample.

The all-order theorem needs no separately accepted general finite bound, divisibility-by-nine exclusion, incidence theorem, module theorem, or orbit-CSP result. It does not establish the target for arbitrary color-permuting-transitive tournaments, because induced-minimality need not preserve ambient symmetry. It does not eliminate arbitrary strict-period-three obstruction cycle words. No novelty, priority, exhaustive-literature, or present-day open-status claim is accepted.

## Review performed

The complete frozen mathematical proof, implementation, test program, integrity checker, fixtures, source note, and verification note were inspected. The independent proof review is STRUCTURAL_PROOF_REVIEW.md. The primary source lemma and surrounding general-minimal-counterexample hypotheses were read from the complete recovered text; exact PDF/text identities and public bibliographic verification are recorded in that review. No source PDF or copied source text is included.

No mathematical correction was required. Before freezing, wording that could imply the kernel automorphism had been proved necessary was narrowed to say that the proof uses it. The first frozen checker failed its own corruption self-test because copied read-only payloads could not be mutated. Acceptance was withheld. The checker was repaired to make only temporary control copies writable, refrozen, and freshly replayed after freezing. The final identity is the one accepted; the rejected initial freeze is separately preserved in the rollback evidence.

## Independent computation

The original checker imports no author oracle. It generates tournaments from independent unordered-pair/orbit rules and computes positive-length color closure by bit-set doubling. Diagonal reachability is added only where reflexive semantics require it. Its actual three executions use Python normal, -O, and -OO; the resulting receipts agree except for optimization metadata.

The complete restricted twisted enumeration covers:

- Order 3: all 6 encodings; 3 have the fixed exact failed-predecessor relation, all with cyclic rainbows.
- Order 9: all 1,296 encodings; 12 have the fixed exact failed-predecessor relation; their 216 ordered offmatching pairs obey both the unique possible path-color conclusion and the actual-arc conclusion.
- Order 9 rainbow-free subset: 432 encodings, all with every vertex an outgoing source; 360 have no single spanning color.

The independently built rigid family is tested at orders 3,9,15,27,45,81. Its exact counts of cyclic rainbow triples are 1,18,95,621,3060,18630. Every tested vertex fails only at its predecessor, and there are no outgoing sources. Those rainbows are why these objects satisfy the target rather than refute it.

Ten concrete false-extension controls test rainbow exclusion, exact-color versus color-twisted symmetry, periodic words without chord symmetry, nonunique class strong colors, failure of induced symmetry inheritance, monochromatic paths without direct arcs, the failed-predecessor premise, outgoing versus incoming reachability, cyclic versus transitive rainbows, and positive versus reflexive reachability. Full fixed matrices, including a 21-vertex example with all three spanning colors in every class, are preserved in EXAMPLES.md; the original independent receipts also contained them. The induced-symmetry-loss example is not claimed to be a conjecture counterexample.

The original checker compares the fixed implementation against the independent matrices and color closures. In each optimization mode it checks all 1,302 encodings, all 31,248 selected shift/color-permutation automorphism comparisons, all 15 exact-predecessor certificates, eight independently built rigid family orders, and 23 malformed-input or missing-hypothesis rejection gates. A further explicit nine-vertex matrix retains exact failure and the kernel symmetry but loses the full twisted shift: the weaker three-fiber certificate accepts it, while the full-twist certificate rejects it.

The author's verifier is also freshly replayed in all three modes, with resulting stdout bytes identical to its frozen RESULT files. Its integrity/corruption checker is run both before and after those replays in each mode against the same external manifest pin. These computations are restricted implementation evidence. The unrestricted all-order mathematical claims are supported by the separate proof, not by finite search.

## Integrity, rollback, and publication boundary

The audit's the original operational record lists the exact payload set with SHA-256 and byte counts. Its external pin fixes that manifest. The original checker checks exact file identity, scope and accepted-object bindings, optimization-mode agreement, tested counts, actual false-extension fixtures, and absence of removable assertions in the audit programs. Its fourteen corruption controls include ordinary byte/file changes and self-consistently rehashed semantic overclaims or missing evidence. All use explicit exceptions.

The external archive/store workflow retains the complete author and audit bytes and pins, extracts an actual archive into a fresh directory, compares every extracted file to its source, then reexecutes the integrity checks and substantive audit computations from the extracted tree. A separate complete-byte content store is reconstructed into another fresh tree and checked in the same way. The external terminal receipt and archive/store identities identify these actual operations; a claimed listing or archive hash alone is not substituted for extraction.

No repository write, remote publication, queue update, copied third-party document, dataset contents, private source, personal data, or private coordination content is part of this audit packet. The other finite orbit-search lane is separately reviewed and is not incorporated as an accepted premise here.
