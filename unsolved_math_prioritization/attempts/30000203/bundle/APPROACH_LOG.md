# Five substantive approaches and research log

Problem 30000203 / OWR-793-006. All times UTC on 2026-10-04. These are five substantive mathematical approach responses, not a count of tool calls. Literature retrieval and control reruns are not hidden extra proof attempts. No complete universal candidate was obtained.

## Readiness checkpoint, 10:58--11:00

The catalogue request failed with HTTP 403. The pinned source record was checked against the official OWR report, p. 692, Question 4, and the full question in the 2006 author-upload text. The live queue had rank 601, queued, 0/5. No matching previous state, attempt directory, exact-ID branch/PR, or title-keyword PR was found. The current assessment and original individual review were read; the one-coordinate suggestion is specifically tested in approach 1. No matching prior research-results record was found in the pinned corpus. A later related-target scan found no other record with “subdegree” or “twisted wreath” in its title/statement.

No verified later resolution was located. This is a bounded negative literature search, not proof that the problem remains open everywhere.

Completion estimate toward the universal research goal: 10% (subjective workflow estimate).

## Response 1: stabilizer optimization and support-one route

Mechanism: replace an enormous orbit problem on T^k by maximizing admissible subgroups of P; test whether the obvious one-coordinate point gives strictness.

Outcome: Propositions 1--2 in PARTIAL_RESULTS.md prove s = |P|/M and show that a point supported in one coordinate from a shortest component orbit has orbit exactly k m. This independently reconstructs the established Section 4 construction. It is not a new universal improvement.

Exact gap: find an admissible R with |R| > c in all primitive data, or exclude all such R in a counterexample. The reformulation alone leaves that task untouched.

Checkpoint: reduction and its obstruction established during 10:59--11:01; written proof frozen at 11:12. Estimated progress toward universal resolution: 15%.

## Response 2: local normalizers and extension of a shortest-class stabilizer

Mechanism: enlarge C_t by a subgroup of N_P(C_t)/C_t disjoint from the induced Q-subgroup.

Outcome: Proposition 3 proves the quotient criterion and a prime-divisibility sufficient condition. Proposition 4 shows that the shortest-component-class strategy fails in A5 twisted by A6: for every 5-cycle t, every admissible R has order <= 5, so this value can do no better than index 72. The normalizer is entirely inside Q. A stronger witness must use another component class.

Exact gap: no universal splitting or escape from Q is provided by primitivity. Restricting to minimum-class values would miss the real minimum even in the smallest example.

Checkpoint: local-extension criterion and finite obstruction developed during 11:01--11:05, then included in the written proof. Estimated progress toward universal resolution: 10%.

## Response 3: Sylow p-groups and fixed-point congruences

Mechanism: a p-group action on B has a positive multiple of p fixed points whenever p divides |T|, forcing a nonidentity point fixed by a Sylow subgroup of P.

Outcome: Proposition 5 proves a p'-subdegree dividing |P|/|P|_p, and strictness whenever |P|_p > c. It gives strict bounds 45 and 40 against 72 in the A6 example. An exact A20/A19 countercontrol shows the numerical premise can fail for every prime, despite valid primitivity.

Exact gap: combine the prime-power information into a larger stabilizer or use an entirely different subgroup. No such combination is proved.

Checkpoint: fixed-point mechanism and A20 obstruction developed during 11:03--11:07; factorial controls passed. Estimated progress toward universal resolution: 8%.

## Response 4: double-coset fixed points and Burnside averaging

Mechanism: parameterize B^R as a product of centralizers indexed by R\P/Q, compute orbit counts, and compare the average orbit size with k m.

Outcome: Proposition 6 proves the exact parameterization. For A5 twisted by A6, Burnside gives 129607960 orbits on 60^6 points, and the nonidentity average exceeds 72. Thus the global average test fails to detect a real orbit of size 15. Counts were computed using groups of order at most 360, without generating the socle's points.

Exact gap: isolate rare large stabilizers. The average-size inequality is too weak even in the base example.

Checkpoint: formula and exact Burnside test implemented and passed during 11:05--11:07. Estimated progress toward universal resolution: 5%.

## Response 5: elementary finite extremal analysis and class-size consistency controls

Mechanism: use the small subgroup orders and involution fixed points in A6 to prove the exact minimum; test the alternating-group class assertions that would support an extension to a family.

Outcome: Proposition 7 proves s = 15 for A5 twisted by A6, using an order-24 even partition stabilizer and an elementary exclusion of admissible subgroups larger than 24. Independent enumeration of all 501 subgroups confirms the maximum 24 and shortest-class maximum 5. Proposition 8 proves the A8 component minimum 105 and verifies strictness for the A9/A8 datum using a 3-cycle witness of index 168.

Two numerical source cautions were identified and carefully scoped: the accessible 2006 author-upload formula overlooks the A8 class-size exception; a visually verified 2021 author manuscript assigns 12 to the A5/A6 example where the proof gives 15. Neither is a resolution of the original problem. No novelty claim or outreach was made.

Exact gap: all other primitive twisted-wreath data remain outside these finite proofs. The partition control through degree 30 is bounded evidence, not an infinite-family classification.

Checkpoint: exact controls first passed at 11:07; written proofs completed at 11:12. Estimated progress toward universal resolution: 5%.

## Budget disposition

Five approaches used; no complete candidate and no verified prior solution. Retain unsolved, 5/5. An independent audit may verify these frozen partials and expose errors; it must not turn into additional research turns toward an unfinished universal proof. The queue proposal changes only this target's Status and Turns. No Findings edit, remote write, release, or external communication was performed.
