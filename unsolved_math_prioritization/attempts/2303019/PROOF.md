# Barth's tangential-limit problem: an attributed proof reconstruction

Problem 2303019 / AMR-022-3019 / Hayman–Lingham 3.19.

**Status:** already solved by Hiroaki Aikawa (1990). This document verifies an existing result, with no novelty or priority claim. The geometric grid and alternating-boundary-data mechanism are Aikawa's. The estimates below are supplied in full, with deliberately generous constants and a direct compact-disk estimate replacing the article's local-density estimate.

## 1. Exact target and published result

Write D={z in C: |z|<1}. Fix a continuous tangential path C in D ending at 1, and set C_theta=e^(i theta)C. The question asks for a single positive real harmonic function v on D whose limit along C_theta as |z| tends to 1 fails to exist for every theta in [0,2 pi]. The function may depend on the chosen C; the quantifier does not require one function to work for all initial paths simultaneously.

Here tangential has the standard meaning used in Aikawa's proof: C eventually leaves every Stolz region at 1. Equivalently, on the terminal portion of the path,

    |1-z|/(1-|z|) -> infinity.

Aikawa's theorem, Proc. Amer. Math. Soc. 108 (1990), p.458, supplies a bounded real harmonic h with the required everywhere divergence. Its proof, pp.461–463, constructs h as the Poisson integral of real bounded boundary data. The construction below gives explicitly

    -1 <= h <= 1,
    liminf_(z in C_theta, |z|->1) h(z) <= -1/4,
    limsup_(z in C_theta, |z|->1) h(z) >=  1/4

for every theta. Consequently

    v=(h+2)/4

satisfies 1/4 <= v <= 3/4 and is strictly positive and harmonic. Its liminf is at most 7/16 and its limsup at least 9/16 on every C_theta. This also rules out convergence in the extended real line.

## 2. Tangential geometry

Parametrize a terminal part by a continuous map gamma:[0,1)->D with gamma(t)->1 as t->1. On a sufficiently short terminal part the principal argument alpha(t)=arg gamma(t) is continuous and lies in (-pi/4,pi/4). Put r(t)=|gamma(t)|. Because

    |1-gamma(t)| <= 1-r(t)+|alpha(t)|,

tangentiality implies |alpha(t)|/(1-r(t))->infinity.

We first prove that arbitrarily near the endpoint there are compact subpaths Y contained in an annulus

    a <= |z| <= b < 1

whose angular projection is an interval of length ell>0 and for which

    ell/(1-a)

is arbitrarily large. Both a and b can be required to exceed any fixed R<1, and a can be required to exceed any prescribed number below 1.

Choose a near 1, greater than the modulus of the starting point of the terminal part. Let t_a be the last time r(t)=a. This time exists: the level is attained by continuity; all its occurrences belong to a compact subinterval because r(t)->1. After t_a the modulus is strictly greater than a. As a->1, t_a->1, since every fixed compact parameter interval has maximum modulus strictly less than 1. Set alpha_a=alpha(t_a). Then

    |alpha_a|/(1-a) -> infinity.

