# Independent red-team of the Eliahou orientation cascade

This directory independently checks the proposed `2`-adic
endpoint-orientation cascade for the twenty open long cases.  It imports
the authoritative adjacent-fold, anti-fold, and long-case definitions,
but it does not import the primary orientation-cascade implementation.

No long case, base sequence, or `H(668)` is claimed.

## Exact orientation audit

`audit_orientation_redteam.py` derives all quantities directly from the
four length-`84,84,83,83` rows.

For every open case it proves that the plus-fold PAF divided by four is
affine in the 78 support bits and vanishes on the complete 57-dimensional
anti-mod-2 affine space.  The proof checks all `3,003` second differences
per case, not only a random sample.  Thus the plus-fold equations are
automatically zero modulo eight.

For a fixed exact-weight-39 support:

- the 21 plus-fold equations modulo 16 are affine in the 39 endpoint
  choices;
- two further affine equations impose the parities of the exact `+1/-1`
  root profile;
- the surviving orientation fiber normally has dimension 17 or 18;
- the next digit modulo 32 consists of 21 exact quadratic Boolean forms.

The checker enumerates every point in each sampled mod-16 fiber, counts
the four exact signed root values before and after the mod-32 gate, and
replays survivors in the physical folded rows.

The four exact-root constraints themselves are four disjoint
constant-weight conditions after a sign gauge, one for each
`(long/short) x (even/odd cell)` bin.  In the independent 200-support
sample they retained `120,455 / 26,476,544 = 0.0045495` of the mod-16
points, an observed reduction of about `7.78` bits.  This is again a
sample statistic, not a whole-fiber theorem.

With five deterministic supports per profile and a seed base different
from the parallel audit, the 200-support control gave:

```text
mod-16 inconsistent supports                 5
consistent fibers                          195
mod-16 fiber points                 26,476,544
points with all four exact roots       120,455
mod-32 survivors                              24
supports with zero mod-32 survivors          178
mod-32 survivors with exact roots              0
```

This agrees in scale with the independent parallel sample but remains a
bounded diagnostic.  It is not a frequency theorem for all weight-39
supports.

The pure-quadratic row rank in this sample ranged from 13 through 20.
The common polar radical had dimension zero in 170 fibers, one in 23,
and two in 2.  Thus the individual forms have low polar ranks, but there
is almost never a useful common radical.

`verify_pinned_root_survivor.py` independently replays the one exact-root
mod-32 point found by the parallel 200-support sample.  It confirms case
5/profile 0, support hash
`b1ac33262ac93f840ed08870a61b65d6b13c5a1acde4ed803b8ebd8f424a9d20`,
the exact roots `(-3,-5,4,-4)`, and the fact that the point fails the next
plus-fold digit modulo 64.

## What the two folds do and do not prove

Writing the total aperiodic correlations as `C_k`, exact cyclic plus-fold
and negacyclic anti-fold norms imply

```text
C_42 = 0,
C_(84-k) = -C_k,       1 <= k <= 41.
```

They prove periodic length-84 complementarity, not aperiodic
complementarity.  The nonzero correlation kernel

```text
C_1 = 2, C_83 = -2
```

is integral, has the parity required of the binary quadruple, and is
invisible to both folds.  Adding it to the target norm even leaves a
strict spectral lower bound of `326`.

One equation from each cancellation pair is therefore necessary.  Taking
the causal half

```text
C_43 = ... = C_83 = 0
```

adds 41 equations and reconstructs every omitted aperiodic coefficient.

## Exact ternary formulation

`audit_exact_ternary_model.py` uses

```text
t_j in {-1,0,1},  u_j=t_j^2,
```

where `t_j=0` means no flip and the two signs choose the lower or upper
endpoint.  It symbolically reconstructs and randomly replays all 84
physical correlations in every open long case.

The exact system is:

```text
sum u_j = 39                         shell / C_42
20 anti-fold equations in u only
21 plus-fold equations in t only
41 causal equations C_43,...,C_83
```

This is a clean exact formulation, but it does not reduce the global
quadratic-product inventory.  In every case both the direct aperiodic
system and the fold-plus-causal system use exactly

```text
5,928 products =
1,482 uu + 1,482 ut + 1,482 tu + 1,482 tt.
```

The 41 causal equations alone touch all 5,928 products.  They reuse all
1,445 or 1,446 anti-fold products and all 1,482 plus-fold products.

Fixing the support `u` leaves genuine `tt` quadratics.  Prescribing an
endpoint sign for each prospective support bit leaves genuine `uu`
quadratics.  The causal equations become linear only after the complete
lower half of the four physical rows is fixed; then they are linear in
the upper half.  This gives a rigorous staged enumeration/linear-solve
architecture, but no host-scale outer bound: exhaustive lower-half
branching remains enormous, and the 41 low equations are still nonlinear.

## Reproduction

From the repository root:

```text
PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  hadamard_668_search/eliahou_long_orientation_redteam/audit_orientation_redteam.py \
  --samples-per-profile 5 --skip-redundancy --compact

PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  hadamard_668_search/eliahou_long_orientation_redteam/audit_exact_ternary_model.py

PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  hadamard_668_search/eliahou_long_orientation_redteam/verify_pinned_root_survivor.py
```

The first command is a bounded deterministic sample.  Omit
`--skip-redundancy` to repeat the complete all-case mod-8 affine proof.
The second command is the frozen exact product/equivalence certificate.
