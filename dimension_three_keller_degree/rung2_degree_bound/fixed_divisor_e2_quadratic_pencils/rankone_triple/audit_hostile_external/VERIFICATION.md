# Verification

Run the external \(A=0\) reconstruction and its mutation guards:

```sh
./verify_a0_external_pari_strict.sh
./test_fail_closed.sh
```

Run the complete \(A=0/A\ne0\) theorem-coverage ledger:

```sh
./verify_full_coverage_strict.sh
```

The external PARI program rebuilds:

- the raw \(36\times26\) \(E_7\) matrix and complete kernel;
- the effective four-dimensional legal gauge space;
- denominator-free \(A=0\) \(E_6\) branch syzygies;
- both \(D\)-charts and both \(r=a_3\)-charts on \(w_3\ne0\);
- both origin charts;
- the determinant-one \(q\)-shear and its exact translation
  compensation;
- every \(xz\) augmented-rank drop; and
- the full \(xy\) \(h\)-, factor-, \(G\)-, descendant-, and
  intersection tree.

No matrix is imported from the primary SymPy verifier.  The strict wrapper
requires the complete transcript to match exactly.  Seven mutations are
required to fail.

Exact checks are evidence about the encoded algebra.  They are not peer
review.