In particular alpha_a is nonzero for a sufficiently close to 1. Choose t'>t_a with |alpha(t')|<|alpha_a|/2. Choose b strictly between max_[t_a,t'] r(t) and 1, and let t_b>t_a be the first time r(t)=b. Then t_b>t', and Y=gamma([t_a,t_b]) lies in the stated annulus. By continuity its arguments form a compact interval I. Its length ell satisfies

    ell >= |alpha(t_a)-alpha(t')| > |alpha_a|/2.

Thus ell/(1-a) can be arbitrarily large. Moreover ell->0 if the construction is placed sufficiently far along the path, because all arguments on such a terminal part tend uniformly to 0. No differentiability, rectifiability, simple-path assumption, or monotonicity of r(t) is used.

## 3. A finite radial grid meeting every rotation

For one such Y, let d=1-a and let N=ceil(2 pi/ell). Set eta_k=2 pi k/N for k=0,...,N-1, and

    M = union_k {r exp(i eta_k): a<=r<=b}.

The grid spacing 2 pi/N is at most ell. The angular projection of exp(i theta)Y is the interval theta+I modulo 2 pi, so it contains some eta_k. At an associated point the radius lies in [a,b]. Therefore

    exp(i theta)Y intersects M for every theta.

This is a geometric statement for all rotations, not an almost-everywhere or dense-set statement.

Set m=16 and choose d<1/16. Let E be the union on the angle circle of closed arcs of circular radius md around the eta_k. Its Lebesgue length obeys

    |E| <= 2md N <= 2md(2 pi/ell+1).

Consequently |E| can be made arbitrarily small while a is as close to 1 as desired. Indeed d/ell can be arbitrarily small by Section 2 and d can be arbitrarily small. Overlap and wraparound of arcs do not affect this upper bound.

## 4. Two elementary Poisson estimates

For real integrable f on the angle circle write

    P[f](r exp(i eta)) = (1/(2 pi)) integral_(-pi)^pi P_r(t) f(eta+t) dt,
    P_r(t) = (1-r^2)/((1-r)^2+2r(1-cos t)).

The kernel is positive and has integral 2 pi. Its integral against bounded real data is a real harmonic function. These standard Poisson facts follow, for example, by taking the real part of (exp(i t)+z)/(exp(i t)-z), differentiating under the integral on compact disks, and using the constant Fourier coefficient 1 of its geometric-series expansion.

**Local sign estimate.** Suppose 1/2<=a<=r<1, d=1-a<1/16, |f|<=1, and f=s on the circular arc of radius md around eta, where s is either +1 or -1. For |t|<=pi, the concavity of sine on [0,pi/2] gives

    1-cos t = 2 sin^2(t/2) >= 2t^2/pi^2.

Since r>=1/2 and 1-r<=d,

    P_r(t) <= pi^2 d/t^2  (t != 0).

It follows that the normalized kernel mass outside |t|<=md is at most

    (1/(2 pi))*2*pi^2*d*integral_(md)^pi t^(-2) dt
    <= pi/m < 1/4.

The complementary mass exceeds 3/4. Therefore

    s P[f](r exp(i eta)) > 1/2.

**Compact-disk estimate.** For 0<=r<=R<1,

    P_r(t) <= (1+r)/(1-r) <= (1+R)/(1-R).

Hence, for any measurable E,

    sup_(|z|<=R) P[1_E](z) <= K(R)|E|,
    K(R)=(1+R)/(2 pi(1-R)).

These two estimates are the only analytic bounds needed below.

## 5. Recursive construction and convergence

Put b_0=1/2 and epsilon_j=2^(-j-4) for integers j>=1. Inductively apply Sections 2–3 to choose Y_j, a_j, b_j, M_j, E_j so that

    b_(j-1)<a_j<b_j<1,
    a_j>1-2^(-j),
    1-a_j<1/16,
    |E_j|<=2^(-j),
    K(b_(j-1))|E_j|<=epsilon_j.

There is no circularity: at stage j, b_(j-1) and the required positive upper bound on |E_j| are already fixed. Section 3 allows that bound to be met arbitrarily far out. In particular a_j->1, and

    sup_(|z|<=b_(j-1)) P[1_(E_j)](z)<=epsilon_j.

Define f_0=0. With s_j=(-1)^j, define f_j to equal s_j on E_j and f_(j-1) elsewhere. Thus

    f_j is real, |f_j|<=1,
    f_j=s_j on E_j,
    |f_j-f_(j-1)|<=2*1_(E_j).

Because sum_j |E_j|<infinity, the measure of the set of points belonging to infinitely many E_j is zero: for every J its measure is at most sum_(j>=J)|E_j|, which tends to zero. At every other boundary point the overwriting eventually stops. Let f be its eventual value there, and assign f=0 on the exceptional null set. Then f is real measurable, |f|<=1, and f_j->f almost everywhere.

Put h_j=P[f_j] and h=P[f]. Dominated convergence shows h_j->h uniformly on each compact disk, using the displayed compact-disk bound for the kernel. In particular h is a bounded real harmonic function with -1<=h<=1.

For |z|<=b_j and k>j, we have b_j<=b_(k-1), so

    |h_k(z)-h_(k-1)(z)|
    <=2 P[1_(E_k)](z)<=2 epsilon_k.

The tail telescopes, giving

    sup_(|z|<=b_j)|h(z)-h_j(z)|
    <=2 sum_(k>j)epsilon_k
    =2^(-j-3)<=1/16.

For z in M_j, its angle is a grid center and its radius is at least a_j. The local sign estimate applies to f_j and gives s_j h_j(z)>1/2. Hence

    s_j h(z)>1/2-1/16=7/16>1/4  (z in M_j).

## 6. Every rotated path oscillates

Fix any theta. For every j, Section 3 supplies a point z_j in exp(i theta)Y_j intersect M_j. Then z_j belongs to C_theta and |z_j|>=a_j->1. Along even j, h(z_j)>1/4; along odd j, h(z_j)<-1/4. Therefore its limsup and liminf along C_theta are separated as claimed in Section 1. The construction of h precedes the choice of theta and uses the same E_j and f for all theta.

The affine function v=(h+2)/4 now settles the original positive-harmonic question for every theta, including theta=0 and theta=2 pi, which represent the same rotation. This completes the verification.

## Dependencies, attribution, and scope limits

All substantive geometric and kernel estimates are proved above. The remaining standard inputs are continuity and the intermediate value property, compactness of a closed bounded real interval, elementary Lebesgue integration and dominated convergence, and the explicitly described Poisson-kernel representation facts. No unproved research conjecture is imported.

The proof reconstructs Aikawa's published mechanism, with its inner-disk perturbation estimate replaced by a simpler sufficient bound for the finite circle. It is not a claim that every printed estimate in the 1990 article was mechanically certified. It does give a complete independent check of the theorem needed here. No claim is made for disconnected sequential approach sets, nontangential paths, every possible initial path simultaneously, or a new result in higher dimensions.

## References

- H. Aikawa, *Harmonic functions having no tangential limits*, Proc. Amer. Math. Soc. 108(2) (1990), 457–464. [DOI](https://doi.org/10.1090/S0002-9939-1990-0990410-X). Main theorem p.458; proof pp.461–463.
- H. Aikawa, *Harmonic functions and Green potentials having no tangential limits*, J. London Math. Soc. (2) 43 (1991), 125–136. [Author manuscript](https://www.isc.chubu.ac.jp/aikawa/research/AikawaPapers/har.pdf), Section 1, Theorem A. This manuscript explicitly restates the disk result and identifies it as answering Barth's question.
- W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed p.66, Problem and Update 3.19; reference [12].
