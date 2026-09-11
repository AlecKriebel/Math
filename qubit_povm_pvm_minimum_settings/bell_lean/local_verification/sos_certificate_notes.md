# Exact SOS coefficient certificate audit

Checkpoint: 2026-09-11T01:54:13.287755+00:00; coefficient-certificate verification completion estimate: 100%.

`lake build Bell.SOSCertificate` succeeded using pinned Lean 4.19.0 and the actual compiled `Bell.SOSAlgebra` dependency. No source changes to SOSCertificate were needed. Lean checked the 144 exact real rational LDL entries, all twelve strictly positive pivots, and numerator symmetry. The three theorem axiom sets contain only `propext`, `Classical.choice`, and `Quot.sound`; none contains `sorryAx`.

An independent Python Fraction computation confirmed that the Lean numerator, L, and d literals exactly match the certificate JSON, that all pivots are positive, and that every LDL entry is the corresponding integer numerator divided by 600. This is additional reproducible arithmetic evidence, distinct from kernel checking.

The earlier temporary isolated-source compile was intentionally interrupted when SOSAlgebra became available; only the successful actual module build certifies the dependency chain. Its temporary source and empty diagnostic log do not establish compilation success.

These results establish the exact positive Gram coefficient matrix. Identification with the Bell operator and the link to Born-expectation upper bounds belong to separate modules and are not inferred from positive coefficients alone.
