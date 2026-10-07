# Real-variable approaches to the Nyman criterion

Problem 30002495 / OWR-12866-002. **Status: unresolved.** This is a report of five approaches to a methodological equivalence, with proved partial statements and explicit missing implications. It does not prove the Riemann hypothesis, its negation, or a new proof of the complete criterion. No novelty is asserted. All arguments below are authored exposition rather than source transcription.

## 0. Exact target and conventions

Let
\[
H_p=L^p((0,\infty),dt/t^2),\quad e_a(t)=\{t/a\},\quad
\chi(t)=\mathbf1_{[1,\infty)}(t),\quad
B_p=\overline{\operatorname{span}_{\mathbb R}\{e_a:a\ge1\}}^{H_p}.
\]
The span consists of finite sums. The question asks for a real-variable proof of the equivalence between

(P) for every epsilon > 0, pi(x) = li(x) + O_epsilon(x^(1/2+epsilon));

(N) chi belongs to B_2.

The primary report prints a >= 1 and chi = 1_[1,infinity). Replacing chi(1) makes no difference in H_p. Replacing a >= 1 by a > 1 also makes no difference: for a in a compact positive interval, |e_a(t)| <= min(t/a_0,1); its p-th power is integrable against dt/t^2 for p>1. Dominated convergence outside a countable breakpoint set proves H_p-continuity in a. In particular e_1 is the norm limit of e_(1+1/n). This elementary background is not a new research result or a counted approach.

Real coefficients suffice even if complex coefficients were intended: the real part of an approximant has no greater error against the real target. There is no coefficient-sum constraint in the half-line formulation. One can impose sum c_a/a=0 without changing target membership: below 1 a finite sum f is t C(f), where C(f)=sum c_a/a and |C(f)| <= ||f-chi||_(H_2). Thus f-C(f)e_1 has zero sum and error at most (1+||e_1||) ||f-chi||. In reciprocal coordinates x=1/t, this is the usual constrained formulation supported in (0,1).

The source calls the question methodological, without prescribing an axiomatized meaning of “real variable.” Our working goal allows real integration, elementary divisor identities, Hilbert-space methods and real-variable operator inequalities. Simply citing (P) iff RH iff (N), or importing a complex-analytic zero-location theorem into the missing step, does not answer that goal. This is an explicit interpretation, not a newly discovered restriction in the source.

## 1. Prime-counting error versus von Mangoldt error

Define theta(x)=sum_(p<=x) log p, Lambda(p^k)=log p and Lambda(n)=0 otherwise, and psi(x)=sum_(n<=x) Lambda(n). Let Li_2(x)=integral_2^x dt/log t for x>=2. The usual li differs by a fixed constant, which is immaterial here.

**Proposition 1.** The following three families of bounds are equivalent by real-variable arguments:
\[
\pi(x)-\operatorname{Li}_2(x)=O_\epsilon(x^{1/2+\epsilon}),\qquad
\theta(x)-x=O_\epsilon(x^{1/2+\epsilon}),\qquad
\psi(x)-x=O_\epsilon(x^{1/2+\epsilon})
\]
for every epsilon > 0.

**Proof.** Summation by parts gives
\[
\theta(x)=\pi(x)\log x-\int_2^x\frac{\pi(t)}t\,dt.
\]
Replacing pi by Li_2 produces x-2. If its error is O(x^(1/2+eta)), the displayed identity has error O(x^(1/2+eta) log x); choosing 0<eta<epsilon absorbs the logarithm. Conversely,
\[
\pi(x)=\frac{\theta(x)}{\log x}
       +\int_2^x\frac{\theta(t)}{t\log^2t}\,dt.
\]
The contribution of theta(t)=t is Li_2(x)+2/log 2. For any fixed exponent beta>0, the contribution of O(t^beta) is O(x^beta): bound log denominators below by log 2 and integrate t^(beta-1). This proves the first equivalence with the requisite epsilon choices.

Finally,
\[
0\le\psi(x)-\theta(x)=\sum_{2\le k\le\log_2x}\theta(x^{1/k})
\le\lfloor\log_2x\rfloor\sqrt{x}\log x.
\]
Here theta(y)<=y log y is sufficient; terms with x^(1/k)<2 vanish. This O(sqrt(x) log^2 x) error is absorbed by every positive epsilon. ∎

