# Independent analytic checks for PR263 v03

Reviewer: second newly commissioned whole-preprint adversary, 11 October 2026. These are this reviewer's deductions, completed before consulting the preceding whole-preprint review or its repair receipt. They audit the exact manuscript with SHA256 `caf327484a7068244ab98494eab835f50b84521a6d7ba364007bda31f7478677`. They use the actual primary PRT2000 equivalence and PR2010 definition at the bounded extents in `PRIMARY_READ_EXTENTS.json`; they do not independently reprove those general theorems.

## 1. Exact claims and falsification criteria

The hypotheses are: for every fixed real SPD coefficient metric, failure of set prox-regularity at the monic origin and at the full exact-degree base; arbitrarily close unstable inputs with two distinct attained GLOBAL nearest stable coefficient points; failure of whole-epigraph set prox-regularity for every fixed SPD joint coefficient/height metric, including mixed metrics. Remark 2 asserts an exact closed stability chart and its edge cases. Proposition 3 asserts positive Euclidean function prox-regularity at the monic origin relative to EVERY FINITE limiting subgradient, with constants allowed to depend on it and the strict PR2010 support convention.

An incorrect ambient derivative, outward sign, covector/vector identification, unattained projection, missing zero-leading exclusion, unsupported nonlinear metric transfer, bounded-gradient cancellation, omitted finite subgradient, or non-strict support would defeat the relevant claim. Finite runs cannot establish the universal or limiting quantifiers. No explicit nearest pair or firstness claim is hypothesized.

## 2. Monic root and all ambient directions

For t>0 the polynomial

    p_t(z) = (z+it)(z+t²-it) = z²+t²z+t²+it³

has roots lambda=-it and mu=-t²+it. The root lambda is simple and has real part 0, while Re(mu)=-t²<0. This strict gap is positive for each fixed t; it need not be uniform as t approaches 0. In real coefficient order (Re(a),Im(a),Re(b),Im(b)), implicit differentiation gives

    d lambda = -(lambda da+db)/(t²-2it).

Taking the real part in the four real coordinate directions gives

    d alpha/da_R = -2/(t²+4),
    d alpha/da_I = -t/(t²+4),
    d alpha/db_R = -1/(t²+4),
    d alpha/db_I =  2/[t(t²+4)].

Thus gamma=2/[t(t²+4)]>0 and the OUTWARD covector is

    n_t = (-t,-t²/2,-t/2,1),  grad alpha = gamma n_t.

The signs follow from the local constraint alpha<=0: for a stable nearby displacement d, Taylor expansion gives grad(alpha)·d<=O(||d||²). The exact symbolic controls clear the denominator and check all four derivative numerator identities as polynomials in t, along with the two root identities. This goes beyond checking a finite mesh of t values.

## 3. Genuine proximal normals and the metric distinction

For a fixed SPD real G, n_t is a covector; its representing vector is v_t=G^{-1}n_t. The support is n_t^T d = <v_t,d>_G. It is generally wrong to regard the same coordinate tuple n_t as the normal vector in G.

For each fixed t, alpha is smooth in a sufficiently small G-ball of radius r_t about c_t. Taylor's theorem and gamma>0 give a finite K_t such that

    n_t^T(c-c_t) <= K_t ||c-c_t||_G²

for stable c in that ball. Set q=c_t+tau v_t. Then

    ||q-c||_G² - ||q-c_t||_G²
      = ||c-c_t||_G² - 2tau n_t^T(c-c_t)
      >= (1-2tau K_t)||c-c_t||_G².

Choose tau>0 so 2tau K_t<1, and also tau||v_t||_G<r_t/2. Every stable point in the ball other than c_t is strictly farther. For any point outside the open ball, the triangle inequality gives

    ||q-c||_G >= r_t-tau||v_t||_G > tau||v_t||_G = ||q-c_t||_G.

So c_t is an actual attained unique global closest stable point for this normal step. There is no unsupported passage from a merely local stationary normal to a genuine proximal normal, and no need for uniform K_t or a uniform gap.

## 4. The nonproximal limit for every fixed metric

Put n_0=(0,0,0,1), e=(1,0,1,0), f=n_0. Then c_t=t²e+t³f, n_t->n_0, and

    n_0^T c_t=t³,
    ||c_t||_G²=t⁴(A+2Bt+Ct²),
    A=e^TGe>0, B=e^TGf, C=f^TGf>0.

