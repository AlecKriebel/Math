# External-ray rotation: partial results and the remaining boundary problem

Target: 5300074 / AMR-052-0074. Date: 8 October 2026.

**Disposition: partial only after five substantive approaches.** This is neither a solution nor a counterexample to the full question. No full prior resolution was verified, and no novelty is claimed for the deductions below. The strongest deduction supplied here is continuity on the strictly repelling locus. The indifferent boundary, with disconnected Julia sets allowed, remains untreated in the required generality.

## 1. Exact scope and conventions

Fix an integer d >= 2 and put

    X_d = {P(z)=z^d+a_(d-1)z^(d-1)+...+a_1 z : |a_1|>=1},
    U_d = {P in X_d : |a_1|>1},
    B_d = {P in X_d : |a_1|=1}.

The topology is coefficient convergence. The marked fixed point is always 0. Bielefeld's problem list [B], section 2, Question 12, printed page 8, does not impose connectedness of the Julia set. It asks for a unique continuous circle-valued extension of the ray rotation, with value theta at multiplier exp(2*pi*i*theta).

Use the normalized Böttcher coordinate B_P(z)/z -> 1 at infinity and the Green function G_P. An ordinary external ray follows the descending gradient trajectory with the prescribed Böttcher angle. It can stop at an escaping precritical point. The conventional generalized rays add the immediate-left and immediate-right continuations at every such collision. They are the one-sided limits of ordinary rays, not arbitrary choices of turns. This convention is described in [GM], Appendix A, and [PZ], section 2.2. The original short problem statement does not separately specify the collision convention. We therefore distinguish the smooth-ray domain from the generalized-ray domain rather than silently identifying them.

Let sigma_d(t)=d*t modulo 1. A nonempty compact forward-invariant set A in the circle (sigma_d(A) contained in A) is a rotation set when sigma_d restricted to A has a continuous nondecreasing degree-one circle extension. Its rotation number is independent of the extension, since an orbit starting in A determines that number. For a finite set on which sigma_d acts as a cyclic-order-preserving permutation, this is the cyclic shift divided by the number of points; it is not the external angle itself. Several cycles can have the same rotation number.

The relevant accessibility theorem is due to Levin and Przytycki [LP], with a precise restatement in [PZ], Theorem 2.1 and its introduction: at a repelling or parabolic periodic point the generalized landing angles form a nonempty rotation set. At a fixed point this uses sigma_d. A nondegenerate filled-Julia component gives a finite set of periodic angles. The main theorem of [PZ] additionally supplies a smooth ray in that case.

All uses of these results concern their stated hypotheses. A smooth ray is not assumed at a singleton component, and an irrational rotation number is not assumed to be rational merely because the landing point is repelling.

## 2. Circle-map lemmas

These elementary lemmas make the compactness argument precise.

### Lemma 2.1. Bounded-slope extension

Suppose A is a nonempty proper closed subset of R/Z and sigma_d|A admits a nondecreasing degree-one extension. Such an extension can be chosen d-Lipschitz in the lifted real coordinate.

Proof. Start with any nondecreasing lift F satisfying F(x+1)=F(x)+1. If x<y<x+1 are lifts of points of A, then

    0 <= F(y)-F(x) <= 1,
    F(y)-F(x) = d(y-x)-k for some integer k.

The first inequalities force k>=0: a negative k would make the difference strictly bigger than 1. Consequently F(y)-F(x)<=d(y-x). On every complementary interval of the lifted A, replace F by affine interpolation between its endpoint values. Each resulting slope belongs to [0,d]. The endpoint estimate and the affine interpolation give the d-Lipschitz estimate globally, including for infinitely many complementary intervals. If A consists of one circle point, the single complementary interval has slope 1. This construction preserves the original values on A and has degree one. QED.

The same statement applies to a finite union I of closed intervals whenever sigma_d|I has such an extension; invariance of I is unnecessary.

### Lemma 2.2. Continuity of translation number

For continuous nondecreasing degree-one lifts F_j converging uniformly to F, their translation numbers tend to that of F.

Proof. For each positive integer N set m_N=inf_x(F^N(x)-x) and M_N=sup_x(F^N(x)-x). Monotonicity and degree one give M_N-m_N<=1. The sequence m_N is superadditive and M_N is subadditive. Thus their normalized limits coincide, giving the translation number tau(F), and

    |F^N(x)-x-N*tau(F)| <= 1.

For fixed N, uniform convergence implies F_j^N(x)->F^N(x). Hence

    limsup_j |tau(F_j)-tau(F)| <= 2/N.

