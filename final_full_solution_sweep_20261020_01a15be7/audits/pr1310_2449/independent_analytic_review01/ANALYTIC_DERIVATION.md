# Independent analytic/original-scope derivation for EP1038

## Statement actually under review

The current primary EP1038 statement quantifies over every nonconstant monic real polynomial f whose n>=1 roots, with multiplicities, are real and in[-1,1], and asks for both extreme lengths of {x inR:|f(x)|<1}. The1958 EHP original Problem1 printed131 is phrased more generally with roots in I_r=[-r,r]. Its r=1 specialization is exactly the modern problem and database2449. The PR's original-source wording should explicitly say this specialization; the submitted result does not solve every radiusr. Nor is an arbitrary-probability minimizer classification required by the finite-polynomial question.

For empirical probability mu=n^-1 sum delta_rj, V_mu=integral log|x-t|dmu=n^-1 log|f|, including minus infinity at roots. Thus the strict set is exactly {V_mu<0}. It lies in(-2,2). The equality set |f|=1 is finite because f^2-1 is a nonzero polynomial. Strict/non-strict lengths agree for every finite f, but this observation must NOT be transferred to the continuous zero-platform reference.

## The exact conditional inputs, not assumed executions

Call A the complete numerical obligation6.1: correct branch brackets and root/derivative signs on the stated tail, bulk and soft charts, all joins and endpoints, one strict stationary bracket in a strictly convex tube, and the exact comparisons identifying the global minimum L of the specified family and its displayed decimal enclosure. The independent family here does not replay these global slabs or adopt historical aggregatePASS fields.

Call B the complete numerical/reference obligation7.1: for every finite k>=29/20 there is a stated reference with positive density, simple physical main crossings, positive adjoint and a strictly positive scalar block surplus for EVERY positive pair of block masses within its caps. This includes the affine/constant covers,32 closed u-interval derivative checks, terminal simple/refined covers, singular tail, conversion overlaps and exact L<=T linkage. Again the omitted records/programs are not reconstructed here. Their truth is a necessary remaining input to a full lower-bound acceptance by the parent.

The analytic argument below proves: A+B imply the claimed finite-polynomial infimum and strict finite nonattainment. Separately, an independently executed Fraction calculation proves the fixed-candidate upper bound infimum<T without accepting A or B. The supremum uses the authenticated statement of Tao's external Theorem2.1, not a reconstruction of its full proof.

## 1. Reduction remains within the finite original

Every negative component of an empirical potential contains a root; otherwise the strictly concave potential would be nonnegative between its zero endpoints. Collapse all the root mass of each component simultaneously to its weighted mean. That point stays inside the component and in[-1,1]; the masses are rational with denominatorn, so the result is another admissible empirical root measure. Outside the old negative set, log|x-t| is concave as a function of t on each component. Jensen raises the collapsed potential there, hence the new negative set is contained in the old one. Each old component now has exactly one pole; strict concavity on each side and nonnegative old endpoints give exactly one new negative interval around it. Nonnegative separators, including single contact points, remain separators.

Reflect so the finite mean m<=0. For -1<x<0 and -1<=t<=1, |x-t|<=1-xt and Jensen gives V(x)<=log(1-xm)<=0. Equality throughout would require a point mass at0, for which the first inequality is strict. Thus(-1,0) lies in one negative component. Its unique clusterc is the leftmost cluster, so c<=m<=0. Translate by-c-1: support stays in[-1,-c]subset[-1,1], mean remains nonpositive, and the main cluster moves to-1.

Let r0>=0 be that component's old right endpoint. If r0-c<1, the distance to the main root is<1 and all distances to residual roots on its right are<=1, contradicting zero potential. Therefore the new endpoint beta=r0-c-1 is>=0, and residual roots lie to its right in[beta,1]. If the mass at-1 isA, weighted arithmetic-geometric mean at beta yields 1<=1+(2A-1)beta. This gives A>=1/2 for beta>0. At beta=0 equality forces all residual roots to1, and nonpositive mean gives the same result. The single-atom case has length2.

