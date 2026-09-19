# Backward dependency map

Legend: `[D]` substantial proof bodies written but UNCOMPILED; `[H]` general
conditional helpers written, concrete hypotheses not all discharged; `[M]`
missing; `[X]` externally tested only. No marker means kernel certification.

```
[M] Ordinary notebook existence theorem
 |-- [D] prime/exponent arithmetic (not the substantive result)
 |-- [M] actual BCH Group G on the finite Lie carrier
 |    |-- [D] raw coefficients = original table
 |    |-- [D] arbitrary-vector Lie identities via finite basis checks
 |    |-- [D] adapted basis / weighted integral embedding / scaled Lie bracket
 |    |-- [D] quotient coordinate carrier and its exact cardinality
 |    |-- [D] length-847 vanishing / gamma_847 = 0
 |    `-- [H/M] Dynkin and coefficient helpers -> missing full BCH validation
 `-- [M] Nat.card (MulAut G) = 1009^52359
      |-- [M] both directions of FULL group/Lie automorphism correspondence
      |-- [M] FULL Lie automorphism set <-> COMPLETE derivation kernel
      |    |-- [D] all additive maps are residue-ring linear
      |    |-- [D] full LieRing/linear/matrix automorphism equivalences
      |    |-- [D] concrete finite-field generation and full/infinitesimal flag rigidity
      |    |-- [D] explicit p-adic generation with unit denominators
      |    |-- [H/M] error estimate + word induction + weighted flags
      |    |          -> missing concrete arbitrary-representative lifting assembly
      |    `-- [H/M] actual two-lattice power and tensor factor lemmas
      |               -> missing integral exp/log, precision and actual U(X)
      `-- [M] actual matrix kernel cardinality
           |-- [D] actual K definition and exact kernel/derivation equivalence
           |-- [D] independent 30-direction characteristic-zero rank upper bound
           |-- [H] generic elementary-operation checker soundness
           |-- [X/M] actual 931-pivot plan externally checked earlier;
           |          actual Lean acceptance still missing
           `-- [D/H] general scalar / diagonal / padded / transport cardinalities
                       -> missing application to the actual K
```

The direct flag proof bypasses the full `PGL2`/involution classification and
cohomology calculations for the lifting path. Separate formal theorems for the
ambient perfectness and exact centre have not been supplied; the rank argument
instead uses an explicit left-inverse witness for 30 actual inner directions.
This change in proof organization must not be described as a formalization of
every proposition of the paper.
