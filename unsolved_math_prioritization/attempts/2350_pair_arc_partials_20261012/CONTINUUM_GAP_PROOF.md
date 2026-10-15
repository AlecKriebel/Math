# An explicit gap in the nonlinear continuum cover problem

12 October 2026. Authored mathematical proof and exact certificate. No publication, repository mutation, or novelty claim. Arithmetic applications remain conditional on independently establishing the stated continuum inequality for the limits under consideration.

## Theorem

Let `d:[0,1] -> [0,1]` be Lebesgue measurable. Suppose that for almost every `(x,y,z)` in the open simplex

    Delta = {x,y,z > 0 : x+y+z < 1},

with `w=x+y+z`, one has

    d(x)+d(y)+d(z)+d(w)
      >= 1 + (2/3)[d(x)d(y)+d(x)d(z)+d(y)d(z)].       (N)

Then

    integral_0^1 d >= 1/5 + 1/6075 = 1216/6075.

In particular there is a uniform explicit improvement over `1/5`, with no assumption of continuity, uniqueness of a linear optimizer, or realizability by an arithmetic deletion set. This is a lower bound, not a claimed sharp optimum.

The proof also gives the slightly stronger irrational bound

    integral_0^1 d >= 1/5 + (18-8 sqrt(5))/675.

The principal exact rational certificate below uses only `1/6075`.

## 1. Passing a null-supported coupling through smooth densities

We first justify carefully all uses of the one-dimensional coupling. Extend `d` by zero outside `[0,1]`. For a bounded measurable function `f` on a bounded interval, its zero extension belongs to `L1(R)` and

    sup_{|v| <= h} integral_R |f(u+v)-f(u)| du -> 0  as h -> 0.   (1)

For completeness, approximate `f` in `L1` by a continuous compactly supported function `g`. Translation preserves the two approximation errors, while the translated `g` converges uniformly on a common compact set. This proves (1), including the displayed uniformity. Consequently, if `r(t)=t+c` or `r(t)=c-t`, then

    integral_I |f(r(t)+v)-f(r(t))| dt
      <= integral_R |f(u+v)-f(u)| du.                         (2)

For values in `[0,1]`, products are equally well behaved because

    |a b - a' b'| <= |a-a'|+|b-b'|.                          (3)

Here is an explicit smoothing of the required singular coupling. Fix `0<delta<1/100`, set `epsilon=delta/10`, and choose an even nonnegative `C-infinity` probability density `rho_epsilon` supported on `[-epsilon,epsilon]`. Give the parameter interval

    I_delta = [delta,1/5-delta]

ordinary Lebesgue mass `dt`. At parameter `t`, independently choose a uniform permutation of the sources

    (t, t+1/5, 3/5-t),

and then add three independent noises `Z1,Z2,Z3`, each with density `rho_epsilon`, to those source roles. The target is the sum of the resulting sources, namely

    4/5+t+Z1+Z2+Z3.

This source measure has a nonnegative smooth density `W_delta`: it is the convolution of the finite source measure with the smooth compactly supported product density. Its mass is `1/5-2delta`. Every source is at least `9delta/10>0`, and the target is at most `1-7delta/10<1`. Thus `W_delta` is compactly supported in `Delta`, so the assumed almost-everywhere inequality may be integrated against it.

The aggregate source marginal before noise is `1_{U_delta}`, where

    U_delta = [delta,1/5-delta]
              union [1/5+delta,2/5-delta]
              union [2/5+delta,3/5-delta].

After noise it is `1_{U_delta} * rho_epsilon`. The target marginal is

    1_{V_delta} * rho_epsilon * rho_epsilon * rho_epsilon,
    V_delta = [4/5+delta,1-delta].

Both densities are bounded by one. Their supports are disjoint: the source support ends at `3/5-9delta/10`, while the target support begins at `4/5+7delta/10`. Hence the aggregate four-role density is bounded by one. More importantly, the source and target marginal densities converge in `L1` respectively to `1_(0,3/5)` and `1_(4/5,1)` as `delta -> 0`.

Let

    Q = integral_0^(1/5) [
          d(t)d(t+1/5)
          + d(t)d(3/5-t)
          + d(t+1/5)d(3/5-t)] dt.

Equations (1)--(3), applied separately to each source role, show that the integral of the sum of the three pair products against `W_delta` converges to `Q`. Source permutations do not change that sum. The omitted parameter ends have total length `2delta`, with uniformly bounded integrands; target noises, being bounded in absolute value by `3epsilon`, likewise cause no difficulty. This is an `L1` translation argument for the fixed measurable `d`, not evaluation of the assumed inequality on a null set.

Integrate (N) against `W_delta` and let `delta -> 0`. We obtain

    integral_0^(3/5) d + integral_(4/5)^1 d >= 1/5+(2/3)Q.     (4)

In particular, on defining

    e = integral_0^1 d - 1/5,
    G = integral_(3/5)^(4/5) d,
    J = integral_0^(1/5) d(t)d(t+1/5) dt,

we have the fundamental inequality

    e >= G+(2/3)J.                                          (5)

This proves at once that `e>=0`. Notice that (5) discards the other two nonnegative terms of `Q`, so it does not require any characterization of linear minimizers.

## 2. A scale-local linear cover lower bound

