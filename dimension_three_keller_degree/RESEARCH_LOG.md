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
