# Five-turn research log

Problem: 30004319 / OWR-17295-003. All times below are UTC on 2026-10-04.
These are five substantive approach responses, not a count of tool calls.
Completion estimates are subjective progress heuristics toward the exact
unrestricted problem, not confidence levels or fractions of a proof.

## Source and duplication checkpoint, 11:07

The original OWR question was recovered after the catalogue endpoint returned
HTTP 403. Wiedemann's 2024 §5.3.3 explicitly leaves the target open; the 2024
rank-three classification is inapplicable. Live queue: rank 602, queued, 0/5.
No attempt directory for 30004319, no matching problem-ID or alternativity PR,
and no related-target-group entry were found. The prior desk review suggested
Hall–Witt and warned about missing independent root directions. Its judgement
was treated as a hypothesis. Estimated progress: 3%.

## Turn 1: propagate unit Moufang identities

**Mechanism.** Use the published strong-unit Moufang result, then remove a
nuclear summand from the repeated argument of an associator.

**Proof response.** Lemma 1 and Proposition 2 in `PROOFS.md`: alternativity
holds under R=R^×+N(R), with integer-unit-shift and division special cases.
Both left and right laws are proved without dividing by two.

**Failed extension.** The grading provides no proved unit-density or
nuclear-translate theorem. Additive generation by units leaves mixed quadratic
terms. A generic scalar translate with bijective L and R is not automatically
a strong unit; Turn 3 supplies an explicit obstruction.

**Disposition.** Partial, exact target unresolved. Estimated progress: 8%.
The exact polynomial shift controls were replayed at 11:15:24.

## Turn 2: positive-root collection and higher-rank identities

**Mechanism.** Try to extract the alternative laws from nested commutators,
positive-root uniqueness, and the Hall–Witt strategy that works in rank three.

**Proof response.** Proposition 3 constructs the positive-root group H(R)
for every distributive ring. Its associativity and faithful three-root
coordinates require no associativity or alternativity in R. The A2 positive
root system has zero length-three nested root chains; A3 has such chains.

**Obstruction.** Positive-root-only identities cannot settle this question.
Negative roots and their compatibility with Weyl elements must enter.
This blocks the particular rank-three transplant, not all commutator methods.

**Disposition.** Partial route obstruction. Estimated progress: 7%.
Finite positive-group controls completed at 11:10:49; symbolic root checks
completed at 11:15:24.

## Turn 3: exact small-ring search

**Mechanism.** Enumerate every unital bilinear product on F2³ with fixed unit
and test the actual strong-unit Moufang identities, including all ring elements.

**Proof response.** All 4,096 labelled tables were exhausted. Exactly 76
are alternative, all associative in this family. There are 3,900 nonalternative
unit-test survivors. The first gives an explicit ring R0 with e²=ef=f²=0,
fe=1, only strong unit 1, and two explicit alternative-law failures.

**Obstruction.** Necessary identities are too weak to establish the existence
of a full group. R0 is subsequently rejected by Turn 5. Ordinary two-sided
inverses and invertible multiplication matrices would give false positives.

**Disposition.** Exact finite evidence and an algebraic insufficiency example;
no group counterexample. Estimated progress: 8%. First exhaustive run 11:10:49.

## Turn 4: Lie and matrix representations

**Mechanism.** Try to transfer known root-graded Lie-algebra structure through
a canonical matrix or operator representation of the abstract group.

**Proof response.** The cyclic Jacobi expression for aE12,bE23,cE31 in the
naive matrix commutator algebra is the diagonal of the three cyclic
associators. Jacobi there forces full associativity. Elementary shears using
left multiplication operators force the same identity.

**Obstruction.** These constructions exclude known nonassociative alternative
parameter rings. A valid faithful Lie construction is extra structure, not
part of the group axioms. Thus citing the Lie classification alone does not
answer the group question.

**Disposition.** Proved obstruction to the explicit representation route.
Estimated progress: 7%. Free nonassociative symbolic check: 11:15:24.

## Turn 5: full six-root presentation and opposite-root compatibility

**Mechanism.** Retain all six roots and exploit the fact that an element
centralising two others also centralises their commutator.

**Proof response.** Lemma 4 and Proposition 5 establish (Z): ab=ca=0 implies
(bc)(at)=(ta)(bc)=a((bc)t)=(t(bc))a=0 for every t. This proves R0 cannot
coordinatise an A2-graded group. Exhaustively applying (Z) rejects 3,324 of the
3,900 nonalternative unit-test survivors, leaving 576. All 76 alternative
control tables pass. A separate coordinate implementation independently checks
R0 and the simple surviving ring R1 with e²=f²=0, ef=fe=1.

Proposition 7 states and proves the exact universal-group reduction. The
unrestricted problem is equivalent to forcing alternativity from root-map
injectivity and positive-system nondegeneracy in S(R).

**Exact gap.** Neither these two obligations for a nonalternative ring nor a
general theorem excluding them has been proved. The remaining 576 tables are
not claimed to coordinate groups. No further proof-search turn is hidden in
the verification or source-check steps.

**Disposition.** Unsolved, 5/5. Estimated progress: 10%.
Opposite-root exhaustive check: 11:12:04; final combined rerun: 11:14:00;
independent witness check: 11:15:24; full written proof checkpoint: 11:18:14.

## Final boundary

This is an unresolved partial-results package. There is no claimed solution,
no prior-resolution claim, and no novelty claim. The appropriate mathematical
status is `unsolved`, with `turns_used=5`. Independent review may verify or
correct these artifacts; it must not be counted as evidence that the original
problem is solved.
