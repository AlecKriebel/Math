# Negative-p Aleksandrov concentration: scoped results

Problem 30004953, OWR-8415364-011. Author research record, 5 October 2026.

**Status:** The full problem for every n >= 2 and p <= -1 is unresolved here. The results below include a complete candidate for the separately identified planar p = -1 threshold and an all-dimensional p = -1 sufficient condition. Independent review is pending. No novelty, priority, human verification, or editorial acceptance is asserted.

## 1. Conventions and exact scope

Let sigma denote ordinary surface measure on S^(n-1), and let omega = sigma(S^(n-1)). A convex body has nonempty interior. K_o^n denotes bodies containing 0 in their interiors; K_e^n denotes the origin-symmetric members. Write rho_K for the radial function and h_K for the support function. The curvature measure in this problem is

    J(K,A) = sigma(alpha_K(A)),       dJ_p(K,u) = rho_K(u)^p dJ(K,u),

where alpha_K is the radial Gauss image. Equivalently, J is the pushforward of sigma under the almost-everywhere uniquely defined map taking a normal direction to the radial direction of its supporting point. In particular,

    J(K,S^(n-1)) = omega,      J_p(aK,.) = a^p J_p(K,.).

These are radial-direction measures. The surface-area measure S_p is different. For the standard dual convention with a factor 1/n,

    J_p(K,.) = n * Ctilde_(p,0)(K*,.),

with the **polar** K*. Neither dropping the polar nor treating negative p here as a negative dual index q is legitimate. In smooth support-function PDE descriptions the support function is accordingly that of the polar body. No dual-Minkowski concentration theorem is transferred without this identification.

The original OWR sufficient theorem concerns finite, nonzero, **even** Borel measures. The catalog's short question suppresses this hypothesis and the origin-symmetric conclusion. Those hypotheses are restored throughout. Here n >= 2 and p = -s, s >= 1, unless explicitly stated otherwise. Every great subsphere is S^(n-1) intersected with a proper nonzero linear subspace; for a single uniform bound it is equivalent to test hyperplanes, because each smaller subspace lies in a hyperplane. Dimension-sensitive assertions will always name the subspace dimension. Ratios are normalized by total mass. By homogeneity it suffices to work with a probability measure mu; rescaling the resulting body recovers any positive total mass.

Define

    beta_(n,s) = exp[-(s/2)(psi(n/2)-psi(1/2))].

The cited OWR/Mui sufficient condition is mu(S intersect L) <= beta_(n,s) for all proper L. It is a sufficient condition, not a necessary condition for individual solvable measures.

### Separate subproblem solved by the argument below

For n = 2 and p = -1, determine the largest possible universal concentration threshold for even measures. The candidate answer is

    a_2 = pi/(pi+2).

Every even probability measure with mu({v,-v}) < a_2 for every v has an origin-symmetric solution. At equality there is an even four-atom measure having no solution at all, including nonsymmetric bodies. Consequently, for conditions written with <= c, every c < a_2 works and c >= a_2 fails: the supremum is a_2, but there is no largest admissible closed-inequality constant. This distinction is essential.

## 2. Compactification and a correct endpoint argument

For s > 0 define

    I_s(K) = integral rho_K(u)^s dmu(u),
    H(K) = (1/omega) integral log h_K(v) dsigma(v),
    F_s(K) = (1/s) log I_s(K) - H(K).

This functional is scale invariant. We extend it to nonzero origin-symmetric compact convex sets, including lower-dimensional ones, taking rho_K = 0 outside span(K) and F_s = -infinity if I_s = 0. Sets are normalized to have circumradius 1. Denote this compact class by D. Hausdorff compactness follows from Blaschke selection, and circumradius 1 prevents the zero set from appearing.

### Lemma 2.1 (entropy continuity and radial upper semicontinuity)

On D, H is finite and continuous, I_s is upper semicontinuous, and F_s is upper semicontinuous.

**Proof.** If v is a unit point of K, then [-v,v] is contained in K, so

    |v dot u| <= h_K(u) <= 1.

Thus 0 <= -log h_K(u) <= -log|v dot u|, whose spherical integral is finite. If K_j -> K, choose unit v_j in K_j and pass to a subsequence with v_j -> v. Support functions converge uniformly, and -log h_(K_j) converges almost everywhere to -log h_K. The nonnegative majorants -log|v_j dot u| converge almost everywhere and have the same finite integral by rotation invariance. Scheffe's lemma gives L1 convergence of these majorants, hence uniform integrability. The generalized dominated-convergence theorem gives H(K_j) -> H(K). The subsequence argument gives continuity for the original sequence as well.

