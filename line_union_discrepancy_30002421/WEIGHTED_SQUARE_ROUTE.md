# Weighted square discrepancy: a large-square transfer

Date: 2026-10-20 UTC.

## Result

The side-length factor in the vertical-line lift can be controlled. In fact, for every finite signed Borel measure mu on the closed unit square,

    sup_S |mu(S)| <= 6 sup_{side(S) >= 1/10} |mu(S)|,
    sup_S side(S) |mu(S)| >= (1/60) sup_S |mu(S)|.

All tests are closed axis-parallel squares contained in the unit square. This includes signed measures with arbitrary boundary mass. For a point set P in the closed unit square, apply this to mu = sum_{p in P} delta_p - N Lebesgue. In the notation

- Delta(P) = sup_S |#(P intersect S) - N area(S)|;
- Delta_large(P) = sup_{side(S) >= 1/10} |#(P intersect S) - N area(S)|;
- W(P) = sup_S side(S) |#(P intersect S) - N area(S)|.

Here S ranges over closed axis-parallel squares contained in [0,1]^2. Then

    Delta(P) <= 6 Delta_large(P),
    W(P) >= Delta(P)/60.

Consequently the known planar square lower bound implies

    W(P)/N >= c log(N)/N

for an absolute positive c. An independent boundary-point reduction is also given below, so the application does not depend on an implicit endpoint convention in the cited ordinary discrepancy theorem.

This resolves the extra side-weight issue for parallel vertical lifts. It makes no assertion for arbitrary directions of the lines or for rotated cubes.

## 1. A four-square indicator identity

Use a consistent half-open convention initially. Let

    Q_s(z) = z + [0,s)^2,

and take t > s > 0. The following identity holds pointwise:

    1_{Q_s(z)} + 1_{Q_s(z+(t,t))}
      = 1_{Q_{t+s}(z)}
        + 1_{Q_{t-s}(z+(s,s))}
        - 1_{Q_t(z+(0,s))}
        - 1_{Q_t(z+(s,0))}.                 (1)

To verify it, translate z to the origin and split both coordinate axes into the three intervals [0,s), [s,t), [t,t+s). The large square contributes every cell once; the central square contributes the central cell once more; the two subtracted squares remove every cell except the southwest and northeast s by s cells. The central cell is subtracted twice. Thus exactly the two asserted small squares remain.

The identity is invariant under reflections of either coordinate. In a reflected identity the endpoint convention is reflected as well.

For a signed measure mu, denote the right-hand side after integration by E_t(z). Equation (1) says

    E_t(z) = mu(Q_s(z)) + mu(Q_s(z+(t,t))).

Now let z_0=z, z_1=z+(t,t), and z_2=z+(2t,2t). Apply (1) to the pairs (z_0,z_1), (z_1,z_2), and (z_0,z_2). Then

    2 mu(Q_s(z_0)) = E_t(z_0) + E_{2t}(z_0) - E_t(z_1).      (2)

Every E is a signed sum of four square measures. Hence, whenever all twelve squares are admissible large squares,

    |mu(Q_s(z_0))| <= 6 sup_{large squares Q} |mu(Q)|.         (3)

No extremal rectangle, packing argument, or scale iteration is needed.

## 2. Fitting all auxiliary squares inside the unit square

Fix a target square S of side s < 1/10, and choose t in the interval (1/5, 21/100). The freedom to choose t will handle all boundary masses below. In each coordinate independently, choose the direction in which the free gap between S and the boundary of [0,1]^2 is larger. This gap is at least

    (1-s)/2 > 9/20 > 2t. (Indeed, 2t < 42/100.)

Reflect either coordinate, if needed, so that both chosen directions are positive. The three translated small squares S, S+(t,t), and S+(2t,2t) then fit inside the unit square. The entire outer square of side 2t+s that contains them also fits, and all auxiliary squares from (2) lie inside that outer square.

Their side lengths belong to

    {t-s, t, t+s, 2t-s, 2t, 2t+s}.

Every one is strictly greater than 1/10. Thus (3) applies once endpoint conventions are handled. If the original square has side s >= 1/10, its measure is already bounded by the large-square supremum. Taking the supremum gives the claimed factor 6.

Since every large square has side at least 1/10,

    W >= (1/10) Delta_large >= Delta/60.

## 3. Endpoint conventions for arbitrary finite signed measures

Let mu be a finite signed Borel measure on the closed unit square and |mu| its total variation. The set of x-coordinates whose vertical lines have positive |mu| mass is countable. The corresponding set of horizontal coordinates is also countable.

First take a target closed square S of side s<1/10 whose internal boundary lines have zero |mu| mass. Ambient boundary lines are allowed to carry mass. Orient the coordinates toward the larger free gaps as in Section 2. In these oriented coordinates, S has a starting corner z=(a,b), and its far edges, at a+s and b+s, are strictly inside the ambient square. Only the starting edges can coincide with ambient boundaries.

All auxiliary boundary coordinates in (2) have one of the forms

    a + c t + d s,    b + c t + d s,
    where c is in {0,1,2} and d is in {0,1}.

The c=0 coordinates are target boundary coordinates. For each coordinate with c>0, the forbidden t-values that place it on a positive-|mu|-mass line form a countable set. Choose t in (1/5,21/100) outside their finite union. All auxiliary nonambient boundary lines then have zero |mu| mass.

