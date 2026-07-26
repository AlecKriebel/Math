# Clean-room hostile lower audit of `D4-DN-3`

**Audit completed (UTC):** 2026-07-26  
**Verdict:** **PASS — full frozen-family exclusion**  
**Scope:** lower descent from the already-audited D4-DN-3 contact atlas

## Result

No degree-four Keller counterexample over \(\mathbb C\) has normalized top
data
\[
h=(p+q)^2,\qquad
P=hp^2,\qquad Q=hq^2,\qquad R=(p+q)^3
\]
in the frozen `D4-DN-3` family.

This closes this one frozen family.  It does not close the parent
fixed-quadratic row and does not by itself improve the universal quartic
degree bound.

## Independence protocol

The descent was derived without reading `d4_dn3_full_descent` or any lower
script or note in `delta_ge3_survivor_probe`.  The only imported mathematical
input was the previously hostile-audited contact atlas:

\[
c_\pm=\frac{-4\pm2\sqrt2}{3},
\]
\[
U_1=\frac{4k-3(s+c_\pm k)}3p^2+
    \frac{4k-3s}3pq,\quad
V_1=(s+c_\pm k)pq+s q^2,\quad
T_1=k(p+q).
\]

A standalone script rebuilt the weighted determinant with:

- all four binary cubic coefficients of each of \(U_0,V_0\);
- all three binary quadratic coefficients of \(T_0\);
- all six quadratic coefficients of each of \(A,B\); and
- all nine entries of the linear matrix \(L\).

All clean-room formulas were timestamped in
`PRECOMPARISON_FORMULAS.md` before any prior descent file was opened.

## Complete chart cover

The audited contact locus is the union of two planes.  The following four
charts are disjoint and exhaustive:

| Chart | Lower conclusion |
|---|---|
| \(c_+\), \(k\ne0\), arbitrary \(s\) | inconsistent at \(E_5\) |
| \(c_-\), \(k\ne0\), arbitrary \(s\) | inconsistent at \(E_5\) |
| \(k=0,\ s\ne0\) | forces \(\det L=0\) |
| \(k=s=0\) | binary nonlinear collapse and Moh exit |

No generic value of \(s/k\) is chosen.

## 1. Transverse interiors

The complete seven-pivot \(E_6\) solve retains all eleven unpivoted lower
variables.  Its pivots are
\[
373248(7\mp5\sqrt2)k^2.
\]
Two coefficients of \(E_5\), independent of every remaining lower
coefficient, are
\[
\begin{aligned}
[p^3r^2]E_5
 &=3(\pm\sqrt2-2)k(s+c_\pm k)^2,\\
[q^3r^2]E_5
 &=3(\pm\sqrt2-2)k(s-4k/3)^2.
\end{aligned}
\]
For \(k\ne0\), simultaneous vanishing would require
\(-c_\pm=4/3\), which is false.  Both plane interiors are therefore empty,
including every special line in the \(s\)-direction.

## 2. Punctured intersection

Set \(k=0,\ s\ne0\).  A fresh \(E_6\) solve has pivot
\[
-279936s.
\]
It is not a specialization of either \(k^{-1}\)-solution.

The \(r\)-linear \(E_5\) block has rank three; a clean-room pivot
\[
192s^4
\]
solves \(b_{qr},L_{33},t_1\).  The binary \(E_5\) block also has rank three;
a pivot
\[
216s
\]
solves three further variables and leaves one compatibility \(C=0\).

The \(r^2\)-part of \(E_4\) forces
\[
S=v_0-v_1+v_2-v_3=0
\]
through
\[
[p^2r^2]E_4=-\frac94s^3S
\]
and its two companion coefficients.  On \(S=0\),
\[
C=
\left(u_1-2u_2+3u_3-v_1+2v_2-3v_3\right)^2.
\]
Thus the displayed linear factor also vanishes.

The remaining \(r\)-linear \(E_4\) system has rank two and a clean-room
pivot \(6s^4\).  All four equations are checked after back-substitution.

One initially selected binary \(E_4\) pivot contained
\[
V=v_1-2v_2+3v_3.
\]
The audit did not discard its zero set:

- on \(V\ne0\), a pivot
  \(-9s^2V^2/4\) solves the system and literal substitution gives
  \(\det L=0\);
- on \(V=0\), the system is rebuilt before division and has a pivot
  \(-9s^2\); literal substitution again gives \(\det L=0\).

Every \(E_5\) and \(E_4\) coefficient is asserted to vanish after the
appropriate complete solution.  Since a Keller map has
\(\det L=\det JF(0)\ne0\), the entire punctured intersection is excluded.

After the formulas were frozen, comparison with the independent PARI
boundary verifier revealed an even cleaner global binary \(E_4\) pivot
\(9s^2\), avoiding the \(V\)-split.  This is compatible with, and stronger
than, the explicit two-chart clean-room cover.

## 3. Origin

At \(k=s=0\), a fresh rank-five \(E_6\) solve has constant pivot
\[
31104.
\]
After the complete solve, two necessary \(E_4\) coefficients are
\[
[p^3r]E_4=3b_{qr}^2,\qquad
[q^3r]E_4=\frac13(3b_{qr}-4L_{33})^2.
\]
They force \(b_{qr}=L_{33}=0\).  Exact substitution into all five
\(E_6\)-pivot formulas then sets the other five nonbinary quadratic
coefficients to zero.

The contact is zero, so every nonlinear term now depends only on \(p,q\).
After subtracting the constant, invertibility of \(L\) permits a target
linear normalization to
\[
(g_1(p,q),g_2(p,q),r+g_3(p,q)).
\]
The first two coordinates are a plane Keller map of degree at most four.
Moh's unconditional degree-\(<100\) theorem makes that plane map an
automorphism, and the triangular lift is an automorphism.  If \(L\) is
singular, the map was not Keller in the first place.

It is unnecessary to solve \(E_5\) at the origin: the displayed \(E_4\)
identities are necessary for every Keller solution and already force the
binary collapse.

## Post-freeze comparison

The clean-room formulas agree with:

- the independent PARI transverse-plane verifier;
- the independent PARI punctured-intersection and origin verifier; and
- the earlier legacy SymPy descent after its documented certificate gap is
  repaired by explicit \(S\)-forcing and complete-residual assertions.

Some pivot constants differ because different rows and variables were
selected.  Their zero loci agree, and no mathematical mismatch was found.

## Verification

Run:

```sh
./verify_strict.sh
```

The terminal marker is:

```text
D4_DN3_CLEANROOM_FULL_EXCLUSION_STRICT_PASS
```

The wrapper runs all four standalone clean-room charts, rejects disabled
Python assertions, runs the independent PARI transverse verifier, and runs
the mutation-guarded independent PARI boundary verifier.

## Disclosure

This audit and its code were produced with substantial AI assistance.  The
work is not peer reviewed.  Exact computer-algebra checks certify the
encoded algebra only; they are not a substitute for human review of the
normal-form taxonomy or the surrounding quartic program.