Let N tend to infinity. Changing a lift by an integer changes its translation number by that integer, so the corresponding circle rotation number is continuous as well. QED.

### Lemma 2.3. Compactness of abstract rotation sets

If nonempty compact sigma_d-rotation sets A_j converge in Hausdorff distance to A, then A is a rotation set and rot(A_j)->rot(A).

Proof. Invariance passes to the limit. Choose the d-Lipschitz extensions from Lemma 2.1 and lifts with F_j(0) in [0,1]. Every subsequence has a uniformly convergent further subsequence on [0,1], hence on compact subsets of R, with a nondecreasing degree-one limit F. For a in A, select a_j in A_j tending to a. The uniform Lipschitz bound implies that the limiting circle map agrees with sigma_d at a. Thus it is an extension for A. Lemma 2.2 identifies the limit of rotation numbers with rot(A), independent of the subsequence. QED.

This is a statement about abstract angle sets. It does not assert continuity of polynomial landing sets.

## 3. Continuity on the strictly repelling locus

Write rho(P) for the generalized-ray rotation at 0 when P is in U_d.

### Proposition 3.1. Smooth periodic access implies local constancy

If some smooth ray of periodic angle lands at the repelling fixed point 0 of P, then rho is constant in a coefficient neighborhood of P inside U_d.

Proof. Stability of a smooth periodic ray landing at a repeller is [GM], Lemma B.1. Apply it simultaneously to the finite orbit of the ray angle. The marked repelling fixed point continues as 0 in this family. Its continued ray orbit has the same cyclic permutation, which determines rho for the entire landing rotation set. QED.

In particular this applies when the filled-Julia component containing 0 is nondegenerate, by [PZ]. This uses stability of the rotation number, not equality of the full landing-angle sets; the latter can fail, as [GM], Example B.3 shows.

### Proposition 3.2. Continuity at a singleton component

If P_0 is in U_d and the filled-Julia component containing 0 is {0}, then rho(P)->rho(P_0) as P->P_0 in U_d.

Proof. The argument uses only compact pieces at positive potential, not parameter continuity of complete rays.

**Persistent degree-one domains.** Write V_r(P) for the component containing 0 of {G_P<r}. Its closure is compact. These nested closures shrink, as r decreases to zero, to the filled-Julia component containing 0. For the present P_0 their intersection is {0}: the intersection is connected, lies in K(P_0), and contains that whole component. Compactness then implies that the closures eventually lie in any prescribed neighborhood of 0.

Choose a small disk D centered at 0 on which P_0 is univalent. It can be chosen so that |P_0'(z)-P_0'(0)|<|P_0'(0)|/3 on a slightly larger disk; integrating along line segments shows that all sufficiently nearby polynomials are univalent on D as well. Choose t>0 small enough that closure(V_(dt)(P_0)) lies in D. Also require t and dt to be regular levels of G_(P_0). Such a choice exists: the positive critical levels are among G_(P_0)(c)/d^n for the finitely many escaping critical points c and n>=0, and this collection is locally finite away from zero.

A positive regular level of G_P is a finite disjoint union of smooth Jordan curves. Its sublevel components are Jordan domains: a bounded hole would contradict the maximum principle for the globally subharmonic function G_P. Consequently V_t(P_0) and V_(dt)(P_0) are bounded Jordan domains, with closure(V_t(P_0)) contained in V_(dt)(P_0). The functional equation G_P(P(z))=d*G_P(z) makes

    P_0: V_t(P_0) -> V_(dt)(P_0)

a proper onto map. It has degree one because P_0 is univalent on D. Here V_t is the inverse-image component containing 0, not the full polynomial inverse image.

The two boundary curves persist for nearby P. For completeness, on a compact subset of {G_(P_0)>0}, a common sufficiently large iterate lies in a common Böttcher neighborhood of infinity. There

    G_P(z)=d^(-N)*log|B_P(P^N(z))|.

The normalized Böttcher coordinate depends holomorphically on coefficients in that neighborhood. This formula gives uniform convergence of G_P and its spatial derivatives on the compact set. The implicit function theorem therefore supplies the unique nearby regular level curves at t and dt. They continue to surround 0, and compact containment and containment in D persist. The maximum principle identifies their interiors with V_t(P) and V_(dt)(P); no assertion about continuity of K(P) is needed. The same properness and univalence argument now applies to every nearby P.