For any fixed tau>0,

    ||c_t-tau G^{-1}n_0||_G² - ||tau G^{-1}n_0||_G²
      = t⁴(A+2Bt+Ct²)-2tau t³ < 0

for all sufficiently small positive t. The stable competitors c_t tend to the base, so even a local proximal-normal interpretation fails. The threshold in t may depend on both G and tau; the theorem asserts each fixed metric, not one threshold uniform over all SPD matrices. Limits of the actual proximal vectors from Section 3 show G^{-1}n_0 is a limiting normal. PRT2000 Definition 1.1 and Proposition 1.2 rule out prox-regularity when such a limiting normal is not itself proximal.

## 5. Projection quantifiers and global attainment

The quadratic formula is

    alpha(a,b)= -Re(a)/2 + Phi(a²-4b)/2,
    Phi(D)=sqrt((|D|+Re(D))/2).

Phi is continuous on C, including its negative real ray and origin. Hence the monic stable set S={alpha<=0} is closed and nonempty. Given any finite input q, comparison with the stable origin bounds a distance-minimizing sequence; in finite dimension it has a convergent subsequence in S attaining the infimum.

The actual PRT2000 Theorem 1.3(a),(k) is used for a CLOSED finite-dimensional set and its actual nearest-point mapping P_C. Weak closedness is automatic here. It equates set prox-regularity at the point with single-valued nearest projection throughout some neighborhood of that point, rather than uniqueness of a locally stationary solution. Failure of prox-regularity therefore means that every neighborhood has an input whose P_S is not single-valued. Attainment excludes empty values. Such a value has at least two DISTINCT coefficient points, each realizing the GLOBAL infimum. An input already in S has the unique zero-distance nearest point itself, so each witness input is unstable.

This is an existence argument from a cited primary theorem, not a computation of a pair. The manuscript expressly makes that distinction. Generic nonconvexity by itself would not have sufficed.

## 6. Full exact-degree coefficients and zero-leading limits

For coordinates (ell_R,ell_I,a_R,a_I,b_R,b_I), the derivative is

    d lambda = -(lambda² d ell+lambda da+db)/(t²-2it).

The two additional derivative components are

    d alpha/dell_R = t²/(t²+4),
    d alpha/dell_I = -2t/(t²+4).

Dividing by gamma gives

    N_t=(t³/2,-t²,-t,-t²/2,-t/2,1),
    N_0=(0,0,0,0,0,1).

Both leading-coefficient directions are present. The previous Taylor-plus-distance argument works in the six-dimensional ambient space. The displacement from (1,0,0) is (0,0,t²,0,t²,t³), so N_0^T displacement=t³ and its squared G-norm is t⁴ times a continuous expression with positive leading coefficient. This gives the same nonproximal limiting normal without appealing to the monic slice as an unsupported transfer.

S_full need not be globally closed because ell=0 is excluded. Locally alpha_full=alpha(a/ell,b/ell) is continuous on ell!=0. Select a closed G-ball B_R about (1,0,0) with all leading coefficients nonzero. C=S_full intersect B_R is nonempty and compact. For small t, the path is in its interior, so its normals and nonproximal limit are the same. For any input q with ||q-base||_G<R/3, each stable point on or outside the boundary has distance at least R-||q-base||_G>2R/3, whereas the stable base has distance <R/3. Thus P_C(q)=P_S_full(q); C supplies attainment and outside competitors cannot tie or improve it. Limits with zero leading coefficient are outside the chosen ball and have this same exclusion. Applying the closed-set characterization to C gives nearby unstable full inputs with distinct attained GLOBAL nearest coefficient polynomials.

## 7. Whole epigraph, including height-mixing metrics

At the path points (c_t,0), the epigraph is locally defined by alpha(c)-r<=0. Its outward covector is (gamma n_t,-1), and positive rescaling gives

    w_t=(n_t,-1/gamma) -> w_0=(n_0,0).

The same construction uses N_t for full degree. The covectors represent normal vectors H^{-1}w_t for ANY fixed real SPD matrix H on joint coefficient/height space. The local smooth constraint and small-step argument prove they are genuine proximal normals in H. The comparison epigraph points have displacement (c_t,0), support w_0^T(c_t,0)=t³, and squared H-norm of order t⁴ with a positive leading coefficient. The cubic support therefore defeats every fixed positive normal step at the height-zero base. The monic epigraph is globally closed; the full version is locally closed in a ball avoiding ell=0, which suffices.

