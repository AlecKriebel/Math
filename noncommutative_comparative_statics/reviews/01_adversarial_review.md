# Adversarial Review 01 — Initial “Recourse Geometry” Premise

**Verdict:** no-go as a claimed new branch in its initial form; conditional
go only after a sharper novelty target.

## Fatal dichotomy

Let \(B\) be an external parameter space, \(X\) an internal state space,
\(E=\{(b,x):F(b,x)=0\}\), and \(\pi:E\to B\).

1. **Static/global recourse.** If
   \(x^\*(b)=\arg\min_{x\in E_b}C(b,x)\) is unique and strongly regular, it is
   a local section. The state depends only on \(b\), so a closed loop returns
   to \(x^\*(b_0)\). Any claimed holonomy here is a definition error.
2. **Incremental recourse.** If a base velocity \(u\) is lifted by minimizing
   \(\tfrac12v^\top Mv\) subject to
   \(D_xF\,v+D_bF\,u=0\), then

   \[
   v^\*(u)=
   -M^{-1}A^\top(AM^{-1}A^\top)^{-1}Cu.
   \]

   This is the standard weighted-pseudoinverse horizontal lift. Its
   Lie-bracket defect is ordinary Ehresmann curvature and its loop drift is
   ordinary holonomy.

Moreover, allowing an arbitrary positive-definite cost is weakly predictive:
essentially any chosen Ehresmann connection can be made orthogonal by a
suitable metric.

## Principal collision zones

- Ehresmann connections and Riemannian submersions.
- Redundant inverse kinematics and pseudoinverse drift.
- Geometric mechanics and geometric phase.
- Parametric optimization, KKT sensitivity, and variational analysis.
- Moreau sweeping processes and rate-independent systems.
- Convex-body chasing and smoothed online optimization.
- Algorithmic recourse, including ordered and sequential recourse.
- Projected dynamics, differential variational inequalities, and nonsmooth
  mechanics.

Key leads supplied by the reviewer include:

- Shamir and Yomdin, “Repeatability of Redundant Manipulators: Mathematical
  Solution of the Problem,” *IEEE Transactions on Automatic Control* 33
  (1988), DOI `10.1109/9.14412`.
- Bay, “Geometry and Prediction of Drift-Free Trajectories for Redundant
  Machines Under Pseudoinverse Control” (1992), DOI
  `10.1177/027836499201100103`.
- Moreau, foundational sweeping-process paper (1977), DOI
  `10.1016/0022-0396(77)90085-7`.
- Stechlinski, Khan, and Barton, nonsmooth sensitivity of nonlinear programs,
  DOI `10.1137/17M1120385`.

## Required repairs to the program

The reviewer required:

1. an exact data object and morphisms;
2. explicit separation of static reset, incremental carry, and integrated
   path optimization;
3. coordinate/gauge invariance;
4. correct treatment of nonuniqueness, inequality constraints, singular
   fibers, and active-set changes;
5. a small-loop theorem with limited, accurate scope;
6. separate local-curvature and global-topology claims;
7. at least one result not immediate from connection, KKT, or sweeping theory;
8. a prior-art correspondence table and cross-domain falsifiable examples.

## Falsification tests retained for later checkpoints

- Static-section test: a unique reset optimizer has no loop residue.
- Standard-reduction test: translate the smooth theory into connection
  language and identify what, if anything, remains.
- Unit/gauge test.
- Small-loop \(\epsilon^2\) scaling test.
- Reversal and rate tests for the quasistatic connection sector.
- Discretization-refinement test.
- Flat-but-topologically-nontrivial test.
- One-dimensional hysteresis test.
- Active-set stress test.
- Held-out loop/order prediction test.
- Full-relaxation test: residual should vanish under complete reset.

## Disposition

Accepted. The project dropped “recourse geometry” as the field-level claim and
pivoted to noncommutative comparative statics, with ordinary recourse geometry
retained only as one reduction sector.