There is a useful exact smoothed consequence. Put E(t)=psi(t)-t. If phi is C^1 and compactly supported in (1,2), Stieltjes integration by parts gives
\[
\sum_n\Lambda(n)\phi(n/x)-x\int_1^2\phi(u)\,du
=-\int_1^2 E(xu)\phi'(u)\,du.
\]
Under (P), its modulus is at most
C_epsilon x^(1/2+epsilon) integral_1^2 u^(1/2+epsilon)|phi'(u)| du.

**Outcome and gap.** This removes pi and the logarithmic integral from the target using only elementary estimates. It does not connect the resulting signed prime-power error to the fractional-part closure. The uniformity above is only for a fixed test function with its displayed derivative norm; it cannot silently be used for sharp cutoffs whose derivative norms grow.

## 2. Attempted real-variable inversion from primes to Möbius cancellation

Let mu be the Möbius function, M(x)=sum_(n<=x) mu(n), and M(x)=0 for x<1.

**Proposition 2.** For every x>=1,
\[
M(x)\log x
=\int_1^x\frac{M(t)}t\,dt
 -x\int_1^x\frac{M(t)}{t^2}\,dt
 -\sum_{n\le x}\mu(n)R(x/n),                 \tag{2.1}
\]
where R(y)=psi(y)-(y-1), y>=1.

**Proof.** The divisor identity
\[
\mu(n)\log n=-\sum_{d\mid n}\Lambda(d)\mu(n/d)             \tag{2.2}
\]
follows by applying the logarithmic derivation D a(n)=a(n)log n to mu*1=delta. Indeed D(a*b)=(Da)*b+a*(Db); convolving the resulting equality with mu and using 1*Lambda=log gives Dmu=-mu*Lambda. The identity 1*Lambda=log follows immediately by prime factorization. All these identities are finite divisor sums.

Sum (2.2) through x and apply ordinary partial summation:
\[
M(x)\log x-\int_1^xM(t)\frac{dt}{t}
=-\sum_{n\le x}\mu(n)\psi(x/n).
\]
Split psi(y)=(y-1)+R(y). The elementary identity
\[
\sum_{n\le x}\mu(n)(x/n-1)
=x\int_1^x M(t)\frac{dt}{t^2}
\]
follows by interchanging a finite sum and an integral, since x integral_n^x t^(-2)dt=x/n-1. Substitution proves (2.1), including integer endpoints. ∎

For a fixed beta in (1/2,1), (P) yields |R(y)|<=C_beta y^beta for all y>=1 after adjusting a constant. The absolute-value estimate on the last term is only
\[
\left|\sum_{n\le x}\mu(n)R(x/n)\right|
\le C_\beta x^\beta\sum_{n\le x}n^{-\beta}
\le C_\beta\left(x^\beta+\frac{x}{1-\beta}\right).       \tag{2.3}
\]
The power loss from x^beta to x is explicit. Equation (2.1) still contains signed terms and might admit a better analysis, but (2.3) alone cannot yield a square-root-scale estimate for M. No claim is made that every real-variable inversion is impossible. The missing ingredient is a cancellation estimate in this very signed convolution, or another inversion argument that avoids this loss.

## 3. A real convolution route and the endpoint it does not reach

The implication in this section is classical in substance: it is the Möbius-integral method of Báez-Duarte, Theorem 3.1(a) in [BD00], expressed in the present weighted coordinates. The complete argument is included to expose precisely which norm is needed. We neither claim a new criterion nor promote its subcritical conclusion to the endpoint.

**Proposition 3.** For 1<p<infinity, if
\[
\int_1^\infty |M(u)|^p\frac{du}{u^2}<\infty,                \tag{3.1}
\]
then chi belongs to B_p. The argument uses no analytic continuation or complex zeros.

**Proof: bounded operator.** On H_p define
\[
(Sf)(t)=\int_0^\infty f(u)\{t/u\}\frac{du}{u}.
\]
To establish its bounded extension, set (W_p f)(v)=exp(-v/p) f(exp v). The substitution t=exp v gives ||W_p f||_(L^p(R))=||f||_(H_p). Direct change of variables gives
\[
W_p Sf=k_p*(W_p f),\qquad
k_p(v)=e^{-v/p}\{e^v\}.
\]
For v<0, k_p(v)=exp((1-1/p)v); for v>=0, |k_p(v)|<=exp(-v/p). Hence
\[
\|k_p\|_1\le\frac p{p-1}+p.
\]
Minkowski's integral inequality, or its proof by integrating translated L^p norms, gives
\[
\|Sf\|_{H_p}\le(p+q)\|f\|_{H_p},\qquad q=p/(p-1).       \tag{3.2}
\]
Initially this calculation can be made for bounded functions supported in a compact subinterval of (0,infinity), and then extended by density. For the specific M in (3.1), the integral also converges absolutely at every t: on [1,max(1,t)] use local boundedness, and on [max(1,t),infinity) use {t/u}=t/u and integral |M(u)|u^(-2)du<infinity. This last fact follows from Hölder in the finite measure du/u^2 on [1,infinity). Truncation identifies this pointwise integral with the H_p extension almost everywhere.

