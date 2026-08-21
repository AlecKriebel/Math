# Research log: binary fixed-quadratic line double cover

## 2026-07-25T10:01:53Z — frontier opened

- Opened the unresolved binary locus in
  \((e,a,b,\delta,\nu)=(2,1,2,1,2)\):
  \[
  H_4=h(p,q)(p^2,q^2,0),\qquad 0\ne h\in\mathbb C[p,q]_2.
  \]
- Isolated the full stabilizer of the reduced squaring cover.  On the
  pencil \(\langle p,q\rangle\), it is the diagonal torus together with
  the swap \(p\leftrightarrow q\); source changes in the complementary
  coordinate act trivially on \(h\).
- The induced action on
  \(h=Ap^2+Bpq+Cq^2\), up to a common target scalar, is
  \[
  [A:B:C]\longmapsto
  [A\alpha^2:B\alpha\beta:C\beta^2],
  \]
  together with \(A\leftrightarrow C\).
- The set-theoretic orbit space is a one-parameter interior
  \(\kappa=B^2/(AC)\in\mathbb A^1\), plus three boundary orbits represented
  by \(p^2\), \(pq\), and \(p(p+q)\).  The square value in the interior is
  \(\kappa=4\); it is not equivalent to the branch square \(p^2\).

## 2026-07-25T10:08Z — top identities reduced to binary syzygies

- For \(P=hp^2,\ Q=hq^2,\ R=(H_3)_3\), direct determinant expansion gives
  \[
  E_8=8h^2pq\,R_r.
  \]
  Hence \(R\) is a binary cubic.
- With \(U=(H_3)_1,\ V=(H_3)_2,\ T=(H_2)_3\),
  \[
  E_7=J(Q,R)U_r-J(P,R)V_r+8h^2pq\,T_r.
  \]
- Splitting by powers of the complementary source variable gives exact
  systems with \(2,5,8\) unknown coefficients.  Transverse squarefree
  examples have ranks \((2,5,8)\), while generic double-factor examples
  have ranks \((2,5,7)\).  Thus the first has no \(E_7\) tangent and the
  second has a unique \(r^0\) tangent.
- A first hostile sample check found that \(\gcd(h,R)=1\) is not sufficient
  to determine the last rank.  For \(h=p^2+q^2\), the transverse cubics
  \(p^3+p^2q+q^3\) and \(p^3+q^3\) give last ranks \(7\) and \(6\),
  respectively, whereas
  \(p^3+2p^2q+3pq^2+4q^3\) gives the generic rank \(8\).
  The exhaustive \(E_7\) tree must therefore retain the Hilbert--Burch
  splitting invariant, not only a common-root index.
- These are top-identity statements only.  No surviving tangent has been
  called a Keller map.

## 2026-07-25T10:19:35Z — determinant and Hilbert--Burch split

- Factored the complete \(8\times8\) \(r^0\) determinant on all four
  fixed-divisor charts.  In the interior chart it is
  \[
  -41472(\eta^2-4)(4c-3d\eta)(3a\eta-4b)
  \operatorname{Res}(h,R)^2.
  \]
  This retains the orbit modulus \(\kappa=\eta^2\) and exposes two
  ramification-contact divisors not detected by \(\gcd(h,R)\).
- Verified that the Hilbert--Burch degree calculation remains valid even
  though \(P,Q\) share \(h\).  Outside constant-linear dependence,
  \(\delta=\deg\gcd(J(Q,R),J(P,R),J(P,Q))\le4\), and the six possible
  \(\{k_1,k_2\}\) shapes give exact tangent nullities.
- Proved that constant-linear dependence is unique, up to swap:
  \(h=p^2,\ R=p^3\).  Its rank tuple is \((1,2,3)\).
- Reconstructed the complete signed \(E_6\) block identity.  If the
  \(r^0\) determinant is nonzero, \(E_7\) and \(E_6\) make every nonlinear
  piece binary, so the established degree-four plane exit proves
  automorphy.  Every counterexample must therefore lie on the displayed
  determinant divisor.
- Recorded the exact top-three survivor
  \[
  F=(p+p^4,\ r+p^2q^2,\ q+p^3).
  \]
  It has \(E_8=E_7=E_6=0\) and \(\det L_0=-1\), but
  \(E_3=-4p^3\), so it is explicitly not Keller.

## 2026-07-25T10:37:42Z — scope repair and first \(\delta=1\) contacts

- Separated the \(R=0\) boundary from both the Hilbert--Burch table and
  the power-fibre exception.  Its exact rank tuple can differ from both;
  geometrically the quadratic-component coordinate lemma plus the plane
  low-degree exit already gives automorphy.
- Filled the degree-sum gap in the Hilbert--Burch proof.  Wedge the two
  gradient columns and compare with a minimal Hilbert--Burch basis:
  the determinant of the change-of-basis matrix is a scalar multiple of
  the removed gcd \(g\), hence \(k_1+k_2=\deg g=\delta\).
- Added exact \(E_6\) contact-minor certificates on four open
  \(\delta=1\) components.  The \(h=pq\) component routes to
  \(R=dq^3\); all three one-branch components route to their pairwise
  intersections.
- Found a genuine \(E_6\)-surviving branch-square locus:
  \[
  h=p^2,\qquad R=bp^2q+dq^3,\qquad bd\ne0.
  \]
  The explicit family (31) satisfies \(E_8=E_7=E_6=0\), but exact
  expansion gives
  \(E_5=-4p^3(bp^2+3dq^2)\ne0\).  It is therefore an exact top-three
  survivor, not a Keller map.