Let g_P:V_(dt)(P)->V_t(P) be the inverse branch fixing 0. Its image is relatively compact in V_(dt)(P). Conjugating by a Riemann map taking 0 to 0 gives a disk self-map f with f(0)=0 and f(Disk) contained in {|z|<=r} for some r<1. Schwarz's lemma applied to f/r gives |f(z)|<=r|z|, so the iterates contract to 0. The marked filled component lies in V_t(P), since it is connected and cannot cross a positive-level boundary. Every forward image of that component lies in the same component, so each of its points belongs to every g_P^n(V_(dt)(P)). The contraction just proved forces the component to be {0}.

**Finite-interval circle extensions.** Let I(P) be the set of angles for which one of the prescribed generalized rays crosses boundary(V_t(P)). Apply the finite-interval construction in the proof of [L], Proposition 2.3, with its open domain K_0=V_(dt)(P) and its inverse branch g_P. It says that I(P) is a finite union of closed intervals, sigma_d restricted to I(P) has a continuous nondecreasing degree-one extension, and the nonempty landing rotation set A(P) is contained in I(P). The source's standard slope pi/2 is the ordinary Green-gradient convention used here.

Choose a d-Lipschitz extension h_P by Lemma 2.1. Since it agrees with sigma_d on the forward-invariant set A(P), its circle rotation number is rho(P).

**Persistence of the collision-free angles.** Let S(P_0) consist of angles u whose ordinary ray has no collision at potentials >=t and whose point at potential t belongs to boundary(V_t(P_0)). Then

    u in S(P_0) implies u in I(P) for all P sufficiently close to P_0.

Indeed, start the ray at a common large potential H in the Böttcher neighborhood. The initial point varies continuously with P. Along the compact reference segment from H down to t, the normalized vector field grad(G_P)/|grad(G_P)|^2 is smooth and has no singularity, uniformly for P sufficiently close to P_0. Ordinary differential-equation dependence gives a collision-free segment for P and a nearby endpoint at level t. A tubular neighborhood of the reference boundary contains only its continued level component, so that endpoint belongs to boundary(V_t(P)). The assertion is only for each fixed u; no uniform parameter neighborhood over all u is required.

Furthermore, S(P_0) is dense in I(P_0). There are finitely many angles with a collision at potential >=t, by [PZ], section 2.2(I). At any exceptional angle belonging to I(P_0), choose the left or right ray that crosses the marked boundary. The one-sided uniform convergence in [PZ], section 2.2, approximates its point at potential t by points of ordinary rays at angles avoiding that finite exceptional set. Because t is regular and different level components are separated, these nearby points lie on the same boundary component. Thus the approximating angles belong to S(P_0). This also treats interval endpoints and does not permit arbitrary turns at a collision.

**Taking the limit.** For any sequence P_j->P_0, the d-Lipschitz lifts of h_(P_j), normalized with value at 0 in [0,1], have a uniformly convergent subsequence on [0,1]. Its limit induces a continuous nondecreasing degree-one circle map h. For each fixed u in S(P_0), the persistence just proved gives h_(P_j)(u)=sigma_d(u) on the circle for all sufficiently large j. Hence h(u)=sigma_d(u). By density and continuity this holds on I(P_0), in particular on A(P_0). Therefore rot(h)=rho(P_0). Lemma 2.2 gives rho(P_j)->rho(P_0) along that subsequence. Applying the same argument to every subsequence proves the full limit. QED.

### Corollary 3.3

The generalized-ray rotation function rho:U_d->R/Z is continuous.

This is a deduction from the stated prior inputs and the compactness argument above. It is offered for mathematical review as a partial result; it is not an assertion that this observation is absent from the literature.

## 4. Uniqueness, including the smooth-ray interpretation

For the generalized convention, uniqueness of a continuous extension is immediate: U_d is contained in its domain by [LP] and is dense in X_d.

The smooth-ray domain is also dense in X_d. The following argument includes the normalization needed for the claimed angle shift.

Fix P in U_d. If its Julia set is connected, the periodic-access theorem already supplies a smooth ray. Otherwise consider, for real s close to zero, the shear

    F_s(r*exp(i*v))=r*exp(i*(v+s*log r)).

In logarithmic coordinates x+i*y, this is L_s(x+i*y)=x+i*(y+s*x). It commutes with multiplication by d and hence F_s commutes with w->w^d. The complex derivatives of L_s are 1+i*s/2 and i*s/2, so its Beltrami coefficient has modulus |s|/sqrt(4+s^2)<1 and tends uniformly to zero as s->0.

