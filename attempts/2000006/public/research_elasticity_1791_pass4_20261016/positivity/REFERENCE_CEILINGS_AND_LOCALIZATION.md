# Reference-volume ceilings and local-affine replacement obstructions

E-6322, shared pass 4, 16 October 2026.

## 1. Changing the global reference cannot raise its safe level without bound

The pass-3 reference truncation uses a smooth positive-determinant extension H of the prescribed entire trace and is admissible for

lambda<=m_H/(2C_Omega),  m_H=min_{closure Omega}sigma_min(DH).

The domain constant C_Omega is independent of the chosen reference. All such references satisfy the same null-Lagrangian volume identity

integral_Omega det DH=V,  V=|G(Omega)|>0.

Since det DH>=m_H^3,

m_H <= (V/|Omega|)^{1/3},

and therefore

lambda_0(H)<= (V/|Omega|)^{1/3}/(2C_Omega).              (1)

Thus replacing H by another smooth same-trace reference, or iterating such references, cannot remove this construction's finite safe-threshold ceiling simply by increasing its minimum singular value. This is a consequence of the complete fixed trace, not a technical defect in the maximal-function extension.

The explicit upper energy bound for the replacement also grows with ||DH||_infinity^6. A proposed iteration whose reference gradients grow without bound has not retained a uniform comparison constant. These observations do not rule out every adaptive method; they rule out treating the existing fixed-reference estimate as a uniform high-level truncation merely by renaming the reference.

## 2. Low-volume local references have a still smaller ceiling

Whenever a local reference H on a ball B has the same complete trace as y there and a strictly positive minimum singular value, the same null-Lagrangian calculation gives

min sigma_min(DH) <= (average_B J_y)^{1/3}.               (2)

Consequently the safe local level provided by the same construction is no larger than a constant times (average_B J_y)^{1/3}. If this average is small, the safe level becomes small, not large. At an L^6-Lebesgue point of Dy with small positive determinant, shrinking balls have average J_y tending to that determinant. Almost every point has this property.

This statement is conditional only on the existence of that local reference. Unlike the original complete boundary datum, the trace of y on an interior sphere is not supplied as smooth or diffeomorphic. One cannot silently transfer the original hypothesis on G to every interior comparison ball.

An affine matrix A by itself has the further necessary bound sigma_min(A)<=det(A)^{1/3}. The coordinate normalization F=A M removes the explicit determinant sign scale from M, but its energy coefficients and coercivity constants remain A-dependent, as the next section shows.

## 3. Barrier-normalized affine blow-ups lose gradient coercivity

Let A_epsilon=diag(1,1,epsilon) and fix a matrix M in GL^+(3). Direct substitution yields

epsilon^2 W(A_epsilon M)
 =epsilon^2 H(A_epsilon M)+d(det M)^{-2}
 ->d(det M)^{-2}.                                       (3)

The convergence is uniform on each compact set of positive-determinant M. For the precise relative-minor excess R_A from pass 3,

epsilon^2 R_{A_epsilon}(A_epsilon M)
 ->d[(det M)^{-2}+2 det M-3].                            (4)

Here the positive-degree Bregman terms stay bounded for fixed bounded M and vanish after multiplication by epsilon^2; the determinant-square term vanishes as well. This is a direct finite-dimensional limiting formula, not a claimed Gamma-convergence or regularity theorem.

In particular, for any fixed M in SL(3), the limiting excess is zero. Taking M=diag(2,1/2,1) gives

|A_epsilon M-A_epsilon|^2=5/4

for every epsilon, while the left side of (4) tends to zero. Therefore no uniform lower bound of this normalized excess by a fixed positive multiple of unweighted |F-A_epsilon|^2, or its sixth power, can hold for all these centers. The barrier-dominated normalized limit sees determinant change but not arbitrary volume-preserving strain.

This is compatible with the pass-3 exact rank-one stiffness degeneration. It does not preclude an anisotropic excess or another argument that retains the vanishing positive-degree terms at their correct scales. It does show why simply normalizing the barrier and applying a center-independent strain excess criterion would lose essential coercivity.

## 4. Baseline local traces need not admit a Lipschitz replacement

If a map z belongs to W^{1,infinity}(B_r), its continuous trace on the sphere is Lipschitz, with a constant controlled by ||Dz||_infinity because the ball is convex. Therefore an everywhere Lipschitz replacement agreeing with y on the entire sphere is impossible unless that trace is Lipschitz.

The baseline finite-energy class does not supply this property, even on some sequence of small centered spheres. A concrete example is the logarithmic shear already constructed in pass 2:

y=(x_1,x_2,x_3+epsilon u(rho)eta(rho)chi(x_3)),
u(rho)=rho^{2/3}[log(e/rho)]^{-sigma},  sigma>1/6.

Choose the cutoffs equal to one on a small product neighborhood of the origin and supported inside a smooth ball, and take epsilon small enough that J_y lies between 1/2 and 3/2. The map has identity complete outer trace and finite energy: the critical radial gradient integral is integral d rho/[rho(log(e/rho))^{6sigma}].

For every sufficiently small r, compare the north pole P=(0,0,r) of the sphere with

X_rho=(rho,0,sqrt(r^2-rho^2)).

The third component difference is

y_3(X_rho)-y_3(P)=epsilon u(rho)+O(rho^2/r).

Since |X_rho-P| is comparable to rho,

|y(X_rho)-y(P)|/|X_rho-P| -> infinity as rho down to zero.

Thus the trace on every such sphere is non-Lipschitz. No globally Lipschitz map on that ball can share it. This example is not a minimizer; the identity is the unique minimizer for its outer data. Its precise role is to show that the required local boundary regularity cannot be borrowed from baseline membership when setting up a minimizer proof. Any improved trace property of actual minimizers would itself need proof.

The exact lane supplies a different compatible example in this pass: smooth volume-preserving identity-trace maps can approach the identity arbitrarily closely in W^{1,6}, uniformly, and in energy, while their midpoint with the identity has negative determinant on an open set. Thus those smallness conditions alone do not justify affine interpolation either. That example likewise is not a minimizer and is not used to deny a possible properly proved minimizer epsilon-regularity theorem.

## 5. What remains after the new one-sided estimate

The accompanying mixed-moment theorem is a genuine minimizer-specific advance: it accepts rank-one-connected endpoints with nonnegative determinant even when their inverse energy is infinite. Its localized consequence is

integral_E H(Dy)<=integral_E H(Dv)+2 integral_E dJ_y^{-2}.

Taking smaller amplitudes cannot remove the coefficient 2. A useful high-level argument would need an admissible endpoint with quantitative relative determinant control on the changed set, or some different control of this barrier source. The global volume ceiling, local trace issue, and loss of normalized strain coercivity identify separate gaps in the attempted affine-reference route.

No unconditional higher-integrability or global essential lower-bound conclusion has been obtained. E-6322 remains unresolved.
