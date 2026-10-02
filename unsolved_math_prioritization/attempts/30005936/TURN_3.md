# Turn 3: a quantitative exit tail for the exact superlinear white-noise solution

Substantive author turn **3/5**. For the source's coefficient g(v)=v_+^(5/4), smooth nonnegative Dirichlet initial data, and each finite T, the exact local mild solution extends globally, stays nonnegative, and satisfies

 P{sup_{0<=t<=T,0<=x<=1}u(t,x)>=R} <= C_{q,T,u0} R^(−q)
                                      for every 0<q<1/2,           (27)

for all sufficiently large R. An explicit choice below proves q=1/4. This tail is weak: it does not give a second moment or justify mean-square convergence of an uncut numerical scheme.

Global nonexplosion in this subcritical exponent range is classical. Mueller's 1999 primary paper, arXiv:math/9902126, explicitly credits the result for powers below3/2 to his 1991 paper. No new global-existence priority is claimed. We give the cutoff/mass/Hölder argument here to supply the quantitative estimate needed for numerical localization.

## 1. Globally defined cutoffs and consistent local solutions

For R>=1 let g_R(v)=min(v_+,R)^(5/4), and let u^R be its globally defined mild solution driven by the same white noise. It is nonnegative by turn 1. Define

 tau_R=inf{t>=0: sup_x u^R(t,x)>=R},

with the usual infinite value if the level is never reached. The cutoff solution has an adapted continuous C([0,1])-valued version; its supremum norm is adapted and continuous, so this hitting time is a stopping time for the usual completed right-continuous filtration. Assume R>||u0||_infinity. Local Lipschitz uniqueness implies that cutoffs at different levels agree until the smaller level is first reached. They therefore define a consistent local solution of the uncut equation up to tau_infinity=lim_R tau_R. We shall bound tau_R uniformly and obtain tau_infinity=infinity.

The useful feature of the capped coefficient is its **amplitude bound** |g_R|<=R^(5/4), not its Lipschitz constant. It gives polynomial Hölder estimates even though the Lipschitz-based estimates of turn 2 grow exponentially in R.

## 2. Unweighted mass is a nonnegative supermartingale

Put M_R(t)=∫_0^1u^R(t,x)dx. Since the coefficient is bounded, the mild stochastic integrals are integrable and, for deterministic s<=t,

 E[u^R(t,·)|F_s]=S_{t−s}u^R(s,·),                               (28)

where S is the killed Dirichlet heat semigroup. Conditional Fubini is justified by the bounded coefficient and finite moments on each fixed time interval. For a nonnegative field v, self-adjointness gives integral S_r v = integral v S_r 1 <= integral v, because 0<=S_r 1<=1 for the killed Dirichlet semigroup. Integrating (28) therefore gives

                E[M_R(t)|F_s]<=M_R(s).                            (29)

Thus M_R is a continuous nonnegative supermartingale with M_R(0)=m0:=∫u0. Optional stopping at the first level-z crossing, capped at T, yields

                   P{sup_{t<=T}M_R(t)>=z}<=m0/z.                 (30)

There is no boundary normal-derivative calculation here. The killed-semigroup identity supplies the sign of mass loss and avoids assuming spatial differentiability of a white-noise-driven solution. There is also no claim that the uncut field has an integrable square.

## 3. Polynomial Hölder bounds from bounded noise

Let Z_R(t)=u^R(t)−S_tu0 be the stochastic convolution. The continuous heat-kernel increment estimates and BDG give, for each fixed p>=2,

 E|Z_R(t,x)−Z_R(s,y)|^p
 <=C_{p,T} R^(5p/4)[|t−s|^(p/4)+|x−y|^(p/2)].                    (31)

The coefficient can depend on the solution; only its deterministic bound R^(5/4) enters BDG. Independence of the integrand is not assumed. The kernel estimates follow from the same sine-series sums used in turn 2: the integrated spatial difference is O(|x−y|), and the old/new time difference is O(sqrt(|t−s|)).