- `verify_orbits_top_sympy.py` and `verify_e6_delta1_sympy.py` both pass
  with assertions enabled.  The remaining \(\delta=1\) work is the
  interior orbit and deeper intersections; \(\delta=2\) has not yet been
  eliminated.

## 2026-07-25T10:51:42Z — exact \(\delta=1\) contact classification

- Closed the interior ramification-contact calculation.  On
  \(3a\eta=4b\), the leading contact coefficient and three exact wedges
  reduce the \(a\ne0\) chart to two resultants with gcd \(\eta^2\).
  Two incompatible factors give the same conclusion in the \(a=0\)
  chart.  Thus contact forces \(\eta=0,\ b=d=0\).
- This leaves a second genuine \(E_6\)-surviving normal form:
  \[
  h=p^2+q^2,\qquad R=ap^3+cpq^2,\qquad c(a-c)\ne0.
  \]
  Its normalized tangent has \(K_N=-2\beta\).  An exact sparse
  completion satisfies \(E_8=E_7=E_6=0\) but has the nonzero \(E_5\)
  displayed in (38).
- Parameterized the common-root divisor by
  \(h=(p-sq)(sp-q)\), \(R=(p-sq)S\).  Endpoint evaluations force both
  contact multipliers to be \(-2s\); evaluation at the common root then
  routes contact to \(p-sq\mid S\), hence to \(\delta\ge2\).
- On the doubled nonbranch-root divisor, reduction modulo \(p+q\) gives
  \(-324q^5(a-b+c-d)^3\), so the exact-\(\delta=1\) open part is also
  obstructed.
- Consequently the only exact-\(\delta=1\) \(E_6\)-surviving normal
  forms, up to the stabilizer and swap, are the two rows in (41).
  This is a top-identity classification, not a Keller classification.
  The exact verifier passes all new resultant, evaluation, and full
  determinant assertions.

## 2026-07-25T11:28:03Z — exact \(\delta=1\) lower exclusion

- Replaced both sparse \(E_5\) guards by the completely general lower
  family: all binary \(H_3,H_2\) coefficients and all nine entries of
  the linear part were retained.
- On the branch-square survivor, solved \(E_6\) and \(E_5\) exactly.
  The remaining \(E_4\) is
  \[
  2bM_3p^4+(bM_0+6dM_3)p^2q^2-3dM_0q^4.
  \]
  It forces \(M_0=M_3=0\) and exposes the nonzero kernel vector
  \(L(\kappa,0,-v_2)^T=0\).
- On the interior survivor, the analogous full solve gives
  \[
  [3aM_1+(-3a+4c)M_4]p^4+
  [(6a-c)M_1+cM_4]p^2q^2+2cM_1q^4.
  \]
  It forces \(M_1=M_4=0\) and
  \(L(0,\kappa,-u_1)^T=0\).
- Therefore no Keller counterexample in this binary fixed-quadratic row has
  exact \(\delta=1\); Keller maps on the stratum exit as automorphisms.  The
  surviving counterexample frontier is \(\delta\ge2\), together with the
  separately constant-dependent power fibre.
- Froze the result in `DELTA1_EXCLUSION_NOTE.md`.  The strict verifier
  runs a general-family SymPy derivation and an independent PARI/GP
  replay, with mutation guards for every divisor
  \(b,d,c,a-c,\kappa\) and both final kernel vectors.

## 2026-07-25T11:59:13Z — exact \(\delta=2\) HB classification

- Derived a local linear-factor valuation formula for Jacobians of
  binary quartics and cubics.  Applied to
  \[
  g=\gcd(J(Q,R),-J(P,R),J(P,Q)),
  \]
  it gives an exhaustive enumeration of exact-\(\delta=2\) incidence
  types on all four fixed-divisor orbit charts.
- Corrected the initial working hypothesis that the
  \(\{k_1,k_2\}=\{2,0\}\) Hilbert--Burch shape might be absent.  It
  genuinely occurs.  A mandatory rational regression is
  \[
  h=p^2+4pq+q^2,\qquad
  R=p^3+3p^2q+6pq^2+2q^3.
  \]
  It has \(g=2pq\), \(\operatorname{Res}(h,R)=-18\), block ranks
  \((2,4,6)\), and literal \(r^1\)-kernel
  \((-5,-1,1,5,3)^T\).
- Completed the exact split classification.  Every boundary-orbit
  exact-\(\delta=2\) point has shape \(\{1,1\}\).  The complete
  \(\{2,0\}\) list in the interior is:
  two ramification contacts at \(\kappa=16\); one fixed root plus one
  ramification contact at \(\kappa=16/3\); and a codimension-one
  coefficient locus on the doubled-root orbit \(\kappa=4\).
- Froze the proof in `DELTA2_HB_STRATIFICATION.md`.  The strict SymPy
  and PARI/GP suite checks every decisive maximal minor, the three
  exceptional mechanisms, exact gcds, rank tuples, resultants where
  applicable, and literal kernel vectors.
- The highest-information next split is now the rational
  \(\kappa=16\), \(\{2,0\}\) family, because its nonzero \(r^1\)
  tangent enters \(E_6\) one level earlier than the \(\{1,1\}\) row.

