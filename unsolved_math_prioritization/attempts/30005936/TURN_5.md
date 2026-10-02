# Turn 5: a fixed-midpoint mean-square obstruction for the exact white-noise scheme

Substantive author turn **5/5**. Let the source equation have g(v)=v_+^(5/4), homogeneous Dirichlet boundary on [0,1], and **u0(x)=sin(πx)**. Set the final time T=1. Let u be the global nonnegative solution constructed in turn 3. For every even N and every positive integer M, the source's original LT recursion satisfies

 E U_{M,N/2} − E u(1,1/2) >= δ_* >0,                            (49)

where δ_* is independent of N,M. In particular

 (E|U_{M,N/2}−u(1,1/2)|²)^(1/2) >= δ_*                          (50)

with the left side allowed to be infinite. Taking M=N², so τ=h², disproves mean-square convergence to the continuum at this fixed point, and hence disproves a quarter-order mean-square extension to the source's superlinear example even on balanced meshes. This conclusion is about the **space-time-white-noise** equation and its spatially discretized source scheme.

The proof does not infer strict loss of expectation merely from a quadratic-variation lower bound. It uses an explicit concave backward Itô barrier and Fatou's lemma. Thus neither uniform integrability at a random clock nor equality in an unbounded optional-stopping argument is assumed.

This obstruction coexists with turn 4's same-noise convergence in probability and logarithmic bounded-Lipschitz path-law rate. The linear point observable is unbounded. The full source bundle, with unspecified rough coefficient class and unspecified weak test class, remains unresolved after five author turns.

## 1. Drift-removed weighted mass and its white-noise bracket

Write λ=π² and φ(x)=(π/2)sin(πx). Then φ is nonnegative, positive in the interior, zero at the endpoints, satisfies φ''=−λφ, and has integral1. Define

 X_t=∫_0^1 φ(x)u(t,x)dx,       V_t=e^(λt)X_t,       v=V_0=π/4.

Testing the localized mild equation against φ and using stochastic Fubini gives

 V_t=v+∫_0^t∫_0^1 e^(λs)φ(x)u(s,x)^(5/4) W(ds,dx).              (51)

Here localization at a bound for the continuous field makes the coefficient bounded, so stochastic Fubini and the weak equation are valid in L². The consistent cutoff solutions then give (51) as a local identity. Global nonexplosion from turn 3 implies that on every compact time interval the field and its weighted bracket are pathwise finite. Thus V is a continuous nonnegative local martingale, and in particular an integrable supermartingale. Its bracket is absolutely continuous with density

 σ_t²=e^(2λt)∫_0^1 φ(x)²u(t,x)^(5/2)dx.                         (52)

This is the integral of the **square** of the weighted noise integrand, as required for space-time white noise. It is not the square of its spatial integral, which would belong to a common time-only driver.

For any nonnegative continuous w, put X=∫φw and I=∫φ^(1/3). Hölder with exponents5/2 and5/3 gives

 X=∫(φ²w^(5/2))^(2/5)φ^(1/5)
   <=(∫φ²w^(5/2))^(2/5) I^(3/5).

Hence ∫φ²w^(5/2)>=X^(5/2)/I^(3/2). Since the interval has length1 and ∫φ=1, concavity gives I<=1. Consequently

             σ_t² >= e^(−λt/2)V_t^(5/2).                        (53)

All constants and the drift-removal exponent are explicit. At V=0 this inequality is harmless. Indeed nonnegativity, continuity and positivity of φ in (0,1) imply that X=0 only when the entire field is zero. The zero field is absorbing by local pathwise uniqueness, or by the absorbing-zero property of a nonnegative local martingale followed by the same spatial argument. No division by V at zero will occur in the proof.

## 2. An explicit concave barrier, including the endpoint at zero

For s>0,v>0 define

 b=8/(s sqrt(v)),
 F(s,v)=v[1−(1+b)e^(−b)],       F(s,0)=0.                         (54)

The elementary inequality e^b>1+b gives 0<F(s,v)<v. Direct differentiation gives

 F_v=1−(1+b+b²/2)e^(−b),
 F_vv=−b³e^(−b)/(4v) <=0,
 F_s=−v b²e^(−b)/s = (1/2)v^(5/2)F_vv.                         (55)

In particular F is concave in v. At v↓0, F_v→1 and F_vv,F_s→0; all inverse powers are dominated by e^(−8/(s sqrt(v))). These limits are locally uniform when s stays in a compact subset of (0,infinity). Extending F(s,v)=v for v<0 gives a C^(1,2) extension through zero on such time strips, if an open spatial neighborhood is desired for Itô's formula. Only nonnegative v is used. Also F(s,v)<=v and F(s,v)→v as s↓0 for each fixed v>=0.

