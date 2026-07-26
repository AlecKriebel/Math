# Complement/local-balance attack evidence log

- Date: 2026-07-26 14:55 PDT
- Base repository commit: `0f9f72d32f5d85d5ddf04b8a8dadc5c089370528`
- Model: attacks only at unoccupied vertices; exactly one adjacent guard
  moves; every successor dominates.
- Production solver or proof checker invoked: no.
- Largest graph inspected: 11 vertices.

Command:

```text
python3 -I -B -W error gamma_theta_eternal_domination/math/working/universal_complement_local_balance_attack_evidence/probe.py
```

Result: `PASS` (exit status zero).

The probe checked the following diagnostics.

1. On `C4`, it replayed the four-move loop
   `02 -> 12 -> 13 -> 01 -> 02`; all attacks were unoccupied, every move
   followed one edge, every state dominated, and the two physical guard
   labels were exchanged.  It recomputed
   `(gamma,i,alpha,gamma_infinity,theta)=(2,2,2,2,2)`.
2. On `C7`, it replayed the seven forced maximum-independent-state moves
   `024 -> 025 -> 035 -> 135 -> 136 -> 146 -> 246 -> 024`.  The final
   labels at vertices `0,2,4` were respectively the initial labels
   `2,0,1`, a three-cycle.  It recomputed
   `(3,3,3,4,4)` and verified in `H=bar(C7)` that every pair has a common
   neighbor, all seven maximal cliques are triangles, and all vertex links
   are bipartite.
3. For the accepted deep near-miss `J@l|bfNuVK_`, it recomputed
   `(3,3,3,4,4)`.  Its complement has the all-pairs common-neighbor
   property, eight maximal triangles, and bipartite vertex links.  The
   simultaneous three-guard kernel sizes were
   `110,105,100,88,64,10,0`; all eight maximum independent triples survived
   through level four, six survived level five, and none survived level six.
4. It streamed all 853 connected unlabeled order-seven graphs.  Sixteen had
   `(gamma,i,alpha,gamma_infinity,theta)=(3,3,3,3,3)`.  Four of their
   complement flag complexes had first mod-two homology dimension one:
   `FCpbO`, `FCpbo`, `FCXfO`, and `FCZbg`.  This scan is diagnostic only;
   the main note gives a self-contained proof for `FCpbO`.
5. On those sixteen equality graphs it checked the family-response Hall
   inequality for 103 maximum-independent reference states and 986
   independent outside sets.  It found zero violations.  This finite scan
   is diagnostic only; Lemma 5 in the note has a definition-level proof.

Frozen hashes at this log entry:

```text
working note
ed88c3ace73acc061bab41e8d7ab9a7a74ede1d739ef9c3aae9ed05b38aa0772

probe
327424e37242aafd7da0cf0e06774fcb0ecf25d5fa7669d7837cbb8f478209df
```

Status boundary:

- The hand proofs in the working note are labeled `PROVED`, pending
  independent hostile review and any novelty audit.
- The order-seven scan and the direct properties of the named deep
  near-miss are `OBSERVED` diagnostics, except where they repeat accepted
  C-023/C-026 records.
- No universal proof, counterexample, finite exclusion, or new minimum-order
  bound is claimed.