For each fixed u, any subsequential limit r of rho_(K_j)(u) satisfies r u in K, so limsup rho_(K_j)(u) <= rho_K(u). Since 0 <= rho_(K_j)^s <= 1, reverse Fatou gives limsup I_s(K_j) <= I_s(K). Taking the increasing continuous logarithm proves the assertion when I_s(K)>0; if I_s(K)=0, the logarithmic term tends to -infinity while H stays finite. QED.

**Important caution.** Radial functions need not converge pointwise under Hausdorff convergence to a lower-dimensional set. For example, take ellipses with semiaxes 1 and epsilon^2, rotated through angle epsilon. They converge to the unit horizontal segment, but their radial value in the horizontal direction tends to 0 rather than 1. We use upper semicontinuity, not the false unrestricted pointwise assertion.

### Lemma 2.2 (the compact maximum equals the original supremum)

F_s attains a finite maximum on D. This maximum equals its supremum over K_e^n.

**Proof.** Put C_n = exp[(psi(n/2)-psi(1/2))/2]. The preceding segment bound gives H(K) >= -log C_n, while I_s(K)<=1. Therefore F_s <= log C_n. The unit ball has F_s = 0. Upper semicontinuity and compactness give a maximizer with finite value. For a possibly degenerate K, the full-dimensional sets K+epsilon B decrease to K as epsilon decreases to 0; their radial functions decrease pointwise to rho_K. Their entropies converge by Lemma 2.1 after harmless radius normalization. Dominated convergence for I_s proves F_s(K+epsilon B)->F_s(K), including a limit of -infinity if appropriate. Scale invariance completes the claim. QED.

### Lemma 2.3 (interior maximizers solve the equation)

If a full-dimensional K maximizes F_s, then a positive dilation of K solves J_(-s)(K,.)=mu.

**Proof.** For continuous even g, put f_t(u)=rho_K(u) exp(t g(u)) and K_t=conv{f_t(u)u:u in S^(n-1)}. Its radial function dominates f_t. Hence

    (1/s) log integral f_t^s dmu - H(K_t) <= F_s(K_t) <= F_s(K),

with equality at t=0. For almost every normal v, the supporting point of K is unique (by almost-everywhere differentiability of its Lipschitz support function). The envelope derivative of log h_(K_t)(v) is g(u(v)), where u(v) is that supporting point's radial direction. Moreover the difference quotient is bounded by ||g||_infinity, because exp(-|t| ||g||)h_K <= h_(K_t) <= exp(|t| ||g||)h_K. Dominated convergence and the pushforward definition of J give

    d/dt H(K_t)|_0 = (1/omega) integral g dJ(K).

Both positive and negative t are available. Differentiating the displayed maximality inequality at 0 therefore yields

    (1/I_s(K)) integral g rho_K^s dmu = (1/omega) integral g dJ(K).

Both measures are even, so equality against all continuous even functions gives equality of measures. Thus J_(-s)(K,.) = (omega/I_s(K)) mu. For a=(omega/I_s(K))^(1/s), the scaling identity gives J_(-s)(aK,.)=mu. QED.

This proof supplies the variation calculation explicitly; it does not require assuming that every solution is a global maximizer.

### Proposition 2.4 (recovery of the cited sufficient constant)

For every s>0, if mu is even and mu(S intersect L)<=C_n^(-s) for every proper L, a full-dimensional maximizer exists, hence the desired body exists.

**Proof.** A degenerate K in D with span L has I_s(K)<=mu(S intersect L), while H(K)>=-log C_n. Therefore F_s(K)<=0. If the maximum over D is positive, all its maximizers are full dimensional. If that maximum is 0, the unit ball already attains it and is full dimensional. Apply Lemma 2.3. QED.

This is a derivation of the established bound, not a novelty claim. Merely obtaining a non-strict comparison with the ball does not contradict maximality; the second case above is the correct endpoint argument.

## 3. Convex-hull thickening and excluded collapse dimensions

Let L be k-dimensional, 1<=k<n, origin symmetric, with span E. Assume its circumradius is 1 and r B_E is contained in L for some r>0. Let g_L be its gauge on E. Form the join

    Q_t = conv(L union t B_(E-perp)),        0<t<1.

This is full dimensional and remains in D. For u=x+y with x in E, y in E-perp,

    rho_(Q_t)(u) = 1/(g_L(x)+|y|/t),
    h_(Q_t)(u) = max(h_L(x), t|y|).

