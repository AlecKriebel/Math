# Research Log

All times are UTC.

## 2026-07-24T22:30:00Z — Program start

- Opened the dimension-three Keller degree program on the repository's
  `main` worktree.
- Active rung: generic-degree-two exclusion.
- Preserved unrelated uncommitted work in the original worktree; this program
  is isolated in its own directory.
- Launched independent field-theoretic, purity/involution, and topological
  double-cover investigations.
- Local root track: nonproperness geometry, normalization of the target in the
  quadratic function-field extension, and a current-priority sweep.
- No theorem claimed.

## Checkpoint estimate

Best-guess completion toward a publishable Rung 1 result: **3%**.  This is only
an initialization estimate and may decrease after hypothesis audits.

## 2026-07-24T22:42:23Z — Rung 1 banked; total-degree frontier located

### Generic degree

- Three independent audits found the same decisive classical theorem.  If
  \(K(F_1,\ldots,F_n)\subset K(x_1,\ldots,x_n)\) is Galois and \(F\) is
  Keller, then \(F\) is an automorphism (Campbell 1973 over \(\mathbb C\);
  Razar 1979 and Wright 1981 in characteristic zero).
- A separable quadratic extension is Galois.  Thus generic degree two is
  impossible for a counterexample in every characteristic-zero dimension.
  Generic degree one is excluded by the same theorem.
- An independent elementary proof was checked: write a hypothetical quadratic
  extension as \(L=K(\sqrt h)\) with squarefree \(h\).  Normality of the source
  polynomial ring puts \(g=\sqrt h\) in that ring.  Differentiating
  \(g^2=h(F)\) sends the hypersurface \(V(g)\) into
  \(\operatorname{Sing}V(h)\), contradicting quasi-finiteness and the
  codimension-two bound for the singular locus of a reduced hypersurface.
- The weighted-lift family already present in the repository realizes every
  generic degree \(d\geq3\) by an explicitly noninjective Keller map in
  dimension three.  Hence the counterexample spectrum over \(\mathbb C\) is
  exactly \(\{3,4,5,\ldots\}\).  This conclusion is already public.
- Additional consequence: every generic-degree-three counterexample has
  geometric monodromy \(S_3\), since the only transitive alternative \(C_3\)
  would make the degree-three extension Galois.

### Total polynomial degree

- Wang's general theorem excludes total degree at most two.
- Vistoli, *The Jacobian conjecture in dimension 3 and degree 3*,
  J. Pure Appl. Algebra 142 (1999), 79--89, excludes total degree at most
  three in dimension three.  Therefore the current certified floor for a
  dimension-three counterexample is total degree four.
- This floor is classical, not a new table entry.  Searches to this timestamp
  found no theorem excluding total degree four and no explicit
  dimension-three counterexample of total degree below seven.
- A public “degree-four” example found during the sweep has **generic** degree
  four but component degrees \((12,11,4)\); it does not improve the
  total-degree upper bound.

### Active round

- Route A reconstructs Vistoli's degree-three argument and isolates the first
  quartic obstruction.
- Route B expands the Keller determinant for
  \(F=X+H_2+H_3+H_4\) and seeks universal constraints on the leading pieces.
- Route C studies generic target-line pullbacks and the boundary/nonproperness
  geometry of quartic maps.
- The leading-form grading search remains independent and is being compared
  against the unreviewed skeleton-rigidity claims posted publicly on 23 July.

## Checkpoint estimate

Rung 1 mathematical classification: **100%**, with priority occupied.
Packaging and visual verification: **65%**.
Best-guess progress toward a new total-degree-four exclusion or structural
lemma: **5%**.  No novel theorem is claimed at this timestamp.

## 2026-07-24T23:00:00Z — Generic-line defect candidate

- A generic target-line pullback produced the exact candidate identity
  \[
  K=2g-2+\delta+r,
  \]
  where \(K\) is total missing-sheet defect over the intersection with the
  nonproperness hypersurface, \(g\) is the genus of the completed pullback
  curve, \(\delta\) is generic degree, and \(r\) is its number of punctures.
- Independent derivations use Euler characteristic of the finite étale cover
  and Riemann--Hurwitz with exact boundary local degrees.
- The first numerical consequence is
  \[
  2g\le s(\delta-2)-\delta+1.
  \]
  The coarse corollary \(s\ge2\) is prior: the hyperplane case is already
  excluded by Nollet--Xavier (2007).
- Combining the line inequality with Jelonek's degree bound and Bézout gives,
  for a hypothetical total-degree-four counterexample,
  \[
  3\le\delta\le56,\qquad
  2\le s\le
  \min\{15,\lfloor(64-\delta)/4\rfloor\}.
  \]
- In the coprime-leading-quartic case the generic line closure is a
  \((4,4)\) complete intersection of arithmetic genus \(33\).  For
  \(\delta=3\) it must lose at least \(27\) units of genus at infinity.
- The argument is recorded in
  `rung2_degree_bound/WORKING_LINE_SECTION.md`.  It remains a candidate until
  the Bertini irreducibility and compactified-boundary base-change steps pass
  adversarial audit.

## 2026-07-24T23:04:08Z — First program release prepared

- Rung 1 was packaged as a fully attributed archival result, including
  `NOTE.md`, a typeset paper, two exact regression scripts, a verification
  record, and a rung-specific priority audit.
- No novelty is claimed for Rung 1.
- The working Rung 2 line-section lemma is included with candidate status and
  explicit remaining audit obligations.

## 2026-07-24T23:09:25Z — Line-section proof audit and release verification

- Adversarial review proved generic-line integrality by two successive
  applications of Bertini irreducibility to
  \(\mathbb P\langle1,F_1,F_2,F_3\rangle\), and proved boundary detection on
  a resolution of the compactified graph.
- The exact defect identity and its sandwich
  \[
  K=2g-2+\delta+r,\qquad
  2g+\delta+s-1\le K\le s(\delta-1)
  \]
  now have a complete internal proof.  They remain unpublished working
  results pending a broader priority and citation audit.
- The quartic complete-intersection conclusion was narrowed correctly: it
  applies only when the two leading quartics are coprime.  No uniform
  “large singularity” claim is made.
- Rung 1's four-page PDF was rebuilt and visually inspected after the final
  divisibility proof was added.  The independent SymPy and PARI/GP exact
  regression checks both pass.

## 2026-07-24T23:43:08Z — Quartic conductor and leading-form checkpoint

### Banked working lemmas

- In the coprime-leading \((4,4)\) complete-intersection case, finite duality
  and the Keller adjunction residue give the exact divisor equation
  \[
  \operatorname{div}(dt)+A=4E.
  \]
  For a boundary branch of hyperplane multiplicity \(m\) and local target
  degree \(e\), the conductor exponent is
  \[
  c=4m-e+1
  \]
  over a finite target value and \(c=4m+e+1\) over infinity.
- In generic degree three this yields an exact boundary-profile table.  If
  \(s=\deg S_F=2\), the only profile is
  \[
  q=1,\quad g=0,\quad b=0,\quad \tau=2,\quad
  \Delta_\infty=33,
  \]
  and the two finite local-degree-two branches must meet the same projective
  singular support.
- For a primitive line-valued quartic leading pencil
  \(H_4=(P,Q,0)\), the degree-eight and degree-seven Keller identities force
  either a pencil member \(L^4\) paired with
  \((H_3)_3\propto L^3\), or a pencil member proportional to
  \((H_2)_3^2\).  If both subleading third components vanish, the map is an
  automorphism.
- If \(F=X+H_3+H_4\) and \(\operatorname{rank}JH_4\le1\), then
  \(JH_3,JH_4\) share a strict triangular flag and \(F\) is an automorphism.
  With \(H_2\ne0\), the same conclusion holds whenever the constant image
  line of \(JH_4\) is invariant under both \(JH_2\) and \(JH_3\).

### Adversarial corrections

- The first conductor draft falsely asserted that every finite conductor
  exponent is positive.  An exact smooth local complete-intersection branch
  has \(m=1,e=5,c=0\).  All boundary-singularity conclusions were restricted
  to generic degree three, where \(e\le2\).
- The first line-type draft falsely inferred primitive parametrization from
  line image.  The example \(H_4=(x^4,y^4,0)\) disproves that inference.
  Relative algebraic closedness is now an explicit hypothesis; the composite
  \((2,2)\) and \((1,4)\) parameter strata remain active.
- Rank-one \(JH_4\) does not force simultaneous triangularization once
  \(H_2\ne0\).  The exact automorphism
  \[
  (x,y,z)\mapsto(x+y^2,\ y+(x+y^2)^2,\ z)
  \]
  supplies a counterexample to that strategy.

### Verification and frontier

- Independent SymPy and PARI/GP exact regressions pass.  A separate
  mathematical audit checked the duality sign, local conductor formulas,
  divisor partitions, nilpotent matrix pencil, and common-flag arguments.
- Source-specific searches found the imported homogeneous theorems but no
  exact occurrence of these mixed quartic structural lemmas.  This is not a
  guarantee of worldwide priority.
- The universal certified degree floor remains \(4\).  The current
  highest-information experiment is the composite line-image
  \((\deg(p,q),\deg A)=(2,2)\) stratum, where the degree-eight identity has
  already reduced to a concrete vertical-divisor syzygy.

## 2026-07-25T00:10:26Z — Rational-image quartic strata banked

### New structural theorems

- **Quadratic-component exit.**  A total-degree-at-most-four Keller map in
  dimension three is an automorphism whenever a nonzero target-linear
  combination of its components has degree at most two.  A nowhere-critical
  quadratic is straightened by a degree-two polynomial automorphism; the
  resulting plane fibres have degree at most eight and are automorphisms by
  the established plane lower bound.
- **Genuine line image, type \((2,2)\).**  For a primitive quadratic pencil
  with no scheme-theoretic double-line member, the degree-eight identity
  forces the third cubic component to vanish, so the quadratic-component
  exit applies.  A counterexample in this stratum must have a unique
  double-line fibre and cubic normal component
  \[
  cL^3\quad\text{or}\quad cL(\alpha p+\beta q).
  \]
- **Genuine line image, type \((1,4)\).**  With binary quartics \(P,Q\) and
  binary cubic \(R\), a map is an automorphism whenever
  \[
  \gcd\bigl(J(P,Q),J(P,R),J(Q,R)\bigr)=1.
  \]
  The proof uses the exact Hilbert--Burch resolution of the ramification
  minors.  Keeping the arbitrary linear part exposed was essential: degree
  six also forces its complementary source direction into the leading target
  plane.
- **Conic image, type \((2,2)\).**  Away from a double-line fibre, the
  nonlinear part has the exact form
  \[
  \operatorname{Ver}(p+\ell,q+m)+M(p,q).
  \]
  This is a normal-form constraint, not yet an automorphism theorem.

### Verification, corrections, and scope

