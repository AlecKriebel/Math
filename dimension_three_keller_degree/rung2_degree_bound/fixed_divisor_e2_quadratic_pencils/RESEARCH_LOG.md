# Research log: fixed-divisor \(e=2\) quadratic pencils

## 2026-07-25T08:20:00Z — program opened

The audited all-vertical top obstruction leaves
\[
H_4=(p^2,pq,0),
\]
where the minimal quadratic pencil is one of
\[
\langle x^2,yz\rangle,\qquad
\langle x^2,y^2+xz\rangle.
\]
The complete cubic kernel is \(x\langle p,q\rangle\).  A target pencil
shear therefore reduces the nonzero cubic companion to the triple orbit
\(R=xp=x^3\) or the mixed orbit \(R=xq\).  This gives four lower-identity
packages.  They are separate from the genuine \(e=0\) line-\((2,2)\)
outer-cover cases.

For the rank-two pencil \(p=x^2,q=yz\) and mixed companion \(R=xyz\), the
complete degree-seven normal form found by exact linear algebra is
\[
\begin{aligned}
U&=4Cx^2y+4Dx^2z,\\
V&=Ax^3+Cy^2z+Dyz^2+w_3xy^2+w_5xz^2,\\
W&=w_0x^2+w_3y^2+w_4yz+w_5z^2.
\end{aligned}
\]
The degree-six compatibility equations include
\(Cw_3=Dw_5=0\).  If either \(C\) or \(D\) is nonzero, the next identity
has a nonzero pure-cube obstruction (respectively \(-12C^3\) or
\(12D^3\)).  The remaining branch \(C=D=0\) is now under exact
elimination.

## 2026-07-25T08:34:34Z — both mixed companions excluded provisionally

The rank-two \(C=D=0\) branch closes already at \(E_5\): four literal
coefficients make the last two entries of row one zero and the last two
entries of row two proportional to row three, hence \(\det L=0\).

For the rank-one pencil, exact \(E_6\) compatibility is
\[
Dw_5=0,\qquad Cw_5+Dw_4=0.
\]
The \(D\ne0\) branch has a polynomial \(E_5\) syzygy equal to \(24D^3\).
For \(D=0,C\ne0\), two polynomial syzygies have resultant
\(-250C^9\).  Thus \(C=D=0\).

The zero-normal branch required four specialization charts.  The sole
delicate leaf is
\[
w_4=w_5=0,\qquad d=w_2-w_3\ne0.
\]
After the complete \(E_5\) solve, two literal \(E_4\) coefficients give
\(\ell_{32}(\ell_{23}+w_3\ell_{33})=0\) and
\(\ell_{13}\ell_{32}=0\); these are exactly the two products occurring
in \(\det L\).  Hence every leaf has \(\det L=0\).

`verify_mixed_orbits_sympy.py` passes all exact assertions.  The result is
not promoted until a methodologically independent hostile audit passes.

## 2026-07-25T08:49:20Z — rank-two triple companion excluded provisionally

For \(H_4=(x^4,x^2yz,0)\) and \(R=x^3\), the raw \(E_7\) kernel has
nullity \(18\).  After five legal gauges its thirteen-parameter normal
complement is controlled by a short \(E_6\) split with
\[
K=9A-12w_4.
\]

On \(K\ne0\), an \(E_5\) resultant forces \(w_1=w_2=0\).  The generic
aligned branch has a two-equation \(E_4\) determinant exit.  The two
resonances \(9A=2K\) and \(9A=K\) close respectively by a pure fourth
power and another proportional-row exit.

On \(K=0,A\ne0\), six \(E_5\) equations remove all nonaligned \(B\)
parameters and a fresh rank-drop solve makes \(\det L=0\).  On
\(K=A=0\), nonzero \((w_1,w_2)\) is excluded by a pure fourth power,
with both denominator charts recomputed separately; the origin has two
literal \(E_4\) squares that zero the last two entries of row three.

The exact fail-closed SymPy certificate passes.  The theorem is not promoted
before an independent hostile audit.

## 2026-07-25T08:52:17Z — mixed companions independently audited

