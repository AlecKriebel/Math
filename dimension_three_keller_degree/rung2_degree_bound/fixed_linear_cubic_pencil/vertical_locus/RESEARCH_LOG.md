# Research log: vertical fixed-linear cubic pencil

## 2026-07-25T10:55:06Z — vertical program opened

- Kept the audited horizontal theorem fixed and isolated all new work in
  this directory.
- Normalized the unique vertical member to
  \(p=h^m r_{3-m}\), \(1\le m\le3\).
- Applied the existing homogeneous first-integral descent at every prime
  of the vertical fibre, retaining the unknown order at infinity rather
  than setting it to zero.

## 2026-07-25T11:12:00Z — multiplicity obstruction

- For a degree-\(d\) normal first integral \(G\), derived
  \[
  4v_f(G)-d(a+\mathbf1_{f=h})=a\,\operatorname{ord}_\infty R
  \]
  at every multiplicity-\(a\) component of \(p=0\).
- For \(d=3\), the congruences exclude all \(m=1\) and \(m=2\) shapes,
  independently of the companion cubic \(q\).
- For \(m=3\), divisor degree gives the exact cubic kernel
  \(\langle h^3,q\rangle\).
- Repeating the calculation for \(d=2\) recovers exactly the simple-square
  witness \(p=hL^2,G=hL\), excludes \(m=2\), and gives \(G=h^2\) for
  \(m=3\).

## 2026-07-25T11:28:00Z — source orbits and boundaries

- Classified the \(m=1\) quadratic cofactor under the parabolic preserving
  \(h=0\) by the pair of ranks
  \((\operatorname{rank}(r|_h),\operatorname{rank}r)\), obtaining five
  and only five representatives.
- Recorded \(q\) as an honest quotient by the full stabilizer instead of
  pretending its continuous moduli form finitely many orbits.
- Located every nonminimal boundary using the fact that a nonminimal
  cubic pair is binary in a two-dimensional linear space.  The
  triple-vertical boundary consists of cubics binary in \(h\) and one
  additional linear form.

## 2026-07-25T11:39:00Z — top-three escape

- On the primitive sample
  \(p=z^3,q=x^3+y^3\), found exact representatives of both nonzero cubic
  companion orbits, \(G_3=z^3\) and \(G_3=q\).
- With \(L_0=I,H_2=0\), direct determinant expansion gives
  \(E_8=E_7=E_6=0\) for both.  Lower coefficients are nonzero, so these
  are obstruction witnesses and not Keller maps.
- This pins the next genuine frontier at \(E_5\) or below.

## 2026-07-25T12:02:00Z — exact E7 split and E5 escape

- Row expansion on the triple-vertical branch gives
  \[
  E_7=z^3\{q,4zW-3U\}_{x,y}
  \]
  for \(G_3=z^3\), and
  \[
  E_7=\{q,4z^4W-4z^3V+qU\}_{x,y}
  \]
  for \(G_3=q\).
- For the primitive sample \(q=x^3+y^3\), the choice
  \[
  H_3=(q+\tfrac43z^3,0,z^3),\qquad
  H_2=(0,xz,z^2),\qquad L_0=I
  \]
  has determinant
  \[
  (1+3\tau^2x^2)(1+2\tau z+3\tau^2z^2).
  \]
  Therefore \(E_8,E_7,E_6,E_5\) vanish exactly while \(E_4\ne0\).
- Added the three binary-root strata as a finite atlas for the full
  triple-vertical stabilizer quotient, retaining rather than suppressing
  the residual continuous moduli.

## 2026-07-25T12:35:00Z — full E7 gauges and first E4 rank ledger

- Solved both \(E_7\) companion families modulo only legal target shears:
  \[
  \begin{array}{ll}
  G_3=z^3:&U=\frac43zW+aq,\quad [z^3]V=0,\\
  G_3=q:&U=dz^3,\quad V=zW+fz^3.
  \end{array}
  \]
- Proved the degree-six first-integral kernel needed in the second line is
  \(\operatorname{Sym}^2\langle z^3,q\rangle\), using the same exact
  vertical-divisor partition as for degrees two and three.
- Partitioned the \(z=0\) solve by the squarefree/double/triple root type
  of \(q_0=q|_{z=0}\).  On the vertical \(a\ne0\) branch, \(E_6\) forces
  \(W_0=0\) away from the triple-root locus.  The binary \(E_5\) matrix has
  precisely the two double-root/root-line rank drops and the
  \(W/z|_{z=0}=0\) leaf; squarefree root collisions do not drop rank.
- On the generic nontriple vertical leaf, \(E_4\) forces
  \(\kappa A_0=aB_0\), where \(V_0=\kappa q_0\).
- On the nonvertical companion, away from the triple-root locus,
  \(E_6,E_5,E_4\) successively force
  \[
  A_0=0,\qquad \bar L_1=0,\qquad
  A=\alpha z^2\ \text{or}\ B_0=0.
  \]
- Recorded every exceptional divisor and the remaining seven leaves in
  `E8_E4_RANK_LEDGER.md`; none is declared excluded.
- The exact symbolic ledger check passed and retains the \(E_5\) survivor
  as a regression guard.

## 2026-07-25T11:36:16Z — nonvertical nontriple companion excluded

- Returned from the \(E_4\) plane split to the full \(E_6,E_5\)
  coefficient systems.
- On the branch \(A=\alpha z^2\), a constant pivot minor
  \(-2^{19}\) forces \(B_0=0\), identifies the \(z\)-linear part of \(B\)
  with the \(x,y\)-part of the third linear row, and kills the \(x,y\)
  part of the second linear row.