- Independent SymPy and PARI/GP scripts check the determinant coefficients,
  chain-rule factors, conic adjugate and syzygies, double-line examples, and
  quadratic coordinate change.
- Independent mathematical audits checked the arbitrary linear part, divisor
  parity, relative-algebraic-closedness hypotheses, and the exact degree
  tracking.  The conic-pencil primitive-fibre lemma now includes its explicit
  determinant calculation.
- A final adversarial pass caught two omitted proof bridges rather than false
  conclusions: it required an explicit homogeneous first-integral lemma
  before descending \(D\)-invariants to \(\mathbb C(p/q)\), and a separate
  proof of geometric integrality when there is exactly one double-line
  fibre.  Both repairs are now in the notes.  The same pass found that the
  conic degree-seven coefficient was not fully represented in the initial
  harness; both exact systems now expand that complete identity.
- The leading sharpness examples certify only the corresponding homogeneous
  determinant identities; none is presented as a Keller map.
- The universal certified lower bound remains total degree \(4\).  The active
  rational-image loci are common ramification in type \((1,4)\), the unique
  double-line branches in type \((2,2)\), and the lower identities in the
  conic normal form.

### Priority and next experiment

- A fresh required-channel sweep after the UTC date change found no checked
  source containing these exact quartic statements.  This is source-specific
  evidence only and is not a guarantee of worldwide priority.
- The highest-information experiment is to classify the common factor of the
  three binary ramification minors in type \((1,4)\), while independently
  expanding the lower identities of the conic normal form.

## 2026-07-25T00:26:09Z — No-double-line conic stratum excluded

- The conic \((2,2)\) normal form was pushed through the next Keller
  coefficient.  Writing
  \[
  F=AX+\Phi(P,Q),\qquad
  \Phi(s,t)=\operatorname{Ver}(s,t)+M(s,t),
  \]
  the rank-two determinant formula shows that degree six is exactly
  \[
  (q^2,-2pq,p^2)A(\nabla p\times\nabla q)=0.
  \]
- The syzygies of \((q^2,-2pq,p^2)\) reduce this to a statement about
  \[
  W=\{\operatorname{Jac}(p,q,h):h\text{ linear}\}
  \quad\text{and}\quad U=\langle p,q\rangle.
  \]
  Either the residual constant matrix \(A\) vanishes, or \(U\subseteq W\).
- A nonsingular member identifies the pencil with a self-adjoint
  three-dimensional operator.  Absence of a double line leaves exactly
  three Jordan types: three distinct eigenvalues, a \(2+1\) type with
  distinct eigenvalues, or one size-three block.  In the three canonical
  forms,
  \[
  W\cap U=0,\quad 0,\quad\langle p\rangle,
  \]
  respectively, and the derivation on linear forms is injective.  Hence
  \(A=0\), which makes \(JF\) have rank at most two, a contradiction.
- Therefore **no** quartic Keller map, automorphism or counterexample, has a
  conic-image \((2,2)\) leading part whose quadratic pencil has no
  double-line member.
- An adversarial agent independently reconstructed the rank-two determinant,
  Jordan classification, intersections, and row/column orientations.
  SymPy and PARI/GP also check the generic determinant formula and rank-nine
  coefficient systems for all three canonical types.
- Scope remains exact: the unique-double-line conic locus is not excluded.
  The universal degree floor remains \(4\).

## 2026-07-25T00:45:17Z — Binary and quartic-curve ramification shapes

- In the genuine line-image \((1,4)\) stratum, put
  \[
  g=\gcd\bigl(J(Q,R),J(P,R),J(P,Q)\bigr).
  \]
  If the first two minors are independent, Hilbert--Burch forces
  \[
  \deg g\le4,\qquad
  \{k_1,k_2\}\in
  \{\{1,0\},\{2,0\},\{1,1\},\{2,1\},\{2,2\}\}.
  \]
  These are the complete possible degree-seven third-direction syzygy
  shapes, and exact binary representatives realize every splitting.
- If the first two minors are dependent and \(R\ne0\), the case is exactly
  the power fibre \(L^4/L^3\), with \(\deg g=5\).  The already excluded
  \(R=0\) branch is recorded separately.
- Every nonexceptional root of \(g\) has multiplicity at most three.  The
  resulting \(\operatorname{PGL}_2\)-normal divisor list and a local
  coefficient normal form are explicit in the working note.
- The exact degree-six equation contains a curvature term \(T_6\); simple
  divisibility by \(g\) is weaker than the required ideal-membership test.
  A degrees-eight-through-six construction with nonzero degree five proves
  that this frontier is sharp.
- The adversarial audit caught a cross-term error in the initial
  \(\{2,2\}\) statement.  The corrected formula applies the quadratic
  contact curvature to the combined syzygy
  \(N_\gamma=\sum\gamma_iN_i\).  All shifts, signs, local forms,
  representatives, and sharpness coefficients then passed.
- Independently, if the leading projective image is a birationally
  parametrized plane quartic and the three normal minors have gcd one,
  Hilbert--Burch forces the cubic and quadratic terms to be independent of
  the complementary source coordinate.  The map reduces to a degree-four
  plane automorphism plus a shear.  Thus any counterexample in that stratum
  must have a nonconstant ramification divisor in its basepoint-free
  parametrization.
- Both exact regression systems and separate mathematical audits pass.  These
  are structural classifications, not a complete degree-four exclusion; the
  universal floor remains \(4\).

## 2026-07-25T00:59:22Z — Genuine conic-image \((2,2)\) eliminated

- A primitive quadratic pencil with one double-line member has exactly two
  canonical forms:
  \[
  (p,q)=(X^2,YZ)
  \quad\text{or}\quad
  (p,q)=(X^2,Y^2+2XZ).
  \]
  Their invariant rings give the full degree-eight cubic normal form.
- Exact degree-seven comparison has rank twelve, kernel \(M(p,q)\), and
  compatibility \(\alpha\ell_Y=\alpha\ell_Z=0\).  The two complete solution
  families for \(H_2\) are recorded in the conic note.
- Degree six immediately makes the linear part singular in the
  \(\ell=0\) branch.  In the remaining branch it kills all exceptional
  normal coefficients except one Jordan-pencil residue.
- In that residue, five displayed degree-five coefficients successively
  force \(\beta=\gamma=\delta=0\).  The remaining map factors through
  \(T=(X,P,Q)\); the unit product, dominance of \(T\), and injective pullback
  make the outer Jacobian constant, whose quadratic top then forces its
  first column to vanish.  This is a contradiction.
- The independent audit checked every canonical form, rank/kernel,
  compatibility ideal, affine translation, arbitrary \(L_0\) orientation,
  and coefficient.  New SymPy and PARI/GP scripts retain exact certificates.
- Together with the no-double-line theorem, this excludes the entire
  genuine/minimal conic-image \((2,2)\) stratum.  Pencils with two double
  lines are nonminimal and reclassify into type \((1,4)\).
- The universal certified degree floor remains \(4\); this is not yet a
  complete quartic exclusion.

## 2026-07-25T01:46:16Z — Primitive rank-one quotient pencils excluded

- For a rank-one quartic leading part, homogeneous rank one gives
  \(H_4=ah\) with a constant target line.  Projecting the cubic part modulo
  that line produces a cubic pencil \(\langle P,Q\rangle\).
- The degree-seven Keller identity is exactly
  \[
  \operatorname{Jac}(P,Q,h)=0.
  \]
  If the pencil is primitive and its generic member is geometrically
  integral, the degree-\((3,4)\) first-integral divisor has degree four.
  It forces a unique triple-line member and the exact exceptional form
  \[
  P=L^3,\qquad h=L(\alpha P+\beta Q).
  \]
- In that form, degree six gives a quintic first integral.  When
  \(\beta\ne0\), its degree-five base divisor forces \(L^2\) to divide the
  quadratic part of the \(P\)-component.  In the pure \(h=L^4\) case,
  degree five gives a quartic first integral and forces one factor \(L\).
- The selected full component is therefore
  \[
  f=L^3+LM+\ell.
  \]
  Its nowhere-vanishing differential makes it an explicit degree-three
  polynomial coordinate.  Straightening \(f\) leaves plane Keller fibres
  of degree at most \(4\cdot3=12\); the unconditional plane bound,
  fibrewise injectivity, and Ax--Grothendieck make the original map an
  automorphism.
- The independent audit caught an omitted
  \(6\Delta(L_0,JH_3,JH_4)\) term in the pure-power degree-five equation.
  The corrected first integral is
  \[
  9L^2U-2\mu S^2-12\mu L^3\ell_0.
  \]
  It has the same reduction modulo \(L\), so the theorem survives.  Both
  exact systems pass with arbitrary \(L_0\).
- If the projected cubic pencil has no fixed component but is
  nonprimitive, generalized Lüroth forces it to be a binary cubic pencil.
  On the gcd-one locus for
  \[
  J(P,Q),\quad J(P,h),\quad J(Q,h),
  \]
  Hilbert--Burch kills all third-variable nonlinear dependence and the map
  is a plane automorphism plus a shear.  The audit again caught the missing
  arbitrary-linear-part contribution; correctly retained, it is a
  total-degree-five syzygy and also forces the first two entries of
  \(L_0(\partial_z)\) to vanish.
- Thus a rank-one-leading quartic counterexample must now have either a
  fixed component in its projected cubic pencil or a nonconstant binary
  common-ramification factor.  This is a structural stratum theorem, not a
  universal quartic exclusion.  The certified floor remains \(4\).

## 2026-07-25T02:04:55Z — Curve taxonomy and nodal-cubic row

- Every rank-two quartic leading map with projective curve image has the
  minimal-pair form
  \[
  H_4=hA(p,q),\qquad e+ab=4,\qquad b=\delta\nu.
  \]
  Here \(e=\deg h\), \(a=\deg p=\deg q\), \(b=\deg A\),
  \(\delta\) is the image-curve degree, and \(\nu\) is the normalization
  cover degree.
- Enumerating these two exact equations gives thirteen rows.  The audit
  checked the de Bondt specialization, fixed divisor, base-scheme support,
  and every row.  It also corrected earlier coverage language: several
  line rows are only constrained, not excluded.
- The taxonomy exposes a previously hidden conic double-cover row
  \[
  H_4\sim\operatorname{Ver}(p^2,q^2),
  \]
  as well as all fixed-divisor rows \(e>0\).  The genuine conic
  \((2,2)\) theorem does not exclude this nonminimal two-double-line row.
- In the transverse nodal-cubic row, the degree-eight identity first gives
  \[
  H_3=A_p(\ell+\alpha r)+A_q(m+\beta r).
  \]
  The degree-seven normal minor factors as
  \[
  6(p^3+q^3)
  \bigl(cp^2+(d-a)pq-bq^2\bigr)^2,
  \]
  forcing \(H_3=\lambda A+r(\alpha A_p+\beta A_q)\).
