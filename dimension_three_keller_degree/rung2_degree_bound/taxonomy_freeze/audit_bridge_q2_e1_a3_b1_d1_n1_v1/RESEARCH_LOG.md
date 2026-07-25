# Independent hostile bridge audit log

## 2026-07-25T22:27:27Z — sealed pre-comparison routing enumeration

At this checkpoint I had **not** read
`../BRIDGE_Q2_E1_A3_B1_D1_N1_v1.md`,
`../verify_bridge_q2_e1_a3_b1_d1_n1_v1.py`, or any pre-existing checker
for that bridge.  I reconstructed the following routing solely from
`../FROZEN_TAXONOMY_v1.md`, `../frozen_manifest_v1.json`, and theorem/audit
artifacts below `../../fixed_linear_cubic_pencil/`.

### Frozen input and normalization that must be justified

The row is
\[
R=\texttt{Q2-E1-A3-B1-D1-N1},
\qquad(\operatorname{rank},e,a,b,\delta,\nu)
=(2,1,3,1,1,1).
\]
Thus every point of \(R\), after invertible source and target changes, has
\[
H_4=(hp,hq,0)^T,
\]
where \(h\) is linear and \(p,q\) are coprime, nonproportional homogeneous
cubics forming the canonical minimal pair.  In particular
\(\mathbb C(p/q)\) is relatively algebraically closed in
\(\mathbb C(\mathbb P^2)\).  Any bridge must explain why this normalization
is available for every point of the frozen row, preserves the Keller and
automorphism questions, and does not add a coefficient-pivot hypothesis.

### Exhaustive theorem route

1. **Horizontal/vertical split.**

   - If no nonzero pencil member is divisible by \(h\), the horizontal
     theorem applies.  It forces the cubic and quadratic normal components
     \(G_3=(H_3)_3\) and \(G_2=(H_2)_3\) to vanish, and then uses the
     plane-fibre exit.  The aggregate hostile audit gives PASS, conditional
     on the frozen rank-two factorization and the established plane
     degree-at-most-four theorem.
   - Otherwise the vertical member is unique by \(\gcd(p,q)=1\).  A pencil
     change makes it
     \[
     p=h^m r,\qquad m\in\{1,2,3\},\qquad h\nmid rq.
     \]

2. **Vertical multiplicity.**

   - \(m=1\) or \(m=2\): the audited vertical-multiplicity theorem forces
     \(G_3=0\).  The full third component then has degree at most two and
     must be sent to the separately banked quadratic-component exit.
   - \(m=3\): normalize \(h=z,p=z^3\).  The audited cubic-kernel theorem
     gives
     \[
     G_3\in\langle z^3,q\rangle.
     \]
     If \(G_3=0\), again use the quadratic-component exit.  If \(G_3\ne0\),
     residual pencil and target changes give exactly the two disjoint
     companions \(G_3=q\) and \(G_3=z^3\).

3. **Nonvertical companion \(G_3=q\).**

   Put \(q_0=q|_{z=0}\ne0\).  Its only binary-root partitions are
   \(1+1+1,2+1,3\).

   - Partitions \(1+1+1\) and \(2+1\) are excluded by
     `NONVERTICAL_NONTRIPLE_LEMMA.md`.
   - For partition \(3\), the complete minimal atlas has exactly
     \[
     x^3+y^2z+\alpha xz^2,\qquad x^3+xyz,\qquad x^3+yz^2.
     \]
     These are excluded by `NONVERTICAL_TRIPLE_ROOT_LEMMA.md`.
     The omitted binary-in-\((x,z)\) shape is precisely the nonminimal
     boundary, hence not a point of \(R\).

   The aggregate independent report
   `audit_nonvertical_companion/REPORT.md` gives PASS for this entire
   companion.

