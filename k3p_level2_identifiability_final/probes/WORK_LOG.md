# Probe and port-word work log

## 2026-08-24T21:26:00-07:00 — Companion topology import

- Imported the exact model-independent restoration/probe graph package from the
  completed K2P workstream at clean repository snapshot
  `962c707c1cf70c8a188481a1e666e16849b0e399`.
- Bound all 28 imported files in `COMPANION_DEPENDENCY_LOCK.json`.
- Explicitly excluded every K2P sign, rank, sector-equality, and model
  conclusion from active K3P evidence.

## 2026-08-24T21:31:00-07:00 — K3P anchor regeneration

The literal K3P atlas independently reconstructed the imported topology
contract without using K2P algebra:

```text
anchors                         176
source sites                    2,206
target sites                    2,206
one-port Cartesian pairs        29,964
isomorphic anchors              143
ordinary-triangle anchors       33
runtime                         14.51 s
maximum resident set size       409,190,400 bytes
```

Every anchor locator, graph hash, exact relation, site profile, and parent
transport agreed with the frozen graph contract.

## 2026-08-24T21:37:00-07:00 — Three-sector one-port closure

Replaced the K2P-only `T_i` sign oracle with a K3P oracle that:

1. uses graph-derived triple type only as a finite finder;
2. constructs each literal restricted K3P map with independent `C`, `G`, and
   `T` edge variables;
3. checks exact vanishing of all six cubic circuits on the tree descriptor;
4. checks a nonzero circuit deck on the ordinary-sunlet descriptor; and
5. invokes the exact six-circuit sum-of-squares proof of strict positivity on
   every ordinary sunlet in `D_{3,+}`.

The complete one-port regeneration passed:

```text
displayed-quartet mismatch      27,758
isomorphic                       1,915
ordinary triangle                 192
K3P tree--sunlet SOS                99
unresolved                            0
equality parents retained         2,107
runtime                          114.42 s
maximum resident set size       386,400,256 bytes
logical payload SHA-256         94844ba0ae4592d3ba9b5ad75bdff07fb56384f58fc120c47f794ed9a900bfa5
```

This reproduces the completed topology census while replacing all 99
model-specific K2P rows with exact three-sector K3P evidence.  It does not yet
promote the arbitrary-word theorem because the full two-port regeneration and
independent replay remain pending.

Strongest verified result in this lane: zero unresolved one-port rows and
complete exact parent transports over all 176 physical anchors.

Best-guess completion toward the restoration/probe subgoal: **45%**.

## 2026-08-24T22:24:00-07:00 — Failed first two-port attempt preserved

The first full two-port run stopped closed on the first parent because a
reticulation-count finder had admitted a suppressed three-leaf restriction
whose literal mixed graph was not an ordinary sunlet: every one of the six
K3P circuits vanished.  No row from that failed run was retained as active
evidence.  The finder was strengthened to require exactly one ordinary mixed
triangle, six vertices, six edges, degree census `[1,1,1,3,3,3]`, and the
literal nonzero circuit deck.  Reticulation count remains a finder only.

## 2026-08-24T22:35:00-07:00 — Complete corrected regeneration

One uninterrupted `caffeinate`-protected run regenerated both probe ledgers
from the frozen graph contract and literal K3P atlas:

```text
one-port raw pairs                  29,964
one-port displayed-quartet          27,758
one-port isomorphic                  1,915
one-port ordinary triangle             192
one-port K3P tree--sunlet SOS            99
one-port unresolved                      0
two-port parents                     2,107
two-port raw pairs                  544,571
two-port displayed-quartet          511,266
two-port isomorphic                  30,969
two-port ordinary triangle            1,760
two-port K3P tree--sunlet SOS            576
two-port unresolved                       0
two-port equality survivors          32,729
exact graph transports               67,741
parent restrictions                   4,379
runtime                            2,996.19 s
maximum resident set size       428,195,840 bytes
logical payload SHA-256       b6d836f1a85a11749d49fb714acef955ae0393c80d32186d957c7149a3695565
```

## 2026-08-24T22:42:00-07:00 — Independent replay and mutations

A separately structured streaming verifier, which does not import the
producer, replayed every ordered row, Cartesian product, transport,
restriction, reversed-order certificate, K3P relation certificate, and the
frozen six-circuit separator theorem.  It passed in 17.20 seconds with a
75,988,992-byte peak resident set and logical payload
`16618c24651d28bb6c1848f026f2546cd19efcf53a86259b632fc86b44f62166`.

All 17 probe mutations were rejected, including omissions, wrong parentage,
order reversal, incoherent triangles, a broken graph transport, corruption of
the tree zero-circuit deck, a false K2P sector equality, and a corrupted
six-circuit theorem reference.  The mutation payload is
`887a8f72d5437854920cdc9c968bb71a10cbf6c2cf8342e3c73663861f51752e`;
runtime was 175.20 seconds and peak resident set 78,266,368 bytes.

Strongest verified result in this lane: the complete one-/two-port K3P probe
closure has zero unresolved or incoherent rows and is independently replayed.
The imported fixed-full restoration forest is still active only as a
model-independent graph/parentage contract; its K2P algebra certificates are
not promoted as K3P evidence and require a separate K3P restoration audit.

Best-guess completion toward the restoration/probe subgoal: **82%**.