The hostile PARI/GP reconstruction passed.  It independently rebuilt both
raw \(E_7\) kernels, the constant-pivot \(E_6\) residual ideals, every
nonzero-normal cube obstruction, all four rank-one zero-normal charts, and
the final determinant identities.  It also cleared the apparent
\((C-w_4)^{-1}\) left-kernel artifact and evaluated the polynomial
syzygies directly at \(w_4=C\), obtaining \(2C^4\) and \(-6C^4\).

Strict-runner and arithmetic-corruption/missing-attestation injections pass.
The mixed-companion theorem is promoted to audited.  Its scope is exactly
the two \(e=2\) forms with \(R=xq\).

## 2026-07-25T09:46:39Z — rank-two triple companion audited

- Hostile PARI/GP reconstruction confirmed the raw rank-eight
  \(E_7\) system, five legal gauges, thirteen normal directions, the
  constant-pivot \(E_6\) split, and every lower branch.
- The audit found three unsafe specializations in the provisional proof:
  the aligned \(9A=2K\) zero-end resonance, the
  \(r=0,B_3=0\) tail chart, and the terminal \(B_1=0\) rank drop.
- Each was rebuilt before solving.  The repairs respectively close by
  two squares plus a \(2\times2\) minor, a fresh
  \([y^4]E_4=4s^4/27\) contradiction, and a global \(E_5\) product
  split followed by fresh \(E_4\) rows.
- Corrected SymPy, independent PARI/GP, optimized-mode rejection, and
  fail-closed injections all pass.  Verdict: PASS.
- The rank-two canonical pencil is now completely excluded for both
  cubic companion orbits.  The rank-one triple companion is the sole
  remaining fixed-divisor \(e=2\) lower frontier.

## 2026-07-25T10:48:53Z — entire fixed-divisor \(e=2\) row closed

- The remaining rank-one triple package
  \[
  H_4=(x^4,x^2(y^2+xz),0),\qquad(H_3)_3=x^3
  \]
  passed its primary exact certificate, independent \(A=0\) and
  \(A\ne0\) PARI/GP reconstructions, and a separate hostile replay.
- Hostile review found a hidden \(a_3=0\) specialization under an
  \(a_3^4\)-supported \(E_4\) pivot.  The leaf was rebuilt with an
  \(s^8\)-supported pivot and again forces \(\det L=0\).  It also
  corrected the axis-gauge explanation to use an \(x\)-translation plus
  free-\(V\)-tail relabeling.
- All strict transcripts and fault injections pass.  No theorem leaf
  survives.
- The top theorem gives exactly two canonical pencils and two cubic
  companion orbits for each.  The mixed package and the two triple
  packages now exclude all four.  Hence the entire all-vertical
  fixed-divisor \(e=2\) quadratic-pencil row is closed.
- This removes a quartic taxonomy row but does not exclude all quartic
  leading forms.  The universal total-degree floor remains \(4\).

## 2026-07-25T22:53:24Z — prior row-closure claim retracted

The post-freeze bridge audit found that the preceding conclusion was too
strong.  The four lower packages identify the marked component gcd \(h\)
with the pencil's unique double-line member \(s\).  They therefore close
only the marked-equal sublocus \(h=s\).  The marked-distinct locus
\(h\ne s\) has a genuine \(3+\mathbb P^1+3\) nonzero companion quotient
and was not covered.  The parent note has been corrected, and the frozen
row remains provisional while that quotient is treated.

This is a scope failure, not an extra frozen row.  In accordance with the
freeze protocol, all former language saying that the entire row was closed
is historical and superseded by this entry.

## 2026-07-26T00:19:51Z — marked-distinct candidate closure

The thirteen marked-distinct strata now have exact candidate routes:

- three zero companions use the independently audited
  quadratic-component automorphism exit;
- a single calculation over the punctured projective parameter line
  excludes `CTAU` and its finite `CT` boundary;
- six `CH/CS` endpoints have fresh exact solves, including one genuine
  invertible survivor through \(E_5\) that is killed only by \(E_4\);
- the two discrete `CO` orbits have complete raw \(E_7\) quotients and
  exhaustive \(E_6/E_5\) determinant exits.

The strict candidate aggregate passes.  A fresh clean-room bridge auditor
has independently reconstructed the 45 coefficient-chart routing, the
thirteen-stratum denominator, and both `CO` computations.  Promotion is
withheld until that auditor finishes the localization guards and executable
coverage ledger.
