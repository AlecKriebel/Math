# Functional-analytic dependencies of the triangle product bridge

Checked independently against Cohn–de Laat–Salmon arXiv:2206.15373v1,
Section 3, and de Laat–Vallentin arXiv:1311.3789v3, Sections 3.2 and 5.1.
The corrected 2021 v3, rather than only the published 2015 text, is used:
its arXiv record and Section 3.2 footnote explicitly record a repair of
Lemma 5. Compact theta-prime duality is proved directly in Section 5.1,
Lemma 10; the general hierarchy statement is Theorem 1.1 in this version.

This audit isolates standard functional-analysis foundations from the
substantive application. It does not assert formal-machine verification.
The relevant sign sets are closed, symmetric, and at distance at least 1
from the origin. Their topology and zero-coordinate strata are essential.

## 1. Schwartz duality, with the perturbation repair made explicit

Work in the real even Schwartz space X in R^N. This loses no feasible
functions: real functions with real nonnegative Fourier transform are
even. Let C be a closed symmetric set disjoint from the origin, and let p
be the infimum of f(0) subject to f in X, fhat(0)=1, fhat>=0, f|C<=0.
Its dual supremum is over c for which an even tempered measure

    T=delta_0+mu,  mu>=0, supp(mu) subset C,
    That=c delta_0+nu,  nu>=0

exists. Pairing with a feasible f gives f(0)>=<T,f>=<That,fhat>>=c, so
weak duality holds. Evenness removes any reflection convention in Fourier
distributional pairings. The nonnegative distributions are Radon measures
of polynomial growth by the standard positive-distribution theorem.

Here is the crucial perturbation construction, spelled out because a
literal reading of Lemma 3.4's abbreviated use of a_j would not give
convergence to zero when a_j tends to a nonzero g off C.

For an even rapidly decreasing measurable u, choose an even Schwartz
h>=0 with h(0)>0 and supp(hhat) contained in the closed unit ball. One
choice is h=phihat^2, for an even nonnegative smooth phi supported in the
half-unit ball. Pick epsilon in (0,1] with h>=epsilon on the epsilon ball,
and set

    G(y)=sup_{|x|>=|y|-1}|u(x)|,
    E(u)=G*h/(epsilon vol(B_epsilon)).

E(u) is Schwartz, dominates |u| everywhere, and its Fourier transform is
supported in the unit ball. The domination follows by integrating over
|y-x|<=epsilon. Every derivative is a convolution of G with a Schwartz
derivative of h, so it is rapidly decreasing. If u_j tends to zero in all
weighted supremum norms, then E(u_j) tends to zero in every Schwartz
seminorm. The support conclusion follows from the Fourier convolution
identity in tempered distributions. No differentiability of u is needed.

For rapidly decreasing u,v tending to zero, set e0=-E(u), and let k be an
envelope of |v|+|e0hat| in the Fourier-variable space. Taking the inverse
Fourier transform kcheck, define e=e0+kcheck. The function kcheck is
supported in the unit ball, and vanishes on its boundary by continuity.
Thus

    e(x)<=-|u(x)|  for |x|>=1,
    ehat>=|v|,
    e_j -> 0 in Schwartz seminorms when u_j,v_j -> 0.

This proves the perturbation lemma used by Cohn–de Laat–Salmon. An arbitrary
positive distance from C to the origin is handled by rescaling first.

Define K0 as the convex subset of X times X of pairs (a,b) for which some
f in X with fhat(0)=1 satisfies a>=f on C union {0} and fhat>=b everywhere.
Let K be its closure. Fix c<p and choose a smooth even g supported in a
small ball avoiding C, with g(0)=c. If (g,0) belonged to K, metrizable
Schwartz topology would give pairs (a_j,b_j) tending to (g,0) and witnesses
f_j. Apply the perturbation lemma to

    u_j=(a_j-g) 1_C,   v_j=b_j.

These inputs tend to zero in all rapidly decreasing weighted supremum
norms. On C, u_j=a_j. The resulting e_j tends to zero in Schwartz space,
and F_j=f_j+e_j has F_j|C<=0 and F_jhat>=b_j+|b_j|>=0. Its Fourier mass
t_j=F_jhat(0) tends to 1 and is positive for large j. Moreover

    F_j(0)<=a_j(0)+e_j(0)->c.

Normalizing F_j/t_j gives feasible functions with limsup objective at most
c, contradicting c<p. Therefore (g,0) is outside K. This establishes the
nonclosure assertion rather than assuming continuity of the optimizer.

Separate this point from K by a continuous real linear functional on X
times X. Write it as (T1,T2). Monotonicity in a and b gives T1>=0 and
T2<=0; the freedom to alter a away from C union {0} gives
supp(T1) subset C union {0}. Hence

    T1=lambda delta_0+mu,  lambda>=0, mu>=0, supp(mu) subset C,
    T2=-nu,  nu>=0.

The coefficient lambda cannot be zero: inserting any feasible f into the
separator would demand <mu,f>-<nu,fhat>>0, although both terms have the
opposite sign. Feasible f exists, for example by rescaling a normalized
Gaussian polynomial negative beyond the distance from C to the origin.
Normalize lambda=1. For every even f with fhat(0)=1, the pair (f,fhat)
belongs to K0, so

    <That-nu,fhat> > c,   T=delta_0+mu.

The Fourier transform runs through all even Schwartz functions of value
1 at zero. Varying freely in the subspace of functions vanishing at zero
forces That-nu=c' delta_0, with c'>c. This supplies a dual value exceeding
every c<p. Together with weak duality, it proves the no-gap theorem for
the closed symmetric sign sets needed here.

