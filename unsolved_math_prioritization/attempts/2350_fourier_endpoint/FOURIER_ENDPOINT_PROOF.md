# The fourth-order Fourier endpoint: an unavoidable residual and its phase

12 October 2026. Authored analytic partial for problem 2350 / Erdős 864 (queue row 1741).

## Scope and result

The symmetric residual problem asks whether a Sidon set B in (0,L], with repetitions allowed and B disjoint from B+B+B, necessarily has cardinality at most (sqrt(2/3)+o(1))sqrt(L). This note does not prove that bound, improve the unrestricted upper constant, or construct an integer counterexample. It identifies a precise obstruction to transferring four-variable counts by Fourier norm estimates, and isolates a quantitatively sharp additional phase hypothesis for the macroscopically uniform subclass. No novelty or priority claim is made.

For a macroscopically uniform Sidon sequence of size k~c sqrt(L), write F for its Fourier transform, G for the Fourier transform of the constant-density interval model, and R=F-G. We prove

    integral |R|^4 = (2c^2 - (2/3)c^4 + o(1)) L,
    #{a+b+c=d in B^4} = (c^4/6 + o(1)) L
                         + Re integral R^3 conjugate(R).

At c=1, the residual fourth moment is 4L/3, eight times the putative main term L/6. In particular, neither an L^4-small-error transfer nor the conventional L-infinity/L^2/L^4 transfer can settle this endpoint: the latter would need an o(L^(1/4)) uniform error, whereas the true residual always has supremum at least (2/sqrt(3)+o(1))L^(1/4).

An avoiding near-maximal sequence, if one exists, must have normalized signed residual phase correlation tending to -1/8. The scalar norm data allow exactly this cancellation. Section 6 gives an explicit Fourier-function countermodel, with all leading second/fourth moments and stronger supremum uniformity, for which the signed four-variable functional is exactly zero. It is expressly not the Fourier transform of an indicator set and is not a counterexample to the integer conjecture.

## 1. Normalization and exact finite identities

Let B_L be a Sidon subset of [L]={1,...,L}, and put k=|B_L|. Define, on the circle T with Haar probability measure,

    e(t) = exp(2 pi i t),
    F(alpha) = sum_{b in B_L} e(b alpha),
    D_L(alpha) = sum_{n=1}^L e(n alpha),
    G(alpha) = (k/L) D_L(alpha),
    R(alpha) = F(alpha)-G(alpha).

The convention is unnormalized Fourier sums and a probability integral on T. Orthogonality gives the exact identities

    integral |F|^2 = k,
    integral |F|^4 = 2k^2-k,                              (1)
    integral |R|^2 = k-k^2/L.                             (2)

In (1), a Sidon set has k ordered equal-entry pair sums of multiplicity one and binom(k,2) distinct-entry pair sums of multiplicity two. Formula (2) also follows directly from summing (1_B(n)-k/L)^2 on [L].

Let T(B) count ordered quadruples, with repetitions allowed, satisfying a+b+c=d. Then

    T(B) = integral F^3 conjugate(F).                     (3)

The integral is real. The corresponding exact interval-model values are

    integral |G|^4 = (k/L)^4 (2L^3+L)/3,
    integral G^3 conjugate(G) = (k/L)^4 binom(L,3).        (4)

Indeed the interval's pair-sum energy is (2L^3+L)/3, while summing binom(d-1,2) for 3<=d<=L counts its triple-to-single solutions.

## 2. Mixed quartic terms vanish under macroscopic uniformity

Assume k/sqrt(L) tends to c>0 and that

    L^(-1/2) sum_{b in B_L} delta_{b/L}
        converges weakly to c 1_[0,1](x) dx.             (U)

Global Fourier uniformity is sufficient for (U), but is not needed for the argument below. In particular, this is not an inference from weak convergence to microscopic fourth-order convergence.

**Lemma 1.** Under (U), for j=1,2,3,

    integral |G|^(4-j) |R|^j = o(L).                     (5)

**Proof.** For each fixed K, weak convergence and equicontinuity imply

    sup_{|t|<=K} |R(t/L)| = o(sqrt(L)).                   (6)

To see equicontinuity, the derivatives in t of F(t/L)/sqrt(L) have absolute value at most 2 pi k/sqrt(L); the analogous assertion holds for G. Weak convergence gives pointwise convergence on each fixed t, so a finite mesh proves uniform convergence on [-K,K].

By (1), (4), and the triangle inequality in L^4,

    integral |R|^4 = O(L).                               (7)

The geometric-series bound gives

    |D_L(alpha)| <= min(L, 1/(2 ||alpha||_T)).

Consequently, for K>=1 and L>2K,

    integral_{||alpha||_T>K/L} |G(alpha)|^4
        <= C L K^(-3),                                 (8)