- The full degree-seven and degree-six systems have ranks sixteen and nine:
  \[
  H_2=\frac13(uA_p+vA_q)+\frac r2D^2A,
  \qquad
  \det L_0=
  \frac49(\alpha^3+\beta^3)(\alpha v-\beta u)^2.
  \]
  Degree five is the square
  \[
  \frac49(p^3+q^3)
  \bigl((3\beta\lambda-v)p+(u-3\alpha\lambda)q\bigr)^2.
  \]
  Its vanishing makes \(\alpha v-\beta u=0\), contradicting invertibility
  of \(L_0\).  Therefore the entire transverse nodal-cubic leading row is
  empty.
- An independent raw coefficient solve and SymPy/PARI regressions reproduce
  all ranks, signs, and factors.  The cuspidal and scalar-aligned cubic
  branches remain.
- Separately, the unique-double-line line-\((2,2)\) audit caught a false
  simultaneous-normalization claim.  Its degree-seven equations and kernel
  computations are correct only on conditional charts; the outer critical
  pair and companion conic carry cross-ratio parameters.  The note now
  records an exact missed configuration and makes no exhaustive claim.
- These are structural stratum results, not a universal quartic exclusion.
  The certified floor remains \(4\).

## 2026-07-25T02:48:29Z — Complete nodal row and fixed-conic opening

- The scalar-aligned nodal branch was computed with the fixed divisor left
  as \(h=p+kq\); the smooth marked-point modulus was not normalized away.
  Four division-free left-null certificates in the full
  \(15\times30\) degree-seven system force the two complementary-variable
  coefficients of \(H_3\) to vanish for every \(k\).
- The remaining degree-seven equation is
  \[
  \frac43h^2(A_p\times A_q)\cdot\partial_rH_2=0.
  \]
  Hilbert--Burch gives no linear syzygy, so all nonlinear terms are binary.
  The map is a degree-at-most-four plane Keller block plus a shear and is
  therefore an automorphism.
- An independent raw-column audit reconstructed the complete polarization,
  Hilbert--Burch shifts, all four specialization-safe certificates, the
  \(h=q\) chart, and the plane exit.  Both SymPy and PARI regressions pass.
  Together with the prior transverse theorem, this excludes the entire
  nodal-cubic fixed-divisor row.  The cuspidal row remains.
- The first calculation in the binary fixed-divisor conic row writes
  \(H_4=h\operatorname{Ver}(p,q)\), with \(h=pq\) or \(p^2\).
  Degree six reduces the nonzero tangent field to finitely many Jordan
  branches.  For \(h=pq\), the opposite-weight branch has the exact
  degree-five incompatibility \(64=0\); the scalar branch ends in a
  degree-two square whose vanishing makes \(\det L_0=0\).
  These conic calculations remain unpromoted pending a second derivation.
- The exact priority search found no checked overlap with the complete
  nodal-row exclusion.  This is not a guarantee of worldwide priority.
- The certified universal floor remains total degree \(4\).

## 2026-07-25T03:19:56Z — Binary fixed-divisor conic subrow excluded

- The full raw determinant audit closed every branch of
  \[
  H_4=h(p,q)\operatorname{Ver}(p,q),\qquad \deg h=2.
  \]
  The two binary quadratic orbits are \(h=pq\) and \(h=p^2\).  Degree
  eight gives the tangent Hilbert--Burch form, degree seven removes its
  quadratic \(r\)-part, and the coefficient of \(r^2\) in degree six gives
  the exhaustive scalar/opposite/semisimple/nilpotent/zero branch list.
- In the split-root scalar and double-root scalar branches, the final
  determinant coefficient is an exact square.  Its vanishing cancels the
  exact square factor of \(\det L_0\), without dividing by any branch
  parameter.  The split opposite branch has the constant obstruction
  \(64\).
- The double-root semisimple branch has a constant \(9\times9\) linear-system
  minor \(32768\) and its unique \(L_0\) is singular.  The nilpotent branch
  was split at the essential parameter \(K=0\); on that branch two columns
  of \(L_0\) are exactly proportional.  All nonzero zero-tangent support
  orbits have constant degree-five obstructions.  The remaining zero orbit
  is a degree-at-most-four plane Keller block plus a shear and is an
  automorphism.
- The adversarial audit found no missing binary branch, but caught a scope
  overstatement before promotion.  For a general quadratic fixed factor,
  the binary condition is intrinsically \(\iota_kB_h=0\).  The five
  nonbinary parabolic normal forms
  \[
  r^2,\quad r^2+p^2,\quad r^2+pq,\quad pr,\quad pr+q^2
  \]
  remain open.
- The new SymPy regression covers all seven tangent branches; an independent
  PARI/GP expansion covers the top reductions and both scalar endgames.
  Both pass, and the raw-system audit supplies the methodologically
  independent check.
- The source-specific priority sweep found no exact overlap.  It is not a
  guarantee of worldwide priority.  The universal certified floor remains
  total degree \(4\).

## 2026-07-25T04:03:51Z — Complete fixed-divisor conic row excluded

- For
  \[
  H_4=h(p,q,r)(p^2,pq,q^2)^T
  \]
  with nonbinary quadratic \(h\), the degree-eight adjugate identity reduces
  to
  \[
  4Hn_s=3H_sn.
  \]
  A logarithmic valuation at every \(s\)-dependent irreducible factor of
  \(H\) forces \(n=0\), so \(H_3\) lies in the Veronese tangent module.
- The parabolic group preserving \(\langle p,q\rangle\) has exactly five
  nonbinary normal forms:
  \[
  r^2,\quad r^2+p^2,\quad r^2+pq,\quad pr,\quad pr+q^2.
  \]
  Affine translations remove the apparent cubic tangent moduli.  The
  complete degree-seven quadratic kernel followed by a triangular
  degree-six subsystem forces the linear part to be singular in every
  branch.
- A draft homogeneous-orbit modulus was rejected during audit: translations
  in \(r\) add its scalar part, while translations in \(p,q\) remove the
  remaining tangent parameters.  Retaining affine rather than homogeneous
  equivalence is essential.
- The two exact implementations pass, and a final independent raw-system
  audit reconstructed the seven-form taxonomy, compatibility radicals,
  affine signs, complete kernels, and singular exits.  Combining this with
  the audited binary theorem excludes the entire fixed-divisor conic row
  \[
  (e,a,b,\delta,\nu)=(2,1,2,2,1).
  \]
- The source-specific priority sweep found no exact checked overlap.  This
  is not a guarantee of worldwide priority.  The result is an unreviewed
  stratum theorem and does not raise the universal certified floor above
  total degree \(4\).

## 2026-07-25T04:07:17Z — Transverse cuspidal-cubic branch excluded

- Every transverse fixed-divisor map in the cuspidal cubic row normalizes
  to
  \[
  H_4=r(p^2q,p^3,q^3)^T.
  \]
  Its reduced normal has Hilbert--Burch syzygies of coefficient degrees one
  and two.  The degree-eight equation gives their complete cubic tangent
  family.
- A specialization at \(r=0\) produces an exact square.  The full
  degree-seven system has rank \(14\); its three compatibility entries force
  the two exceptional tangent parameters to vanish, and its four-dimensional
  kernel gives the complete quadratic part.
- The degree-six system retains an arbitrary nine-entry \(L_0\), has rank
  \(8\), and solves all but one entry.  Degree five factors into two
  conjugate polynomial factors; degree three then forces the same square
  whose multiple is \(\det L_0\) to vanish.  Thus no Keller map occurs.
- Exact SymPy and independent PARI/GP regressions pass.  A separate audit
  reconstructed the projective normalization, raw ranks, kernel
  completeness, lower factors, and verifier failure paths.  It found no
  correction or scope overreach.
- This closes only \(h\notin\langle p,q\rangle\).  The scalar-aligned
  cuspidal branch remains active.  The source-specific priority sweep found
  no exact checked overlap, which is not a guarantee of worldwide priority.
  The universal certified floor remains total degree \(4\).

## 2026-07-25T04:36:50Z — Complete cuspidal-cubic row excluded

- The stabilizer of the embedded cuspidal parametrization
  \((p^2q,p^3,q^3)\) is diagonal, not the full
  \(\operatorname{PGL}_2\).  A scalar-aligned fixed linear divisor therefore
  has exactly three marked-point orbits:
  \[
  h=p,\qquad h=q,\qquad h=p+q,
  \]
  marking the cusp, the smooth flex, and a general smooth point.
- The common reduced normal has Hilbert--Burch generators of coefficient
  degrees one and two.  Each raw degree-seven system has rank \(8\), and
  its division-free compatibility tree leaves only binary cubic branches
  plus three explicit nonzero tangent branches.
- Binary branches with zero quadratic tangent force the third column of
  \(L_0\) to vanish.  Nonzero quadratic tangent gives degree-six ranks
  \(7,6,7\) and the parameter-free degree-five obstruction \(24\).
  The three nonzero cubic tangent leaves have degree-six constants
  \(-12,-48,12\).
- Exact SymPy and independent PARI/GP regressions pass.  A separate audit
  reconstructed the stabilizer, all raw radicals and converses, every
  kernel dimension, and all constants.  Combining this theorem with the
  transverse cusp theorem excludes the complete cuspidal row
  \[
  (e,a,b,\delta,\nu)=(1,1,3,3,1).
  \]
- The source-specific priority sweep found no exact checked overlap.  This
  is not a guarantee of worldwide priority.  The universal certified floor
  remains total degree \(4\).

## 2026-07-25T04:41:47Z — Nonbinary fixed-cubic line subrow excluded

- For
  \[
  H_4=h(p,q,r)(p,q,0)^T,\qquad h\notin\mathbb C[p,q],
  \]
  the leading Jacobian has
  \[
  \operatorname{adj}JH_4=-hke_3^T,\qquad
  k=(ph_r,qh_r,rh_r-4h)^T.
  \]
  The degree-eight identity is therefore a logarithmic derivation equation
  for \((H_3)_3\), and factor residues force that component to vanish.
- The corresponding degree-seven equation for \((H_2)_3\) has residue
  condition \(2v=m\).  It vanishes unless
  \(h=\ell(p,q)m(p,q,r)^2\).  In the vanishing case the third component is
  linear and the established degree-at-most-four plane theorem over
  \(\overline{\mathbb C(r)}\), followed by the birational Keller theorem,
  makes the whole map an automorphism.
- The exceptional factorization normalizes to \(h=pr^2\), with complete
  normal-component space \(r\langle p,q\rangle\).  Its two nonzero
  stabilizer orbits \(qr\) and \(pr\) were carried through the lower
  determinant identities; both force \(\det L_0=0\).
- Exact SymPy and independent PARI/GP regressions pass.  A separate audit
  reconstructed the factor classification, stabilizer quotient, raw
  normalized systems, and plane-field exit.  A strict wrapper prevents GP
  diagnostics from being followed by a false pass.
