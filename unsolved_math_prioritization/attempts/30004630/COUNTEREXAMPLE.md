# Failure of unmodified quadratic growth when beta_2=0

30004630 / OWR-4990378-001. **First-turn full negative candidate, independent review pending.** The result concerns the source's unmodified strict positivity on the critical cone. It does not exclude useful strengthened conditions or weaker growth/stability theorems without quadratic regularization. The critical cone in this example is exactly {0}; this is an explicit, essential feature, not an omitted nondegeneracy assumption.

## 1. Source model and precise conclusion

The PDE is y_tt-Delta y+y^5=u on a smooth bounded domain Omega in R^3, with homogeneous Dirichlet boundary condition and prescribed energy initial data. Put H=L^2(Omega). The source's admissible set is ||u(t)||_H<=omega(t) almost everywhere. Its objective is

J(u)= (1/2)||y_u(T)-y_d||_H^2 + (nu/2)||(y_u)_t(T)||_(H^-1)^2
      +(gamma/4)||y_u||_(L^4(0,T;L^12))^4
      +beta_1||u||_(L^1(0,T;H))+(beta_2/2)||u||_(L^2(0,T;H))^2.             (1)

The OWR report includes the nonnegative nu term; the full referenced paper's displayed objective omits it. The construction below works for every fixed nu>=0, so covers either version. We take gamma=beta_1=1, beta_2=0. The report states a quadratic growth estimate in an L^2 neighborhood, whereas the inspected full-paper Theorem4.17 uses an L^infinity neighborhood with the same L^2-squared growth. Our sequence converges in L^infinity, so the distinction does not rescue either conclusion.

**Theorem.** There are smooth-domain, zero-initial-data examples of (1), with a positive constant admissible radius omega=rho, for which:

1. u_bar=0 is the unique global minimizer over the entire admissible set.
2. All first-order conditions hold and the source critical cone is {0}. Thus its strict second-order condition ell_r''(u_bar;v^2)>0 for every nonzero critical v is satisfied.
3. For feasible u_h ->0 in L^infinity, [J(u_h)-J(0)]/||u_h||_(L^2)^2 ->0. There is no positive quadratic growth constant even in the full paper's smaller neighborhood.
4. Under terminal-target perturbations of H norm epsilon, every global optimizer u_epsilon satisfies ||u_epsilon||_(L^2)/epsilon ->infinity. In particular no local Lipschitz L^2-control estimate with respect to this target datum can hold at this optimizer. This specific failure is stated explicitly; no claim that every possible weaker stability estimate fails is made.

## 2. Exact data and a uniform small-input estimate

Let Omega be the open unit ball in R^3, T=1, y(0)=y_t(0)=0. Let e be the first normalized radial Dirichlet eigenfunction:

e(x)=sin(pi|x|)/(sqrt(2pi)|x|), with its smooth value at x=0.

Then ||e||_H=1 and -Delta e=pi^2 e. Take y_d=pi e. Fix a positive constant rho, chosen sufficiently small below, and U_ad={u: ||u(t)||_H<=rho a.e.}.

Write A=||u||_(L^1(0,1;H)). The standard linear-wave energy and Strichartz estimates on the smooth bounded ball, as used in Kunisch–Meinlschmidt Lemma2.9, yield constants a_0,C>0 such that for A<=a_0 the unique solution obeys

||y_u||_Y <= C A,
||y_u-z_u||_Y <= C A^5,                                                     (2)

where z_u solves the zero-data linear wave equation with forcing u, and Y is the norm combining C([0,1];H_0^1 x H) energy with L^4(0,1;L^12) for the position. Increasing C if needed, (2) also bounds the terminal H norm and terminal velocity H^-1 norm.