For context, (54) is the classical mean formula for dY=Y^(5/4)dB: it is the inverse fourth power of a dimension-six Bessel radius. The needed identity and sign are fully verified in (55), so the proof below does not need a time-change theorem or an assumed moment formula. One can also check its normalization directly: for r=4v^(−1/4) and a six-dimensional Brownian motion B,

 4^4 E|z+B_s|^(−4)
 =4^4∫_0^infinity q(1+2sq)^(−3)exp(−q r²/(1+2sq))dq
 =4^4∫_0^(1/(2s)) a exp(−r²a)da
 =v[1−(1+r²/(2s))exp(−r²/(2s))],    |z|=r.

The first equality uses x^(−2)=∫_0^infinity q e^(−qx)dq and the elementary Gaussian Laplace transform, with Tonelli; the substitution is a=q/(1+2sq). This calculation is supplementary, not an integrability assumption about the SPDE.

## 3. Deterministic-time strict expectation loss, with all limit passages

Fix any deterministic t0>0 and set

 k(t)=e^(−λt/2),
 c(t)=∫_t^t0 k(r)dr,       0<=t<t0,
 c0=c(0)=2(1−e^(−λt0/2))/λ>0.

Apply Itô to H(t,V_t)=F(c(t),V_t), first for t<=t0−epsilon and stopped when either V or its quadratic variation reaches a large deterministic level. All derivatives are bounded on the resulting compact region, c stays positive, and the stopped stochastic integral has mean zero. By (53)–(55), the drift is

 −k(t)F_s(c(t),V_t)+(1/2)σ_t²F_vv(c(t),V_t)
   =(1/2)[σ_t²−k(t)V_t^(5/2)]F_vv(c(t),V_t) <=0.                 (56)

It follows that the expected stopped H is at most F(c0,v). On removing the stopping levels, the continuous path and bracket are finite on each compact physical-time interval. Thus the stopping times exceed each fixed t<t0 eventually almost surely. Since H>=0, **Fatou**, not uniform integrability, gives

                         E F(c(t),V_t)<=F(c0,v),  t<t0.           (57)

Let deterministic times increase to t0. Continuity gives V_t→V_t0. If V_t0>0, (54) gives F(c(t),V_t)→V_t0; if V_t0=0, the bound 0<=F(c(t),V_t)<=V_t gives the same conclusion. A second application of Fatou yields

 E V_t0 <= F(c0,v)
          =v[1−(1+b0)e^(−b0)] < v,
                  b0=8/(c0 sqrt(v)).                            (58)

This establishes strict loss at **every** deterministic t0>0, with no clock-stopping or optional-sampling gap. In original mass units,

 ∫φ(x)[S_t0 u0(x)−E u(t0,x)]dx >= δ_t0,
 δ_t0=e^(−λt0)v(1+b0)e^(−b0)>0.                                 (59)

The left identity uses the eigenfunction relation ∫φ S_t0u0=e^(−λt0)v and Tonelli for the nonnegative field. It is a finite quantity. This barrier argument shows directly why the bracket lower bound suffices, rather than treating “large bracket” as a synonym for strict local martingality.

## 4. Conditional killed-heat domination and propagation of the defect

For every fixed cutoff R, its bounded coefficient gives, at deterministic s<t and x,

 E[u^R(t,x)|F_s]=(S_(t−s)u^R(s))(x).                             (60)

By the global construction in turn 3, along integer R→infinity, u^R and u are eventually equal on every fixed compact space-time rectangle, almost surely: once R exceeds the path supremum, cutoff consistency applies throughout that rectangle. Conditional Fatou and nonnegativity therefore imply

 E[u(t,x)|F_s] <= (S_(t−s)u(s))(x).                              (61)

The right sides of (60) converge almost surely because of this eventual equality of the entire field at time s. No uniform integrability of the cutoff family is claimed. With s=0, (61) gives E u(t,x)<=S_tu0(x), so all point means in use are finite.

Put m(t,x)=E u(t,x) and d(t,x)=S_tu0(x)−m(t,x)>=0. Joint measurability follows from the continuous random-field version. Taking expectations in (61), using nonnegative Tonelli and the semigroup identity, gives

                  d(t,x)>=(S_(t−s)d(s,·))(x).                    (62)