The first identity follows by writing the convex hull as g_L(x)+|y|/t<=1; the second is the support function of a convex hull. On E the radial function is unchanged.

### Lemma 3.1 (entropy cost)

As t decreases to 0,

    0 <= H(Q_t)-H(L) = O(t^k).

**Proof.** Since h_L(x)>=r|x|, the integrand is at most log max(1,t|y|/(r|x|)). For uniform U on the sphere, R=|P_E U| has density

    f(R) = [2/B(k/2,(n-k)/2)] R^(k-1)(1-R^2)^((n-k)/2-1),  0<R<1.

The integrand vanishes unless R<t/r. For sufficiently small t this lies below 1/2, where the last density factor is bounded. Consequently its integral is at most a constant times

    integral_0^(t/r) R^(k-1) log((t/r)/R) dR = (t/r)^k/k^2.

This proves the bound. QED.

### Proposition 3.2 (collapse ranks k>s are impossible for maximizers)

Suppose mu is not concentrated in a proper linear subspace. A maximizer of F_s in D cannot have dimension k>s.

**Proof.** Such a maximizer L must have I_s(L)>0 by Lemma 2.2. Outside E, g_L(x)<=1/r and |y|<=1, whence

    rho_(Q_t)(u) >= t/(1+t/r).

Thus

    I_s(Q_t)-I_s(L) >= mu(S outside E) [t/(1+t/r)]^s,

with positive coefficient. The logarithmic gain in F_s is bounded below by a positive constant times t^s for small t. Lemma 3.1 bounds the entropy loss by O(t^k). If k>s the gain wins, contradicting maximality. QED.

For s=1 the only remaining possible degenerations are line segments. For general s>=1 this leaves ranks 1,...,min(n-1,floor(s)); no argument here excludes those ranks uniformly.

## 4. A sharper p=-1 sufficient condition

Define

    d_n = 2 Gamma(n/2)/(sqrt(pi) Gamma((n-1)/2)),
    a_n = 1/(1+d_n).

### Theorem 4.1 (line-mass criterion at p=-1)

Let mu be a nonzero finite even Borel measure on S^(n-1), n>=2. Suppose it is not concentrated in a proper linear subspace and

    mu({v,-v})/mu(S^(n-1)) < a_n     for every v in S^(n-1).

Then there is K in K_e^n with J_(-1)(K,.)=mu.

**Proof.** Normalize mu to be a probability measure. Let L maximize F_1 on D. Proposition 3.2 excludes every degenerate dimension k>=2. If L is one-dimensional, write L=[-v,v], and set m=mu({v,-v}). A finite maximum requires m>0. Use Q_t=conv([-v,v] union t B_(v-perp)). For a=u dot v and b=sqrt(1-a^2),

    rho_(Q_t)(u)=1/(|a|+b/t).

On the two endpoints this is 1. On their complement, rho_(Q_t)(u)/t=1/(t|a|+b) increases to 1/b as t decreases to 0. Monotone convergence therefore gives

    [I_1(Q_t)-m]/t -> A_v := integral_(u not in {v,-v}) 1/sqrt(1-(u dot v)^2) dmu(u),

allowing A_v=+infinity. In particular A_v>=1-m.

The entropy difference equals

    D_n(t) = E log max(1,t/T),       T=|U dot v|/sqrt(1-(U dot v)^2),

for uniform U. A change of variables from the first-coordinate density gives

    f_T(z)=d_n (1+z^2)^(-n/2),    z>=0.

Thus D_n'(t)=P(T<t)/t and D_n(t)/t -> d_n. This also follows directly from D_n(t)=integral_0^t log(t/z)f_T(z)dz.

Since I_1(Q_t)->m, we obtain

    lim_(t->0) [F_1(Q_t)-F_1(L)]/t = A_v/m-d_n,

in the extended sense when A_v=infinity. The hypothesis m<1/(1+d_n) makes (1-m)/m>d_n, so the right side is positive. This contradicts maximality. L must be full dimensional. Lemma 2.3 and a final dilation to restore the original mass give the result. QED.

The stronger directional condition A_v>d_n m suffices in the same proof. The uniform line bound is only a convenient consequence. No smoothness or absolute continuity of mu is used.

### Corollary 4.2 (uniform great-subsphere version)

If an even probability measure has mu(S intersect E)<=c for every proper subspace E, where c<a_n, it has an origin-symmetric J_(-1) solution.

