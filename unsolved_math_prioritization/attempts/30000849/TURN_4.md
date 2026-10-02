# Turn4: power input in the strict finite-cluster regime

**Unreviewed scoped theorem; full intended question remains unresolved.**
We now allow the primary source's exact input alpha t^omega. The result covers
zero initial data in the strict parameter region

    alpha>0, omega>-1/2, 0<p<1,
    beta=omega+1, d=beta(1-p)<1/2.                       (1)

The lower-p, critical and general initial-data questions remain open here.
The proof below supplies the nonlinear asymptotic through a finite bootstrap;
no regular-variation hypothesis is imposed on the unknown solution.

## 1. Precise theorem and time-origin convention

Use the standard source equation, with birth(j-1)^p, as in Turns2–3. Put
kappa=alpha/beta. There exists a global nonnegative solution with zero initial
data and total mass M(t)=kappa t^beta. For omega<0 the input itself is singular
at0; the solution means a continuous, locally absolutely continuous integral
solution at0, classical componentwise for t>0. For omega>=0 it is classical
also at0. No differentiability of alpha t^omega at0 is assumed.

For every such mass-conserving solution there is N_infinity in(0,infinity) with

    N_infinity=lim sum_(j>=2)c_j(t)=integral_0^infinity c_1(t)^2dt.

Writing tau=integral_0^t c_1 and sigma=[(1-p)tau]^(1/(1-p)), we have

    sigma(t) ~ (kappa/N_infinity)t^beta,
    c_1(t) ~ B t^(d-1),
    B=alpha^(1-p) beta^p N_infinity^(p-1).                (2)

In particular

    tau(t) ~ B t^d/d
           = (kappa/N_infinity)^(1-p)t^d/(1-p).          (3)

Define

    r=1/d-1>1,
    q=p+(1-p)r=2p-1+1/beta,
    A_*=N_infinity^(1/beta) kappa^(omega/beta)/alpha.     (4)

Then A_* sigma(t)^q c_j(t) has the off-front limit
eta^(-p)(1-eta^(1-p))^(-r) for0<eta<1 and0 for eta>1, along
j/sigma(t)->eta!=1. The mass measures normalized by kappa t^beta converge
weakly to the point mass at eta=1, exactly as in Turn3. No pointwise front
limit is claimed.

The input, model and clock are taken from the original contribution and
primary survey. The strict regime, exponent and constants above are deductions
of this author turn, not purported quotations from the unpublished source notes.

## 2. Existence, mass and elementary upper bounds

Finite truncation gives M_n'<=alpha t^omega, so M_n<=kappa t^beta. Since the
input is locally integrable, the finite ODEs are well-defined in integral form,
with nonnegative solutions. Away from0 they are ordinary smooth ODEs. For each
T the same weighted-tail estimate is bounded by
kappa T^beta(L+1)^(p-1). The finite second-moment bound becomes

    S_n'<=alpha t^omega+2kappa t^beta S_n.

Its integrating-factor bound is finite on[0,T]. The finite boundary flux is
O_T(n^(p-1)), so it vanishes and uniform mass tails pass to the limit. This
is the proof of Turns1/3 with the locally integrable source retained; it gives
M(t)=kappa t^beta, continuity at0, local absolute continuity and the specified
componentwise regularity. Equicontinuity at0 follows from integrating the
common locally integrable derivative bound, not from a bounded J at0.

The monomer inequality x'<=alpha t^omega-2x² gives, for t>=1,

    x(t)=c_1(t)<=C(1+t)^a0,    a0=max(omega/2,0).         (5)

For omega>=0 use a sufficiently large multiple of(1+t)^(omega/2) as a
supersolution; its derivative is nonnegative. For omega<0 the input is bounded
for t>=1 and comparison with a sufficiently large constant suffices. On[0,1]
the mass bound already controls x. Notice a0<beta.

## 3. Exact cohort facts and the clock bounds