## 2026-07-25T12:16:54Z — provisional \(\kappa=16\) exclusion

- Retained the complete integrated \(E_7\) family on the
  \(\kappa=16,\{2,0\}\) row, including both \(r^0\) tangents, the genuine
  \(r^1\) tangent, all binary \(H_3,H_2\) coefficients, and all nine
  entries of the linear part.
- The \(r^3\) coefficient of \(E_6\) kills the genuine \(r^1\) tangent.
  The remaining \(r\)-coefficient, including the endpoint mutations
  \(a=-2d\) and \(d=-2a\), kills both \(r^0\) tangents and the two
  quadratic \(r\)-coefficients of \(H_2\).
- The constant \(E_6\) solve leaves a single parameter
  \[
  (A_{1,r},A_{2,r},\ell_{33})
  =\lambda(5p+q,-p-5q,3(a-d)).
  \]
  At \(\lambda=0\), \(E_5\) forces a zero third column of the linear
  part.  At \(\lambda(a-d)\ne0\), triangularizing the third component
  yields a plane Keller map of degree at most four over
  \(\mathbb C(w)\); the banked plane-field and birational Keller exit
  proves automorphy without using the full plane Jacobian Conjecture.
- In the only residual branch \(a=d\ne0,\lambda\ne0\), the complete
  rank-six \(E_5\) solve gives
  \[
  [r]E_4=72a\lambda^2(p+q)^3\ne0.
  \]
- Froze the candidate theorem in
  `DELTA2_KAPPA16_EXCLUSION.md`, the exact SymPy/PARI replay in
  `verify_delta2_kappa16_exclusion_strict.sh`, and the adversarial tasks
  in `KAPPA16_HOSTILE_REVIEW_CHECKLIST.md`.  Promotion awaits hostile
  mathematical replay.

## 2026-07-25T12:25:43Z — provisional \(\kappa=16/3\) exclusion

- Put the one-fixed-root/one-ramification-contact orbit in the rational
  normal form
  \[
  h=(p+q)(3p+q),\qquad
  R=(p+q)(ap^2+2bpq+bq^2),
  \]
  on the exact open \(b(a-b)(a+3b)\ne0\).
- Starting from the complete integrated \(E_7\) family, the
  \(r^3\)-coefficient of \(E_6\) kills the genuine \(r^1\) tangent.
  The remaining \(r\)-coefficient kills all nonlinear \(r\)-terms,
  including on the exceptional divisor \(a=-2b\).
- The constant \(E_6\) kernel is
  \[
  (A_{1,r},A_{2,r},\ell_{33})
  =\lambda(4p+q,-3q,a-b).
  \]
  The \(\lambda=0\) branch has a zero third column; the
  \(\lambda\ne0\) branch exits through the unconditional
  degree-at-most-four plane-field theorem and the birational Keller
  theorem.
- Froze the candidate in `DELTA2_KAPPA16OVER3_EXCLUSION.md`, its hostile
  checklist, and its independent SymPy/PARI strict wrapper.  Promotion
  remains pending.

## 2026-07-25T12:32:17Z — provisional \(\kappa=4\) exclusion and umbrella

- Put the doubled nonbranch-root row in the complete normal form
  \[
  h=(p+q)^2,\quad
  R=ap^3+bp^2q+\frac32d\,pq^2+dq^3,\quad
  d=(5b-6a)/3,
  \]
  on the exact open \(b(3a-2b)\ne0\).
- The full \(E_6\) solve kills the genuine \(r^1\) tangent and every
  nonlinear \(r\)-coefficient without dividing by the exceptional
  divisor \(6a+11b=0\).  Its surviving constant kernel is
  \[
  (A_{1,r},A_{2,r},\ell_{33})
  =\lambda(6p+4q,-2q,6a-b).
  \]
- The zero-column and plane-field exits handle all but
  \(a=b/6,\lambda\ne0\).  On that residual divisor, the complete
  rank-six \(E_5\) solve yields
  \[
  [r]E_4=6b\lambda^2(p+2q)^3\ne0.
  \]
- Froze the candidate in `DELTA2_KAPPA4_EXCLUSION.md` and its
  independent SymPy/PARI strict wrapper.
- Since the exact-\(\delta=2\) HB classification proves that
  \(\kappa=16,16/3,4\) exhaust the \(\{2,0\}\) shape, froze
  `DELTA2_K20_UMBRELLA.md`.  It is only a provisional shape exclusion:
  exact \(\delta=2\) remains open on \(\{1,1\}\), which is now the
  active lower-identity frontier.

## 2026-07-25T12:56:53Z — first provisional \(\{1,1\}\) exclusion

- On the exact-\(\delta=2\) family
  \[
  h=p^2,\qquad R=p(Ap^2+Bpq+Cq^2),\qquad BC\ne0,
  \]
  replaced generic tangent sampling by the lifted contact map on
  \((s^2,st,t^2,x_5,y_5)\).
- Signed \(4\times4\) minors give a rank-four kernel whose exact
  Veronese obstruction is
  \[
  3C^2(256AC+11B^2).
  \]
  The pivot divisor \(\Delta=4AC-B^2=0\) was recomputed with a fresh
  Hilbert--Burch basis and has obstruction \(225B^2\).  The mutations
  \(B=0,C=0\) route to \(\delta\ge3\), while \(A=0\) stays in the
  nonsurviving exact-\(\delta=2\) open.