- The source-specific priority sweep found no exact checked overlap.  This
  is not a guarantee of worldwide priority.  The binary locus
  \(h\in\mathbb C[p,q]\) remains active, and the universal certified floor
  remains total degree \(4\).

## 2026-07-25T05:19:48Z — Conic double-cover row excluded

- Every degree-two normalization map in the row
  \((e,a,b,\delta,\nu)=(0,1,4,2,2)\) is left-right equivalent to the
  squaring map, giving the exhaustive leading form
  \[
  H_4=(x^4,x^2y^2,y^4)^T.
  \]
- The degree-eight operator has rank \(16\) and a complete
  \(14\)-parameter cubic kernel.  Degree seven has constant rank \(9\),
  with exactly two endpoint compatibilities.  The stabilizer reduces their
  tangent parameters to the zero, two-nonzero, and one-nonzero patterns.
- In the two-nonzero pattern, a constant rank-\(6\) degree-six solve and
  division-free affine gauge give one canonical family; degree five kills
  the first two columns of \(L_0\).  In the one-nonzero pattern, the
  complete affine slice has five moduli with the exact equation \(PM=0\).
  The \(P\ne0\) branch loses its second column, while \(P=0\) loses its
  first column.  The zero pattern is a plane degree-at-most-four
  automorphism plus a shear.
- Exact SymPy and independent PARI/GP regressions pass.  A hostile audit
  reconstructed the normalization, stabilizer, raw ranks, all gauges and
  converses, every specialization endpoint, and the plane input.  It found
  no omitted branch or false-hypothesis inheritance.
- The source-specific priority sweep found no exact checked overlap.  This
  is not a guarantee of worldwide priority.  The universal certified
  total-degree floor remains \(4\).

## 2026-07-25T05:38:33Z — Nonbinary fixed-quadratic line double cover excluded

- The degree-two outer line cover normalizes exhaustively to
  \[
  H_4=h(p,q,r)(p^2,q^2,0)^T.
  \]
- For nonbinary \(h\), logarithmic residues kill the cubic normal
  component.  A nonzero quadratic normal forces the global polynomial
  square \(h=c(r+uq+vp)^2\), not merely a square over
  \(\mathbb C(t)\).
- After \(h=r^2\), the full stabilizer has exactly the two nonzero normal
  orbits \(pr\) and \((p+q)r\).  Complete constant-rank degree-six and
  degree-five solves, followed by division-free lower identities, force
  \(\det L_0=0\) in both.
- A separate hostile audit reconstructed the normalization, global
  rehomogenization, stabilizer, ranks, converses, \(K\)-split, determinant
  divisibilities, and the plane-field exit.  Verdict: PASS.
- Exact SymPy, supplied PARI/GP, and independent audit PARI/GP checks pass
  behind fail-closed guards.  The binary locus remains active, and the
  universal certified floor remains total degree \(4\).

## 2026-07-25T05:47:58Z — Transverse fixed-linear line triple cover excluded

- In the row \((e,a,b,\delta,\nu)=(1,1,3,1,3)\), a transverse fixed line
  gives
  \[
  H_4=r(A(p,q),B(p,q),0)
  \]
  with completely general coprime binary cubics \(A,B\).
- The leading cross-product derivation diagonalizes after
  \(q=pt,r=ps\).  Its degree-three and degree-two normal equations have
  eigenvalues \(4j-3\) and \(4j-2\), respectively, so both nonlinear normal
  components vanish.
- The remaining linear normal coordinate reduces to a degree-at-most-four
  plane Keller map over \(\mathbb C(r)\); the established plane theorem
  and birational Keller theorem make the map an automorphism.
- A hostile audit retained every cubic-cover modulus, recomputed the
  Wronskian identity and polarizations, justified cancellation in the
  integral domain and generic-degree descent, and fault-tested both
  verifiers.  Verdict: PASS.
- The binary fixed-line locus remains active.  The universal certified
  total-degree floor remains \(4\).

## 2026-07-25T06:06:25Z — Finite unique-double-line line-\((2,2)\) chart excluded

- For \(p=x^2,q=yz\), the simultaneous moduli of a two-finite-critical-point
  outer double cover and a finite mixed cubic companion are
  \[
  H_4=((p-aq)^2,(p-bq)^2,0),\qquad
  (H_3)_3=x(p-cq),\qquad a\ne b,
  \]
  modulo common scaling of \((a,b,c)\).
- Exact raw \(E_7\) weight blocks split the chart into the open locus,
  the triple branch \(c=0\), and the two resonances
  \(3ab-2ac-bc=0\) and \(3ab-ac-2bc=0\).  Complete lower solves in every
  finite-chart specialization force \(\det L_0=0\).
- The hostile audit found a real scope error before promotion: the
  stabilizer fixes \(p/q=\infty\), so
  \(H_4=((p-aq)^2,q^2,0)\) is a separate outer chart.  It reconstructed
  its resonances \(c=3a\) and \(2c=3a\), raw-rank strata, and exact
  leading witnesses.  No claim of whole-row closure is made.
- After narrowing and renaming the theorem, exact SymPy and PARI/GP checks,
  two independent direct reconstructions, optimized-mode rejection, and
  forged-GP diagnostic tests all pass.
- The universal certified floor remains total degree \(4\).

## 2026-07-25T06:11:00Z — Marked-critical infinity orbit excluded

- In the separate outer-critical-at-infinity chart, the point
  \[
  H_4=(x^4,y^2z^2,0),\qquad (H_3)_3=x^3
  \]
  has raw \(E_7\) rank \(8\), nullity \(18\), and a complete affine gauge.
- The rank-\(4\) \(E_6\) converse splits into four \((A,C)\) branches.
  Exact degree-five cubes, degree-four squares, and the resonant identity
  \(\det L_0=(\ell_{31}/3)[x^2]E_2\) close every specialization.
- A hostile audit reconstructed the complete gauges, target-shear ledger,
  lower converses, all zero cases, and executable failure paths.  Verdict:
  PASS after five nonfatal exposition/certificate corrections.
- This removes only \((a,c)=(0,0)\).  Both mixed resonances, the
  noncritical endpoint, the generic infinity chart, and both
  companion-at-infinity orbits remain active.
- The universal certified floor remains total degree \(4\).

## 2026-07-25T06:18:12Z — Horizontal fixed-linear cubic-pencil locus excluded

- In the row
  \[
  (e,a,b,\delta,\nu)=(1,3,1,1,1),\qquad H_4=h(p,q,0),
  \]
  assume the cubic pencil is minimal and no member contains the fixed line
  \(h=0\).
- If a homogeneous normal component \(G\) of degree \(d\) satisfies
  \(\operatorname{Jac}(hp,hq,G)=0\), scaling descent and relative
  algebraic closure give \(G^4/(hp)^d=R(q/p)\).  The \(h\)-valuation then
  forces \(4v_h(G)=d\), impossible for \(d=2,3\).
- Thus the top two Keller identities kill both nonlinear normal
  components.  The remaining linear normal coordinate gives a
  degree-at-most-four plane Keller map on every fibre, hence a polynomial
  automorphism.
- A hostile audit reconstructed every field, valuation, determinant, and
  plane-exit step and added fail-closed runners plus a dependency-free
  finite-field audit.  Verdict: PASS.
- The vertical determinantal locus remains active.  Exact primitive
  witnesses show that the top-identity vanishing fails there, though they
  are not Keller maps.
- The universal certified floor remains total degree \(4\).

## 2026-07-25T06:54:01Z — Fixed-divisor verticality unified across line pencils

- The scaling-descent argument extends from the fixed-linear
  cubic-pencil row to every primitive quartic line-pencil leading form
  \[
  H_4=(hp,hq,0),\qquad
  \deg h=e,\quad\deg p=\deg q=4-e,\quad1\le e\le3.
  \]
- If \(f^m\mid h\) is horizontal, a homogeneous cubic normal first
  integral satisfies
  \[
  \frac{G_3^4}{(hp)^3}=R(q/p),\qquad 4v_f(G_3)=3m.
  \]
  Since \(1\le m\le3\), this is impossible.  Thus \(G_3=0\), and the
  audited quadratic-component theorem makes the Keller map an
  automorphism.
- Consequently every prime component of \(h\) must be vertical.  For
  \(e=3\) this recovers \(h\in\mathbb C[p,q]\); for \(e=1\) it recovers
  the vertical fixed-line condition; and for \(e=2\) it leaves exactly
  the irreducible, double-line, and split-two-member vertical shapes
  listed in the dedicated note.
- A hostile audit independently reconstructed the field descent,
  valuation at finite and infinite pencil values, determinant
  orientation, and plane exit.  It added a dependency-free modular check
  and repaired a fail-closed PARI-wrapper defect.  Verdict: PASS.
- This is a structural restriction, not a universal quartic exclusion.
  The certified total-degree floor remains \(4\).

## 2026-07-25T07:02:00Z — Rank-one-restriction open orbit excluded

- For the second unique-double-line quadratic pencil
  \[
  p=x^2,\qquad q=y^2+xz,
  \]
  the exact source stabilizer induces the full Borel fixing the marked
  double-line value.
- When the two outer critical points avoid that value, the joint leading
  data normalize to
  \[
  H_4=((p-q)^2,(p+q)^2,0),\qquad
  (H_3)_3=x(p-cq),\qquad c\sim-c.
  \]
  The finite raw \(E_7\) rank is \(18\) away from
  \(c=0,\pm3\); a complete affine/target gauge then makes \(E_6\) kill ten
  transverse variables and \(E_5\) zero the last two columns of the
  linear part.
- Thus \(c(c^2-9)\ne0\) is impossible for a Keller map.  The theorem
  includes the critical-companion incidence \(c^2=1\) and leaves exactly
  the three marked-pair orbits plus unmarked \(c=0,c^2=9,\infty\).
- A hostile audit reconstructed the full stabilizer and six-row orbit
  taxonomy, found alternate exact \(E_7/E_6/E_5\) certificates, and
  confirmed every scope boundary.  Verdict: mathematical PASS.
- Before promotion, a missing plus sign, Borel-action wording, the
  verification-independence disclosure, and a permissive PARI wrapper were
  corrected; all fault-injection tests now pass.
- The certified universal total-degree floor remains \(4\).

## 2026-07-25T07:05:00Z — Binary fixed-cubic line row excluded

- In the binary half of
  \[
  (e,a,b,\delta,\nu)=(3,1,1,1,1),\qquad
  H_4=h(p,q)(p,q,0),
  \]
  the squarefree, double-root, and triple-root types of the binary cubic
  \(h\) give an exhaustive stabilizer quotient for the cubic normal part
  \(W=(H_3)_3\).
- The local marked-root formula
  \[
  \operatorname{ord}_{\ell}\gcd(a,b,c)
  =\min(2m,m+n-1)
  \]
  controls every raw \(E_7\) splitting.  Exact lower identities close all
  residual parameter pivots, including two algebraic multiplier branches
  and precisely four zero-normal lower leaves with constants
  \(-24/5,-15/2,3/2,-12\).