**Proof: exact arithmetic identity.** Write
\[
I=\int_1^\infty M(u)\frac{du}{u^2}.
\]
For a real number s>1, absolutely convergent Dirichlet multiplication and the elementary divisor identity sum_(d|n) mu(d)=1_(n=1) give
\[
\left(\sum_{n\ge1}n^{-s}\right)
\left(\sum_{n\ge1}\mu(n)n^{-s}\right)=1.
\]
The first real sum tends to infinity as s decreases to 1: each finite harmonic partial sum is its lower limit. Meanwhile ordinary summation by parts gives
\[
\sum_{n\ge1}\mu(n)n^{-s}
=s\int_1^\infty M(u)u^{-s-1}\,du.
\]
For 1<s<=2, the integrand is dominated by 2|M(u)|/u^2. Dominated convergence therefore shows I=0. This uses only real absolutely convergent series at s>1, not a complex zero-free result.

For v>=1, finite divisor inversion gives sum_(n<=v) M(v/n)=1. Integrating with dv/v from 1 to t, and substituting v=nu term by term, proves
\[
\log t=\int_1^t M(u)\lfloor t/u\rfloor\frac{du}{u}\quad(t\ge1).
\]
The floor is zero for u>t. Consequently
\[
SM(t)=tI-\log t=-\log t\quad(t\ge1),\qquad
SM(t)=tI=0\quad(0<t<1).                                  \tag{3.3}
\]
Call this function L(t)=-chi(t)log t.

**Proof: closure and target.** The truncations M_R=M 1_[1,R] tend to M in H_p, so SM_R tends to L by (3.2). On [1,R] the H_p-valued function u -> e_u is continuous. Partition this compact interval into subintervals and in each replace e_u by the value at one sample point; the approximation error is bounded by its uniform continuity modulus times integral_1^R |M(u)|du/u. Thus SM_R is in B_p, and therefore L is in B_p.

For a>1 let D_a f(t)=f(t/a). Then ||D_a f||_(H_p)=a^(-1/p)||f||_(H_p) and D_a e_u=e_(au), so D_a B_p is contained in B_p. The function
\[
h_a=\frac{D_aL-L}{\log a}
\]
is zero below 1, is log t/log a on [1,a), and is one on [a,infinity). It belongs to B_p and tends to chi in H_p as a decreases to 1, by domination by chi. Hence chi belongs to B_p. ∎

**Subcritical corollary, with an explicit additional assumption.** Suppose, separately from (P), that for every eta>0 one has |M(x)|<=C_eta x^(1/2+eta). For any 1<p<2 choose eta>0 so that p(1/2+eta)<1. Then (3.1) follows by direct integration and hence chi belongs to B_p. At p=2 this calculation gives no finite bound: the proposed majorant has integral integral_1^infinity u^(-1+2eta)du, which diverges. Divergence of an upper-bound integral does not prove divergence of the actual Möbius integral; it only invalidates this inference.

Nor does convergence for every p<2 imply H_2 convergence. An exact escaping-mass control is
\[
v_N(t)=\sqrt N\,\mathbf1_{[N,2N]}(t),\qquad
\|v_N\|_{H_p}^p=\tfrac12 N^{p/2-1}.
\]
It tends to zero in each H_p with p<2 and on every fixed compact set, while ||v_N||_(H_2)^2=1/2 for all N. This is a logical norm-limit control, not a claim that v_N is a Möbius approximant.

**Important endpoint qualification.** [BD00], Proposition 2.2 and Remark 2.4, records that the actual Möbius function has infinite H_2 norm, using the known existence of critical-line zeta zeros. This is credited literature background, not a real-variable result proved here or an input to our propositions. Thus imposing M in H_2 is not a viable hypothesis for the actual Möbius function, even if RH holds. The conditional endpoint theorem is a diagnostic of the failure of this route, not a proposed route to proving RH.

