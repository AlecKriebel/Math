# Reviewed positivity-loss counterexample: problem 30003571

The precise result is loss of total-space positivity for Naumann's probability-normalized relative Kähler–Ricci flow, published equation (13), on an \(\mathcal O_E(r)\)-weight. The compact example has \(E=\mathcal O_{\mathbf P^1}(1)\oplus\mathcal O_{\mathbf P^1}(1)\), strictly positive initial curvature, and horizontal curvature exactly \(-1/96\) at time \((\log2)/2\).

Read [NORMALIZATION_SCOPE.md](NORMALIZATION_SCOPE.md) first for the relation to the actual source question and the apparent coefficient conflict in published equation (14). The counterexample does not concern the Griffiths conjecture itself, and no novelty or priority claim is made.

The [frozen proof](public/PROOF.md), [source gate](public/SOURCE_GATE.md), and [three-approach log](public/ATTEMPT_LOG.md) are preserved unchanged. The [independent adversarial audit](audit/ADVERSARIAL_AUDIT.md) gives a PASS for the exact equation-(13) claim. Wording about pending review inside the frozen files describes their earlier frozen state; the separate audit records the subsequent assessment.

Reproduce with Python 3 and SymPy:

```sh
cd public
python verify.py
cd ../audit
python audit_verify.py ../public
```

The author verifier checks 40 symbolic identities and 441 supplementary rational points. The independent verifier checks 43 exact identities and frozen-file hashes, without a grid. The universal positivity proof is analytic and algebraic; the finite-time smooth flow-existence theorem is a stated dependency from Naumann's Theorem 5, not a consequence of computation.

All delivered files are enumerated by PUBLICATION_MANIFEST.json. Original frozen and audit manifests remain intact. Downloaded sources and full extracted texts are excluded.

## Research checkpoints

* 2026-10-03: third substantive approach produced the complete compact counterexample; estimated completion of the stated counterexample proof, 100%, pending independent validation.
* 2026-10-04: frozen proof passed independent adversarial review, including the normalization discrepancy, all coordinate charts, and the exact sign; estimated completion of the stated mathematical deliverable, 100%. Human review and historical-priority determination remain separate.

Draft for human review. No merge or release is requested.