The limiting COVECTOR is horizontal. A mixed H can make its representing VECTOR have a height component. This distinction is necessary: the obstruction does not assume a coefficient/height product metric. It establishes failure of whole-set epigraph prox-regularity, not failure relative to every individual finite function subgradient.

## 8. Exact closed stability chart and edge cases

Write a=x+iy, b=u+iv and substitute z=w-iy/2. The transformed polynomial is

    w²+xw+U+iV, U=u+y²/4, V=v-xy/2.

The imaginary shift does not alter root real parts. The formula for alpha gives stability exactly when x>=0 and

    |x²-4U-4iV| <= x²+4U.

The RHS must be nonnegative before squaring. For x>0, squaring is equivalent to V²<=x²U, which forces U>=0; this also guarantees the RHS sign. For x=0, the UNSQUARED inequality is | -4U-4iV |<=4U, forcing U>=0 and V=0. Conversely these edge conditions satisfy it. Thus the complete closed chart is

    x>=0, U>=0, V²<=x²U.

At U=0 this forces V=0 and the roots are 0 and -x. At x=0, V=0,U>=0 give imaginary roots, with the repeated root included at U=0. If one drops the sign condition while squaring, x=0,U=-1,V=0 incorrectly qualifies even though w²-1 is unstable. This adversarial edge is excluded by the manuscript. For real monic coefficients the chart reduces to a>=0,b>=0, a closed convex orthant. Every SPD squared-distance objective is strictly convex on it and attains a unique minimum.

As an independent credit check, the normalized real quartic boundary a1 a2 a3=a1²+a3² converts under

    x=(a1+a3)/2, V=(a1-a3)/2, U=(a2-2)/(a2+2)

to V²=x²U near (a1,a2,a3)=(0,2,0). This is a smooth local change of coordinates. It explains the inherited positive Whitney-umbrella geometry, but does not preserve every fixed coefficient metric and is not used to transfer the projection conclusion. Bottema's criterion has repeated-root exclusions, so it is credited for boundary geometry, not imported as the complete closed-stability criterion.

## 9. Scalar subdifferentials needed for the positive proposition

Let L=(-infinity,0] inside C. For D=x+iy outside L and r=|D|,

    grad Phi(D)=(Phi(D)/(2r), y/(4r Phi(D))).

Using y²=(r+x)(r-x) gives ||grad Phi(D)||²=1/(4r). Hence its norm is 1/(2sqrt(r)) and diverges on every off-ray approach to zero.

At D=-s<0, rationalization and smooth expansion of the denominator give

    Phi(-s+h)=|Im(h)|/(2sqrt(s))+O(|h|²).

Real increments of both signs force the real component of a regular or proximal subgradient to be zero; imaginary increments bound its imaginary component to the interval |q_I|<=1/(2sqrt(s)). The displayed expansion gives a quadratic lower support for every point of that interval. The two off-ray gradient limits yield the endpoints, while on-ray proximal subgradients yield the whole interval. No extra limiting subgradients arise. All three subdifferentials equal this imaginary interval.

For |D|<=delta, the distance estimate

    Phi(D)>=dist(D,L)/(2sqrt(delta))

holds: if Re(D)>=0, dist=|D| and Phi²>=(|D|)/2>=(|D|²)/(4delta); if Re(D)<0, rationalize to |Im(D)|/sqrt(2(|D|-Re(D))) with denominator <=2sqrt(delta).

At zero, a subgradient q must have Re(q)>=0 by negative real increments. Conversely every such finite q belongs to the convex normal cone N_L(0), and

    q·D <= |q| dist(D,L) <= Phi(D)

on a sufficiently small ball chosen depending on q. This is a local LINEAR lower support, hence a proximal and regular support. Bounded off-ray gradients cannot converge to any finite q at zero. Bounded on-ray subgradients are imaginary and belong to N_L(0). Constant base sequences include every proximal subgradient at zero in the limiting definition. Therefore regular, proximal, and limiting subdifferentials at zero all equal {q:Re(q)>=0}. Negative real components are excluded; arbitrary finite imaginary components are included.

## 10. Exact coefficient transport; bounded-gradient localization

