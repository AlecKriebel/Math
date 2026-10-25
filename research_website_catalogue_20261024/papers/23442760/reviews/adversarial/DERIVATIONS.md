# Independent complete mathematical derivations

These are deductions for the literal original statements. They do not rely on supplied verification programs, prior reviewing opinions or finite numerical grids. The notation follows the actual manuscript so each inequality can be checked against the original.

## 1. The quadratic proxy covers every permitted minimizer

Let K be compact, convex and have nonempty interior in R^n, n>=1. Its Lebesgue volume V is finite and strictly positive. A real polynomial f attains its minimum at a. For each x in K, the scalar function s -> f(a+s(x-a)) has a minimum at the permitted endpoint s=0 of [0,1]. Its right derivative is nonnegative. Therefore ell(x)=gradient f(a).(x-a)>=0 for every x in K, including boundary minimizers and nonconvex objectives.

Taylor's formula with integral remainder along that segment gives

`f(x)-f(a) = ell(x) + integral_0^1 (1-s) (x-a)^T Hessian f(a+s(x-a)) (x-a) ds`.

The whole segment is in K. The absolute value of its quadratic form is at most H||x-a||^2, where H=max_K||Hessian f||_op. Hence

`0 <= f(x)-f(a) <= ell(x)+(H/2)||x-a||^2 <= g(x)`.

The added coefficient gamma=1+H/2 is strictly positive. Since ell>=0, g(x)>0 for x!=a in K and g(a)=0. Full dimension gives some x!=a, so continuity and compactness give 0<G=max_K g<infinity. Thus u=g/G is a polynomial of total degree at most two, with 0<=u<=1 on K. These arguments do not assume f convex, a unique minimizer, or a smooth boundary. Also G<=B D+gamma D^2 by Cauchy-Schwarz, where D=diam(K) and B=max_K||gradient f||.

## 2. Relative sublevel mass requires no boundary or density regularity

Write S_t={x in K:u(x)<=t}, F(t)=vol_n(S_t), t>0. These sets are compact and measurable; F(t)=V for t>=1. For 0<s<=t put alpha=s/t. Convexity keeps T_alpha(x)=a+alpha(x-a) in K, and exact algebra gives

`g(T_alpha(x)) = alpha ell(x)+alpha^2 gamma||x-a||^2 <= alpha g(x)`.

Consequently T_alpha(S_t) is contained in S_s. This is an injective homothety with determinant alpha^n, so

`alpha^n F(t) <= F(s)`, equivalently `F(t) <= (t/s)^n F(s)`.

The same argument works for t>1; no saturation exception is needed. Taking t=1 gives F(h)>=h^n V>0 for 0<h<=1. The estimate applies at nonsmooth and nonsimple exposed points, because it uses volume under a homothety of the actual body rather than a local tangent-ball approximation. There is no assumption about differentiability or absolute continuity of the push-forward distribution F.

## 3. Universal kernel estimates

Let m>=1, N=2m+1, and A_m(t)=[1+2 sum_{j=1}^m T_j(1-2t)]/N. It is a real polynomial of degree m and A_m(0)=1. For 0<t<=1 let v=arcsin(sqrt(t)). The elementary geometric-sum identity

`sum_{j=-m}^m exp(2ijv) = sin((2m+1)v)/sin(v)`

and cos(2v)=1-2t give A_m(t)=sin(Nv)/(N sqrt(t)). This proves the identity for every m, rather than inferring it from the finite symbolic controls.

Since each T_j(1-2t) has absolute value at most one on [0,1], the triangle inequality gives |A_m|<=1 there. Since |sin(Nv)|<=1, the second estimate is |A_m(t)|<=1/(N sqrt(t)). Let h=N^-2. Convexity of arcsin makes its graph lie below the endpoint chord, so arcsin(z)<=pi z/2 on [0,1]. Also arcsin(z)>=z, for example by its derivative >=1. If 0<t<=h then 0<Nv<=pi/2, and

`A_m(t) >= (2 Nv/pi)/(N sqrt(t)) >= 2/pi`.