4. **Vertical companion \(G_3=z^3\).**

   The complete legal \(E_7\) gauge is
   \[
   H_3=\left(\frac43zW+s q,\ V,\ z^3\right)^T
   \]
   after removal of the independent \(z^3\) terms.  The invariant first
   split is \(s\ne0\) versus \(s=0\).

   - **\(s\ne0\), \(q_0\) nontriple.**  The binary \(E_6\) restriction
     forces \(W_0=0\), so \(W=z\ell+wz^2\).
       - \(\ell=0\): excluded by
         `VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md`, hostile-audit PASS.
       - \(\ell\ne0\): squarefree positions, double-root noncollision,
         and both double-root root-line collisions are all excluded by
         `VERTICAL_NONZERO_ELL_NONTRIPLE_LEMMA.md`, hostile-audit PASS.

   - **\(s\ne0\), \(q_0=x^3\) triple-root.**  The binary restriction gives
     \(W_0=\gamma x^2\).
       - \(\gamma\ne0\): all three minimal triple-root charts are excluded
         by `VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md`, hostile-audit
         PASS.
       - \(\gamma=0\): write \(W=z(\ell+wz)\).  The audited
         `VERTICAL_TRIPLE_GAMMA0_REDUCTION.md` forces \(\ell=0\), and the
         audited terminal theorem
         `VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md` excludes all three minimal
         charts.

   - **\(s=0\), \(W_0=0\).**  All two nontriple and three minimal
     triple-root charts are excluded by
     `VERTICAL_A0_W0_ZERO_EXCLUSION.md`, hostile-audit PASS.

   - **\(s=0\), \(W_0\ne0\).**  The theorem in
     `a0_w0_nonzero_attack/NOTE.md` forces
     \[
     q\in\operatorname{Sym}^3\langle z,L\rangle,
     \]
     exactly the nonminimal boundary.  The independent report
     `audit_a0_w0_nonzero/REPORT.md`, completed at
     2026-07-25T22:25:43Z, gives PASS with sentinel
     `A0_W0_NONZERO_INDEPENDENT_STRICT_PASS_94A60D`.

5. **Reclassification boundaries.**

   A cubic pair that becomes binary in a two-dimensional linear space is
   not in this canonical \(a=3,b=1\) row.  The frozen routing rule requires
   recomputing the canonical tuple; such a boundary goes to one of the
   \(e=1,a=1,b=3\) rows according to the recomputed \((\delta,\nu)\).
   It is not legitimate to call the boundary contradicted or to append a
   new leaf.

This tree is exhaustive: horizontal versus vertical; vertical
\(m=1,2,3\); for \(m=3\), \(G_3=0,q,z^3\); for the vertical companion,
\(s\ne0\) versus \(s=0\); and within those branches the complete binary
root, \(\ell\), \(\gamma\), and \(W_0\) partitions above.

### The 45 frozen coefficient pivots

The theorem route is global on \(R\), so it must be applied separately to
every frozen intersection
\[
R/\mathrm C_i=R\cap\{c_0=\cdots=c_{i-1}=0,\ c_i\ne0\}.
\]
The exact manifest IDs are:

```text
C00 C01 C02 C03 C04 C05 C06 C07 C08 C09
C10 C11 C12 C13 C14 C15 C16 C17 C18 C19
C20 C21 C22 C23 C24 C25 C26 C27 C28 C29
C30 C31 C32 C33 C34 C35 C36 C37 C38 C39
C40 C41 C42 C43 C44
```

Empty intersections are allowed.  For a nonempty intersection, the first
nonzero coefficient only certifies \(H_4\ne0\); it is not a denominator in
any theorem above.  Therefore the required coverage map is the constant
map from each of these 45 pivot IDs to the same global route root.  Any
checker that tests only the count 45, a range abbreviation, or a proper
subset is insufficient; it must compare the exact ID set and verify that
each ID has a route assignment.

### Assumptions and gaps identified before comparison

