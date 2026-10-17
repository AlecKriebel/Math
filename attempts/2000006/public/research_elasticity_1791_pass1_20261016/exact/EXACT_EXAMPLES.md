# Exact examples, thresholds, and stationarity checks

E-6322, pass 1, 2026-10-16. This report concerns the fixed density

W(F) = a|F|^6 + b|cof F|^3 + c(det F)^2 + d(det F)^(-2),

with arbitrary fixed a,b,c,d > 0 and det F > 0. All norms are Frobenius. The full frozen target was read before this work. The conclusions below do **not** resolve the global-minimizer question.

## Principal findings

1. Finite energy, even arbitrarily near the minimum energy for identity data, cannot alone force an essential positive Jacobian lower bound.
2. For each 0<=gamma<1/2, interior Jacobian degeneration is compatible with an admissible homeomorphism of class C^{2,gamma}. For each 0<=gamma<1, boundary-only degeneration is compatible with a smooth interior diffeomorphism of class C^{2,gamma} on the closed ball. These are families of examples, with the map allowed to depend on gamma.
3. The examples below with identity trace are provably **not** minimizers. The identity is the unique full-class minimizer for that trace. The radial examples also have an explicit strict annular descent variation.
4. Finite benchmark energy does not imply integrability of the ordinary first Piola stress DW(Dy). This obstructs unqualified additive Euler–Lagrange arguments.
5. Conditional regularity thresholds based only on the inverse-Jacobian integral are sharp within the displayed Hölder scales: C^{2,1/2} rules out interior zeros; C^{2,1} up to a smooth boundary rules out boundary zeros as well. No such regularity of full-class minimizers is established here.

## 1. Affine data: exact full-class minimization

Let Omega be a bounded smooth connected domain and prescribe y(x)=F0 x+v on its entire boundary, with det F0>0. For every y in the target admissible class, the null-Lagrangian identities give

average Dy = F0,
average cof Dy = cof F0,
average det Dy = det F0.

They hold for W^{1,6} maps with the prescribed trace; one can approximate y−(F0 x+v) in W^{1,6}_0 by smooth compactly supported maps and pass in the minors. Convexity of |F|^6, |H|^3 and h(J)=cJ^2+dJ^(−2) on J>0 gives

I(y) >= |Omega| W(F0).

The strictly convex a|F|^6 term forces Dy=F0 almost everywhere in every equality case, and the trace then fixes y=F0 x+v. Thus the affine map is the unique minimizer in the **entire** target class, with no injectivity restriction needed.

Consequently, every nonaffine identity-trace map in Sections 2–5 is a nonminimizing admissible example, never a counterexample to E-6322.

## 2. Isotropic radial degeneration: exact energy and strict descent

On B1 in R^3, set

y_alpha(x)=|x|^alpha x,  alpha>0,  q=1+alpha.

At r=|x|>0, the principal stretches are q r^alpha, r^alpha, r^alpha, and

J_alpha=q r^(3alpha).

The map has identity trace, is a homeomorphism of the closed ball, is smooth away from 0 and is Lipschitz. It belongs to the target admissible class exactly when 0<alpha<1/2. Its essential Jacobian infimum is zero. The exact energy is

I(y_alpha) = 4 pi { [a(q^2+2)^3 + b(2q^2+1)^(3/2) + c q^2]/(3+6alpha)
                    + d q^(−2)/(3−6alpha) }.

The threshold alpha<1/2 comes from the barrier integral; all positive-degree terms are finite for every alpha>0. At alpha=1/2 the barrier diverges logarithmically.

The energy excess near the identity is

I(y_alpha)−I(id)
 = (4 pi/3)(63a+5 sqrt(3)b+c+3d) alpha^2 + O(alpha^3).

In particular, for every delta>0 there is a nonminimizing, zero-infimum-Jacobian admissible map with energy less than I(id)+delta. A sufficiently tight energy upper bound alone cannot certify a positive Jacobian infimum.

### Explicit annular nonstationarity

Write a radial map as y=f(r)e_r and define Psi(s,t)=W(diag(s,t,t)). Its radial first variation is