- On the branch \(B_0=0\), a constant pivot minor \(-2^{11}\) first
  kills the \(z\)-linear part of \(A\), then gives the same solution.
- Together with the \(E_5\) condition that the first linear row is a
  multiple of \(dz\), both branches force two proportional rows of the
  linear part.
- The minors are literally constant for both
  \(q_0=xy(x-y)\) and \(q_0=x^2y\); all lower \(q\)-moduli, \(W\), and
  the companion scalars remain symbolic.  Thus no internal rank divisor
  was discarded.
- Added a separate exact checker
  `verify_nonvertical_nontriple_e4_sympy.py`.  The triple-root \(q_0=x^3\)
  leaf remains open and separate.

## 2026-07-25T11:39:23Z — nonvertical triple-root companion excluded

- Classified the full triple-root stabilizer locus.  The minimal part has
  exactly three families:
  \[
  x^3+y^2z+\alpha xz^2+\beta z^3,\quad
  x^3+xyz+\beta z^3,\quad
  x^3+yz^2.
  \]
  The remaining coefficient shape is binary in \(x,z\) and therefore
  nonminimal.
- Reconstructed the full \(E_6,E_5\) systems on all three families with
  every displayed modulus, all six coefficients of \(W\), and both
  companion scalars symbolic.
- Found literal constant \(14\times14\) minors
  \(-2^{24}3^8\), \(-2^{18}3^6\), and \(-2^{20}3^7\).
  All three solves force \(A\) to be a multiple of \(z^2\), identify the
  \(z\)-linear part of \(B\) with the third linear row, and kill the
  \(x,y\)-parts of the first two linear rows.
- Hence the linear part is singular on the entire triple-root locus.
  Combined with the nontriple lemma, the whole nonvertical companion is
  provisionally closed.
- Added the standalone note and exact checker
  `NONVERTICAL_TRIPLE_ROOT_LEMMA.md` and
  `verify_nonvertical_triple_root_sympy.py`.

## 2026-07-25T20:53:41Z — complete nonvertical companion hostile-audited

- A dependency-free sparse-polynomial reconstruction independently derived
  the legal \(E_7\) gauge, the complete squarefree/double/triple-root atlas,
  all seven literal constant minors, every residual lower equation, and the
  final singular-linear-part contradiction.
- No omitted minimality boundary, parameter divisor, or illegal target shear
  was found.  The complete nonvertical companion \(G_3=q\) is now certified
  excluded on the primitive triple-vertical stratum.
- Scope remains local to this companion.  The vertical companion
  \(G_3=z^3\) keeps the frozen row open.

## 2026-07-25T21:02:00Z — zero-\(\ell\), nontriple vertical subcase reduced

- Targeted construction searches repeatedly approached only a noncompact
  singular-linear-part limit.  The stable relations suggested an exact
  elimination rather than a numerical construction.
- For arbitrary retained lower-\(z\) moduli of \(q\), and for both
  \(q_0=xy(x-y)\) and \(q_0=x^2y\), a literal
  \(2^5 3^{11}s^8\) degree-six minor gives the complete three-parameter
  family
  \[
  V=kq+\frac zs(A-a_5z^2)
    -\frac4{3s}z^2(\ell_{31}x+\ell_{32}y).
  \]
- Degree five forces \(\ell_{31}=\ell_{32}=0\), then a literal
  \(-2^4 3^5s^5\) minor solves the relevant coefficients of \(B\).
  Degree four makes the first two entries of the second linear row
  proportional to the first row, so \(\det L=0\).
- The exact SymPy and optimized-Python fail-closed checks pass.  This
  candidate subcase exclusion is awaiting an independent hostile audit and
  does not close the frozen row.

## 2026-07-25T21:07:39Z — zero-\(\ell\), nontriple subcase hostile-audited

- A fresh dependency-free sparse-polynomial reconstruction checked the
  simultaneous gauges, the complete squarefree/double-root atlas, both
  constant minors, every retained lower-\(z\) modulus, and the final
  singular-linear-part contradiction.
- Negative controls detect mutations of the degree-six solve, degree-five
  solve, and final determinant calculation.
- The audit passed at exactly the candidate lemma's scope.  The result
  excludes this sublocus but does not close the frozen row.

## 2026-07-25T21:22:00Z — first triple-root zero-\(\gamma\), zero-\(\ell\) chart

- On \(q=x^3+yz^2\), \(W=wz^2\), constant \(E_6,E_5,E_4\) pivots give
  the complete successive solutions and force the linear part singular.
- A fresh dependency-free sparse reconstruction independently checked the
  chart normalization, all pivots and residuals, and fail-closed mutations.
- The one-chart result passed hostile audit.  A unified calculation now
  covers the other two minimal triple-root charts and awaits its own
  broader-scope hostile audit.

## 2026-07-25T21:31:00Z — unified triple-root zero-\(\gamma\), zero-\(\ell\) audit

- Constant pivots extend the one-chart calculation uniformly to the
  \(y^2z+\alpha xz^2\), \(xyz\), and \(yz^2\) minimal charts.
- A fresh sparse reconstruction independently derived the atlas, gauges,
  pivots, complete solves, residuals, and singular-linear-part conclusion,
  retaining \(\alpha,w\) and testing mutations on every chart.
- The unified hostile audit passed.  The result still excludes only the
  \(\gamma=\ell=0\) triple-root sublocus, not the frozen row.
