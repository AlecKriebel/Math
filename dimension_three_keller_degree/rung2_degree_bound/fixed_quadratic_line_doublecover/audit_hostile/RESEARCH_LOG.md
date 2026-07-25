# Hostile audit log: nonbinary fixed-quadratic line double cover

**Scope:** Reconstruct and attack the provisional theorem without modifying
its note or supplied verifiers.

**2026-07-25T05:24Z — Audit opened**

- Confirmed the worktree remains on `main`.
- Baseline SHA-256 hashes:
  - theorem:
    `b6c9defea68ee2ee145b3e2f2c6251428fd1149385bd9fcf0557d4f01f64ca60`;
  - SymPy verifier:
    `8c3a3e8c83d2daeb98b57f6c5805371383e574ff77a9cf4615d8cdf27de7ec9a`;
  - PARI/GP verifier:
    `15d1646420d1631f88c23f666768d8aca5268fecb657f9ec142eff7156eefba9`;
  - strict wrapper:
    `1444668003525b0c0fdd879354f84e3669fa3e9934e1f6d3efc2037bfd6f34ee`.
- Both supplied verifier commands pass.
- Initial independent reconstruction confirms the adjugate and logarithmic
  derivation formulas.  No scope failure has yet been found.

**Checkpoint estimate:** 25% complete.

**2026-07-25T05:39Z — Exact branch reconstruction**

- Over \(K=\mathbb C(t)\), the residue equation for a homogeneous component
  of degree \(d\) is \(4v_\phi(g)=dm\).  For \(d=3\) no multiplicity
  \(m=1,2\) works.  For \(d=2\), a nonzero solution forces
  \(H=c(s+ut+v)^2\); the constant \(s^2\)-coefficient and degree-two
  homogeneity then give
  \(h=c(r+uq+vp)^2\) in \(\mathbb C[p,q,r]\).  Thus no merely rational
  square is lost during rehomogenization.
- The full stabilizer of \(r^2(p^2,q^2,0)\) must preserve both the fixed line
  \(r=0\) and the reduced-pencil base point \([0:0:1]\).  Its pencil action
  therefore preserves or exchanges the two ramification lines, so it is
  diagonal or anti-diagonal.  This proves that nonzero
  \(r(\alpha p+\beta q)\) has exactly the support-one and support-two
  orbits represented by \(pr\) and \((p+q)r\).
- An audit-only PARI/GP reconstruction independently obtains constant
  coefficient matrices:
  - \(pr\) raw \(E_6\): rank \(10\), nullity \(13\);
  - \((p+q)r\) raw \(E_6\): rank \(14\), nullity \(9\);
  - \(pr\) raw \(E_5\): rank \(4\), nullity \(14\);
  - \((p+q)r\) post-square \(E_5\): rank \(6\), nullity \(12\).
- The displayed solution families have the full corresponding dimensions,
  so all four converses hold at every specialization.
- In the \(pr\) branch, the \(K\ne0\) degree-three and degree-two matrices
  have ranks \(4\) and \(3\), respectively, and are exactly \(K\) times
  constant full-rank matrices.  Hence \(K=0\) versus \(K\ne0\) is the only
  rank split.
- In the sum branch, the recurrence matrix has minors
  \(D^2,D(\alpha+E),D\beta,(\alpha+E)^2-D\beta,
  (\alpha+E)\beta,\beta^2\).  Its sole rank-drop point is
  \(D=\alpha+E=\beta=0\).  Exact polynomial division confirms
  \(M\mid\det L_0\) and \(M_*\mid\det L_0\), while
  \(a[pr]E_2-[p]E_1=M_*^2\) is an identity.

**Checkpoint estimate:** 85% complete.

**2026-07-25T05:47Z — Audit complete**

- The plane-field exit was checked through algebraic base change and generic
  degree, rather than by inheriting the unresolved plane Jacobian
  conjecture.
- The supplied SymPy verifier fails closed under `PYTHONOPTIMIZE=1`.
- Fault injection against the supplied GP wrapper confirmed that it rejects
  a diagnostic, trailing output, and nonzero exit.
- The independent audit GP verifier reaches the unique marker
  `AUDIT_FIXED_QUADRATIC_LINE_PARI_PASS_41D8C2`.
- No omitted zero specialization, rank drop, or counterexample was found.
- Final verdict: **PASS**, with exposition-strengthening corrections
  recorded in `REPORT.md`.

**Checkpoint estimate:** 100% complete.
