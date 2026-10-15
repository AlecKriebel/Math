# Substantive turn 1: admissibility does not imply local convexity

**Partial, unreviewed. No optimality or blocking counterexample is claimed.** Date: 2026-10-01. This first mathematical turn tests whether the broad single-barrier hypotheses alone force the missing shape condition. They do not, even for a smooth strictly admissible prefix with strictly increasing arrival time.

## Exact nonconvex admissible prefix

Take isotropic unit-speed fire with initial unit disk and construction speed sigma=3. For 0<=theta<=pi/2, set

    h(theta) = theta + sin(10 theta)/20,
    r(theta) = exp(h(theta)),
    zeta(theta) = r(theta)(cos(theta), sin(theta)).

Reparametrize this curve by arc length s starting at zero. It is smooth, simple, starts at (1,0), and remains outside the initial disk because

    h'(theta)=1+cos(10 theta)/2 >= 1/2.

Every radial segment from the initial disk to zeta(theta) meets this barrier only at its final point. Therefore the arrival-time trace is exactly

    u_Z(zeta(theta)) = r(theta)-1.

This can equivalently be computed as an infimum of paths approaching the endpoint from the unblocked side; it does not assume that a fire trajectory can cross the constructed wall. Euclidean distance gives the lower bound and the visible radial segment gives the matching upper bound. The arrival time is strictly increasing along the curve.

The length and radial derivatives satisfy

    ds/dtheta = r sqrt(1+h'^2),
    du/dtheta = r h',
    (ds/du)^2 = 1+1/h'^2 <= 5.

Integrating from theta=0 gives

    s(theta) <= sqrt(5) (r(theta)-1) < 3 (r(theta)-1)

for theta>0. Hence the barrier can be built in the displayed order at speed 3 before the fire can reach any new point: its construction time s/3 is strictly smaller than the unobstructed arrival time. This directly verifies dynamic admissibility, as well as the static prefix budget, without relying on delays created by an already built wall.

For a polar graph r=exp(h), the signed curvature numerator is

    det(zeta',zeta'') = r^2 (1+h'^2-h'').

At theta=pi/20 this factor is 7, while at theta=3pi/20 it is -3. Thus the smooth curve changes curvature sign and has an inflection between these points. It is not locally convex in the oriented sense used by the sources; the inflection also prevents a convex-graph description in a neighborhood of that point under either consistent orientation.

This is a finite admissible **prefix**, not a confining barrier and not a minimizer of either objective in the source audit. It refutes the shortcut “simplicity plus increasing arrival time plus admissibility already forces local convexity.” An actual optimality argument must use more than those hypotheses.

## The two initial-angle conditions have different elementary content

The prefix above starts with tangent direction proportional to (3/2,1), so it satisfies both displayed acute-angle conditions. It therefore isolates failure of convexity rather than exploiting the axis discrepancy.

Separately, if a curve starts at (1,0), stays outside the unit disk, and has a right derivative t at zero, then differentiating |zeta(s)|^2 >= 1 at s=0 gives t dot e1 >= 0. With the ordinary unsigned angle convention, this proves the later paper's horizontal e1 condition whenever that tangent exists, independently of optimality. Existence of the tangent is not automatic for an arbitrary Lipschitz curve and is not supplied by this argument.

Reflection across the horizontal axis preserves length, the isotropic initial fire, simplicity, arrival-time monotonicity and admissibility. It changes the sign of t dot e2. Thus the OWR's vertical e2 condition requires an orientation convention or an actual shape conclusion; it cannot be identified with the horizontal feasibility condition solely from the displayed inequalities. A reflected prefix is not a counterexample to an optimizer statement that has already fixed the counterclockwise convention.

## Consequence for the research route

The source's later convex-class parametrization cannot establish the desired automatic convexity by itself, and neither can bare feasibility. The next route must investigate a genuine local or global optimality comparison in a stated objective. The OWR's missing objective specification remains material; no weighted-cost statement or terminal-angle statement is being silently substituted for it.

`turn_1_check.py` verifies the symbolic curvature identity, its two exact signs, the initial tangent and the clock inequality factorization. These checks corroborate the analytic construction; they do not establish optimality.

Substantive author turns: **1/5**. Estimated completion toward the original target: **4%**. Original automatic-convexity/initial-angle question unresolved; this partial result awaits separate review.
