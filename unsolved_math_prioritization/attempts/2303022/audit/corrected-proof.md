# Partial results and unresolved sharpness

## 1. Exact scope

Write U = {z in C : |z| < 1} and T = boundary U. Let E be relatively closed in U,
with 0 outside E and with positive distance from 0. Every open radius
{r exp(i theta): 0 < r < 1} must intersect E. The relevant domain is the component
D_E of U minus E containing 0. The target additionally describes T as its outer
boundary. Our upper estimates hold even if some of T is inaccessible.

Let B be planar Brownian motion, tau_T its first exit time from U, and tau_E its
first hit on E. Put

    h(E) = P_0(tau_E < tau_T),    q(E) = P_0(tau_T < tau_E).

Thus q(E) = 1 - h(E), and the target is S = sup_E q(E). This interpretation
agrees with Perron harmonic measure and handles irregular obstacles. Compact
sets E contained strictly in U are included. No connectivity of E is assumed.
We use standard Brownian/harmonic-measure correspondence, the strong Markov
property, conformal invariance under a nonconstant analytic map with its usual
time change, and the planar Harnack inequality.

The original typography distinguishes the domain D_E from the unit disk U.
It must not be read as placing the inner boundary inside the open domain itself.
The exact primary statement and its update were checked in Hayman--Lingham,
Problem 3.22, printed page 67 of arXiv:1809.07200v2.

## 2. Monotonicity, compact selectors, and the connector obstruction

**Lemma 2.1.** If E is contained in F, then h(E) <= h(F), equivalently
q(F) <= q(E).

Proof. A path that avoids F until exiting U also avoids E. Take probabilities.
This proof does not assume regularity or connectedness. End proof.

Consequently, finding a connected F containing E and applying an upper bound
to q(F) gives no upper bound on q(E).

**Lemma 2.2.** Suppose a compact E contained in U minus {0} intersects every
radius exactly once. Then q(E) = 0.

Proof. Radial projection p:E -> T, p(z)=z/|z|, is a continuous bijection from a
compact space to a Hausdorff space. Its inverse is continuous. Consequently
E={r(theta) exp(i theta)} for a positive continuous function on T, with maximum
less than one. The parametrization is injective on T, so E is a Jordan curve.
Its bounded complementary region is precisely the star-shaped set with radial
coordinate less than r(theta), and contains 0. Every continuous path from 0
to T crosses E. Brownian paths are continuous, proving the assertion. End proof.

Compactness is essential to this argument. A measurable radial selector need
not have a closed graph. We use such selectors as measures in Section 4, but
never assert that they are admissible replacement obstacles.

Here is an explicit strict connector obstruction. Set

    E_1 = {(1/4) exp(i theta): 0 <= theta <= pi},
    E_2 = {(1/2) exp(i theta): pi <= theta <= 2pi},
    E = E_1 union E_2.

This compact two-arc set meets every radius and avoids 0. Its complement is
connected (two disjoint nonseparating Jordan arcs); in particular the path
constructed in Section 5 connects 0 to the outer annulus, so its origin component
has all of T as outer boundary. Section 5 proves q(E)>0 quantitatively.

Adjoin the real intervals [1/4,1/2] and [-1/2,-1/4]. The resulting set F is a
simple Jordan curve surrounding 0, whence q(F)=0. Thus even this elementary
connectedification can strictly change the objective, all the way to zero.
F is a diagnostic obstruction to the proposed reduction; it is not asserted to
retain the target's outer-boundary condition.

## 3. The connected benchmark and the rectangle control

For the application below, we use only the following interior-obstacle
consequence of the published Marshall--Sundberg connected-set theorem: for a
compact continuum K contained in U minus {0},

    h(K) >= C_conn * |p(K)|/(2pi).

Here h(K) has the strict-before-T hitting-time definition of Section 1. The
source's broader closed-disk theorem uses a boundary-harmonic-measure
convention; we do not assert it with that strict hitting-time definition for
sets meeting T. The source theorem's sharp constant C_conn equals the harmonic
measure of the two long sides of a 3:1 rectangle at its center. The primary
author abstract specifies approximately 0.977126698498665669. This theorem is
a cited premise, not reproved here. Its connectivity hypothesis is
indispensable to our use.
The 2018 update points to the earlier connected extremal result. Betsakos's
Problem 1 separately asks for the infimum for a union of two curves.

We independently compute the rectangle value. In
R=(-3,3) x (-1,1), let v be harmonic with boundary values 1 on the vertical
short sides and 0 on the horizontal long sides. Separation of variables gives

    v(x,y) = (4/pi) sum_{n>=0} [(-1)^n/(2n+1)]
               cos((2n+1) pi y/2)
               cosh((2n+1) pi x/2) / cosh((2n+1) 3pi/2).

On compact subsets this series and its derivatives converge normally. It
satisfies Laplace's equation; on the interiors of the sides it has the stated
boundary values by the Fourier cosine expansion of the constant function 1
on (-1,1). The corner values do not affect harmonic measure. Uniqueness of the
bounded Dirichlet solution identifies v. At the center,

    q_rect = (4/pi) sum_{n>=0} (-1)^n / ((2n+1) cosh((2n+1) 3pi/2)).

