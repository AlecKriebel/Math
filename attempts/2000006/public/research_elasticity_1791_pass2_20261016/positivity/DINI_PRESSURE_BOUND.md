# A quantitative global Dini criterion for the pressure

E-6322, shared mathematical pass 2, 2026-10-16.

## 1. Precise new conditional theorem

Let Omega be a bounded connected C^2 domain in R^3. Suppose p belongs to L^1(Omega), Q has a continuous representative on the closure, and

integral_Omega p div phi = -integral_Omega Q:Dphi

for every phi in C_c^infinity(Omega;R^3). Define the uniform modulus

omega(r) = sup{|Q(x)-Q(z)|: x,z in closure Omega, |x-z|<=r}.

If

integral_0^{R0} omega(r) dr/r < infinity

for some R0>0, then p is essentially bounded on the entire domain. There are a geometric radius R>0 and a constant C, depending only on Omega, such that

||p||_infinity <= C[R^{-3}||p||_1 + omega(R) + integral_0^R omega(r) dr/r].

Shrinking R changes only geometric constants. If convenient, a fixed multiple of R can be used in the modulus and its integral. This does not change the Dini condition or the conclusion.

No pressure trace or pressure boundary condition is assumed. No continuity of p is assumed. In the elasticity application, no continuity of J needs to be assumed separately.

## 2. Scale-invariant mean-oscillation estimate

For any bounded connected Lipschitz subdomain U compactly contained in or touching the boundary of Omega, the distributional equation holds for all compactly supported tests in U. Apply the Nečas negative-norm theorem with exponent two, subtracting any constant matrix Q0:

||p-p_U||_{L^2(U)} <= C_U ||Q-Q0||_{L^2(U)}.

The initially L^1 pressure is sufficient for this theorem. In particular the argument does not first test against p, whose L^2 membership is the conclusion.

For an ordinary ball, scaling makes C_U independent of the radius. For the boundary caps described next, C_U is likewise uniform. If U has diameter at most c r and Q0=Q at a point of its closure, this gives

(average_U |p-p_U|^2)^{1/2} <= C omega(c r).

If V is a nested smaller set with |U|/|V| uniformly bounded, Cauchy–Schwarz gives

|p_V-p_U| <= C omega(c r).

These two facts are the entire analytic mechanism behind the theorem.

## 3. Uniform geometry of small boundary caps

For b on the boundary, use a rigid coordinate change placing b at the origin, with the domain locally above a C^2 graph t=h(z), z in R^2, h(0)=0, Dh(0)=0, and |D^2h|<=L. By compactness of the boundary, both the available chart radius and L can be chosen uniformly.

For sufficiently small r, the cap

U(b,r)=Omega intersect B_r(b)

is star-shaped with respect to a ball centered at (0,r/2) with radius kappa r, for one fixed small kappa>0. Here is the relevant geometric check.

Take x=(z,t) in the cap and a in that small ball. The segment joining them stays in B_r(b) by convexity of the ball. The Hessian bound gives, for 0<=s<=1,

h((1-s)z+s a_z)
<= (1-s)h(z)+s h(a_z)+(L/2)s(1-s)|z-a_z|^2.

Since t>h(z), while a_t-h(a_z)>=c r, the segment height above the graph is at least

s c r-C L s r^2,

which is positive for a uniform small radius. This proves the star-shaped property. The cap volume is bounded above and below by fixed multiples of r^3.

After scaling by r^{-1}, these domains fit in a fixed ball and are star-shaped with respect to a ball of fixed positive radius. The standard Bogovskii construction on such domains therefore has a uniform L^2-to-W_0^{1,2} bound. Its dual Nečas estimate in Section 2 is uniform as well. This uniformity is essential: invoking a separate unspecified constant for each shrinking domain would not justify the Dini sum.

The standard support-preserving Bogovskii construction and its Sobolev mapping are documented in Costabel–McIntosh, especially the starlike-domain construction, Corollaries 3.3–3.4, and Proposition 4.1. The uniform dependence here follows by using the same normalized bump in the fixed-radius star ball after translation and dilation, with one fixed outer cutoff. The resulting operator on a cap is a restriction of an operator with the same fixed symbol bounds.

## 4. Boundary mean telescoping

Fix a small uniform geometric radius R and put r_k=2^{-k}R. At each boundary point b, the nested caps have a uniformly bounded volume ratio. Section 2 gives

