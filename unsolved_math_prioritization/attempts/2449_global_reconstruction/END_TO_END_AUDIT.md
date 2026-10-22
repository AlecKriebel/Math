# Erdős Problem 1038: end-to-end proof audit

Public edition dated 2026-10-12. This retains the complete substantive mathematical report, with transparent editorial changes to private references and review-status wording. Independently authored executable checkers, raw interval certificates, full numerical records, detailed diagnostic outputs, and source copies are not included. Hashes identify omitted evidence but do not provide executable public reproducibility. The work is AI-assisted and unrefereed, with no external human peer review or formal proof-assistant certification.

## Disposition and exact scope

This audit checks the original finite-polynomial problem, not a stronger problem about all probability measures. The analytic argument of Shouqiao Wang's proposed manuscript, combined with the two independently reconstructed certificates and their independently audited exact arithmetic, establishes the following theorem, subject to the standard external mathematical inputs listed below.

Let P be the nonconstant monic real polynomials all of whose roots, with multiplicity, belong to [-1,1]. Define E_f={x:|f(x)|<1}. Put

    H(q)=2q/(1+q)^2, s(q)=(1-q)/(1+q), A(q)=log H(q)/log q.

Let q_s be the unique solution of A(q)=s(q) in (0,3-2sqrt(2)). For 0<q<q_s let u_+(q) be the unique nontrivial root in (1,1/q), and u_-(q) the unique root in (1/q,infinity), of

    A(q) log((u-q)/|1-qu|)-log u=0.

Continue u_+(q_s)=1 and set

    Lambda(q)=H(q)[u_-+u_-^(-1)-u_+-u_+^(-1)].

There is one and only one minimizer q_* of this function on (0,q_s]. With L=Lambda(q_*),

    inf_{f in P}|E_f|=L,
    |E_f|>L for every individual f in P,
    1.834430475762661 < L < 1.834430475762662,
    0.025715536866527 < q_* < 0.025715536866528.

Thus the infimum over finite polynomials is not attained. Using Tao's explicitly cited upper-extremum theorem as an external input, the supremum is 2sqrt(2), with equality precisely for f=(x^2-1)^m, m a positive integer.

The uniqueness statement concerns the parameter of the specified one-cut family only. Neither certificate, nor this audit, proves uniqueness of minimizing arbitrary probability measures, classifies all relaxed minimizers, or proves a universal lower bound for arbitrary non-empirical root measures. No relaxed compactness or minimizer-existence theorem is needed for the finite-polynomial conclusion. No novelty is claimed: the construction is credited to Wang and Tao, and this is an independent verification and audit.

Final acceptance is tied to the exact artifact hashes and final receipts recorded in the companion `ACCEPTANCE.md` and aggregate `VERIFICATION_SUMMARY.json`; a scalar PASS without the analytic argument below is not whole-problem acceptance.

## Sources, inspection, and citation boundary

The full 29-page text of Wang's *A Proposed Complete Solution to Erdős Problem 1038* was read, including Sections 2–10 and Appendix A. The endpoint-adjoint calculation on printed page 14 was additionally inspected as a rendered page. The retained PDF is 488289 bytes, SHA-256 `3a7e857b12e59f24af17f36a30030b0ad6368c2d59955ef58e643400917565ad`, available at [the proposed manuscript](https://multiscalar.ai/results/erdos-1038/paper.pdf). Its public page described it as Proposed at the previously inspected snapshot. This audit does not claim a change in the author's public status or external community acceptance.

