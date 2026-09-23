# Exact finite checks

Run with Python 3.9 or newer; no third-party packages are needed:

```sh
python3 verification/verify.py
python3 verification/verify.py --json
```

Run from the problem folder. A failure raises an exception and exits nonzero.
The checks use `fractions.Fraction` throughout, including the real and imaginary
parts of complex values. They use no numerical tolerance or randomness.

The four groups check:

1. The signs of the shifts and the identity `D B = S D` for the stated weight
   convention, together with the scalar isometry for `p=1`.
2. A three-atom fibre model of bounded distortion. Its atom densities are
   `c_j` times a permutation of `(1/2, 1, 3/2)` for `j != 0`, and are all one
   for `j=0`. Thus the fibre masses are exactly `3 c_j`, and `K=2` works.
   Every subset of the fibre and a complex-valued `p=2` norm comparison are
   checked for the finite range `-7 <= j <= 7`.
3. The finite-support perturbation identity
   `lambda S^n(a + lambda^-1 S^-n b) = lambda S^n a + b`, using two-dimensional
   complex fibres and `lambda=3+4i`. At `n=40` and `c_j=2^(-|j|)`, both the
   input perturbation and output error have norm less than `1/1000`.
4. Two-sided tails for `p=1,2`, four finite symmetric blocks, and two error
   thresholds. With `c_j=2^(-|j|)` and `n>N`, each tail sum on `|j|<=N` is
   exactly `2^-n sum_{|j|<=N} 2^-j`, which tends to zero. With constant
   weights `c_j=1`, both unscaled sums equal `|F|`. Multiplying the two
   desired inequalities shows they cannot both hold when `epsilon<=1`:
   their product is `|F|^(2/p)>=1`, independently of the nonzero scalar.
   The script checks representative moduli; this product argument establishes
   the all-moduli obstruction analytically.

These are **finite sanity checks, not machine verification of the theorem**.
They help expose incorrect indices, norm factors, or perturbation identities.
They cannot establish density, a Baire-category argument, separability of a
given measure space, necessity of the tail criterion, or a claim quantified over
every set of complex scalars. Those conclusions require the accompanying
analytic proof and its hypothesis audit.