4 pi integral [r^2 Psi_s eta' + r Psi_t eta] dr,

for radial perturbations eta supported in an annulus. For f(r)=r^(1+alpha), define

R(r)=(r^2 Psi_s)'−r Psi_t.

Direct differentiation gives

R(r) = alpha {6a(q^2+2)^2(7+5alpha)
                 +6b sqrt(2q^2+1)(5+4alpha)+6c q} r^(1+5alpha)
       +18d alpha q^(−3) r^(1−7alpha).

Every coefficient is positive. Thus R(r)>0 at every r>0. Every nonzero nonnegative smooth eta compactly supported in an annulus yields first variation −4 pi integral R eta <0. Small positive perturbations remain orientation preserving because the annulus is separated from the degeneracy. This is a genuine admissible local descent direction and does not assume stress integrability at the origin.

### Nonintegrable ordinary Piola stress

Let Q=I+alpha e_r tensor e_r. Then F=r^alpha Q, J=q r^(3alpha), and the barrier stress is exactly

P_barrier = −2d q^(−3) r^(−7alpha) cof Q.

Its norm is 2d q^(−3) sqrt(1+2q^2) r^(−7alpha). All the positive-degree stress terms are O(r^(5alpha)), so there is no leading singular cancellation. Consequently,

DW(Dy_alpha) is locally L^1 near 0 iff alpha<3/7.

For 3/7 <= alpha < 1/2 the map has finite benchmark energy but DW(Dy_alpha) is not locally integrable. These remain nonminimizing maps; this finding limits conclusions from coercivity alone, not any additional integrability that minimization may force.

## 3. Rank-two interior degeneration with C^{2,gamma} regularity

On B1, set

y_beta(x)=(x1,x2,x3 |x|^beta),  beta>0.

Let mu=x3/r. At r>0,

J_beta=r^beta(1+beta mu^2).

The map has identity boundary trace. On each vertical fiber with (x1,x2) fixed, the third component is strictly increasing and fixes both fiber endpoints. Hence it is a homeomorphism of the closed ball onto itself. Its Jacobian is positive away from 0, where its derivative has rank two. It is a smooth diffeomorphism on the punctured ball and its essential Jacobian infimum is zero.

Its gradient is bounded. The only integrability restriction is

integral J_beta^(−2) dx < infinity iff beta<3/2.

The exact barrier integral is

integral_B1 J_beta^(−2) dx
 = [2 pi/(3−2beta)] {1/(1+beta)+atan(sqrt(beta))/sqrt(beta)}.

The exact determinant-square integral is

integral_B1 J_beta^2 dx
 = [4 pi/(3+2beta)] (1+2beta/3+beta^2/5).

For K=beta(beta+2), the exact sixth-gradient integral is

4 pi {8/3
 + 12(1+K/3)/(3+2beta)
 + 6(1+2K/3+K^2/5)/(3+4beta)
 + (1+K+3K^2/5+K^3/7)/(3+6beta)}.

For completeness,

|cof Dy_beta|^2
 =1+r^(2beta)[2+(beta^2+4beta)mu^2+beta^2 mu^4],

which is uniformly bounded and proves finiteness of its cubic integral.

For 1<beta<3/2 the map is C^{2,beta−1} on the closed ball. Thus, choosing beta=1+gamma gives a C^{2,gamma} interior degeneration for every 0<gamma<1/2. For gamma=0, any such example is also C^2.

### Direct local nonstationarity, independent of Section 1

For a map (x1,x2,u), put v=grad u=(p,q,h), h>0. The density becomes

a(2+|v|^2)^3 + b(1+p^2+q^2+2h^2)^(3/2)+c h^2+d h^(−2),

a strictly convex function of v. Along the positive x3-axis for u=x3 r^beta, let Q=1+beta and h=Q z^beta. The divergence of the third stress row is

6a beta z^(beta−1)[2(2+h^2)^2+Q(2+h^2)(2+5h^2)]
+6b beta z^(beta−1)[sqrt(1+2h^2)+Q(1+4h^2)/sqrt(1+2h^2)]
+2c beta Q z^(beta−1)
+6d beta Q^(−3) z^(−3beta−1),

which is strictly positive. At any fixed positive-axis point, it remains positive in a sufficiently small interior ball avoiding 0. A nonnegative third-component test supported there is therefore a strict descent direction. No distributional treatment of the singular point is needed.

### Arbitrary smooth diffeomorphic traces: class-level extension

These failures of a coercivity-only inference are not confined to affine boundary data. If G is any permitted smooth orientation-preserving diffeomorphism on a neighborhood of the closed ball, then G composed with y_beta has trace G, finite energy and essential Jacobian infimum zero. This follows from boundedness of DG and cof DG and a positive lower bound for det DG on the compact closed ball.

More locally, one may put the rank-two construction in an interior ball of any permitted domain: replace r^beta by a nondecreasing positive cutoff h(r) equal to r^beta near 0 and 1 near the ball boundary. The determinant h(r)+(x3^2/r)h'(r) is positive away from 0. Extend the map by the identity outside the ball and compose with G. This supplies class-level degenerating competitors for every permitted datum. **No minimizing or stationary property is asserted after composition.**

## 4. Boundary-only degeneration, smooth throughout the interior

Fix 1<k<2, write z=x3, rho^2=x1^2+x2^2, and let

q=|x−e3|=sqrt(rho^2+(1−z)^2).

On B1 define

y_k(x)=(x1,x2,z+(1−|x|^2)(1−q^k/4)/2).

It has identity trace on the entire sphere. Direct differentiation gives

J_k=1−z+(z/4)q^k+(k/8)(1−|x|^2)(1−z)q^(k−2).

The last term is nonnegative in B1. If z>=0, the remaining terms are nonnegative and 1−z>0 in the interior. If z<0, q<2 and

J_k >= 1−2^(k−2)>0.

Thus J_k>0 everywhere in the open ball and J_k extends continuously to the closed ball, where J_k(e3)=0 and it is positive at every other point. Each vertical fiber is strictly increasing and fixes its boundary endpoints. The map is consequently a smooth diffeomorphism B1 onto B1 and a homeomorphism of the closed ball.

Near e3 put t=1−z. Since

1−|x|^2=2t−q^2,

the nonsmooth contribution is a linear-coordinate multiple of q^k plus a smoother q^(k+2) term. It follows directly from homogeneous derivative estimates that y_k is C^{2,k−1} on the closed ball. Its gradient is bounded.

For z>=1/2,

J_k >= t+rho^k/8.

Therefore, bounding the spherical cap by a cylinder,

integral_cap J_k^(−2) dx
 <= C integral_0^epsilon rho d rho integral_0^epsilon (t+rho^k/8)^(−2) dt
 <= C' integral_0^epsilon rho^(1−k) d rho < infinity.

Outside that cap J_k has a positive lower bound. Hence the map belongs to the full target class and has essential Jacobian infimum zero, despite smooth interior diffeomorphism regularity and C^{2,gamma} boundary regularity for gamma=k−1 arbitrarily close to 1.

This example is not a minimizer by Section 1. It demonstrates specifically why a merely interior positive-Jacobian estimate cannot establish E-6322's conclusion over all of Omega. Composition with any permitted G on the closed ball preserves finite energy, boundary-only degeneration and the smooth diffeomorphic trace.

## 5. Independent certification: a collapsed segment is admissible

The first-variation lane proposed the following example. Let Omega=B(0,3), r=sqrt(x1^2+x2^2), z=x3. Choose smooth nondecreasing h0 with h0=0 for |z|<=1/2 and h0(z)=z for |z|>=1. Let s(r)=r^alpha near 0, with 0<s<=1 for r>0, s=1 for r>=1, and smoothness away from 0. Set

y(x)=(x1,x2,h0(z)+s(r)(z−h0(z))).

Then

J=(1−s)h0'(z)+s >= s.

All changes are inside the cylinder {r<1, |z|<1}, which lies strictly inside B(0,3), so the entire boundary trace is the identity. The singular gradient entries are O(r^(alpha−1)). On a positive-length subinterval of 0<|z|<1/2 they are exactly a nonzero multiple of r^(alpha−1), and J=r^alpha. With cylindrical measure r dr dz dtheta, the sharp thresholds are

sixth-gradient integrability: alpha>2/3;
cofactor-cubic integrability: alpha>1/3;
inverse-square determinant integrability: alpha<1.

Thus every 2/3<alpha<1 is admissible. The segment {(0,0,z): |z|<=1/2} collapses to a point. For each r>0 the vertical map is strictly increasing and fixes the fiber endpoints. It is onto the ball and one-to-one except for its axis fibers, a null set, but it is not a homeomorphism. This independently confirms that finite benchmark energy, positive determinant almost everywhere, identity boundary trace and almost-everywhere injectivity do not alone imply global topological injectivity. It is not a minimizer by Section 1.

## 6. Conditional regularity thresholds: what the barrier would suffice to prove

Assume a candidate map has the stated regularity as an additional hypothesis. Since J>=0 almost everywhere and is continuous, J>=0 everywhere in the closure.

### Interior

If y is C^{2,gamma} locally, then J is C^{1,gamma} locally. At an interior zero x0 of the nonnegative J, grad J(x0)=0. Thus

0<=J(x)<=C|x−x0|^(1+gamma).

The inverse-square integral dominates a constant times integral_0^epsilon r^(2−2(1+gamma)) dr, which diverges if gamma>=1/2. Hence local C^{2,1/2} regularity excludes interior zeros. Section 3 shows sharpness of this integrability argument for every smaller positive Hölder exponent.

### Boundary and the global lower bound

If y is C^{2,1} on the closed smooth domain, J is C^{1,1}. At a boundary zero, its tangential first derivatives vanish because its boundary restriction is nonnegative. In flattened boundary coordinates (xi,t), xi in R^2, t>=0 inward, Taylor's estimate gives

0<=J(xi,t)<=C(t+|xi|^2).

But

integral_{|xi|<epsilon} integral_0^epsilon (t+|xi|^2)^(−2) dt dxi = infinity

(logarithmic divergence). Thus there can be no boundary zero either. Compactness of the closed domain then gives min J>0. C^3 regularity on the closure also suffices, since it implies the required C^{2,1} regularity on compact coordinate patches.

Section 4 shows that no C^{2,gamma}, gamma<1, boundary version of this integrability-only argument can establish the global bound. This is a conditional theorem, not a regularity theorem for minimizers and not a resolution of the frozen target.

## 7. Independent scaling check of the homogeneous-core replacement

The counterexample lane's broader exclusion considers y(r,theta)=r^k phi(theta), 1<k<3/2, with smooth angular data and positive degree-one cone Jacobian D(theta). In a ball of radius R replace it by R^(k−1) r phi(theta), preserving the spherical trace.

The original inverse-square barrier has coefficient

[1/(k^2(9−6k))] R^(9−6k) integral_S2 D^(−2),

whereas the replacement has coefficient

(1/3) R^(9−6k) integral_S2 D^(−2).

Their difference is a strict improvement because k^2(3−2k)<1 for 1<k<3/2: its value is 1 at k=1 and its derivative is 6k(1−k)<0 thereafter. The change of the positive degree-six energy is a finite constant times R^(6k−3). Since 9−6k<6k−3 exactly when k>1, the barrier improvement dominates at sufficiently small R. This independently verifies the scalar coefficient and exponent checks; the companion counterexample report contains the full admissibility construction. Such exact homogeneous collapsing cores cannot be local minimizers.

## Verification and limitations

The companion `verify_exact.py` performs exact symbolic checks of the radial energy expansion, radial first-variation residual, triangular gradient/cofactor formulae, boundary determinant and homogeneous-core coefficients. It also compares the exact integrals with independent quadrature for several exponents. The results are in `verification.json`.

No external sources were needed for these authored elementary derivations. No example here is offered as a full-class global minimizer with degenerating Jacobian. No assertion about general minimizer regularity, a universal positivity theorem or a compliant global counterexample is made.
