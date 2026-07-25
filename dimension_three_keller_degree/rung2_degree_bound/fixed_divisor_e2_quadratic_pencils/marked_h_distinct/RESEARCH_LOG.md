# Research log

## 2026-07-25T23:19:15Z — clean-room match and symbolic \(\tau\) survival

- Read the completed clean-room report only after its derivation was
  checkpointed.  It independently recovered the exact companion quotient
  \(3+\mathbb P^1+3\), with stable internal IDs.
- Mapped all six endpoint calculations to those IDs and recorded the four
  omitted orbit/moduli entries in `FREEZE_READINESS_COMPARISON.md`.
- Adopted the homogeneous middle-family parameter
  \[
  [u:v],\qquad r=uh+vs,
  \]
  with affine \(\tau=v/u\), and retained the intrinsic boundaries
  \(\tau=0,-1,\infty\).
- Computed the middle family symbolically.  At finite \(\tau\ne0\), the
  raw \(E_7\) matrix has rank \(18\), and a complete legal normal form is
  \(U=Ax^3,V=Bx^3,W=Tx^2\).  The \(E_6\) lower matrix has rank \(10\)
  and identically zero compatibility right side.
- Two exact pivot charts cover every \(\tau\ne0\); their extra factors
  are \(9\tau^2+6\tau-1\) and \(3\tau-1\), which are coprime.  Their only
  common rank-drop divisor is \(\tau=0\), already a separate endpoint.
- Conclusion: every \(\tau\in\mathbb P^1\) survives through \(E_6\).
  The intrinsic \(\tau\)-modulus is not removed by either identity.
- Added independent exact SymPy and PARI/GP certificates for the symbolic
  family.  No \(E_5\) work was resumed.

## 2026-07-25T23:08:29Z — F3 companion-taxonomy failure

- Audited the assumption that the two endpoint cubics \(xh\) and \(xs\)
  exhaust the nonzero top kernel.
- Found the exact omitted point
  \[
  h=yz,\quad s=x^2,\quad G=x(s+h),
  \]
  whose top Jacobian is zero.  The quotient \(G/x=s+h\) has quadratic
  rank three, while \(h\) and \(s\) have ranks two and one, so it cannot
  be equivalent to either computed endpoint.
- Found the parallel rank-two witness on the smooth marked member:
  \(h=x^2+yz,\ G=xyz\).  Its quotient has rank two, distinct from the
  ranks of \(h\) and \(s\).
- Identified the faulty step: choosing a new pencil basis
  \(q'=G/x\) changes the second leading coordinate but does not change
  the third cubic.  Shearing the leading pair back restores the mixed
  coefficient.
- Recast the six \(E_7/E_6\) computations as valid endpoint slices, not
  a taxonomy, and halted \(E_5\) work under the freeze-violation
  protocol.
- Formulated the invariant companion space
  \(\Gamma_{V,[h]}\backslash\mathbb P(V)\) and a candidate quotient
  stratification in `COMPANION_MODULI_GAP.md`.  It requires independent
  reconstruction before freezing.
- Added exact independent SymPy and PARI checks of the discriminants,
  source actions, full top lines, and counterexamples.

## 2026-07-25T23:00:24Z — six missing branches reconstructed

- Began from the three marked-member orbits omitted when the earlier
  lower packages silently identified the fixed gcd \(h\) with the unique
  double member \(s=x^2\).
- Computed the two endpoint cubic companions \(R=xh\) and \(R=xs=x^3\)
  in each marked orbit.  The initially proposed six-branch denominator
  was later found incomplete; see the newer entry above.
- Reconstructed the raw \(E_7\) equation in all six branches.
  Companion-\(H\) branches have rank \(14\), nullity \(12\), and a
  seven-parameter normal complement after five legal gauges.
  Companion-\(S\) branches have rank \(16\), nullity \(10\), and a
  five-parameter complement.
- Retained twelve arbitrary coefficients in the first two components of
  \(H_2\) and all nine coefficients of \(L\).  The resulting \(E_6\)
  matrices have constant rank \(8\) in companion-\(H\) branches and
  constant rank \(10\) in companion-\(S\) branches.
- Derived the four exact compatibility ideals recorded in `NOTE.md`.
  Every maximal pivot is a nonzero rational constant, so no
  specialization divisor or hidden rank-drop chart occurs through
  \(E_6\).
- Found a uniform sharp witness for every branch:
  \(H_2=0\), \(U=V=W=0\), the fixed nonzero \(R\), and
  \(L=((0,1,0),(0,0,1),(1,0,0))\).  It has determinant one and satisfies
  \(E_9,E_8,E_7,E_6\), but its displayed \(E_5\) polynomial is nonzero.
- Slice verdict: zero of six computed endpoints are excluded through
  \(E_6\).  The later taxonomy failure blocks promotion to \(E_5\).
- Implemented independent exact SymPy and PARI/GP reconstructions.  The
  strict aggregate passes.

No frozen status ledger, parent row note, program README, root research
log, commit, or remote state was changed.  No row closure is claimed.
