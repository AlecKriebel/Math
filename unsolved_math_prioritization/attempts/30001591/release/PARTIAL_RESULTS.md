# Borderline soliton–potential interactions: rigorous partial results

Problem 30001591 / OWR-4429-002. **Unsolved.** These are authored mathematical deductions; they do not prove the requested long-time PDE asymptotic. There is no novelty claim. All limits in the PDE question keep a positive, sufficiently small epsilon fixed and then let time tend to infinity.

## Notation

Let m be 2, 3, or 4. Set q=(5-m)/(m+3), p=4/(m+3), alpha=2/(m-1)-1/2=q/(1-q), and beta=1/(m-1)-1/2. The positive decaying solution of Q''-Q+Q^m=0 is

Q(x)=[(m+1)/(2 cosh^2((m-1)x/2))]^(1/(m-1)),
Q_c(x)=c^(1/(m-1)) Q(sqrt(c)x).

The critical number lambda=lambda_tilde is the unique point of (q,1) satisfying

lambda ((1-q)/(lambda-q))^(1-q)=2^p.                    (T)

Uniqueness follows since the logarithmic derivative of the left side, viewed as a function of lambda, is q(lambda-1)/(lambda(lambda-q))<0; its endpoint limits are infinity and 1. For m=4 this number is exactly 1/4, by substitution and uniqueness.

Throughout the ODE results, a is C^1, strictly increasing, 1<a<2, with limits 1 and 2. Where needed, exponential decay or the stronger exact tail asymptotic is separately stated. The PDE results explicitly state their regularity and decay hypotheses.

## 1. The exactly normalized critical modulation orbit

This section concerns an auxiliary ODE, not an exact PDE solution:

C'=epsilon p C(C-lambda/q) a'(epsilon P)/a(epsilon P),
P'=C-lambda.                                               (O)

Define, for 0<c<lambda/q,

H(c)=c^q ((lambda-q c)/(lambda-q))^(1-q).

Its logarithmic derivative is

H'(c)/H(c)=q(lambda-c)/(c(lambda-q c)).                      (1.1)

Consequently every orbit of (O) in this strip conserves H(C)/a(epsilon P)^p. An orbit incoming from C=1, P=-infinity has invariant 1. At (T), H(1)=1 and H(lambda)=2^p. H is strictly decreasing on (lambda,1). Thus, for each P in R, there is exactly one C_*(P) in (lambda,1) with

H(C_*(P))=a(epsilon P)^p.                                  (1.2)

The implicit-function theorem makes C_* continuously differentiable at every finite P. Solve P'=C_*(P)-lambda by separation. The solution exists for all real time: the positive derivative is bounded above by 1-lambda, so reaching either spatial infinity takes infinite time; conversely a finite endpoint limit P would have strictly positive speed, impossible. Differentiating (1.2) shows that (C_*(P(t)),P(t)) solves (O). In particular,

P(t) -> +infinity, C(t) decreases to lambda, P'(t)>0 and P'(t)->0.

This proves slow escape only for the auxiliary ODE. Under a(r)-1=O(exp(gamma r)) as r->-infinity, (1.1) at c=1 is nonzero. Hence C_*(P)-1=O(exp(gamma epsilon P)), and integration of dt/dP gives P(t)-(1-lambda)t tending to a constant. Time translation fixes that constant to zero.

For the outgoing asymptotic, (1.1) yields

H''(lambda)/H(lambda)=-q/[lambda^2(1-q)].

Taylor expansion at the maximum, followed by expansion of a^p at a=2, gives the exact leading relation

(C_*(P)-lambda)^2 ~ [p lambda^2(1-q)/q] [2-a(epsilon P)].    (1.3)

If, additionally, 2-a(r)~A exp(-kappa r) for A,kappa>0, put D=lambda sqrt(p(1-q)A/q). Then

P'(t)~D exp(-kappa epsilon P(t)/2),
exp(kappa epsilon P(t)/2)~(kappa epsilon D/2)t,
P(t)=(2/(kappa epsilon)) log t+O_epsilon(1),
P'(t)~2/(kappa epsilon t).                                (1.4)

The second line follows by differentiating exp(kappa epsilon P/2): its derivative tends to kappa epsilon D/2, and integrating gives the ratio limit. Substitution proves the remaining lines. The exact tail equivalence is stronger than the source's upper exponential bound; (1.4) is not claimed for every admitted potential. No PDE approximation estimate valid for all t is established here.

