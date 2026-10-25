# Independent derivation and analytic controls

This note reconstructs the mechanism from the submitted update rule, rather than treating a certificate's encoded response formula as proof. Throughout, `r` is in a fixed compact subset `[r_-,r_+]` of `(1,infinity)`, `C=t^4`, `q=t`, `m/q -> lambda>0`, and `sigma>0` is fixed. All little-oh estimates below have that compact-uniform meaning. The mathematical target is eventual strict amplification for each fixed fitness; neither a finite useful population bound nor uniformity up to neutrality is asserted.

## 1. Finite controls from the event process

Multiplying a Bd row of changing probabilities by total population fitness gives continuous-time rates `f_u w_uv/d_u`. Multiplying a dB row by population order gives rates `f_u w_uv / sum_x f_x w_xv` for each death target. Positive statewise changes of clock preserve fixation committors. Summing these event rates on the clique with hub pendants gives the six rates printed on manuscript p.7. My separate generic event enumerator checks every labelled state for `(C,m)=(2,1),(3,2),(4,2)` at `r=3/2,1,2/3`, under both rules: 624 exact rational row comparisons, without importing the submitted transition builder.

On `K_n`, let `A_k=n-1+(r-1)k`. The down/up odds are `1/r` for Bd and `A_k/(r A_{k-1})` for dB. Hence the products in the standard nearest-neighbor committor formula are respectively `r^{-j}` and `r^{-j} A_j/A_0`. Summing the telescoping geometric expressions gives

`rho_Bd=(1-r^{-1})/(1-r^{-n})`,

`rho_dB=((n-1)/n)(1-r^{-1})/(1-r^{-(n-1)})`.

The neutral limits are `1/n`. In particular a two-vertex pair fixes from one mutant with probability `r/(r+1)` for Bd and exactly `1/2` for dB, including reciprocal fitness. My independent count-chain computation verifies these identities exactly for `2<=n<=9` and all three fitness controls, 48 comparisons. These finite tests check the stated formulas; the geometric summation establishes them for general order.

## 2. Finite weak-cut limit

At zero cut, every connected module absorbs internally. The finite fast block `Q_0` is transient; even when multiple modules are mixed, the continuous-time representation gives the sum of their isolated module generators, so no unproved independence assumption is needed. From a monomorphic-module state a first weak-cut event introduces one opposite-type vertex into exactly one module. The first-order monomorphic trace generator therefore is

`L=A+B(I-Q_0)^{-1}C_0`.

This follows by eliminating fast coordinates in the finite harmonic system and dividing the monomorphic equation by the cut. Its entries sum the introduction rate times the exact isolated-module absorption law. Global extinction and fixation remain boundary states. Positive invasion rates make the other finitely many macro states transient: there is a positive path to a global absorbing state from each. On each compact fitness interval, the fast inverse and the interior inverse of the scaled limiting Schur complement are continuous and bounded. This proves compact-uniform convergence for each fixed finite `C,m,q`; no bound uniform in growing population is required because the cut is diagonalized only after each finite size is fixed.

The initial mutant must first fix its initial module. Thus

`rho^0_U=((C+m)/N) a_H^U P_H^U +(2q/N) a_P^U P_P^U`.

The rational dependence on fitness follows from finite harmonic linear systems. Positive event denominators and positive transient `M`-matrix determinants permit clearing denominators. Universal polynomial inequalities on an algebraic interval are decidable, so the least admissible positive dyadic exponent exists and is computable. Its computation may be impractical; effectiveness is the theorem's claim, not an efficiency bound.

## 3. Why the center estimates are at the required scale

The relevant gain is `eta=q/C=C^{-3/4}`. An `o(1)` center estimate alone would fail.

For one ordinary mutant while hub and pendants remain resident, the exact down/up odds are `r^{-1}(1+O(C^{-1}))` up to `K=A log C`. The ordinary change intensity is proportional to its count, while hub activation has an extra factor `1/C`. Conditional expected count changes before `{0,K}` are `O(K)`. Thus the probability of an intervening hub change is `O(K/C)`, and the product-odds establishment probability is `p+O(K/C)+O(r^{-K})`, `p=1-1/r`. Both an upper bound and a lower bound follow: without a hub interruption, reaching count zero is global extinction, while reaching `K` invokes completion.

For every hidden hub/pendant state the ordinary up/down odds are uniformly greater than one from count one through a fixed density below one, once `C` is large. The exact rate tables, not a Markov assumption on the count marginal, give the conditional bias at the next count-change epoch. They justify the stopped exponential supermartingale. In the high-mutant core strip the deficit `R=C-1-i` has inward/outward odds at least `alpha R/(R+1)` for `alpha>1`. Above a fixed boundary layer, `exp(theta R)` controls an excursion to a macroscopic resident deficit by `exp(-gamma C)`. The total count-change intensity is `O(C)`, so only a polynomial prefactor is incurred through any polynomial time. Direct substitution also gives `G R <= -kappa R` outside the fixed boundary layer; this supplies the logarithmic return tail.