At zero the same core bound follows from the polynomial value one. Oscillatory signs and zeros away from the core are allowed; they are never used for the lower normalizer.

## 4. The common mass cancels before summation

Let L=n+2 and Q_m(x)=A_m(u(x))^(2L). This is the global square of A_m(u)^L, including off K. On K,

`0<=Q_m<=min(1,(h/u)^L)` for u>0,

and the normalizer Z_m=integral_K Q_m is at least `(2/pi)^(2L) F(h)>0`.

The core u<=h contributes at most hF(h) to integral_K uQ_m. The disjoint sets E_j={2^j h<u<=2^(j+1)h}, j>=0, cover its complement; equality endpoints belong only to the lower shell. For each j,

`integral_Ej uQ_m <= (2^(j+1)h) 2^(-jL) F(2^(j+1)h)`

`<= h F(h) 2^(n+1) 2^(j(n+1-L))`.

Here the relative volume estimate compares the shell to *the same F(h)* used in the denominator. With L=n+2 the exponent is -j, whose infinite geometric series sums to two. Only finitely many actual shells meet K, because u<=1, so extending their nonnegative majorants to an infinite sum is permitted. It follows that

`integral_K uQ_m <= h F(h) (1+2^(n+2))`.

Dividing by Z_m cancels F(h), giving

`(integral_K uQ_m)/Z_m <= (pi/2)^(2L) (1+2^(n+2))/(2m+1)^2`.

There is no lost body-dependent core constant, absolute lower-volume substitution, logarithmic cutoff, or assumed sign cancellation of tails. Taking L=n+1 would give a divergent constant majorant, so the strict exponent margin in the actual manuscript is necessary for this particular argument.

## 5. Global square, all integer orders and explicit C_n

For r>=2L take m=floor(r/(2L)). Since deg(u)<=2, the global square root A_m(u)^L has total degree at most 2mL<=r, and Q_m has degree at most 4mL<=2r. Thus

`q_r = Q_m/Z_m = [A_m(u)^L/sqrt(Z_m)]^2`

is a genuine global SOS, not just nonnegative on K, and has unit Lebesgue mass on the entire original body. Multiplying the preceding ratio bound by G bounds integral_K(f-f_*)q_r. For x=r/(2L)>=1 and m=floor(x), one has x<m+1<=2m+1. Therefore `(2m+1)^-2 <= 4L^2/r^2`, giving exactly

`0 <= H_r(f,K)-f_* <= C_n G/r^2`,

`C_n=4L^2 (pi/2)^(2L)(1+2^(n+2))`.

For integers 1<=r<2L use q_r=1/V, itself the square of the real constant 1/sqrt(V). Its error is at most G. Since C_n>4L^2>r^2, it also meets the same displayed inequality. These two ranges exhaust every requested integer r; r=0 is correctly excluded. No f-degree factor is missing because the composed polynomial is the quadratic proxy, not f itself.

Finally, the definition of Sigma_r agrees with global SOS polynomials of degree at most 2r. If a finite SOS representation had maximal summand degree d>r, its highest homogeneous part would be a sum of squares of nonzero degree-d homogeneous polynomials. It cannot vanish identically over the reals, as evaluation at every real point would force each summand polynomial to vanish identically. Hence the sum would have degree 2d>2r, a contradiction.

## 6. Universal interval and product lower bound

Rodrigues' formula gives orthogonality of P_j to every lower degree polynomial by j integrations by parts. Its leading coefficient is c_j=(2j)!/[2^j(j!)^2]. The same integrations give

`integral_-1^1 P_j(x)^2 dx = (c_j/2^j) integral_-1^1 (1-x^2)^j dx = 2/(2j+1)`,

using the elementary beta integral `integral_-1^1(1-x^2)^j dx = 2^(2j+1)(j!)^2/(2j+1)!`.

Expanding the finite-polynomial Laplace identity in the manuscript gives `P_j(x)=pi^-1 integral_0^pi[x+i sqrt(1-x^2) cos(theta)]^j dtheta`. For -1<=x<=1 its base has modulus squared `x^2+(1-x^2)cos(theta)^2<=1`, so |P_j(x)|<=1. These identities apply for every degree; finite exact Gram checks are only diagnostics.

