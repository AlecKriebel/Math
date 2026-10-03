# Author turn 1: a uniform Poisson-road length estimate

**Scoped result, original general question unresolved; 1/5 turns used.**
The following is a credited uniform corollary of Kahn's time-diameter and
multi-scale speed arguments. The proof is written out because replacing a
fixed pair by an infinite sampled family requires a single common event;
a union bound over infinitely many endpoints would prove nothing.
Historical novelty is not claimed.

## 1. Model and statement

Use Kahn's speed-marked isotropic Poisson line model in R^d, d≥2, with speed
parameter gamma>d. A line with mark v has speed limit v. Disjoint sets in
line-space, with their marks, are independent. If V(r) is the fastest mark
among lines meeting the Euclidean ball B(0,r), then

    P(V(r)≥v) = 1−exp(−c r^(d−1) v^(−(gamma−1)))
              ≤ c r^(d−1) v^(−(gamma−1)),              (1)

for the positive normalization constant c. Kahn's Pi-paths obey these speed
limits; the assigned route is a minimum-time geodesic, not necessarily a
shortest-Euclidean-length path.

Let (z_i) be a countable family in B(0,1), on a realization where the chosen
minimum-time routes from 0 exist. For the original question, take z_i=U_i,
independent uniform points independent of the line process. Put

    M = sup_i len R(0,z_i).

**Theorem.** For every 0<q<gamma−1, E[M^q]<infinity. The bound is uniform in
the number and locations of the endpoints; it is supplied by a common
measurable envelope depending only on the line process. In particular, in
d=2 every gamma>2 gives E[M]<infinity, answering the question affirmatively
in this concrete SIRSN model.

The random family interpretation only requires measurability of the stated
countable maximum. No uncountable supremum or new jointly measurable route
version is asserted. Existence and the SIRSN construction are credited to
Kendall and Kahn; the proof below does not re-prove that construction.

## 2. One travel-time bound for all endpoints

Kahn, Theorem 3.1, applies to the connected unit ball, with no forbidden
lines and a finite ball cover. It constructs a common upper bound Tau for
the minimum travel times between every pair of its points. From the theorem's
explicit tail, there is a finite deterministic C_T such that, for n≥0,

    P(Tau > T_n) ≤ 2^(−(n+1)),
    T_n = C_T (n+1)^(1/(gamma−1)).                      (2)

Indeed, substitute epsilon=epsilon_max·2^(−(n+1)) into its equation (3),
and absorb log(1/epsilon_max)+(n+1)log 2 into C_T^(gamma−1)(n+1).
The actual unrestricted minimum-time route takes no longer than these
constructed paths. Its Euclidean excursion is not assumed to stay in the
unit ball or in the region used for the comparison construction.

Consider any Pi-path from 0 with total Euclidean length exceeding r and
travel time at most T. The initial arclength-r segment stays in B(0,r),
because its displacement from the starting point is bounded by arclength.
Its speed is at most V(r) almost everywhere; hence

    V(r) ≥ r/T.                                         (3)

This also holds if the whole path remains inside that ball. Thus, on
{Tau≤T}, the event that ANY of the routes has length >R forces (3) at every
r≤R. The same speed constraints apply to every endpoint. Their probability
need be estimated once, not multiplied by the number of endpoints.

## 3. Multi-scale record bound

Fix deterministic T>0, r_0>0 and integer m≥0. Set r_j=2^j r_0 and v_j=r_j/T.
Write

    E_m = intersection_{j=0}^m {V(r_j)≥v_j}.

For every realization in E_m, there is a sequence

    0=a_0<a_1<...<a_k≤m,       a_(k+1)=m+1,

such that, for i<k,

    v_(a_(i+1)) > V(r_(a_i)) ≥ v_(a_(i+1)−1),           (4)

and V(r_(a_k))≥v_m. To construct it, start at a_0=0; if V(r_0)≥v_m, stop.
Otherwise choose the first index j with v_j>V(r_0), put a_1=j, and repeat.
At every new index E_m guarantees V(r_(a_i))≥v_(a_i), so the indices
strictly increase. The construction terminates after at most m+1 steps.