|p_{U(b,r_{k+1})}-p_{U(b,r_k)}| <= C omega(2r_k).

The initial mean has the uniform bound

|p_{U(b,R)}| <= C R^{-3}||p||_1.

Because omega is nondecreasing, the dyadic sum of omega(2r_k) is bounded by a constant times omega(2R)+integral_0^{2R} omega(t)dt/t. Hence all these boundary-cap means are uniformly bounded, independently of b and k. Intermediate radii are handled by comparing with an adjacent dyadic cap; their volume ratio is bounded.

This establishes boundedness of the means all the way down to the boundary. It has not silently presumed a boundary trace of p.

## 5. From bounded means to an essential supremum

Let x be an interior Lebesgue point of p and let delta=dist(x,boundary Omega).

If delta is bounded below by a fixed fraction of R, start with an ordinary interior ball of fixed radius. Its mean is controlled by R^{-3}||p||_1, and ordinary-ball dyadic telescoping applies.

Otherwise choose a nearest boundary point b. Then

B_{delta/2}(x) is contained in U(b,2delta),

and the two volumes are comparable by universal geometric constants. The cap mean-oscillation estimate controls the difference of their pressure means by C omega(4delta). The cap mean itself is bounded by Section 4. Finally telescope ordinary balls centered at x from radius delta/2 down to zero. The same Dini sum converges, and Lebesgue differentiation identifies the limiting mean with p(x).

This proves the asserted uniform bound at almost every x, including points in arbitrarily thin boundary collars. It proves an essential bound directly; continuity of p or J is unnecessary.

## 6. Application to the frozen minimizer

For E-6322 the already justified inner stationarity is

div(p I+Q(Dy))=0,

with p=3dJ^{-2}, J=det Dy, and

Q(F)=[a|F|^6-2b|cof F|^3-c(det F)^2]I
     -6a|F|^4F^TF+3b|cof F|(cof F)^T(cof F).

Consequently, if this positive-degree tensor Q(Dy) has a uniform Dini-continuous representative on the closure, the theorem gives

ess inf_Omega J >= sqrt(3d/||p||_infinity)>0.

The finite mean is already controlled: ||p||_1 <= 3 I(y) <= 3 I(G), where G is any permitted smooth diffeomorphic extension used as a competitor.

A sufficient special case is uniform Dini continuity of Dy on the closure. If |Dy|<=M, the polynomial-minor formula gives

|Q(F)-Q(H)| <= C(a+b+c)M^5 |F-H|

for |F|,|H|<=M. Thus a Dini modulus for Dy transfers to Q(Dy). Hölder continuity is one special case, but Dini continuity also permits slower moduli such as [log(e/r)]^{-1-epsilon}.

This strengthens pass 1's conditional regularity criterion. The new theorem controls the pressure directly and does not first derive all finite moments and then invoke Hölder continuity of J to exclude zeros.

## 7. Exact stopping point

Nothing here proves that an arbitrary W^{1,6} minimizer has Dini-continuous Q or Dy. At baseline, Q lies only in L^1. The dyadic estimate starts from a modulus which has not been obtained from the minimizer inequality.

The exact lane's continuous-tensor example in `../exact/ENDPOINT_CERTIFICATION.md`, Section 4, has an unbounded pressure satisfying the same abstract first-order equation and belonging to every finite L^q. Therefore uniform continuity alone is insufficient for this generic operator argument; a summable modulus or another constitutive/variational input is needed. That example does not assert that its tensor is Q(Dy) for a frozen-law minimizer.

## Sources and verification scope

- Breit–Cianchi, *Negative Orlicz-Sobolev norms and strongly nonlinear systems in fluid mechanics*, arXiv:1401.4885v2, equations (1.1)–(1.2): the initially L^1 pressure version of the Nečas theorem. https://arxiv.org/pdf/1401.4885v2
- Costabel–McIntosh, *On Bogovskii and regularized Poincaré integral operators for de Rham complexes on Lipschitz domains*, author manuscript, Corollaries 3.3–3.4 and Proposition 4.1: the starlike-domain construction and support/Sobolev properties. These passages were inspected in this pass. https://costabel.perso.math.cnrs.fr/publis/PoiBogdeRhv2.pdf

The boundary-cap geometry, pressure mean telescoping, and specialization to E-6322 are derived above. The result is not claimed to be novel in the general theory of pressure reconstruction, nor to resolve the target without its added regularity assumption.
