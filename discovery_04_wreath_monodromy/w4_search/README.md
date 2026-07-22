# Level-four branch-norm search

This directory contains the bounded-memory search and certified local
transposition needed to prove

```text
Mon(F^4) = S_3 wr S_3 wr S_3 wr S_3.
```

This is a degree-81 group of order
`6^40=13,367,494,538,843,734,067,838,845,976,576`.

It is deliberately separate from the proved level-three certificate.  Nothing
in this directory is currently used by `NOTE.md` or by the paper.

## Mathematical target

On the target line `(a,b,c)=(1,2,s)`, let `t,r,q` be the three successive
inverse-resolvent roots and let `X_3` be the corresponding third inverse point.
The inverse cubic at a point `(a,b,c)` is

```text
2 a T^3 - b T^2 + 2 T - c,
```

with reduced discriminant

```text
Delta(a,b,c) = 27 a^2 c^2 - 18 a b c + 16 a + b^3 c - b^2.
```

The object being computed is the quotient-tower norm

```text
N_3(s) = Norm(Delta(X_3))
```

from the degree-27 inverse tower down to `F_p(s)`.  A characteristic-zero
certificate needs a squarefree numerator divisor of `N_3`, coprime to all
reconstruction denominators and to the branch loci already present at lower
levels.  Such a divisor would give a genuine deepest-level leaf
transposition.  Together with the proved 81-cycle, the proved `W_3` quotient,
and the elementary kernel lemma, that would imply the full fourth wreath
product.

## Why evaluation rather than expansion

Direct symbolic substitution expands rapidly.  The search instead specializes
`s` in a prime field and constructs the three cubic quotients successively.
Every element is represented in a basis of size at most 27.  Inversion and the
final norm are ordinary modular Gaussian elimination, so memory use is bounded
independently of the degree of the unknown rational function in `s`.

`finite_field_norm.py` is the evaluator.  It emits one JSON record per usable
specialization and records exceptional values (where a reconstruction
denominator is a zero divisor) without treating them as zeros of the norm.
Runs are naturally checkpointable by choosing disjoint `--start/--count`
ranges.

Example (after the level-three verifier is no longer running):

```console
python3 finite_field_norm.py --prime 1000003 --start 1 --count 100
```

The script defaults to a 1 GiB address-space ceiling where the platform
supports `RLIMIT_AS`; pass `--memory-mib 0` only in a controlled environment.

## Current exact status

As of 2026-07-22, the global level-four norm has not been reconstructed.
However, a complete scan modulo 1009 found a usable zero at `s=801`, and a
targeted computation modulo `1009^2` proves that the zero is simple.  All lower
branch norms and every leading/reconstruction guard are units there.  The
exact data and good-reduction argument are in `RESULT.md`, and
`verify_w4_modular.py` recomputes the certificate.

Together with the following facts already proved elsewhere in the repository,
the certificate proves `W_4`:

1. the degree-81 cover has an 81-cycle (the all-level Newton-edge argument);
2. its quotient through level three is the full `W_3`;
3. a genuine new leaf transposition would force the full base kernel
   `S_3^27` and hence `W_4`.

An independent bounded-memory audit completed on 22 July 2026 checked the
good-reduction localization, the norm-to-single-inertia deduction, and the
81-cycle kernel argument.  It also added a direct scalar check of the unique
vanishing sheet and its nonzero dual-number derivative.  The main note remains
unchanged so that this upgrade can be reviewed and published separately.

Possible corroborating follow-ups are:

1. Repeat at a second prime or reconstruct the global modular norm
   as corroboration (neither is needed by the targeted simple-zero argument).

This directory is a self-contained computational proof artifact.  It has not
received external peer review.
