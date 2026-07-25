# Research log: fixed-linear primitive cubic-pencil row

This folder records the horizontal-locus theorem for the taxonomy row
\[
(e,a,b,\delta,\nu)=(1,3,1,1,1),\qquad H_4=h(p,q,0).
\]
The vertical locus remains a separate active problem.

## 2026-07-25T05:35Z — program opened

- Isolated the row from `WORKING_QUARTIC_CURVE_TAXONOMY.md`.
- Fixed notation \(P=hp\), \(Q=hq\), where \(h\) is linear and \(p,q\)
  are coprime minimal cubic pencil generators.
- The immediate top Keller identities are
  \[
  E_8=\operatorname{Jac}(P,Q,(H_3)_3)=0
  \]
  and, after \((H_3)_3=0\),
  \[
  E_7=\operatorname{Jac}(P,Q,(H_2)_3)=0.
  \]
- The candidate obstruction is the valuation of the degree-zero invariant
  \(G^4/P^d\) along \(h=0\).  If \(h\) is not a component of any cubic
  pencil member, every rational function of \(q/p\) has valuation zero
  there, while
  \[
  v_h(G^4/P^d)=4v_h(G)-d.
  \]
  This cannot vanish for \(d=2,3\).

## 2026-07-25T05:45Z — vertical escape located

- The sole failure of the \(h\)-valuation argument is the vertical locus
  \[
  h\mid \alpha p+\beta q
  \quad\text{for some }[\alpha:\beta]\in\mathbb P^1.
  \]
  Equivalently, the restrictions of \(p,q\) to \(h=0\) are proportional.
- Coprimality makes the vertical member unique.  A pencil-coordinate
  change puts it in the form
  \[
  p=h^m r_{3-m},\qquad 1\le m\le3,\qquad h\nmid q r_{3-m}.
  \]
- Two primitive examples show that this is a genuine exceptional locus
  for the top identities, not merely a defect of the proof:
  \[
  h=z,\quad p=zx^2,\quad q=x^3+y^3
  \]
  has \(hp=(zx)^2\), so \(G_2=zx\) is a nonzero degree-two first
  integral; and
  \[
  h=z,\quad p=z^3,\quad q=x^3+y^3
  \]
  has \(hp=z^4\), so \(G_3=z^3\) is a nonzero degree-three first
  integral.  Their generic cubic fibres are geometrically integral, so
  these examples do not evade the minimal-pencil hypothesis.

## 2026-07-25T05:55Z — proof architecture fixed

- Algebraicity: the vanishing ternary Jacobian makes a homogeneous
  \(G\) algebraic over \(\mathbb C(P,Q)\).
- Scaling descent: \(G^4/P^d\) has degree zero.  Since \(P\) is a
  transcendental scaling coordinate over
  \(\mathbb C(\mathbb P^2)\), algebraicity over
  \(\mathbb C(q/p,P)\) descends to algebraicity over
  \(\mathbb C(q/p)\).
- Relative closure: minimality of the cubic pair rules out a proper
  algebraic intermediate generator.  Otherwise generalized Lüroth and
  homogeneity would express \(p/q\) as a degree-three rational function
  of a linear pencil, contradicting minimality.
- Exit: once both normal components vanish, the third component of the
  full map is linear.  Normalizing it to a source coordinate reduces
  each fibre to a plane Keller map of degree at most four.

## 2026-07-25T06:04Z — exact checks and source sweep completed

- The SymPy check passed.  It verifies the universal derivation identities,
  formal \(E_8/E_7\) matrix weights, rank-two restriction and zero
  degree-two/degree-three kernels for a horizontal Hesse pencil, generic
  smoothness, and the two vertical exceptions.
- The independent PARI/GP check passed.  It reconstructs the weighted
  determinant coefficients and kernel ranks with exact rational arithmetic.
- A source-specific priority sweep found de Bondt's minimal-pair
  factorization as the closest structural input, but no checked source
  stating the horizontal valuation theorem or its sharp vertical boundary.
- The provisional theorem and all supporting work remain confined to this
  folder.  No global documentation was modified and nothing was promoted.

## 2026-07-25T06:15Z — hostile audit passed

- An independent audit reconstructed the minimality/relative-closure
  implication, the degree-zero scaling descent, the prime-divisor
  valuation, both determinant weights, and the plane-fibre exit.
- The audit found no theorem-breaking error or omitted horizontal case.
- It corrected the exceptional locus from “codimension-one” to the
  complete escape visible at the codimension-one divisor \(h=0\): for
  fixed \(h\), the rank-one restriction locus itself has codimension
  three.
- The SymPy verifier now refuses optimized execution, and a strict GP
  wrapper passed injected-failure tests.
- A dependency-free finite-field reconstruction passed 64 horizontal
  kernel samples, 128 determinant-polarization samples, and the two
  vertical witnesses.
- Full verdict and artifacts are in `audit_hostile/REPORT.md`.

## 2026-07-25T06:18:12Z — scoped theorem promoted

- Re-ran the supplied SymPy check, strict PARI/GP reconstruction,
  dependency-free finite-field audit, and all runner fault injections.
- Promoted exactly the horizontal locus.  The vertical rank-one restriction
  locus remains open; its displayed witnesses are not Keller maps.
- Updated the global taxonomy and verification records without changing
  the universal total-degree floor \(4\).
