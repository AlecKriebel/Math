# Independent audit of the characteristic-three anti-fold jet

This folder is intentionally separate from `eliahou_char3_jet`.

`verify_char3_jet_audit.py` reconstructs the relevant cyclotomic
polynomials from `z^n-1`, rather than copying their coefficients from the
search code.  Over `F_3` it verifies

```
Phi_12 = Phi_4^2,
Phi_84 = Phi_28^2,
z^42 + 1 = (z^14 + 1)^3,
Phi_4 Phi_28 = z^14 + 1.
```

It also reconstructs the quadratic support equations for canonical cases
0 and 26 and checks them against 68 direct four-row negacyclic norm
replays.  This includes the diagonal Boolean identity
`(1-x)^2 = 1-x`, which is the subtle special case in the expansion.
Across all 30 canonical cases, it independently checks that the PySAT and
CP expansions each expose twenty equations of integer content four.  The
support-domain census is 29 cases with 78 variables and one case with 79.

Run with the shared solver environment:

```
/Users/alec/Documents/tmp/hadamard-env/bin/python \
  verify_char3_jet_audit.py
```

Passing this audit certifies the algebraic reduction and implementation
agreement.  It does **not** make the characteristic-three condition
sufficient for an integer Golay repair.

## Search result

`CASE26_CHAR3_WITNESS.json` is a 39-cell support for canonical case 26
(`S`, q-index 12) whose complete twenty-coordinate normalized anti-fold
residual is zero modulo three.  It was found by the independent sampled
two-out/two-in search and is replayed from the physical four rows by the
verifier.  All twenty residuals are pinned in that JSON file.  This is a
full characteristic-three (three-jet) survivor, **not** a joint modulo-six
survivor and not an integer repair: several normalized residuals are odd.

An exact Hamming-ball SAT check found no simultaneous modulo-two/modulo-three
support within distance 8 of this witness (radii 2, 4, 6, and 8 were checked
successively).  This is a local exclusion only.

For example, the radius-eight check is reproducible with:

```
/Users/alec/Documents/tmp/hadamard-env/bin/python \
  search_hamming_sat.py --case 26 \
  --center CASE26_CHAR3_WITNESS.json --radius 8 --moduli 2,3
```

The separate characteristic-two affine-code derivation and its bounded
intersection search are documented in `MOD2_AFFINE_CODE.md` and
`MOD2_CODE_SEARCH_RESULTS.md`.
