# Research log: hostile audit of the quadratic-component exit

## 2026-07-25T22:27:36Z — independent reconstruction started

- Created a dedicated audit folder.  The aggregate
  `rung2_degree_bound/VERIFICATION.md` remains unread.
- Scope fixed to the claim that a Keller map
  \(F:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}\) of total
  degree at most four is an automorphism if a nonzero target-linear
  combination of its components has degree at most two.
- Independently identified the proposed chain to audit:
  target normalization; quadratic-submersion coordinate lemma; conjugation
  to \((G_1,G_2,z)\); restriction to plane fibres of degree at most eight;
  an unconditional bounded-degree plane theorem; fibrewise injectivity;
  Ax--Grothendieck.
- No plane Jacobian-conjecture assumption is permissible.  Exact primary
  literature, theorem/page, field, and degree hypotheses will be checked
  before assigning a verdict.
- Best-guess completion toward this local audit: **10%**.

## 2026-07-25T22:35:23Z — clean reconstruction and primary-source checkpoint

- Completed the reconstruction before reading the aggregate verification.
  The complete chain is:
  1. an invertible target-linear change makes the low-degree combination the
     third component;
  2. invertibility of the Keller Jacobian makes its gradient nowhere zero;
  3. the kernel of the constant symmetric Hessian supplies a source direction
     in which the polynomial is affine-linear with nonzero coefficient;
  4. this gives a polynomial coordinate \(T=(Y_1,Y_2,f)\), with both \(T\)
     and \(T^{-1}\) of degree at most two;
  5. \(G=F\circ T^{-1}=(G_1,G_2,z)\) has degree at most \(8\), and every
     \(z=c\) restriction is a plane Keller map of degree at most \(8\);
  6. the published degree-\(12\) plane theorem makes each restriction an
     automorphism, hence \(G\) is injective;
  7. Ax--Grothendieck plus étaleness makes \(G\), and therefore \(F\), an
     isomorphism.
- Stress-tested the Hessian step in arbitrary rank, including the linear case
  \(H=0\).  For symmetric \(H\),
  \(\operatorname{im}H=(\ker H)^\perp\), so absence of a critical point gives
  \(v\in\ker H\) with \(b^Tv\ne0\).  Completing \(v\) to a linear basis is the
  precise source-coordinate change suppressed by the informal notation.
- Checked the fibre Jacobian directly:
  \[
  JG=
  \begin{pmatrix}
  G_{1x}&G_{1y}&G_{1z}\\
  G_{2x}&G_{2y}&G_{2z}\\
  0&0&1
  \end{pmatrix},
  \qquad
  \det JG_c=\det JG\in\mathbb C^\times .
  \]
  Specialization \(z=c\) cannot increase total degree, so
  \(\deg G_c\le8\).
- Inspected Angelo Vistoli's primary journal PDF directly.  On journal p. 79
  he fixes an algebraically closed field \(k\) of characteristic zero and
  defines the degree of a polynomial map as the maximum component degree.  On
  journal p. 80 he states:
  - an étale polynomial map \(\mathbb A^n\to\mathbb A^n\) that is injective
    is surjective (citing Bass--Connell--Wright);
  - an étale polynomial map \(\mathbb A^2\to\mathbb A^2\) of degree at most
    \(12\) is an isomorphism (citing Moh), adding that Moh actually proves the
    result through degree \(100\).
  Thus the only planar input needed here is an explicit unconditional
  bounded-degree theorem, not the plane Jacobian Conjecture.
- Only after the reconstruction and source check, read the relevant
  quadratic-component passages of the aggregate `VERIFICATION.md`.  They
  agree on the degree-\(8\) bound and contain no additional premise needed by
  this proof.
- No mathematical gap found.  Four presentation improvements will be
  recorded: correct the pre-/post-target-change Jacobian notation; cite
  Vistoli's exact degree-\(12\) formulation rather than merely saying a
  counterexample has degree “at least \(100\)”; name the first two source
  basis coordinates explicitly; and state the
  bijective-étale-to-isomorphism bridge.
- Best-guess completion toward this local audit: **70%**.

## 2026-07-25T22:41:32Z — audit completed

- Wrote the standalone hostile audit `REPORT.md` with a **PASS** verdict,
  the full reconstructed proof, a hypothesis ledger, circularity and scope
  checks, exact journal-page citations, and the four non-blocking exposition
  improvements.
- Added `verify_quadratic_component_exit_exact.py`.  It checks the generic
  quadratic coordinate and inverse, Hessian-basis identities, both Jacobian
  determinants, the exhaustive degree-\(4\) monomial pullback bound, and the
  fibre determinant identity over exact symbolic coefficient rings.
- Ran:
  ```text
  /usr/bin/python3 verify_quadratic_component_exit_exact.py
  ```
  with terminal output:
  ```text
  PASS: exact quadratic-coordinate, degree, and fibre identities verified
  ```
- Re-ran the checker with Python optimization enabled to ensure its custom
  fail-closed assertions are not disabled.  It passed.
- Ran the repository whitespace/error check on the dedicated audit folder;
  no errors were reported.
- No status ledger, parent proof, or aggregate verification was edited.  No
  commit or push was made.
- Final completion for this local audit: **100%**.