The original EHP problem, the retained prior audit, and the exact scope of [draft PR 1310](https://github.com/AlecKriebel/Math/pull/1310) were checked. The previously accepted result was only a fixed-candidate upper bound, not this matching lower bound. The retained EHP source is *Metric properties of polynomials*, [1958 PDF](https://users.renyi.hu/~p_erdos/1958-05.pdf), 4304732 bytes, SHA-256 `5d20ad770563e425ac3343e31581859a24facabf744f10489b8f8d201b0ec12a`.

Tao's *Superlevel sets of logarithmic potentials*, dated December 27, 2025, is [available here](https://terrytao.wordpress.com/wp-content/uploads/2025/12/erdos-1038-2.pdf), 359077 bytes, SHA-256 `7ef1d231d1689873bafba3bbe5e70710bc605eee245d71614f3abd0917824d41`. Its Theorem 2.1 is an external input for the upper extremum. Its statement and empirical specialization, rather than its complete proof or optional computational scalar checks, are accepted here.

The lower proof uses the standard Pringsheim theorem for a power series with nonnegative coefficients: a finite convergence radius has a singularity at the positive real radius. It is used with all its hypotheses verified below. Basic analytic implicit-function, Lagrange inversion, dominated-convergence, and measure-integration theorems are also external standard inputs.

The circle rearrangement input deserves a strengthened citation. Wang cites Baernstein's 1989 paper, which has a 1995 correction, [DOI](https://doi.org/10.1080/17476939508814799), absent from Wang's bibliography. Rather than assume that correction's content, this audit checked an accessible primary replacement: Michael Christ and Marina Iliopoulou, *Inequalities of Riesz-Sobolev type for compact connected Abelian groups*, Theorem 1.1, equation (1.3), and Theorem 1.5. The [author/publisher-hosted PDF](https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-christ-iliop.pdf), edited March 12, 2021, was retrieved in this audit: 548600 bytes, SHA-256 `40bd076e6f40ce4b907520f095ffc853ba117e0ddb2999c50e4199bcaf1aeab3`. It gives exactly the nonnegative circle-convolution inequality required here and cites both Baernstein papers. No equality or stability theorem from that paper is needed. Its proof is a cited mathematical input, not independently reconstructed in this audit.

The author numerical verifier and linked Lean project were not executed. Only independently authored arithmetic/replay/interface code was used. Local retained source PDFs were read for research and are not included as authored deliverables. No source copy was published, and no repository change or queue mutation was performed.

## 1. Original target and finite atomization

For a degree-n polynomial f with roots r_j, its empirical root probability is mu=n^(-1)sum delta_(r_j). Exactly, V_mu(x)=n^(-1)log|f(x)|, so E_f={V_mu<0}. Every such set lies in (-2,2). Its boundary is finite because it is contained in the zero set of the nonzero polynomial f^2-1. Thus the strict/non-strict convention changes no length for a finite polynomial. This statement is not extended to continuous measures with zero-potential platforms.

Every component (a,b) of E_mu contains a root. Otherwise V_mu is continuous with zero endpoint values and strictly concave on (a,b), which forces V_mu>=0 there. In each component collapse its finitely many roots to their mass-weighted barycenter. All roots belong to E_mu and are accounted for. For any x outside E_mu, log|x-t| is concave as a function of t on each component; Jensen says that each collapse raises V_mu(x). Consequently the new strict negative set is contained in the old one globally.

Within an old component the new potential has exactly one pole. On either side it is strictly concave, tends to -infinity at the pole, and is nonnegative at the old endpoint. Its negative part on that side is the interval adjacent to the pole: the superlevel set of a concave function is an interval. Old intervening nonnegative points stay nonnegative. Therefore the collapsed measure has exactly one distinct cluster in each of its components. This remains true when distinct open components share a zero boundary point. The weights stay rational, hence empirical, and all barycenters remain in [-1,1].

This direct finite argument avoids a relaxed minimizing measure altogether. Lower semicontinuity under weak convergence would not by itself transfer a lower bound for empirical measures to every probability measure; that incorrect direction is not used.

## 2. Orientation, normalization, and all exceptional cases

Reflect if necessary to make the mean m nonpositive. For -1<x<0 and -1<=t<=1,

    |x-t| <= 1-xt,
    V_mu(x) <= integral log(1-xt)dmu <= log(1-xm) <=0.

Equality throughout is impossible: strict concavity in Jensen would force a single point mass, and the last equality would make it delta_0, where the first inequality is strict. Thus (-1,0) is in one component, containing its unique cluster c. Every possible cluster left of c would also lie in that same component, so c is leftmost and c<=m<=0.

Translate roots and variable by -c-1. The support moves from [c,1] into [-1,-c], a subset of [-1,1], and the mean remains nonpositive. Translation preserves lengths and the one-cluster structure. If r_0 was the old right boundary of the main component, then r_0>=0. If r_0-c<1, its distance to the main atom is <1 and its distances to all residual roots to its right are <=1. The weighted geometric mean could not equal exp V_mu(r_0)=1. Hence the translated boundary beta=r_0-c-1 is nonnegative.

Let A be the mass at -1 and B=1-A. If B=0, the length is exactly 2, exceeding L. Otherwise the remaining roots lie in [beta,1]. At beta, weighted AM-GM gives

    1 <= A(1+beta)+(1-A)(1-beta)=1+(2A-1)beta.

For beta>0 this gives A>=1/2. If beta=0, equality forces every residual root to be 1, and the nonpositive mean again gives A>=1/2. No division by beta is made in that case.

Shift by one and divide the potential by B. The sign and lengths are unchanged, and the target becomes

    W(x)=k log|x|+sum_i q_i log|x-d_i|,
    k=A/B>=1, 1<=d_1<...<d_N<=2,
    q_i>0 rational, sum_i q_i=1.

The component containing zero and each residual component are distinct, possibly with single-point contact. This separation fact is retained and is essential to the main-width argument.

## 3. Residual radii and elementary range

Write M_k for the main width and

    R_i=exp(-(k log d_i+sum_(j!=i) q_j log|d_i-d_j|)/q_i)>0.

The main component contains (0,1), since W(x)<=k log x+log(2-x)<0 there. Thus every residual component lies to the right of 1. On the residual component containing d_i, removing its self-pole leaves a strictly concave background. If the two distances to its endpoints are s,u>0, the background's endpoint values and concavity imply

    R_i <= s^(u/(s+u))u^(s/(s+u)) <= (s+u)/2.

The sign reverses on division by -q_i; keeping that reversal is essential. Hence

    |E_mu| >= J_k:=M_k+2sum_i R_i.

If rho^k(2+rho)=1, then (-rho,1) is in the main component. The scalar left side is strictly increasing in rho>0, so rho is unique, and for k>=1 it is at least sqrt(2)-1. Thus M_k>=sqrt(2).

For 1<=k<=K=29/20, a nonnegative separation point b in (0,d_1) exists even in the contact case. Jensen implies b>=1 and

    sum_i q_i(2-d_i) <= epsilon_K
      :=2-(K+1)K^(-K/(K+1)) <1/25.

The final numerical inequality has an exact elementary proof: exp(3/8)>29/20 and the cubic lower Taylor estimate for exp(-87/392) give the positive rational margin 522631/245862400. Put Q=sum q_i^2, t=1-Q, and S=sum R_i. Concavity of log, |d_i-d_j|<= (2-d_i)+(2-d_j), and weighted AM-GM give

    Q log(3S) >= log3-k log2-t log(6epsilon_K/t).

For t=0 the pair sum and t log(c/t) have their limiting value zero. Otherwise t log(c/t)<=c/e. Using epsilon_K<1/25 and e>8/3 bounds the last term strictly by 9/100. Positive atanh-series bounds log3>263/240 and log2<1123/1620 leave the exact margin 11/16200. Therefore S>1/3 and J_k>sqrt(2)+2/3>2>L. The preceding exact checks were already accepted in the fixed-candidate audit. No global numerical chart is needed here.

## 4. Main-width supporting inequality, including contact and differentiation

The reference residual probability on [a,2] is

    eta=(k+1)e_[a,2]-k omega_(0,[a,2]),
    d eta(d)=[k+1-k sqrt(2a)/d] dd/[pi sqrt((d-a)(2-d))].

Its mass is one. Positivity is equivalent to a>=2(k/(k+1))^2. Every actually certified reference has strict positivity. Its potential with the field k log|x| is a constant C on [a,2]. The arcsine/balayage formulas follow by the change d=c-r cos(theta) and its Poisson expansion; no unproved extremal property of equilibrium measures is being used.

For a residual quantile T, define

    Psi_T(y)=y exp((1/k)integral_0^1 log(1-y/T(u))du),
    R(T)=exp(-(1/k)integral_0^1 log T(u)du).

Then W_T(y)/k=log(|Psi_T(y)|/R(T)). For a finite target, Psi_T has exactly one positive critical point y_c<d_1: its logarithmic derivative is 1/y-(1/k)sum q_i/(d_i-y), strictly decreasing from +infinity to -infinity. The component separation proved earlier yields R(T)<=Psi_T(y_c). Strict inequality gives a separated main crossing; equality is exactly a shared zero-contact point. On the negative axis Psi_T is strictly increasing from -infinity to zero. Thus the main endpoints are the inverse branch Phi_T evaluated at -R(T), R(T), with increasing limiting interpretation at positive contact.

Lagrange inversion gives Phi_T(z)=sum_(n>=1) a_n z^n with nonnegative coefficients. Each a_n R(T)^n for a finite quantile is a nonnegative sum of monomials product d_i^(-gamma_i), gamma_i>0. Its Hessian quadratic form divided by the monomial is

    (sum_i gamma_i v_i/d_i)^2+sum_i gamma_i v_i^2/d_i^2 >=0.

Every odd width truncation is therefore convex. Rational target weights allow a common equal-mass partition refining all target blocks; approximate the continuous reference quantile on that partition. At any fixed truncation the coefficients are polynomials in finitely many inverse moments integral T^(-j), multiplied by powers of R(T). Values and directional derivatives converge by dominated convergence, since 1<=T<=2 and |v|<=1. This is a finite-dimensional convexity limit, rather than an unsupported appeal to infinite-dimensional convexity.

At a strictly separated reference, the simple positive crossing occurs before a positive critical value and strictly below a. Pringsheim's theorem excludes an earlier complex singularity of the nonnegative inverse series: such a finite radius would produce a positive-real singularity, contrary to the regular real inverse there. Choose a closed complex z disk of radius greater than R(T_0) but within this convergence disk, small enough that Phi_(T_0)(|z|)<a. Nonnegative coefficients give |Phi_(T_0)(z)|<=Phi_(T_0)(|z|)<a. On this compact disk the logarithmic integrals and their derivatives are analytic under any sufficiently small bounded material perturbation T_0+s v, and Psi' at the inverse is nonzero. The analytic implicit-function theorem therefore gives uniform analytic dependence of the inverse on s; R(T_0+s v) is analytic too. Cauchy estimates justify the locally uniform differentiated inverse series and absolute convergence at the reference endpoints. This supplies the material-derivative limit used when the truncation order goes to infinity.

For a separated target the same inverse argument identifies the odd series with its exact width. For a contact target replace R by lambda R, 0<lambda<1. All convexity arguments remain valid because the monomials receive only positive factors lambda^n. The nonnegative odd series increases to the full width as lambda tends to one, while reference values and derivatives converge absolutely. Hence in both target cases,

    M_k(T)>=M_k(T_0)+D M_k(T_0)[T-T_0].

No pathwise assumption that every interpolated quantile stays separated is needed to establish this global supporting inequality.

## 5. Endpoint-corrected adjoint and discontinuous target velocities

The certificate supplies simple reference crossings x_-<0<x_+<a and slope signs W'(x_-)<0<W'(x_+). Put sigma_-=-1/W'(x_-), sigma_+=1/W'(x_+), K_j=sqrt((a-x_j)(2-x_j)), and

    d xi(d)=[D-sum_j sigma_j K_j/(d-x_j)] de_[a,2](d),
    D=sum_j sigma_j K_j/(a-x_j).

The numerator vanishes at a and has strictly positive derivative on (a,2]. Thus xi is finite, atomless, and positive on every nonempty subinterval; its total mass R_0 is positive.

For the spatial material velocity v=T-T_0 define F(d)=A_density(d)v(d). Differentiating the constant-platform identity cancels all terms containing v(d), leaving

    g(d)=pv integral F(e)/(e-d) de_[a,2](e),
    D M_k=-sum_j sigma_j integral F(d)/(d-x_j) de_[a,2](d).

In d=c-r cos(theta), write F=f_0+2sum_(n>=1)f_n cos(n theta). The finite Hilbert-transform identity for each cosine and Poisson orthogonality give coefficients -Gamma for f_0, -2Gamma for even n, and +2Gamma for odd n in D M_k-integral g dxi, where Gamma=sum sigma_j/K_j. These are exactly the coefficients of -Gamma F(2). Thus

    D M_k-integral g dxi
       =-A_density(2)v(2)(sigma_-/K_-+sigma_+/K_+).

For an atomic target v(2)=d_N-2<=0, so the correction is nonnegative. It must not be silently omitted or declared an equality with the adjoint pairing.

The target velocity has finitely many interior jumps, not global smoothness. In the angular variable F is piecewise analytic. Subtract its jumps to obtain a continuous piece with cosine coefficients O(n^(-2)); its regularized finite Hilbert transform is bounded by a constant times 1+|log min(theta,pi-theta)|. A jump at theta_l has regularized transform proportional to

    [log|1-lambda exp(i(theta+theta_l))|
      -log|1-lambda exp(i(theta-theta_l))|]/sin(theta).

The only interior singularity is logarithmic and uniformly integrable as lambda tends to one. At the angular endpoints the numerator difference is O(sin theta), uniformly in lambda. The adjoint angular density is bounded and is O(theta^2) at zero. These bounds justify convergence of the pairings, while the exterior integrals converge by domination and the endpoint Fourier sum converges because F is continuous at pi. Thus the identity holds for the finite-block velocities actually used. Combining it with the supporting inequality yields

    M_k(T)>=M_0+integral g dxi.

## 6. From every target block to an explicit scalar inequality

Pull xi back to quantile space, let I_i be a target block of length q_i, and put r_i=xi_hat(I_i)>0. Its mixed logarithmic energy is

    E(I_i)=integral_(I_i) integral_(I_i)
             log|T_0(u)-T_0(v)| dv dxi_hat(u).

These integrals are absolutely convergent: in angular coordinates the logarithm is a sum of two log-sine kernels and both density factors are bounded. Fubini is valid even at shared block endpoints.

Off-block target and reference differences have the same sign by monotonicity of the quantiles. Applying log y-log x<=(y-x)/x to their absolute values is therefore valid. Within the same block the difference quotient is exactly -1. Applying the same tangent inequality to the positive external-field coordinates and using the platform identity gives

    g(u)>=-q_i log R_i-C-q_i
             +integral_(I_i) log|T_0(u)-T_0(v)|dv.

After integration and adding 2sum R_i, minimize each expression over R_i>0. Its unique minimum occurs at R_i=q_i r_i/2 and equals

    E(I_i)-q_i r_i log(q_i r_i/2)-C r_i.

Consequently if every nonempty block satisfies

    E(I)>=qr log(qr/2)+C_eff r,
    C_eff=C+(L-M_0)/R_0,

then J_k>=L. A strict positive normalized surplus in every block gives J_k>L, because q,r>0 and the sum has finitely many terms. No equality classification of the preceding tangent or rearrangement steps is needed for that strictness.

## 7. Circle reduction and normalization

Let eta=A(theta)dtheta/pi, xi=B(theta)dtheta/pi. Both factors are nonnegative increasing on [0,pi]. For any angular block J put

    Q=integral_J A(theta)/a_pi dtheta,
    R=integral_J B(theta)/b_pi dtheta,
    q=a_pi Q/pi, r_block=b_pi R/pi.

The even extensions 1_J(|theta|)A(|theta|)/a_pi and its B counterpart lie in [0,1] and have circle masses 2Q,2R. The identity

    |d(theta)-d(phi)|/H
       =|exp(i theta)-exp(i phi)| |exp(i theta)-exp(-i phi)|

gives the circle mixed energy with factor 1/(2QR), not 1/(QR) or 1/(4QR). For the nonnegative decreasing kernel ell(t)=log2-log|exp(it)-1|, circle rearrangement followed by the elementary fixed-mass bathtub comparison bounds its cross energy above by that of centered arcs. Equivalently the logarithmic chord kernel's energy is bounded below by the arcs' energy.

The needed external rearrangement statement can also be applied directly through Christ–Iliopoulou Theorem 1.5: layer-cake decompose ell into centered-arc indicator kernels, apply the [0,1]-function inequality at each layer, and integrate by Tonelli. This verifies all function and mass hypotheses without using any equality or stability result, and accounts for the correction to the older citation.

The normalized centered-arc energy is

    A_circ(Q,R)=-sum_(n>=1) sin(nQ)sin(nR)/(n^3 QR).

The Fourier calculation follows first for Abel regularization and then for the integrable kernel. Completing the square gives

    2 A_circ(Q,R)-A_circ(Q,Q)-A_circ(R,R)
       =sum_(n>=1)(sinc(nQ)-sinc(nR))^2/n >=0.

Define h(Q)=A_circ(Q,Q)-log(Q/pi). Its integral formula shows it decreases on (0,pi], because sin x/x decreases on (0,pi); h(pi)=0, so h>=0. Cancelling physical masses yields exactly

    E(I)/(qr_block)-log(qr_block/2)-C_eff/q
      >= log(2H/(a_pi b_pi))+h(Q)+h(R)
          +sum_(n>=1)(sinc(nQ)-sinc(nR))^2/n
          -pi C_eff/(a_pi Q).

All factors of 2 and pi have been checked independently. This is the expression bounded by the independent Certificate 7.1 replacement.

## 8. Certificate 6.1: exact claim mapping and chart endpoints

The reconstructed certificate proves existence, branch correctness, global one-cut minimization, and the stated enclosures. It is not by itself a lower bound for arbitrary finite targets.

The zero-platform relation C=0 gives k=-log H/log(H/q), A=k/(k+1)=log H/log q, and shifted conductor edge a_sh=2s^2. In the exterior coordinate x_sh=1+s^2-H(u+u^(-1)), the factorization x_sh=(H/q)(u-q)(1-qu)/u and the arcsine/Poisson formulas give W_0(x_sh)=-(k+1)F(q,u). Thus u in (1,1/q) corresponds precisely to 0<x_sh<a_sh, while u>1/q corresponds to x_sh<0. The desired branches are physical main crossings, not arbitrary roots of a transformed equation. Their endpoint difference is exactly the Lambda stated in the theorem.

In rho=-1/log q, z=qu, the same equation becomes G=A log((z-q^2)/|1-z|)-log z-d=0, with A=1-rho d. Its width is 2(z_--z_+)/(1+q)^2+2q^2(z_-^(-1)-z_+^(-1))/(1+q)^2. Ordinary implicit first and second differentiation of these displayed functions yields precisely the reconstructed bulk expressions, with q_rho=q/rho^2 and q_rhorho=q(1-2rho)/rho^4. The independently audited jets carry actual derivatives, including the product's factor-two cross term. The tail uses only the first derivative; unused second-order placeholders are not proof inputs.

Admissibility is controlled by f(q)=(1+q)d(q)+2q log q, d(q)=log2-2log(1+q). Its derivative is log(2q^2/(1+q)^2)<0 and its limit at zero is log2>0. Certified opposite endpoint signs isolate its unique zero q_s. The isolated interval is below 0.124, and 0.124^2-6(0.124)+1>0 proves it lies below 3-2sqrt(2). Thus all required densities are nonnegative. Below q_s they are strictly positive.

For u in (1,1/q), F_u has numerator q u^2-Bu+q, B=1+q^2-A(1-q^2)>2q. Its two roots are positive reciprocal numbers, with exactly one in (1,1/q). Thus F first decreases from F(1)=0 then increases to +infinity, giving exactly one nontrivial root. For u>1/q, F_u=-A(1-q^2)/((u-q)(qu-1))-1/u<0, with opposite infinite endpoint limits. At q_s the positive-side numerator is q(u-1)^2, and the nontrivial branch limits to u=1. Every certified box is identified by these analytic facts, not by numerical proximity or merely by overlap with a neighboring root box.

The exact independent chart cover is:

| Chart | Domain | Sign |
|---|---|---|
| singular tail | 0<=rho<=1/50 | Lambda_rho<0 |
| left bulk | 1/50<=rho<=27/100 | Lambda_rho<0 |
| convex tube | 27/100<=rho<=28/100 | Lambda_rhorho>0 |
| right bulk | 28/100<=rho<=87/200 | Lambda_rho>0 |
| regular soft | 1/10<=q<=0.12362 | Lambda_q>0 |
| soft endpoint | 0.12362<=q<=q_s | Lambda_q>0 |

Here rho=-1/log q and dq/drho=q/rho^2>0. Exact interval evaluation proves 1/10<exp(-200/87)<q_s, so the rho and q charts overlap. Exact rational subdivision and outward dyadic endpoints cover all joins. The tail includes rho=0 as a regular limiting transformed equation, with z_+=1/2,z_-=3/2; no finite positive cutoff is substituted for the omitted limit. The original parameter domain remains q>0.

Within the convex tube, certified strictly opposite derivative signs at two interior dyadic points imply a stationary point by continuity, and positive second derivative gives exactly one. The outer signs imply strict decrease before it and strict increase after it on the complete admissible domain, hence a unique global minimum in this family.

At the soft edge, use y=(log u_+)^2 and the deflated equation D(q,y)=A-1+2A b atanhc(w)=0. The checked domains 1-q cosh(sqrt(y))>0 and 0<=w<0.03 imply q exp(sqrt(y))<1, so the deflation uses the correct real branch. Positive D_y proves uniqueness and regularity. For the last slab, the numerically evaluated q interval extends slightly beyond the true q_s isolation endpoint and the lower sign is deliberately not tested there. Existence is asserted only at admissible q<=q_s, where the exact identity D(q,0)=A/s-1<=0 supplies the missing lower sign. Its upper sign and D_y>0 then include y=0 at q_s. This is valid restricted-domain reasoning, not proof of an inadmissible nonnegative-y root beyond q_s. The width uses cosh(sqrt(y)), analytic in y, so its one-sided derivative stays regular.

The normal, -O, and -OO exact replays check the shorter theorem decimals against the underlying dyadic endpoints. The enclosures include

    0.123630684649383 < q_s < 0.123630684649384.

## 9. Certificate 7.1 replacement: physical roots, all k, and scalar implications

The independent finite-reference code does not need root monotonicity in k: opposing endpoint signs and strict slopes are checked uniformly over each entire parameter slab. These prove a zero in each proposed interval at every parameter. For the actual nonnegative reference probability, W'<0 on (-infinity,0) and the endpoint limits are +infinity,-infinity. Its negative zero is unique. On (0,a),

    W''(x)=-k/x^2-integral (d-x)^(-2)d eta(d)<0.

A positive-slope zero is therefore the unique ascending zero and exactly the main right boundary. It has a positive point immediately after it and is strictly separated from the support. Thus the slope-certified roots meet the analytic supporting and adjoint hypotheses, not just a local algebraic equation.

For every finite-reference slab the code verifies strict density and adjoint positivity, C_eff(T)<0, and 0<R_max<Q_max<pi, with the exact rational target

    T=1.83443047576266171109075363512901884952989750747.

With B0=log(2H/(a_pi b_pi))+h(Q_max)+h(R_max), P=-pi C_eff(T)/a_pi>0, the constant-edge regime is bounded by B0+P/Q_max. In the affine regime, Q<=R_max is bounded by B0+P/R_max; for R_max<=Q<=Q_max use the n=1 square and monotonicity of sinc. The resulting function B0+P/Q+(sinc Q-sinc R_max)^2 has negative derivative on a closed 32-piece cover, so its minimum is at Q_max. This covers every block, including arbitrarily small positive Q or R; no lower mass cutoff is used. The first 80 Fourier terms of h have the explicit signed tail [-1/(2*80^2*X^2),0], and monotonicity allows outward upper mass caps in its lower bounds.

The independent sufficient ranges and normalized lower bounds are:

| Range/reference | Slabs | Strict lower bound |
|---|---:|---:|
| 36/25<=k<=21/10; a=1153/500-k/4 | 395 | 0.028229353338717 |
| 21/10<=k<=21/5; a=9/5 | 840 | 0.036361685512222 |
| zero platform, 0<rho<=1/50 | one tail | 0.961762019209 |
| zero platform, 1/50<=rho<=rho(26631/10^6) | 256 | 0.000564594536104 |
| zero platform, rho(26631/10^6)<=rho<=rho(41542/10^6) | 39 | 0.065630278169259 |

These replace, rather than reproduce, Wang's stronger claimed affine/simple-terminal margin figures and original slab counts. The smaller positive lower bounds are sufficient for every mathematical conclusion. They are not evidence that the stronger source figures are false.

For terminal references put t=rho d=1-A, P0=t+2qA/(1+q), and

    raw(z)=1-A(1-q^2)z/((1-z)(z-q^2)),
    w_+=-1/raw(z_+), w_-=1/raw(z_-).

The code checks q<z_+<1<z_- and raw(z_+)<0<raw(z_-). Independently, raw=-u F_u, W=-(k+1)F, and dx/du=-H(1-u^(-2)), so sigma=t K w. Consequently

    a_pi=P0/t, b_pi=4tH(w_++w_-),
    D:=2P0(w_++w_-)=a_pi b_pi/(2H),
    Q_max=pi t/P0,
    R_max=pi[(1+q/z_+)w_++(1+q/z_-)w_-]/[2(w_++w_-)].

Thus the simple-terminal test -log D>0 is exactly the desired scalar after dropping nonnegative terms. The refined test retains both h terms. The identities are valid for each positive finite rho; no cancellation at zero is used to assert a finite reference there. In the tail, q<2^(-72), q/rho is increasing, and kq<=50*2^(-72)/d_lower proves reference positivity without dividing an interval containing zero. The cancelled D has an upper bound below one. For actual rho>0, D>0, so -log D>=1-D gives the positive tail surplus. There is no missing infinite-k case: every finite polynomial with residual mass has finite k, while B=0 was already handled separately.

The parameter map k(q)=-log q/d(q)-1 has derivative -f(q)/(q(1+q)d(q)^2)<0 throughout the needed family and tends to infinity at q=0. At q_cap=41542/10^6, certified k(q_cap)<4.199981974346<21/5 gives strict overlap with the constant range. The split is shared with outward overlap in rho: the simple range reaches the split's upper isolation endpoint and the refined range begins at its lower endpoint. The refined range reaches the cap's upper isolation endpoint. The elementary/affine overlap is also strict, 36/25<29/20. Hence every finite k>=1 is covered.

All terminal rho values needed are below 87/200; Certificate 6.1 already certifies exp(-200/87)<q_s. Monotonicity of q(rho) therefore proves every terminal reference lies in the same admissible family to which its global minimum applies. Alternatively f(q_cap)>0 and monotonicity of f prove admissibility directly. For terminal C=0 and M_0=Lambda(q)>=L, so C_eff=(L-M_0)/R_0<=0. Dropping its contribution is legitimate only after Certificate 6.1; a fixed-candidate upper bound alone would not justify this step.

## 10. Exact target comparison, with both available bridges

The finite-reference test is decreasing in its target level: replacing L by T adds (T-L)/R_0 to C_eff and subtracts (T-L)/(q R_0) from the normalized surplus. Hence it is sufficient to prove L<=T exactly, not merely L<1.834430475762662.

The new Certificate 6.1 raw dyadic enclosure gives the stronger exact inclusion

    1.83443047576266171109075363512055343651186425665
      < L_interval_lower <= L <= L_interval_upper
      < T.

The independent interface check verifies these comparisons with exact rational arithmetic directly on integer endpoints, not on their printed shared decimal prefix. The strict positive gaps, rather than rounded displays, are the acceptance facts. The detailed gap records are omitted from this public edition. The full LSTAR interval containment is established, although only its upper endpoint is necessary.

As a second bridge, the previously accepted fixed-candidate proof gives Lambda(q_c)<the very same exact T. Once one-cut minimality is established, L<=Lambda(q_c)<T. Its outward displayed upper endpoint is exactly below T as checked in the interface record. Neither bridge uses the shortened 1.834430475762662 as a substitute comparator.

## 11. Strict lower bound and nonattainment are separate from recovery

After atomization, the single-atom case has length 2>L. The elementary k range has J_k>2>L. At every other finite k a certified reference gives a strictly positive normalized surplus for each nonempty target block. All q_i>0 and r_i>0, so each unnormalized surplus is strictly positive. A finite sum remains strictly positive. The supporting/block inequalities therefore give J_k>L, and the actual atomized length is at least J_k. Since the old sublevel set contains the atomized one,

    |E_f|>L for every individual finite f in P.

No uniform positive excess over all degrees or all k is asserted; none is needed. This proves nonattainment once recovery proves that the infimum is L. Nonattainment is not inferred merely from the candidate having a continuous density.

## 12. Sharp recovery by actual finite monic polynomials

At q_* let s=s(q_*), a=2s^2-1, A_*=A(q_*). Since q_*<q_s, A_*<s. For A>A_* sufficiently close to A_* define

    mu_A=A delta_(-1)+[1-2As/(t+1)]dt/[pi sqrt((t-a)(1-t))], a<t<1.

The density is nonnegative because A<s. The arcsine integrals give total continuous mass 1-A, so this is a probability supported in [-1,1]. Its potential on [a,1] is the positive constant

    C(A)=log((1-a)/4)-A log q_*>0.

Off that support, with S(z)=sqrt((z-a)(z-1)) chosen as S(z)~z at infinity,

    V_A'(z)=[1-2As/(z+1)]/S(z).

For x<-1 the derivative is negative and the potential decreases from +infinity to -infinity, giving one simple zero. For -1<x<a, the derivative changes sign once, from positive to negative, at x_0=2As-1<a. The potential rises from -infinity, then decreases to the positive C(A); hence it has exactly one zero on the increasing branch. For x>1 the derivative is positive and there is no additional zero. Thus E_(mu_A) is one interval and its zero set consists of exactly two points. The atom at -1 gives -infinity, not a further zero.

At A=A_* the main crossings are simple because q_*<q_s; their difference is Lambda(q_*)=L by the exact exterior coordinate x=s^2-H(u+u^(-1)). The implicit-function theorem gives |E_(mu_A)|->L as A decreases to A_*.

Now fix A>A_*. Every probability on [-1,1] has equal-weight empirical approximants, for example mid-quantile samples. If nu_n converges weakly to mu_A, the potentials converge in L^1 on each bounded interval: t maps continuously into log|.-t| in L^1, uniformly on compact [-1,1], and a finite continuous partition-of-unity approximation reduces the assertion to weak convergence of finitely many continuous functions. This supplies a direct proof, without depending on continuity of the logarithmic kernel at its singularity.

Since the zero set of V_(mu_A) has measure zero, convergence in measure of potentials implies L^1 convergence of negative-set indicators. Indeed their mismatch set is contained in {|V_(mu_A)|<=delta} union {|V_(nu_n)-V_(mu_A)|>=delta}; first let n tend to infinity, then delta to zero. All negative sets lie in (-2,2), so no escaping length is omitted.

For nu_n=n^(-1)sum_j delta_(t_(j,n)), the actual polynomial f_n(x)=product_j(x-t_(j,n)) is nonconstant and monic with roots in [-1,1], and its strict sublevel set is precisely {V_(nu_n)<0}. Thus |E_(f_n)| tends to |E_(mu_A)|. Choosing A_m down to A_* and one empirical approximant with length error below 1/m proves a diagonal sequence with |E_f|->L. Combined with Section 11 this establishes the exact infimum and finite nonattainment.

The positive-platform stage is indispensable: at mu_(A_*) the conductor [a,1] has potential identically zero and positive length. Direct weak empirical approximation there does not itself control negative-set lengths from above. The proof never replaces <0 by <=0 on that zero-platform measure.

## 13. Supremum and final boundaries

Tao's Theorem 2.1 applies to every probability on [-1,1] and bounds the measure of {U_mu>0}, U_mu=-V_mu, by 2sqrt(2); its equality measure is (delta_(-1)+delta_1)/2. For an empirical probability, equality forces an even degree 2m and m copies of each endpoint, hence f=(x^2-1)^m. Conversely |x^2-1|<1 gives (-sqrt(2),0) union (0,sqrt(2)), of length 2sqrt(2). The omitted point zero matters for exact set notation but not measure.

This upper theorem remains an attributed external input. The independent lower audit does not promote the optional source upper-scalar routines or any Lean project to verified status.

No noncomputational gap remains identified for the original finite-polynomial theorem once the frozen independently reconstructed certificates and audited kernels are accepted. The remaining explicit trust boundary is conventional mathematical reasoning and AI-assisted review, the cited standard analytic/rearrangement results, Tao's upper theorem, exact-integer Python execution, and the pinned independent programs and records. This work is unrefereed, with no external human peer review or formal proof-assistant certification. It does not assert official problem-site acceptance. The programs and full records are not included in this public edition.

## 14. Reproducibility and interface records

Certificate 6.1 is tied to the exact independent checker hash `604c89d60cb6640f3c965b6037249e379e56e013e1d37bf7ff17368061bfc992` and certificate hash `01a37c997aa6c705b7dc48995f7d731848eccabe802136097a07c31762818e9a`.

Certificate 7.1's sufficient replacement is tied to finite checker hash `48b28eb878de3d868d25ab4b23fdf34752fa0eb7b621df41e62b49f43c82e43d` and terminal checker hash `2020a31e3db7e7c2c4c0275660d68448d4f6a70f6916a380c2f668c2b6e9921c`. The final replacement manifest is `d755191feb3e6a21a856302ba5ad193610cda60413f957164c36eea1a73126b9`.

The standalone interface checker imports no mathematical checker and replays no author code. It pins the exact input JSON, checks all coverage joins, terminal family admissibility linkage, raw positive scalar minima, and exact target comparisons. Its normal/-O/-OO output is byte-identical, SHA-256 `e3959d26383114617587211202205ca2785bb9d1b6f7e569256cba1c83352b3b`. It supplements rather than substitutes for the complete arithmetic replays. Final receipt hashes and source byte metadata appear in the acceptance record.

This auditor also independently invoked and completed the full frozen Certificate 6.1 replay, recomputing all recorded root signs, interval-Newton contractions, derivative and endpoint checks. After separate code hash gates and static formula review, this auditor independently recomputed every Certificate 7.1 finite and terminal slab, including actual reference roots, all remainder evaluations, and all scalar tests. The entire recomputed JSON byte streams matched the frozen records: 1100247 bytes with hash `911f446ad8a1d9133baf6f2775dd05a6ab70a3f5ca4d1c680b54c2041177326f`, and 301772 bytes with hash `7f63d1b0af640f2f64be4329a124d2c31e1dcee75f3b972aca805e4bd6f66fd1`. This is not acceptance based only on builder-supplied outputs or a metadata scan. The Certificate 7.1 generator still uses untrusted floating proposals, but every accepted sign and enclosure is checked by the audited exact-integer calculations; it is not described as a float-free generator.

The separate final kernel review accepts the pinned arithmetic on its declared actual domains, with 2454 exact-rational tests including 29 rejection controls and byte-identical normal/-O/-OO receipts. Its report hash is `b4b60ea3e248c3bb2d9edba728fbc07ebf7fe69ba0187713377042a1278122ba`; its manifest hash is `3f5b1e303245992ce28a2fab9eecae49fb8a1869f6f55bd23ccfe2a663860bc1`. The kernel report alone excluded full runs and all analytic reductions; those exclusions are discharged only by this full independent replay and the separately checked arguments above.
