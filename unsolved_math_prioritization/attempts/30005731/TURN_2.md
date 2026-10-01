# Substantive turn 2: a budget-preserving outward variation

**Conditional partial theorem, unreviewed.** Date: 2026-10-01. This turn studies a genuine length minimization problem without assuming local convexity or slack in the construction constraint. It proves a shape condition in the radially visible, strictly outward prefix regime. It does not identify this prefix objective with the OWR's unspecified global optimizer or control the arrival field after a full winding.

## Precise reduced problem

Fix sigma>1 and 0<Theta<2*pi. Consider C2 radial graphs

    z(theta) = r(theta)(cos(theta), sin(theta)),  0<=theta<=Theta,

with r(0)=1, r'(theta)>0, fixed terminal radius, and construction budget

    L(theta) = integral_0^theta sqrt(r(t)^2+r'(t)^2) dt,
    G(theta) = sigma*(r(theta)-1)-L(theta) >= 0.

The objective is L(Theta), with both endpoints fixed. These curves are simple and each radial segment from the unit disk is unobstructed until the barrier endpoint. Thus the arrival-time trace is r-1, and the displayed budget constructs the prefix before that arrival. This is an actual admissible-prefix class, rather than the already-convex class AS used in the later source.

**Claim.** A local length minimizer in this class has nonnegative signed curvature everywhere in its open parameter interval. The conclusion does not require G>0 and therefore also covers arcs meeting the active budget constraint.

## Proof by a one-sided shape variation

Write

    F(r,p) = sqrt(r^2+p^2),
    P = F_p = r'/sqrt(r^2+r'^2),
    E = F_r - d/dtheta(F_p)
      = r*(r^2+2*r'^2-r*r'')/(r^2+r'^2)^(3/2).

Since r>0, the sign of E is exactly the sign of the curvature numerator of the polar curve. Suppose it is negative at an interior point. Continuity gives an open interval I compactly contained in (0,Theta) on which E<0. Choose a nonzero, nonnegative smooth bump eta with compact support in I, and put

    r_epsilon = r + epsilon*eta,  epsilon>=0.

For sufficiently small epsilon, strict radial monotonicity persists and E_epsilon remains negative on the compact support of eta. Simplicity, radial visibility and both endpoints persist. These facts do not use convexity.

At any theta, integration by parts gives the exact derivative with respect to epsilon:

    dL_epsilon(theta)/depsilon
      = P_epsilon(theta)*eta(theta)
        + integral_0^theta E_epsilon(t)*eta(t) dt.

There is no initial boundary term because eta vanishes near zero. Consequently

    dG_epsilon(theta)/depsilon
      = (sigma-P_epsilon(theta))*eta(theta)
        - integral_0^theta E_epsilon(t)*eta(t) dt >= 0.

Indeed |P_epsilon|<1<sigma, eta>=0, and the integrand E_epsilon*eta is nonpositive. This inequality holds at every prefix time, not merely at the endpoint or to first order at epsilon=0. Integrating it in epsilon proves G_epsilon(theta)>=G_0(theta)>=0 simultaneously for all theta. Active constraints cannot be violated by this perturbation.

At Theta the boundary term vanishes and

    dL_epsilon(Theta)/depsilon
       = integral_0^Theta E_epsilon(t)*eta(t) dt < 0.

Thus the perturbed prefix is feasible and strictly shorter, contradicting local optimality. This proves the claim.

For a regular C2 plane curve, nonnegative signed curvature gives an oriented locally convex arc after taking a sufficiently small tangent graph chart. Here regularity follows from r>0. No conclusion about corners or merely Lipschitz candidates is included in the theorem.

## What this closes and what it does not

Turn 1's smooth outward nonconvex prefix is therefore demonstrably nonoptimal for this fixed-endpoint prefix length problem: a negative-curvature neighborhood admits the variation above. The variation does more than the usual free-arc Euler equation: every construction margin improves, so a missing strict-slack assumption is not the obstruction in this visible regime.

The unresolved extension is geometric. After a barrier winds around the initial fire, its arrival trace need not be r-1. Modifying an earlier arc can change later shortest fire paths and all later budgets. The proof has not shown that a changed prefix can be spliced into an arbitrary confining spiral while preserving admissibility or its terminal-ray objective. It also assumes C2 regularity and strict outward radial motion; none is derived for general optimal spiral-like strategies. Arbitrary spatially weighted burned-area or barrier costs have different first variations and are outside this statement.

The source's separate outer-boundary convexification argument in Zizza's 2023 thesis, Lemma 6.0.3 and Remark 6.0.4 (pp. 106–107), is useful context. It concerns length minimization in an external-boundary/internal-barrier setting, under that chapter's assumptions including sigma<2. The remark explicitly does not extend its convexity conclusion to nonzero burned-area costs. That published-in-thesis argument is credited, and is not being silently promoted to a theorem about all spiral prefixes or the OWR target.

`turn_2_check.py` checks the Euler derivative, the curvature identity, and the exact prefix integration-by-parts identity algebraically. The continuous sign argument above, rather than any finite sample, proves the conditional theorem.

Substantive author turns: **2/5**. Estimated completion toward the original target: **10%**. The original broader-class automatic-convexity and A1 question remains unresolved. This partial awaits separate review.