with C independent of L,K (since k=O(sqrt(L))). On the complementary arc of length 2K/L, (6) and |G|=O(sqrt(L)) show that the integral in (5) is o_K(L). On the outer arc, Hölder, (7), and (8) bound it by

    C L K^(-3(4-j)/4).

First take L to infinity for fixed K, then take K to infinity. This proves (5). No estimate for R at individual outer-arc points was used. QED.

## 3. Exact leading residual energy and the endpoint barrier

**Theorem 2.** Under (U),

    integral |R|^4
       = (2c^2-(2/3)c^4+o(1)) L,                         (9)

    T(B_L)
       = (c^4/6+o(1)) L + Re integral R^3 conjugate(R).  (10)

**Proof.** Expand |G+R|^4 and (G+R)^3(conjugate(G)+conjugate(R)). Each term other than the two pure fourth-degree terms contains between one and three R factors; its absolute integral is bounded by one of (5). Use (1), (3), and (4). QED.

For ordinary Sidon sets with k/sqrt(L) tending to one, hypothesis (U) holds. One self-contained proof is the difference-measure argument in the [accompanying continuum note](../2350/CONTINUUM_BARRIER.md): every subsequential weak limit has an L^2 density f on [0,1] with integral f^2<=1; mass one forces f=1 almost everywhere. Triple-sum avoidance is unnecessary for this conclusion. The source theorem in Section 7 supplies another route.

Thus for every near-maximal Sidon sequence,

    integral |R|^4 = (4/3+o(1))L.                        (11)

This disproves any proposed implication from extremal Sidonicity or its Fourier uniformity to integral |R|^4=o(L).

Moreover integral |R|^4 <= ||R||_infinity^2 integral |R|^2, so (2) and (9) give

    ||R||_infinity
       >= (sqrt(2c-(2/3)c^3)+o(1))L^(1/4).             (12)

At c=1 the leading constant is 2/sqrt(3).

For comparison, a conventional telescoping estimate for the four-variable functional is

    |T(F)-T(G)| <= C ||R||_infinity L^(3/4).             (13)

Here T(H)=integral H^3 conjugate(H). To verify (13), each telescoping term is one R factor times three factors, each F or G. Hölder bounds the remaining integral by the corresponding L^3 norms; interpolation gives ||F||_3^3 <= ||F||_2 ||F||_4^2 = O(L^(3/4)), and G satisfies the same upper bound. This estimate would certify o(L) error only from ||R||_infinity=o(L^(1/4)), which (12) makes impossible. This is an obstruction to that absolute-value estimate, not to every possible Fourier proof.

## 4. The missing signed phase condition, with exact threshold

For c in (0,1], define

    E_R = integral |R|^4,
    Psi_L = Re integral R^3 conjugate(R) / E_R.

By (9), E_R>0 for all sufficiently large L. Writing R=|R| exp(i theta) shows that Psi_L is the |R|^4-weighted average of cos(2 theta). Thus the norm-only estimate is merely -1<=Psi_L<=1.

If T(B_L)=0, (9)-(10) force

    Psi_L -> -c^2/[4(3-c^2)].                            (14)

In particular c=1 requires -1/8, not a phase value near the extremal lower bound -1.

**Conditional theorem 3.** Suppose (U), T(B_L)=0, and for a fixed kappa>=0,

    Re integral R^3 conjugate(R)
        >= -kappa integral |R|^4 + o(L).                (H_kappa)

Then

    c^2 <= 12 kappa/(1+4 kappa).                        (15)

**Proof.** Equations (9)-(10) and (H_kappa) imply

    0 >= c^4/6 - kappa(2c^2-(2/3)c^4).

Divide by c^2 and rearrange. QED.

In particular, (H_(1/14)) would give c<=sqrt(2/3) in this uniform-profile subclass. The coefficient 1/14 is exactly the threshold in this conditional argument: substituting c^2=2/3 into (14) gives -1/14. A bound with any kappa<1/8 would already rule out a near-maximal avoiding sequence c=1. Neither phase inequality is proved here. Norm information alone does not imply it, as Section 6 makes explicit. Nonuniform limiting profiles also remain outside this conditional theorem.

## 5. Three carry coefficients, rather than just their sum

For integers v, put

    T_v(B)=#{(a,b,c,d) in B^4:a+b+c-d=v}.

The proof of Lemma 1 also gives, uniformly in v,

    T_v(B) = (k/L)^4 T_v([L])
               + integral R^3 conjugate(R)e(-v alpha) + o(L). (16)

The uniformity follows because the extra character has absolute value one. The integral is real by conjugate symmetry. For v=jL, j=0,1,2, direct bounded-composition counting gives

    T_0([L]) = binom(L,3),
    T_L([L]) = (2L^3-2L)/3,
    T_(2L)([L]) = binom(L+2,3).                          (17)