- The sole nonzero \(E_6\) contact divisor is one stabilizer orbit.
  Its rational regression is
  \[
  R=p(-11p^2+16pq+q^2),\quad
  (U_r,V_r,T_r)=k(4p^2,6pq+q^2,15p+30q),
  \]
  with \(([r^2]H_{2,1},[r^2]H_{2,2})=(6k^2,9k^2)\).
- Retaining every binary lower coefficient and all nine entries of the
  linear part, the complete rank-six \(E_6\) solve gives
  \[
  [r^2]E_5=-24k^3(72p^3+7p^2q-11pq^2+q^3).
  \]
  Hence the nonzero contact fails \(E_5\); the zero-contact branch is
  the all-binary automorphism exit.
- Froze the candidate theorem in
  `DELTA2_11_P2_SIMPLE_FIXED_EXCLUSION.md`, the hostile checklist, and
  a strict SymPy/PARI wrapper.  This closes only one \(\{1,1\}\)
  incidence mechanism, pending hostile replay.

## 2026-07-25T13:12:34Z — both \(h=p^2\), \(\{1,1\}\) leaves closed provisionally

- Treated the second exact-\(\delta=2\) family
  \[
  h=p^2,\qquad R=Ap^3+Cpq^2+Dq^3,\qquad D\ne0.
  \]
  Its generic lifted-contact determinant is
  \(-71663616C^2D^6(27AD^2+4C^3)^3\).
- Recomputed the pivot divisor \(27AD^2+4C^3=0\) in a fresh tangent
  basis; its contact determinant is \(-12288C^2\).
  At \(C=0,A\ne0\), the rank-four kernel misses the Veronese cone.
- Isolated the unique \(E_6\) contact endpoint
  \[
  R=Dq^3,\quad
  (U_r,V_r,T_r)=k(2p^2,q^2,0),\quad(x_5,y_5)=(k^2,0).
  \]
- In the full lower family, \(E_5\) has compatibility
  \(3Dkv_0^2\).  The completed \(E_4\) solve gives
  \[
  E_4=D(6M_3p^2q^2-3M_0q^4),\qquad
  L(k,0,-v_2)^T=(M_0,M_3,0)^T,
  \]
  contradicting invertibility of the linear part.
- Froze `DELTA2_11_P2_BRANCH_CONTACT_EXCLUSION.md`, its hostile
  checklist, and an independent strict SymPy/PARI replay.
- Created `DELTA2_11_LEAF_REGISTRY.md`: two \(\{1,1\}\) leaves are
  closed provisionally and thirteen remain open.  The next active leaf
  is the pivot-generic \(h=pq,R=p^2(Ap+Bq)\), \(AB\ne0\).

## 2026-07-25T13:17:07Z — third provisional \(\{1,1\}\) exclusion

- On
  \[
  h=pq,\qquad R=p^2(Ap+Bq),\qquad AB\ne0,
  \]
  the complete lifted \(E_6\) contact matrix has determinant
  \(-2332800000A^3B^8\).  Thus both tangent parameters and both
  quadratic \(r\)-coefficients vanish on the entire exact open.
- The remaining constant \(E_6\) system has determinant
  \(-3240A^3B\), forcing every nonlinear term to be binary; the
  established plane-field/birational exit proves automorphy.
- The mutations \(A=0\) and \(B=0\) have gcd degrees three and are
  routed rather than divided away.
- Froze `DELTA2_11_PQ_DOUBLE_EXCLUSION.md`, its hostile checklist, and
  an independent strict SymPy/PARI replay.  Updated the leaf registry
  to three provisional closures and twelve open leaves.

## 2026-07-25T13:20:14Z — all \(h=pq\), \(\{1,1\}\) leaves closed provisionally

- For the remaining family
  \[
  h=pq,\qquad R=pq(Ap+Bq),\qquad AB\ne0,
  \]
  the lifted contact matrix has rank four, with kernel
  \((1,7/5,1,0,0)\).
- The kernel misses the Veronese cone by \(24/25\), so every
  \(r\)-dependent nonlinear coefficient vanishes.  The constant
  \(E_6\) block has determinant \(8A^2B^2\), giving the all-binary
  automorphism exit.
- Checked explicitly that \(A=0\) and \(B=0\) have gcd degree three.
- Froze `DELTA2_11_PQ_TWO_SIMPLE_EXCLUSION.md`, its hostile checklist,
  and its strict dual-CAS replay.  The leaf registry now has four
  provisional closures and eleven open leaves.

## 2026-07-25T13:24:34Z — fifth provisional \(\{1,1\}\) exclusion

- On
  \[
  h=p(p+q),\qquad R=p^2(Ap+Bq),
  \]
  recomputed the exact-open boundaries:
  \(B=0,A=B,3A=4B\) all have gcd degree three, while \(A=0\)
  remains exact \(\delta=2\).
- The lifted contact determinant is
  \(-6220800B^5(A-B)^2(3A-4B)\), and the constant \(E_6\)
  determinant is \(-1080B(A-B)^2(3A-4B)\).  Both are nonzero on the
  exact open, yielding the all-binary automorphism exit.
- Froze `DELTA2_11_PELL_DOUBLE_P_EXCLUSION.md`, its hostile checklist,
  and its strict dual-CAS replay.  Registry: five provisional closures,
  ten open leaves.

