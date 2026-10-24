# Rank-five improvement after the initial frozen certificate

2026-10-24 21:53 UTC. The originally frozen index1024 certificate remains correct. Direct lift and cocycle checks improve it to index **512**, with exactly the same64-vertex free-fiber graph and the same9 integral edge cochains.

The cover-construction program conservatively doubled the monodromy power from8 to16. For this selected character that doubling was unnecessary: \(\theta^8\) already fixes every cover vertex, and every recorded edge cochain is already \(\theta^8\)-invariant modulo a vertex potential. The direct certificate `rank5_cocycle_certificate_index512.json` changes the stable-letter power to8 and recomputes its vertex potentials. The standalone verifier checks the full set of2880 edge-cell identities and19 target evaluations again.

Thus \(K_8=\langle L,t^8\rangle\) has index \(64\cdot8=512\), and admits an integral homomorphism taking \(a_1^2\) to1. It retracts onto \(\langle a_1^2\rangle\). All18distinct target elements remain detected in this smaller subgroup. No claim of minimal index is made. Powers1,2,4 do not preserve this particular based subgroup, as separately recorded by exact edge-endpoint checks; this does not exclude other covers at those indices.

This delta is a stronger finite partial control only. No virtual-specialness, RFRS, universal cyclic-retraction or new-solution claim is supported. Independent review is pending.
