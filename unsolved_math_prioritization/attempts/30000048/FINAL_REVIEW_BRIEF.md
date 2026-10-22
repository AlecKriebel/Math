# Problem 30000048: frozen five-turn review packet

## Original conclusion

**Unresolved after five substantive author turns; attempt exhausted.** No full candidate proof or counterexample is presented. The requested original concerns every connected simply connected compact Lie group and every pointwise nonnegative integral virtual complex character with normalized Haar mean one. Positivity is pointwise, not a condition that all irreducible coefficients be nonnegative. The desired conclusion is equality with one irreducible character's square modulus.

The complete source gate and primary URLs are in SOURCE_GATE.md. Serre's original SU(2) result is credited prior work. The 2025 source still states the general classification as Problem 4.6. No worldwide novelty certification is made for any retained partial.

## Claims requiring independent review

1. TURN_1.md: classification for every SU(2)^r, using integral polynomial domination and the rank-one Laurent equality case. This is the only result here covering arbitrary products.
2. TURN_2.md: exact finite classification in the five center-neutral SU(3) irreducibles (0,0),(1,1),(3,0),(0,3),(2,2). All exclusions have actual rational group-trace witnesses; survivors have global square certificates.
3. TURN_3.md: classification of all real SU(3) virtual characters supported on a+b<=4, including every noncentral term. It depends on turn 2 and uses unit-circle trace realization plus local positivity at trace 0 or 1.
4. TURN_4.md: all-weight classification of the affine-single-irrep family 1+c chi, and of integral convex combinations of irreducible squares. It supplies the diagonal tensor multiplicity formula used next.
5. TURN_5.md: all-weight Hermitian-SOS classification on SU(3), allowing arbitrary complex character combinations and non-diagonal Gram matrices. It depends on the turn-4 diagonal multiplicity and independently proves the needed stable-strip cross multiplicity.

Turn 5 subsumes turn 4's convex-square rigidity, but does not subsume its separate explicit affine-family negative witnesses. Turn 3 covers all pointwise-positive functions in its support range, without assuming an SOS certificate.

## Exact gap

For unrestricted SU(3), an S-character outside the irreducible-square family would have to be outside the entire Hermitian polynomial SOS cone. The proof does not show that integral Haar mean one forces membership in that cone. The explicit positive Weyl discriminant has Haar mean 15 and demonstrates that positivity alone is insufficient. It is not a normalized counterexample. The classification for other higher-rank simple groups and products is likewise not established.

Do not promote any support bound, SOS hypothesis, sparse family, or convex construction into the unrestricted source claim. A proof of an unverified SOS decomposition would be additional mathematical work, not an inference supplied by this packet. The five-turn budget is exhausted; independent verification may check and correct these frozen claims but should not become a sixth search turn.

## Reproducibility

All files can be placed in one directory. The source uses Python's standard library:

    python3 verify_turn1.py
    python3 verify_turn2.py
    python3 verify_turn3.py
    python3 verify_turn4.py
    python3 verify_turn5.py

Expected receipts: turn 1, 4,072 assertions; turn 2, 19,889 assertions; turn 3, 364 new assertions plus a turn-2 rerun; turn 4, 2,265 assertions; turn 5, 11,403 new assertions plus a turn-4 rerun. These are exact algebra/finite-enumeration controls and not proof-assistant verification of the analytic or all-weight arguments. Exploratory modular probes are not used as proof.

Suggested audit priorities: the all-r divisibility argument in turn 1; soundness and completeness of the turn-2 finite bound; every center-lifting case in turn 3; the LR skew-shape bookkeeping in turns 4–5; integrality of leading Gram coefficients; non-diagonal band cancellations; boundary-mass induction; and the exact mean-15 status of the non-SOS discriminant example.

Final disposition is original unresolved, partial claims pending independent review. No completed original result is asserted by this packet.