**Outcome and gaps.** We have a full real-variable conditional implication from M in H_2 to (N), and subcritical implications from an explicitly assumed family of Möbius bounds. We have not derived those bounds from (P) by a real-variable proof, and even importing them would leave the H_2 endpoint unproved by this route. The source [BD00] itself distinguishes its elementary forward implication from its converse using the usual zeta argument; its title is not evidence of a solution of the later methodological question.

## 4. Real annihilators, infinite tails, and the one-sided orbit

Put W=W_2, g(v)=exp(-v/2){exp v}, and h(v)=exp(-v/2)1_[0,infinity)(v). Then W is an isometry from H_2 onto L^2(R), Wchi=h, and
\[
We_a(v)=a^{-1/2}g(v-\log a).
\]
Writing tau_s g(v)=g(v-s), we obtain the exact reformulation
\[
\text{(N)}\quad\Longleftrightarrow\quad
h\in\overline{\operatorname{span}\{\tau_sg:s\ge0\}}^{L^2(\mathbb R)}. \tag{4.1}
\]
The scalar a^(-1/2) is nonzero and does not change the span. Real orthogonal projection gives the exact dual formulation: whenever v in L^2(R) satisfies integral_R v(u)g(u-s)du=0 for every s>=0, it must satisfy integral_0^infinity v(u)exp(-u/2)du=0. All these integrals converge by Cauchy–Schwarz. Thus a real-variable proof could proceed by excluding a separating annihilator using (P), without explicitly constructing approximants. Such an exclusion has not been achieved here.

**Proposition 4.1 (no separating annihilator bounded above in t).** Suppose f in H_2 vanishes almost everywhere for t>R, for some finite R, and is orthogonal to e_a for every a>=1. Then f=0 almost everywhere on (1,infinity), so <f,chi>=0.

**Proof.** The scalar C=integral_0^R f(t)dt/t is well-defined by Cauchy–Schwarz, since its second factor is sqrt(R). For a>max(R,1), e_a(t)=t/a on the support of f, so C=0. For a>=1 expand the floor in e_a=t/a-floor(t/a):
\[
0=\langle f,e_a\rangle
=-\sum_{1\le n\le R/a}\int_{an}^R f(t)\frac{dt}{t^2}.    \tag{4.2}
\]
The sum is finite. If R>1 and a in (max(1,R/2),R), only n=1 can contribute. The absolutely continuous tail integral in (4.2) is zero there, so f vanishes almost everywhere on that interval, and hence above max(1,R/2). Repeat with R replaced by R/2 while this number exceeds 1. After finitely many repetitions, f vanishes above 1. The claimed pairing is then zero. Conversely, any f supported below 1 with integral_0^1 f(t)dt/t=0 is an annihilator and has zero target pairing. ∎

This result concerns the full parameter half-line, not a finite cutoff. It shows that a nonmembership witness for (N), if one exists, must have an unbounded upper tail. Truncating a hypothetical annihilator does not preserve its infinitely many orthogonality conditions.

**Proposition 4.2 (bilateral density does not supply unilateral density).** There is a completely explicit real kernel k in L^1(R) intersect L^2(R) whose full translation orbit is dense in L^2(R), while the closed span of its nonnegative translates does not contain h.

**Proof.** Take
\[
k(u)=\bigl(e^{-u}-\tfrac32e^{-2u}\bigr)\mathbf1_{[0,\infty)}(u),
\qquad v(u)=e^{-u}\mathbf1_{[0,\infty)}(u).
\]
For s>=0 direct integration gives
\[
\langle v,\tau_s k\rangle
=e^{-s}(\tfrac12-\tfrac32\cdot\tfrac13)=0,
\qquad \langle v,h\rangle=\tfrac23\ne0.
\]
Thus v separates h from the nonnegative translation span. For instance the negative translate s=-log 2 has <v,tau_s k>=1/8, so this annihilator does not extend to the full group.