For a fixed such sequence let B_i be event (4), i<k, and let A_i be the
lower inequality V(r_(a_i))≥v_(a_(i+1)−1), including i=k. For i>0, on B_(i−1),
all lines hitting B(0,r_(a_(i−1))) have speed <v_(a_i). Since
v_(a_(i+1)−1)≥v_(a_i), the fast line needed for A_i must be in the new
line-space layer

    [B(0,r_(a_i))] minus [B(0,r_(a_(i−1)))].

Its marked Poisson process is independent of the previously revealed
layers. Consequently, iterated conditioning on the fixed record events gives

    P(B_0 intersection ... intersection B_(k−1) intersection A_k)
    ≤ product_{i=0}^k P(A_i).                            (5)

This is ordinary independent-increment conditioning in line-space. It does
not condition on Tau or on a geodesic, which would bias the line process.
Using (1) and gamma>d gives, with

    a = 2^(gamma−1) c r_0^(d−gamma) T^(gamma−1),

    P(A_i) ≤ 2^(−(gamma−1)(a_(i+1)−a_i)) a.              (6)

There are binomial(m,k) sequences with k further record indices. Summing
(5) and (6) yields the deterministic-threshold estimate

    P(E_m)
    ≤ 2^(−(gamma−1)(m+1)) a(1+a)^m
    ≤ [2^(−(gamma−1))(1+a)]^(m+1).                     (7)

This is Kahn's record-speed argument with the events written in an
unconditional form. In particular, the conclusion we use is

    P(M>r_m, Tau≤T) ≤ P(E_m),                            (8)

not a claim that P(E_m | Tau≤T) is bounded by its unconditional value.
The source proof's displayed conditional notation is not needed for (8).

## 4. Integrate the uniform tail

Fix 0<kappa<gamma−1, and put

    a_* = 2^(gamma−1−kappa)−1 >0,
    r_0(n) = [2^(gamma−1)c/a_*]^(1/(gamma−d))
             T_n^((gamma−1)/(gamma−d)),
    m(n) = floor((n+1)/kappa).

These choices make a=a_* in (7), so (8) is at most
2^(−kappa(m(n)+1))≤2^(−(n+1)). Combining with (2) gives

    P(M > b_n) ≤ 2^(−n),
    b_n = C (n+1)^(1/(gamma−d)) 2^((n+1)/kappa),         (9)

where C is deterministic and finite. The slight replacement of 2^m by its
upper bound makes b_n nondecreasing and only weakens the estimate.

For 0<q<kappa, layer decomposition at the b_n gives

    E[M^q] ≤ b_0^q + sum_{n≥0} b_(n+1)^q P(M>b_n)
           ≤ C' + C'' sum_{n≥0}
                 (n+2)^(q/(gamma−d)) 2^(n(q/kappa−1))
           < infinity.                                (10)

Because kappa may be chosen arbitrarily close to gamma−1, the theorem
follows. The countable supremum is measurable and (9) also proves its
almost-sure finiteness. More strongly, the event used in (9) rules out every
length>b_n Pi-geodesic of time≤Tau starting at 0; this is the common envelope
interpretation. Endpoint independence is used for the original sampled
route model, not as an independence assumption inside the proof of (7).

## 5. Already-known example and exact remaining gap

Aldous's binary hierarchy has deterministic bounded stretch: Proposition
3.1 and the continuum/randomization passage in §3.7 give

    len R(x,y) ≤ sqrt(2) K_gamma |x−y|.

Thus M≤sqrt(2)K_gamma in that model. This is an immediate credited source
consequence, not a new answer for arbitrary SIRSNs.

The Poisson proof uses additional structure absent from the general axioms:
a minimum-time metric, a common stretched-exponential travel-time diameter,
and independent Poisson speed records. Ordinary SIRSN routes are not
assumed shortest for Euclidean length or for any explicitly given cost.
Finite E[D] alone does not supply any of those inputs. The general original
question remains unresolved after this first substantive turn. Subsequent
turns should seek a criterion at the countably sampled/FDD level or a genuine
SIRSN obstruction, rather than repeat the model-specific estimate.

## Sources and controls

Kahn, arXiv:1503.03976v3, Theorem 3.1 and proof, Theorem 5.1 and proof,
and Remark 5.1; source version bound by SOURCE_MANIFEST.json. Aldous (2014),
Proposition 3.1 and §3.7, for the binary hierarchy. All main mechanisms are
credited. The finite checker verifies record partitions, composition sums
and exponent relations; it is not a simulation or proof of the continuum
model's existence or the missing general assertion.