## 2026-07-25T13:33:17Z — sixth provisional \(\{1,1\}\) exclusion

- Treated independently the doubled-\((p+q)\) contribution
  \[
  h=p(p+q),\qquad R=(p+q)^2(Ap+Bq),
  \qquad B(5A+4B)\ne0.
  \]
  The two excluded coefficient boundaries have gcd degree three;
  the internal pivot \(A=B\) remains exact \(\delta=2\).
- A single contact minor has an apparent extra quartic factor, so it
  was replaced by the exact two-minor cover
  \[
  \begin{aligned}
  &-466560000B^3(A-B)^6(5A^2+26AB+23B^2),\\
  &-311040000B^3(A-B)^6(2A+7B)(5A+4B).
  \end{aligned}
  \]
  These cannot vanish simultaneously on the exact open.
- Recomputed \(A=B\) in a fresh tangent chart, obtaining contact
  determinant \(276480\).  The remaining constant \(E_6\) determinant
  is \(-648B^3(5A+4B)\), giving the all-binary automorphism exit.
- Froze `DELTA2_11_PELL_DOUBLE_L_EXCLUSION.md`, its hostile checklist,
  and its strict independent SymPy/PARI replay.  Registry: six
  provisional closures, nine open leaves.

## 2026-07-25T13:39:13Z — seventh provisional \(\{1,1\}\) exclusion

- On
  \[
  h=p(p+q),\qquad R=p(p+q)(Ap+Bq),\qquad
  B(A-B)(A+4B)\ne0,
  \]
  recomputed all three excluded boundaries from the signed row.  Their
  gcds are \(p^2(p+q),p(p+q)^2,pq(p+q)\), and their fresh \(E_7\)
  ranks are five, so every one routes to \(\delta=3\).
- Found a complete polynomial two-tangent basis and a rank-four lifted
  contact kernel.  In polynomial scale its Veronese obstruction is
  \(24B^2(A-B)^2\), nonzero throughout the exact open.
- The remaining constant \(E_6\) block has determinant
  \(8B^2(A-B)(A+4B)\), yielding the all-binary automorphism exit.
- Froze `DELTA2_11_PELL_TWO_FIXED_EXCLUSION.md`, its hostile checklist,
  and a strict independent SymPy/PARI replay.  Registry: seven
  provisional closures, eight open leaves.

## 2026-07-25T13:47:46Z — eighth provisional \(\{1,1\}\) exclusion

- Treated the fixed-\(p\) plus ramification-contact family
  \[
  h=p(p+q),\quad R=p(4Tp^2+3Tpq+Cq^2),\quad
  C(C+T)\ne0.
  \]
  Fresh boundary reruns give gcds \(p^2q\) at \(C=0\) and
  \(pq(p+q)\) at \(C=-T\), with \(E_7\) rank five in both cases.
- Factored the generic lifted contact determinant as
  \[
  27648C^5(C+T)^2(12C+7T)(16C-9T)^3.
  \]
  The apparent \(16C-9T\) pivot disappears in a fresh full-rank chart
  with determinant \(422400000\).
- On the genuine \(12C+7T=0\) rank-drop chart, the contact kernel has
  Veronese obstruction \(3053435/192\ne0\).  The constant \(E_6\)
  determinant is \(72C^2(C+T)^2\), giving the all-binary exit.
- Froze `DELTA2_11_PELL_P_CONTACT_EXCLUSION.md`, its hostile checklist,
  and its strict independent SymPy/PARI replay.  Registry: eight
  provisional closures, seven open leaves.

## 2026-07-25T13:54:16Z — all one-branch \(\{1,1\}\) leaves closed provisionally

- Independently treated the fixed-\((p+q)\) plus contact family
  \[
  h=p(p+q),\quad
  R=(p+q)(-4Bp^2+Bpq+Cq^2),\quad C(5B-C)\ne0.
  \]
  The boundary gcds are \(pq(p+q)\) at \(C=0\) and \(q(p+q)^2\)
  at \(C=5B\), with fresh \(E_7\) rank five.
- The generic lifted contact determinant factors as
  \[
  -746496C^3(B+16C)^3(5B-4C)(5B-C)^4.
  \]
  A fresh \(B=-16C\) chart has full determinant \(6967296\).
- The fresh \(5B=4C\) chart has rank four; its kernel misses the
  Veronese cone by \(99225/4\).  The constant \(E_6\) determinant is
  \(-648C^3(5B-C)\), giving the all-binary exit.
- Froze `DELTA2_11_PELL_L_CONTACT_EXCLUSION.md`, its hostile checklist,
  and a strict independent SymPy/PARI replay.  All five one-branch
  fixed-divisor leaves are now provisionally closed.  Registry:
  nine provisional closures, six open leaves.

## 2026-07-25T14:28:58Z — first squarefree-interior leaf closed provisionally

- Treated
  \[
  h=(p-wq)(wp-q),\qquad
  R=(p-wq)^2(Ap+Bq)
  \]
  on the complete no-additional-incidence open.  Recomputed the three
  deeper gcd boundaries as \(L^2M,qL^2,pL^2\).
- The six contact minors have different residual factors, so a
  multivariate gcd was rejected as insufficient.  On \(B\ne0\), four
  residual cubics in \(A/B\) have pairwise-resultant gcd
  \(w^3(w^2-1)^{12}\); the \(B=0\) endpoint has residual gcd \(w^2\).
  Both are disjoint from the squarefree interior open.
