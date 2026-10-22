# Attempt 5: multidirectional flow mixtures and why fixed mixtures do not evade rotations

Date: 2026-10-20 UTC. Queue row 1825, ID 30002421.

## Outcome

A natural counterexample search is to mix several of the exceptionally uniform oblique torus-flow chord families from Attempt 2, hoping their rotated-cube errors cancel. For any fixed finite collection of pairwise nonparallel positive algebraic directions, this construction still satisfies a logarithmic lower bound for rotating cubes. The reason is that one family can be made resonant with the test cube orientation, while all other families retain bounded unnormalized error in that same orientation.

This does not settle arbitrary multidirectional full-line unions. The number of directions may grow with L, and arbitrary line families do not inherit the uniform bounded-error estimates needed to control cancellation.

## 1. Exact admissible construction

Fix k>=2 vectors α_1,...,α_k∈R^3. Assume:

1. Every coordinate is positive and algebraic.
2. The three coordinates of each vector are Q-linearly independent.
3. Each vector has a coordinate equal to 1.
4. No two vectors are parallel.

For each integer n, form A_{j,n} from the full chords traced by tα_j modulo Z^3 for 0<=t<=n, as in Attempt 2. The start is a vertex and the end is a crossing of the coordinate with speed 1, so these are full chords, without endpoint completion. Let v_j=||α_j|| and L_{j,n}=n v_j.

Define

    A_n = union_{j=1}^k A_{j,n},
    V = sum_{j=1}^k v_j,
    L_n = nV.

Lines within each family are distinct by the irrationality argument in Attempt 2. Lines from different families have different directions, so cannot coincide. They meet at most in finitely many points, which have zero arclength. Thus L_n=nV exactly as a set, without multiplicity.

For any test cube Q, write

    E_{j,n}(Q) = H^1(A_{j,n}∩Q) − L_{j,n}|Q|.

Then the exact signed decomposition is

    H^1(A_n∩Q) − L_n|Q| = sum_j E_{j,n}(Q).       (1)

The generic inequality D(A_n)>=max_j D(A_{j,n}) is false as a matter of algebra: (1) permits cancellation. The following special construction lets us control it.

## 2. An algebraic test frame resonant with exactly one family

Choose an orthonormal frame U=(e_1,e_2,e_3) with e_3=α_1/v_1. All coordinates can be chosen algebraic. Vary e_1 in the plane perpendicular to α_1, and set e_2=e_3×e_1.

For j>1 require

    e_1·α_j != 0,  e_2·α_j != 0,  e_3·α_j != 0.             (2)

The third condition holds because the α_j have positive coordinates. Each of the first two conditions excludes finitely many directions on the circle, since α_j is not parallel to α_1. Start with an algebraic basis of the perpendicular plane and take a rational linear combination outside the finite forbidden set; normalizing and taking the cross product preserve algebraicity. Thus U can satisfy all requirements at once.

Let C_U be all cubes inside C whose edges are parallel to this one fixed frame. This is a genuine subclass of unrestricted-orientation cubes.

For j=1, two face normals are perpendicular to α_1, deliberately violating Borda's nonresonance condition. For j>1, every face normal is algebraic and has nonzero scalar product with α_j by (2).

## 3. The selected family supplies a logarithm

The proof of Attempt 4 works in ANY chosen frame whose third axis is the common line direction. It does not need to optimize the remaining in-plane rotation. Therefore, with this particular U,

    sup_{Q∈C_U} |E_{1,n}(Q)| >= c_0 log L_{1,n}             (3)

for all sufficiently large n, where c_0>0 is universal. The fixed interior cube and weighted planar square theorem give this conclusion.

## 4. Every other family contributes only a bounded error

Borda's Theorem 1, not merely its axis-parallel corollary, applies to each j>1 and to all cubes of the fixed orientation U. The normal vectors are fixed, so its constant is uniform over cube centers and side lengths. The exact flow/chord identity gives constants B_j<∞ independent of n and Q such that

    sup_{Q∈C_U} |E_{j,n}(Q)| <= B_j.                       (4)

These constants may depend on the chosen directions and the frame. That is harmless for a fixed finite family, but important if the family changes with n.

Combining (1)-(4), and approximating the supremum in (3) if it is not attained,

    L_n D_rot(A_n)
       >= sup_{Q∈C_U} |sum_j E_{j,n}(Q)|
       >= c_0 log(n v_1) − sum_{j=2}^k B_j.

For a fixed family, log(nv_1)=log L_n+O(1), and the B_j sum is fixed. Hence for all sufficiently large n,

    D_rot(A_n) >= (c_0/2) log L_n / L_n.                   (5)

The necessary threshold can depend on the fixed directions and k. Thus fixed mixtures of the Borda counterexamples fail as rotating-cube counterexamples for a rigorous reason, not merely because a numerical search found no violation.

In contrast, the axis-parallel errors of every family are bounded by Borda's Corollary 2, so their union still satisfies D_axis(A_n)=O(1/L_n) for fixed k. This supplies genuinely multidirectional examples for the axis-parallel negative result.

## 5. Exploratory finite computation

The script test_direction_mixtures.py numerically approximates the full-chord lists for the three cyclic permutations of (sqrt(2),sqrt(3),1), then evaluates clipped arclength in 1,920 sampled cubes. It uses floating-point arithmetic and a deterministic random seed. Frames include the ambient axes, one frame aligned with each family, and 24 additional random orthonormal frames. Centers and side lengths are chosen to keep the complete cube inside C.

This is exploratory evidence only. An exactly evaluated maximum over admissible sampled cubes would be a lower bound on the true supremum, never an upper bound. The reported floating-point values are not certified lower bounds: cube validity, event ordering, clipping, and rounding error have not been verified by exact or interval arithmetic. No finite sample can disprove a universal logarithmic lower bound, and no asymptotic inference is drawn from it.

For n=8,16,32,64,128,256, the sampled values of L times discrepancy for the three-direction union were approximately

    1.647, 2.260, 2.901, 4.346, 5.736, 5.488.

Their corresponding ratios to log(L) were approximately

    0.404, 0.474, 0.531, 0.706, 0.838, 0.728.

The experiment therefore found no candidate behavior that even suggested rapid suppression of the logarithm in this fixed mixture. The proof in sections 2-4, not these data, excludes that asymptotic mechanism.

Full reproducible exploratory output is in DIRECTION_MIXTURE_EXPERIMENT.json. It records chord counts, length-sum checks, maximal chord lengths, sample count, and the maximizing sampled cube parameters. The source code and data contain no external dataset or copied third-party source text.

## 6. Honest remaining gap after five attempts

The following have now been established in these notes:

- Universal axis-parallel baseline: D_axis >= 1/(8 max(1,L)^(3/2)).
- Axis-parallel logarithmic conjecture: false, by explicit admissible algebraic-flow full-chord unions with D_axis=O(1/L).
- Universal rotating-cube baseline: D_rot >= 1/(16 max(1,L)).
- Every mutually parallel family, with rotations allowed: D_rot >= c log(L)/L.
- Every fixed finite nonparallel mixture of the specified algebraic-flow families: the same logarithmic rate for large L.

The unrestricted-rotation statement for arbitrary finite unions of full lines is NOT proved or disproved. The unqualified source word “cubes” remains an orientation ambiguity. Nothing in these attempts licenses relabeling the whole original question solved merely because the axis-parallel interpretation is disproved.


## Public source

Bence Borda, *Bounded error uniformity of the linear flow on the torus*, Theorem 1 and Corollary 2: https://arxiv.org/html/1803.06968
