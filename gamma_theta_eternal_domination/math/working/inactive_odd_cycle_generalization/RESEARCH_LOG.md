# Research log: inactive odd-cycle generalization

## 2026-07-28 PDT

- Read the accepted inactive-\(C_5\) certificate, C-108 target-response
  propagation, C-111 exact-two-list physicality, and C-113 inactive-link
  suspension theorem.
- Generalized the local SAT template to arbitrary rim length.
- Exhausted all 877 restricted-growth strings for \(C_7\) in discovery
  mode; every formula was UNSAT.
- Quotiented the 877 equality patterns by the dihedral action on the rim,
  obtaining 93 orbits with sizes \(1,7,14\).
- Generated and checked one DRAT proof for every orbit representative.
- Wrote a separate checker that independently enumerates all partitions,
  rebuilds the orbit map, reconstructs each DIMACS instance byte-for-byte,
  verifies artifact hashes, and replays all 93 proofs.
- Independent replay passed: 1,418,936 clauses reconstructed and 1,739,039
  proof bytes verified.
- Derived the human private-star propagation lemma and its distance-two
  inactive-path exclusion.
- Identified the stronger path-parity statement as the exact
  length-independent target.  A two-edge recurrence using only endpoint
  family membership is false as a local shortcut; additional dynamic state
  is required.
- Verified a uniform even-cycle product-family construction, showing the
  local theorem is parity-sharp.
- Ran one all-distinct-witness \(C_9\) discovery instance; it was UNSAT, but
  no complete partition coverage or certificate claim is made.

## Exact current boundary

- Certificate-backed candidate: no local inactive witnessed \(C_7\).
- Consequence after hostile review: in the equality-critical target branch,
  the inactive complement has no induced \(C_3,C_5,C_7\), so its shortest
  possible odd cycle has length at least nine.
- Open: arbitrary inactive odd cycles and the path-parity induction.