- Every other branch has a quadratic, pure-cube, matched-linear-factor, or
  binary plane-plus-shear coordinate exit whose plane degree is below the
  unconditional bound \(100\).  Hence every Keller map in this binary
  stratum is an automorphism.
- A hostile audit independently reconstructed the full orbit list, every
  raw rank and pivot, both conjugate algebraic branches, the delicate
  \(t4\) converse, all lower leaves, and the coordinate degree costs.
  Verdict: PASS; optimized and fault-injected executions fail closed.
- Together with the previously audited nonbinary theorem, this closes the
  entire fixed-cubic line taxonomy row.  The certified universal
  total-degree floor remains \(4\).

## 2026-07-25T07:08:00Z — Outer-infinity finite companions excluded

- In the one-outer-critical-point-at-infinity chart for
  \(p=x^2,q=yz\),
  \[
  H_4=((p-aq)^2,q^2,0),\qquad
  (H_3)_3=x(p-cq),
  \]
  simultaneous scaling makes the nonzero joint orbits
  \([a:c]\in\mathbb P^1\).
- Exact raw \(E_7\) ranks split this line into the generic locus, the
  resonances \(c=3a\) and \(2c=3a\), and the endpoints \(c=0\) and
  \(a=0\).  Complete \(E_6/E_5\) solves, with division-free \(K=0\)
  \(E_4\) square exits at both resonances, make columns two and three of
  the linear part proportional on every stratum.
- The origin \((a,c)=(0,0)\) was already excluded separately.  Therefore
  every finite companion in this outer chart is impossible; only the
  companion-at-infinity form \((H_3)_3=xq\), with its two residual outer
  orbits, remains there.
- A hostile audit independently reconstructed the orbit ledger, every raw
  rank and maximal minor, complete kernels, lower converses, endpoint
  specializations, and target-shear legality.  Verdict: PASS after
  correcting one overlapping generic-row label.
- The certified universal total-degree floor remains \(4\).

## 2026-07-25T08:05:00Z — All-vertical fixed-quadratic frontier reduced to two pencils

- Starting from the audited verticality theorem for
  \(H_4=(hp,hq,0)\), \(\deg h=\deg p=\deg q=2\), compared two simple
  primes in one pencil fibre:
  \[
  4(v_{f_1}G_3-v_{f_2}G_3)
  =3(v_{f_1}(hp)-v_{f_2}(hp)).
  \]
- The genuine \(h=\ell^2,p=\ell m\) shape gives \(4N=6\).
  The split \(h=\ell_1\ell_2\) shape gives \(4N=3\), unless it degenerates
  to the nonminimal pencil \(\langle\ell_1^2,\ell_2^2\rangle\).
  Both shapes are therefore excluded for Keller maps by the
  quadratic-component exit.
- In the remaining \(p=h\) shape, divisor parity forces a unique
  double-line member \(s=\ell^2\).  The exhaustive source/pencil normal
  forms and complete cubic kernels are
  \[
  \langle x^2,yz\rangle,\quad\langle x^3,xyz\rangle,
  \qquad
  \langle x^2,y^2+xz\rangle,\quad
  \langle x^3,x(y^2+xz)\rangle.
  \]
- A hostile audit reconstructed the valuation, parity, normal-form, kernel,
  and exit arguments in exact PARI and dependency-free arithmetic.
  Characteristics \(5\) and \(11\) were discarded after producing
  spurious modular kernels; modulo \(101\) and all fault tests pass.
- This identifies the sole all-vertical top frontier with the two
  canonical unique-double-line quadratic pencils.  It is still the
  separate \(e=2\) fixed-divisor form \(H_4=(p^2,pq,0)\), not the
  genuine \(e=0\) outer double cover on the same pencil.  Its two lower
  frontiers remain active, so the universal floor remains \(4\).

## 2026-07-25T08:32:00Z — Rank-one unmarked triple \(c=0\) excluded

- In the pencil \(p=x^2,q=y^2+xz\), the unmarked triple companion
  \[
  H_4=((p-q)^2,(p+q)^2,0),\qquad(H_3)_3=x^3
  \]
  has raw \(E_7\) rank \(16\) and a complete five-direction gauge.
- Degree-six and degree-five compatibility successively force
  \(w_2=w_3\) and \(w_1=0\), with no parameter division.
- The final constant pivot gives
  \(\ell_{12}=\ell_{22}=\ell_{32}=0\), so the linear part is singular.
- An independent hostile PARI reconstruction recovered literal square and
  cubic row syzygies and the full converses.  Verdict: PASS.

## 2026-07-25T08:38:00Z — Both rank-one marked mixed orbits excluded

- For the marked pair \(H_4=(p^2,q^2,0)\), the residual Borel quotient has
  exactly two mixed companions:
  \[
  (H_3)_3=xq,\qquad(H_3)_3=x(p-q).
  \]
- Each raw \(E_7\) system has rank \(18\), with a complete
  five-gauge/three-normal kernel.
- Constant \(E_6/E_5\) minors give complete solutions and force
  \(\ell_{12}=\ell_{22}=\ell_{32}=0\), including at
  \(w_2=w_3\).
- A hostile PARI audit reconstructed both orbit normal forms, all lower
  converses, and the collision specialization.  Verdict: PASS.
- The audited rank-one-restriction frontier is now the marked triple,
  unmarked \(c^2=9\), and unmarked companion at infinity.  Each has an
  exact provisional exclusion undergoing independent audit.  The
  universal floor remains \(4\).

## 2026-07-25T08:52:17Z — Both fixed-divisor \(e=2\) mixed companions excluded

- For the two canonical all-vertical pencils
  \[
  \langle x^2,yz\rangle,\qquad
  \langle x^2,y^2+xz\rangle,
  \]
  the fixed-divisor leading form is \(H_4=(p^2,pq,0)\).  The mixed cubic
  companion \(R=xq\) is impossible in both cases.
- The rank-two branch has exact \(E_6\) residuals
  \(Cw_3=Dw_5=0\); every nonzero normal produces a cube obstruction,
  while the zero-normal leaf has four literal \(E_5\) coefficients
  forcing \(\det L=0\).
- The rank-one branch has residuals
  \(Dw_5=Cw_5+Dw_4=0\).  Nonzero normals exit by \(D^3\) or the exact
  resultant \(-250C^9\).  Four separately recomputed zero-normal charts
  exhaust every rank drop and force \(\det L=0\).
- A hostile PARI reconstruction independently verified all raw kernels,
  constant pivots, syzygies, the apparent \(w_4=C\) denominator
  resonance, and every determinant exit.  Fault injections pass.
- Only the triple companion \(R=x^3\) remains for each \(e=2\) pencil.
  The universal total-degree floor remains \(4\).

## 2026-07-25T09:19:25Z — Rank-one marked triple orbit excluded

- In the genuine \(e=0\) line-\((2,2)\) stratum with
  \(p=x^2,q=y^2+xz\), the marked leading pair
  \(H_4=(p^2,q^2,0)\) and triple companion \((H_3)_3=x^3\) are
  incompatible with the Keller condition.
- The raw \(E_7\) kernel has rank profile \(8/18\) and a complete
  five-gauge/thirteen-normal decomposition.  The exact \(E_6\) ideal and
  lower identities close all \(K\ne0\), \(K=0,A\ne0\), and \(K=A=0\)
  leaves by square, minor, or singular-column exits.
- Hostile review rejected the first proof at three specialization
  points.  After repair, the primary SymPy certificate and a separately
  implemented PARI/GP reconstruction both pass, together with injected
  failures aimed at each repaired leaf.
- This is scoped to the genuine marked triple orbit and does not concern
  the separate fixed-divisor \(e=2\) triple problem.  The genuine
  rank-one frontier is now only unmarked \(c^2=9\) and the unmarked
  companion at infinity.  The universal total-degree floor remains \(4\).

## 2026-07-25T09:46:39Z — Fixed-divisor rank-two triple orbit excluded

- For the separate fixed-divisor \(e=2\) leading form
  \(H_4=(x^4,x^2yz,0)\), the triple companion
  \((H_3)_3=x^3\) is incompatible with the Keller condition.
- The corrected branch proof covers the two \(K\ne0\) resonances,
  \(K=0,A\ne0\), the nonzero-\((w_1,w_2)\) tail charts, and the
  full terminal chart.  Every leaf gives either a literal fourth-power
  contradiction or \(\det L=0\).
- Hostile audit found three parameter-dependent pivots that had been
  specialized illegally.  Fresh calculations repaired all three; the
  primary SymPy and independent PARI/GP certificates now pass, together
  with optimized-mode and fault-injection guards.
- Combined with the audited mixed-companion theorem, this closes every
  cubic companion orbit for the rank-two pencil
  \(\langle x^2,yz\rangle\).  The rank-one triple is the sole remaining
  fixed-divisor \(e=2\) orbit.  The universal total-degree floor remains
  \(4\).

## 2026-07-25T09:55:40Z — Unmarked finite resonance \(c^2=9\) excluded

- For the genuine \(e=0\) rank-one-restriction pencil
  \(p=x^2,q=y^2+xz\), the unmarked joint orbit
  \[
  H_4=((p-q)^2,(p+q)^2,0),\qquad(H_3)_3=x(p\mp3q)
  \]
  is incompatible with the Keller condition.
- Four division-free \(E_6\) squares reduce to a constant-rank lower
  system.  The only \(E_5\) resonance has a constant pivot, and two
  literal \(E_4\) coefficients close its nonzero-column branch.
- A hostile PARI/GP audit independently reconstructed every raw rank,
  specialization, lower converse, and the \(c=3\leftrightarrow-3\)
  symmetry. Strict and fault-injection tests pass. Verdict: PASS.
- The unmarked companion at infinity is the sole remaining genuine
  rank-one line-\((2,2)\) orbit. The universal total-degree floor remains
  \(4\).

## 2026-07-25T10:00:00Z — Rank-one companion at infinity excluded

- For
  \[
  p=x^2,\quad q=y^2+xz,\quad
  H_4=((p-q)^2,(p+q)^2,0),\quad(H_3)_3=xq,
  \]
  constant raw and lower minors force the last two columns of the linear
  part to vanish.
- A dependency-free hostile implementation reconstructed the determinant
  using sparse rational arithmetic, proved raw kernel completeness by a
  rank sandwich, and checked every gauge and lower converse. All strict
  and fault-injection tests pass. Verdict: PASS.
- Every joint orbit for the rank-one-restriction line-\((2,2)\) pencil is
  now excluded. The rank-two-restriction companion-at-infinity package is
  the sole remaining genuine line-\((2,2)\) frontier and is under final
  audit. The universal total-degree floor remains \(4\).

## 2026-07-25T10:07:13Z — Entire genuine line-\((2,2)\) row closed

