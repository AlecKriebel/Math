# Certified level-five branch certificate

First released: **2026-07-25T11:23:41Z**.

## Result

Let \(F\) be the announced degree-seven Keller map of generic degree three,
and write
\[
W_m=\underbrace{S_3\wr\cdots\wr S_3}_{m\ {\rm factors}}
\leq S_{3^m}.
\]
The quotient-tower calculation below supplies a transposition on exactly one
bottom three-leaf block at level five.  The previously certified equality
\(\operatorname{Mon}(F^{\circ4})=W_4\) and the all-level full-cycle inertia
theorem then give
\[
\boxed{\operatorname{Mon}_{\mathbb C}(F^{\circ5})=W_5.}
\]
This is geometric monodromy over \(\mathbb C\), in its natural degree \(243\)
action.  Its order is
\[
|W_5|=6^{1+3+9+27+81}
=14331818396160659865344412250308798484976574959068545045852379196157177795134806700610715385856.
\]

This finite-level result does **not** prove the all-iterate wreath-product
statement.

## Certificate

Restrict the target to the line \((1,2,s)\).  Let \(X_i\) be the \(i\)-th
successive inverse point and put
\[
N_i(s)=\operatorname{Norm}\bigl(\Delta(X_i)\bigr),
\]
where the norm is through the rank-\(3^i\) inverse quotient algebra.  At
\[
p=23,\qquad s_0=3,
\]
the target discriminant followed by the four inverse-level norms is
\[
(\Delta(1,2,s_0),N_1(s_0),N_2(s_0),N_3(s_0),N_4(s_0))
=(10,22,10,4,0)\pmod {23}.
\]
Thus every lower cover is unramified at the candidate point.

The norms of the five cubic leading coefficients are
\[
(2,14,19,11,1),
\]
and the norms of all twelve denominators inverted by the four rational
reconstruction steps are
\[
(18,14,5,\;2,8,21,\;13,13,7,\;8,17,12).
\]
Every displayed guard is a unit modulo \(23\).  Hence the rank-\(81\)
quotient tower specializes without a pole or degree drop.

The simple-zero check is performed over \(\mathbb Z/23^2\mathbb Z\):
\[
\begin{array}{rcl}
23^2&=&529,\\
N_4(3)&=&460=20\cdot23,\\
N_4(3+23)&=&299=13\cdot23,\\
N_4(3+2\cdot23)&=&138=6\cdot23.
\end{array}
\]
Consequently
\[
\frac{N_4(3+23)-N_4(3)}{23}=16\pmod {23},
\]
while the two-step difference is \(9=2\cdot16\pmod {23}\).  Thus
\[
N_4'(3)=16\neq0\pmod {23}.
\]

There is also a sheet-level check that uses only scalar dual-number
arithmetic, not quotient-algebra determinants.  The unique rational
vanishing path is
\[
(t_1,t_2,t_3,t_4)=(10,22,13,1),
\]
and the successive inverse points modulo \(23\) are
\[
(2,18,22),\quad(11,1,6),\quad(10,9,13),\quad(22,2,21).
\]
Implicit differentiation along this path gives
\[
\frac{d}{ds}\Delta(X_4)=18\neq0\pmod {23}.
\]
The final inverse cubic at \(X_4=(22,2,21)\) has the simple root \(1\) and
the double root \(22\).

## From the modular zero to geometric inertia

Work over \(\mathbb Z_{(23)}[s]\), localized at all displayed leading and
reconstruction guards.  The four cubic quotients form a finite free algebra
\(E\) of rank \(81\).  Localizing further at the four nonzero lower
discriminant norms makes \(E\) étale.  If \(d=\Delta(X_4)\), then
\[
N_4(s)=\operatorname{Norm}_{E/R}(d)=A(s)/B(s)
\]
with \(B(3)\) a \(23\)-adic unit.  The modular and prime-square calculations
give
\[
A(3)=0\pmod {23},\qquad A'(3)=16B(3)\neq0\pmod {23}.
\]
Hensel's lemma produces a unique \(23\)-adic zero \(\sigma\equiv3\pmod
{23}\).  Let \(P\) be the characteristic-zero irreducible factor containing
that zero.  It occurs to multiplicity one and divides no lower discriminant
or guard.

At the generic point of \(P\), the norm-valuation formula is
\[
\operatorname{ord}_{P}\operatorname{Norm}(d)
=\sum_{\mathfrak q\mid P}
 f(\mathfrak q/P)\operatorname{ord}_{\mathfrak q}(d)=1.
\]
Every summand is a nonnegative integer.  Exactly one prime above \(P\)
therefore has residue degree one and a simple zero of \(d\); every other
sheet is unramified.  The discriminant of the final inverse cubic
\[
2aT^3-bT^2+2T-c
\]
is \(-4\Delta(a,b,c)\).  Its leading coefficient is a unit, and a simple
discriminant zero is not the triple-root locus.  Geometric inertia is thus
one transposition supported on one bottom block of three leaves.

## Wreath-product conclusion

Geometric monodromy embeds in \(W_5\), and its projection to the first four
levels is the already certified full group \(W_4\).  The all-level Newton
argument supplies a \(243\)-cycle \(\alpha\).

Label the leaves so that the \(81\) bottom blocks are
\[
\{j,j+81,j+162\},\qquad0\leq j<81.
\]
Then \(\alpha^{81}\) is a three-cycle on every bottom block.  The new
transposition and its \(\alpha^{81}\)-conjugate generate \(S_3\) on one
block.  Conjugating this local \(S_3\) by
\(\alpha^j,\ 0\leq j<81\), gives \(81\) factors with disjoint supports and
hence the entire bottom kernel
\[
S_3^{81}.
\]
A subgroup of \(W_5\) containing this kernel and surjecting to \(W_4\) is
all of \(W_5\).

## Verification and disclosure

Run

```console
/usr/bin/python3 ../w4_search/test_finite_field_norm.py
/usr/bin/python3 test_depth4_evaluator.py
/usr/bin/python3 verify_w5_modular.py
./audit_w5_hostile/verify_strict_and_faults.sh
```

The first suite tests the underlying finite quotient-algebra arithmetic.  The
second checks that the depth-agnostic loop exactly reproduces the banked
\(W_4\) profile and that its fast and diagnostic paths agree.  The third
recomputes every number displayed above, the scalar sheet derivative, the
final double root, and the elementary \(S_3^{81}\) kernel lemma.

The hostile replay imports none of that quotient-vector code.  It builds the
rank \(1,3,9,27,81\) algebras as block regular-representation matrices,
checks the companion relation, forward reconstruction, and resolvent recovery
at every level, and independently reproduces all norm and derivative data.
It also audits the norm-valuation and geometric group steps and rejects
twelve injected faults.  Its strict run used about \(18.9\) MiB peak resident
memory.  The audit caught and corrected an initial wording error that confused
total degree seven with generic degree three; no arithmetic claim changed.

This work was produced with substantial AI assistance.  It is a public
computational research draft, **not peer reviewed**.  Exact checks establish
facts about the encoded algebra; they are evidence supporting the proof and
are not a substitute for expert mathematical review.