## 2. Stationary capture and a cubic compactness obstruction

### 2.1 No nonzero H^1 stationary state under strict monotonicity

Assume epsilon,lambda>0; a and a' are bounded and continuous; a>0 and a'>0 everywhere. A real H^1 stationary distributional solution of the PDE must vanish, for each m=2,3,4.

Indeed, its equation implies U''-lambda U+a(epsilon x)U^m is a constant distribution. This distribution belongs to H^-1(R), since U is H^1 and U^m is L^2 by the one-dimensional H^1 embedding. A nonzero constant does not belong to H^-1(R): test against smooth functions equal to one on an interval of length R, with H^1 norm O(sqrt(R)), while their integrals are order R. Thus the constant is zero. It follows that U'' is L^2, U is H^2, and U,U' tend to zero at both infinities. The equation and continuity also give U in C^2.

For even m, any negative value of U would give a negative global minimum (because U tends to zero). At its minimum x_0,

U''(x_0)=lambda U(x_0)-a(epsilon x_0)U(x_0)^m<0,

contrary to the second derivative test. Hence U is nonnegative. For odd m=3, no sign assumption is needed. Multiply the stationary ODE by U' and integrate. The boundary terms vanish, giving

0=-(epsilon/(m+1)) int_R a'(epsilon x) U(x)^(m+1) dx.

The integrand is nonnegative in all three cases and strictly positive wherever U is nonzero. It follows that U=0.

This excludes literal stationary trapping at a finite location. It does not exclude a soliton whose center escapes while its velocity tends to zero, a persistent radiative component, or nonstationary recurrent behavior.

### 2.2 Cubic positive-energy solutions cannot have a precompact forward orbit

Let m=3 and assume a' is bounded and strictly positive. Suppose a global real H^1 solution satisfies the energy conservation law and the integrated mass identity

M(u(t))=M(u(0))-(epsilon/4) int_0^t int_R a'(epsilon x)u(s,x)^4 dx ds,

where M(v)=int v^2/2, and suppose its conserved energy E is positive. Then {u(t):t>=0} cannot be relatively compact in H^1(R).

Otherwise its closure K is compact and, by continuity of energy in H^1, has constant energy E>0, so 0 is not in K. The functional F(v)=int a'(epsilon x)v^4 is continuous in H^1 and positive on every nonzero member of K. It has a strictly positive minimum delta on K. The mass identity then gives M(u(t))<=M(u(0))-epsilon delta t/4, contradicting M>=0.

For the incoming solution of the question, continuity of energy, the incoming H^1 convergence, and a(epsilon x)->1 along the translating soliton imply E=(lambda-q)M(Q)>0 at the critical lambda. The energy computation is proved in Section 3. Thus the compactness obstruction applies whenever the stated standard conservation identities are available for this solution. A precompact family after translations with unbounded centers is not ruled out. No positivity-preservation assertion is made for gKdV.

## 3. Exact energy matching and its branch-selection failure

For a sufficiently regular decaying real solution define

E_a(u)=int [u_x^2/2+lambda u^2/2-a(epsilon x)u^(m+1)/(m+1)].

Its variational derivative is -u_xx+lambda u-a(epsilon x)u^m=-F, while u_t=-F_x. Thus dE_a/dt=int F F_x=0. Similarly, integrating u u_t and integrating by parts gives

dM/dt=-(epsilon/(m+1)) int a'(epsilon x)u^(m+1).             (3.1)

These computations are exact for smooth decaying solutions; their extension to H^1 solutions needs an approximation/flow argument. The partial statements relying on them explicitly assume the identities, rather than supplying that well-posedness argument.

