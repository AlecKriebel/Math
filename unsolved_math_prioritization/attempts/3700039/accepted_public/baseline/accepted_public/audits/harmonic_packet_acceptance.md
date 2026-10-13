# Independent acceptance of fourth-pass harmonic packets

## Decision, normalization, and scope

The [critical-layer report](../proofs/packets/REPORT.md) and [fixed-harmonic embedding](../proofs/packets/HARMONIC_EMBEDDING.md) are accepted under their stated hypotheses. No mathematical correction is required. The radial-curvature-defect theorem, explicit two-harmonic packet construction, and arbitrary fixed harmonic-polynomial embedding are valid. The unrestricted normalized-supremum conjecture remains unresolved.

The explicit center numerator is **-3 sqrt(3)/2**, its actual joint maximum is **2**, and its limiting quotient is **-3 sqrt(3)/4**. Both frozen reports already use this normalization correctly. The more general embedding transfers the accepted fixed-radius sharp lower infimum **-pi** to honest records of smooth all-flat triples, as an infimum over the class. It does not claim a single triple attains limit -pi. Both constructions have positive radial gaps with quotient exactly **2 pi**; their supremum and small-radius limsup are therefore exactly 2 pi.

This is an audit within the fourth shared substantive pass, not a fifth research pass. No historical novelty claim is made. The source target is A. Eremenko, *Conjectured inequality for subharmonic functions*, 4 April 2015, https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. Its harmonic and homogeneous affirmative cases remain credited prior results. All integrals use unnormalized angular measure. Quotients use actual B>0 radii; no equivalence to assigning zero to 0/0 is asserted.

## 1. Radial-curvature defect: the sign, kernel, and hypotheses

For a fixed C2 circle profile h_j(theta)=U_j(t_*,theta), set

R_j=(U_{j,tt}-lambda^2 h_j)^+.

The pointwise cylindrical subharmonicity hypothesis gives

h_j''+lambda^2 h_j >= lambda^2 h_j-U_{j,tt} >= -R_j.

