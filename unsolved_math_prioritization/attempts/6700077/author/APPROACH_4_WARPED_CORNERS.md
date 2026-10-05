# Approach 4: the piecewise-smooth test in a warped surface class

## Restricted closure theorem

Let I be an open interval and y the coordinate on a circle of fixed period. Let

g_j = dt^2 + f_j(t)^2 dy^2

on I x S1, where f_j > 0 is continuous, piecewise C2 with locally finitely many seams, and has finite one-sided first and second derivatives at each seam. Suppose f_j -> f locally uniformly, with continuous f > 0. Fix kappa >= 0. Assume each g_j satisfies the intended volumic lower bound kappa; at zero it suffices to use the relaxed numerical lower bound, not the stronger Euclidean comparison as an added hypothesis.

Then the limit g=dt^2+f^2dy^2 satisfies locally

area_g(B_g(p,r)) <= V_kappa(r),

where V_0(r)=pi r^2 and, for kappa>0,
V_kappa(r)=(4pi/kappa)[1-cos(sqrt(kappa/2) r)].
In particular it has the intended volumic lower bound kappa. This proves closure only in this special two-dimensional, fixed-coordinate warped class, not for arbitrary surfaces or higher-dimensional gluing.

## Step 1: smooth pieces and seam sign

On a smooth piece the only nonzero curvature is Gaussian curvature K=-f_j''/f_j, so scalar curvature is -2f_j''/f_j. Smooth compatibility of the quantitative volumic lower bound gives

f_j'' + (kappa/2) f_j <= 0.

At a seam t=0 rescale the y coordinate so f(0)=1, and write
f(t)=1+a_+ t+O(t^2) for t>=0,
f(t)=1+a_- t+O(t^2) for t<=0.
We prove the centered ball expansion

area(B((0,0),r)) = pi r^2 + (a_+-a_- ) r^3/3 + o(r^3).       (1)

Use Euclidean polar coordinates (t,y)=rho(cos theta,sin theta). On either half-plane, the metric perturbation is 2a_sign t dy^2+O(rho^2), and its density is 1+a_sign t+O(rho^2). The distance from the origin along endpoint direction theta is

d(0,rho theta)=rho+(a_sign/2)cos(theta)sin(theta)^2 rho^2+o(rho^2),

uniformly in theta. Here and below theta in the distance expression denotes the corresponding unit vector.

Justification of this first variation does not assume radial geodesics of the perturbed metric. After rescaling, the metric is I+rho H+O(rho^2) with continuous Lipschitz H. Energy minimizers between fixed endpoints converge uniformly and strongly in H1 to the unique Euclidean segment: their Euclidean energies tend to the minimum, and the identity integral|gamma'-z|^2=integral|gamma'|^2-|z|^2 supplies strong convergence. The minimum energy's first-order term is therefore the integral of H along that segment, by comparing the minimizing curve and the segment in both directions. Taking the square root gives the stated distance expansion. Uniformity over directions follows by compactness and the same argument for any sequence of directions. All curves remain in a fixed small coordinate neighborhood by ellipticity.

For each ray, the inequalities obtained from this uniform distance expansion enclose its intersection with the metric ball between radial intervals with endpoints
rho=r-(a_sign/2)cos(theta)sin(theta)^2 r^2+o(r^2).
This enclosure is sufficient; monotonicity of distance along every ray is not assumed. Integrating the density, the coefficient of r^3 is

integral_0^(2pi) a_sign [cos(theta)/3 - cos(theta)sin(theta)^2/2] dtheta.

On cos(theta)>0 the two integrals of cos(theta) and cos(theta)sin(theta)^2 are respectively 2 and 2/3. On the opposite half they are -2 and -2/3. The result is (a_+-a_-)/3, proving (1).