Otherwise k=A/(1-A)>=1. Shift by1 and divide the potential by1-A. This preserves length/sign and leaves

    W(x)=k log|x|+sum_i p_i log|x-d_i|,
    1<=d_1<...<d_N<=2, p_i>0, sum p_i=1,

with distinct main/residual components, allowing contact. Only nonempty FINITE blocks are subsequently used. No limiting probability is subjected to this atomization/lower argument.

## 2. Residual widths and the elementary k range

Remove the pole p_i log|x-d_i| from the potential in a residual component with endpoint distances s,u. The remaining background is strictly concave. Its two endpoint equations imply

    R_i :=exp[-(k log d_i+sum_(j!=i)p_j log|d_i-d_j|)/p_i]
        <=s^(u/(s+u))u^(s/(s+u)) <=(s+u)/2.

The last scalar inequality follows by maximizing (1-w)logw+wlog(1-w), with maximum-log2 atw=1/2. Therefore total length>=J_k=M_k+2sum R_i. On(0,1), W<=klogx+log(2-x)<0, and on the negative side W(-b)<=klogb+log(2+b). The root of b^k(2+b)=1 is at least sqrt2-1; hence M_k>=sqrt2.

For1<=k<=K=29/20, separation supplies b in(0,d1) withW(b)>=0. Write y_i=2-d_i and ybar=sum p_i y_i. Jensen gives b^k(2-ybar-b)>=1. This forces b>=1, and then ybar<=max_b(2-b-b^-K)=epsilon<1/25, with the explicit rational Taylor witnesses in the pinned proof.

Put Q=sum p_i^2,t=1-Q,S=sumR_i. Pairwise log-concavity and |d_i-d_j|<=y_i+y_j give

    sum p_i^2 logR_i >=-klog2-tlog(2epsilon/t).

Since eachR_i<=S, QlogS bounds the left side from above. Equivalently Qlog(3S)>=log3-klog2-tlog(6epsilon/t). The conventiont=0 uses continuity. With tlog(c/t)<=c/e and the pinned rational log estimates, the right side is>0. Thus S>1/3 and J_k>sqrt2+2/3>2. This argument needs no global numerical certificate and includes N=1.

## 3. Reference potentials and exact width support

For1<=a<2, let de=dd/[pi sqrt((d-a)(2-d))] on[a,2], c=(a+2)/2,r=(2-a)/2,H=r/2. The probability omega=sqrt(2a)e/d has mass1. The reference eta=(k+1)e-komega has density mathcalA(d)=k+1-k sqrt(2a)/d and mass1; strict positivity is a>2(k/(k+1))^2. Its weighted potential W0=klog|x|+integral log|x-d|deta is the constant C=logH+klogD0 on the conductor, D0=(a+2+2sqrt(2a))/4. These are arcsine/Poisson identities, not a claimed extremal characterization.

Assume the reference's physical simple main crossings x_-<0<x_+<a, W0'(x_-)<0<W0'(x_+), as B must establish. Positivity gives strict concavity on(0,a); the positive-slope zero is the first crossing and is strictly separated from the conductor.

For residual quantile T, set Psi(y)=y exp(k^-1 integral log(1-y/T)), R=exp(-k^-1 integral logT). Then W(y)/k=log(|Psi(y)|/R). For a finite target Psi has one positive maximum before d1. Separation/contact gives R<=Psi_max; on the negative axis Psi increases from-minus-infinity to0. The inverse branch Phi at0 therefore gives the main endpoints Phi(-R),Phi(R), using limits at contact.

Lagrange inversion yields positive coefficients. Every term of a finite odd width truncation is a positive multiple of a monomial product_i d_i^-gamma_i, gamma_i>0. Its Hessian quadratic form, divided by the monomial, is

    (sum gamma_i v_i/d_i)^2 + sum gamma_i v_i^2/d_i^2 >=0.