Set nu=p/(1-p). The pure-birth representation from Turn3 remains valid:

    c_j(t(tau))=integral_0^tau f(u)P(Y_(tau-u)=j)du,
    f(tau)=c_1(t(tau)),
    N(tau)=sum_(j>=2)c_j(t(tau))=integral_0^tau f(u)du.   (6)

The process Y has rates k^p and starts at2. For all0<p<1 its expectation
bound is G(v)=[2^(1-p)+(1-p)v]^(1/(1-p)). One may first prove this bound
for the stopped process by concavity. Markov's inequality then bounds the
probability of reaching n in fixed time by G(v)/n, proving nonexplosion.
Thus(6) does not presuppose finite N_infinity.

The clock tends to infinity. Otherwise the finite-sum mass estimate of Turn3
would give M_h<=2e^tau integral_0^t x². By(5) the latter integral is at most
C(1+t)^a0 tau(t). Together with x<=C(1+t)^a0, a bounded clock would imply
M(t)=O(t^a0), contradicting a0<beta.

An existing positive2-cluster cohort at a fixed positive clock time gives,
by the hitting-time Markov estimate in Turn3,

    M(t(tau))>=c tau^(nu+1),
    P(t(tau)):=sum_(j>=2)j^p c_j(t(tau))>=c tau^nu        (7)

for large tau. Hence

    tau(t)<=C t^d.                                       (8)

The expectation upper bound and(6) also give

    M_h(t)<=G(tau(t))N(t)<=C tau(t)^(nu+1)N(t)           (9)

for large t. All constants in these inequalities may depend on the solution.

## 4. A moving physical-time monomer barrier

The monomer equation is

    x'=alpha t^omega-2x²-P(t)x.

By(7), P(t)>=c tau(t)^nu eventually. We claim that

    x(t)<=C t^omega tau(t)^(-nu) eventually.              (10)

Choose C>2alpha/c and put u(t)=C t^omega tau(t)^(-nu).
At a crossing x=u, since tau'=x,

    u'=C omega t^(omega-1)tau^(-nu)
          -nu C²t^(2omega)tau^(-2nu-1).                 (11)

If omega<=0, division of both negative terms by t^omega shows that they
tend to0: t^(-1)tau^(-nu)->0 and t^omega tau^(-2nu-1)->0. If omega>0,
the first term in(11) is nonnegative. To control the second, use(5)-(6):
N(t)<=C t^(omega/2)tau(t). Because x=o(M), (9) yields

    tau(t)>=c t^k,    k=(1+omega/2)/(nu+2).              (12)

The finite-cluster assumption d=(omega+1)/(nu+1)<1/2 implies
omega<(nu-1)/2<(4nu+2)/3. This is precisely strong enough to give
omega-k(2nu+1)<0. Therefore t^omega tau^(-2nu-1)->0 also in this case.

It follows that, at all sufficiently late crossings, u'>= -o(t^omega).
But the vector field evaluated at u is at most
(alpha-cC)t^omega<=-alpha t^omega, so an upward crossing is impossible.
There is an eventual entry below u: if x>u held forever, x'<=-alpha t^omega,
whose integral diverges since omega>-1, forcing x negative. This proves(10).
The crossing calculation only substitutes tau'=u at the crossing itself;
it does not replace tau'=x away from a crossing.

## 5. A finite exponent bootstrap proves N_infinity is finite

Suppose x(t)<=C t^a eventually, for some real a. Combining d tau=x dt with
(8), integration by parts for integral x d tau gives

    N(t)=O(t^(a+d)) if a+d>0,
    N(t)=O(log t)  if a+d=0,
    N(t)=O(1)      if a+d<0.                             (13)

For a>=0 the first bound follows directly from N<=C t^a tau plus a finite
initial contribution. For a<0, use
integral_T^t s^a d tau(s)=t^a tau(t)-T^a tau(T)-a integral_T^t s^(a-1)tau(s)ds.
The bound tau(s)<=Cs^d proves all three cases of(13). The finite initial
part of N is never discarded.