The summands' positive magnitudes strictly decrease to zero. The alternating
series remainder lies between zero and the first omitted term, with its sign.
The exact rational script uses Machin's arctangent identity for pi, positive
Taylor bounds for exp, and four terms plus the fifth-term remainder to prove

    0.0228733015013343 < q_rect < 0.0228733015013344.

Therefore C_conn=1-q_rect under the cited geometric theorem. No identification
of S with q_rect is made. A correct rectangle calculation cannot replace the
missing theorem for disconnected E.

## 4. A self-contained non-sharp universal upper bound

**Theorem 4.1.** Every obstacle in Section 1 satisfies

    h(E) >= 1/16,     q(E) <= 15/16.

This estimate is deliberately non-sharp; no improvement on Hall-type literature
is claimed. The purpose is a checkable universal partial result.

### 4.1 Compact obstacles near the boundary

First let K be compact with 3/4 <= |w| < 1 for every w in K. Let A=p(K),
represented by angles modulo 2pi. Choose the smallest radius r(theta) with
r(theta) exp(i theta) in K for theta in A. This is measurable: along a convergent
sequence of angles, a convergent subsequence of minimizing radii has its limit
in the limiting compact fiber, proving lower semicontinuity on A. Compactness
also bounds r away from 1.

The disk Green function, in the logarithmic normalization, is

    g(z,w) = log |(1 - conjugate(w) z)/(z-w)|.

Define the positive potential

    V(z) = integral_A g(z,r(theta) exp(i theta))/[-log r(theta)] dtheta.

The source measure is finite and supported on K. Therefore V is positive and
harmonic on U minus K. Also V(0)=|A|, and V tends uniformly to zero at T because
K is compactly contained in U. We now prove the global bound V(z)<=32pi.

Rotation lets us take z=s>=0 and use the angular difference phi in [-pi,pi].
Let t=1-r and a=1-s. The identity

    g(s,r exp(i phi))
      = (1/2) log(1 + (1-s^2)(1-r^2)/|s-r exp(i phi)|^2)

and -log r >= 1-r give, if s<=1/2,

    g/[-log r]
      <= (1-s^2)(1+r)/(2 |s-r exp(i phi)|^2)
      <= 16.

Indeed |s-r exp(i phi)| >= r-s >=1/4 and the numerator factor
(1-s^2)(1+r)/2 is at most one. Integration gives V<=32pi.

For s>1/2, put c=3/(2pi^2). Since r>=3/4 and
sin(|phi|/2)>=|phi|/pi,

    |s-r exp(i phi)|^2 >= (a-t)^2 + c phi^2,
    g/[-log r] <= [1/(2t)] log(1+4at/((a-t)^2+c phi^2)).

Three cases give integrable envelopes:

    t<=a/2:       g/[-log r] <= 2a/(a^2/4+c phi^2),
    t>=2a:        g/[-log r] <= 2a/(a^2+c phi^2),
    a/2<t<2a:     g/[-log r] <= (1/a) log(1+8a^2/(c phi^2)).

At phi=0 the last envelope is infinite, which is harmless on a null set.
The sum of these three nonnegative envelopes bounds the kernel for any
measurable choice of t. Their integrals over the entire real line are,
respectively, 4pi/sqrt(c), 2pi/sqrt(c), and 4sqrt(2)pi/sqrt(c).
For the last identity use
integral_R log(1+b^2/x^2) dx=2pi b for b>0; differentiation in b and the value
at b=0 verify it. Thus

    V(z) <= (6+4sqrt(2)) pi^2 sqrt(2/3) < 32pi.

For an explicit rational check of the last inequality use sqrt(2)<10/7,
sqrt(2/3)<5/6, and pi<22/7:

    (6+4sqrt(2)) pi sqrt(2/3)
       < (82/7)(22/7)(5/6) = 4510/147 <32.

Now stop Brownian motion in U minus K. The bounded harmonic martingale V(B)
converges at its exit; on exit through T its limit is zero, while on hitting K
its limit is at most 32pi. No continuity at irregular points of K is needed
for this upper bound. The stopped bounded martingale consequently gives

    |A|=V(0) <= 32pi h(K),

so h(K)>=|A|/(32pi).

### 4.2 Moving a compact obstacle near the boundary without a false radial shove

For a general compact K in U minus {0}, choose a positive integer n large enough
that min_{w in K}|w|^(1/n)>=3/4. Let

    K'={z in U : z^n in K}.

