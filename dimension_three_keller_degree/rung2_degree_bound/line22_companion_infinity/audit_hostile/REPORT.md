# Hostile audit: line-\((2,2)\) companion at infinity

**Initial audit:** 2026-07-25T07:34:00Z.
**Resonance audit completed:** 2026-07-25T10:07:13Z.

## Verdict

**PASS.**  No omitted orbit, hidden division, false zero specialization,
or surviving lower branch was found.

The exact scope is:
\[
p=x^2,\qquad q=yz,\qquad R_3=xq.
\]

1. Every valid outer-critical-at-infinity form
   \[
   H_4=((p-aq)^2,q^2,0),\qquad a\in\mathbb C,
   \]
   is impossible.
2. If both outer critical points are finite, normalize
   \[
   H_4=((p-tq)^2,(p-q)^2,0).
   \]
   Every orbit with \(t\ne1\) is impossible, including the single
   reciprocal resonance orbit \(t=-2\sim-1/2\).  The value \(t=1\) is the
   degenerate, coincident-critical-point form and is not a line-\((2,2)\)
   double cover.

## 1. Stabilizer and orbit coverage

The unique double line forces \(x'=\alpha x\).  On \(x=0\), preservation
of the reduced rank-two member \(yz\) forces the pair \(y',z'\) either to
preserve or swap the two lines \(y=0,z=0\).  In the preserving branch,
write
\[
y'=\beta y+r x,\qquad z'=\gamma z+s x.
\]
The \(xy,xz\) coefficients of \(y'z'\) are \(\beta s,\gamma r\).
Invertibility therefore forces \(r=s=0\).  The swapped branch is
analogous.  Thus the induced base action on \(u=p/q\) is exactly
\[
u\longmapsto\lambda u,
\]
with the line swap acting trivially.

Because the companion is \(u=\infty\), there are exactly two outer-pair
families.

### One outer point at infinity

The pair is \(\{a,\infty\}\).  Scaling has two orbits:
\[
a=0,\qquad a\ne0.
\]
The raw \(E_7\), \(E_6\), and \(E_5\) certificates have constant nonzero
minors, so the proof genuinely covers every \(a\), including \(a=0\);
it does not normalize by \(a\).

### Both outer points finite

Every unordered distinct pair is \(\{t,1\}\), with \(t\ne1\).  For
\(t\ne0\), changing which point is normalized to \(1\) gives
\[
t\sim t^{-1}.
\]
The obstruction factors are exactly reciprocal:
\[
\begin{aligned}
t^{18}f_7(1/t)&=f_7(t),\\
t^{10}f_6(1/t)&=f_6(t),\\
t^2f_5(1/t)&=f_5(t).
\end{aligned}
\]
Hence \(-2\) and \(-1/2\) are one orbit.

The orbit \(t=0\) is included in the generic theorem: all three relevant
matrix ranks are maximal there.  It is not identified with infinity,
because its outer pair \(\{0,1\}\) does not contain the companion point.

The projective boundary \(t=\infty\) satisfies
\[
t^{-2}(p-tq)^2\longrightarrow q^2.
\]
After swapping the two target coordinates it is precisely the
outer-critical-at-infinity chart with \(a=1\), already excluded by the
constant-minor argument.

This exhausts the projective outer-pair moduli.

## 2. Complete raw \(E_7\) kernels

For the finite chart, an exact maximal minor is
\[
-347892350976
(t-1)^{10}(t+2)^4(2t+1)^4.
\]
For the outer chart, the recorded maximal minor is the constant
\[
-5566277615616.
\]

In both charts there are eight independent kernel directions: the six
first-integral directions
\[
(x^3,0,0),\ (xq,0,0),\ (0,x^3,0),\ (0,xq,0),\
(0,0,p),\ (0,0,q)
\]
and the \(y,z\) source-translation jets.  Their independence minor is the
constant \(4\).  Thus the kernels are complete wherever the displayed
maximal minors are nonzero, and for every \(a\) in the outer chart.

The exact finite special ranks are
\[
\operatorname{rank}E_7=
\begin{cases}
18,&t=0,\\
14,&t=-2,-1/2,\\
8,&t=1.
\end{cases}
\]
The outer rank is \(18\) at both \(a=0\) and a nonzero representative.

## 3. Affine and target gauges

After using the \(y,z\) translations, the kernel has
\[
U=Ax^3+Bxq,\quad V=Cx^3+Dxq,\quad W=w_0p+w_1q.
\]
The missing \(x\)-translation is not omitted; it is already a linear
combination of the six first-integral directions.

For the finite chart its jet is
\[
\tau_x=(4x(p-tq),4x(p-q),q).
\]
Translation by \(h=-A/4\) kills the \(x^3\) term of \(U\), changes the
\(x^3\) term of \(V\) to \(C-A\), and merely relabels \(w_1\).
Target shears adding multiples of the third component then kill both
\(xq\) terms.  No division by \(t\) occurs.

For the outer chart,
\[
\tau_x=(4x(p-aq),0,q).
\]
The same \(h=-A/4\) kills the first \(x^3\) coefficient, and target
shears kill the \(xq\) terms without division by \(a\).  Thus the complete
normal form is
\[
H_3=(0,Cx^3,xq),\qquad W=w_0p+w_1q.
\]
Affine translations relabel the lower pieces and replace \(L\) by a
Jacobian matrix at another source point; its determinant remains the
same nonzero Keller constant.  Target row shears preserve \(\det L\).

## 4. \(E_6\) converse

The complete \(E_6\) system is homogeneous linear in ten transverse
variables:

- the \(xy,xz,y^2,z^2\) coefficients of each of the first two quadratic
  components;
- \(\ell_{32},\ell_{33}\).

It is independent of the other eleven quadratic/linear coefficients.
The forcing minors are
\[
\begin{aligned}
-1048576(t-1)^6(t+2)^2(2t+1)^2
   &&\text{(finite)},\\
-4194304
   &&\text{(outer)}.
\end{aligned}
\]
Substitution of the ten zero values annihilates every \(E_6\)
coefficient, proving the converse.  No \(C,w_0,w_1\), modulus, or lower
coefficient is cancelled.

The finite constrained-matrix ranks are \(10\) at \(t=0\), \(8\) at
each resonance, and \(4\) at the degenerate \(t=1\).  The outer rank is
constantly \(10\).

## 5. \(E_5\) and the singular-linear exit

After the complete \(E_6\) solve, the only still-unforced entries in the
last two columns of \(L\) are
\[
\ell_{12},\ell_{13},\ell_{22},\ell_{23}.
\]
The exact \(E_5\) minors on these four variables are
\[
64(t-1)^2\qquad\text{and}\qquad64.
\]
The full residual is homogeneous in those four entries; setting them to
zero kills every \(E_5\) coefficient.  Hence \(E_5=0\) forces them all to
zero on every valid nonresonant finite orbit and for every \(a\).
Together with \(\ell_{32}=\ell_{33}=0\), columns two and three of \(L\)
vanish, contradicting the Keller condition.

At \(t=0,-2,-1/2\) the restricted \(E_5\) matrix has rank \(4\); at the
invalid \(t=1\) it has rank \(2\).  The resonance required a separate proof
because its larger raw \(E_7\) kernel invalidates the nonresonant cubic
normal form, not because this restricted \(E_5\) matrix degenerates.

## 6. Resonance reconstruction

The fresh PARI/GP backend `verify_resonance_pari.gp` reconstructs the
\(t=-2\) chart without importing the supplied SymPy matrices.

An exact raw \(14\times14\) minor is
\[
-990677827584.
\]
Together with the twelve kernel directions and their independence minor
\(82944\), this proves rank \(14\), nullity \(12\), and completeness.  The
first five directions are exactly two determinant-one target shears and the
three affine source-translation jets.  The remaining seven reconstruct the
displayed resonance normal.

At \(E_6\), denominator-cleared polynomial left syzygies reproduce
\[
w_3^2,\quad w_5^2,\quad Kw_3-w_1^2,\quad Kw_5-w_2^2.
\]
Because the syzygy vectors satisfy the polynomial identity \(M^Tv=0\),
these are necessary at every specialization; no generic denominator is
being cancelled.  They force \(w_3=w_5=w_1=w_2=0\).  On that closed locus,
the constant minor \(5308416\) and direct converse give the complete
rank-eight solve.

The independent \(E_5\) pivot is \(576\), and substitution gives the full
residual
\[
36K(\ell_{32}y^3z^2-\ell_{33}y^2z^3).
\]
For \(K\ne0\), its two distinct monomials force
\(\ell_{32}=\ell_{33}=0\).  For \(K=0\), the pivot formulas make both
columns multiples of \((0,0,1)^T\).  Hence \(\det L=0\) in both branches.

## 7. Independent verification

`verify_companion_infinity_pari.gp` independently reconstructs the raw
coefficient matrices, both complete kernels, all special ranks, reciprocal
orbit factors, translation ledgers, the \(E_6/E_5\) converses, and the
forcing minors directly in PARI/GP.

`verify_companion_infinity_pari_strict.sh` requires zero process status,
rejects diagnostics, and requires the entire output to equal the exact
sentinel.  `test_companion_infinity_guards.sh` tests optimized Python,
diagnostic output, extra output, wrong sentinel, nonzero status, and a
valid control.

`audit_orbits_and_gauges_sympy.py` separately verifies the stabilizer
action, reciprocal quotient, \(t=\infty\) boundary, and the complete
translation/shear ledger.

`verify_resonance_pari_strict.sh` whitelists the entire hostile resonance
transcript.  `test_resonance_fail_closed.sh` rejects mutations of the raw
minor, kernel minor, square chain, reduced \(E_6\) minor, \(E_5\) residual,
and final completion marker.

No algebraic or scope defect was found.  The primary note received only two
precision edits: it now justifies removing the constant term by target
translation and calls the unreduced \(E_6\) rank generic before recording
the constant-rank compatible locus.

Exact checks are evidence about the encoded algebra, not peer review.