Indeed c<1 prevents concentration in any proper subspace and also bounds every line atom.

For n=2, d_2=2/pi and a_2=pi/(pi+2)>1/2=beta_(2,1). Thus this theorem, if accepted after review, proves that the cited bound is not optimal in at least this parameter case. It does not settle the optimal function for all p<=-1 and n.

## 5. Four-atom classification and the sharp planar endpoint

Let e_1,e_2 be orthogonal unit vectors and

    mu = (m/2)(delta_e1+delta_-e1) + ((1-m)/2)(delta_e2+delta_-e2),   0<m<1.

### Lemma 5.1 (finite-support rigidity)

If J_p(K,.) is supported on finitely many directions u_i, then K is the convex hull of its radial boundary points rho_K(u_i)u_i.

**Proof.** The density rho_K^p relative to J is positive and bounded above and below, so J has the same support. Let P be the hull of the stated boundary points. If K is not P, separation gives an open set of normal directions v with h_K(v)>h_P(v). At almost every one of these directions the unique supporting point of K lies outside the finite set. The pushforward description of J would give positive measure outside the stated directions, a contradiction. QED.

In the four-axis setting this means K is a quadrilateral with vertices

    (a,0), (0,b), (-c,0), (0,-d),       a,b,c,d>0.

Every vertex occurs because each prescribed atom is positive.

### Lemma 5.2 (evenness forces central symmetry for these data when p<=-1)

For s>=1, any solution of J_(-s)(K,.)=mu in the four-axis setting is origin symmetric.

**Proof.** The exterior angle at (a,0) is atan(a/b)+atan(a/d), so its J_(-s) mass is

    f(a)=[atan(a/b)+atan(a/d)]/a^s.

At (-c,0) the mass is the same function f(c), with b,d fixed. For each q>0,

    d/da [atan(a/q)/a^s]
      = a^(-s-1)[(a/q)/(1+(a/q)^2)-s atan(a/q)] < 0,

because atan z>z/(1+z^2) for z>0 (differentiate their difference). Equal opposite masses force a=c. The identical argument for the other pair forces b=d. QED.

### Proposition 5.3 (exact ratio equation)

For K=conv{(+/-a,0),(0,+/-b)} and t=a/b,

    J_(-s)(K,{+/-e1}) / J_(-s)(K,{+/-e2})
       = R_s(t) := t^(-s) atan(t)/atan(1/t).

Each exterior angle at +/-ae1 is 2 atan(t), and each at +/-be2 is 2 atan(1/t). Multiplication by the radial powers gives the formula. The ratio equation determines the relative masses; a positive dilation matches their total mass.

### Proposition 5.4 (p=-1 classification)

The four-atom probability measure above has a solution if and only if

    2/(pi+2) < m < pi/(pi+2).

There is no nonsymmetric exception.

**Proof.** At s=1, R_1 is continuous and

    lim_(t->0) R_1(t)=2/pi,    lim_(t->infinity) R_1(t)=pi/2,
    R_1(1/t)=1/R_1(t).

For completeness these are strict bounds at all finite t. The inequality R_1(t)>2/pi is equivalent to

    atan t > pi t/(pi+2t).

Let G(t)=atan t-pi t/(pi+2t). It vanishes at t=0 and tends to 0 at infinity, while its derivative has the sign of

    t[4pi-(pi^2-4)t].

Hence G first strictly increases and then strictly decreases to 0, so G(t)>0 for every t>0. Reciprocity gives R_1(t)<pi/2. Continuity and the endpoint limits show that every value in (2/pi,pi/2) occurs, without requiring a monotonicity claim. Since m/(1-m)=R_1(t), the displayed interval follows. Lemmas 5.1-5.2 exclude any other solution shape. QED.

### Theorem 5.5 (sharp universal planar p=-1 threshold)

For even probability measures on S^1, the strict bound

    mu({v,-v}) < pi/(pi+2)  for every v

guarantees an origin-symmetric solution. The constant is optimal and equality cannot in general be allowed, even if nonsymmetric solutions are permitted.

**Proof.** This is Theorem 4.1 in dimension 2; the strict bound already rules out support on a line. At m=pi/(pi+2), the four-atom measure has maximum line mass exactly pi/(pi+2) and has no solution by Proposition 5.4. Therefore any larger strict threshold, or any closed threshold at least this value, fails. QED.

This is a separately scoped endpoint result. The 2026 Feng-Hu-Li-Lv publisher abstract already states existence counterexamples at p=-1. Its full text was not available in the checked route, so possible overlap with the particular obstruction above is unresolved and no priority claim is made.