Pull its Beltrami structure back by B_P near infinity, extend it to the escaping basin using iterates of P, and put the standard structure on K(P). Commutation makes these definitions consistent and P-invariant almost everywhere; the critical/precritical set is negligible. This is the invariant-structure integration used in [L], section 4. The pure shear is written out here because the source's additional fixed-slope parametrization is not itself the specialization "stretching factor 1 with arbitrary twist."

The measurable Riemann mapping theorem gives a quasiconformal H_s, initially normalized to fix 0, 1 and infinity, such that Q_s=H_s P H_s^(-1) is a degree-d polynomial. The dilatations tend to 1, so compactness of normalized quasiconformal maps gives H_s and H_s^(-1) tending locally uniformly to the identity; every limit is the normalized conformal map fixing 0, 1 and infinity. Thus Q_s tends coefficientwise to P.

Near infinity, C_s=F_s B_P H_s^(-1) is conformal and satisfies C_s Q_s=(C_s)^d. Let b_s be its leading coefficient at infinity. It tends to 1: the maps C_s converge to B_P on a common sufficiently large circle, so their leading coefficients converge by the Laurent coefficient integral. Replace H_s by b_s H_s and Q_s by its conjugate under z->b_s*z, denoting the results by H_s and P_s again. Comparing leading coefficients in the displayed conjugacy shows that P_s is monic. The marked point is still 0, and the exact normalized identity is now

    B_(P_s) H_s = F_s B_P

near infinity. We have P_s->P coefficientwise, hence P_s remains in U_d for sufficiently small s. No preservation of the repelling multiplier by quasiconformal conjugacy is assumed.

For each escaping critical point c of P, choose N_c so that P^(N_c)(c) is in that common Böttcher neighborhood. Quasiconformal conjugacy preserves local degree and escape, so c_s=H_s(c) accounts for all the escaping critical points of P_s. The displayed identity shifts the Böttcher angle of P_s^(N_c)(c_s) by exactly

    s*G_P(P^(N_c)(c))/(2*pi) modulo 1.

This slope is positive. For each of the finitely many c, the parameters s making that angle rational form a countable set. Choose arbitrarily small s outside their union. Then P_s has no broken periodic ray: if a periodic-angle ray collided with an escaping precritical point omega, an iterate would take omega to some c_s, and a further iterate to P_s^(N_c)(c_s) near infinity. The angle of that point would be an integer power of d times the original rational ray angle, contradicting the choice of s. This uses the ray-image rules in [PZ], section 2.2.

The marked landing rotation set of P_s is either finite, consisting of periodic angles, or a minimal Cantor set, by the accessibility/dichotomy statement recalled in [PZ]. In the finite case every landing ray is now smooth. In the Cantor case there is a smooth landing ray because the set is uncountable while there are only countably many broken-ray angles. This proves density of the smooth-ray domain in U_d. Perturbing a boundary coefficient a_1 radially outward proves U_d dense in X_d and gives the asserted density in X_d.

Whenever a smooth ray lands at the marked repeller, its forward rays remain smooth and lie in the generalized landing set. Its rotation data therefore agree with the generalized rotation used here. Two continuous circle-valued extensions agreeing with the smooth-ray data agree on this dense subset, and hence agree everywhere. This is an existence-free uniqueness statement. It supplies neither the missing neutral-boundary limit nor compatibility at an initially accessible indifferent point.

## 5. What the multiplier inequalities do prove

Suppose P_j are degree-d polynomials with connected Julia sets, with the marked point repelling, and a_(1,j)->exp(2*pi*i*theta). Write their rotation numbers p_j/q_j in reduced form. The connected-case Yoccoz disk, recalled in [L], section 5, gives a choice L_j of log a_(1,j) such that

    |L_j-2*pi*i*p_j/q_j-log(d)/q_j| <= log(d)/q_j.

Put x_j=Re L_j=log|a_(1,j)|. Expanding the squared inequality yields

    (Im L_j-2*pi*p_j/q_j)^2
       <= 2*x_j*log(d)/q_j-x_j^2
       <= 2*x_j*log(d).

It follows that the circle distance between rho(P_j) and arg(a_(1,j))/(2*pi) is at most sqrt(2*log(d)*log|a_(1,j)|)/(2*pi). Thus rho(P_j)->theta. The branch of logarithm causes no ambiguity after passing to the circle.

The disconnected estimate does not have the same uniform constant. In [L], Theorem 5.1, for rational rotation p/q at a singleton component and fixed ray slope, its disk radius is

    R = pi*log(d)/(q*phi),

