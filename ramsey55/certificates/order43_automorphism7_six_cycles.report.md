# Order-7 automorphism branch at order 43

Evidence status: **EXACT ENCODING VERIFIED; SOLVE UNRESOLVED**

This branch concerns graphs admitting an automorphism with cycle structure
\(7^6 1^1\). It does not cover arbitrary order-43 graphs.

## Exact orbit formula

The prescribed action partitions the 903 unordered pairs into 129 orbits of
size seven. Each orbit is one Boolean edge-color variable. Exhaustively
mapping all \(\binom{43}{5}=962{,}598\) five-sets gives 136,848 distinct
edge-orbit signatures and 273,696 positive/negative Ramsey clauses.

An independently written checker reconstructed the permutation, all 129 edge
orbits, every five-set signature, every clause, and all metadata fields. It
matched the formula exactly.

- CNF SHA-256:
  `8045d463f68d78a745e18bb02ccc7d49fa02b47176a7282b1ef6f436fb109eb1`
- metadata SHA-256:
  `04f18fdcf4d50bda27580e1653f99f423d9799ba1ddbf0e95b1683542e6b7a56`
- independent checker result SHA-256:
  `091060845957d7d8cd7b19fbeeee5b9f91f4a96da0828be5617e506ca47b1748`
- formula plan SHA-256:
  `c9635c7778cfbe5159ba1f83a180d159a87cd3665094166a831db51a93dffc5e`

## Solver outcomes

The proof-producing Glucose run was interrupted without a solver result when
its hidden proof tempfile caused free space to cross the immutable 2 GiB
reserve. The tempfile was released on termination. No DRAT, LRAT, SAT, or
UNSAT result was produced.

A separately preregistered proof-free portfolio then gave:

| Solver | Registered conflicts | Outcome | Observed conflicts |
|---|---:|---|---:|
| CaDiCaL 1.9.5 | 500,000 | `BUDGET_EXHAUSTED` | 500,002 |
| MapleChrono | 500,000 | `BUDGET_EXHAUSTED` | 500,000 |
| Glucose4 | 500,000 | `BUDGET_EXHAUSTED` | 535,126 |
| Lingeling | 500,000 | infrastructure error: limited solve unsupported | 0 |

None is a mathematical decision. The branch remains SAT/UNSAT unresolved.

## Degree-21 side-gluing reduction

The unique fixed vertex has degree divisible by seven. The certified
\(18\le d(v)\le24\) degree bound therefore forces degree 21, so it is adjacent
to exactly three of the six cycles. Permuting cycles canonically fixes those
three neighbor cycles.

The 21 neighbors must induce a \(K_4\)-free, \(I_5\)-free graph; the 21
nonneighbors must induce a \(K_5\)-free, \(I_4\)-free graph. Each side has a
30-variable \(C_7\)-orbit formula with 3,618 clauses. Fixing one model on each
side and complementing the nonneighbor-side model fixes 66 global orbit
variables, leaving 63 cross-edge variables.

An adversarial audit verified this mathematics, the exact 66/63 partition,
model decoding, pair schedule, and both graph-verifier bindings. It also
hardened storage/toolchain enforcement and atomic outputs. Ten no-production
controls pass.

- hardened runner SHA-256:
  `5bc3852bb0e81f127652f14e15e806f9e3712e8ecc8163a92c8255bfa743a906`
- test SHA-256:
  `749d1a800544f8ea15f8b3d7c9c965bee5d1555d8fae94785ac651cabc4806f4`
- audit SHA-256:
  `823e59cf9c6c56fd3fbf6396281429e73d4158f556e12053c8bd00ca87ce4f69`
- frozen v2 production plan SHA-256:
  `bdf6b8fecded2cee35a6eb2568d387f5ed844de601a9942ee483a4a3ac1c12a5`

The 256-pair v2 side-gluing production has not launched because its unchanged
2,149,483,648-byte preflight gate currently fails. It has no outcome.
