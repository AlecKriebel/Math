# Turn 3: a finite, nonvanishing weak error for weighted mass

Status: the scheme fails even first-moment convergence for a natural linear observable. This does not rule out weak convergence for bounded smooth tests. The source bundle remains only partially answered, pending independent review.

Use the exact global local mild solution constructed in Turn2 and nonzero nonnegative smooth compactly supported u0 on D=(0,1). Let lambda=pi² and phi(x)=(pi/2)sin(pi x), so phi>0 inside D, phi vanishes at the boundary, integral phi=1 and Delta phi=-lambda phi.

## 1. Weighted exact mass as a time-changed CEV process

Put X_t=integral phi(x)u(t,x)dx and V_t=exp(lambda t)X_t. Testing the locally stopped mild equation against phi gives

dV_t=sigma_t d beta_t, sigma_t=exp(lambda t) integral phi(x)u(t,x)^(5/4)dx.

All statements may first be stopped at the scalar comparison levels from Turn2. Jensen under the probability measure phi(x)dx gives

sigma_t ≥ exp(-lambda t/4)V_t^(5/4).

Also sigma_t/V_t ≤ ||u(t)||_infinity^(1/4) whenever V_t>0. The right side is pathwise bounded on every compact time interval by the scalar comparison process. If X_t=0, nonnegativity and the positivity of phi imply u(t,.)=0 and sigma_t=0. Defining the ratio as zero there, the corresponding linear stochastic equation shows V_t=V_0 times a stochastic exponential. Hence V is strictly positive and finite at every finite time, and its minimum over a fixed compact interval is positive almost surely. No expectation of that minimum's inverse is needed.

Let a_t=sigma_t/V_t^(5/4)>0. It is locally bounded pathwise, and a_t≥exp(-lambda t/4). Define the strictly increasing clock A_t=integral_0^t a_s² ds. Standard Brownian time change applied to integral a_s d beta_s gives a Brownian motion W in the time-changed filtration, and

V_t=Y_(A_t), where dY_s=Y_s^(5/4)dW_s and Y_0=V_0.

The construction can be extended by an independent Brownian motion beyond the clock's lifetime if that lifetime is finite. For every fixed T, A_T is a finite stopping time in the time-changed filtration, and

A_T≥c_T:=integral_0^T exp(-lambda s/2)ds=2(1-exp(-lambda T/2))/lambda>0.

The scalar process Y is a nonnegative local martingale and therefore a supermartingale. Optional sampling, first with bounded stopping times and then Fatou, implies

E V_T=E Y_(A_T) ≤ E Y_(c_T).

This comparison does not assume that the random clock is independent of Y. Its stopping-time property and the deterministic lower bound are the relevant facts.

## 2. Exact loss of the scalar first moment

For Y_0=v>0, let r=4v^(-1/4). Turn2 gives Y_t=4^4 R_t^(-4), where R_t has the law of |z+B_t| in six dimensions with |z|=r. Using s^(-2)=integral_0^infinity q exp(-qs)dq and nonnegative Tonelli,

E R_t^(-4) = integral_0^infinity q(1+2tq)^(-3) exp(-q r²/(1+2tq))dq.

The substitution h=q/(1+2tq) reduces this exactly to integral_0^(1/(2t)) h exp(-r²h)dh. Thus

E Y_t = v[1-(1+b)exp(-b)], b=r²/(2t)=8/(t sqrt(v)).

For every t>0 this is strictly less than v, since (1+b)exp(-b)>0. In particular the CEV process is a strict local martingale. No inaccurate second-moment argument is used to obtain this first-moment loss.

Combining with Section1, and writing v=X_0 and b_T=8/(c_T sqrt(v)), gives the positive explicit lower bound

exp(-lambda T)X_0 - E X_T ≥ delta_T
:=exp(-lambda T)v(1+b_T)exp(-b_T)>0.

## 3. Numerical weighted mass has exactly the heat-equation mean

The scheme's first-moment identity from Turn1 and self-adjointness of the Dirichlet heat semigroup give, for every uniform partition tau=T/M,

E[integral phi U_M]=exp(-lambda T) integral phi u0.

Therefore the weak error for the linear observable L(w)=integral phi w is finite but at least delta_T for every M. It does not tend to zero with tau. This strengthens the infinite unbounded-power expectation obstruction: here both compared expectations are finite and their difference is bounded away from zero.

For the natural coupling, E|L(U_M)-L(u(T))|≥delta_T. The same lower bound holds for every coupling of their scalar mass distributions. Their Wasserstein-1 distance is at least delta_T, because the identity function is1-Lipschitz and both marginals have finite first moments. Also

E||U_M-u(T)||_(L1(D)) ≥ delta_T/||phi||_infinity.

Thus the full field does not converge strongly in expected L1 norm either. This conclusion is about the unmodified scheme and the specified superlinear power, not a tamed or stopped alternative.

## 4. Bounded-test boundary

The source's cited finite-dimensional weak theorem uses bounded C4 test functions. L is unbounded, so this result must not be advertised as excluding convergence of every bounded test. A sequence of nonnegative variables may converge in probability to a strict local-martingale limit while failing uniform integrability, retaining excess expectations in very rare large values. The remaining question is whether, under an explicit bounded-test class and appropriate coefficient assumptions, a weak rate can still be proved. Nothing above supplies or refutes such a rate.

## 5. Checks

`verify_turn3.py` checks exact Laplace-substitution algebra, dimension/exponent consistency, and strict positivity bounds. The analytic time-change and stopping-time arguments are separate and should receive adversarial review; a finite numerical test cannot certify them.
