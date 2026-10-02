# Turn 4: a quantitative Lipschitz localization estimate

Status: a uniform-in-time error estimate for globally Lipschitz cutoff equations, followed by convergence in probability for the superlinear scheme. It does not contradict the failure of all error moments above one. This is a new proof attempt, not an independent review.

Work on D=(0,1), H=L²(D), V=H_0¹(D), with norm ||v||_V²=||v||_H²+||v'||_H². E_t is the Dirichlet heat semigroup. Let g∈C¹(R), g(0)=0 and ||g'||_infinity≤L. Set f(v)=g(v)/v, continuously extended at zero, and h(v)=g'(v)-f(v), h(0)=0. Then |f|≤L and |h|≤2L. Take deterministic u0∈V. Constants below may depend on T and ||u0||_V, but not on the time step or on higher derivatives of g.

## 1. Interpolation and exact Gaussian derivative bounds

On t_m≤t≤t_(m+1), put s=t-t_m, v=U_m, Z=beta(t)-beta(t_m), and

N_s(v)=v exp(f(v)Z-s f(v)²/2), V_tau(t)=E_s N_s(v).

This continuous interpolation agrees with the scheme at grid points. Its mild differential is

dV_tau=Delta V_tau dt + sigma_tau(t) d beta(t),

where sigma_tau(t)=E_s[f(v)N_s(v)].

For v≠0, spatial chain rules use the scalar derivatives

N_s'(v)=exp(fZ-sf²/2)[1+h(Z-sf)],

J_s'(v)=exp(fZ-sf²/2)[g'(v)+f h(Z-sf)], J_s(v)=f(v)N_s(v).

The formulas extend continuously to v=0. Conditional on v, Gaussian integration gives

E[N_s'(v)²]=exp(sf²)[(1+s f h)²+s h²] ≤ exp(9L²s),

E[J_s'(v)²]=exp(sf²)[(g'+s f²h)²+s f²h²] ≤ L² exp(9L²s).

Indeed, with x=L²s, both brackets after factoring L² where appropriate are bounded by 1+8x+4x²≤exp(8x). Also E N_s(v)²≤v²exp(L²s), and E J_s(v)²≤L²v²exp(L²s). These bounds do not require a bound on f' itself near zero; the bounded combination vf'=h is used.

The Sobolev chain rule, conditional Tonelli, and heat contraction therefore imply

E||U_m||_V² ≤ exp(9L²t_m)||u0||_V²,

and E||sigma_tau(t)||_V²≤L²exp(9L²t)||u0||_V².

## 2. Maximal Sobolev bounds

The standard Hilbert-space energy estimate for dZ=Delta Z dt+B d beta, using dissipativity and BDG followed by Young's inequality, gives

E sup_(t≤T)||Z_t||_V² ≤ C[||Z_0||_V²+E integral_0^T||B_t||_V²dt].

It applies first to spectral approximations and then by the usual energy limit; the same estimate holds in H. Applying it to V_tau gives a bound by C(1+L²T)exp(9L²T)||u0||_V². For the exact globally Lipschitz equation, ||g(u)||_V≤L||u||_V, so the corresponding energy/BDG/Gronwall estimate gives

E sup_(t≤T)||u_t||_V² ≤ C exp(C L²T)||u0||_V².

Only the C¹ chain rule is needed. To justify V regularity without assuming that the Nemytskii map is globally Lipschitz on V, run the standard Picard construction in H. Each iterate is V-valued, and its V-energy obeys E||u^(j+1)_t||_V²≤||u0||_V²+L² integral_0^t E||u^j_s||_V²ds. Iteration gives a uniform exponential bound. The linear maximal estimate gives a uniform maximal V bound as well. Strong H convergence and weak Sobolev compactness put the H-limit in V; the chain rule gives g(u)∈L²(Omega×[0,T];V). Its linear stochastic convolution then has a V-continuous version and the displayed energy bounds. Spectral approximation justifies the intermediate Itô formulas. No g'' bound is used. The C⁰ versions used below follow from V embedding in dimension one; nonnegativity follows from the cutoff comparison argument, not from these norm estimates.

## 3. A local coefficient defect of size tau^(1/2)

Let R_tau=sigma_tau-g(V_tau). Insert and subtract g(v) and g(E_s v):

R_tau=E_s[f(v)(N_s-v)] +(E_s g(v)-g(v)) +(g(v)-g(E_s v)) +(g(E_s v)-g(E_s N_s)).

Use ||E_s w-w||_H²≤s||w'||_H² and

E[||N_s(v)-v||_H² | v]≤sL²exp(sL²)||v||_H².

The four terms yield

E||R_tau(t)||_H² ≤ C tau(L²+L⁴)exp(9L²T)||u0||_V².

This is an integrated stochastic coefficient estimate, not a pathwise Taylor expansion with uncontrolled remainders.

Let e=V_tau-u. It solves de=Delta e dt+[g(V_tau)-g(u)+R_tau]d beta, e(0)=0. H-energy, BDG and Gronwall give

E sup_(t≤T)||e_t||_H² ≤ C_T(1+L⁴)exp(C_T L²) tau.

The harmless1 permits L=0; its actual error is zero. Combining this with the maximal V bounds and the one-dimensional inequality ||w||_infinity²≤2||w||_H||w'||_H gives

E sup_(t≤T)||V_tau(t)-u(t)||_infinity²
≤ B(L) tau^(1/2), B(L)=C_T,u0(1+L⁴)exp(C_T,u0 L²).

Indeed Cauchy–Schwarz bounds the expectation of the product of the maximal H and V norms. The estimate is deliberately not called a half-order C⁰ strong bound: its root-mean-square C⁰ rate is1/4. The H root-mean-square rate is1/2.

## 4. Applying fixed cutoffs to the superlinear equation

For K≥max(1,2||u0||_infinity), take g_K(v)=v_+^(5/4) for v≤K and the tangent linear extension K^(5/4)+(5/4)K^(1/4)(v-K) for v>K. This is C¹, globally Lipschitz with L_K=(5/4)K^(1/4), and has g_K(0)=0. Let U^K and u^K be its numerical and exact solutions.

Let Y be the scalar comparison process from Turn2. Its nonnegative-supermartingale maximal inequality gives P(sup_(t≤T)Y_t>K/2)≤2||u0||_infinity/K. On the complement, u^K=u and ||u^K||_infinity≤K/2 throughout the interval. If also sup_t||V_tau^K-u^K||_infinity≤K/2, then U_m^K≤K at every grid point. Induction in m shows that U_m=U_m^K, since the original and cutoff coefficients agree at every input used by the scheme.

Thus for any epsilon>0,

P(max_m||U_m-u(t_m)||_infinity>epsilon)
≤2||u0||_infinity/K + B(L_K) tau^(1/2)/min(epsilon,K/2)².

For fixed K the second term tends to zero, and then K can tend to infinity. The original superlinear scheme therefore converges in probability, uniformly over grid times in C⁰(D). In particular expectations of fixed bounded continuous functionals of the final field converge. This qualitative result does not yet supply a rate uniform over a specified bounded-test class; that optimization is left to the final turn.

## 5. Scope

The C⁰ estimate and localization here use one spatial dimension. No higher-dimensional C⁰ rate is claimed. Convergence in probability is compatible with Turns2–3: the exceptional large-value events destroy uniform integrability and retain a nonvanishing excess first moment. `verify_turn4.py` checks the exact Gaussian derivative algebra and elementary bounds, not the Hilbert-space argument, which requires independent review.
