# Audit correction record

This is a separate corrected release of the original five-attempt author
package, whose manifest SHA-256 is
`93334356491d6719b98b628ebb4b011fcb6438428b46e454935d544702fd1ff7`.
The original files were not edited.

## R1: required source-hypothesis clarification

Theorem 5.1 in the corrected Chatzidakis–Zalesskii paper has a global
faithfulness convention. Attempt 1 now uses it directly only for a
faithful action. A fixed vertex is immediate from coherence. Otherwise a
nonfaithful action kernel lies in a polycyclic edge stabilizer, so it is
polycyclic and finitely presented. The quotient stabilizers are coherent
by the existing Lemma Q, the maximal-stabilizer hypothesis passes to the
quotient, and Theorem 5.1 plus the finite-decomposition criterion proves
finite presentation of K/N. The existing Lemma E lifts this to K.

The repair proves only the required finite-presentation conclusion in the
nonfaithful case. It does not add a claim that an actual graph decomposition
lifts. The dependency is acyclic: the finite-decomposition criterion is
independent of its application; Lemmas E and Q are proved independently;
polycyclic finite presentability uses Lemma E. This applies the auditor's
requested correction without a new proof-search mechanism.

## R2 and R3: portable flat-package paths

Attempts 4 and 5 now reference `chain_obstruction.py` and
`power_commutator_frontier.py` without the obsolete `checks/` prefix.
The scripts themselves and their outputs are unchanged.

## Provenance, checks, and disposition

The complete initial audit and its status are copied byte-for-byte. Their
HOLD verdict is historical and retained, not overwritten as PASS.
`CHANGE_MAP.json` lists the changed files and before/after hashes; the
portable checker verifies those hashes, the two provenance pins, and
deterministic finite-check replay.

The full problem remains unresolved, exhausted at 5/5 substantive attempts.
No sixth attempt, remote mutation, full-solution claim, historical novelty
claim, or assertion of completed narrow review is made.
