# K3P fixed-full restoration theorem

Status: **PASS**.

## Theorem

For every fixed-full restoration obligation represented by the frozen corrected
restoration forest, the corresponding physical K3P source child is excluded
from the target child by an exact observable certificate.  The K3P proof
terminates all 36,568 first-layer rows.  In
particular, the 32 nodes that were structural continuations in the imported
K2P forest are already separated in K3P by direct four-port marginal quartics.

The complete imported graph forest is nevertheless replayed: it has
36,824 edges, 32 structural continuation nodes,
256 depth-two edges, and
36,792 legacy/full-forest leaves.  The last
256 edges are redundant for the minimal K3P proof but each is independently
reconstructed and separated.

## Exact K3P proof census over all forest edges

* displayed-quartet mismatch: 36,006
* three-sector tree--ordinary-sunlet SOS: 614
* regenerated K3P multihomogeneous quadratics: 148
* transported active K3P marginal quartics: 56

The 614 old `T_i` rows are replaced by literal three-sector K3P maps and the
six-circuit sum-of-squares theorem.  The 148 old quadratic rows are regenerated
with independent C, G, and T variables.  The 24 old transported K2P quartic
rows, together with the 32 former continuation nodes, use exact active K3P
L20-01/H21-01 quartics.  No K2P equality such as C=T is imposed.

## Why the direct marginal is legitimate

The argument marginalizes the original fixed-full containment; it never lifts
an abstract selected relation.  Deleting the restored leaf and suppressing its
subdivision replaces each serial K3P edge chain by

`((c_i,g_i,t_i)) -> (product c_i, product g_i, product t_i)`.

Its Jacobian has three disjoint positive rows and rank three.  Since the strict
principal domain is open, the source restriction has a relative open image;
the target marginal only needs to be physical, not open.  Thus a target
identity with nonzero source pullback on the selected marginal excludes the
original full containment.  Every concrete graph restriction and parent
transport is replayed exactly in the machine ledger.

## Reproduction

```bash
cd /Users/alec/Documents/Math/k3p_level2_identifiability_final/restoration
../.venv/bin/python regenerate_k3p_restoration.py --resume
../.venv/bin/python verify_k3p_restoration.py
../.venv/bin/python test_k3p_restoration_mutations.py
```