These add to L^3 exactly. Their leading coefficients are (1/6,2/3,1/6).

In the modular near-perfect setting of the [accompanying carry note](../2350/MODULAR_CARRY_PROOF.md), with modulus L and k~sqrt(L), the exact modular identity gives sum_{j=0}^2 T_(jL)(B)=(1+o(1))L. Indeed its hole count is o(L), and its zero-sum correction is O(k), since strong Sidonicity bounds each ordered sum multiplicity by two. Thus the three residual Fourier coefficients in (16) have sum o(L). If the zero carry is absent, its residual coefficient must be -L/6+o(L), and the other two must compensate by +L/6+o(L) in total.

This is an exact leading description of the needed carry bias. It supplies no positivity or cancellation estimate excluding that bias. In particular it does not convert modular coincidences into zero-carry integer coincidences.

### Half-integer radii

The main asymptotic statements extend without a factor-of-two loss when all radii lie in the single coset Z+1/2. If B is a subset of (0,L] intersected with Z+1/2, put A=B+1/2, so A is an integer Sidon subset of [M] with M=L+O(1). The equation a+b+c=d in B becomes a'+b'+c'-d'=1 in A. Use (16) with v=1; the dense-model count is T_1([M])=binom(M+1,3), with the same leading coefficient 1/6. Equivalently, use the actual half-integer Fourier residual e(-alpha/2)R_A(alpha): its magnitude moments are unchanged, and its signed quartic integral is integral R_A^3 conjugate(R_A)e(-alpha). This signed quartic is periodic even though the residual itself is antiperiodic. Thus (9), (12), and the phase thresholds in (14)-(15) retain their constants, with the stated phase factor understood. Scaling the lattice by two is unnecessary.

## 6. An explicit norm-and-phase countermodel

The following construction disproves the analytic implication that the leading scalar second/fourth moments, small supremum residual, the correct zero-frequency mass, and conjugate symmetry force a positive cL four-variable functional. It does not impose nonnegative Fourier coefficients, indicator coefficients, or Fourier support in [L]. Those additional arithmetic constraints may still matter decisively.

Represent T by [-1/2,1/2). Let

    E = {alpha:1/8<=|alpha|<=1/2},   measure(E)=3/4,
    a = 2/sqrt(3),
    G_L = L^(-1/2) D_L,
    R_(L,theta)(alpha)
       = a L^(1/4) 1_E(alpha) exp(i theta sign(alpha)),
    F_(L,theta) = G_L + R_(L,theta).

Define R to be zero at the endpoint of the coordinate interval if needed; changing a point changes no integral. Then F(-alpha)=conjugate(F(alpha)) almost everywhere, F(0)=sqrt(L), and

    ||R||_infinity = (2/sqrt(3))L^(1/4),
    integral |R|^2 = sqrt(L),
    integral |R|^4 = (4/3)L,
    integral R^3 conjugate(R) = (4/3)L cos(2 theta).     (18)

Since E stays a fixed distance from zero, G_L=O(L^(-1/2)) on E. Every mixed quartic term is therefore O(L^(1/4)), uniformly in theta. The second-moment mixed term is O(L^(-1/4)). Consequently

    integral |F_(L,theta)|^2 = sqrt(L)+1+O(L^(-1/4)),
    integral |F_(L,theta)|^4 = 2L+O(L^(1/4)),
    integral F_(L,theta)^3 conjugate(F_(L,theta))
       = L/6 + (4/3)L cos(2 theta) + O(L^(1/4)).        (19)

The last functional is real and continuous in theta. At theta=0 it is positive for sufficiently large L; at theta=pi/2 it is negative. The intermediate value theorem therefore gives theta_L for which it is exactly zero. Equation (19) then implies cos(2 theta_L)=-1/8+O(L^(-3/4)).

This countermodel matches all the leading scalar moments in (1), (2), (9), and (11), has the correct zero-frequency mass, and has stronger supremum uniformity than the published sufficient theorem. Its L^2 total differs from the exact indicator identity by only O(1), and its fourth moment differs by o(L); exact indicator identities and nonnegative coefficient structure are not claimed. The model proves a sharply scoped failure of the norm-only implication, not a failure of every inequality using Sidonicity. It also saturates the leading lower bound (12) at c=1.

### 6.1. The obstruction persists for real coefficient polynomials on [L]

One can additionally impose real Fourier coefficients and frequency support [L], provided the coefficient nonnegativity/indicator requirement is still omitted. Here is a finite-polynomial construction.

Choose x in (4/5,81/100) such that, on putting

    y = 1/(36x^3),      z = 1-x-y,

