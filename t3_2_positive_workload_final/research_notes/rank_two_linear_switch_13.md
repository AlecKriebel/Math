# The thirteen all-active-only rank-two pairs: exact selector and seam obstruction

## 1. Claim scope

This note isolates thirteen pairs inside the exact twenty-pair rank-two
linear-workload switch family.  It is a finite selector and an exact
obstruction certificate, not a recurrence theorem.  Every analytic and
global flag remains false.

The thirteen pairs are characterized by the fact that every
affine-feasible failed descriptor is all-active.  Their pair fingerprint is

```text
f089ad4dbf064da8512d4854e824c36216e3eb74655ec435d06eecc69fb4f27e
```

The complementary seven pairs have active profile \(\{1,3\}\) and
fingerprint

```text
93717536ce82eceefe6909c62568afab31e06695dada8b69defb93335d576957
```

Those seven retain the separate Perron--Frobenius activation obligation.

## 2. Exact all-active workload

Each of the thirteen pairs has one affine-feasible failed descriptor.  The
other linkage is exactly

\[
 R=\{0,C\}.
\]

The whole-top linkage has stoichiometric rank two and lies in one positive
workload plane.  Eleven pairs use \(w=(1,1,1)\), one uses
\(w=(1,2,1)\), and one uses \(w=(2,1,1)\).  Thus

\[
 H_w(x)=w\mathbin\cdot x,
 \qquad \mathcal L_T H_w=0
\]

for every strong orientation and every positive top rate vector.  Since the
two-node lower linkage is strongly connected,

\[
 \mathcal L H_w(x)
   =w_C\{\kappa_{0C}-\kappa_{C0}C\}.                 \tag{2.1}
\]

Equation (2.1) tends to minus infinity on every all-active divergent
sequence.  This is precisely the already audited dimension-local rank-two
workload theorem.

## 3. Why the absence of failed boundary descriptors does not close the pair

All thirteen pairs share the affine-feasible descriptor

\[
       \omega=(0,1,0),\qquad \operatorname{caps}=(0,2,0). \tag{3.1}
\]

It is the divergent \(B\)-axis with \(A=C=0\).  The top D-tier and top
S-tier coincide at the enabled source \(2B\), except for the one unary-top
support where they coincide at \(B\).  Hence (3.1) passes the universal
top-S/top-D criterion for every strong orientation.  It is absent from the
failed-incidence list for exactly that reason.

But (2.1) gives on the same states

\[
       \mathcal L H_w=w_C\kappa_{0C}>0.             \tag{3.2}
\]

Thus `active_profile == {3}` says only that boundary cones are
factorial-good.  It does not say that the all-active workload is good on
them.  In particular, neither the all-active theorem nor the finite atlas
allows these thirteen pairs to be promoted.

The obstruction is especially sharp for the uncorrected factorial
potential.  At \(C=0\), the reaction \(0\to C\) changes
\(\log(C!)\) by

\[
       \log(1!)-\log(0!)=0.                           \tag{3.3}
\]

Consequently a naive positive sum of the rank-two workload and the
uncorrected factorial fourth power cannot obtain its missing negative sign
from that activation jump.  Conversely, in the all-active interior an
arbitrary strongly connected deficiency-positive top can have positive
factorial drift of quadratic propensity order while conserving \(H_w\).
The switch is therefore substantive, not bookkeeping.

## 4. Remaining analytic target

A valid closure must supply one of the following.

1. A single proper state function whose top-shell correction is negative on
   (3.1), has controlled discrete curvature through the activation layer,
   and becomes constant along top reactions once \(C\) is large enough for
   (2.1) to dominate.
2. A physical-time episode which starts in a factorial-good boundary cone,
   reaches a service region, and has a negative expected increment of one
   common proper shell function, with endpoint and duration integrability.

The finite certificate proves neither item.  It freezes the exact thirteen
pair target and prevents the false inference that a passing boundary cone is
automatically \(H_w\)-good.

If these thirteen pairs were eventually certified, they would have zero
overlap with the post-26 certified union and would change the claim-neutral
remainder from \((733,36)\) to \((720,36)\).  That arithmetic is not a
promotion.

## 5. Reproduction

Run

```text
PYTHONPATH=src python3 -B src/rank_two_linear_switch_13.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_rank_two_linear_switch_13.py -v
```

The executable freezes the \(13+7=20\) partition, all-active rows,
workloads, canonical passing-boundary witnesses, disjointness, and
claim-neutral remainder arithmetic.  The recurrence and global T3-2 flags
remain false.
