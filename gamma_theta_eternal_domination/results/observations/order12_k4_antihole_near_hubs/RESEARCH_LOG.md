# Research log: order-12 anti-\(C_7\) near-hubs

## 2026-07-26T02:33:44-07:00

- Started from accepted C-038 templates
  \(C_5,C_7,\overline{C_7}\) and the accepted hub constraints.
- Tested every one-vertex extension of \(C_7\) by its cycle-neighborhood.
  The only extension requiring five guards is the isolated extension.  Thus
  the accepted anti-\(C_7\) no-hub condition is sharp for one outside vertex.
- Tested all ordered nonempty pairs of cycle-neighborhoods and both choices
  of the edge between the two outside vertices: \(127^2\cdot2=32{,}258\)
  nine-vertex graphs.  Exactly \(2{,}282\) require more than four guards.
- Isolated a proof-sized sharp pattern.  If both outside vertices have
  cycle-degree one, the nine-vertex graph has one-guard eternal domination
  number four exactly when the pair is adjacent and has the same unique
  cycle neighbor.  All other \(91\) labeled ordered cases have value five.
- Reduced the unequal-neighbor obstruction to three dihedral cases.  Each
  has a forced independent four-configuration, one first attack, and one
  second attack after the sole dominating first response.
- Combined the common-gap conclusion with P3.  Three explicitly chosen rim
  triples have no common neighbor inside the anti-\(C_7\) and together cover
  its rim.  If four of the five outside vertices are near-hubs with the
  common gap, the sole remaining outside vertex must witness all three
  triples and becomes a forbidden full hub.  Therefore at most three
  near-hubs can occur; the incidence subbranch with at least four is empty.
- Drafted
  `math/lemmas/order12_k4_antihole_near_hubs.md`.  No novelty claim is made;
  no literature audit was performed.

## 2026-07-26T02:47:37-07:00

- Froze the proposed note at SHA-256
  `39182554433e413741f15d7c70e89d07389c8d1ebd658ab74c39bc596fc825c5`.
- Added a clean-room greatest-fixed-point probe.  It checked all 128
  one-vertex cycle attachments, all 98 ordered singleton-spoke pairs, the
  three explicit two-attack certificates, all 49 stable-triple avoidance
  cases, and 896 rotated P3-cap neighborhood patterns.
- The probe returned
  `PASS_PROPOSED_LEMMA_REGRESSION`; exact output and resource use are frozen
  in `reviews/order12_k4_antihole_near_hubs_probe.log`.
- No solver was launched for the structural result.  The note remains
  `PROPOSED_PENDING_INDEPENDENT_HOSTILE_REVIEW`.

## 2026-07-26T03:12:00-07:00

- The independent hostile audit accepted Theorem 1, Corollary 3, and
  Theorem 4 with verdict
  `ACCEPT_PROVED_LOCAL_LEMMAS_WITHOUT_SCOPE_INFLATION`.
- The requested editorial revision makes explicit that the displayed
  independent four-set and the assumed upper bound give
  \(\gamma^\infty=4\), so a four-guard eternal family exists.  Reversing
  only that clarification and the status label reproduces the originally
  frozen note byte-for-byte.
- The independent probe uses a separate `frozenset` configuration-digraph
  evaluator.  It checked 98 two-spoke graphs, 49 independent-five-set
  witnesses, all three attack-table rows, and 896 P3 cap cases; a fresh
  replay exited zero.
- The accepted theorem excludes only the subbranch with four or five
  near-hubs.  The full anti-\(C_7\) branch remains open, and neither novelty
  nor a finite-slice exclusion is claimed.