To prove full-group density without a Fourier theorem, let w in L^2(R) annihilate every translate of k. Set
\[
F_j(s)=\int_s^\infty w(u)e^{-j(u-s)}\,du\quad(j=1,2).
\]
Cauchy–Schwarz proves existence, and the L^1 exponential-kernel bound gives F_j in L^2(R). The functions are locally absolutely continuous and satisfy F_j'=jF_j-w almost everywhere: differentiate e^(js) integral_s^infinity w(u)e^(-ju)du on any finite interval. The annihilation equation is F_1=(3/2)F_2. Differentiate it and use the two derivative identities to get w=3F_2. Hence F_2'=-F_2. Local absolute continuity yields F_2(s)=C exp(-s) on R; its L^2 membership forces C=0, then w=0. The orthogonal complement of the full translation span is zero, proving density. ∎

**Outcome and gap.** The actual Nyman problem is a one-sided translation problem. A bilateral real-variable density theorem does not settle it, as Proposition 4.2 demonstrates with a real kernel. Proposition 4.1 eliminates only finite-tail separators for the actual kernel. No control of the infinite-tail annihilators is derived from the prime error in (P). The counterexample kernel is not the Nyman kernel and is not a counterexample to the known Nyman criterion.

## 5. Damped Möbius approximants and a boundedness criterion

For epsilon>0 and integer N>=1 define the finite, admissible approximant
\[
f_{\epsilon,N}(t)=-\sum_{n=1}^N\mu(n)n^{-\epsilon}e_n(t),\qquad
A_{\epsilon,N}=\sum_{n=1}^N\mu(n)n^{-1-\epsilon}.
\]
These are the sign-changed reciprocal-coordinate finite approximants of [BD03], Section 2.2; damping is classical. The following elementary derivation separates a provable local limit from the missing global norm estimate.

**Proposition 5.1 (unconditional local approximation).** If epsilon_j decreases to zero, N_j tends to infinity, and N_j^(-epsilon_j)/epsilon_j tends to zero, then f_(epsilon_j,N_j) tends to chi in H_2 restricted to (0,R] for every finite R.

**Proof.** Real, absolutely convergent Dirichlet multiplication gives
\[
A_\epsilon:=\sum_{n\ge1}\mu(n)n^{-1-\epsilon}
=\left(\sum_{n\ge1}n^{-1-\epsilon}\right)^{-1}.
\]
Integral comparison implies 0<A_epsilon<=epsilon. Absolute summation of the tail gives
\[
|A_{\epsilon,N}|\le\epsilon+\frac{N^{-\epsilon}}\epsilon.  \tag{5.1}
\]
For N>=R>=1 and 0<t<=R, expand each fractional part:
\[
f_{\epsilon,N}(t)
=\sum_{n\le t}\mu(n)n^{-\epsilon}\lfloor t/n\rfloor
 -tA_{\epsilon,N}.                                      \tag{5.2}
\]
The exact identity sum_(n<=t) mu(n) floor(t/n)=chi(t) follows from finite divisor inversion. Since 0<=1-n^(-epsilon)<=epsilon log n, (5.2) implies on [1,R]
\[
|f_{\epsilon,N}(t)-\chi(t)|
\le\epsilon R\sum_{n\le R}\frac{\log n}{n}
    +R|A_{\epsilon,N}|.
\]
Below 1 the error is precisely -t A_(epsilon,N). Its H_2 norm on (0,1) is |A_(epsilon,N)|, while the dt/t^2 measure of [1,R] is at most one. The triangle inequality therefore yields the explicit local estimate
\[
\|f_{\epsilon,N}-\chi\|_{H_2(0,R)}
\le\epsilon R\sum_{n\le R}\frac{\log n}{n}
 +(R+1)\left(\epsilon+\frac{N^{-\epsilon}}\epsilon\right). \tag{5.3}
\]
The hypotheses make the right side tend to zero. Smaller R follow by restriction. ∎

For example, epsilon_j=1/j and N_j=ceil(exp(j^2)), j>=3, meet the conditions, with |A_(epsilon_j,N_j)|<=1/j+j exp(-j). This is an existence construction; no computation through those enormous cutoffs is claimed.

**Proposition 5.2 (uniform boundedness would suffice).** Let f_j be finite linear combinations of the e_a, a>=1, tending to chi in H_2(0,R) for every R. If sup_j ||f_j||_(H_2)<infinity, then (N) holds. A uniformly bounded subsequence has the same consequence.

**Proof.** Let C bound the norms. For any w in H_2 and any R>=1,
\[
|\langle f_j-\chi,w\rangle|
\le\|f_j-\chi\|_{H_2(0,R)}\|w\|_{H_2}
 +(C+1)\|w\mathbf1_{(R,\infty)}\|_{H_2}.
\]
Take j to infinity, then R to infinity. Thus f_j converges weakly to chi. Every w orthogonal to the closed subspace B_2 is orthogonal to chi by passage to this weak limit. The elementary identity (B_2^perp)^perp=B_2 proves chi in B_2.