The foundations used are Hahn–Banach separation for Fréchet spaces,
distributional Fourier transform, the positive-distribution theorem, and
ordinary convolution and Schwartz-space estimates. The central no-gap
assertion is not imported without inspecting its proof.

## 2. Continuous and Schwartz primal infima coincide

Let f be continuous and integrable, with fhat>=0, fhat(0)=1, and f<=0 on
C. Fourier positivity implies positive definiteness and |f(x)|<=f(0).
For a dual certificate T=delta_0+mu and That=c delta_0+nu, choose a smooth
even nonnegative phi supported in the unit ball with integral 1 and
phihat>=0. For example phi=psi*psi where psi is even smooth nonnegative,
supported in the half-unit ball, and of integral 1. Put

    phi_epsilon(x)=epsilon^(-N)phi(x/epsilon),
    H=(f phihat_epsilon1)*phi_epsilon2.

The function H is Schwartz: the first factor is rapidly decreasing because
f is bounded, and convolution with smooth compact support gives smooth
rapidly decreasing derivatives. Its Fourier transform is

    Hhat=(fhat*phi_epsilon1) phihat_epsilon2>=0.

Tempered pairing gives

    H(0)+integral H dmu = c Hhat(0)+integral Hhat dnu
                        >= c (fhat*phi_epsilon1)(0).

Let epsilon2 tend to zero. Approximate-identity convergence and domination
against the polynomial-growth measure mu give

    f(0)+integral f phihat_epsilon1 dmu
      >= c (fhat*phi_epsilon1)(0).

The left side is at most f(0) because f<=0 on supp(mu) and
phihat_epsilon1>=0. Letting epsilon1 tend to zero gives f(0)>=c, since
fhat is continuous at zero and fhat(0)=1. Supremizing the dual certificates
gives f(0)>=p. The reverse infimum inequality follows because Schwartz
functions are continuous and integrable. Thus the infima coincide, with
no assertion of primal attainment and no unsupported sign-preserving
mollification of the original f.

Domination is explicit: f phihat_epsilon1 is bounded by C_k(1+|x|)^(-k)
for every k, and its convolution with phi_epsilon2, for epsilon2<=1, has
the same kind of bound uniformly. Choosing k above the polynomial-growth
degree of mu makes that bound integrable. The approximate identity in
frequency converges because fhat is bounded and continuous, as f is L1.

## 3. Compact theta-prime duality in the needed Euclidean model

For a cube, or a disjunctive product of two cube graphs with adjacency
threshold 1, let V be its compact vertex set, D the diagonal in V^2, and
E the compact set of distinct nonedges. E is at Euclidean distance at
least 1 from D in displacement coordinates. Therefore D is open and
closed inside S=D union E. A nonnegative measure on S with diagonal mass
1 is exactly the compact theta-prime primal model in BRIDGE_PROOF.md.
The unordered-pair model eta of de Laat–Vallentin Lemma 10 pushes forward
to this ordered-pair model by splitting each off-diagonal pair equally
between its two orders and keeping singleton mass on the diagonal; its
objective and normalization are preserved.

The core closed-cone condition in that proof concerns

    K1={(i_*eta,eta(S)): eta>=0 on S, eta(D)=0},
    K2={(nu,0): nu positive definite on V^2}.

K2 is weak-star closed because its defining pairings with continuous
positive definite kernels are nonnegative. K1 has a compact convex base:
take the probability measures supported on E and apply the injective map
eta -> (i_*eta,eta(S)). Their weak-star compactness is Banach–Alaoglu (or
compactness of probabilities on a compact metric space). The compact-base
theorem gives that K1 is closed and locally compact.

The intersection K1 intersect K2 is zero immediately: their second
coordinates agree only when eta(S)=0, and eta is nonnegative. This avoids
depending on the repaired higher-level hierarchy Lemma 5. As an additional
support control, a nonnegative positive definite measure supported on E
must vanish: cover V by finitely many small relatively open cliques U_j,
use zero mass on U_j^2, and apply positive definiteness to
(1_Ui+s 1_Uj) tensor (1_Ui+s 1_Uj) for s=1 and s=-1. Each cross mass is
zero, and the finite cover gives zero total mass. The measurable tests are
justified by bounded continuous approximation and dominated convergence;
min(1,t dist(x,V\U)) tends pointwise to the open-set indicator on a compact
metric space. This extra support check is not needed for cone intersection.

The Klee–Dieudonné closed-cone difference theorem applies: closed cones
with zero intersection and one locally compact cone have a closed
Minkowski difference. Hence K1-K2 is closed. Standard conic separation
(the closed-cone duality theorem used in de Laat–Vallentin Section 3.2)
gives theta-prime primal-dual equality. Feasibility is explicit: a point
mass on a vertex supplies the primal; a finite open-clique cover and a
partition-of-unity kernel, as in their Lemma 7, supplies a finite dual.
Alternatively the periodicized admissible Gaussian in BRIDGE_PROOF.md
supplies a finite dual for each cube, and the product is a compact
topological packing graph admitting such a finite cover.

The resulting dual is precisely continuous K with K-1 positive definite,
K<=0 on distinct nonedges, minimizing max K(x,x). The proof of equality
of these compact primal and dual values has thus been checked in the
specific Euclidean model needed for the bridge. The general hierarchy
correction in v3 is recorded but its higher-level assertions are unused.

## Audit disposition

For the product upper inequality, the substantive standard analytic inputs
now have checked proof mechanisms and exact model translations: Schwartz
no-gap separation, continuous-test extension, compact theta-prime closed
cone separation, and ordinary Poisson summation. Their boundary and
regularity conditions hold for Csquare, Ctriangle, and the cube graphs.
The remaining central gap in Target B is the sharp planar two-point
upper input, not the product or lower-bound bridges. A fresh adversarial
review of these owned derivations remains appropriate before promotion.