The function d(s,·) is measurable, nonnegative and bounded above by S_su0, so this propagation formula requires no regularity assumption about its mean and no interchange of a Riemann sum with an expectation.

We use s=1/2,t=1 and an explicit lower bound for the Dirichlet heat kernel. The sine expansion and |sin(jθ)|<=j sinθ for θ in [0,π] give

 G(1/2,x,y)
 >=2e^(−π²/2)sin(πx)sin(πy)
           [1−Σ_(j>=2)j²e^(−(j²−1)π²/2)].                       (63)

The sine inequality follows by expressing sin(jθ)/sinθ as a sum of j unit complex numbers; endpoints follow by continuity. Since π²/2>4 and j²−1>=3(j−1) for j>=2, the sum is at most

 Σ_(k>=1)(k+1)²e^(−12k)
 <=Σ_(k>=1)(k+1)²(1/16)^k =977/3375 <1/2.                       (64)

Here e^12>16 already follows from its first three nonnegative Taylor terms, and π>3 suffices for π²/2>4. The positive coefficient in (63) is therefore at least1/2, and

 G(1/2,x,y)>=e^(−π²/2)sin(πx)sin(πy).

At x=1/2, (59) and (62) yield the fixed-point bound

 d(1,1/2) >= (2/π)e^(−π²/2) ∫φ(y)d(1/2,y)dy
           >= (2/π)e^(−π²/2) δ_(1/2) =: δ_* >0.                 (65)

Thus the weighted expectation deficit really reaches the **specified midpoint at the specified time**; it is not only an integrated mass statement or a statement about an unknown spatial point.

## 5. The original numerical scheme has the wrong limiting first moment

For a fixed old grid state U_m, every frozen geometric-Brownian multiplier has conditional expectation1, even though its variance may be very large. All values are nonnegative and finite at every finite step. Conditional Gaussian integration and induction using Tonelli therefore give

                    E U_(m+1)=P_τ E U_m,
                    E U_M=exp(TA_N)u0^N.                        (66)

In particular these first moments are finite; no higher numerical moment is needed. The sampled sine vector u0^N(n)=sin(πn/N) is an eigenvector of A_N with eigenvalue −λ_N, where

 λ_N=4N²sin²(π/(2N))<=π².

For even N and T=1, its midpoint entry is1. Consequently

 E U_(M,N/2)=e^(−λ_N)>=e^(−π²)
                         >=E u(1,1/2)+δ_*.                      (67)

Both random variables have finite first moment, and nonnegativity gives integrability of their difference. Jensen/Cauchy–Schwarz, in the extended sense if the second moment is infinite, gives (49)–(50) under the common-noise coupling and in fact under any coupling with these marginals.

Choose even N→infinity and M=N². This has h=1/N, τ=h², and T=1, and satisfies the source mesh condition with γ=1. The proposed Cτ^(1/4) continuum mean-square error bound would tend to zero, contradicting (50). The correctly distinguished full bound Ch^(1/2) would likewise tend to zero, so the obstruction is independent of the OWR continuum/semidiscrete display discrepancy. This does not assert a negative theorem for every different spatial or time integrator.

## 6. Exact scope, credit and remaining gap

- Numerical and exact positivity hold here. The midpoint continuum mean-square convergence claim fails for the exact source power5/4 example, even along balanced meshes.
- The unbounded 1-Lipschitz point observable F(w)=w(1,1/2) has a positive weak error bounded away from zero. It is not one of turn 4's bounded tests. The proven probability convergence and bounded-Lipschitz logarithmic rate are compatible with the failure of uniform integrability exposed by (67).
- No claim is made that the coupled mean-square error is infinite, that bounded smooth tests fail to converge, or that the logarithmic rate is optimal. The source does not specify a weak-test class, so an unqualified universal weak-rate answer would be misleading.
- The strict-local-martingale/mean-preservation obstruction and inverse-Bessel template are credited classical tools; related prior target30005935/PR317 used a common-noise mass strategy. The white-noise bracket (52), its weighted Hölder lower bound, the direct concave barrier and the fixed-midpoint heat propagation are proved here rather than imported from that different noise model. No novelty certification is made.

Together the five turns give a nonsmooth globally Lipschitz extension of the credited strong theorem, quantitative cutoff estimates, a subcritical exact exit bound, a bounded-test convergence theorem for the original superlinear scheme, and a negative mean-square subquestion. The full rough-coefficient/weak-rate bundle remains **unresolved5/5**. No sixth author search is proposed; the complete frozen packet requires independent review.