Thus these truncations are convex on positive root coordinates. Approximate the continuous reference quantile by common equal-mass partitions refining all rational target blocks. For each coefficient only finitely many inverse moments occur, and their values and first variations converge by bounded dominated convergence(T>=1, boundedvelocity). This passes the finite-dimensional tangent inequalities to the reference.

The convergence step is essential: positive inverse coefficients and Pringsheim's theorem exclude a smaller complex radius before a regular positive real inverse level. At the separated reference, R lies strictly inside the radius. A slightly larger disk has |Phi(z)|<=Phi(|z|)<a, so the logarithmic integral and its inverse remain analytic under small bounded quantile perturbations. Implicit functions and Cauchy estimates justify convergence of the width series AND its first variation. No separation of the entire interpolation path is assumed. At a contact target apply the positive truncations at lambdaR,0<lambda<1, then letlambda increase to1. The target odd series increases to the exact contact width; reference values/derivatives converge absolutely. Therefore

    M_k(T)>=M0+DM_k(T0)[T-T0].

## 4. Corrected adjoint and jump velocities

Let sigma_-=-1/W0'(x_-),sigma_+=1/W0'(x_+),K_j=sqrt((a-x_j)(2-x_j)), allpositive. Set

    D=sum sigma_j K_j/(a-x_j),
    dxi=[D-sum sigma_j K_j/(d-x_j)]de.

The numerator vanishes at a and strictly increases, so xi is finite, atomless and positive on every nonempty interval. Let R0=xi([a,2])>0. Write v(d)=T-T0 at the material point and F=mathcalA v. Direct differentiation of the constant-platform identity yields the explicit principal-value function

    g(d)=pv integral F(e)/(e-d)de(e),
    DM=-sum sigma_j integral F(d)/(d-x_j)de(d).

The exact adjoint relation is

    DM-integral g dxi =-F(2)sum sigma_j/K_j.                  (A)

It is not an uncorrected equality. The independent rational cosine-moment diagnostics reproduce(A), including a constantF that falsifies omission of the boundary term.

For a proof, put d=c-r cos(theta) and K_j/(d-x_j)=P_rhoj(theta),0<rhoj<1. For F=f0+2sum fn cos(n theta), the arcsine Hilbert transform of cosn is-U_(n-1)/r. Integrate the elementary cosine expansions of U against Poisson kernels. The coefficients of DM-integral gdxi are-Gamma forf0,-2Gamma for evenn,+2Gamma foroddn, withGamma=sum sigma/K. These are exactly-F(pi)Gamma.

For the actual finitely discontinuous velocity, subtract its finite angular jump steps. The remaining continuous piece is piecewise analytic with cosine coefficients O(n^-2). Poisson-Abel regularization of its transformed series is bounded by a multiple of1+|log min(theta,pi-theta)|. A jump at interior theta0 has transform proportional to

    [log|1-lambda exp(i(theta+theta0))|
     -log|1-lambda exp(i(theta-theta0))|]/sin(theta).

Near theta0 the logarithm has uniformly integrable O(delta(1+|logdelta|)) mass; near0 andpi the numerator is O(sin theta) uniformly inlambda because theta0 is interior. The adjoint angular density is bounded and O(theta^2) at0. These facts justify the paired Abel limit; the periodic F extension is continuous at pi, giving the endpoint term. No unjustified differentiation through coincident target atoms is required: off jumps g is the explicit integrable principal-value function used in the inequalities.

The target's final root d_N<=2 gives F(2)=mathcalA(2)(d_N-2)<=0. Thus(A)'s correction is nonnegative and M_k(T)>=M0+integral gdxi.

## 5. Mixed energy, strictness and the actual circle import

For target quantile block I_i, set p_i=|I_i|>0,r_i=xi_hat(I_i)>0 and E(I)=integral_I integral_I log|T0(u)-T0(v)|dv dxi_hat(u). Angular densities are bounded and the kernel is the sum of log-sines, so these integrals are absolutely convergent and Fubini is legitimate. Off a target block the ordered target/reference differences have the same sign. The inequality y/x-1>=logy-logx gives

    g(T0(u))>=-p_i logR_i-C-p_i+integral_Ii log|T0(u)-T0(v)|dv.

