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