If a_+-a_->0, there is an order-r^3 volume excess. Every smooth finite-curvature model has first correction only of order r^4 in dimension two. Such an excess violates all finite lower scalar bounds. For negative comparison thresholds implemented by adding a round two-sphere, the same conclusion follows from the product-ball integral: integrating a positive r^3 excess against two-dimensional sphere shells gives a positive order-r^5 excess in dimension four, whereas the smooth model correction is order r^6. Thus even the relaxed zero lower bound excludes this upward derivative jump. Restoring f(0), the necessary sign is

f'_+(0)-f'_-(0) <= 0.

## Step 2: distributional inequality and its closure

For a continuous piecewise C2 function with locally finitely many seams,

f_j'' = (classical second derivative on the pieces) dt
        + sum_seams (f'_{j,+}-f'_{j,-}) delta_seam

as a distribution. To verify it, integrate f_j times the second derivative of a compactly supported test function twice by parts on every smooth interval; continuity cancels the first-derivative-of-test boundary terms and leaves exactly the displayed derivative jumps. Step 1 therefore gives the distributional inequality

f_j''+(kappa/2)f_j <= 0.

For every nonnegative smooth compactly supported test function phi, this means
integral f_j(phi''+(kappa/2)phi)dt <= 0.
Local uniform convergence allows passage to the limit in this ordinary integral. Thus

f''+(kappa/2)f <= 0                                  (2)

distributionally, with no piecewise regularity assumption on the limit.

## Step 3: smooth approximation with a uniform curvature bound

On a relatively compact subinterval, convolve f with a nonnegative smooth mollifier of small support. The resulting f_e is positive and smooth, tends locally uniformly to f, and (2) commutes with convolution:

f_e''+(kappa/2)f_e <= 0.

Hence the smooth warped metrics g_e have Gaussian curvature >= kappa/2. Their small metric balls satisfy the standard surface area comparison with the constant-Gaussian-curvature kappa/2 sphere (Euclidean plane if kappa=0).

Here is the local comparison mechanism. Along a minimizing geodesic from p, the polar Jacobi density J has J(0)=0, J'(0)=1 and J''+K J=0 until its first conjugate point. For s(small)>0 solving s''+(kappa/2)s=0 with the same initial data, the Wronskian derivative is

(J's-Js')' = -(K-kappa/2)Js <= 0.

Therefore J/s is nonincreasing and J<=s while the ray minimizes. Integrate J in radius and angle only up to each cut time; discarded rays contribute no extra positive volume. This gives area(B(p,r)) <= 2pi integral_0^r s(u)du=V_kappa(r) for radii below the spherical first conjugate radius when kappa>0.

Uniformly small radii keep all balls in the chosen strip: the dt^2 term bounds below the distance to either t-boundary, independently of e. Thus the preceding bound holds on a fixed positive radius interval for all e and centers in a smaller strip. Approach 1's determinant-and-ball inclusion proof now passes this explicit comparison to g. No closure theorem for continuous scalar curvature is assumed in this step.

For kappa>0 and any 0<lambda<kappa, V_kappa(r)<V_lambda(r) for all sufficiently small positive r, either by their expansions or by monotonicity of sin(u)/u before pi. This is exactly the required volumic comparison. For kappa=0 the result directly gives the stronger Euclidean comparison.

For clarity, the latter also implies every negative relaxed lower threshold: the product-ball identity
vol_(X x S2)(B((x,z),r)) = integral_(B_S2(z,r)) vol_X(B(x,sqrt(r^2-d(z,w)^2))) dvol_S2(w)
first bounds X by Euclidean space, and then compares the spherical radial distribution strictly with the Euclidean two-dimensional one. Integration by parts against the strictly decreasing nonnegative kernel (r^2-s^2)^(n/2) gives a strict product-volume deficit for small r. In our surface case n=2. QED.

## Residual obstruction

The proof uses one warping function and a scalar inequality that is linear in that function. For general tensor metrics the scalar curvature inequality is nonlinear and second order; its singular terms need not reduce to a signed one-dimensional derivative-jump measure. No general volumic-to-distributional equivalence, or uniform smoothing theorem for arbitrary continuous metrics, was established.