Write L=int Q_c^2, K=int (Q_c')^2, N=int Q_c^(m+1). Multiplying Q_c''-cQ_c+Q_c^m=0 first by Q_c and then by xQ_c' gives

K+cL=N, and K/2-cL/2+N/(m+1)=0.

Therefore K=(m-1)cL/(m+3), N=2(m+1)cL/(m+3). Since L=c^alpha int Q^2, the constant-coefficient energy at the soliton A^(-1/(m-1))Q_c is

E_A(c)=A^(-2/(m-1)) M(Q) c^alpha (lambda-q c).              (3.2)

Let f(c)=c^alpha(lambda-q c). The identity alpha=q/(1-q) gives

f'(c)=alpha c^(alpha-1)(lambda-c).

Thus f has its unique global maximum for c>0 at c=lambda. Raising (T) to the positive power 1/(1-q) proves

E_2(lambda)=M(Q)(lambda-q)=E_1(1).                          (3.3)

If the incoming solution is globally H^1-asymptotic at plus infinity to 2^(-1/(m-1))Q_c translated by a center tending to plus infinity, conservation and continuity of energy imply E_2(c)=E_1(1). Potential convergence in this step follows by dominated convergence after translating the exponentially decaying profile; the H^1 error contributes o(1) since a is bounded. Equations (3.2)-(3.3) force c=lambda. Consequently energy forbids a globally pure, positive-terminal-speed transmitted soliton at critical lambda, but does not rule out the proposed zero-speed endpoint.

For a hypothetical decomposition with an energy-decoupled radiation remainder of asymptotic energy D, conservation instead gives D=E_2(lambda)-E_2(c). Here energy-decoupled means precisely that E_a(u)-E_2(c)-E_a(w)->0 and E_a(w)->D; existence of such a decomposition is not asserted. As c->lambda,

D=2^(-2/(m-1))M(Q) [alpha lambda^(alpha-1)/2](c-lambda)^2
  +O(|c-lambda|^3).                                       (3.4)

This shows that a positive small defect is compatible with two nearby algebraic scales on opposite sides of lambda. Energy alone does not select the dynamics; kinematic restrictions and a controlled PDE decomposition would still be needed. The quadratic degeneracy also explains why a small energy error cannot be converted to a linear scale error at this endpoint.

On the left, E_1(c)=E_1(1) has exactly one root c_R in (0,lambda): f increases from zero to f(lambda)>f(1)>0 there. The other positive root is c=1. Thus energy alone also permits a pure reflected terminal scale c_R. This is an algebraic compatibility statement, not existence of a reflected PDE solution at equality.

## 4. Signed-integral conservation and the escaping-tail obstruction

For solutions for which the spatial integral and boundary fluxes are controlled, integrating the PDE gives conservation of I(u)=int u. This is a signed integral, not the L^1 norm. If incoming convergence also holds in L^1, its value is I(Q)>0. Merely assuming the incoming H^1 convergence in the question does not establish this value by itself.

Scaling gives

I(A^(-1/(m-1))Q_c)=A^(-1/(m-1))c^beta I(Q),
beta=(3-m)/(2(m-1)).                                      (4.1)

At the only pure transmitted scale allowed by energy, c=lambda, the ratio to the incoming integral is

m=2: sqrt(lambda)/2 < 1;
m=3: 1/sqrt(2) < 1;
m=4: 2^(-1/3)lambda^(-1/6) = 1,

where the last equality uses the exact critical value lambda=1/4. Consequently, a pure transmitted critical asymptotic in both H^1 and L^1, together with conserved signed integral equal to I(Q), is impossible for m=2 or 3. For m=4, the signed-integral and energy conditions are exactly compatible. This exceptional cancellation prevents even the strengthened L^1 argument from solving all three cases.

For a pure reflected endpoint c_R from Section 3, the ratio is c_R^beta. Because 0<c_R<lambda<1, this differs from 1 for m=2 and m=4, but equals 1 for m=3. The same strengthened L^1 argument excludes those reflected endpoints only in the even cases.

Here is an explicit obstruction to removing the extra L^1 hypothesis. Choose a smooth compactly supported function phi with int phi=1, and any nonzero real number b. Set

w_L(x)=(b/L) phi(x/L), L>1.

Then int w_L=b, while

||w_L||_H1^2=(b^2/L)int phi^2+(b^2/L^3)int (phi')^2 -> 0.

Translations can place this low-amplitude broad tail arbitrarily far from a soliton without changing either identity. These functions are a functional-analytic control, not constructed PDE radiation. They show rigorously that global H^1 smallness or convergence does not make signed-integral discrepancies disappear. Thus the signed-integral approach requires genuine PDE tail/tightness control that has not been established at equality.

## 5. Higher-order drift, finite initialization, and threshold instability

To test whether a more accurate modulation estimate could settle the PDE, assume also that a is C^2, and consider any C^1 parameter curves in 0<C<lambda/q satisfying the perturbed system

C'=epsilon p C(C-lambda/q)a'(epsilon P)/a(epsilon P)+r_C,
P'=C-lambda+r_P.

No assertion is made that the unknown critical PDE already supplies such curves with usable errors. Direct differentiation gives the exact identity

d/dt log[H(C)/a(epsilon P)^p]
 = [q(lambda-C)/(C(lambda-q C))]r_C
   -p epsilon [a'(epsilon P)/a(epsilon P)]r_P.              (5.1)

Thus a uniform local error bound alone is inadequate: the time integral of the right side, including its sign, matters. An error bound O(epsilon^k) on a time interval of unbounded length does not imply an O(epsilon^k) accumulated error. Even a small, convergent integral can move the invariant to either side of its critical value.

This sensitivity can be proved without numerical evolution. Fix the same critical lambda and consider exact unperturbed ODE orbits with invariant J=H(C)/a(epsilon P)^p close to 1.

* If 0<J<1, choose a point on the branch C>lambda. The outgoing limiting equation H(c)=J 2^p has a unique root c>lambda within (lambda,lambda/q). The orbit remains on that branch, P tends to plus infinity, and P' tends to c-lambda>0. This follows by the same inverse-function and separation argument as Section 1. The whole orbit lies in a compact positive C-subinterval of (lambda,lambda/q).
* If 1<J<2^p, there is a unique finite turning location P_* with a(epsilon P_*)=2 J^(-1/p). The upper branch exists for P<P_*. At the turning point C=lambda, its time derivative is strictly negative, since a'>0, so the smooth ODE crosses to C<lambda and P has a strict local maximum. Arrival is in finite time: Taylor expansion at H's nondegenerate maximum gives C-lambda comparable to sqrt(P_*-P), whose reciprocal is integrable. Thereafter C decreases, P decreases to minus infinity, and C approaches the unique root in (0,lambda) of H(c)=J. To see that no other forward endpoint occurs, the invariant bounds C away from zero, global boundedness prevents finite-time breakdown, and any finite limiting P with limiting C=lambda would contradict C'<0 there. Thus this branch reflects.

For J<1 sufficiently close to 1, the terminal transmitted speed satisfies

(c-lambda)^2 ~ [2 lambda^2(1-q)/q](1-J).                   (5.2)

This is Taylor's theorem applied to H(c)=JH(lambda). Both transmission and reflection therefore occur for arbitrarily small changes of this *ODE* invariant. They are not PDE counterexamples to any proposed critical behavior.

There is also a definite finite-start bias. If the unperturbed system is initialized at a finite negative point P_0 with C_0=1, then

J=a(epsilon P_0)^(-p)<1.

Even at the exact critical lambda, this finitely initialized orbit is transmitted with a strictly positive terminal speed. If eta=a(epsilon P_0)-1 tends to zero, then 1-J~p eta and (5.2) yields

(c-lambda)^2 ~ [2p lambda^2(1-q)/q] eta.                   (5.3)

Hence one must not identify the source's finite-start modulation trajectory with the exactly incoming critical orbit of Section 1. Exponentially tiny initialization errors are still decisive at the degenerate endpoint. In the exact-tail model of (1.4), a uniform velocity uncertainty eta_0 ceases to determine the sign of the leading velocity on the scale t comparable to 1/(epsilon eta_0).

The attempted higher-order route stops at (5.1). There is no proved critical-PDE remainder estimate with a signed, controlled infinite-time integral, no outgoing scattering decomposition at equality, and no proof of which ODE branch (if any) accurately describes the PDE for all late times.

## Scope of the outcome

The five approaches establish auxiliary-orbit asymptotics, stationary-state exclusion, a cubic compactness obstruction, exact conditional energy and signed-integral restrictions, and a quantified instability of the reduced threshold. They do not classify the original PDE at lambda=lambda_tilde. In particular, there is no proof here of transmission, reflection, logarithmic PDE escape, convergence to a stationary state, a shifted epsilon-dependent threshold, or radiation size at equality. None of these conclusions follows by taking lambda to the endpoint in a theorem whose constants or escape times diverge. No numerical PDE experiment is used as asymptotic evidence.
