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

