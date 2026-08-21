# Research log: binary fixed-linear line triple cover

All timestamps are UTC.

## 2026-07-25T11:36:00Z — abstract binary-quartic lemma transferred

- Applied the independently audited binary-quartic Hilbert--Burch/\(E_6\)
  lemma without specializing the degree-three cover \(A/B\).
- Excluded \(R=0\) by the quadratic-component exit.
- Excluded the entire \(\delta=0\) stratum by the injective \(E_7,E_6\)
  blocks and plane-plus-shear exit.
- Reduced every possible counterexample to
  \(\delta\in\{1,2,3,4\}\) or the power fibre.
- In this row, unique factorization turns the power fibre into the explicit
  requirement that the cubic pencil \(\langle A,B\rangle\) contain \(p^3\)
  and \(R=p^3\).
- No claim is made yet on the remaining strata.

## 2026-07-25T12:36:00Z — scope wording corrected before promotion

- Corrected the theorem headline from the unsupported statement “no Keller
  map has \(\delta=0\)” to the proved statement “every Keller map on the
  stratum is an automorphism,” equivalently no Keller **counterexample**
  lies there.
- Downgraded “first exact release” to a candidate checkpoint.  The abstract
  Hilbert--Burch input is audited, but this fixed-linear row transfer still
  requires its own hostile scope and automorphism-exit replay.

## 2026-07-25T13:16:35Z — two binary frontiers provisionally closed

- The constant-dependent power fibre now has complete SymPy and independent
  PARI/GP lower-identity replays.  Its nonzero \(r^3\) and \(r^2\) branches
  force a singular linear part; the zero branch exits through plane degrees
  \(6\) and \(10\).
- The marked half of exact \(\delta=1\) is also provisionally closed.
  Its divided-gradient contact either creates a second linear gcd divisor
  or lands in one of two explicit families with gcd degrees four and three.
  Hence only zero contact remains, giving the all-binary automorphism exit.
- Both results have candidate notes, strict dual-CAS suites, hostile
  checklists, and candidate-specific priority sweeps.  Neither is promoted
  before independent hostile audit.

## 2026-07-25T13:50:07Z — first unmarked \(\delta=1\) contact leaf closed

- In the generic unmarked chart, the \(a_3=1/2\) contact component is an
  exact one-parameter family.  Its exact open is \(z(64z-1)\ne0\).
- Solving the full lower identities without suppressing free
  coefficients gives
  \(L(1,-4,2u_1)^T=0\), so no Keller linear part occurs.
- A premature exploratory specialization was removed before banking:
  the corrected proof retains all free \(E_5\) parameters and is checked
  by separate SymPy and PARI/GP reconstructions.
- The cubic-root contact component and the boundary charts remain open;
  no claim is made for the full unmarked stratum.

## 2026-07-25T13:58:58Z — cubic unmarked contact component leaves the stratum

- The remaining cubic factor on the generic chart was solved exactly
  over its degree-three coefficient field.
- All three Hilbert--Burch minors share the chart divisor times a monic
  quadratic.  Its gcd degree is therefore at least three, so this contact
  component is disjoint from exact \(\delta=1\).
- The boundary charts and saturation of the full generic contact
  decomposition remain open.

## 2026-07-25T14:04:18Z — first unmarked boundary chart closed

- The \(a_2c_0\ne0,b_1=0\) contact equations force an additional common
  line in all three minors.  Hence no contact point remains in exact
  \(\delta=1\), and the zero-tangent plane exit applies.
- The \(a_2=0\) and \(c_0=0\) boundary charts remain.

## 2026-07-25T14:12:07Z — \(c_0=0\) boundary closed by a linear kernel

- Its unique exact contact orbit survives the gcd test, but the complete
  lower identities force the nonzero vector \((9,-36,16w)^T\) into the
  kernel of the linear part.
- Only the \(a_2=0\) unmarked boundary remains in exact \(\delta=1\),
  subject to hostile audits of the provisionally closed charts.

## 2026-07-25T14:21:02Z — unmarked exact-\(\delta=1\) primary classification closed

- The final \(a_2=0\) boundary is excluded by a repeated-divisor identity:
  its first contact coefficient forces \(q^2\) into the three minors.
- Together with the generic contact components and the \(b_1=0,c_0=0\)
  boundaries, this closes the primary unmarked exact-\(\delta=1\)
  calculation.  A single synthesis and hostile saturation audit are still
  required before promoting the whole stratum.

## 2026-07-25T14:36:33Z — complete exact-\(\delta=1\) synthesis

- Combined the constant-dependent power fibre, marked divisor,
  unmarked generic chart, every zero-pattern boundary, and the
  zero-tangent exit into one candidate theorem.
- The synthesis audit found a previously unstated
  \(c_0=0,b_1=0,c_2\ne0\) endpoint.  Its contact equations force a
  second common line, and both exact engines now include it.
- Added a strict umbrella runner.  Every leaf has dual-CAS checks; only
  the generic component-saturation completeness still lacks an
  independent implementation.

## 2026-07-25T15:01:52Z — marked-double exact-\(\delta=2\) component closed

- For the component \(\gcd(\alpha,\beta,\gamma)\sim p^2\), constructed
  two divided-gradient Hilbert--Burch columns whose change-of-basis
  determinant is exactly \(-p^2\).  This forces the \(\{1,1\}\) shape
  and removes the nominal \(\{2,0\}\) branch.