- Recomputed the internal \(Aw+B=0\) pivot as \(R=L^3\).  A fresh
  tangent basis gives contact determinant
  \[
  48977602560w^5(w-1)^6(w+1)^6
  \,(w^2-3)^4(3w^2-1),
  \]
  nonzero after the exact branch-contact exclusions.
- The constant \(E_6\) block is full rank, giving the all-binary exit.
  Froze `DELTA2_11_INTERIOR_DOUBLE_FIXED_EXCLUSION.md`, its hostile
  checklist, and a strict SymPy/PARI replay.  Registry: ten
  provisional closures, five open leaves.

## 2026-07-25T14:42:02Z — second squarefree-interior leaf closed provisionally

- On
  \[
  h=(p-wq)(wp-q),\qquad R=h(Ap+Bq),
  \]
  recomputed the four exact-open boundary gcds as
  \(LM^2,L^2M,qLM,pLM\).
- The lifted \(E_6\) contact map has rank four.  A cofactor construction
  gives its complete primitive kernel, whose Veronese obstruction
  simplifies exactly to
  \[
  24(A+Bw)^2(w-1)^2(w+1)^2(Aw+B)^2.
  \]
  This is nonzero on the two-fixed-root exact open.
- The constant \(E_6\) block is full rank, yielding the all-binary
  automorphism exit.
- Froze `DELTA2_11_INTERIOR_TWO_FIXED_EXCLUSION.md`, its hostile
  checklist, and a strict independent SymPy/PARI replay.  Registry:
  eleven provisional closures, four open leaves.

## 2026-07-25T15:01:31Z — genuine \(E_6\) survivor in the interior fixed/contact leaf

- Put the squarefree-interior one-fixed-root/one-ramification-contact
  family in the chart
  \[
  L=p-wq,\quad M=wp-q,\quad h=LM,
  \]
  \[
  R=L\{Ap^2+(1-3w^2)Tpq+4wTq^2\}.
  \]
  The exact open removes
  \[
  w(w^2-1)(w^2-3)
  \{A+T(w^3+w)\}
  \{-Aw+3Tw^2-5T\}
  \{Aw^2-3A+12Tw^3-4Tw\}=0.
  \]
- The generic contact determinant has internal pivots
  \[
  D=-16Aw+T(9w^4-6w^2+1),\qquad
  H=12Aw^3-4Aw+T(7w^6+9w^4-3w^2-5).
  \]
  Fresh \(D=0\) and \(H=0\) bases were recomputed rather than
  specializing a singular generic basis.
- In the \(H=0\) chart, with \(u=w^2\), the contact block has rank four
  and its Veronese obstruction has numerator
  \[
  V(u)=515u^4-548u^3+162u^2-324u+243.
  \]
  Thus \(V(u)=0\) is a genuine \(E_6\) survivor, not a discarded pivot
  artifact.  Both \(V(u)\) and \(V(w^2)\) are irreducible over
  \(\mathbb Q\), and
  \(\operatorname{disc}V=36520347436056576\ne0\).
- Exact resultants certify that this survivor is disjoint from every
  current open/pivot factor.  For
  \[
  u,\ u-1,\ u-3,\ u+1,\ 5u^2-6u+5,\ F_0,\ G_0,\ J,\ 11u-9,
  \ 5u-3,\ 3u-1,\ u^2+18u+1,\ 5u+1,
  \]
  where
  \[
  F_0=7u^3+45u^2-75u+15,\quad
  G_0=-7u^4+156u^3-66u^2+12u-15,\quad
  J=55u^3+9u^2-3u-21,
  \]
  the respective resultants with \(V\) are
  \[
  243,\ 48,\ 27648,\ 1792,\ 209715200,\
  155797791178752,\ 1017307740436955136,\
  18119393280000,\ 248832,\ 34560,\ 11264,\
  14815330304,\ 199680.
  \]
  The next check is the complete lower weighted-Jacobian system over
  \(\mathbb Q[u]/(V)\), adjoining \(w\) with \(w^2=u\) only where
  necessary.  No numerical conjugate selection is allowed.

## 2026-07-25T15:18:39Z — the quartic \(E_6\) survivor dies in \(E_5\)

- Worked exactly over
  \[
  \mathbb Q[w]/(V(w^2)).
  \]
  The kernel coordinate \(X\) is invertible there.  A
  denominator-cleared Veronese lift is
  \[
  c_1=(u+1)N_X,\qquad c_2=2wN_Y,
  \]
  where
  \[
  \begin{aligned}
  N_X={}&49u^5-987u^4-3126u^3+4650u^2+405u-1215,\\
  N_Y={}&343u^5-165u^4+1734u^3+150u^2-2925u+1215.
  \end{aligned}
  \]
  The resultant
  \[
  \operatorname{Res}(V,N_X)
  =46746446734136993390788608
  \]
  is nonzero, so this normalization loses no survivor.
- With the corresponding polynomial \(r^2\)-coefficients in \(H_2\),
  the top-only coefficient in the next weighted Jacobian identity
  factors as
  \[
  [r^2p^3]E_5=
  -96w^5(u+1)^2F_0^3J(-G_0)N_XC(u),
  \]
  where
  \[
  \begin{aligned}
  C(u)={}&47705u^8-413356u^7+546080u^6+294804u^5\\
        &-623574u^4+87132u^3-152280u^2+362556u-142155.
  \end{aligned}
  \]
  Every displayed factor except \(C\) was already certified invertible
  on this exact chart.  The last one is certified by
  \[
  \gcd(V,C)=1,\qquad
  \operatorname{Res}(V,C)
  =2^{81}3^{20}5^2\cdot1291\ne0.
  \]
  Thus the genuine \(E_6\) survivor is unconditionally incompatible
  with \(E_5=0\).