- The remaining rank-two-restriction companion-at-infinity resonance
  \(t=-2\sim-1/2\) has raw \(E_7\) rank \(14\), a complete
  five-gauge/seven-normal kernel, and a division-free \(E_6\) square
  chain.
- A fresh PARI/GP reconstruction confirms the constant-rank lower
  converse and the \(E_5\) residual
  \(36K(\ell_{32}y^3z^2-\ell_{33}y^2z^3)\). Both \(K\)-branches force
  dependent columns of the linear part. Strict and six mutation tests
  pass.
- The projective orbit ledger covers the finite, outer, \(t=0\),
  \(t=\infty\), and reciprocal-resonance charts. Combined with the
  separately audited rank-one-restriction packages and the no-double-line
  exit, this excludes the entire genuine taxonomy row
  \((e,a,b,\delta,\nu)=(0,2,2,1,2)\).
- A fresh source-specific web sweep found no checked collision. This is
  not a worldwide-priority guarantee, and the result is not peer reviewed.
  The universal total-degree floor remains \(4\).

## 2026-07-25T10:48:53Z — Entire fixed-divisor \(e=2\) row closed

- The all-vertical top theorem leaves precisely
  \[
  H_4=(p^2,pq,0),\qquad
  \langle p,q\rangle=\langle x^2,yz\rangle
  \ \hbox{or}\ \langle x^2,y^2+xz\rangle,
  \]
  with cubic normal component in \(x\langle p,q\rangle\).
- A pencil shear gives exactly the mixed orbit \(xq\) and the triple
  orbit \(x^3\).  The previously audited mixed package closes both
  pencils, the rank-two triple package closes \(\langle x^2,yz\rangle\),
  and the new rank-one triple package closes
  \(\langle x^2,y^2+xz\rangle\).
- The last hostile audit found a hidden \(a_3=0\) specialization beneath
  an \(a_3^4\)-supported pivot.  A fresh \(s^8\)-pivot solve closes the
  leaf; it also corrected the legal axis gauge to an \(x\)-translation
  plus free-tail relabeling.  Three independent exact implementations,
  strict transcripts, and mutation guards now pass.
- A targeted arXiv, MathOverflow, Tao-blog, Secret Blogging Seminar, and
  publicly indexed X/Twitter sweep found no checked collision.  This is
  source-specific only and not a worldwide-priority guarantee.
- This closes a second full quartic line-image taxonomy row today.  Other
  quartic rows remain, so the universal certified floor remains \(4\).

## 2026-07-25T18:40:21Z — Exceptional unmarked-double component closed

- In the binary fixed-linear line-triple-cover row, the exact \(q^2\)
  normal form has exceptional Hilbert--Burch divisor
  \(3b_1^2-8b_2=0\).
- The \(b_1\ne0\) chart is excluded by a complete contact solve and a
  lower-independent \(E_5\) obstruction, with its sole zero-contact
  resonance obstructed literally at \(E_4\).
- At \(b_1=0\), exact gcd normalizes the top to
  \((P,Q,R)=(pq^3,p^4,dp^3+q^3)\).  Its rank-12 \(E_7\) system has a
  three-dimensional contact kernel.  Every nonzero projective contact
  chart forces two columns of the linear part to be proportional; the
  zero chart has the unconditional plane-field exit.
- Exact SymPy and independently reconstructed PARI/GP suites pass.  The
  full exceptional unmarked-double \(\{2,0\}\) component is
  provisionally excluded pending hostile audit.  Its complementary
  \(\{1,1\}\) component remains active, and the universal certified
  floor remains \(4\).

## 2026-07-25T19:01:34Z — Full unmarked-double \(q^2\) locus closed

- The complementary \(K=3b^2-8c\ne0\) component has two explicit
  determinant-\(q^2\) Hilbert--Burch columns of splitting
  \(\{1,1\}\).
- Four scaling charts exhaust its parameter space.  On the generic
  chart, every contact along the first tangent lies on the exact
  larger-gcd boundary \(eJ=0\); the second projective tangent chart is
  inconsistent by two exact resultants and an augmented determinant.
  The three boundary charts have no contact off \(K=0\).
- Exact SymPy Gröbner/saturation checks and an independent PARI/GP
  remainder-resultant reconstruction pass.  An independent hostile
  audit is running.
- Together with the \(K=0\) package, this provisionally excludes the
  entire unmarked-double exact-\(\delta=2\) locus in the fixed-linear
  row.  The universal certified floor remains \(4\).

## 2026-07-25T19:02:24Z — Fixed-quadratic thirteenth \(\{1,1\}\) leaf closed

- The squarefree-interior two-ramification-contact leaf now has a
  complete generic/alternate contact atlas.
- Exact algebraic-field pivots route every sextic, octic, quartic, and
  \(P_{16}\) projection factor.  The sole exact-open lift at
  \(w^2=-1,a=0\) survives top-only \(E_5\), but the full lower chain
  forces the first and third columns of the linear part to be
  proportional.
- Exact SymPy and independently reconstructed PARI/GP suites pass.
  Thirteen of fifteen fixed-quadratic exact-\(\delta=2,\{1,1\}\)
  leaves are now provisionally closed.  The two remaining leaves both
  have doubled nonbranch fixed divisor \(h=(p+q)^2\).
- Hostile audit remains pending; the universal certified floor stays
  \(4\).

## 2026-07-25T20:15:16Z — Symmetric monodromy banked for every weighted lift

- For an arbitrary admissible Gallagher seed \(p\) of degree \(d-1\), exact
  elimination gives the inverse polynomial
  \[
  \Phi(T)-PT+cQ
  \]
  and rational recovery of every source coordinate from a generic root.
  The derivative at the source root is \(-c\gamma\), which certifies that
  denominator clearing has not supplied an extra generic branch.
- Brink's theorem for a monic polynomial with independent linear and
  constant coefficients gives geometric Galois group \(S_d\).  Therefore
  every admissible weighted lift has geometric monodromy \(S_d\), and every
  \(S_d\), \(d\ge3\), is realized by a dimension-three Keller
  counterexample.
- An independent hostile audit passed.  Exact SymPy and PARI/GP checks cover
  the uniform formulas and finite rows used as regression tests.
- The priority record credits the public \(3\le d\le13\) computation in
  MathOverflow answer 513470 and its linked Note 19.  The candidate addition
  is only the all-degree, all-admissible-seed combination of Gallagher's
  construction with Brink's classical theorem.  It is unreviewed and does
  not change the total-degree floor.

## 2026-07-25T20:24:52Z — Quartic denominator frozen at fourteen leaves

- Replaced the drifting and overlapping 68-bucket proposal by fourteen
  disjoint inclusive leading leaves: one rank-one leaf and thirteen
  rank-two relative-closure tuples satisfying
  \[
  e+ab=4,\qquad b=\delta\nu.
  \]
- A blinded derivation, reconciliation, hostile replay, corrected re-audit,
  machine-readable manifest, and fail-closed checksums all pass.  The fixed
  boundary device has 45 first-nonzero coefficient strata in every leaf.
- This certifies F1/F2 and the denominator only.  It does not certify any
  exclusion.  A fresh hostile bridge audit is checking whether each older
  normal-form proof either covers the frozen coefficient partition or is
  genuinely division-free.
- The completed hostile bridge audit gives the fail-closed verdict
  \[
  0/14\text{ frozen-certified},\qquad
  7/14\text{ provisional legacy exclusions},\qquad
  7/14\text{ open}.
  \]
  No mathematical error was found in the seven old packages, but none yet
  connects its normal-form atlas to the frozen coefficient cover.  Those
  labels are now treated as algebraic evidence, not global progress, until
  explicit bridges are written.

## 2026-07-25T20:50:37Z — First frozen quartic leaf certified

- The post-freeze bridge for
  `Q2-E0-A1-B4-D2-N2` proves that every conic-double-cover leading term is
  linearly equivalent to
  \[
  (x^4,x^2y^2,y^4)
  \]
  without selecting a frozen coefficient as a denominator.
- A clean-room hostile reconstruction independently recovered the unique
  separable degree-two cover orbit, the symmetric-square target lift, the
  primitive affine triple, and the exact transfer of Keller and automorphism
  properties under the required source/target changes.
- The audit checked the codimension-two source basepoint explicitly.  It is
  not a component gcd or an omitted cover branch.  All nonempty frozen
  pivots `C00`--`C14` are covered and `C15`--`C44` are empty.
- The bridge verifier, independent SymPy reconstruction, existing exact
  SymPy lower calculation, independent PARI/GP lower audit, mutation wrapper,
  and unchanged frozen-manifest verifier all pass.
- The honest frozen count is now
  \[
  \boxed{1/14\text{ certified},\quad
         6/14\text{ provisional},\quad
         7/14\text{ open}.}
  \]
  This does not improve the universal total-degree floor above four.

## 2026-07-25T22:49:00Z — fixed-divisor \(e=2\) scope correction

- A post-freeze readiness audit found that the 10:48 “entire row closed”
  entry overclaimed the scope of the retained lower packages.
- The audited top theorem leaves a marked fixed quadratic member \(h\) and
  a unique double-line pencil member \(s=\ell^2\).  The lower packages
  silently specialized to \(h=s\); the top theorem does not force that
  equality.
- Three \(h\ne s\) marked-member orbits, each with mixed and triple cubic
  companions, remain: at least six lower branches or a uniform theorem are
  missing.  Exact top witnesses show the distinction is genuine.
- The frozen row `Q2-E2-A2-B1-D1-N1` therefore remains provisional.  No
  denominator changed and this is not a freeze violation; it is an internal
  coverage failure caught by the required post-freeze bridge audit.

## 2026-07-25T22:53:24Z — fixed-linear primitive cubic-pencil row certified

- The frozen row `Q2-E1-A3-B1-D1-N1` has the uniform leading form
  \(H_4=h(p,q,0)\), with \(h\) linear and \((p,q)\) a coprime minimal
  cubic pencil.
- The horizontal route and the complete unique-vertical route are now
  hostile-audited.  The latter has 47 disjoint internal atoms; its last
  \(s=0,W_0\ne0\) branch collapses already at \(E_6\) to the exact
  nonminimal binary boundary.
- A standalone hostile audit repaired the quadratic-component exit's
  provenance using Vistoli's unconditional degree-\(\le12\) plane theorem;
  the induced plane maps here have degree at most eight.
- The independent post-freeze bridge accounts for all 45 frozen pivots,
  expands the full row into 48 disjoint route atoms and 15 audited terminal
  groups, and rejects missing-route, overlap, provenance, semantic
  truncation, and optimized-Python mutations.
- The honest frozen count is now
  \[
  \boxed{3/14\text{ certified},\quad
         5/14\text{ provisional},\quad
         6/14\text{ open}.}
  \]
  This is a candidate novel structural row theorem.  It does not yet raise
  the universal total-degree floor above four.

## 2026-07-25T23:00:00Z — amended program adopted

