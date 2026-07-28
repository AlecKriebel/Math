# Frozen scope and dependency checklist

Frozen: 2026-07-28 (PDT)

## Dependencies used

- [x] Standard one-guard-moves model: attacks are unoccupied, exactly one
  adjacent guard moves, and every retained state dominates.
- [x] C-094 only in its proved literal form: an exact two-list port has a
  same-list, same-sign physical representative.
- [x] The exact no-full response-formula interpretation: same-sign ports
  name the same Boolean event; a literal complement edge enforces proper
  coloring at its endpoints.
- [x] \(\gamma(G)=3\): every vertex pair has a common complement neighbor.
- [x] Direct swaps named by a response list belong to the specified eternal
  family and therefore dominate.
- [x] No inference from an absent family response to a graph nonedge.

## Scope of the proved theorem

- [x] Reference state \(S=\{a,b,c\}\) is independent.
- [x] Every outside list is nonempty and has size at most two.
- [x] The theorem applies to one original cross-clause edge with types
  \(\{a,b\}\) and \(\{b,c\}\), after physicalizing both endpoint events.
- [x] If the physical representatives are \(G\)-adjacent, a common
  complement cap exists, misses at most one anchor, and satisfies the
  list conclusions in Theorem 2.1.
- [x] The original clause and the two cap edges give the exact local
  virtual-rainbow table in Theorem 2.2.
- [x] “Derived unit” means a Boolean resolution consequence supported by
  the displayed original/cap incidences.  It is not asserted to be an
  original unit clause or a retained direct response.
- [x] The terminal-chain/lollipop/bicycle discussion is a local logical
  reduction.  It is not an arbitrary-bicycle exclusion or a one-guard
  contradiction.

## Exact controls and excluded overclaims

- [x] `MFzJbZYhlrDZdMhd_` refutes retention of two specified original
  edges by one unique same-sign physical representative.
- [x] `NFzJbZZhlrDZdMhd|h_` refutes joint physicalization of one original
  clause and realizes the exact third-color tight gate.
- [x] Both controls use their greatest eternal triple-family and have
  \(\gamma=i=\alpha=\gamma^\infty=\theta=3\).
- [x] Both controls have two compatible response-list colorings.
- [x] Neither control has an unsatisfiable response formula.
- [x] No counterexample, universal proof, finite-frontier increase, or
  order-exclusion claim is made.
- [x] The remaining unit-free tight-gate holonomy is explicitly open.

## Reproduction boundary

- [x] `verify.py` imports no campaign evaluator or search core.
- [x] It reconstructs the two graphs, greatest fixed points, all 4,539
  one-guard obligations, response lists, frozen projections,
  representative sets, cap signatures, and compatible colorings.
- [x] Frozen replay command:

  ```text
  python3 -I -B -W error \
    math/working/original_edge_core_incidence/verify.py \
    --check math/working/original_edge_core_incidence/result.json
  ```

## Frozen SHA-256 values

| File | SHA-256 |
|---|---|
| `NOTE.md` | `a36132397975352582c0051cbc9f45e9f89e33d9835e378d612ed136909deb91` |
| `verify.py` | `2a1f8ff43c0373a83e271e8ecb0b1c5117bd4e9f6da65f9ff97359eabd079efd` |
| `result.json` | `dd473b421915adf6af5a5eb900a7561ee4efae44ce365233d9f738ae64ad0481` |
| `RESEARCH_LOG.md` | `04c3fdc143078dfffcc04474f3fc659e0029e637d129a2b5224de68e8af4d738` |

