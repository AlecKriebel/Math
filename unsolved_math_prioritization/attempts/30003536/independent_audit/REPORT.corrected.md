# Intermediate Riesz maximum principle: five partial approaches

Problem 30003536 / OWR-15577-004, queue rank 1001. Research date: 2026-10-08 UTC.

**Disposition: unsolved after five substantive author approaches (5/5).** This document proves restricted estimates and obstructions to particular proof strategies. It neither proves nor disproves the requested global estimate. No novelty, priority, independent audit, formal verification, or peer-review claim is made.

## 1. Exact target and provenance

Fix an integer d >= 3 and a real exponent 1 < s < d-1. Put K_s(z)=z/|z|^(s+1) for z != 0. The question is whether a finite C(d,s) works, independently of f, in

    sup_{x in R^d} |F_f(x)| <= C(d,s) A_f,
    F_f(x) = integral K_s(x-y) f(y) dy,
    A_f = sup_{x in supp f} |F_f(x)|,

for every nonnegative f in C_c^infinity(R^d). The norm is the full Euclidean vector norm, not a single component, an operator norm, or a maximal-truncation norm. Support means the closed support, including boundary points where f vanishes. The zero function is trivial (the right side can be assigned zero); all proofs below assume f is nonzero. Since s<d, the integral is absolutely convergent. Local integrability of K and convolution with a compact smooth density give continuity; F_f tends to zero at infinity. Thus the two nonzero suprema are attained maxima.

The original question was visually checked at printed p.2124 of Oberwolfach Report 34/2017, in Benjamin Jaye's contribution, joint with Fedor Nazarov. The formula, open exponent interval, positivity, smoothness, compact support, and full vector norm agree with the corpus. Eiderman--Nazarov use the opposite kernel sign; this has no effect on either norm. Their Conjecture 1.1 permits continuous compactly supported nonnegative densities, a broader class than the smooth OWR target. We do not silently extend the target to arbitrary finite measures or signed densities.

The bibliography and scope in SOURCES.md are part of this report. Literature and duplicate checks are not counted among the five approaches.

## 2. Approach 1: antisymmetric moment and far-field localization

**Attempt.** Use positivity and antisymmetry to force a lower bound on A_f, then compare the field away from the support.

### Proposition 2.1
Let M=integral f >0, S=supp f, and D=diameter(S)>0. For every a in S,

    integral (x-a) dot F_f(x) f(x) dx
      = (1/2) double-integral |x-y|^(1-s) f(x)f(y) dxdy.          (2.1)

Consequently

    A_f >= M/(2 D^s).                                           (2.2)

For every x outside S, with delta=dist(x,S)>0,

    |F_f(x)| <= 2 (D/delta)^s A_f.                              (2.3)

**Proof.** All double integrals used here are absolutely convergent: on the compact support, the bounded factor |x-a| multiplies the locally integrable singularity |x-y|^-s. Write the left side as a double integral. Swap x,y, use K_s(y-x)=-K_s(x-y), and average the two expressions. The numerator becomes (x-y) dot (x-y), giving (2.1). The diagonal has product Lebesgue measure zero. Because s>1 and |x-y|<=D, the right side is at least M^2 D^(1-s)/2. The left side is at most D M A_f by the triangle inequality. Division gives (2.2). Also |F_f(x)|<=M delta^-s, proving (2.3). D>0 follows because a nonzero continuous nonnegative density is positive on a ball. QED.

For example, |F_f(x)|<=2A_f whenever delta>=D. Given a in S, |x-a|>=(1+2^(1/s))D implies delta>=2^(1/s)D and hence |F_f(x)|<=A_f. Thus a possible ratio larger than one is confined to a quantitatively bounded region after diameter normalization.

**Precise gap.** The estimate deteriorates as delta/D tends to zero. It gives no uniform control in holes or thin gaps close to S, exactly where the global maximum could matter. Normalizing mass and diameter bounds A_f below but does not bound the global field above. This route does not establish the target.