For an explicit norm-convergent existence argument, write x_j=f_j-chi. Choose a subsequence recursively such that, for m>i, |<x_(j_m),x_(j_i)>|<=1/m; weak convergence permits each finite collection of inequalities. Then
\[
\left\|\frac1m\sum_{i=1}^m x_{j_i}\right\|^2
\le\frac{(C+1)^2}{m}+\frac{2}{m^2}\sum_{r=2}^m\frac{r-1}{r}
\le\frac{(C+1)^2+2}{m}.
\]
The corresponding arithmetic means of f_(j_i) are still finite admissible sums and converge in H_2 to chi. No effective rule for locating this subsequence is claimed. ∎

**Attempted estimate and remaining gap.** Scaling gives ||e_n||_(H_2)=n^(-1/2)||e_1||_(H_2), and ||e_1||_(H_2)<=sqrt(2) by splitting at 1. The unconditional triangle inequality supplies only
\[
\|f_{\epsilon,N}\|_{H_2}
\le\sqrt2\sum_{n\le N}n^{-1/2-\epsilon}
\le\sqrt2\left(1+\frac{N^{1/2-\epsilon}-1}{1/2-\epsilon}\right)
\quad(0<\epsilon<1/2).                                  \tag{5.4}
\]
For the above diagonal this is far from a uniform bound. Proposition 1 or (P) has not been shown to improve (5.4) to a bounded subsequence. The local convergence is unconditional and therefore cannot itself be treated as evidence of a proof of (N); its mass may escape to infinity. Proposition 5.2 shows precisely what additional global estimate would make this route work. It is only a sufficient condition for this particular family; necessity for (N) is not asserted.

## 6. Dependency and gap summary

All proved propositions use real integration, finite divisor algebra, elementary real convergent series, Hölder/Minkowski, or real Hilbert-space orthogonality. Proposition 3 restates a credited classical implication with a full proof; the other elementary reductions and controls carry no novelty claim. No RH assumption is silently used.

The five approaches leave the following dependencies unresolved:

1. Prime error (P) is equivalent to the stated psi-error family, but a real prime-error-to-closure bridge is absent.
2. The direct Möbius inversion loses the desired power in its absolute-value convolution bound.
3. The real integral norm estimate would need M in the endpoint H_2, but the literature shows this moment is infinite for the actual Möbius function. A hypothetical square-root-plus-epsilon estimate supplies only subcritical H_p conclusions by this argument.
4. Duality requires control of genuine infinite-tail, one-sided annihilators. Finite-tail elimination and bilateral density do not provide it.
5. Damped finite approximants have the right local limit, but the required global H_2 bounded subsequence is unproved.

No route here proves the reverse implication (N) => (P) by the required real-variable method either. Its usual proof through complex zero information is deliberately not relabeled as a real-variable proof. The methodological target therefore remains **unsolved after five approaches**. Finite controls validate finite identities and counterexample constants only; they cannot establish any of these infinite asymptotic gaps.

## References used

[OWR14] M. Balazard, “Nyman’s and Báez-Duarte’s criteria for the Riemann hypothesis: survey and open problems,” in *Dirichlet Series and Function Theory in Polydiscs*, Oberwolfach Reports 11 (2014), pp. 348–352; target Question 1, p. 350, following formulas on p. 349. https://ems.press/journals/owr/articles/12866 ; https://doi.org/10.4171/OWR/2014/06 .

[BD00] L. Báez-Duarte, *Arithmetical Aspects of Beurling’s Real Variable Reformulation of the Riemann Hypothesis*, arXiv:math/0011254v1 (2000), especially Section 3 and the endpoint qualifications. https://arxiv.org/abs/math/0011254v1 .

[BD03] L. Báez-Duarte, “A strengthening of the Nyman–Beurling criterion for the Riemann hypothesis,” Rend. Lincei Mat. Appl. 14 (2003), 5–11; author preprint arXiv:math/0202141v2. https://arxiv.org/abs/math/0202141v2 ; https://www.bdim.eu/item?id=RLIN_2003_9_14_1_5_0 . The integer-parameter strengthening is credited background, not used to infer a real-variable proof of (P) iff (N).
