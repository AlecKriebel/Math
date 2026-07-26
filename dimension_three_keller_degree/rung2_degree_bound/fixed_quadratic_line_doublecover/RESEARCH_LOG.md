# Research log: fixed-quadratic line double cover

## 2026-07-25T04:43Z — logarithmic reduction opened

- Selected the uncovered taxonomy row
  \((e,a,b,\delta,\nu)=(2,1,2,1,2)\).
- Normalized the outer degree-two cover to
  \((p^2,q^2)\).
- Found
  \[
  \operatorname{adj}J\!\left(h(p^2,q^2,0)^T\right)
  =-2hpq\,k e_3^T,\qquad
  k=(ph_r,qh_r,rh_r-4h)^T.
  \]
- The resulting factor residues kill the third cubic component for every
  nonbinary \(h\), and kill the third quadratic component except when
  \(h\) is a square.

## 2026-07-25T04:59:28Z — both square-factor orbits closed

- The exceptional square normalizes to \(h=r^2\), whose quadratic
  invariant space is \(r\langle p,q\rangle\).
- Diagonal source changes and the swap reduce nonzero invariants to \(pr\)
  and \((p+q)r\).
- In the \(pr\) orbit, \(K=2bc-e=0\) immediately makes two rows of \(L_0\)
  proportional.  For \(K\ne0\), degrees four through two give a complete
  parameterization whose linear determinant vanishes identically.
- In the \((p+q)r\) orbit, four degree-four coefficients form a
  specialization-safe two-variable recurrence.  Its sole resonance is
  killed by the degree-three squares \(-2X^2\) and \(-2Y^2\).  Outside that
  resonance, degree three has one common factor dividing \(\det L_0\); at
  the resonance, one degree-two coefficient and one degree-one coefficient
  differ by the square of the remaining factor.
- Independent SymPy and PARI/GP regressions pass.  The GP check is
  fail-closed behind a diagnostic-rejecting wrapper.
- The theorem remains provisional pending an adversarial scope audit and a
  current source-specific priority sweep.  The binary fixed quadratic
  remains open.

## 2026-07-25T05:38:33Z — hostile audit passed and theorem promoted

- An independent reconstruction proved that the square over
  \(\mathbb C(t)[s]\) rehomogenizes globally as
  \(h=c(r+uq+vp)^2\).
- The full stabilizer preserves the doubled fixed line, reduced-pencil base
  point, and the two ramification lines.  Its nonzero quadratic-normal
  orbits are exactly \(pr\) and \((p+q)r\).
- The audit obtained constant raw ranks \(10,14\) in degree six and \(4,6\)
  in degree five, with the full displayed nullities and converses.
- It independently verified the \(K=0/K\ne0\) split, the rank-\(4\) and
  rank-\(3\) lower solves, the literal divisibilities by \(M,M_*\), and the
  division-free identity
  \(a[pr]E_2-[p]E_1=M_*^2\).
- Optimized-Python and GP-diagnostic fault injection both fail closed.
- Verdict: PASS.  The nonbinary subrow is promoted; the binary locus
  remains open.

## 2026-07-26T01:31:00Z — canonical \(\delta\ge3\) denominator frozen

- A primary saturation-safe enumeration and a clean-room reconstruction
  independently classified the formerly untouched high-gcd binary locus.
- The primary package froze before reconciliation at
  \(17\) exact-\(\delta=3\) families, \(6\) exact-\(\delta=4\)
  families, and one dependent power fibre.
- The blinded audit obtained \(19+6+1=26\).  Reconciliation showed that
  the count difference is exactly two branch-square torus endpoint splits,
  but also found two substantive primary guard errors:
  `D3-DN-L3` overlapped two \(\delta=4\) contact points, and the
  oriented `D3-SF-2C` family incorrectly identified the reciprocal
  \(z\)-sheets and omitted the exact-\(\delta=3\) point \(z=-1/5\).
- The blinded \(19+6+1\) ledger is canonical.  Its exact local-valuation
  proof and dependency-free replay are reconciled with the primary
  SymPy/PARI saturation calculation.
- Twelve retained pivots and twenty-four exit arrows now have separate
  stable F1 identifiers.  They certify boundary coverage without changing
  the main count twenty-six.
- The complete reconciliation replay ends with
  `DELTA_GE3_RECONCILIATION_STRICT_PASS_26`.
- This freezes the incidence search space only.  The parent quartic row
  remains open, the global count remains \(4/14\) certified, and the
  universal total-degree floor remains four.

## 2026-07-26T02:11:00Z — `D4-SF-11CC` candidate closed

- The first canonical family tested after the high-incidence freeze is the
  isolated squarefree point \(\kappa=16\), with rational representative
  \(h=p^2-4pq+q^2,\ R=h(p+q)\).
- The full \(E_6\) contact locus is a two-parameter plane even after
  arbitrary binary lower summands are restored.
- The lower solve has three necessary charts: generic,
  \(m^2-4mn+n^2=0\) nonzero, and zero contact.  These fail at
  \(E_5,E_5,E_4\), respectively; the zero chart becomes binary and exits
  by the unconditional plane low-degree theorem.
- Independent SymPy and PARI/GP replays pass with terminal marker
  `D4_SF_11CC_FULL_STRICT_PASS`.
- Hostile mathematical audit is pending, so the family is provisional and
  no parent-row or global count is changed.

## 2026-07-26T03:34:51Z — `D4-SF-21C` candidate closed

- The second isolated exact-\(\delta=4\) family tested is
  `D4-SF-21C`, with
  \(s^2=-5,\ h=(p-sq)(sp-q),\ R=(p-sq)^2(sp-q)\) and
  \(\kappa=-16/5\).
- Four explicit compatibility equations force the complete \(E_6\)
  contact plane with arbitrary binary lower summands retained.
- The lower matrix has generic rank seven, rank six at the two directions
  \((m,n)\sim(1,3),(-1,6)\), and rank five at the origin.  The generic
  chart is killed by two \(E_5\) cubics with pure-power resultants, the two
  boundary charts by the same nonzero \(E_5\) constant, and the origin by
  two successive \(E_4\) squares before the unconditional plane exit.
- Independent SymPy and direct PARI/GP reconstructions pass with terminal
  marker `D4_SF_21C_FULL_STRICT_PASS`, including a fail-closed mutation.
- This is the second of 26 canonical main families with a provisional full
  exclusion.  Hostile audit is pending; the parent row and the global
  \(4/14\) count remain unchanged.

## 2026-07-26T04:36:36Z — hostile promotions and full `D4-DN-3` contact atlas

- Clean-room hostile audits promote `D4-SF-11CC` and `D4-SF-21C` from
  candidate to certified family-level exclusions.
- `D4-DN-1CC` also has a complete dual-CAS descent and an independent
  hostile replay.  The exact nonzero-contact obstruction is
  \(16\kappa^4/135\); the origin exits through a binary plane block.
- The first `D4-DN-3` computation was only a zero-binary slice and is
  retained as a bounded negative audit.  The corrected full-lower
  elimination retains all 18 lower variables and gives precisely two
  conjugate affine contact planes with four specialization-safe rank
  charts.
- Therefore \(3/26\) frozen high-incidence main families are certified
  excluded.  The containing global row is still open, so no global
  \(4/14\) status or degree-floor number changes.