Same-block quotients are exactly-1. Integrate, add the residual-width bounds and minimize -p_i r_i logR_i+2R_i at R_i=p_i r_i/2. This yields

    J_k>=M0+sum_i[E(I_i)-p_i r_i log(p_i r_i/2)-C r_i].       (B)

Let Ceff=C+(L-M0)/R0. Strict positivity, for every nonempty block, of

    E(I)/(p r')-log(p r'/2)-Ceff/p                         (C)

therefore implies J_k>L after a FINITE sum. No uniform lower bound on p orr' is needed. The excess need not stay uniform as the degree tends to infinity; sum p_i r_i can tend to0, consistently with recovery.

The primary Christ-Iliopoulou Theorem1.1 and equation(1.3) really apply to arbitrary nonnegative measurable functions on a compact connected Abelian group. Their admissibility/stability/equality conditions belong to other theorems and are not conditions on this basic inequality. The directly requested JHU PDF gave403, but the actual web PDF statement and a newly downloaded NSF public-archive edition both state this unconditional input. The latter cites Baernstein's1995 correction. It is a different payload from the PR's pinned2021 PDF; no fresh byte identity is claimed. The theorem's full proof is imported, not independently reproved.

On the circle of length2pi put K(t)=log|exp(it)-1| and ell=log2-K. Then ell is nonnegative, even, integrable, decreasing away from0. Even-extend the capped block densities f=1_J mathcalA/a_pi,g=1_J mathcalB/b_pi, both in[0,1], with ordinary masses2Q,2R. Apply the nonnegative rearrangement theorem to truncatedell then pass by monotone convergence. The fixed-mass sign comparison against a centered-arc indicator and the fact that convolutions of symmetric decreasing nonnegative circle functions remain such replace both rearranged densities by arcs. This increases ell energy, hence decreases K energy. Normalized Haar to ordinary measure multiplies both sides by the same(2pi)^2.

