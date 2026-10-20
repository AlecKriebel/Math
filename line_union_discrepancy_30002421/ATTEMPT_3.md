# Attempt 3: a universal 1/L lower bound using rotating cubes

Date: 2026-10-20 UTC. Queue row 1825, ID 30002421.

## Result

Let D_rot(A) be the discrepancy over all closed Euclidean cubes contained in C=[0,1]^3, with unrestricted orientations. For every finite union A of full affine-line chords of positive total length L,

    D_rot(A) >= 1 / (16 max(1,L)).

This is an authored geometric argument. It does not rely on replacing cubes by boxes. The bound is still missing the logarithm in the proposed problem.

## Proof

Remove repeated defining lines and lines with zero-length intersection with C. Let K=[1/4,3/4]^3. If A∩K is empty, testing K gives D_rot(A)>=1/8, which suffices.

Otherwise choose a point x∈A∩K and one supporting line ell_0 through x. Choose a unit vector e_1 along ell_0. We will choose a unit vector e_2 perpendicular to e_1, and then let e_3 complete an orthonormal basis.

For each other supporting line ell_j, with direction v_j not parallel to e_1, avoid choices with e_2·v_j=0. Each such condition excludes at most two points of the circle of choices for e_2. For a line parallel to e_1 but distinct from ell_0, choose a point p_j on it and avoid e_2·(p_j−x)=0. Its nonzero perpendicular displacement likewise excludes at most two choices. There are finitely many lines, so a choice remains.

Consequently the plane H={y:(y−x)·e_2=0} contains ell_0 and contains no other supporting line. It meets each nonparallel supporting line in a single point; every other parallel line misses H.

For a>0 let

    Q_a = { x + u_1 e_1 + u_2 e_2 + u_3 e_3 :
                 |u_1|<=a/2, 0<=u_2<=a, |u_3|<=a/2 }.

One face lies in H, and ell_0∩Q_a is a segment of length a in that face. Select a in [1/8,1/6] so that no other supporting line is contained in any of the remaining five boundary planes. Only finitely many a are excluded: if a line is parallel to one such plane, containment requires one fixed coordinate value to equal a, a/2, or −a/2, each specifying at most one a; if it is not parallel, it cannot be contained in the plane.

Every point of Q_a has distance at most sqrt(3/2)a <= sqrt(3/2)/6 < 1/4 from x. Since x is at least coordinate distance 1/4 from the boundary of C, Q_a and all sufficiently small translates Q_a+t e_2 are contained in C.

For any supporting line ell_j other than ell_0, its arclength in the boundary of Q_a is zero. Thus dominated convergence on its finite chord implies

    H^1(ell_j∩C∩(Q_a+t e_2)) → H^1(ell_j∩Q_a)

as t→0 from either side. Distinct lines have only point intersections, so the same continuity holds for the sum of all their contributions.

For ell_0 itself, the intersection length is a for sufficiently small t<0 and zero for t>0: its e_2 coordinate is zero, whereas the translated cube occupies t<=u_2<=a+t. Its e_1/e_3 coordinates remain unchanged by this translation. The full-chord property ensures that the whole segment of length a is present whenever the cube contains it.

Therefore the one-sided limits of

    mu_A(Q_a+t e_2) − |Q_a+t e_2|

differ by a/L. The volume is exactly a^3 on both sides. At least one of the two limits has absolute value at least a/(2L), hence the supremum over admissible cubes is at least

    a/(2L) >= 1/(16L).

For L>=1 this is the desired bound. For L<1, the same nonempty-core branch gives at least 1/(16L)>=1/16, while the empty-core branch gives 1/8. This proves the assertion for all L>0.

## Boundary and scope audit

- The argument uses actual nearby positive-side cubes contained in C, not a degenerate test set or an essential supremum.
- Closed cubes cause no difficulty: the discrepancy at t=0 is not needed. The one-sided limits are approached by admissible translated closed cubes.
- Other lines crossing cube edges only contribute sets of zero arclength at the limit, so dominated convergence applies.
- Repeating lines does not increase the measure, and is eliminated at the start.
- Many short grazing chords are harmless. The selected core-crossing chord supplies a fixed segment; all other contributions are controlled by continuity, not by their number or length.
- Free rotation is essential: the face containing the selected line is chosen after its direction is known. This is not an axis-parallel result.

## What remains

The discontinuity of one face accounts for only a single jump of order 1/L. To obtain log(L)/L by this route, one would need a multiscale or multi-line accumulation argument that cannot be canceled by the remaining lines. This proof supplies no such accumulation. The Borda construction from Attempt 2 shows that fixing a single global test orientation cannot supply that missing step for all configurations.