where phi is the angle of access. The resulting estimate is

    (Im L-2*pi*p/q)^2 <= 2*R*Re L-(Re L)^2.

It does give convergence to the multiplier argument along any such sequence for which R*log|a_1| tends to zero, in particular if R is bounded. No lower bound on q*phi sufficient for arbitrary coefficient-convergent sequences has been proved here. The irrational case cannot be handled by assigning it a positive access angle: [L], Remark 5.1, explicitly identifies the corresponding angle as zero.

Localization to a polynomial-like restriction was considered within this approach. The nearby restricted filled Julia set may disconnect. Simply invoking straightening and then the connected-Julia inequality would reintroduce the missing assumption, so that step is not used.

## 6. A verified failed shortcut

The multiplier argument alone is not the desired function, even inside the connectedness locus.

Take

    P(z)=z^2+(2+i/2)z.

The other fixed point is 1-(2+i/2), with multiplier 2-(2+i/2)=-i/2, which is attracting. Under translation w=z+(2+i/2)/2 the centered parameter is exactly

    c=(2+i/2)/2-(2+i/2)^2/4 = 1/16-i/4.

This is in the quadratic main cardioid, parameterized by the attracting multiplier -i/2, so the Julia set is connected. The fixed external ray of angle 0 lands at a repelling or parabolic fixed point. The attracting fixed point cannot be that landing point, and the only other fixed point is the marked 0. Hence its ray rotation is 0. But arg(2+i/2)/(2*pi) is nonzero modulo 1.

The family X_d deformation retracts onto its multiplier unit circle. Thus the multiplier argument supplies a continuous boundary-matching map for purely topological reasons. The example proves that this fact alone does not solve the dynamical interpolation problem.

## 7. Exact remaining gap and stopping point

The five approaches were: domain/density/uniqueness; repelling stability and finite positive-potential maps; indifferent-boundary multiplier estimates; the multiplier/topological formula; and Hausdorff compactness of rotation sets.

To finish, one still needs the following full boundary statement:

    If P_j in U_d converge coefficientwise to P in B_d,
    and P'(0)=exp(2*pi*i*theta), then rho(P_j)->theta,

without requiring connected Julia sets, a nondegenerate marked component for P_j, a positive lower bound for access angles, or rational rotation numbers. One must also verify agreement at any indifferent point already in the source's initial ray-landing domain. The present proofs do not establish that assertion.

Abstract compactness of rotation sets does not remove this gap. Given a sequence A(P_j), Lemma 2.3 controls any Hausdorff limit as an abstract rotation set. It does not identify its rotation with the multiplier angle at the limiting polynomial. Complete rays and their landing points can change under parameter limits; [GM], Appendix B, gives explicit parabolic-implosion changes in ray portraits. Replacing the missing identification by an assumed upper semicontinuity of landing would therefore be unjustified.

If the boundary statement and initial-domain compatibility were supplied, Corollary 3.3 and density would immediately give the requested unique extension by setting the boundary value to theta. That is a precise reduction, not an additional solution claim. No sixth proof strategy was pursued.

## References

[B] B. Bielefeld (editor), Conformal Dynamics Problem List, 1990, section 2, Question 12, printed p. 8. https://www.math.stonybrook.edu/preprints/ims90-1.pdf

[GM] L. R. Goldberg and J. Milnor, Fixed points of polynomial maps. Part II. Fixed point portraits, Annales scientifiques de l'Ecole Normale Superieure 26 (1993), 51-98; especially Appendices A-C. https://www.numdam.org/item/10.24033/asens.1667.pdf

[L] G. Levin, Disconnected Julia set and rotation sets, Annales scientifiques de l'Ecole Normale Superieure 29 (1996), 1-22; Proposition 2.3, section 4 and Theorem 5.1. https://www.numdam.org/article/ASENS_1996_4_29_1_1_0.pdf

[LP] G. Levin and F. Przytycki, External rays to periodic points, Israel Journal of Mathematics 94 (1996), 29-57. https://doi.org/10.1007/BF02762696 . The accessibility result used here was checked in the explicit restatement and attribution in [PZ]; this packet does not claim a full independent proof audit of [LP].

[PZ] C. L. Petersen and S. Zakeri, Periodic points and smooth rays, Conformal Geometry and Dynamics 25 (2021), 170-178, DOI 10.1090/ECGD/364. Author preprint: https://arxiv.org/abs/2009.02788 ; https://arxiv.org/pdf/2009.02788 .
