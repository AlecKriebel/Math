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