For Bd leaf synchronization, freeze the leaf count `ell` and use hub phases. With activation `a`, deactivation `b`, leaf gain `u`, and loss `v`, the exact next-leaf-gain committors are

`p_0=au/[au+v(b+u)]`, `p_1=u(a+v)/[au+v(b+u)]`.

Here `p_1>=p_0`. Replacing activation/gain by lower rates and deactivation by an upper rate gives a subharmonic function even while the core moves; core jumps leave it constant until strip exit, assigned success value one. Its gain/loss odds are at least `r_-^2/(1+2delta)*(1-o(1))>1`. The stopped leaf-count trace therefore needs `O(m)` expected changes, and each change takes `O(C)` expected calendar time, uniformly over hidden core histories. This gives `E Sigma=O(Cm)` up to synchronization or strip exit.

After hub and all leaves are mutant, suppressing hub loss gives the exact Bd deficit drift

`G R=-R[r/(C-1+m)+(r-1)(1-R/(C-1))]`.

Its negative drift bounds the expected accumulated deficit before cleanup by `2delta(C-1)/kappa`. Hub-loss hazard is `R/(C-1)`. Jensen's inequality gives a fixed positive probability of no hub loss through cleanup, `>=exp(-2delta/kappa)-o(1)`. Nested strips bound exceptional escapes and return times after ordinary failures. Strong-Markov repetition over `O(log C)` polynomially bounded blocks makes the completion failure `O(C^{-B})` for every fixed `B`, plus an exponential confinement error. It does not require independent blocks.

Under dB, leaf copying of a mutant hub is pure death of resident leaves at rate one each. Once `R` is in its fixed boundary layer and the hub is mutant, hub deactivation intensity is at most `K(R+m-ell)/C`. Under suppressed deactivation, integrated deficit is bounded and integrated resident-leaf count is at most `m`, so deactivation costs `O(m/C)=o(1)`. At time `beta log C`, resident-leaf and deficit tails can each be made `O(C^{-B-2})`; `beta` must depend on both the decay rate and `m=O(C^{1/4})`, as it does in the submitted proof. Repeated activated attempts give the analogous arbitrary polynomial failure bound.

Consequently core starts give `p+o(eta)`. The distinguished hub's averaged mass `1/C` is itself `o(eta)`. For Bd a mutant leaf has activation probability `1-O(1/C)` before its loss, and a core-seeding success probability at least a constant divided by `m` in each hub excursion. The original leaf's per-trial loss probability is `O((1+K)/C)`. A graphical deletion coupling gives a valid adverse trial process and a renewal loss/success ratio `O(m(1+K)/C)=o(1)`. For dB, a mutant leaf dies at rate one while hub activation is only `O(1/C)`; activation is necessary. Thus

`a_H^Bd=(Cp+m)/(C+m)+o(eta)`,

`a_H^dB=Cp/(C+m)+o(eta)`.

## 4. Reciprocal invasion, separately from beneficial establishment

At reciprocal fitness `s=1/r`, with hub resident and no mutant leaves, the ordinary-count process below `delta C` has up/down odds at most `vartheta<1` and drift at most `-kappa i`. Its probability of reaching `delta C` from a bounded count is exponentially small, its expected integrated count is bounded, and the integrated count above level `L` has an exponentially decreasing tail. Since hub activation hazard is `O(i/C)`, activation costs `O(1/C)` with the same hazard-weighted count tail.

A crude `O(1/C)` bound is insufficient. Starting instead with a mutant hub and bounded ordinary cloud, Bd hub loss is at least `m`, while ordinary changes are `O(1)` and pendant seeding `O(m/C)`. Hence its fixation probability tends to zero. Under dB, before hub loss the ordinary cloud is dominated by a subcritical birth-death process with immigration. Its exponential Lyapunov function `z^i` bounds the maximum through a *fixed* time. The hub has uniformly positive loss hazard before a macroscopic ordinary excursion. Splitting at fixed time `T` proves tightness of the cloud through hub loss by first increasing a finite cloud cutoff and then `T`; an infinite-horizon maximum of an immigration process is not assumed bounded.

After hub loss, suppressed hub reactivation leaves a subcritical ordinary cloud and at most `m` mutant leaves with pure-death clearance. The probability of reactivation before clearance is `O((m+a_L)/C)=o(1)` for fixed cutoff `L`; a larger-count excursion is charged separately by the subcritical tail. These statements make mutant-hub fixation `o(1)`. Combining this with the first-activation hazard and then increasing the fixed cutoff yields ordinary-start fixation `o(1/C)`, rather than merely `O(1/C)`. Averaging or portal weighting gives