For ell=pi/lambda, integration by parts using

    [sin(lambda s) h_j'(theta+s)-lambda cos(lambda s) h_j(theta+s)]'
    = sin(lambda s)[h_j''+lambda^2 h_j](theta+s)

gives exactly the report's half-period identity. Its kernel sin(lambda s)/lambda is nonnegative on [0,ell] and has integral 2/lambda^2. Neither an integer lambda nor a shift dividing 2 pi is needed. Periodically extend each profile before applying the identity, including when ell exceeds one whole period.

Writing e_j as that kernel applied to R_j gives h_j(theta+ell)>=-h_j(theta)-e_j(theta). Coordinatewise monotonicity, sign reversal, and maximum-norm Lipschitz continuity of the median yield

median(h(theta+ell))+median(h(theta)) >= -max_j e_j(theta).

Circle translation invariance and Fubini now give

2 I >= -integral max_j e_j >= -sum_j integral e_j
    = -(2/lambda^2) sum_j ||R_j||_1.

Both factors of two are accounted for. The sharper maximum-error integral and the separable bound in the report are therefore correct. Replacing the positive radial-defect part by the negative part is invalid: the locally harmonic constant triple U_j=-1 has negative median and identically zero negative part of U_{j,tt}-lambda^2 U_j. This control concerns the theorem's local C2 hypotheses; it is not proposed as a normalized whole-plane input.

For U_j=F g_j, direct differentiation gives

U_{j,tt}-(F''/F)U_j = F(g_{j,tt}+2(F'/F)g_{j,t}).

Thus Corollary 2 follows with kappa=F''/F>0 and lambda^2=kappa. The L1 norm of the positive part is at most ||g_{j,tt}||_1+2|beta|||g_{j,t}||_1. Under bounded F/B and |beta|/sqrt(kappa), the two little-o assumptions make the normalized loss vanish. The weaker direct positive-part condition retains the bounded F/B assumption. Nothing here differentiates the actual B, assumes radial differentiability of a maximizing angle, or asserts that the condition automatically holds in every flat example.

The necessary lower bound for a uniformly negative quotient follows by combining I/B>=-R/(lambda^2 B) with I/B<=-epsilon. A negative value on one selected circle does not imply the uniform premise.

### Distributional boundary of the result

The audited radial-defect theorem explicitly assumes U_j are C2 near the selected circle. Its fixed-circle derivatives, ordinary positive parts, Green formula, and Fubini argument are consequently legitimate. It does not purport to restrict an arbitrary distribution U_{tt} to a chosen circle. For a general nonsmooth subharmonic function such a restriction need not exist; even angular smoothing can retain a radial derivative jump, as the circular mean of log|z-1| is max(t,0). No unsupplied nonsmooth or all-subharmonic extension of the radial-defect criterion is accepted or needed. The constructed triples satisfy the stronger C-infinity hypotheses everywhere.

## 2. The harmonic layer and its actual denominator

Each mode exp(mx)cos(my+phase) is harmonic. For the two-mode input every value is bounded above by exp(x)+exp(2x), with equality at j=0,y=0 for every x. Hence the actual joint maximum is that amplitude sum in this particular example, and equals 2 at x=0.

The root-of-unity shifts permute the triple under y->y+2pi/3; reflection also permutes it. On 0<=y<=pi/3, put X=cos y, Y=cos(y-2pi/3), Z=cos(y+2pi/3). Then X>=Y>=Z, X+Y+Z=0, X in [1/2,1], Y in [-1/2,1/2], and Z in [-1,-1/2]. For f(v)=v+2v^2-1,

f(X)-f(Z)=(X-Z)(1-2Y)>=0,
f(Z)-f(Y)=(Z-Y)(1-2X)>=0.

The median is therefore f(Z), with consistent values at ties. Its sector integral is -sqrt(3)/4, so the full numerator is -3sqrt(3)/2. Division by the attained maximum gives -3sqrt(3)/4. For x<=0, (exp(x)+exp(2x))/2<=exp(x)<=exp(x/2), which is the claimed one-sided growth control. A harmonic layer with this negative median does not contradict the source's affirmative harmonic supremum result.

## 3. Both cutoff transitions and the common radial repair

The full second derivative of chi_L=eta(x+L)eta(L-x) includes a mixed derivative term. For L>=3 the two transition intervals [-L,-L+1] and [L-1,L] are disjoint, and the inactive factor is identically one throughout either interval. All mixed derivative terms therefore vanish there. Outside the two intervals, both cutoff derivatives vanish. On either transition, |chi'|<=||eta'|| and |chi''|<=||eta''||.

On the inner transition, the two-mode |H_j| and |H_{j,x}| are bounded by 2exp(x) and 3exp(x). On the outer transition they are bounded by 2exp(2x) and 3exp(2x). Consequently C=2||eta''||+6||eta'|| bounds the absolute value of the signed forcing chi''H_j+2chi'H_{j,x} by the relevant exponential. The function zeta equals one precisely where the corresponding cutoff derivatives can be nonzero. Its positive padding creates no new adverse sign because F_L''=R_L>=0.

For the general polynomial, the corresponding bounds are S exp(m_0 x), dS exp(m_0 x) on the inner transition, and S exp(dx), dS exp(dx) on the outer transition. This gives exactly C=S(||eta''||+2d||eta'||). The polynomial coefficients may have arbitrary signs and phases; the absolute-value bounds do not assume favorable forcing. The same scalar positive repair works simultaneously for all three components, including zero components.

The inner source support is [-L-1,-L+2], and the outer support is [L-2,L+1]. The angular support is [-L,L]. The correction itself is not compactly supported: it is zero before -L-1 and is nonnegative, nondecreasing, and affine after L+1. The construction correctly retains every affine tail.

For x<=0 the outer source has not begun. Integrating the dominating source Cexp(m_0 s) yields F_L(x)<=Cexp(m_0 x)/m_0^2. Its inner source has length at most three, height at most Cexp(-m_0 L+2m_0), and distance to zero at most L+1. Thus F_L(0)<=3C exp(2m_0)(L+1)exp(-m_0 L), with the matching first derivative bound without L+1. These are the stated K_0 bounds, including m_0=1 in the explicit case.

The total source mass is at most 6C exp(dL+2d), and every source point is at least -L-1. Hence F_L(x)<=6C exp(dL+2d)(x+L+1) for x>=-L-1. The angular term has absolute value at most S exp(dL) on its support. The reported K=S+6Cexp(2d) upper envelope follows; the explicit case has S=d=2 in this bound. All future tails are included.

An exact adverse-sign control uses the usual smooth step eta(s)=exp(-1/s)/(exp(-1/s)+exp(-1/(1-s))) on (0,1). At its midpoint, eta'=2 and eta''=0. The single harmonic mode exp(x)cos y then has negative uncorrected forcing at the inner midpoint with y=pi and at the outer midpoint with y=0. Thus either transition genuinely requires a repair; subharmonicity is not being inferred from the core alone.

## 4. Scale selection, separation, and the full infinite past

The selected N exists because each finite constant is dominated by the stated exponential decay. Monotonicity of the inequalities for all n>=N is also valid. In the last condition, after dividing by the right-hand side, the first term is a constant times (sqrt(n)+1)exp(-m_0 sqrt(n)/2), which decreases once m_0(sqrt(n)+1)>2. The second is a constant times exp(-n/4+m_0 sqrt(n)/2), which decreases for sqrt(n)>m_0. The general lower bound N>=256(d+1)^2 guarantees both. The explicit case has m_0=1 and N>=400. The other two inequalities are plainly decreasing.

Neighboring centers are log 2 apart. The sum of their half-widths is below 4/sqrt(N)<=1/5<log 2 in the explicit construction, and smaller in the general construction. Hence the J_k are disjoint, all outer-index packets vanish for t<=t_k, and every inner packet has finished before the final core [-L_k/2,0] of packet k. This core lies after the kth inner source too: -L+2<=-L/2 because the actual L>=20. The preliminary condition L>=3 alone would not establish that last fact; the construction's stronger scale choice does.

For an inner packet, let sigma_l=t_l-(L_l+1)/n_l. The all-x envelope is K a_l exp(dL_l)[1+n_l(t-sigma_l)] for t>=sigma_l and zero earlier. Multiplying by exp[-M(t-t_k)], taking the supremum over t-sigma_l>=0, and using

sup_(v>=0)(1+n_l v)exp(-Mv)<=1+n_l/M

gives the reported bound valid for every real t, including both transitions. It is not a center-only or truncated-past estimate.

For p=l-k>=1, the elementary inequality 2^p-1-p log(2)/2>=2^(p-2) follows from log 2<1 and the induction 3*2^p>=4+2p. For the explicit slope M=n/2, the remaining positive exponent is at most (9/4)sqrt(z)+1/4 with z=n2^p. This is at most z/8 for z>=400: the remainder at sqrt(z)=20 is positive and increasing thereafter. Thus the full exponent is at most -z/8.

For the general slope M=qn, q<1/4, the positive remainder is at most (d+1/8)sqrt(z)+1/8. The choice sqrt(n)>=16(d+1) makes this at most z/8, again with a positive increasing remainder. The same -z/8 bound follows.

Finally, 2^p>=2p gives the complete geometric majorants

sum_(p>=1)(1+2^(p+1))Q^(2^p)
 <= Q^2[1/(1-Q^2)+4/(1-2Q^2)] <=6Q^2,

sum_(p>=1)(1+2^p/q)Q^(2^p)
 <= Q^2[1/(1-Q^2)+(2/q)/(1-2Q^2)] <=(2+3/q)Q^2

for 0<Q<=1/4. These are exactly T_k=6Kexp(-n_k/4) and T_k=K_qexp(-n_k/4). Every completed inner tail and every more distant active inner packet is covered, uniformly over the entire past.

## 5. Actual honest records in the explicit construction

For x<=-L/2, the kth weighted envelope is bounded by a(C+2)exp(x/2)<=a/2, while all inner packets together contribute at most aT_k<=a/2. The actual center maximum is at least 2a. Thus the entire earlier region is strictly below the center in the weighted comparison.

On -L/2<=x<=0, the kth cutoff is one and every radial contribution is affine. Their common baseline D_k is nonnegative and nondecreasing, and D_k(0)<=exp(-L/2)<=exp(x). With no other angular term active, the actual maximum is exactly

b(t)/a=exp(x)+exp(2x)+D_k(x).

Its derivative minus one half its value is

(exp(x)-D_k(x))/2+(3/2)exp(2x)+D_k'(x)>=0.

The weighted actual maximum is therefore nondecreasing all the way to the center. Combined with the earlier bound, this establishes the honest record inequality for every s<=t_k, not merely locally or at sampled radii. It also gives the accepted integrated record moment A(t_k)/b(t_k)<=1/M_k^2 by direct integration of the exponential envelope.

At the center, a common scalar baseline shifts the median by that same scalar. Integer n_k preserves the full circle integral. Consequently

b(t_k)=a_k(2+delta_k),
I(exp t_k)=a_k(2pi delta_k-3sqrt(3)/2),

with delta_k->0. The claimed limit follows with the actual denominator.

## 6. General harmonic inputs: actual convex maximum and a positive slope

For every nonzero fixed joint harmonic-polynomial collection with h_j(0)=0, some component is nonzero on every positive-radius circle. Its zero circle mean forces a strictly positive maximum. Thus b_H(x)>0 for all real x. The maximum over the compact angular circle and the finite component set is continuous.

Harmonic comparison on annuli with an affine function of log radius proves convexity of b_H. For strict increase, suppose two different radii had the same positive maximum. A component attaining that value on the inner circle is bounded above by it on the outer disk. The strong maximum principle would make the component the same positive constant, contradicting h_j(0)=0. This proves strict increase without assuming differentiability of a maximizing angle.

The finite joint leading expansion is uniform in y, so

b_H(x)=exp(m_0 x)[c+O(exp x)],
c=max_j sqrt(A_(j,m_0)^2+B_(j,m_0)^2)>0.

It follows that b_H(x-1)/b_H(x)->exp(-m_0). Both functions defining eta_0 and c_* are continuous and positive on (-infinity,0], with strictly positive limits at negative infinity. A compact-interval/tail split therefore proves eta_0,c_*>0. Also eta_0<1. Setting q=eta_0/4 gives 0<q<1/4.

The left derivative of a finite convex function dominates its unit backward secant. Hence b'_(H,-)(x)>=b_H(x)-b_H(x-1)>=4q b_H(x). In particular, this holds almost everywhere for the ordinary derivative. The proof needs convexity of b_H, not convexity of log b_H, which can fail. For example, Re(z-z^2) has actual maximum r-r^2 for 0<r<=1/4 and r^2+1/8 for r>=1/4. On the first branch, b b''-(b')^2=-r^3<0, with derivatives in log radius. Its actual unit-circle maximum is 9/8, not the coefficient sum 2. This control confirms why the report's actual-maximum method is needed.

The early-region argument bounds the total weighted maximum by a_k C_0/2, while the center maximum is at least a_k C_0. On the final core the common baseline satisfies D_k(x)<=D_k(0)<=c_*exp(-m_0 L_k/2)<=b_H(x), and

b(t)/a_k=b_H(x)+D_k(x).

Almost everywhere, its derivative minus q times its value is at least

2q b_H(x)+q(b_H(x)-D_k(x))+D_k'(x)>0.

Finite convex b_H is locally Lipschitz, so the weighted maximum is absolutely continuous on each compact core interval. The almost-everywhere derivative inequality proves true interval monotonicity, even across maximizing-angle or maximizing-component switches. This supplies the complete honest-record inequality with slope qn_k.

There is no exclusion of zero components, repeated components, opposite components, missing intermediate degrees, or ties. A constant input component must be zero because h_j(0)=0; it receives the same radial repair as the others. The all-zero triple is expressly excluded, exactly where C_0, m_0, and the normalization would otherwise fail. At least one nonzero degree guarantees finite d>=m_0>=1, S>0, and positive C. Thus all stated degeneracies are covered without redefining a denominator.

## 7. Infinite-series smoothness, origin, and future extension

On a fixed compact t interval, only finitely many packets can have active angular terms or active curvature. All sufficiently large indices have completed affine radial tails. The all-x envelope gives those tails a bound by exp(-n_k+d sqrt(n_k)) times a fixed polynomial in n_k, log n_k, and bounded |t|. Their series and first t-derivative series converge uniformly. Higher cylindrical derivatives of completed tails vanish. This proves C-infinity convergence locally on the punctured plane and permits termwise computation of the Laplacian. Every summand has nonnegative cylindrical Laplacian; the planar Laplacian is its positive r^-2 multiple.

For flatness put Q=1/r. An active packet has n_k comparable to Q, since |log(n_k/Q)|<=(sqrt(n_k)+1)/n_k. A completed inner packet has n_k>=cQ for one fixed c>0 near the origin. Since d is fixed, exp(-n_k+d sqrt(n_k))<=exp(-n_k/2) eventually. Every fixed derivative of an active packet contributes only powers of n_k, fixed cutoff-derivative constants, and powers of 1/r from Cartesian conversion. Completed tails are affine in log r: their zeroth derivatives have at most the additional factor 1+n_k log(n_k/Q)+sqrt(n_k), and each positive-order Cartesian derivative of log r is bounded by a fixed constant times r^-|alpha|. The inequality |log(n_k/Q)|<=n_k/Q+O(1) in this completed region turns that factor into a polynomial bound.

The dyadic tail sum of any such polynomial times exp(-n_k/2), over n_k>=cQ, is bounded by a polynomial in Q times exp(-c'Q). It follows for every multi-index alpha that

|partial^alpha u_j(z)|<=C_alpha exp(-c_alpha/r)r^-p_alpha.

All derivatives tend to zero faster than every power. Repeated differentiation, or induction with difference quotients, then extends each derivative by zero at the origin and gives a C-infinity function flat to every order. Its Laplacian is zero at zero and nonnegative elsewhere. There is no hidden atom, singular gluing term, or loss of subharmonicity at the accumulation point.

Beyond the outermost J_0, every angular and curvature packet has finished. The convergent sum is a common affine function of log r. This gives the stated whole-plane extension directly; no uncontrolled outer cutoff or future repair is omitted.

## 8. Positive denominators, all-radii conclusions, and C-infinity layers

At every positive radius, infinitely many sufficiently inner packets have completed. Each has a strictly positive radial correction because R_L is a nonzero nonnegative source. Every harmonic angular term has zero angular mean, including on its transitions. Thus each component's circle mean is strictly positive, proving B(r)>0 at every r>0.

In every gap all angular terms vanish. The three components equal the same strictly positive baseline, giving I/B=2pi exactly. Such gaps accumulate at zero. At every other radius the pointwise median is at most the actual B, so I/B<=2pi. Therefore both the global supremum and the small-radius limsup are exactly 2pi. No examination limited to the negative record subsequence can change that conclusion.

On a fixed rescaled compact set, the kth cutoff eventually equals one and all other angular packets vanish. The kth inner repair is affine there, with its value and slope tending to zero after division by a_k. Inner completed tails have the same property: the uniform weighted tail estimate bounds their values at both endpoints of any slightly larger fixed x interval by a quantity tending to zero. Since their sum is affine on that interval, its slope tends to zero too. Higher x derivatives vanish and all y derivatives of the baseline vanish. This proves C-infinity convergence on every compact subset of R^2, not merely uniform or distributional convergence. Normalization uses b(t_k)/a_k->2 or C_0 respectively.

The first-pass Fejer input is an accepted fixed finite harmonic-polynomial triple for each desired accuracy, with J_0/C_0 approaching -pi. Apply the audited embedding separately to each such fixed input. Its q may depend on the chosen input but remains strictly positive, so qn_k tends to infinity. The universal lower bound I/B>=-pi remains applicable to every constructed triple, while the limiting record quotient can be made arbitrarily close to -pi from above. This is exactly the claimed class sharpness, with no changing-degree input hidden inside a single embedding and no claim of an attained lower endpoint.

## 9. Verification and preservation

The original main and embedding author outputs reproduce byte for byte in normal, -O and -OO modes, with 57 and 33 checks respectively. The [main author certificate](../certificates/packet_author.json) retains every mathematical field and rebinds only its report hash to the display-repaired public proof. The [embedding author certificate](../certificates/embedding_author.json) and its report remain byte-identical. The public identity projection is checked separately after exact original-output reproduction.

The [independent audit certificate](../certificates/packet_audit.json) comes from a separate reconstruction that does not import either author calculation and uses no angular quadrature. It passes 59 exact and finite-exhaustive controls, including 15,625 median-shift pairs and 343 universal-bound triples. It reconstructs the Green primitive, envelope defect, sector numerator and actual maximum, full cutoff product rule, repair moments, both tail absorptions, full dyadic sums, record margins, general normalization, actual cancellation maximum, and a finite Fejer error certificate. Adverse controls reject the wrong radial-defect sign, wrong lambda power, mean error in place of maximum error, doubled two-mode quotient, uncorrected transitions, inadequate core scale, coefficient-sum denominator, and log-convexity of the actual harmonic maximum.

These computations supplement the complete analytic arguments above. No finite sampling certificate is substituted for all-radii records, smoothness, infinite-tail convergence, or the unresolved target. The [reader reproduction guide](../REPRODUCTION.md) explains the exact values and their limits; the [public manifest](../MANIFEST.json) binds included mathematical files only.