## 3. Approach 2: positive scalar domination loses arbitrarily many scales

**Attempt.** Bound |F_f| by the positive scalar potential J_f(x)=integral |x-y|^-s f(y)dy, then hope to estimate J_f by A_f. The second step is impossible with a uniform constant, even for radial smooth densities.

### Lemma 3.1 (single spherical shell)
Let sigma be normalized surface measure on the unit sphere in R^d and let 0<s<d-1. Its vector field satisfies

    |K_s*sigma(x)| <= B(d,s) min(|x|, |x|^-s)                  (3.1)

for x!=0, and vanishes at zero.

**Proof.** Oddness and spherical symmetry give the value zero at the origin. For |x|<=1/2, all vectors x-y stay at distance at least 1/2 from zero. The bound ||D K_s(z)|| <= (s+2)|z|^(-s-1), the mean value theorem, and integration give |K_s*sigma(x)|<=B|x|.

For 1/2<=|x|<=2, use |K_s*sigma(x)|<=integral |x-y|^-s d sigma(y). A spherical cap estimate gives sigma(B(x,t))<=C_d t^(d-1) for 0<t<=4, uniformly in x. To see the small-radius estimate, if the cap is nonempty choose a point y0 in it; it lies within the spherical cap centered at y0 of chord radius 2t. Local graph coordinates or the polar-angle area formula bound that cap by C_d t^(d-1). Larger t are absorbed into the constant. Layer-cake integration now bounds the potential by

    4^-s + s C_d integral_0^4 t^(d-s-2) dt < infinity.

The exponent condition s<d-1 is essential here. Finally, for |x|>=2, |x-y|>=|x|/2 gives a bound 2^s |x|^-s. On the middle compact radial interval min(|x|,|x|^-s) is bounded below by a positive number. Enlarging B joins the three estimates. QED.

### Proposition 3.2 (smooth multiscale obstruction)
For every fixed 1<s<d-1 there are nonnegative radial functions f_N in C_c^infinity(R^d) such that

    sup_x |F_{f_N}(x)| <= B_0(d,s),
    J_{f_N}(0) >= (5/4)^(-s) N.                               (3.2)

In particular no constant depending only on d,s can give sup_x J_f(x)<=C A_f for all admissible f.

**Proof.** Let r_j=2^-j and let sigma_{r_j} be normalized surface measure on the sphere of radius r_j. Define

    mu_N = sum_{j=1}^N r_j^s sigma_{r_j}.

Scaling (3.1) gives

    |K_s*mu_N(x)| <= B sum_{j=1}^N min(r/r_j,(r_j/r)^s),
    r=|x|>0.

The part with r_j>=r is at most 2, by summing a geometric series toward its largest term. The part with r_j<r is at most 1/(1-2^-s). Thus the vector field is bounded by B_0=B[2+1/(1-2^-s)], independently of N. At the origin the scalar potential is exactly N.

Choose a radial nonnegative smooth probability mollifier phi_delta supported on the closed ball of radius delta=r_N/4, positive in its interior, and put f_N=mu_N*phi_delta. This is a nonnegative radial compactly supported smooth function. Convolution and Fubini give

    F_{f_N}=(K_s*mu_N)*phi_delta,

so its global vector norm remains at most B_0. For Fubini, the scalar shell potentials are globally bounded by the same cap argument and the number of shells is finite; thus absolute integrability is available before interchanging integrations. For a point y on the jth shell and z in the mollifier support, |y+z|<=(5/4)r_j. Hence that shell contributes at least (5/4)^(-s) to J_{f_N}(0). Summing proves (3.2). Proposition 2.1 ensures A_{f_N}>0, while A_{f_N}<=B_0, so J_{f_N}(0)/A_{f_N} tends to infinity. QED.