one has x^2+y^2+z^2=2/3. Such an x exists by continuity: the left side minus 2/3 is -164639/66355200 at x=4/5 and 1273693561750021/114383962274805000 at x=81/100. Throughout this interval y,z>0. Set a=sqrt(x), b=-sqrt(y), d=sqrt(z), and

    P(alpha)=a e(alpha)+b e(3alpha)+d e(10alpha).

The six unordered pair sums from {1,3,10} are distinct. Its only triple-to-single equality is 1+1+1=3. Therefore

    integral |P|^2=1,
    integral |P|^4=2-(x^2+y^2+z^2)=4/3,
    integral P^3 conjugate(P)=a^3 b=-1/6.                (20)

For L>=10, define

    F_L = (L^(-1/2)-P(0)L^(-3/4))D_L + L^(1/4)P.

This is the Fourier transform of a real, signed sequence supported in [L], and F_L(0)=sqrt(L) exactly. Relative to G_L=L^(-1/2)D_L its residual is O(L^(1/4)) in supremum norm. The geometric-series bounds, or the same mixed-term estimate as in Section 2, give

    integral |F_L|^2 = (1+o(1))sqrt(L),
    integral |F_L|^4 = (2+o(1))L,
    integral F_L^3 conjugate(F_L)=o(L).                 (21)

The last functional can be made exactly zero as well. Replace b by b+delta in P and use the resulting P_delta(0) in the dense coefficient above. Uniformly for delta near zero, the last line of (21) refines to

    integral F_(L,delta)^3 conjugate(F_(L,delta))
        = a^3 delta L + O(L^(3/4)).                     (22)

For completeness, the pure polynomial term equals L(-1/6+a^3 delta). The pure dense term equals L/6+O(L^(3/4)); every mixed term is O(L^(3/4)), using integral |D_L|^p=O_p(L^(p-1)) for p>1 and integral |D_L|=O(log L). The constants are uniform for delta in a fixed small interval. Evaluating (22) at delta=+/-M L^(-1/4), with fixed sufficiently large M, gives opposite signs. Continuity supplies delta_L=O(L^(-1/4)) with exact zero. All leading norm identities in (21), and integral |F-G|^4=(4/3+o(1))L, survive this perturbation.

The coefficient at frequency 3 is negative and has order L^(1/4). Thus this remains a signed-function countermodel, not a nonnegative measure or a Sidon set. It shows that even correct Fourier support and realness do not repair the scalar-norm implication; the missing information has to use additional coefficient/occupancy structure or signed phase control.

## 7. Primary-source check and rate discipline

Source inspected: Miquel Ortega and Sean Prendiville, “Extremal Sidon Sets are Fourier Uniform, with Applications to Partition Regularity,” Journal de théorie des nombres de Bordeaux 35 (2023), 115–134, https://doi.org/10.5802/jtnb.1239 ; journal PDF https://jtnb.centre-mersenne.org/item/10.5802/jtnb.1239.pdf .

With the Fourier normalization used here, Theorem 1.2, printed page 116, gives

    ||R||_infinity << L^(1/2)
        ( |k/L^(1/2)-1| + L^(-1/6) )^(1/2).

Theorem 6.3, printed page 128, improves the L^(-1/6) term inside the square root to L^(-1/4). Thus k/sqrt(L)->1 implies ||R||_infinity=o(sqrt(L)). If additionally |k-sqrt(L)|=O(L^(1/4)), the latter theorem yields O(L^(3/8)), not O(L^(1/4)) or O(1). Theorem 1.15 explicitly assumes at least five variables and is not a theorem about a+b+c=d.

Only this short source statement is imported. The quartic decomposition, residual lower bound, conditional phase threshold, and countermodel in Sections 1–6 are proved above. The [continuum note](../2350/CONTINUUM_BARRIER.md), [weighted reflected-core proof](../2350/WEIGHTED_PROOF.md), and [modular-carry proof](../2350/MODULAR_CARRY_PROOF.md) were also read for context. No claim of priority or exhaustive literature review is made.

## 8. Residual and verification

The unresolved issue is an arithmetic lower bound on the signed minor-frequency correlation, rather than smallness of its absolute fourth moment. The latter is impossible at this endpoint. Equation (H_(1/14)) is an explicit sufficient missing hypothesis for the uniform-profile sharp constant, while (14) states exactly what an avoiding near-maximal sequence would have to realize. Neither is promoted to an established property of Sidon sets.

The authored diagnostic program checks the three exact interval carry polynomials against direct bounded-composition sums; checks the exact Sidon second/fourth moments and the full finite polynomial expansions on a short fixed list of example sets; and checks the countermodel constants, polynomial root bracket, and conditional threshold by exact rational arithmetic. It performs no broad finite search, and its checks are diagnostics rather than proofs of the asymptotic statements.