Dropping the nonnegative quadratic terms from (N) gives the ordinary cover condition

    d(x)+d(y)+d(z)+d(x+y+z) >= 1 a.e. on Delta.              (L)

If a measurable `f:[0,1]->[0,1]` satisfies (L), the very same smoothed coupling, with no pair-product terms, gives

    integral_0^1 f >= 1/5.                                  (6)

For any `0<a<=1`, the function `f(u)=d(au)` satisfies (L): the linear change of variables takes the full unit simplex into the original simplex and preserves null sets. Scaling (6) therefore gives

    integral_0^a d >= a/5.                                  (7)

Apply this with `a=1/15` and put

    M = integral_0^(1/15) d,
    T = {t in (0,1/15) : d(t)>=1/10},
    beta = |T|.

Then `M>=1/75`, while the range `0<=d<=1` yields

    M <= (1/10)(1/15-beta)+beta = 1/150+(9/10)beta.

Consequently

    beta >= 1/135 > 0.                                     (8)

This sharper level-set estimate retains the factor `1-1/10`; the weaker estimate `M<=1/150+beta` would not give the stated final constant.

## 3. Triple products of the positive level set

Define

    E = 1/5+T,
    u = integral_T d(1/5+t) dt = integral_E d.

Every triple of points of `E` is in the open simplex, and its sum lies in `(3/5,4/5)`, because `0<t_i<1/15`. Integrating (L) on `E^3` is legitimate by its almost-everywhere hypothesis and Fubini. The three source terms have total integral `3 beta^2 u`.

For the target term, extend `1_E` by zero to `R`. Its triple convolution obeys, for every `s`,

    (1_E * 1_E * 1_E)(s)
       = integral_{E^2} 1_E(s-x-y) dx dy <= beta^2.

Its support lies in the closure of `(3/5,4/5)`, whose endpoints are irrelevant for integration. Thus Tonelli gives

    integral_{E^3} d(x+y+z) dx dy dz <= beta^2 G.

The integrated cover inequality now implies

    beta^3 <= beta^2(3u+G).

Since (8) makes `beta>0`, division is justified and gives

    G+3u >= beta.                                          (9)

By the definition of `T`,

    J >= integral_T d(t)d(t+1/5) dt >= (1/10)u.              (10)

Combining (8)--(10),

    G+30J >= 1/135.                                        (11)

Finally, (5), nonnegativity of `G`, and (11) give

    45e >= 45G+30J >= G+30J >= 1/135.

Therefore `e>=1/6075`, proving the theorem.

## 4. An exact finite linear certificate for the concluding algebra

After the justified integral constructions above, only the following six inequalities are used:

    A: e-G-(2/3)J >= 0,
    B: M-1/75 >= 0,
    C: 1/150+(9/10)beta-M >= 0,
    D: J-(1/10)u >= 0,
    E: G+3u-beta >= 0,
    F: G >= 0.

Their nonnegative exact rational combination

    45 A + (10/9) B + (10/9) C + 30 D + E + 44 F

is precisely

    45e-1/135 >= 0.

This finite certificate is checked independently using sparse-polynomial rational arithmetic. The same script checks all rational endpoints, interval masses, convolution bounds on exhaustive finite models, and the optimized threshold algebra. Those checks are sanity checks of the arithmetic and elementary estimates; they do not replace the measurable-analysis proof above.

## 5. Optional threshold optimization

Keep `a=1/15`, but use the threshold `0<tau<1/5`. Equations (7) and the level-set estimate give

    beta >= a(1/5-tau)/(1-tau).

The translated triple argument and pair bound give `G+(3/tau)J>=beta`. Since (5) implies

    (9/(2tau))e >= (9/(2tau))G+(3/tau)J >= G+(3/tau)J,

we obtain

    e >= (2/135) tau(1/5-tau)/(1-tau).

This expression is maximized at `tau=1-2/sqrt(5)`, where its value is

    (2/135)(1-2/sqrt(5))^2 = (18-8sqrt(5))/675
      = 0.000165120266669159... .

The exact rational choice `tau=1/10` gives the main margin `1/6075 = 0.000164609053497942...`. No numerical optimization is needed for either conclusion.

## Scope and dependencies

- The result is a self-contained continuum theorem conditional only on (N).
- The original first-moment optimizer `h(t)=(3/5-t)_+ +(t-4/5)_+` is neither assumed unique nor used in this proof.
- The given one-fifth singular coupling is used only through the explicit smooth interior densities and fixed-function `L1` limits in Section 1.
- There is no compactness argument, no inferred optimum from discretization, and no numerical solver in the proof.
- An application to Bose--Chowla deletion densities still requires a separately valid arithmetic pair-incidence law and a rigorous passage from finite deletions to (N). These inputs are not proved here.
- If those inputs hold, this theorem would replace the retention constant `4/5` by at most `4859/6075` (or the slightly smaller optimized constant). This is not claimed here as an unconditional arithmetic conclusion.


## Public editorial notice

All mathematical statements, proofs, examples, substantive audit arguments and scope limitations are retained. EDITION_NOTES.md describes the nonmathematical editorial changes: updated acceptance history, public dependency links and removal of excluded provenance metadata. The distributed edition is identified by MANIFEST.json. The complete one-vertex dependency and its audits are linked in DEPENDENCIES.md. Diagnostic summaries report checks rather than replacing mathematical proof. Independent internal AI acceptance is not external human peer review or proof-assistant certification.