- The active goal is now explicitly split into Objective A (a numerical
  total-degree table entry) and Objective B (a novel citable structural
  theorem).  The certified fixed-linear row is banked under Objective B;
  the total-degree floor remains four.
- Quartic progress will be reported only against the immutable denominator
  of fourteen inclusive rows.  Any new internal case is a coverage failure,
  not an increase in the denominator.
- The false promotion attempt on the \(e=2\) row confirms that this audit
  discipline is substantive: it exposed six precise marked-member branches
  before publication.
- The next highest-information experiment is the exact \(E_7/E_6\) solve
  on those six branches, run in parallel with an independent reconstruction
  of their marked-member orbit taxonomy.
- Track B's regular-action obstruction, all-\(d\) symmetric realization,
  and degree-\(\le10\) realizability table remain banked.  Tao's affine
  miracle is removed from the active allocation.

## 2026-07-25T23:08:00Z — second \(e=2\) freeze failure

- The attempted six-branch denominator was not exhaustive.  A pencil shear
  changes the chosen generator but does not normalize the marked
  leading-form data and the cubic companion simultaneously.
- The exact top-identity point
  \[
  h=yz,\quad s=x^2,\quad
  H_4=(h^2,hs,0),\quad G=x(h+s)
  \]
  is not equivalent to either pure companion slice: \(G/x=x^2+yz\) has
  rank three, whereas \(h\) and \(s\) have ranks two and one.
- The existing six \(E_7/E_6\) computations remain valid coordinate
  slices, and all six survive through \(E_6\); they are not a complete
  taxonomy and will not be counted.
- Under the freeze protocol, lower-identity work on this row is halted
  until an independent reconstruction freezes the full stabilizer quotient
  of the marked pencil and the projective companion.  No quartic
  certification count changes.

## 2026-07-25T23:28:00Z — corrected \(e=2\) internal taxonomy frozen

- Two independent reconstructions agree on exactly three marked-pair types.
  The outer two have three nonzero companion orbits; the smooth secant
  marked pair has a pointwise-fixed \(\mathbb P^1\) companion modulus.
- The stable parameterized denominator is \(4+5+4=13\) strata after the
  zero companions are included.  Its nonzero orbit-space shorthand is
  \(3+\mathbb P^1+3\).
- The second hostile audit verified the coordinate change
  \(\theta=1/(1+\tau)\), all \(0,-1,\infty\) boundaries, and rejected four
  semantic mutations.  The version-one frozen file is pinned at SHA-256
  `27e5a4f894ef523156abea389f89c2d4481d58d243c756b70386fdea10e9e01f`.
- Separately, exact SymPy and PARI calculations show that every value of
  the middle modulus survives through \(E_6\).  This is not an exclusion.
- The next authorized high-information experiment is the homogeneous
  \([u:v]\) uniform \(E_5\) compatibility ideal, with the frozen boundary
  divisor \(uv(u+v)=0\) handled explicitly.

## 2026-07-26T00:31:14Z — fixed-quadratic primitive-pencil row certified

- The uniform finite chart excludes every nonzero middle-family parameter,
  including the `CT` boundary at \(k=-1\).  Six fresh endpoint solves cover
  \(k=0,\infty\) in all three marked-pair types.  One rank-one smooth
  endpoint has a genuine invertible survivor through \(E_5\) and closes
  only at \(E_4\).
- Complete raw \(E_7\) quotients and exhaustive \(E_6/E_5\) solves exclude
  the two discrete `CO` orbits.  The primary exact aggregate and its
  independent PARI endpoint/uniform reconstructions pass.
- A clean-room hostile auditor, barred from the candidate bridge and the
  root `CO`/endpoint verifiers, independently reconstructed both `CO`
  quotients and lower exits with a dependency-free sparse-polynomial
  engine.
- The auditor found two scope/coverage defects in the release draft before
  promotion: zero companions give automorphism exits rather than blanket
  determinant contradictions, and frozen pivots `C30`--`C44` are empty in
  the rank-two row rather than entering the intrinsic-minor router.  Both
  were corrected and encoded as hard guards.
- The complete row aggregate ends with
  `Q2_E2_A2_B1_D1_N1_FULL_ROW_STRICT_PASS_4D95A1`; the clean-room bridge
  ends with `AUDIT_BRIDGE_Q2_E2_STRICT_PASS_D9347B`.
- The honest frozen count is now
  \[
  \boxed{4/14\text{ certified},\quad
         4/14\text{ provisional},\quad
         6/14\text{ open}.}
  \]
  The certified universal total-degree floor remains four.

## 2026-07-26T00:32:00Z — next-row readiness result banked

- A fresh readiness audit, recorded at 00:25:06Z, of
  `Q2-E2-A1-B2-D1-N2` derives nine stable
  internal strata before reading the existing status labels: three
  covered, three provisional, and three open.
- The exact-\(\delta=2\) incidence atlas has eighteen chart families.
  Existing artifacts provisionally cover all three \(\{2,0\}\) families
  and fourteen of fifteen \(\{1,1\}\) families.
- The row is not close to promotion: \(\delta=3,4\) have no incidence
  atlas or lower analysis, and the provisional packages lack hostile
  replays and a 45-pivot bridge.
- The highest-information next experiment is a saturation-safe primary
  decomposition of the universal \(\deg\gcd(\alpha,\beta,\gamma)\ge3\)
  locus, separating the \(\delta=3,\delta=4\), and power-fibre components.

## 2026-07-26T01:31:00Z — high-incidence denominator certified

- The fixed-quadratic line-double-cover row now has a canonical fine
  denominator for its previously untouched high-gcd strata:
  \[
  19\text{ exact-}\delta=3+
  6\text{ exact-}\delta=4+
  1\text{ dependent power fibre}.
  \]
- The primary calculation froze independently at \(17+6+1\).  The
  blinded reconstruction both refined two residual-torus endpoint unions
  and caught two real primary defects: an overlapping doubled-nonbranch
  exact open and an invalid reciprocal quotient that deleted the
  \(z=-1/5\) exact-\(\delta=3\) orbit.
- Reconciliation adopts the clean-room \(19+6+1\) ledger, supplies an
  exact ID migration map, and assigns stable IDs to all twelve retained
  pivots and twenty-four exit arrows.  The aggregate strict replay passes.
- No Keller exclusion follows yet.  The frozen global status is still
  \(4/14\) certified, \(4/14\) provisional, \(6/14\) open, and the
  certified total-degree floor remains four.

## 2026-07-26T02:11:00Z — first canonical high-incidence exclusion candidate

- The isolated squarefree \(\kappa=16\) family `D4-SF-11CC` now has a
  complete candidate lower-identity exclusion.
- A first restricted solve was deliberately withheld after it omitted
  arbitrary binary lower summands.  The full recomputation retained those
  summands and exposed an additional pivot factor
  \(m^2-4mn+n^2\).
- Fresh generic, conic-boundary, and zero-contact charts now close at
  \(E_5,E_5,E_4\), respectively.  Exact SymPy and independently rebuilt
  PARI/GP implementations pass.
- The candidate remains provisional until hostile reconstruction.  It
  changes neither the frozen \(4/14,4/14,6/14\) global count nor the
  degree floor four.

## 2026-07-26T04:36:36Z — three high-incidence families certified; `D4-DN-3` rebuilt

- Independent clean-room hostile reconstructions passed for
  `D4-SF-11CC` and `D4-SF-21C`, covering orbit normalization, the full
  contact loci, every generic and rank-drop chart, the lower
  obstructions, the zero-contact collapses, and Moh's unconditional
  degree-\(<100\) plane exits.
- A third complete family exclusion, `D4-DN-1CC`, was derived with
  independent SymPy/PARI checks and then reconstructed by a hostile
  auditor.  Its full contact locus is one affine line; the nonzero chart
  has obstruction \(16\kappa^4/135\), and the origin becomes a binary
  triangular lift.
- The earlier `D4-DN-3` zero-binary slice was explicitly demoted after a
  scope audit found eleven omitted lower coefficients.  A fresh
  all-18-variable elimination now proves that the actual complete
  \(E_6\) contact locus is exactly two conjugate affine planes.  A
  four-chart rank atlas covers their interiors, intersection, and
  origin.  This is a denominator theorem, not yet an exclusion.
- The fine high-incidence status is now \(3/26\) certified family-level
  exclusions.  The parent fixed-quadratic row remains open, so the frozen
  global count remains \(4/14\) certified, \(4/14\) provisional,
  \(6/14\) open, and the universal total-degree floor remains four.

## 2026-07-26T04:53:56Z — fourth high-incidence family certified

- The isolated exact-\(\delta=4\), \(\kappa=16/5\) family
  `D4-SF-20CC` is excluded.  Its normalized representative lies over
  \(\mathbb Q(i)\).
- A primary exact SymPy derivation and a clean-room PARI/GP reconstruction
  independently recover the complete contact line while retaining all 18
  lower variables.  The nonzero line dies at \(E_5\); the origin reaches
  two independent \(E_4\) squares and becomes a binary triangular lift.
- The combined fail-closed wrapper ends with
  `D4_SF_20CC_FULL_STRICT_PASS`.
- The fine count is now \(4/26\) certified family-level exclusions.  The
  containing row and the global \(4/14,4/14,6/14\) denominator do not
  change, so the universal degree floor remains four.

## 2026-07-26T05:40:00Z — fifth high-incidence family certified

- Frozen family `D4-DN-3`, with
  \(h=(p+q)^2\) and \(R=(p+q)^3\), is fully excluded.
- Its complete \(E_6\) contact locus is two conjugate affine planes.  The
  two transverse charts fail at \(E_5\); the punctured intersection forces
  \(\det L=0\); and the origin collapses to an unconditional Moh
  triangular exit.
- Independent clean-room SymPy and direct PARI/GP implementations cover
  every chart and required pivot boundary.  The aggregate verifier ends
  with `D4_DN3_FULL_FAMILY_EXCLUSION_STRICT_PASS`.
- This moves only the frozen fine denominator to \(5/26\).  The global
  quartic status remains \(4/14\) certified, \(4/14\) provisional,
  \(6/14\) open, and the universal degree floor remains four.
- Work began immediately on `D4-DN-2C`, the sole remaining isolated
  exact-\(\delta=4\) family.  Its complete \(E_7/E_6\) contact atlas is
  already frozen as two conjugate planes with ranks \(7,7,6,5\); lower
  descent is active and no exclusion is yet claimed.

## 2026-07-26T07:25:07Z — exact-\(\delta=4\) structural theorem certified

- The final family `D4-DN-2C` is excluded with arbitrary quadratic and
  cubic lower terms retained.  Primary SymPy and direct PARI/GP
  reconstructions independently recover its full \(E_7\) kernel, the two
  \(E_6\) contact planes, all four rank charts, and the complete
  \(E_5/E_4/E_3\) descent.
- The canonical \(19+6+1\) denominator proves that the exact-\(\delta=4\)
  stratum is precisely the six now-excluded families.  The dynamic aggregate
  and a separate hostile assembly wrapper both pass; seven mutations of the
  canonical bridge are rejected.