1. **Quadratic-component-exit provenance caveat.**  The allowed
   fixed-linear corpus repeatedly calls this exit “banked,” but contains no
   theorem statement or hostile-audit report proving it.  The \(m=1\),
   \(m=2\), and \(m=3,G_3=0\) terminals are therefore not independently
   closed by the fixed-linear artifacts alone.  A PASS bridge must cite and
   pin a separately audited theorem establishing that a dimension-three
   Keller map of total degree at most four with one component of degree at
   most two is invertible.  Merely asserting “banked” is a provenance gap.

2. **Conditional horizontal exit.**  The horizontal hostile report is
   explicitly conditional on the frozen rank-two factorization/taxonomy
   and the established unconditional plane low-degree bound.  The bridge
   must not present the report as assumption-free.

3. **Stale status headers.**  Several theorem front pages lag their audit
   artifacts: `WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md` still says
   provisional/not yet hostile-audited; the two nonvertical lemma headers
   still say not yet hostile-audited despite the aggregate PASS; the
   \(E_8\)-\(E_4\) ledger still leaves \(s=0,W_0\ne0\) pending; and
   `a0_w0_nonzero_attack/NOTE.md` still says awaiting hostile audit despite
   the later PASS report.  A bridge must resolve status from the dated
   reports, not silently quote the stale headers.

4. **Audit scope versus identity checking.**  The exact checkers certify
   encoded coefficient identities.  The universal conclusions also use
   the stated atlas, minimality, legal-gauge, and divisor arguments.  A
   bridge checker cannot turn textual marker matching into a new proof of
   those inputs.

5. **Normalization and pivot scope.**  No route may divide by the frozen
   leading coefficient \(c_i\), a pencil discriminant, a root modulus, or
   a lower-jet parameter without a complementary zero branch.  Existence
   of invertible normalizations must be distinguished from a regular
   coefficient chart.  The global theorem route is the only evident
   division-free coverage of all 45 frozen pivots.

This sealed enumeration is the baseline for the subsequent candidate
comparison.

## 2026-07-25T22:43:13Z — candidate comparison and hostile attacks

- Opened the candidate bridge and checker only after the sealed checkpoint.
  The candidate's normalization from the frozen tuple is correct:
  basepoint freeness of the binary linear triple gives three target-minor
  charts, and none uses a frozen coefficient pivot.
- Independently reproduced all thirty leading-tuple witnesses for
  `C00`--`C29`.  Each has linear component gcd, a primitive minimal cubic
  pair, and rank-two leading Jacobian.  These are leading-shape witnesses,
  not Keller completions; the bridge correctly routes the corresponding
  frozen strata only **if nonempty**.
- Independently reproduced the division-free emptiness proof for
  `C30`--`C44`: both first target components vanish, so the leading
  Jacobian has at most one nonzero row, contrary to frozen rank two.
- Expanded the intrinsic route into 48 disjoint audit atoms: one horizontal
  atom plus 47 vertical multiplicity/companion/root/collision/lower-rank
  atoms.  They map uniquely onto the candidate's fifteen terminal groups.
- The later hostile report for \(s=0,W_0\ne0\) passes with no scope change.
  The candidate bridge and checker were written earlier and still recorded
  that terminal as conditional.  This is a stale status defect, not a
  missing mathematical route.
- Confirmed a fail-closed weakness in the supplied checker: it pins theorem
  inputs, but not the bridge itself, and checks only ten bridge marker
  strings.  A file containing only those ten strings still produces its PASS
  sentinel.  The new independent checker pins the exact bridge and rejects
  this mutation, as well as missing/overlapping pivots, missing/overlapping
  route atoms, an unaudited terminal, and optimized execution.
- A standalone hostile audit of the quadratic-component exit has now issued
  PASS.  It independently checked the Hessian-coordinate argument, the exact
  degree-eight plane-fibre bound, Vistoli's published degree-at-most-twelve
  plane theorem, and the final étale/injective implication.  This repairs
  the provenance caveat identified before comparison.
- Final hashes are deliberately not yet recorded: the parent task is
  repairing the stale theorem/bridge headers and candidate checker after the
  quadratic audit files stabilize.  The final replay will pin only that
  repaired state.