**Precise conclusion.** The triangle-inequality majorant destroys cancellation and cannot close the target estimate by a uniform bound on J_f. These radial examples are not counterexamples to the vector maximum principle; the radial positive case is already credited to Eiderman--Nazarov.

## 4. Approach 3: the full vector norm can have a strict local maximum in a hole

**Attempt.** Apply an ordinary local maximum principle to |F_f|^2 outside S, as at the harmonic endpoint. The following construction rules out the necessary no-local-maximum premise within the actual positive smooth class.

### Proposition 4.1
For d=8 and s=2, there exists a nonnegative f in C_c^infinity(R^8) such that |F_f|^2 has a strict local maximum at a point outside supp f.

**Proof.** First use an auxiliary probability measure sigma on a latitude of the unit sphere. Write n=d-1=7 and m=1/sqrt(3). Let

    y=(m,sqrt(2/3) omega),    omega uniformly distributed on S^6 in R^7.

The support of sigma is distance one from the origin. Set F=K_2*sigma. The field is smooth near zero. Rotational symmetry in the last seven coordinates gives

    E[y_1]=m,  E[y_j]=0 (j>1),
    E[y_1^2]=1/3,  E[y_j^2]=2/21 (j>1),
    E[y_i y_j]=0 (i!=j),
    E[y_1^3]=m/3,  E[y_1 y_j^2]=2m/21 (j>1).

For general s, at |z|=1,

    D_j K_i(z)=delta_ij-(s+1)z_i z_j,
    D_j D_k K_i(z)
      =-(s+1)(delta_ij z_k+delta_ik z_j+delta_jk z_i)
        +(s+1)(s+3)z_i z_j z_k.                              (4.1)

At x=0 the kernel argument is z=-y. Substitution with s=2 gives

    F(0)=-m e_1,
    DF(0)=diag(0,5/7,5/7,5/7,5/7,5/7,5/7,5/7),
    D_1^2 F_1(0)=4m,
    D_j^2 F_1(0)=11m/7 for j>1.

All off-diagonal entries of the Hessian of |F|^2 vanish by reflection symmetry in the transverse coordinates. Its gradient is zero because DF(0)^T F(0)=0. Using

    D_j D_k |F|^2=2 (D_j F) dot (D_k F)+2 F dot D_j D_k F,

the Hessian at zero is

    diag(-8/3,-4/147,-4/147,-4/147,-4/147,-4/147,-4/147,-4/147).
                                                                    (4.2)

It is negative definite. In particular zero is a strict local maximum and the Laplacian there is -20/7, so |F|^2 is not subharmonic.

It remains to obtain a density in the precise target class, rather than a singular auxiliary measure. Let phi_epsilon be a nonnegative smooth probability mollifier supported on the ball of radius epsilon, and put f_epsilon=sigma*phi_epsilon. For epsilon<1/4 its support misses the ball of radius 1/2 around zero. The field and its first two derivatives converge uniformly to those of F on, say, the closed ball of radius 1/4: the kernel and the needed derivatives are uniformly continuous and bounded on the compact set of separated arguments, so the usual mollifier convergence applies.

By (4.2) and continuity choose a smaller closed ball B centered at zero on which D^2|F|^2 is uniformly negative definite. There is also a strictly positive gap between |F(0)|^2 and its maximum on the boundary of B. Uniform convergence preserves the boundary gap and uniform C^2 convergence preserves negative definiteness for all sufficiently small epsilon. The continuous function |F_{f_epsilon}|^2 attains its maximum on B at an interior point; strict concavity on B makes that point a strict local maximum. B is disjoint from supp f_epsilon. This proves the statement for an admissible smooth positive density. QED.

**Precise limitation.** A strict local maximum in a hole need not exceed values on S. This does not disprove the requested inequality for any constant, and does not even prove failure of its special case C=1. It proves failure of the local subharmonic/no-interior-maximum argument. The singular latitude is only an intermediate device; the final conclusion is explicitly smoothed into the target class.