- Therefore no quartic Keller counterexample in the frozen binary
  fixed-quadratic line-double-cover locus has
  \(\deg\gcd(J(Q,R),-J(P,R),J(P,Q))=4\).
- This is a certified structural theorem and moves the fine denominator to
  \(6/26\).  It does **not** close the containing global row, so the honest
  global count remains \(4/14\) certified, \(4/14\) provisional,
  \(6/14\) open and the universal total-degree floor remains four.
- Independent and hostile audits of the exceptional power fibre began
  immediately.

## 2026-07-26T08:09:09Z — cube-component exit certified

- Proved an elementary coordinate theorem over every algebraically
  closed field of characteristic zero:
  \[
  \nabla(C+\ell^3+Q_2+L_1)\ne0
  \Longrightarrow C+\ell^3+Q_2+L_1
  \text{ is a coordinate}.
  \]
  A completing coordinate automorphism and its inverse have degree at
  most three.  The division-safe proof exhausts the ranks \(2,1,0\) of
  the quadratic block transverse to \(\ell\).
- Two independent hostile audits reconstructed the algebra and the
  geometric implication.  A dependency-free exact suite and an
  independent PARI/GP suite both pass, including required-failure
  mutations.  The geometry audit repaired the shorthand at the final
  step: Ax--Grothendieck gives surjectivity, while injective étale gives
  an open immersion, hence an isomorphism.
- If a complex Keller map of degree \(d\) has this shape as any nonzero
  target-linear combination of its components, it is an automorphism
  for \(d\le35\), using the plane safe range \(<108\) from
  arXiv:2204.14178.  The conservative Moh fallback is \(d\le33\).
  No plane Jacobian-Conjecture assumption is used.
- The exact bridge closes `PF-BRANCH-FOURTH-THIRD`, `D3-BB-30`, and
  `D3-OB-300`, reproves `D4-DN-3`, and closes only the retained \(z=3\)
  pivot inside `D3-SF-20C`.  Thus the fine denominator moves from
  \(6/26\) to \(9/26\); the containing row remains open.
- The global quartic status remains \(4/14\) certified,
  \(4/14\) provisional, \(6/14\) open.  The certified universal
  total-degree floor remains four.  No exact prior-art collision was
  located, but worldwide novelty is unresolved and no novelty claim is
  made.

## 2026-07-26T09:05:00Z — two provisional exact-\(\delta=3\) descents

- For frozen family `D3-BB-21`,
  \(h=pq,\ R=p^2q\), the complete \(E_7\) syzygy has
  \[
  T_r=ap+bq+cr,\quad
  U_r=\frac85pT_r-\frac15kp^2,\quad
  V_r=kq^2.
  \]
  With all eleven binary integration constants retained, \(E_6\)
  forces \(c=b=0\),
  \(12a^2-8ak+3k^2=0\),
  \(v_0(3a-k)=0\), and \(u_3(2k-a)=0\).
  On every nonzero conic point the raw lower-independent coefficient is
  \[
  [p^2qr^2]E_5=\frac25ak(8a-k)\ne0.
  \]
  At the origin, \(E_6\) leaves
  \(A_r=\frac85\ell_{33}p,\ B_r=0\).  The two
  \(\ell_{33}\)-charts exit to unconditional bounded-degree plane
  automorphisms.  This is a full-family exclusion candidate, not yet
  certified.
- A separate root derivation provisionally closes
  `D3-BS-N2-Z`, \(h=p^2,\ R=p^2q\).  Its complete \(E_7\)
  parameterization is
  \[
  U_r=-2kp^2,\quad
  V_r=2q(ap+bq+cr)+kq^2,\quad
  T_r=ap+bq+cr.
  \]
  The \(E_6/E_5\) identities first force
  \(c=0,\ b+k=0,\ a^2b=0,\ bu_2+6au_3=0\).
  Besides the origin, source scaling of \(r\) gives two charts:
  \(a=1,b=k=0,u_3=0\), and
  \(a=0,b=1,k=-1,u_2=0\).
  In the first chart \(E_5/E_4\) forces \(v_3=0\) and then
  \(\det L=0\).  In the second chart, the \(u_3\ne0\) branch
  forces the first and third columns of \(L\) to be proportional;
  for \(u_3=0\), putting \(d=t_1-v_2\), the \(d\ne0\) branch has
  \([q^2r]E_3=12d^3\), while the \(d=0\) branch has an \(E_3\)
  square forcing a factor of \(\det L\) to vanish.  Its origin has
  \(A_r=0,\ B_r=2\ell_{33}q\) and the same plane exits.
  This second candidate has not yet received an independent
  reconstruction and is not certified.
- If both candidates survive the required independent audits, the frozen
  fine count will move from \(9/26\) to \(11/26\).  Neither changes the
  global \(4/14,4/14,6/14\) status or the total-degree floor four.

## 2026-07-26T09:43:40Z — two fine families and one global row certified

- `D3-BB-21` survived a dependency-free sparse-\(\mathbb Q\) hostile
  reconstruction after two completeness repairs: the zero \(r^2\)
  \(E_7\) kernel and explicit \(E_9/E_8\) replay.  Its strict terminal
  marker is `D3_BB21_HOSTILE_RELEASE_AUDIT_PASS`.
- `D3-BS-N2-Z` survived a fresh direct PARI/GP reconstruction of the
  complete tangent space, both nonzero charts, every lower boundary, and
  the origin.  Its fail-closed wrapper caught a real GP parse-error
  transcript that also printed a success marker; after repair the marker
  is `D3_BS_N2_Z_HOSTILE_STRICT_PASS`.
- These two results move the frozen high-incidence fine count from
  \(9/26\) to \(11/26\).  They do not close the fixed-quadratic parent
  row.
- Independently, the post-freeze bridge for
  `Q2-E0-A2-B2-D2-N1` was derived blind and passed.  The auditor then
  found that the legacy lower scripts checked displayed solution families
  but not their exhaustiveness, and repaired that gap with exact ranks,
  kernels, cokernels, compatibility ideals, and full-solution checks.
- The global frozen quartic score is now
  \[
  5/14\text{ certified},\qquad3/14\text{ provisional},\qquad
  6/14\text{ open}.
  \]
  The universal total-degree floor remains four; no numerical table rung
  is closed.

## 2026-07-26T09:45:00Z — fixed-conic row held fail-closed

- A blind bridge audit independently certified the uniform leading form
  \(LX+H_2+H_3+h(x^2,xy,y^2)\), the `C00`--`C14` routing, and the
  emptiness of `C15`--`C44`.
- It then found the first retained-evidence gap in the legacy binary
  proof: equations (7)--(9) are replayed only after setting the arbitrary
  binary cubic \(V\) to zero and choosing one special \(H_2\).  Neither
  legacy CAS script proves that those \(E_6\) factors are necessary on
  the full \(12+18\)-coefficient lower solution space.
- The row stays provisional.  The smallest repair is now fixed: solve the
  full \(E_7\) system and certify the universal \(E_6\) compatibility and
  tangent-orbit list without generic-rank division.

## 2026-07-26T10:02:40Z — rational-plane-cubic row certified

- A clean-room post-freeze derivation recovered the intrinsic form
  \(H_4=\ell M B_\tau(p,q)\), where \(\tau\) is nodal or cuspidal, and
  the exhaustive aligned/transverse incidence split for the fixed line.
- Every nonempty frozen coefficient pivot lies in `C00`--`C14` and routes
  by explicit division-free coefficient polynomials.  `C15`--`C44` are
  empty because each target component of the leading map is nonzero.
- All four SymPy/PARI proof pairs passed.  The audit found one retained
  provenance gap in the transverse nodal branch and repaired it from a
  general 30-coefficient \(H_3\), general 18-coefficient \(H_2\), and
  arbitrary nine-entry linear part.  The exact ranks are \(24,16,9\);
  the terminal \(E_5\) square was reproduced.
- A separate lower-term scope audit reached the same verdict.  The strict
  wrapper passed three deliberate mutations and the optimized-Python
  guard with marker `Q2_E1_A1_B3_D3_N1_STRICT_PASS_V1`.
- The frozen global score is now
  \[
  6/14\text{ certified},\qquad2/14\text{ provisional},\qquad
  6/14\text{ open}.
  \]
  The universal total-degree floor remains four; no numerical table rung
  is closed.

## 2026-07-26T10:15:00Z — disputed fixed-conic top bridge repaired

- Two independent exact calculations, one in SymPy and one rebuilt in
  PARI/GP, start with the complete degree-eight cubic normal, all twelve
  binary-cubic coefficients, all eighteen quadratic coefficients, and an
  arbitrary nine-entry linear part.
- In both binary divisor types \(h=pq\) and \(h=p^2\), the degree-seven
  matrix in the quadratic coefficients has constant rank seven and an
  eleven-parameter affine fibre.  The PARI constant pivot determinant is
  \(-2^{19}\), so no parameter-dependent rank division is hidden.
- On the full fibres, the universal degree-six \(r^2\) coefficients are
  exactly
  \[
  12p^2q^2(a-d)^2(a+d),\qquad
  24dp^2(cp+(d-a)q)^2.
  \]
  Their radicals recover precisely the legacy tangent-orbit list,
  including all zero and rank-jump intersections.  Polynomial sections
  certify equality of the tangent-elimination ideals.
- This repairs the precise gap found at equations (7)--(9), but does not
  yet certify the global row: the later branch families (13)--(36) still
  must be rederived as complete descendants of these full fibres.  The
  fixed-conic row therefore remains provisional and the global score
  stays \(6/14,2/14,6/14\).

## 2026-07-26T10:26:30Z — quadratic-pencil line-double-cover row certified

- A blinded post-freeze reconstruction classified the primitive pencils of
  ternary quadrics into five symmetric-pencil charts, with all singular,
  gcd, rank-drop, and canonical-degree-drop boundaries routed back into
  the frozen taxonomy.
- The exact first-integral maps \(D:S_2\to S_3\) have
  rank/kernel/cokernel \(4/2/6\) on all five charts.  The maps
  \(D:S_3\to S_4\) have \(10/0/5\) on the three no-double-line charts and
  \(8/2/7\) on the two unique-double-line charts.
- A polynomial convolution formula routes every original coefficient point
  to `C00`--`C44` without dividing by a normalization minor.  SymPy and a
  dependency-free rational RREF reconstruction agree.
- Every primary and hostile terminal package for the two surviving pencil
  charts, including infinity, resonance, marked, and unmarked boundaries,
  replayed successfully.  The strict terminal is
  `PASS: strict post-freeze Q2-E0-A2-B2-D1-N2 bridge and full legacy replay`.
- The global frozen score is now
  \[
  7/14\text{ certified},\qquad1/14\text{ provisional},\qquad
  6/14\text{ open}.
  \]
  The universal degree floor remains four.