Consequently ell_j(t)=sqrt(2j+1)P_j(2t-1), 0<=j<=r, is an orthonormal basis on [0,1]. Expanding p in this basis and applying Cauchy-Schwarz yields

`|p(t)|^2 <= [sum_j ell_j(t)^2] integral_0^1 p(s)^2 ds <= (r+1)^2 integral_0^1 p(s)^2 ds`.

For a feasible finite SOS q=sum_k p_k^2, every p_k has degree<=r. Summation gives 0<=q(t)<=(r+1)^2=:M because total mass is one. For alpha=1/(2M), integral_0^alpha q<=M alpha=1/2. Hence integral_0^1 tq(t)dt >= alpha integral_alpha^1 q>=1/(4M), and taking the infimum proves the proposition.

On the product body, fix y and apply that polynomial bound in t to each p_k(t,y), sum, and integrate in y. The marginal rho(t)=integral q(t,y)dy obeys rho(t)<=M integral_0^1 integral q(s,y)dy ds=M and integral rho=1. Compactness/continuity justify Fubini; no transverse-volume factor appears. The same lower argument applies in every n, including n=1. Combined with T1 on the fixed product body and f=t, this is Theta(r^-2) for one instance per dimension. It is not a lower bound for each objective: constant objectives have identically zero error.

## 7. C2 scope and exact controls outside the assumptions

The foregoing upper proof uses only a minimizer, gradient, bounded Hessian on the actual segments, and a polynomial quadratic proxy. For f of class C2 on an open neighborhood of compact K, these ingredients are still available, and the density remains polynomial. Thus the manuscript's stated C2 extension is valid.

The measure cannot simply be arbitrary: on K=[0,1], f=t and reference measure delta_1, unit mass requires q(1)=1, so every feasible density has objective one although f_*=0. Without unit mass, q=0 already gives objective zero for f=1+t with f_*=1. A body in a proper affine subspace has zero n-dimensional Lebesgue mass, so no density can normalize in the literal ambient problem. The polynomial 1-t^2 is nonnegative on [-1,1] but negative outside; such a merely local nonnegative density cannot be silently equated with the global-SOS cone. These are rejected extensions, not counterexamples to T1.

## 8. Independent check of the acknowledged older-ingredient deduction

This is a source-interface check of an explicit secondary claim, not a replacement for or repair of the main theorem. Totik–Varga Theorem2.1 allows psi(v)=sqrt(v): it is increasing, has psi(0+)=0, satisfies its doubling condition, and integral_1^infinity psi(v)/v^2 dv=integral_1^infinity v^(-3/2)dv=2. At endpoint parameter a=0, it supplies degree-m real polynomials P_m with P_m(0)=1, sup_[0,1]|P_m|<=2, and

`|P_m(t)| <= A exp(-c(m^2 t)^(1/4))`.

Markov's inequality on [0,1] gives sup|P_m'|<=2m^2 sup|P_m|<=4m^2. Therefore P_m(t)>=1/2 for 0<=t<=h=1/(8m^2). The denominator of P_m(u)^2 is >=F(h)/4; the core numerator is <=4hF(h). On the same dyadic shell E_j its numerator is bounded by

`h F(h) 2^(n+1) A^2 2^(j(n+1)) exp(-2c(2^j/8)^(1/4))`.

The infinite series of these constants converges: its successive ratio tends to zero, since 2^(j/4) dominates a linear j. Dividing again cancels the same F(h), producing O(m^-2). The square root P_m(u) has degree <=2m, so m=floor(r/2), plus the constant density for low orders, gives O(r^-2) in the target hierarchy. No theorem asserting global doubling of the whole push-forward measure is needed; the direct relative estimate in section2 is enough.

This verifies the manuscript's acknowledged deduction from older ingredients. It does not show that this combined convex-body theorem was explicitly printed in 2012 or settle priority, first disclosure or worldwide openness.
