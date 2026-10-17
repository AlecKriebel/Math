# A common logarithmic-spiral class obeys the median inequality

This is a partial theorem for the 2015 median conjecture, not a general proof. It extends the credited common-degree homogeneous test class by allowing a common logarithmic angular drift. All integrals below are unnormalized angular integrals.

## Statement

Fix rho > 0 and kappa real. Let h_1,h_2,h_3 be real, continuous, 2*pi-periodic functions such that, in distributions,

L h_j := (1+kappa^2) h_j'' - 2*rho*kappa h_j' + rho^2 h_j >= 0.

For z = r exp(i theta), r > 0, define

u_j(z) = r^rho h_j(theta - kappa log r), and u_j(0) = 0.

Then the u_j are whole-plane subharmonic, and their pointwise median v_2 satisfies

I(r,v_2) = integral_0^{2*pi} v_2(r exp(i theta)) dtheta >= 0

for every r > 0. Consequently the normalized supremum assertion holds at all radii where B(r)>0. If B(r)=0, the angular median integral is also zero.

## Subharmonicity and extension at the origin

In polar logarithmic coordinates t=log r, the planar Laplacian is r^{-2}(partial_t^2+partial_theta^2). Thus

Delta u_j = r^{rho-2} (L h_j)(theta-kappa log r)

in the distributional sense on the punctured plane, and this is a positive measure there. Since h_j is bounded and rho>0, u_j tends uniformly to 0 at the origin. The removable-singularity theorem for bounded-above subharmonic functions gives the subharmonic extension with value 0. Equivalently, one may mollify h_j on the circle, use the elementary smooth calculation, extend at 0, and pass to the uniform limit on compact subsets.

## Half-period inequality

Put

a = rho*kappa/(1+kappa^2), b = rho/(1+kappa^2), s = pi/b.

Then L = (1+kappa^2) ((D-a)^2+b^2). First suppose h is smooth and F := ((D-a)^2+b^2)h >= 0. Variation of constants on [theta,theta+s] gives

h(theta+s) = exp(a*s)[h(theta) cos(b*s) + (h'(theta)-a*h(theta)) sin(b*s)/b]
             + integral_0^s exp(a*(s-x)) sin(b*(s-x)) F(theta+x)/b dx.

Because b*s=pi, the sine in the integrand is nonnegative and the initial derivative term vanishes. Therefore

h(theta+s) + exp(a*s) h(theta) >= 0.                     (1)

Since a*s=pi*kappa, the coefficient is c=exp(pi*kappa)>0. For distributional Lh>=0, take nonnegative circular mollifiers. Each mollified h obeys (1), and uniform convergence gives (1) for h. This is valid even when s exceeds 2*pi or is not a rational multiple of 2*pi.

## Passing to the median

Let H(theta)=median(h_1(theta),h_2(theta),h_3(theta)). For each j, inequality (1) reads

h_j(theta+s) >= -c h_j(theta).

The median is coordinatewise nondecreasing, and median(-c*x_1,-c*x_2,-c*x_3)=-c*median(x_1,x_2,x_3). Hence

H(theta+s)+c H(theta)>=0.

Integrating and using 2*pi-periodicity gives

(1+c) integral_0^{2*pi} H(theta) dtheta >=0.

Finally the circular median equals r^rho H(theta-kappa log r), so its integral is r^rho times this nonnegative angular integral.

## Exact limitation

The proof requires the same rho and kappa for all three functions. With different drifts, neither the shift s nor the coefficient c is common, so the median step does not follow. General discretely scale-invariant functions depend on both log r and theta and are not covered. This theorem does not settle arbitrary whole-plane subharmonic triples.

The source is A. Eremenko, "Conjectured inequality for subharmonic functions", 4 April 2015, https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. The source credits the kappa=0 homogeneous case. The common nonzero-drift extension above is an independently derived partial argument; no novelty claim is made.
