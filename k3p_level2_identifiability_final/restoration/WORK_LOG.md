# Restoration work log

## 2026-08-25 08:18 PDT — exact graph reconstruction and algebra discovery

Reconstructed all 36,824 frozen restoration edges from the primitive K3P atlas
and used the frozen corrected forest only for graph/parentage/transport
metadata.  Exact parent transport failures: 0.

Discovery closed every model-specific residue:

* 614 historical `T_i` rows -> literal three-sector tree--ordinary-sunlet
  six-circuit sum-of-squares certificates;
* 148 historical K2P quadratics -> regenerated exact K3P multihomogeneous
  quadratics;
* 24 transported K2P quartics -> active transported K3P L20-01/H21-01
  four-port marginal quartics.

Best estimate of completion for the restoration subgoal: **55%**.  Algebraic
existence was complete; production sealing, independent replay, and mutations
remained.

## 2026-08-25 08:28 PDT — stronger K3P early termination

Tested all 32 structural first-layer continuation nodes.  None has an earlier
tree--sunlet SOS or K3P quadratic, but every one has a direct four-port marginal
K3P quartic separator.  Therefore the minimal active K3P proof terminates at
depth one.  The imported 256 depth-two edges remain a redundant full-forest
replay.

Count distinction fixed:

* minimal active K3P terminals: 36,568;
* legacy structural continuations: 32;
* redundant depth-two edges: 256;
* legacy/full-forest leaves: 36,792.

Best estimate of completion for the restoration subgoal: **70%**.

## 2026-08-25 09:01 PDT — release package sealed

The deterministic checkpoint-resumable producer completed with manifest
payload `b35346386300bb3f0816a2bbe671280f92f28ee1c5fa2eb9829e6f9fe0863c39`.
The ordered 36,824-edge ledger SHA-256 is
`72ac04b1ecd4968951c56fef29f8ef6c08b4ea510e503ecd345d613d9bf6329b`.

The independently implemented replay rebuilt 424 descriptor classes and
passed with payload
`91a29973bcd333c05270ffd379427a8c949285f791fd5db299a83c46934e82b1`.
It does not import producer code or its support module.

The adversarial suite rejected 20/20 mutations, including omitted/duplicate
children, proof reassignment, K2P sector collapse, wrong quartic transport,
boundary inheritance, target-openness misuse, continuation/depth-two count
conflation, broken parent transports, and optimized-mode bypass.  Mutation
payload: `f770cecb54b459b3ff11d85b0df780e10c07b8fff92dee553ce0feb91120a9c1`.

Best estimate of completion for the fixed-full K3P restoration subgoal:
**100%**.  No unresolved restoration row remains.
