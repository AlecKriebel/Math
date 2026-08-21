# Frozen checkpoint: two explicit L07 representatives

First banked: `2026-07-26T01:35:19Z`.

## Scope

This directory studies only the two displayed representatives

\[
h=(p+q)^2,\qquad
R_{\mathrm{pow}}=(p+q)^3,\qquad
R_{\mathrm{mix}}=(p+q)(2p^2+pq+2q^2)
\]

in the fixed-quadratic leading form
\[
H_4=(hp^2,hq^2,0).
\]
For both representatives, exact calculation gives linearly independent
\(\alpha=J(hq^2,R)\) and \(\beta=-J(hp^2,R)\), and
\(\deg\gcd(\alpha,\beta,J(hp^2,hq^2))=4\).  This places them in the intended
L07 numerical stratum.

No orbit-exhaustiveness or completeness theorem is proved here.  In
particular, these computations do **not** close frozen leaf L07, do not close
the quartic row, and do not prove a new degree bound.

## Exactly verified outputs

All lower binary cubic and quadratic summands are retained in the component
descents below.

- For the mixed representative, the nonzero E6-contact line has
  \[
  U_1=-\frac23kp(p+q),\quad V_1=\frac23kq(p+q),\quad T_1=k(-p+q).
  \]
  After the complete E6 solve, the \(pr^3\) and \(qr^3\) coefficients of E4
  are both \(16k^4/135\).  Hence this component has no solution with
  \(k\ne0\).

- On the mixed zero-contact component, E6 has rank 5 and E4 contains
  \[
  [p^3r]E4=\frac{2(15b_4+2\ell_8)^2}{135},\qquad
  [q^3r]E4=\frac{10(3b_4-2\ell_8)^2}{27}.
  \]
  Thus \(b_4=\ell_8=0\) in characteristic zero.  The exact E6 formulas then
  set every \(r\)-dependent nonlinear quadratic coefficient to zero.

- For the power representative, the zero-contact component has E6 rank 5
  and
  \[
  [p^3r]E4=3b_4^2,\qquad
  [q^3r]E4=\frac{(3b_4-4\ell_8)^2}{3}.
  \]
  Again \(b_4=\ell_8=0\), and the E6 formulas set every \(r\)-dependent
  nonlinear quadratic coefficient to zero.

- On the nonzero power-intersection line
  \[
  U_1=-kp(p+q),\quad V_1=kq(p+q),\quad T_1=0,
  \]
  the complete arbitrary-binary descent gives E5 ranks \(3,3\).  E4 first
  imposes
  \[
  S=v_0-v_1+v_2-v_3=0,
  \]
  after which the E5 compatibility is a nonzero scalar times
  \(kD^2\), where
  \[
  D=u_1-2u_2+3u_3-v_1+2v_2-3v_3.
  \]
  Substituting \(S=D=0\), the remaining E4 equations force
  \(\det L=0\).  The only nonunit division in this reduction is by \(k\);
  the \(k=0\) boundary is the separately checked zero-contact component.

- Exact invertible solutions of E9 through E5 exist on both nonzero contact
  components: one has \(\det L=5\) on the power-intersection line and one has
  \(\det L=-7\) on the mixed line.  Both fail E4.  These witnesses certify
  that an E6/E5-only exclusion would be false and that the E4 descent is
  essential.

The other two transverse power-contact planes were explored but are not
claimed closed here: the current calculation uses a generic linear pivot and
its omitted pivot-boundary charts have not been certified.

## Reproduction

From this directory run:

```sh
sh verify_strict.sh
```

The terminal success marker is:

```text
DELTA_GE3_SURVIVOR_PROBE_STRICT_PASS
```

The wrapper runs two exact SymPy checks.  The second reduction additionally
ends with:

```text
POWER_INTERSECTION_COMPLETE_PASS_DETL_ZERO
```

Assertions must remain enabled.  These exact checks certify the algebra
encoded by the scripts; they are not a proof of representative
exhaustiveness and are not peer review.

## Disclosure

The derivations and verification code were produced with AI assistance.
Every claim in this checkpoint is intentionally representative-scoped.  The
work is not peer reviewed.