Here is a direct quantitative chaining argument. Use nested grids with spatial spacing2^(−j) and temporal spacing T2^(−2j). At level j there are O_T(2^(3j)) horizontal or vertical adjacent edges. Let A_j be the maximum stochastic-convolution increment over these edges. By (31) and the finite-maximum moment inequality,

                  ||A_j||_p <=C R^(5/4)2^(−j(1/2−3/p)).           (32)

For any 0<a<1/2−3/p, Minkowski gives

 ||Σ_{j>=0}2^(aj)A_j||_p
       <=C R^(5/4)Σ_{j>=0}2^(−j(1/2−a−3/p)) <infinity.           (33)

To see the pathwise consequence, approximate two points by their nested grid ancestors at the level comparable to their parabolic distance |x−y|+sqrt(|t−s|). Their coarse ancestors are joined by a bounded number of grid edges. Finer ancestors differ by a bounded number of edges at each successive level. Telescoping and the geometric series bound the increment by a constant times the sum in (33), multiplied by that distance to power a. Continuity extends the estimate from the dense union of grids. This gives spatial a-Hölder control uniformly in time, as well as temporal a/2-Hölder control.

The deterministic heat evolution of the fixed smooth zero-boundary u0 has a bounded corresponding seminorm. Consequently, if

 H_R=sup_{t<=T} sup_{x≠y}|u^R(t,x)−u^R(t,y)|/|x−y|^a,

then, for R>=1,

                         E H_R^p <=C R^(5p/4).                    (34)

The constant C in (34) depends on p,a,T,u0 but not on R or Lip(g_R). Its only R factor is the displayed amplitude power. The finite-dimensional parabolic grid has effective counting exponent3; ignoring the temporal grid would give an unjustified Hölder threshold.

## 4. A high point forces a mass excursion

The seminorm H_R is measurable as a supremum over a countable dense set. We estimated it on the entire deterministic interval [0,T] before evaluating the field at a random time; no deterministic-time BDG estimate is silently substituted at tau_R. On the event tau_R<=T, continuity gives a point x0 with u^R(tau_R,x0)=R. If H_R<=R^(5/4+epsilon), set

 delta=(R/(2H_R))^(1/a).

The case H_R=0 is impossible when R>0 because of the zero boundary values. Those boundary values also imply that both x0 and 1−x0 are at least (R/H_R)^(1/a), so the full interval [x0−delta,x0+delta] lies inside [0,1]. On this interval the solution is at least R/2. Hence

 M_R(tau_R)>=R delta
             >=2^(−1/a) R^[1−(1/4+epsilon)/a].                    (35)

Combining (30), (34), and Markov's inequality, without any independence assumption, yields

 P(tau_R<=T)
 <= C R^(−epsilon p)
       +2^(1/a)m0 R^[−1+(1/4+epsilon)/a].                         (36)

For the concrete choice

                  p=64,  a=3/8,  epsilon=1/32,

we have a<1/2−3/p, epsilon p=2, and 1−(1/4+epsilon)/a=1/4. Thus

                         P(tau_R<=T)<=C R^(−1/4).                 (37)

For any prescribed q<1/2, choose a with (1/4)/(1−q)<a<1/2, then choose epsilon>0 so small that (1/4+epsilon)/a<1−q. Finally choose p large enough that a<1/2−3/p and epsilon p>=q. Equation (36) gives P(tau_R<=T)<=C_qR^(−q).

## 5. Remove the cutoff for the exact equation

The stopping times are increasing by consistency. Their probability bound tends to zero as R→infinity, so P(tau_infinity<=T)=0 for every finite T. Taking integer T proves global nonexplosion. Patching the consistent continuous cutoff solutions gives the global nonnegative solution; local pathwise uniqueness gives global uniqueness in the usual local mild class.

For R larger than the initial supremum, the event that the uncut solution reaches R by time T agrees with tau_R<=T, since the two coefficients coincide below R. This proves (27).

The result concerns the exact white-noise equation, not the one-common-Brownian model in PR317. It supplies a quantitative localization input. The low exponent in (27) does not make unbounded numerical moments harmless, and it does not imply a mean-square error bound. The numerical cutoff still needs to be compared with the uncut recursion before any weak-convergence conclusion can be drawn. Original unresolved3/5.