On the other hand, x=o(M) by(5), so(9) implies

    tau(t)^(nu+1)>=c t^beta/N(t).

If N(t)=O(t^b), equations(10) and nu/(nu+1)=p yield the improved exponent

    x(t)=O(t^(d-1+p b)).                                 (14)

Start with a=a0 from(5) and write b=a+d. As long as b>0, applying(13)-(14)
replaces b by

    b_new=p b+2d-1.                                      (15)

Here0<p<1 and2d-1<0. The affine iteration has a strictly negative fixed
point; thus after finitely many steps b becomes nonpositive. If b=0 occurs
exactly, the logarithmic bound in(13) is O(t^epsilon) for every epsilon>0.
Choose epsilon<(1-2d)/p; the next bound has b_new=2d-1+p epsilon<0.
Then(13) gives bounded N(t). Since N is increasing and positive after time0,

    0<N_infinity<infinity.                               (16)

This is a finite bootstrap of proved inequalities. It assumes neither a
regularly varying monomer concentration nor differentiability of any
asymptotic equivalence. Strict d<1/2 is essential here.

## 6. Closing the asymptotics and profile

The pure-birth hitting-time estimates of Turn2 imply Y_v/s(v)->1 in probability
for every0<p<1, with s(v)=[(1-p)v]^(1/(1-p)). Its expectation upper bound G
upgrades this to L¹ convergence and then to convergence of its pth moment,
as in Turn3. The now finite cohort measure f(u)du permits dominated convergence
in(6), giving

    M_h(t(tau))~N_infinity sigma(tau),
    P(t(tau))~N_infinity sigma(tau)^p.

The original monomer estimate(5) gives x=o(M), so exact mass implies
sigma(t)~kappa t^beta/N_infinity. Consequently

    P(t)~D t^(p beta),   D=N_infinity^(1-p)kappa^p.        (17)

Using this clock growth in(10) already gives x=O(t^(d-1)), which decays and
makes2x negligible in P+2x. Thus the scalar equation is
x'=alpha t^omega-a(t)x, with a(t)~D t^(p beta).
Use upper/lower curves(1±epsilon)(alpha/D)t^(d-1). Their derivative is
O(t^(d-2)), whereas the strict vector-field discrepancy at each curve has
size c_epsilon t^omega. The ratio tends to zero because
(d-2)-omega=-p beta-1<0. Integral divergence of t^omega ensures eventual
entry and the crossing inequalities ensure preservation. Hence

    x(t)~(alpha/D)t^(d-1)=B t^(d-1).

Integration gives(3). Rewriting in the exact clock gives
f(tau)~C tau^(-r), where r=1/d-1 and

    C(1-p)^r=alpha N_infinity^(-1/beta)kappa^(-omega/beta).

Turn2 therefore gives the off-front limit with q and A_* in(4).
The same dominated-cohort argument used for Turn3's mass measures proves
weak concentration of leading mass at eta=1. This establishes every assertion
in Section1 within the strict regime(1).

## 7. Parameter comparison and open gaps

Let r_report=[1-omega(1-p)]/[(omega+2)(1-p)]. Exact algebra gives

    r-r_report=(1-2d)/[d(beta+1)]>0,
    (omega+2)/(3-2p)-beta=(1-2d)/(3-2p)>0.

Thus this strict regime genuinely has a different monomer-clock exponent and
physical size scale from the report's formal extension. Its bulk profile
cannot be used to integrate through the front: the bulk mass scale exponent
beta(2-q) differs from beta by2d-1<0, while r>1 gives a nonintegrable formal
front singularity. The missing leading mass is the atom proved above.

The critical case d=1/2 makes the bootstrap's forcing term zero and is not
settled. The region d>1/2, the original general polynomial-tail initial class,
and a front concentration profile remain unresolved. These are not assigned
new guessed source statements. This is substantive turn4/5 on the primary
physical model; one further author turn remains before the final scoped
unresolved disposition if those gaps persist.