## 5. Approach 4: three-point symmetrization has no pointwise positivity

**Attempt.** Expand the positive energy integral |F_f|^2 f and use a nonnegative curvature-type three-point integrand to control concentration.

For distinct x,y,z define

    p_s(x,y,z)= K_s(x-y) dot K_s(x-z)
              +K_s(y-x) dot K_s(y-z)
              +K_s(z-x) dot K_s(z-y).

### Proposition 5.1
For every s>1 this function takes both positive and negative values. For collinear points 0,e_1,t e_1 with t>1,

    p_s = [(t-1)^s-t^s+1]/[t^s(t-1)^s] < 0.                 (5.1)

For an equilateral triangle of side length l it equals 3/(2l^(2s))>0.

**Proof.** On the line the three terms are respectively t^-s, -(t-1)^-s, and t^-s(t-1)^-s, giving (5.1). Put a=t-1>0. For s>1 the function (a+1)^s-a^s is strictly increasing in a, since its derivative is s[(a+1)^(s-1)-a^(s-1)]>0; its value at a=0 is 1. Thus the numerator is negative. At an equilateral vertex the two difference vectors have angle 60 degrees, so each dot product is l^(-2s)/2. QED.

For an admissible smooth f, all expanded triple integrals are absolutely convergent: f is bounded and compactly supported, and the scalar potential integral |x-y|^-s f(y)dy is uniformly bounded for this fixed f because s<d. Therefore Fubini and permutation symmetry give the exact identity

    integral |F_f(x)|^2 f(x)dx
      = (1/3) triple-integral p_s(x,y,z) f(x)f(y)f(z) dxdydz. (5.2)

Continuity of p_s away from collisions shows that the negative sign remains on triples in three small disjoint neighborhoods of the collinear example. Thus it is not confined to a negligible geometric degeneracy.

**Precise gap.** The full integral in (5.2) is nonnegative, but its integrand is not. Negative cross-cluster contributions do not make the total energy negative: within-cluster contributions cannot be discarded. Consequently the direct pointwise-positive curvature argument fails, not the target inequality. The collinear sign calculation is valid for every real s>1; the executable rational tests below cover selected integer parameters only.

## 6. Approach 5: flat blow-up model and the surviving boundary layer

**Attempt.** Normalize a putative bad sequence, pass to a measure on which the field vanishes on its support, and rule out that limit. For integer exponents the simplest possible rigidity statement is false. Smoothing does not convert this fact into a counterexample.

Take d=4, s=2, decompose R^4=R^2_u x R^2_v, and consider two-dimensional Lebesgue measure lambda on the plane v=0. This measure has infinite mass, is not compactly supported, and is singular relative to four-dimensional volume.

On the plane, define the regularized field using symmetric inner and outer tangential cutoffs centered at the evaluation point:

    F_lambda^sym(u,0)
      = lim_{L -> infinity} lim_{rho -> 0+}
          integral_{rho<|t|<L} (-t,0)/|t|^3 dt = 0.

Every finite annular integral is zero by oddness. The inner cutoff is essential: the ordinary norm integral diverges logarithmically at the origin as well as at infinity. Off the plane, at (u,v) with v!=0, use symmetric outer tangential cutoffs |t|<L; there is no local singularity. The tangential component is zero by oddness and the normal component is

    v integral_{R^2} (|t|^2+|v|^2)^(-3/2) dt
      = 2 pi v/|v|.                                         (6.1)

The normal integral is absolutely convergent; the tangential integral is defined by the stated symmetric cutoff, not by an absolutely convergent integral at infinity. In polar coordinates its scalar integral is

    2 pi integral_0^infinity r(r^2+a^2)^(-3/2) dr = 2 pi/a,

using the antiderivative -(r^2+a^2)^(-1/2). Thus the regularized field is zero on its support yet has constant nonzero magnitude away from it. These are assertions about this specific model and regularization, not a claim that all technical reflectionless-measure hypotheses have been independently verified here.