`u_core^Bd(1/r)=o(1/C)`, `J_H(1/r)=o(1/C)`.

The order of fixed-cutoff limits is essential, and the submitted inequalities support it uniformly on the fixed fitness compact. This is the load-bearing reciprocal estimate in the global sweep.

## 5. Exact macro ladder, including adverse reversals

Set `I_H=sum_{x in clique}1/d_x`, `J_H(r)=sum h_H({x};r)/d_x`, `I_P=2/W`, `J_P=1/W`, and `W=C/sigma`. Directly summing weak cross events and then local committors gives four per-pair rates:

| Rule | mutant pair -> resident center A | resident center -> mutant pair D | mutant center -> resident pair B | resident pair -> mutant center E |
|---|---|---|---|---|
| Bd | `C r I_P u_core(r)` | `2 I_H/(r+1)` | `2r I_H r/(r+1)` | `C I_P u_core(1/r)` |
| dB | `2r J_H(r)` | `(C/r)J_P(1/r)` | `Cr J_P(r)` | `(2/r)J_H(1/r)` |

The actual macro rates carry factors `k` or `q-k` according to the number of source pairs. These common outgoing factors cancel in harmonic equations. Let `f_k` and `g_k` denote fixation from resident and mutant center with `k` mutant pairs. Their equations are

`(A+D)f_k=A g_k+D f_{k-1}`,

`(B+E)g_k=B g_{k+1}+E f_k`.

With `Delta_k=g_k-f_k`, one obtains `Delta_{k+1}=x Delta_k`, `x=D(B+E)/(B(A+D))`. Boundary values `f_0=0`, `g_q=1` give the independent closed forms

`P_H=g_0=[1+(E/B) sum_{j=0}^{q-1}x^j]^{-1}`,

`P_P=f_1=[A/(A+D)](1+E/B)P_H`.

Exact rational harmonic solutions confirm them at 14 parameter/order controls, including substantial adverse reversals. Alternatively, the probability of a first reversal along the monotone conversion path is at most `q E/(B+E)`. The reciprocal bounds give `E/B=o(1/C)`, so `1-P_H=o(q/C)`. The limiting pair gate odds are

`A/D -> sigma(r^2-1)` for Bd,

`A/D -> 2r(r-1)/sigma` for dB.

This establishes global fixation after center establishment; pair survival alone was not substituted for fixation.

## 6. Response algebra, tangency, and quantifiers

Combining the trace with the center estimates, pair committors and gate limits, writing `eta=q/C`, and expanding the population denominator `1+(lambda+2)eta` gives

`rho_Bd^0/rho_Bd(K_N)=1+eta[2(sigma-1)/(1+sigma(r^2-1))+lambda/(r-1)]+o(eta)`,

`rho_dB^0/rho_dB(K_N)=1+eta[2(r(2-r)-sigma)/(sigma+2r(r-1))-lambda]+o(eta)`.

The baseline errors are exponentially small for Bd and `O(1/C)=o(eta)` for dB. Pair-start terms require only `o(1)` accuracy because their mass is already `O(eta)`. Core-center sweep requires `o(eta)`, which is why Section 4 mattered.

Both responses are positive exactly when `L(r,sigma)<lambda<U(r,sigma)`. Their gap is

`U-L=-2r F_r(sigma)/[(1+sigma(r^2-1))(sigma+2r(r-1))]`,

`F_r(sigma)=(r-1)sigma^2+(r^3-4r^2+3r+1)sigma+r(2r-3)`.

The discriminant is precisely the submitted sextic `P(r)`; the minimum equals `-P(r)/(4(r-1))`. Exact Sturm counting gives zero roots on `(1,3/2)` and one on `(3/2,151/100)`, with endpoint values `1/64` and `-39866792399/10^12`. At the unique first root the positive minimizer is `sigma_*` and `lambda_*=L=U`. For this fixed `sigma_*`, `L` is strictly increasing and `U` strictly decreasing throughout `(1,R_hyb)`. Consequently the same fixed parameter pair gives strict positivity throughout that open interval, and no fixed pair can continue an interval beginning at one immediately beyond it. This is a response-model optimality result only.

Independently, the rational pair `sigma=19/137`, `lambda=20/27` gives exact positive responses `232/17361` and `65/12123` at `3/2`. Its first dB zero is `(5069+12 sqrt(147001))/6439>3/2`; Bd is still positive there.

For fixed `r` in the open algebraic interval, eventually `r` lies in `I_t=[1+1/t,R_hyb-1/t]`. The normalized separated gain, multiplied by `N/q`, tends to a strictly positive response. The dyadic definition perturbs it by at most `1/t`. Hence every sufficiently large connected graph in one previously fixed sequence amplifies under both update rules. No interchange of the growing-population and weak-cut limits is required. No conclusion is obtained at `r=R_hyb`, for a fitness approaching the endpoints with population size, or above the response-model threshold.
