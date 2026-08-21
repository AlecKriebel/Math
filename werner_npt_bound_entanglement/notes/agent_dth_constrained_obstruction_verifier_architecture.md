# Exact-verifier architecture for the constrained DTH obstruction

## Status (2026-08-01)

There is now a **strict numerical pseudomoment obstruction** to the complete
five-replica DTH-constrained lift on the exact 2266-dimensional physical
product face.  This is discovery evidence, not yet an exact counterexample.

The preferred S3-symmetric candidate uses the rational mixing parameter

\[
\theta=\frac9{500}=0.018.
\]

Its floating audits are

\[
\begin{aligned}
\operatorname{Tr}x&=1+1.1\cdot10^{-14},\\
\langle \widetilde{\mathcal O}_0,x\rangle
  &=-4.52547025094384\cdot10^{-4},\\
\lambda_{\min}(x|_{K_{\rm hol}})&=7.33695108101\cdot10^{-8},\\
\lambda_{\min}(x^\Gamma|_{R_{\rm prod}})&=1.29666784587\cdot10^{-8}.
\end{aligned}
\]

The pre-repair point is in the common affine linear support to residual
`4.514e-14`; its objective is `-0.00363934020215`.  Mixing with the strict
relative-Slater point moves it into the interiors of both supported PSD
cones while retaining the negative objective above.

No theorem may be claimed until a rational correction and exact PSD/sign
verification have been completed.

## Discovery artifacts and hashes

The current local artifacts are:

| artifact | role | SHA-256 |
|---|---|---|
| `/tmp/dth_constrained_obstruction_theta018_sym.npz` | preferred safe candidate | `ef00cc4ffd390207092c93c45d83d8853e8fa1784b33bc74c7c8e5381a99b093` |
| `/tmp/dth_product_face_bases.npz` | float QR of exact rational 2266-face pivots | `1d7025c13cd5d5f7f62f245e91730a1a3cbf4adf96ba4649b3e357e2ef9117ce` |
| `/tmp/dth_obstruction_diagram_metadata.npz` | selected-diagram conversion metadata | `2d6e26297865ab993e38c33244c10f6b82d16474fd5ffd5d0328970ffe6cdd74` |
| `/tmp/dth_product_slater.npz` | strict relative-interior point | `46d2bc299bfb61ae7b658ec96c20961103603f6e4c98b3876dc2a65195e62fb3` |

The candidate file has fields

```text
x, z, linear_x, linear_z, theta, objective, gamma, multiplier
```

where `x,z` are the safe mixture and `linear_x,linear_z` are its common-
support precursor.  The diagram metadata file has fields

```text
diagram_coefficients
selected_permutations
normalized_hol_restriction
normalized_mixed_restriction
normalized_local_crossing
x, z, theta, objective
hol_reconstruction_error
mixed_reconstruction_error
bridge_error
hol_condition
```

The normalized local diagram bridge has condition number `81.2358263`.
Conversion to and from the diagram tensor has errors below `3.9e-17`.
The diagram tensor is S3 symmetric to `2e-20`, has norm `3.38587e-5`, and
maximum entry magnitude `3.73312e-7`.

## Exact coordinate convention

Use the 103 selected permutations in
`verification/agent_dth_local_crossing_exact.py`.  For a rational diagram
coefficient tensor `c[a,b,c]`, define

\[
 X(c)=\sum_{a,b,c}c_{abc}
 P_a\otimes P_b\otimes P_c.
\]

Partial transpose does not change `c`: it replaces each local `P_a` by its
matched walled diagram `D_a`.  The exact bridge returns rational matrices

```text
HOL_RESTRICTION, MIXED_RESTRICTION
```

whose columns are the flattened highest-weight restrictions of `P_a` and
`D_a`, respectively.  Thus all support equations, trace, objective, and
block matrices are rational functions of one common tensor `c`.

The floating normalized restrictions exported in the metadata are only for
locating a nearby rational point.  The verifier must rebuild the rational
restrictions from the exact bridge and must not trust the NPZ matrices.

## Preferred rational certificate format

The smallest certificate should use the rational holomorphic constrained
coordinates rather than all `103^3` diagram coefficients.

1. Construct an exact rational basis `K_s` of the holomorphic DTH support in
   every ordered local-type triple `s`.  A Hermitian invariant moment is
   represented by symmetric matrices `A_s` through

   \[
   H_s=K_s A_s K_s^{\mathsf T}.
   \]

   The total number of independent entries in the `A_s` is 4139.

2. Use the exact rational pivot columns of the physical product ensemble to
   construct each mixed face basis `R_t`.  Its total column rank is 2266.

