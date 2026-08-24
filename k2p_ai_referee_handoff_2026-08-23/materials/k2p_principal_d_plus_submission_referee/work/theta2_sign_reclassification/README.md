# Independent theta2 full-map sign replay

This package independently replays the direct full-Fourier-map replacement
for the 2,528 revoked theta2 rooted sign rows.  It does not read the legacy
topology-witness table.  Instead, it searches the complete five-port source
maps and discovers that each of the four theta2 repairs has exactly one triple
on which all three orientations of `T_i` vanish: labels `(0,1,2)`.

Transporting that algebraically discovered triple through each row's labelled
port permutation yields an exact target pullback that is strictly negative by
tensor Bernstein coefficients.

## Frozen result

- 2,528/2,528 primitive rows replayed;
- unique source-zero triple `(0,1,2)` for all four repairs;
- 2,528 exact source-zero identities;
- 2,528 exact target strict-negative certificates;
- 85 exact polynomial relation classes;
- zero exact labelled-isomorphism/triangle conflicts; and
- zero unresolved rows.

## Reproduction

```sh
.venv/bin/python work/theta2_sign_reclassification/verify_theta2_full_map_independent.py
.venv/bin/python work/theta2_sign_reclassification/mutation_tests.py
```

The verifier binds the independently produced truth certificate under
`work/adversarial_proof_review/`, but recomputes every load-bearing graph,
transport, polynomial, and Bernstein claim from the primitive inputs.