- `derive_delta2_11_interior_fixed_contact_survivor_lower.py`
  independently reconstructs \(E_7\), the \(E_6\) contact equation,
  and the nonzero \(E_5\) coefficient in the exact degree-eight
  field, without a numerical embedding.  The remaining work before
  banking this leaf is fresh-basis treatment of the internal chart
  artifacts \(u=-1,3/5,9/11\) and \(J(u)=0\).

## 2026-07-25T15:22:51Z — all four internal fixed/contact pivots closed

- Recomputed \(E_7\) bases over the four exact coefficient fields,
  rather than specializing either singular generic basis:
  \[
  \begin{array}{c|c|c|c}
  \text{chart}&\text{field relation}&\operatorname{rank}E_7&
  \text{\(E_6\) contact outcome}\\ \hline
  D=0,\ u=-1&w^2+1=0&6&\text{rank }5\\
  D=0,\ u=3/5&5w^2-3=0&6&\text{rank }5\\
  H=0,\ u=9/11&11w^2-9=0&6&
       \text{rank }4,\ \text{kernel non-Veronese}\\
  D=H=0,\ J(u)=0&J(w^2)=0&6&
       \text{rank }4,\ \text{kernel non-Veronese}.
  \end{array}
  \]
  All four defining field polynomials are irreducible over
  \(\mathbb Q\), so one exact field computation covers every
  conjugate and does not collapse a numerical branch.
- In every row the constant \(E_6\) block has rank five.  Hence after
  excluding the contact tangent, the remaining nonlinear
  \(r\)-coefficients vanish and the banked all-binary automorphism
  exit applies.
- The exact replay is
  `verify_delta2_11_interior_fixed_contact_pivots_sympy.py`.
  Together with the quartic \(E_5\) kill, this removes every internal
  pivot in the squarefree-interior one-fixed-root/one-contact leaf.

## 2026-07-25T15:46:01Z — twelfth \(\{1,1\}\) leaf banked provisionally

- Froze the complete proof in
  `DELTA2_11_INTERIOR_FIXED_CONTACT_EXCLUSION.md`, the adversarial
  tasks in `INTERIOR_FIXED_CONTACT_HOSTILE_REVIEW_CHECKLIST.md`, and
  the strict dual-CAS replay in
  `verify_delta2_11_interior_fixed_contact_strict.sh`.
- The SymPy replay reconstructs the generic and two internal contact
  charts, primitive quartic survivor, top-only \(E_5\) obstruction,
  mixed-determinant lower-jet independence, and all four exact pivot
  fields.  The independent PARI/GP replay recomputes the same objects,
  including primitive contents, irreducibility, and the exact
  \(V,C\) resultant.
- The strict whitelisted wrapper passes.  Registry: twelve
  provisional closures, three open \(\{1,1\}\) leaves.  The next
  squarefree-interior leaf is the two-ramification-contact family.

## 2026-07-25T15:57:09Z — opened the squarefree two-contact leaf

- Used the complete normal form
  \[
  \begin{aligned}
  h&=(p-wq)(wp-q),\\
  R&=4wAp^3-3(1+w^2)Ap^2q
     -3(1+w^2)Dpq^2+4wDq^3.
  \end{aligned}
  \]
  The branch swap \(p\leftrightarrow q\) fixes \(w\) and exchanges
  \(A,D\).  Overall scaling of \(R\) therefore permits \(D=1\),
  including the projective endpoint after the swap, while leaving the
  genuine cross-ratio modulus \(w\) and the coefficient modulus
  \(a=A/D\) modulo \(a\leftrightarrow a^{-1}\).
- The exact open removes \(w=0,w^2=1\), both fixed-root evaluations
  \[
  aw^3-3aw-3w^2+1,\qquad
  -3aw^2+a+w^3-3w,
  \]
  and the already closed \(\kappa=16\) factors
  \(w^2\pm4w+1\).
- Over \(\mathbb Q(w,a)\), the \(E_7\) kernel has dimension two and
  the lifted \(E_6\) contact map has generic rank five.  A
  projective-resultant cover of the six maximal minors reduces the
  common residual-\(Q\) case to
  \[
  (w^2+1)(5w^4-6w^2+5)=0
  \]
  off the exact open.  The other rank-drop branches are controlled
  by two linear factors \(K_1,K_2\); their resultants introduce the
  reciprocal octics
  \[
  \begin{aligned}
  7w^8-156w^6+66w^4-12w^2+15,\\
  15w^8-12w^6+66w^4-156w^2+7,
  \end{aligned}
  \]
  and the two reciprocal sextics obtained from
  \(\operatorname{Res}_a(K_1,K_2)\).
- The generic tangent basis uses an internal denominator
  \(B(w,a)\); \(B=0\) must receive a fresh basis.  No multivariate-gcd
  inference will be used.  The next step is exact field-by-field
  contact/Veronese analysis on this finite atlas, followed first by a
  top-only \(E_5\) test for every genuine \(E_6\) survivor.