## 6. What changes for p<-1

### Proposition 6.1 (two orthogonal antipodal pairs always solvable for p<-1)

For s>1 and every 0<m<1, the four-atom measure in Section 5 has an origin-symmetric solution.

**Proof.** R_s is positive and continuous. As t->0,

    R_s(t) ~ (2/pi)t^(1-s) -> infinity,

and as t->infinity,

    R_s(t) ~ (pi/2)t^(1-s) -> 0.

The intermediate value theorem supplies the target ratio m/(1-m), and dilation supplies total mass. QED.

In fact the same existence conclusion holds for any two distinct unoriented lines. If their smaller angle is alpha in (0,pi/2], and the two vertex radii have ratio t, the exterior angle beta(t) at the first positive vertex is the unique angle in (0,pi) with

    beta(t)=atan2(2t sin(alpha),1-t^2).

The other exterior angle is pi-beta(t). The pair-mass ratio is t^(-s) beta(t)/(pi-beta(t)). Its limits are (2 sin(alpha)/pi)t^(1-s) and (pi/(2 sin(alpha)))t^(1-s), respectively, so the same argument applies. No classification of all nonsymmetric solutions is needed for this existence result.

These solvable examples can have maximum line mass arbitrarily close to 1. They disprove treating the old sufficient bound, or the new p=-1 bound, as a necessary constraint on every negative-p curvature measure. They do **not** show that every even measure with small proper-subspace masses is solvable for s>1.

### Proposition 6.2 (the first-order thickening mechanism stops at s=1)

Take L=[-e1,e1], and let mu have mass m on its endpoints and mass 1-m on the perpendicular great subsphere. Assume 0<m<1. For Q_t=conv(L union t B_(e1-perp)),

    F_s(Q_t)-F_s(L)
      = (1/s)log(1+((1-m)/m)t^s)-D_n(t)
      = -d_n t + o(t),                 s>1.

**Proof.** The radial values on the two supported parts are exactly 1 and t. Section 4 gives D_n(t)=d_n t+o(t), whereas t^s=o(t). QED.

Thus the specific variation that proves Theorem 4.1 decreases the objective for every positive m when s>1. A failure to improve a collapsed maximizer along this variation is not a nonexistence proof.

## 7. A solution need not be a global maximizer

For planar equal axis-pair masses m=1/2, restrict the functional to

    K_x=conv{(+/- exp(x),0),(0,+/-1)}.

Scale invariance removes the radius normalization. Its radial moment is (1+exp(sx))/2. Write H(x)=H(K_x). The part of the circle where exp(x)|cos theta| dominates |sin theta| has normalized length (2/pi)atan(exp x). Therefore

    H'(x)=(2/pi)atan(exp x),
    F_s'(x)=exp(sx)/(1+exp(sx))-(2/pi)atan(exp x),
    F_s'(0)=0,
    F_s''(0)=s/4-1/pi.

Consequently, whenever s>4/pi, the equal-radius diamond is a strict local **minimum along this one-parameter family**, even though a dilation of it solves the prescribed-measure equation by the explicit exterior-angle calculation. In particular this holds at p=-2. This refutes the converse “solution implies global maximizer” and blocks an argument that would deduce nonexistence merely from a boundary global maximum.

For 1<s<4/pi, R_s'(1)=4/pi-s>0 while its two endpoint limits are infinity and 0. Since R_s(1)=1, the level 1 occurs at least once below 1, at 1, and at least once above 1. Thus the equal four-atom data have at least three distinct aspect-ratio solutions in this range. They are different as subsets with fixed coordinate axes; the outer pair are related by a ninety-degree rotation. This is an explicit check of why no uniqueness assumption may silently enter the threshold argument. The 2026 paper already reports nonuniqueness for negative parameters; this calculation carries no claim of being the first example.

## 8. Remaining gap

The original problem requests the optimal guarantee over the entire region n>=2, p<=-1. We have not determined it for any p<-1, nor proved that a_n is the optimal p=-1 constant for n>=3. The general join variation excludes collapse ranks k>s, but leaves precisely the small ranks where its entropy cost competes with or dominates the radial gain. A global-maximizer obstruction alone cannot settle these cases because actual solutions can be nonmaximizing critical points. No degree, minimax, or compactness argument controlling all such critical points has been completed. The endpoint planar theorem is therefore a partial resolution of the selected problem, not a relabeling of the full target as solved.