This is a full inverse image, not independent radial movement of obstacle
points. Brownian conformal invariance under the analytic map z -> z^n gives
h(K')=h(K). More explicitly, the image Brownian path with its analytic time
change hits K exactly when the original path hits K', and hits T exactly when
the original path hits T. The branch point at 0 changes the clock, not the exit
distribution. Equivalently compose the bounded harmonic hitting function with
z^n and use uniqueness of harmonic measure.

Radial projection satisfies p(K')={exp(i theta):exp(i n theta) in p(K)}.
The n-fold map preserves normalized angular Lebesgue measure, so
|p(K')|=|p(K)|. Applying the preceding estimate to K' proves

    h(K) >= |p(K)|/(32pi)

for every compact K in U minus {0}.

### 4.3 Relatively closed obstacles

For E as in Section 1, let K_m=E intersect {|z|<=1-1/m}. These compact sets
increase, and their angular projections increase to T because every radius
meets E strictly inside U. Hence |p(K_m)| tends to 2pi. Monotonicity gives
h(E)>=h(K_m)>=|p(K_m)|/(32pi). Take the limit. This proves Theorem 4.1.

The proof solves only a non-sharp inequality. It does not identify an extremizer
or prove that any of its kernel-envelope inequalities can be saturated together.

## 5. An explicit escape construction with a rigorous positive bound

Use the two arcs E from Section 2 and let q(z) be their escape probability from
z. It is a positive harmonic function on their complement. At z*=3i/4,

    q(z*) >= P_{z*}(hit T before {|z|=1/2})
            = log(3/2)/log 2 > 1/2.

The radial annulus formula follows by applying optional stopping to log|z|.
The strict comparison follows from (3/2)^2>2.

Connect 0 to z* by the following path:

1. The segment from 0 to -3i/8.
2. The right semicircle of radius 3/8, from -3i/8 to 3i/8.
3. The segment from 3i/8 to 3i/4.

Every point of this path has distance at least 1/8 from E and at least 1/4
from T. For the semicircle, radial distance to either obstacle circle is 1/8.
On the lower segment E_1 is in the upper half-plane and E_2 is at radius 1/2;
on the upper segment E_1 is at radius 1/4 and E_2 is in the lower half-plane.
These observations verify the claimed distances, including endpoints.

Partition each straight segment into six pieces and the semicircle into
nineteen equal angular pieces. Every consecutive distance is at most 1/16:
the straight lengths are exactly 1/16, and the arc-piece length is 3pi/152<1/16
because 6pi<19. There are 31 links. The open ball of radius 1/8 centered at
any link's starting point is contained in U minus E. The planar Harnack
inequality therefore gives

    q(z_j) >= (1/3) q(z_{j+1}).

Iterating and using the annulus comparison proves

    q(E)=q(0) > 1/(2 * 3^31) >0.

This quantitatively validates the strict connector obstruction. It is a weak
lower bound for one explicit geometry, not a claim of near-optimality.

## 6. Finite-component probability bounds and the overlap gap

Suppose E=union_{j=1}^k K_j, where each K_j is a compact continuum contained
in U minus {0}, and the union meets every radius. Define A_j to be the event that ordinary
Brownian motion in U (not killed on other K_i) hits K_j before T. Then

    h(E)=P(union_j A_j),   h(K_j)=P(A_j).

By the pointwise count inequality sum_j 1_{A_j} <= k 1_{union A_j},

    h(E) >= (1/k) sum_j h(K_j).

The connected theorem in Section 3 and the projection cover give

    sum_j h(K_j) >= [C_conn/(2pi)] sum_j |p(K_j)| >= C_conn.

Therefore, conditional only on that stated published theorem,

    h(E)>=C_conn/k,     q(E)<=1-C_conn/k.

For k=1 this recovers the connected inequality. For k=2 it is about
h(E)>=0.488563349249..., but does not determine the two-curve infimum. For
unbounded k it degenerates, whereas Section 4 remains uniform.

The probability sum cannot simply replace the union probability. Even E_1 and
E_2 in Section 2 have angular projections disjoint except for two endpoints,
yet P(A_1 intersect A_2)>0. To see this, stop at the first hit on E_1 before T.
The probability of subsequently hitting E_2 before T is a strictly positive
harmonic function at every point of E_1, by the maximum principle for the
nonpolar arc E_2. Since P(A_1)>0, the strong Markov property gives a positive
probability of hitting E_1 and later E_2. Thus disjoint angular coverage does
not remove Brownian-event overlap. Controlling this overlap sharply is the
missing step in this approach.

## 7. Exploratory PDE route and exact remaining target

A finite-difference model was built in logarithmic coordinates x=-log|z|,
theta modulo 2pi. Laplace's equation becomes u_xx+u_thetatheta=0. The outer
boundary x=0 has value one; the two arcs have value zero at x=log2 and
x=2log2 on the corresponding semicircles. The infinite inner cylinder was
truncated at x=8log2 with a reflecting boundary condition.

Three meshes produce approximate values 0.00363386, 0.00421646, and
0.00451445. The empty-obstacle and full-circle controls give one and zero,
respectively. These are finite-difference values, not certified continuum
values. In particular, small linear-system residuals control algebraic solve
error only. There is no validated endpoint discretization error, infinite-
cylinder truncation bound, or global optimization over obstacles. The increasing
values are not proved one-sided bounds. No inference about S follows from them.

**Unresolved target.** Find a sharp constant S_* and prove q(E)<=S_* for every
relatively closed admissible radial-covering E, with a matching admissible
extremizing family. None of Sections 2--7 supplies both directions. Neither a
reduction to one continuum nor the passage from boundedly many components to
arbitrary closed E has been justified. The five approaches end at these gaps.