## 2026-07-25T19:02:24Z — thirteenth \(\{1,1\}\) leaf banked provisionally

- Completed the generic contact-minor stratification.  With
  \(K_1=ab+c,K_2=ac+b\), the simultaneous branch consists of two
  primitive irreducible reciprocal sextics with \(a=\pm1\).  Fresh
  exact-field contact matrices have rank four and non-Veronese
  kernels.
- Treated every octic, quartic, and \(u=-1\) factor as an exact
  algebraic leaf.  The reciprocal octics are exactly \(E_L=0\) or
  \(E_M=0\).  The common-\(Q_i\) polynomial at \(u=-1\) is
  \(a^2+1\); at \(5u^2-6u+5=0\) it is
  \(10a^2+(-5w^3+11w)a+10\).  All four roots are fixed-root
  incidence boundaries.
- Built an alternate \(E_7\) basis on the internal divisor \(B=0\).
  Its contact-resultant projection leaves
  \[
  P_{16}=385w^{16}+9992w^{14}-23012w^{12}+53560w^{10}
  -24250w^8+53560w^6-23012w^4+9992w^2+385.
  \]
  This polynomial is primitive and irreducible.  Substitution of the
  exact reduced \(a(w)\) gives fresh contact rank five, so the
  projection factor is not a survivor.
- The singular alternate pivot \(u=-1\) forces \(a=0\).  Its contact
  matrix has rank three and its restricted Veronese equation is a
  nonzero square.  The unique lift is
  \[
  (N_1,N_2,N_3)=(2p^2+q^2,q^2,0),\qquad
  (x_5,y_5)=(-w,0).
  \]
  It survives top-only \(E_5\), so every lower coefficient was
  restored.
- The full lower solve has rank six at \(E_6\).  The \(E_5\)
  compatibility begins with \(12v_0^2=0\); after the resulting
  substitutions, \(E_4\) fixes the last two relevant entries and
  \(E_3,E_2,E_1\) vanish.  Nevertheless the forced linear part
  satisfies
  \[
  L_0[:,1]=u_2L_0[:,3],
  \]
  so \(\det L_0=0\), excluding the leaf at the Keller constant.
- Recorded the proof in
  `DELTA2_11_INTERIOR_TWO_CONTACTS_EXCLUSION.md`, adversarial tasks in
  `INTERIOR_TWO_CONTACTS_HOSTILE_REVIEW_CHECKLIST.md`, and independent
  exact replays in the SymPy and PARI programs under
  `verify_delta2_11_interior_two_contacts_*`.
- Registry: thirteen provisional closures, two open
  exact-\(\delta=2,\{1,1\}\) leaves, both on the doubled nonbranch
  fixed divisor \(h=(p+q)^2\).

## 2026-07-25T19:15:08Z — fourteenth \(\{1,1\}\) leaf banked provisionally

- On
  \[
  h=(p+q)^2,\qquad
  R=(p+q)(Ap^2+Bpq+Cq^2),
  \]
  recomputed the exact-open boundary gcds
  \(2q(p+q)^2,2p(p+q)^2,2(p+q)^3\) on
  \(A=2B,C=2B,A-B+C=0\), respectively.
- Put \(\Delta=4AC-B^2\).  On \(\Delta\ne0\), a complete polynomial
  \(E_7\) tangent basis gives rank-six minor
  \[
  -768(A-2B)(2B-C)\Delta(A-B+C)^2
  \]
  and lifted contact determinant
  \[
  26542080(A-2B)(2B-C)\Delta^3(A-B+C)^3.
  \]
  Hence there is no nonzero contact lift on the exact open.
- Recomputed \(\Delta=0\) from a fresh basis rather than specializing
  the singular generic chart.  Exactness first forces \(C\ne0\), and
  with \(A=B^2/(4C)\) the fresh contact determinant is
  \[
  -3840B(B-8C)(B-2C)^6(2B-C)^4/C.
  \]
  Each factor is an exact-open evaluation, so this chart also has full
  contact rank.
- The uniform constant \(E_6\) determinant is
  \[
  -512(A-2B)(2B-C)(A-B+C)^2.
  \]
  It forces every nonlinear \(r\)-coefficient to vanish, and the
  established all-binary field/descent exit makes the map an
  automorphism.  There is no lower-coefficient survivor to solve.
- Froze the proof in
  `DELTA2_11_DOUBLED_NONBRANCH_SIMPLE_FIXED_EXCLUSION.md`, the audit
  tasks in
  `DOUBLED_NONBRANCH_SIMPLE_FIXED_HOSTILE_REVIEW_CHECKLIST.md`, and
  the passing dual-CAS replay in
  `verify_delta2_11_doubled_simple_fixed_strict.sh`.
- Registry: fourteen provisional closures and one open
  exact-\(\delta=2,\{1,1\}\) leaf.

## 2026-07-26T07:25:07Z — exact-\(\delta=4\) umbrella promoted

- The canonical high-incidence denominator has six and only six
  exact-\(\delta=4\) families.
- All six now have complete arbitrary-lower-term exclusions with
  independent exact implementations and fail-closed mutations.
- A hostile assembly audit checked disjointness, completeness, aliases,
  every proof path and terminal marker, and all contact boundaries.
- Certified fine status: \(6/26\).  The other 20 high-incidence families
  and the lower-incidence row bridge remain open, so no global row or
  degree-bound count changes.