Here is a direct justification of the power five, not a formal Taylor remainder. The linear forcing map is bounded L^1(H)->Y. Interpolation gives ||y||_(L^5L^10)^5 <= C||y||_(L^4L^12)^4 ||y||_(L^infinity H_0^1). Thus y->L(u-y^5) is a contraction on a ball of radius C A in Y when A is small, using the corresponding quintic difference estimate. Its solution has ||y||_Y<=C A, and y-z=-L(y^5) gives the second estimate. It agrees with the source's unique mild solution. In particular the constants in (2) are uniform over the whole set U_ad once rho<=a_0, since A<=rho. No numerical value of these classical finite constants is assumed.

The eigenmode gives the exact linear endpoint pairing

<e,z_u(1)> = (1/pi) integral_0^1 sin(pi t)<e,u(t)> dt.                        (3)

## 3. A global optimizer with a zero critical cone

Let f(t)=||u(t)||_H, so 0<=f<=rho and integral f=A. Expanding the terminal square and discarding the nonnegative squared-state, velocity and state-regularization terms gives, by (2)–(3),

J(u)-J(0) >= integral_0^1 [1-sin(pi t)]f(t)dt - C_0 A^5.                    (4)

The constant C_0 is uniform. Set s=t-1/2. For |s|<=1/2,

1-sin(pi t)=1-cos(pi s)>=2s^2.

A simple bathtub inequality then gives

integral_0^1 [1-sin(pi t)] f(t)dt >= A^3/(6rho^2).                           (5)

For a proof put r=A/(2rho)<=1/2. The integral of (s^2-r^2)(f(s+1/2)-rho 1_(|s|<r)) is nonnegative pointwise: both factors are nonpositive inside the central interval, and both are nonnegative outside it. Since the two densities have equal mass, this says integral s^2 f >=rho integral_(-r)^r s^2ds=A^3/(12rho^2). Multiplication by two proves (5).

Choose rho>0 with rho<=a_0 and C_0 rho^4<=1/12. Combining (4)–(5) yields, for every admissible u,

J(u)-J(0) >= A^3/(12rho^2).                                                 (6)

Thus zero is the unique global optimizer, not merely a stationary point or a formal candidate. The choice of rho is an existence choice below a positive constant; a numerical PDE constant is unnecessary. It can be chosen rational if desired.

At zero the adjoint in the first derivative is p(t)=-sin(pi t)e. Indeed the velocity and quartic state terms have zero derivative there. The L^1(H) subgradient lambda(t)=sin(pi t)e has norm <=1, so p+lambda=0; the admissible-set multiplier is zero because zero is strictly inside every pointwise ball. The tangent cone is the whole L^r(0,1;H), with r=1 in the paper's beta_2=0 convention, or the whole L^2 if that topology is used. Therefore

J'(0;v) = integral_0^1 [||v(t)||_H-sin(pi t)<e,v(t)>]dt
         >= integral_0^1 [1-sin(pi t)]||v(t)||_H dt >0                       (7)

