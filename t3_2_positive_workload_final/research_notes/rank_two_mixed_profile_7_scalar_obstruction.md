# Exact additive-scalar obstruction on the seven dormant axes

## 1. Statement

For each of the seven mixed-profile rank-two pairs there is a feasible
zero-cap one-active axis.  In the normalized coordinates of
*rank_two_mixed_profile_7_pf_activation.md*, it is

\[
             (A,B,X)=(0,0,n),\qquad n\longrightarrow\infty. \tag{1.1}
\]

Every top complex contains \(A\) or \(B\), so every top reaction is disabled.
The lower linkage is \(0\rightleftarrows A\); its death is disabled and its
birth is the only enabled reaction.

Let

\[
 F=K+\sum_i\log(x_i!),\qquad W=(1+F)^4,
 \qquad H=A+B+X.                                    \tag{1.2}
\]

On the sole jump \(0\to A\),

\[
 \Delta F=\log(1!)-\log(0!)=0,
 \qquad \Delta W=0,
 \qquad \Delta H=1.                                \tag{1.3}
\]

Therefore every additive scalar

\[
                    V=W+\phi(H)                     \tag{1.4}
\]

obeys exactly

\[
 \mathcal LV(0,0,n)
 =\kappa_{0A}\{\phi(n+1)-\phi(n)\}.                 \tag{1.5}
\]

If \(\phi\) is eventually strictly increasing--in particular, if it is a
nonconstant polynomial with positive leading coefficient--then (1.5) is
strictly positive for every sufficiently large \(n\).  The conclusion is
independent of the strong top orientation and of every positive rate except
for the harmless positive multiplier \(\kappa_{0A}\).

## 2. Exact scope

This is an obstruction to a **pointwise additive scalar class**, not to
positive recurrence.  It does not exclude

1. a stopped episode which charges the activation birth together with later
   physical \(A\to0\) service;
2. a state-dependent correction that already decreases on \(0\to A\); or
3. an augmented marked-chain Lyapunov function.

It proves that the all-active workload cannot simply be added, through an
increasing polynomial of total workload, to the common factorial fourth
power and then used in a one-step Foster inequality.  The PF activation
wedge supplies exactly the first half of the needed stopped alternative;
the interior-to-service composition remains the open seam.

All recurrence and global flags remain false.

## 3. Reproduction

```text
PYTHONPATH=src python3 -B \
  src/rank_two_mixed_profile_7_scalar_obstruction.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_rank_two_mixed_profile_7_scalar_obstruction.py -v
```

The executable freezes eight zero-cap rows covering all seven pairs (one
pair has both physical active axes), the disabled-source check, and the
exact generator identity (1.5).