3. Cross the hol blocks through the exact matched-diagram bridge and impose

   \[
   M_t=R_t B_tR_t^{\mathsf T}
   \]

   for symmetric rational `B_t`.  Numerically the resulting linear defect
   has rank exactly 334, with a gap exceeding `10^12` in randomized rank
   tests.  The exact reconstruction should record 334 pivot equations and a
   checksum of their pivot set.

4. Round the free coordinates of the S3-symmetric numerical candidate to a
   large rational denominator and solve the 334 pivot variables exactly.
   The rational parameter `theta=9/500` should be retained explicitly.

The certificate should contain:

```text
common denominator(s)
S3-symmetric free hol coordinates
334 exact pivot coordinates (or enough data to recompute them)
exact face-pivot checksum
exact linear-defect pivot checksum
```

A dense rational diagram tensor is an acceptable fallback, but the 4139
coordinate certificate is substantially smaller.

## Dependency-free verification steps

A final standard-library verifier should perform these checks in order.

### 1. Rebuild all exact local data

Rebuild the selected permutations, rational Specht/highest-weight bases,
exact hol and mixed restriction matrices, rational hol support bases, and
rational product-face pivot bases.  Check the existing exact face-basis hash

```text
2297a5d32caba44ac2dd6a8d26983a9fe61b7bf11d73e7daba06af251a050955
```

and the total face rank `2266`.

### 2. Verify the common linear constraints exactly

Reconstruct every `H_s` and cross it to every `M_t`.  Check exactly that

```text
H_s = K_s A_s K_s^T
M_t = R_t B_t R_t^T
```

with no tolerance.  This simultaneously verifies the holomorphic
Pluecker/Omega support, the mixed support and Omega equations encoded by the
physical product face, and exact partial-transpose consistency.

For additional defense, independently apply the literal support contraction
map `C_s` to each `M_t` and check that it vanishes.

### 3. Verify normalization and negativity exactly

Compute trace in the nonorthogonal highest-weight bases using their rational
Gram matrices, or directly pair the diagram tensor with the identity
diagram.  Require exactly

\[
\operatorname{Tr}X=1.
\]

Compute the objective from the literal rational permutation expression

\[
\widetilde{\mathcal O}_0
=\frac14I-\mathsf A_{15}^{(1)}\mathsf A_{15}^{(2)}
 \mathsf A_{15}^{(3)}
-\mathsf A_{35}^{(1)}\mathsf A_{35}^{(2)}
 \mathsf A_{35}^{(3)},
\]

where each local antisymmetrizer is `(I-F)/2`.  Require its exact numerator
to be strictly negative.

### 4. Verify positivity exactly

Because the safe candidate is strictly positive relative to both supports,
verify positive definiteness of every nonzero rational `A_s` and `B_t`.
A dependency-free route is fraction-free `LDL^T` elimination (or Bareiss
leading principal minors).  Every exact pivot must be strictly positive.
Then `K_s A_s K_s^T` and `R_t B_tR_t^T` are PSD by congruence.

The weakest blocks to audit first are:

```text
hol:   (4,4,4)       numerical minimum 7.33695108101e-8
mixed: (2,4,2) and permutations
                         numerical minimum 1.29666784587e-8
mixed: (2,2,2)       numerical minimum 2.27227480180e-8
```

The next hol minima are the permutations of `(4,3,4)`, at `1.03386e-7`.

### 5. Independent interval replay

After the exact rational checks, a second small interval audit should convert
each rational compressed block outward to binary intervals and certify its
smallest eigenvalue or Cholesky pivots.  This is redundant but useful for
catching coordinate-order mistakes.  It must not replace the exact checks.

## Rounding scale

Naive entrywise rounding of the diagram tensor gives the following floating
errors before exact correction:

| denominator | diagram `l2` error | hol support residual | mixed-face residual |
|---:|---:|---:|---:|
| `10^12` | `3.01e-10` | `1.16e-6` | `1.13e-6` |
| `10^13` | `3.01e-11` | `1.18e-7` | `1.15e-7` |
| `10^14` | `3.01e-12` | `1.16e-8` | `1.13e-8` |

Thus raw rounding is not a certificate.  A denominator around `10^16` or
larger, followed by an **exact solution of the 334 pivot equations**, should
leave corrections safely below the `1.3e-8` mixed PSD margin.  The exact
linear solve, not the denominator alone, is essential.

## Logical scope

An exact certificate built as above would prove only:

> the complete first-level five-replica relaxation, even after the lifted
> support and Omega equations are imposed, admits a negative pseudomoment.

It would not be a physical vector of form `(w tensor w) tensor z`; it would
not refute DTH, square-zero positivity, unrestricted three-copy positivity,
or all-copy Werner undistillability.  Its consequence is a proof-complexity
barrier: a higher Veronese--Segre relation or higher certificate level is
necessary.