for every nonzero v: the coefficient is positive except at the single time1/2, a null set. Consequently C(0)={v in T(0):J'(0;v)=0}={0}. The source's substitute second derivative, including its convention j''(0;v^2)=0, is well defined here. Its strict positivity on C(0)\{0} holds vacuously. No uniformly positive second variation on approximate critical directions is being assumed.

## 4. Feasible pulses violate quadratic growth in both topologies

For 0<h<min(rho,1/2), put

u_h(t)=h e 1_(|t-1/2|<h).

Its norms satisfy

||u_h||_L^infinity=h,  A_h=2h^2,  ||u_h||_L^2^2=2h^3.

From the exact linear solution,

z_(u_h)(1)=[2h sin(pi h)/pi^2]e,   (z_(u_h))_t(1)=0.                       (8)

Its uncancelled first-order cost is

h integral_(-h)^h [1-cos(pi s)] ds <= (pi^2/3)h^4.                          (9)

The terminal quadratic cost is O(h^4), the quartic state penalty is O(A_h^4)=O(h^8), and the nonlinear endpoint error in the linear part is O(A_h^5)=O(h^10). The velocity term has zero linear contribution by (8) and nonlinear cost O(A_h^10), for every fixed nu. Thus

0 <= J(u_h)-J(0) <= C_1 h^4,
0 <= [J(u_h)-J(0)]/||u_h||_L^2^2 <= (C_1/2)h ->0.                          (10)

This contradicts any positive quadratic-growth constant in either the L^2 neighborhood in OWR or the L^infinity neighborhood of the full theorem. It also makes clear why positivity in every fixed nonzero critical direction, of which there are none here, cannot control these concentrating near-critical directions.

## 5. A concrete loss of Lipschitz target stability

Perturb only the target to y_d^epsilon=(pi+epsilon)e, epsilon>0. Its distance from y_d is exactly epsilon. Let J_epsilon denote the otherwise identical objective. Global minimizers exist for these data: the source's existence theorem applies when nu=0 because gamma>0 and omega is integrable. For completeness the same argument includes any fixed nu>=0 in this small-control setting. U_ad is bounded, closed and convex in L^2, hence weakly compact. The uniform Y estimate gives strongly convergent subsequences of y_n in C(L^2), and of (y_n)_t in C(H^-1): the energy bounds and compact spatial embeddings give compactness, with equicontinuity from bounded y_t in L^infinity L^2 and y_tt=Delta y-y^5+u in L^infinity H^-1. The quintic has a weakly convergent subsequence in L^(6/5) identified with y^5 by almost-everywhere convergence. The limit retains L^4L^12 and energy bounds, so y^5 belongs to L^1L^2 and the weak solution is the unique mild solution. The endpoint costs are continuous and both norm penalties are weakly lower semicontinuous. This proves the direct-method claim also with the extra velocity cost.

Fix a=rho/2 and set h_epsilon=pi epsilon/(2a), for epsilon small enough that h_epsilon<1/2. The feasible comparison control

v_epsilon(t)=a e 1_(|t-1/2|<h_epsilon)

has A=pi epsilon. Its linear terminal position equals epsilon e+O(epsilon^3), and its linear terminal velocity is zero. As in (9) its first-order baseline cost is O(epsilon^3); its state penalty is O(epsilon^4), and nonlinear error O(epsilon^5). It follows that

J_epsilon(v_epsilon)-J_epsilon(0)=-epsilon^2/2+O(epsilon^3)
                               <= -epsilon^2/4                            (11)

for small epsilon, with a fixed throughout.

On the other hand, for any feasible u with r=||u||_L^2 and A<=r, the same expansion as (4) gives

J_epsilon(u)-J_epsilon(0) >= -||g_epsilon||_L^2 r-C_2 r^5,
 g_epsilon(t)=[(1+epsilon/pi)sin(pi t)-1]_+.

Since g_epsilon(t)<=(epsilon/pi-2(t-1/2)^2)_+, its support has length at most sqrt(2epsilon/pi) and its height is at most epsilon/pi. Therefore

||g_epsilon||_L^2 <= 2^(1/4)pi^(-5/4) epsilon^(5/4).                       (12)

If r<=K epsilon for any fixed K, this lower bound is -O_K(epsilon^(9/4))-O_K(epsilon^5)=o(epsilon^2), contradicting (11) for a global optimizer. Hence every choice of global optimizers satisfies r/epsilon->infinity. This is an actual finite-dimensional target-data perturbation, not an arbitrary added functional. It rules out the stated natural Lipschitz control estimate; weaker stability has not been ruled out.

## 6. What is and is not answered

The original sufficient-condition package cannot be extended by merely dropping beta_2>0 while retaining the same critical-cone positivity and strong quadratic-growth conclusion. The counterexample keeps beta_1>0, gamma>0, a smooth bounded three-dimensional domain, positive constant control radius, actual global optimality, and the exact energy-critical defocusing nonlinearity. It fails even in the stronger L^infinity localization.

This does not settle a different program of finding added structural hypotheses, enlarged approximate critical cones, nonvacuous uniform second-order conditions, or weaker norms/exponents that recover some beta_2=0 theory. All PDE well-posedness and wave estimates are classical source inputs. No novelty claim or attribution of acceptance to the source authors is made. The separate review must assess both the literal source implication and every analytic estimate.