The strict fit from Section 2 guarantees that every far edge of every auxiliary square is internal. Thus every potentially massive ambient edge is a starting edge, which the oriented half-open convention includes. It follows that each auxiliary oriented-half-open square and its closed version have exactly the same mu measure. The same is true for the target. Therefore the pointwise half-open identity proves (3) for the closed-square integrals, even when mu has ambient-boundary mass.

For an arbitrary target closed square S of side s<1/10, choose slightly larger contained squares S_j that contain S, converge to S, have side less than 1/10, and have all internal boundary lines outside the two countable exceptional sets. For an explicit construction, enlarge an interval [a,a+s] symmetrically to [a-epsilon/2,a+s+epsilon/2] when both endpoints are internal; replace it by [0,s+epsilon] when a=0; and by [1-s-epsilon,1] when a+s=1. Apply this independently to both coordinates with the same epsilon. All internal endpoints then move with nonzero speed. For sufficiently small epsilon the squares are contained, and epsilon can avoid the countably many values putting an internal endpoint on an exceptional line. The indicators converge pointwise to 1_S. Dominated convergence for |mu| gives mu(S_j) -> mu(S).

Apply (3) to S_j and pass to the limit. Squares of side at least 1/10 need no reduction. This proves

    sup_{closed S} |mu(S)| <= 6 sup_{closed S, side(S)>=1/10} |mu(S)|

for every finite signed Borel measure, with no endpoint exception.

## 4. Boundary points do not spoil the lower bound

Let P be any N-point set in [0,1]^2, let k points lie on the ambient boundary, and let P_0 be the remaining n=N-k interior points. Keep unnormalized weighted discrepancy W_N(P) as above, with the reference coefficient N.

Closed interior squares [epsilon,1-epsilon]^2, as epsilon decreases to zero, contain exactly P_0 for sufficiently small epsilon. Their weighted discrepancy tends to k. Hence

    W_N(P) >= k.                                             (4)

Every square discrepancy for P_0 can be approximated by squares strictly inside the ambient unit square, preserving the P_0 count and converging in area and side length. Such squares contain no boundary point of P. For every such square S, with side s,

    s |#(P intersect S) - N s^2|
      = s |#(P_0 intersect S) - n s^2 - k s^2|
      >= s |#(P_0 intersect S) - n s^2| - k.

Taking suprema yields

    W_N(P) >= W_n(P_0) - k.                                 (5)

Combining (4) and (5),

    W_N(P) >= max{k, W_n(P_0)-k} >= W_n(P_0)/2.              (6)

If n >= N/2, the interior result and the known square discrepancy lower bound yield W_N(P) >= c log N for all sufficiently large N. If n < N/2, (4) is stronger, giving W_N(P) > N/2. Thus, after reducing the universal constant to cover the finitely many small N,

    sup_{closed S} side(S) |#(P intersect S)/N - area(S)|
        >= c log(N)/N.

For N=1 the logarithmic right-hand side is zero. For any fixed N>=2, a positive uniform lower bound needed for the finite adjustment follows, for example, by partitioning a fixed interior square into more than N equal subsquares and selecting an empty one; shrink its boundary if necessary. This makes the final constant adjustment legitimate.

## 5. Arbitrary reference coefficient

The point-count lower bound remains usable when the reference coefficient is not the number of points. For any real T, let

    W_T(P) = sup_S side(S) |#(P intersect S) - T area(S)|.

The full closed unit square is an admissible test, so

    |N-T| <= W_T(P).

For every test square, its side times area is at most 1. The triangle inequality therefore gives

    W_N(P) <= W_T(P) + |N-T| <= 2 W_T(P).

Consequently W_T(P) >= c log(N) with a universal c for every real T. This formulation is useful after restricting a line configuration to an inner cube, where the total reference mass is inherited from the larger ambient cube.

## 6. Consequence for full vertical-line lifts

For distinct p in P, let

    A_P = union_{p in P} ({p} x [0,1]).

The set has total length N. A closed axis-parallel cube Q=S x I of side s satisfies

    H^1(A_P intersect Q)/N - volume(Q)
      = s (#(P intersect S)/N - area(S)).

Taking suprema and using the result above proves

    D_axis(A_P) >= c log(N)/N.

The square lower bound was not silently identified with the weighted quantity: equations (1)-(3) supply the missing transfer. This is only the coordinate-parallel subcase of the line-union problem.

## Sources and attribution boundary

The locally derived argument in this note is the elementary twelve-square large-scale transfer (1)-(3), with its geometric fit and boundary handling. No historical novelty claim is intended.

For the pre-existing ordinary square discrepancy lower bound, see Jiří Matoušek, Geometric Discrepancy: An Illustrated Guide, Section 6.3, Theorem 6.3, printed pages 180-182. Its proof compares ordinary square and rectangle discrepancy; its attribution is to Halász and Ruzsa. The side-weight transfer above is separate from that inspected proof.

- Inspected book PDF: https://people.fjfi.cvut.cz/vybirja2/TUM-IBC/Matousek_Geometric_Discrepancy.pdf
- Original line-union question, printed page 2891: https://ems.press/content/serial-article-files/46480?nt=1
- Official report page: https://ems.press/journals/owr/articles/12723
