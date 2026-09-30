# Elastic equilibrium uniqueness: source separation and a restricted multiplier criterion

Original Ball Problem8 remains unresolved by this package, 2/5. Independent review pending. No new general uniqueness or nonuniqueness theorem is claimed.

## 1. Exact physical and variational scope

J.M. Ball, *Some Open Problems in Elasticity* (2002), Section2.6, Problem8, printed p.17, asks whether sufficiently smooth equilibria are unique for pure-displacement problems in a homogeneous body homeomorphic to a ball when the stored energy is strictly polyconvex. Primary source: https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf .

Its setup in Section2.1 is a bounded domain Omega in R^3 and a deformation y:Omega->R^3, energy integral W(Dy), no body force in the simplified model, and prescribed trace on the entire boundary in the pure-displacement case. W is homogeneous (no x dependence), frame indifferent, finite on positive-determinant matrices, and extended to infinity when det<=0. The setup requires blow-up as det tends to zero from above and discusses invertibility to prevent interpenetration. Strict polyconvexity means a strictly convex representing function g of all minors: W(F)=g(F,cof F,det F), not merely rank-one convexity. Problem8's preceding discussion mentions favorable growth but does not specify one universal additional numerical growth exponent in the question itself.

Thus buckling with traction boundary conditions, annular/toroidal domains, cavitating discontinuous maps, or arbitrary noninjective boundary data are not automatically counterexamples to the intended physical question. Equilibrium means the Euler–Lagrange equation div DW(Dy)=0, or its weak form against zero-trace variations; it is not synonymous with global energy minimization.

## 2. Why the frequently cited Spadaro result does not by itself settle this scope

Spadaro, *Non-Uniqueness of Minimizers for Strictly Polyconvex Functionals*, Archive for Rational Mechanics and Analysis193 (2009),659–678, DOI https://doi.org/10.1007/s00205-008-0156-y , proves a negative result in a broader variational formulation. Theorem1 uses a two-dimensional disk mapping to R^2 with noninjective boundary values; its injective-boundary variant maps a two-dimensional disk into R^3. Both have analytic minimizers. The full preprint text was read through a mirror: https://paperzz.com/doc/8462194/15-2007---institut-f%C3%BCr-mathematik ; institutional publication metadata at https://iris.uniroma1.it/handle/11573/1117524 confirms the published article. We do not independently reconstruct the minimal-surface regularity or multiplicity proofs.

Most importantly, Ball's own subsequent article, https://people.maths.ox.ac.uk/~ball/Papers/Ball%20Udine%202009.pdf , printed p.10, explicitly discusses Spadaro and leaves the equidimensional n=2 or n=3 case with injective boundary values as an unestablished extension. This primary scope warning prevents promoting the known broader result to a resolution of the original physical problem. The retrieved evidence does not establish its current full resolution either. The imported dataset's language about general buckling and likely falsity is not a proof.

There is no demonstrated operation that adds a determinant blow-up barrier, changes the target dimension, or imposes injective boundary values while preserving the two analytic equilibria in that construction. We make none of those substitutions.

## 3. A restricted uniqueness certificate using the actual polyconvex representation

The following proposition is conditional and does not assert that arbitrary solutions meet its extra hypothesis. It retains the same pure-displacement boundary condition and can be applied to a material satisfying the physical assumptions, provided the stated representation and multiplier condition hold.

**Proposition.** Let Omega be a bounded connected smooth domain in R^3. Let g(F,C,d) be C1 and strictly convex on a convex open set containing the minor triples of two C2 deformations y,z on the closure of Omega, both with positive Jacobian determinant. Suppose W(F)=g(F,cof F,det F), y=z on the entire boundary, and both y,z are weak equilibria for W. Suppose there are the same constant matrix Q and scalar p such that, at every point of both deformations,

g_C(Dy,cof Dy,det Dy)=g_C(Dz,cof Dz,det Dz)=Q,
g_d(Dy,cof Dy,det Dy)=g_d(Dz,cof Dz,det Dz)=p.

Then y=z throughout Omega.

**Proof.** Write F=Dy, G=Dz and H=F-G=D(y-z). For any fixed constant Q and p, the functional integral [Q:cof Du+p det Du] is a sum of null Lagrangians. Its first variation along a zero-trace smooth field phi is zero:

integral [Q:Dcof(Du)[Dphi]+p cof(Du):Dphi] = 0.

For the determinant this is the Piola identity div(cof Du)=0 followed by integration by parts. Each entry of cof Du is a two-by-two minor, whose first variation is likewise a divergence because mixed derivatives commute. With zero boundary trace the boundary contribution vanishes. Equivalently every minor integral is fixed by the full boundary trace; differentiating that identity gives the formula. The identity is polynomial and can be used even if an interpolating variation were not orientation preserving.

The chain rule gives

DW(F):H = g_F(F,cof F,det F):H + Q:Dcof(F)[H] + p cof F:H,

and the analogous expression at G. Test both equilibrium equations with y-z (justified by smoothness and zero trace), subtract, and use the null-Lagrangian first-variation identity separately at y and z. This yields

integral [g_F(F,cof F,det F)-g_F(G,cof G,det G)]:H = 0.

Strict convexity of a differentiable g implies strictly monotone gradient: for distinct minor triples U,V, (Dg(U)-Dg(V)) dot (U-V)>0. The assumed common minor multipliers cancel the C and d contributions to this dot product, leaving exactly the preceding integrand. If F differs from G, the minor triples differ because they include F itself, so that integrand is positive; it is zero when F=G. Consequently F=G everywhere, by continuity and the integral identity. Connectedness implies y-z is constant, and the boundary trace makes that constant zero. QED.

The same conclusion holds under a strong-convexity bound with a quantitative nonnegative integral, but no strong-convexity assumption is needed here. Domain topology was not used; that does not remove the restrictive common-constant-multiplier hypothesis.

## 4. Why strict polyconvexity alone does not supply the missing estimate

The gradient monotonicity furnished by convex g is an inequality in the enlarged minor variables, involving g_F paired with F-G, g_C paired with cof F-cof G, and g_d paired with det F-det G. The equilibrium test instead pairs DW(F)-DW(G) with F-G. The nonlinear derivatives of cof and det make these different expressions. Variable minor multipliers cannot be pulled outside the null-Lagrangian identities, and they produce derivative terms under integration by parts. The common-constant assumption in Section3 is therefore a real restriction, not a consequence of strict polyconvexity.

For example, the determinant is not affine along general full-rank matrix segments; its second and third variation terms matter even though it is affine on rank-one lines. A finite-dimensional positivity check for the Hessian of g cannot be promoted to monotonicity of DW on all admissible gradients. Nor does uniqueness of an affine global minimizer by a null-Lagrangian/Jensen argument establish uniqueness among every stationary point with arbitrary boundary data.

The exact gap is either to control these nonlinear multiplier terms for the full physical class, or to construct two sufficiently smooth equidimensional positive-Jacobian equilibria with the same admissible full boundary values for one strictly polyconvex material satisfying the stated setup. Neither is accomplished here.

## 5. Verification boundary

Exact symbolic controls check cofactor and determinant first-variation formulas, the Piola identities for polynomial deformations, and the cancellation identity with constant Q,p. These controls verify algebraic ingredients only; the positivity and PDE testing argument is the written proof. They do not construct multiple equilibria, verify a general growth theorem, or independently certify Spadaro's analytic minimizers. Original status stays unsolved2/5.