The identity |d(theta)-d(phi)|/H=|exp(i theta)-exp(i phi)| |exp(i theta)-exp(-i phi)| and the four quadrants of the even extension give

    E/(p r')-logH =(2QR)^-1 integral_T integral_T f g K.

The denominator is2QR, not4QR. Arc comparison gives E/(p r')>=logH+2mathscrA(Q,R), where

    mathscrA(Q,R)=-sum sin(nQ)sin(nR)/(n^3 Q R).

The integrated Fourier series is absolutely convergent for fixed Q,R>0, via Abel regularization of the integrable kernel. Defineh(X)=mathscrA(X,X)-log(X/pi). Its integral representation shows h is decreasing on(0,pi], and the series gives h(pi)=0, so h>=0. Polarization yields

    2mathscrA(Q,R)-mathscrA(Q,Q)-mathscrA(R,R)
       =sum (sinc(nQ)-sinc(nR))^2/n >=0.

Substituting physical masses p=a_pi Q/pi,r'=b_pi R/pi produces exactly the scalar in PR(8.1):

    log(2H/(a_pi b_pi))+h(Q)+h(R)
      +sum (sinc(nQ)-sinc(nR))^2/n-pi Ceff/(a_pi Q).          (D)

No equality case from the circle theorem is needed. This establishes the precise analytic interface that B must bound strictly.

## 6. Symbolic branch and certificate interfaces

For q>0 put s=(1-q)/(1+q),H=2q/(1+q)^2,A=logH/logq and k=A/(1-A). Nonnegative one-cut density is exactly A<=s. This is equivalent to chi(q)=(1+q)(log2-2log(1+q))+2qlogq>=0. Direct differentiation gives chi'=log(2q^2/(1+q)^2)<0. Numerical opposite endpoint signs must still be established to isolateq_s; monotonicity alone supplies uniqueness, not its claimed digits.

For F(q,u)=Alog((u-q)/|1-qu|)-logu, its plus derivative numerator is qu^2-Bu+q, B=1+q^2-A(1-q^2). When A<s, B>2q: the derivative has exactly one zero in(1,1/q), so F first decreases from its trivial root1 then increases to infinity. The unique nontrivial plus root is simple. Foru>1/q, F_u<0 with opposite infinite endpoint limits, giving one simple minus root. The physical coordinate x=1+s^2-H(u+1/u) decreases withu and gives W0=-(k+1)F. This identifies sign boxes with actual main crossings, not roots merely near floating proposals.

The tau=-1/logq,z=qu regularization is nonsingular at tau0 after q(0)=0. At0 the equations are-log(2|1-z|)=0 with roots1/2,3/2. The analytic derivative bound0<=q_tau<=2500exp(-50) on[0,1/50] follows by monotonicity, so the full singular tail can be checked on a closed box. All asserted interval signs remain numerical obligations; no positive cutoff can replace the limiting endpoint.

At the soft endpoint y=(logu_plus)^2, C0=cosh(sqrt y), S0=sinh(sqrt y)/sqrt y, b=qS0/(1-qC0), w=yb^2. The exact deflation is D=A-1+2Ab sum_(m>=0)w^m/(2m+1)=0. The last series is analytic for|w|<1, not entire. Positive1-qC0 and w<1 imply qe^(sqrt y)<1, the needed real branch. At y0, D=(A-s)/s<=0 on q<=q_s. Thus a final numerical slab extending pastq_s is valid only when its use is restricted to q<=q_s, with positive upper sign and D_y>0; it does not certify a nonnegativey root for inadmissibleq. The width's cosh form is regular at y0, so total derivative checks can coverq_s.

The6.1 root existence signs must precede interval Newton contraction. Uniform parameter signs plus strict slope in the initial box give containment; m-G(P,m)/G_z(P,Z) then preserves every already-contained root by the mean-value theorem. Bulk and soft derivative signs, the positive second derivative in the convex tube, stationary opposite signs and exact cross-chart overlaps would imply precisely one global family minimum. They are not inferred here from slab counts, printed margins or hashes.

For finite7.1 references, Ceff(T)<0 makes P=-pi Ceff(T)/a_pi>0. Decreasingh permits upper mass caps in lower bounds. For the affine case split Q<=Rmax and Q>=Rmax; on the latter R<=Rmax<=Q and decreasing sinc give the retained n=1-square lower bound. The actual check f'(Q)<0 on all32closed u-pieces makes testing f(Qmax)>0 sufficient. In the constant case dropping squares gives B+P/Qmax. These reductions cover all tiny positive block masses, not a sampled mass range.

For terminal references C=0. The physical derivative identity raw=-uF_u and x_u=-K/u gives sigma=tKw, t=1-A. Direct cancellation gives a_pi=P0/t,b_pi=4tH(w_plus+w_minus),R0=2tHsum(1+q/z)w, and D*=a_pi b_pi/(2H)=2P0(w_plus+w_minus). A impliesM0=Lambda(q)>=L, hence Ceff<=0; this term may then be dropped. A fixed upper bound ALONE would not justify that sign. The tau0 closed box is used only for cancelled expressions and bounds; every actual finitek has tau>0 andD*>0. Using-logD*>=1-D* avoids evaluatinglog0 at the limiting endpoint.

Actual terminal coverage also needs chi(q_cap)>0,k(q_cap)<21/5,k'(q)<0 and k(q)->infinity, and outward-conversion overlaps at split/cap. These are specific gates, not automatic from a finite table. The elementary range ends29/20, the affine range starts36/25<29/20, finite ranges share21/10, and the terminalcap must overlap21/5 strictly. All written symbolic implications check out; their actual global interval inputs remain outside this family's replay scope.

## 7. Strict lower bound and sharp recovery

Assume A andB. A single cluster has length2; the smallk argument gives>2. Otherwise(C)-(D), B's strict positive surplus, positive p_i,r_i, and finite summation in(B) imply J_k>L. Residual width and collapse inclusion transfer this to every original finite polynomial. It is nonattainment without any arbitrary-measure equality classification.

For recovery fix the minimizing q and let a=2s^2-1. Increase the endpoint mass from A*=logH/logq to A with A*<A<s, keeping the conductor fixed. The density(1-2As/(t+1))de_[a,1] is positive and has mass1-A, since its reciprocal moment is1/(2s); adding A delta_-1 yields a probability. Its conductor potential is C(A)=logH-Alogq>0. With S(z)=sqrt((z-a)(z-1)) asymptotic toz, the exact Cauchy transform is

    V'_A(z)=[1-2As/(z+1)]/S(z).

On the left of-1 it is negative, giving one simple zero; on(-1,a) it is positive up to2As-1<a then negative down to the positive platform, giving exactly one other zero on the increasing branch; on(1,infinity) it is positive. Hence the negative set is exactly one interval and the zero set has only two points. At A* the two exterior crossings stay simple and separated from the zero conductor, so their width tends toLambda(q) asA decreases toA*.

For FIXEDA>A*, choose equal-weight empirical quantile approximations in[-1,1]. Their potentials converge in L1(-2,2): truncate log below-M, use weak convergence for the bounded continuous truncated kernel, and bound the uniform discarded integral by2exp(-M). A zero set of measure0 then gives convergence of negative-set indicators from the inclusion of their symmetric difference in{|V|<=delta}union{|V_n-V|>=delta}. Each empirical measure is the roots of an actual monic real polynomial. First approximate for fixed positive platform, then diagonalize A down toA*. Direct approximation of the zero-platform measure would NOT suffice; the elementary counterexample v_n=-1/n on an interval shows why sign sets need not converge to the strict zero-level set even under uniform convergence.

This proves recovery underA. The same argument for any single strictly admissible q proves the one-sided upper bound independently ofA/B; it needs no global stationary-point claim.

## 8. Independently proved one-sided bound and separate supremum

The own program fixed_candidate_fraction_check.py uses exact Fractions and90 positive atanh terms, with explicit log remainders after exact power-of-two reduction. It imports no source-author or global numerical certificate code. For the exact public rationalq_c and four public rational root-box endpoints it proves A_upper<s and signs(-,+,+,-), with the branch domains checked. The analytic root uniqueness above therefore identifies both crossings. Since u+1/u increases foru>1, the exact rational width_upper=H(m_hi+1/m_hi-p_lo-1/p_lo) boundsLambda(q_c).

The independently computed positive rational comparison is

    T-width_upper >=42327065090/10^40>0,
    T=1.83443047576266171109075363512901884952989750747.

All four strict root signs have explicit positive rational witnesses in the output, and normal/-O/-OO executions agree apart from their mode field. Positive-platform recovery proves the unconditional finite-polynomial upper bound infimum<T<1.834430475762662. It does NOT prove the matching lower bound, lower decimal digits, family minimizer or finite nonattainment.

Tao's actually retrieved Theorem2.1 separately states the supremum2sqrt2 and equality measure(delta_-1+delta_1)/2. Applying it to U=-V and the finite empirical measure gives |E_f|<=2sqrt2. Equality forces even degreen=2m and m roots at each endpoint; monicity gives(x^2-1)^m. Conversely its strict set is(-sqrt2,0)union(0,sqrt2), length2sqrt2. The missing point0 must not be included in the exact strict set, although it has no effect on the length. The external theorem's entire proof is not independently reaudited here.

## Conclusion of this family

No blocking ANALYTIC defect was found in the finite original reduction, the primary circle import or the implication of correctly verified6.1/7.1 inequalities. The conditional analytic theorem is complete within that scope. The actual global numerical inequalities, their full covers and the proposed global digits have NOT been independently reexecuted or accepted by this family. Historical PASS reports and hashes do not discharge them. Root must combine a fresh independently verified numerical record with this analytic implication before promoting the global claim. No row proposal, publication readiness, external service action or approval transfer is issued here.