- On \(R=p^2q\), every generic nonzero contact creates an additional
  quadratic gcd factor.  The sole totally ramified contact family instead
  has the invariant obstruction
  \([q^3r^2]E_5=140\tau^3/9\).
- On \(R=p^3\), every nonzero contact creates an additional linear gcd
  factor; its \(a_2=0\) boundary already lies in \(\delta\ge3\).
- Added a candidate theorem, hostile checklist, full-lower SymPy check,
  independent PARI/GP replay, and priority audit in
  `delta2_marked_double/`.  Promotion awaits an independent hostile
  normalization audit.

## 2026-07-25T15:28:00Z — exceptional mixed \(\{2,0\}\) component closed

- For the mixed divisor \(\gcd(\alpha,\beta,\gamma)\sim pq\), the
  rank-drop divisor \(b_1=0\) admits a twice-divided tangent
  \(N=(P_q,Q_q,R_q)/(pq)\) of component degrees \((1,1,0)\).  This is
  precisely the exceptional Hilbert--Burch splitting \(\{2,0\}\).
- Degree-six curvature forces the \(r\)-coefficient of its multiplier
  to vanish.  The two residual endpoint charts then exhaust all binary
  contacts.
- One endpoint has no projective contact.  The other has exactly two
  nonzero contact loci, but direct reconstruction shows that their
  original minors have gcd degree at least three and four,
  respectively.  They therefore lie outside exact \(\delta=2\).
- The zero-contact branch exits through a plane Keller map over
  \(\mathbb C(r)\), hence is birational and an automorphism.
- Added a candidate theorem, hostile checklist, exact SymPy suite,
  independent PARI/GP replay, and a candidate-specific priority audit in
  `delta2_mixed_k20/`.  Promotion awaits an independent hostile audit of
  the normal form, Hilbert--Burch identification, and plane-field exit.

## 2026-07-25T16:05:16Z — mixed \(\{1,1\}\) component closed

- Constructed both divided-gradient Hilbert--Burch columns on the
  \(b_1\ne0\) mixed divisor and split the residual quotient into its two
  endpoint charts.
- One endpoint has no projective contact.  On the other, both
  \(y=0\) contact components acquire extra gcd factors.
- The genuine \(y\ne0\) contact locus is an explicit curve \(V(b,c)=0\)
  away from two higher-gcd pivot divisors.  The \(r^2E_5\) coefficient
  is independent of every lower integration constant.
- Two exact obstruction resultants force a common zero to \(c=8\) or
  \(c=16\).  The \(c=8\) points are higher-gcd; the \(c=16\) contact
  quadratic is coprime to a direct \(E_5\) remainder.
- The exact SymPy suite and an independent PARI/GP reconstruction pass.
  This provisionally closes both Hilbert--Burch components of
  \(g\sim pq\), but promotion awaits hostile normal-form and saturation
  audits.

## 2026-07-25T18:21:09Z — exceptional unmarked-double open closed

- The \(q^2\)-jet equations give a complete unmarked-double normal form.
  Its exceptional Hilbert--Burch divisor is
  \(3b_1^2-8b_2=0\).
- On \(b_1\ne0\), curvature removes the \(r\)-multiplier and every
  nonzero contact reduces to one \(nqN\) tangent.  Four lower-independent
  \(r^2E_5\) coefficients cannot vanish simultaneously.
- The zero-contact endpoint with vanishing third syzygy component has
  \(R=(p+q/4)^3\).  A full rank-six \(E_5\) solve, with all seven free
  parameters retained, leaves the literal \(E_4\) obstruction
  \((9/64)\eta^2rR\).
- Exact SymPy and independent PARI/GP suites pass.  The \(b_1=0\)
  endpoint and complementary unmarked-double \(\{1,1\}\) component
  remain open, and hostile audit is required before promotion.

## 2026-07-25T18:40:21Z — exceptional unmarked-double endpoint closed

- At \(b_1=0\), exact gcd gives
  \((P,Q,R)=(pq^3,p^4,dp^3+q^3)\).  The complete rank-12 \(E_7\)
  system has the three-parameter contact
  \(f=mp+nq+\rho r\).
- Exhausting the three nonzero projective charts forces columns two and
  three of the linear part to be proportional.  The zero chart reduces
  to the plane-field exit.
- Exact SymPy and independent raw PARI/GP reconstructions pass.  The
  entire exceptional unmarked-double \(\{2,0\}\) component is
  provisionally closed; the complementary \(\{1,1\}\) component and
  hostile audit remain.

## 2026-07-25T19:01:34Z — complementary unmarked-double component closed

- On \(K=3b^2-8c\ne0\), two divided-gradient columns reconstruct the
  binary gradient with determinant \(-16q^2/K\), giving the
  \(\{1,1\}\) Hilbert--Burch splitting.
- Four scaling charts exhaust the parameters.  The generic chart has
  no exact contact: one projective tangent lies entirely on a
  larger-gcd boundary and the other is inconsistent by exact
  resultants.  The remaining three charts have no contact off \(K=0\).
- Independent SymPy and PARI/GP certificates pass.  Thus both
  Hilbert--Burch components of the unmarked-double \(q^2\) locus are
  provisionally closed; hostile audits are running.