### Proposition 6.1 (smooth thickness cannot be ignored)
Let g be a radial C_c^infinity(R^2) function with 0<=g<=1, equal to one on the unit disk and supported on the closed disk of radius two. Let h be a nonnegative C_c^infinity(R^2) probability density positive in the open unit disk and supported on its closure. For R,epsilon>0 define

    f_{R,epsilon}(u,v)=g(u/R) epsilon^-2 h(v/epsilon).

Put e=(1,0) in the normal R^2 and z_epsilon=(0,epsilon e). Then z_epsilon belongs to the closed support of f_{R,epsilon}, and as R/epsilon tends to infinity,

    e dot F_{f_{R,epsilon}}(z_epsilon)
       -> 2 pi L_h,
    L_h = integral h(w) (1-w_1)/|e-w| dw >0.                  (6.2)

The tangential coordinates in (6.2) are omitted from the dot product.

**Proof.** The point lies in the closed support because g(0)=1 and h is positive immediately inside the unit disk; h(e)=0 does not remove e from its support. Tangential oddness at u=0 cancels the tangential field. Change variables v=epsilon w and u=epsilon t. The normal e-projection is

    integral h(w)(1-w_1)
        [integral g(epsilon t/R)
         (|t|^2+|e-w|^2)^(-3/2)dt]dw.                       (6.3)

For almost every w in the unit disk, |e-w|>0 and 1-w_1>0. The inner integral tends to 2pi/|e-w| by dominated convergence on R^2, because 0<=g<=1 and its argument tends to zero. Its nonnegative product with (1-w_1) is at most 2pi, since (1-w_1)<=|e-w|. Dominated convergence in w now gives (6.2). Moreover, on |w|<=1/2 one has (1-w_1)/|e-w|>=1/3, so

    L_h >= (1/3) integral_{|w|<=1/2} h(w)dw >0.

Therefore A_{f_{R,epsilon}}>=pi L_h for all sufficiently large R/epsilon. QED.

For the concrete sequence R=n, epsilon=1/n, the measures f_{R,epsilon}dx converge locally weakly to lambda. Indeed compactly supported test functions see g(u/n)=1 for large n, and the normal approximate identity converges to evaluation at v=0. For any fixed a>0, at (0,ae) the normal field tends to 2pi e: the same computation, with a e-epsilon w in place of epsilon(e-w), follows from the polar integral and dominated convergence; the tangential field remains zero. Nevertheless the support fields at z_epsilon stay bounded below by Proposition 6.1.

**Precise gap.** Local weak convergence to a plane loses the moving normal boundary layer and does not carry a support supremum to a limit. The zero-on-plane field in (6.1) cannot be substituted for the support norm of the smooth approximants. A valid compactness solution would need much stronger control of support evaluations, plus an appropriate rigidity result; neither is obtained here. No counterexample in the target class follows from this model.

## 7. What remains

The uniform estimate for all nonnegative smooth compactly supported f, every fixed d>=3, and every 1<s<d-1 remains unresolved in this packet. No additional geometric regularity, radiality, integer restriction, signed source, or singular/infinite measure is being substituted for that question.

The five distinct mathematical routes were: antisymmetric first moment; positive scalar majorization across scales; local differential maximum principle; cubic symmetrized energy; and weak-limit/flat rigidity. Each includes an actual derivation or construction and an explicit endpoint where it stops. Bibliographic search, exact-source transcription, duplicate checks, and computation count as zero author approaches.

The checker verifies selected algebraic identities, finite geometric sums, scope fields, and package integrity. It does not prove the analytic estimates, the smoothing and limiting arguments, the open status of the literature, or the absence of all prior attempts. Those claims must be read and reviewed mathematically. The files were prepared for a separate independent audit; none has yet been performed as part of this author packet.