F(a,b)=(a,D=a²-4b) is a global real smooth diffeomorphism with inverse b=(a²-D)/4; its real Jacobian determinant is 16. Transforming first-order supports by its Jacobian and quadratic supports by Taylor's theorem, then taking limits through the continuous inverse Jacobian, transports the three subdifferentials exactly. The additive -Re(a)/2 term and positive factor 1/2 give

    v=-e_aR/2 + J_D(a,b)^T q/2,
    v_b=-2q, v_a=-1/2+conj(a)q,
    q in partial Phi(D),

where complex tuples represent the real pairing. At the origin, EVERY finite limiting subgradient is

    v_0=(-1/2,0,-2q_R,-2q_I), q_R>=0.

The relation v_b=-2q eliminates a possible cancellation of divergent scalar gradients by small a: a bounded neighborhood of the finite v_0 directly bounds |q|<=M. It is not enough to look only at the a components. Take M>=1 and delta=1/(16M²). Inside a coefficient ball with |D|<delta, an off-ray subgradient would have norm greater than 2M, contradicting the bound. Thus every nearby base admitting a subgradient close to v_0 lies on D_x in L, where Phi(D_x)=0 and q in N_L(D_x).

For a comparison point y anywhere in that ball, let z be the Euclidean projection of D_y onto L. Convex-normal support gives q·(z-D_x)<=0, so

    q·(D_y-D_x) <= M dist(D_y,L) <= Phi(D_y).

This comparison does not restrict y's subgradient. The exact discriminant remainder is

    D_y-D_x = J_D(x)(y-x) + (Delta a)².

Consequently

    alpha(y) >= alpha(x)+v·Delta + q·(Delta a)²/2
             >= alpha(x)+v·Delta - M||Delta||²/2.

Taking the PR2010 curvature r=M+1 yields STRICT positive slack at least ||Delta||²/2 whenever y!=x. This is the actual strict Definition 1.1, not merely a non-strict version. Continuity gives the required function-attentive localization, and the proof already holds without the additional function-value filter.

For explicit compatible constants one may set M=max(1,(||v0_b||+1)/2), delta=1/(16M²), and epsilon=min(1,delta/10). If ||v-v0||<epsilon then |q|<=M, while coefficient norm <epsilon implies |D|<=epsilon²+4epsilon<=5epsilon<delta. Thus there is no circular choice of the coefficient and subgradient neighborhoods.

The adverse zero-discriminant comparison with x=0, q=M>0, a_y=i tau, b_y=-tau²/4 has alpha(y)=0 and v0·y=M tau²/2. Its norm squared is tau²+tau⁴/16. The required curvature approaches M as tau approaches zero, demonstrating why a common bound independent of v0 is not obtained. The permitted r=M+1 succeeds with strict slack. The independent rational controls include this case and its imaginary-q analogues up to M=10^6 and tau=10^-12; the support argument is analytic for all finite M.

## 11. Why the negative epigraph and positive function statements coexist

Along c_t the unscaled gradients are gamma n_t, with gamma asymptotic to 1/(2t), and diverge. After positive scaling, their epigraph covectors approach (n0,0). A finite function subgradient corresponds to (v0,-1), whose height covector component is nonzero. The horizontal obstruction never supplies a violation localized near such a finite v0. The scalar bound and coefficient support above prove the positive function condition directly. No conclusion for function prox-regularity under all mixed metrics is asserted.

## 12. Prior parameter examples and nontransfer

Cross's Example 5.38 uses a two-real-parameter matrix with characteristic coefficient map (x1,x2)->(a=0,b=-x1²+x2²), whose derivative vanishes at zero. Its abscissa is h=max(0,sqrt(x1²-x2²)) on the appropriate piece. The stable parameter set is the wedge |x1|<=|x2|. The Euclidean nearest parameter points to (c,0), c>0, are (c/2,c/2) and (c/2,-c/2), but both have b=0 and are the SAME coefficient polynomial z². The parameter metric and rank-deficient map cannot deliver the claimed distinct coefficient projection ties. The current paper correctly credits the parameter function example and supplies a separate ambient proof. The printed scalar evaluation defect identified in the bounded source reading is not a premise of the paper or this proof.

## Conclusion of the independent analytic work

No counterexample or missing step was found in Theorem 1, Remark 2, or Proposition 3 at the stated quantifiers. The global projection existence rests on the actual primary PRT2000 equivalence at its stated closed-set scope. Every other special-case identity, support comparison, localization, and discriminant remainder above is independently derived. Finite controls corroborate those deductions and do not replace them. This is an AI adversarial mathematical review, not human peer review or formal proof-assistant certification.
