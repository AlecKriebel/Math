# Independent review of the labelled short-trajectory ratio theorem

**Verdict: PASS_COMPLETE_LABELLED_LENGTH_RATIO. No mandatory mathematical correction.** The frozen proof establishes Fuchs's Conjecture 2.7 with the full source's segment-parity convention for its type labels. It proves the labelled ratio, rather than merely reproducing an unlabelled length spectrum.

Reviewed on 2026-09-30 by a separate GPT-6 Astra agent at xhigh reasoning. This is adversarial AI review, not human peer review or a historical-priority certificate.

## 1. Frozen object and source convention

The reviewed `CANDIDATE.md` has SHA-256
`100454abdfcbeb6647e0e0596a86b86b3a39d330de2605fe485ae242d9e91c9a`.
The submitted verifier has SHA-256
`8e7b57f47567c0cb61f1090af50d1f13da09859f8b63a15444da3f60d1ceb5cd`,
and its receipt has SHA-256
`fb9ccb16be3cd656d9a1700198d19e612a1ebf8deae8cc981cc7f6fe41b6a941`.

I read the complete relevant sections of [Fuchs's published article](https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf), including the rendered type definition on p.502, its continuation and direct-chord illustration on p.503, the elementary lattice rules on p.506, and Conjecture 2.7 on p.512. A short trajectory has no intermediate vertex; there is no small-length asymptotic. The source's direction relation is its dihedral parallelism, not a common itinerary or only one literal slope.

The paragraph immediately before Definition 2.1 specifies the sign by segment parity: the sum relation is used for odd segment count and the difference relation for even count. The candidate correctly retains this contextual selector. It cannot be discarded when applying the displayed branches. For example, a one-segment diagonal of a pentagon with alpha=2pi/5 and beta=4pi/5 satisfies both numerical sum and difference integrality conditions. Reading all branches with parity erased gives overlapping labels A0 and A1; the prescribed odd-segment sum rule gives A1, in agreement with the direct-chord labels in Figure 9. The p.506 shorthand concerning A0 likewise must be read in this context. The reviewed theorem uses this coherent full-source convention, rather than an ambiguous isolated reading of one displayed equality.

The sine weight uses the canonical representative 0<=k<=n-3. Although k is a residue modulo n-2, sin((k+1)pi/n) is not defined by substituting arbitrary representatives. The proof handles this distinction explicitly.

## 2. Translation surface, unfolding and involution

The stated double-polygon surface is the appropriate quotient of ordinary billiard unfolding. Reflecting a regular polygon across one of its sides gives a translate of its half-turn: reflection across the parallel line through its center is the half-turn composed with a polygon symmetry. Successive copies therefore alternate between translates of P and Q=-P. The side identification reverses endpoint order, exactly as specified. A finite billiard path with no intermediate vertex projects to a saddle connection of the same length. Conversely, a connection can be developed through these copies and folded by the side reflections; the intermediate marked-vertex condition is preserved. The even case must retain the two labelled copies even when their geometric shapes coincide.

The corner permutation is (P,j)->(Q,j+1)->(P,j+2). It has one cycle of length 2n for odd n and two cycles of length n for even n. Multiplying by the corner angle (n-2)pi/n and using Euler characteristic gives the stated cone angles and genera. In particular, the even double polygon is not silently replaced by the lower-genus opposite-side single polygon.

The half-turn exchanging P and Q is compatible with the gluing. It has no fixed point in either polygon interior, exactly one fixed midpoint on each identified edge, and the claimed vertex action: one fixed vertex class for odd n, two exchanged classes for even n. Thus it has 2g+2 fixed points when n>=5. Riemann–Hurwitz gives a sphere quotient.

For any affine automorphism f, the conjugate f*iota*f^(-1) has derivative -I on the regular part. Hence it is holomorphic there and extends holomorphically across the finitely many cone points. It is topologically conjugate to iota, so its quotient is again a sphere. Since the genus is at least two, uniqueness of the hyperelliptic involution implies f*iota=iota*f. This remains true if f reverses orientation: the derivative of the conjugate is still -I. No uniqueness assertion for a torus involution is used; n=3,4 are handled separately.

## 3. Cone-germ residue and its affine invariance

For an oriented connection with both ends at one cone point of total angle 2pi*r, its initial and backward terminal germs differ by pi modulo 2pi. Their difference on the full cone circle is therefore pi+2pi*m, with m defined modulo r. When the even double polygon has different endpoint cone points, applying iota to the backward terminal germ brings it to the initial cone point and changes its ordinary direction by pi. The resulting difference is 2pi*m. The endpoint indicator e is preserved by homeomorphisms.

An orientation-preserving invertible linear map induces an increasing angular lift F satisfying F(theta+pi)=F(theta)+pi. This follows from antipodality and degree one; an added cone-sheet offset cancels between germs at the same cone point. Therefore it preserves the two differences above. In the different-endpoint case the commutation with iota supplies exactly the needed compatibility between the two cone points. There is no independently chosen endpoint sheet shift that could change m.

For an orientation-reversing lift the corresponding relation has -pi. Thus m changes to -m-1 in the same-endpoint case and to -m in the different-endpoint case. Reversing an oriented surface connection has the same transformations, using iota^2=1 when necessary. These statements concern the intrinsic cone indices and do not assume the desired length formula.

## 4. Identification with the actual source labels

I checked the corner-angle computation independently, not merely its final congruence. Start at P0 with lower-boundary angle zero. The corner cycle advances by delta=(n-2)pi/n. For even n, choose Q0=iota(P0) as the base of the second cycle; applying iota identifies its angular coordinate with that of the first cycle.

At a terminal P corner, the backward germ has offset pi-beta. At a terminal Q corner, the reflection of the developed polygon reverses that offset, giving delta-(pi-beta)=beta-2pi/n. The angle between the initial germ and the appropriate terminal germ is consequently

    t*delta+pi-(alpha+beta)                 for terminal P,
    t*delta+(beta-alpha)-2pi/n              for terminal Q.

For the even case, the terminal corner parity is t=2a+e in the first expression and t=2a+1-e in the second. Equating these with (1-e)pi+2pi*m yields respectively

    mn=a(n-2)+e(n-1)-s,
    mn=a(n-2)+s+e-2,

with s the source's selected integral angle parameter. Reducing modulo n-2 gives k=2m+1-e. For odd n the same computation has e=0 and gives k=2m+1 modulo n-2. Since n-2 is odd in that case, multiplication by two introduces no loss of labels.

The full inequalities in Definition 2.1 agree with these formulas on the permitted angle intervals, including the two side-boundary descriptions of A0. The independent controls enumerate actual corner positions and admissible angle offsets before comparing with the printed branches. They also verify the physical lower-boundary direction of every corner: for copy s and vertex j it is s*pi-2j*pi/n, agreeing with the cone-cycle coordinate modulo 2pi.

The involution and angular-lift argument therefore preserves the intrinsic label under orientation-preserving affine transport. Orientation reversal changes the label to -k. The canonical sine weights agree under that change: for k nonzero, (-k mod(n-2))+1=n-(k+1), while k=0 is fixed. Polygon symmetries and permitted reversals thus preserve the weight. This is the crucial labelled step absent from a mere length-spectrum argument.

## 5. Classical theorem dependencies and direction reduction

The proof imports classical results, rather than deriving the Veech dichotomy from computations. Their precise needed forms are adequately supported by the full primary sources that were retrieved:

- [Finster, arXiv:1005.4588v3](https://arxiv.org/abs/1005.4588v3), Sections 3.1–3.2 and Remarks 3.2, 3.5, gives the odd double-polygon group with one cusp and the even group with two cusps. In the even case, p.7 explicitly states equality of the Veech group of the double-polygon cover with that of the opposite-side quotient, citing the appropriate prior lemma. Thus the group is not transferred between those surfaces by an unsupported assumption. The base group's two cusp representatives are given on p.20; they are not the more numerous cusps of Finster's later covering family.
- [Boulanger–Lanneau–Massart](https://www.numdam.org/articles/10.5802/ahl.211/), Section 1.4, printed p.791, explicitly states the general Veech-surface saddle-connection/cusp correspondence. Its own one-cusp double-polygon family is odd, and is not used to assert one cusp for even n.

I inspected the rendered even-group, two-cusp and general-correspondence pages. These are precise theorem statements in full retrieved primary papers and suffice as dependencies for the argument. The original Veech 1989 full text was not retrieved; the source-access limitation is accurately disclosed and must remain so. The proof is not foundation-free and does not claim a new proof of those classical results.

The group statements supply an orientation-preserving affine map taking any saddle-connection direction to one of the model symmetry directions. It is one map for the entire direction, not separately chosen maps with unrelated length multipliers. In Finster's coordinates the cusp at infinity is horizontal; the second even representative is obtained by an angle pi/n. Their perpendicular axes are polygon symmetry axes.

In such a model direction, every inward vertex ray in a polygon ends at the reflected vertex across the perpendicular symmetry axis. Convexity ensures that this entire chord is inside the polygon and meets no side interior first. A vertex fixed by the reflection has only a supporting line in that direction, so contributes no additional interior ray. Boundary rays are polygon sides. Considering every polygon corner therefore exhausts the model saddle connections without an unproved assumption about their combinatorics.

For a chord from P0 to Pj, the elementary chord formula gives length 2R*sin(j*pi/n). Its one-segment source angles give k=j-1 modulo n-2; the final side j=n-1 has the same weight as k=0. Every model connection therefore has length 2R*w_n(k). A common affine derivative multiplies both lengths in one unoriented direction by the same positive factor. Transporting back proves the labelled ratio.

The final dihedral alignment handles Fuchs's broader direction relation. Odd-polygon half-steps modulo pi may also be realized on the double polygon by rotation through pi/n and exchange of its copies. Such isometries preserve length and the already identified weight. This does not assume the neighboring type-distribution or reachable-polygon conjectures.

## 6. Small n and the marked-vertex issue

The low cases are correctly separated from the general cusp argument. For n=3, every first vertex in triangular-lattice unfolding is primitive, and there is only one type. For n=4, primitivity and the both-coordinates-odd condition give the stated square types and are preserved by its direction symmetries.

For n=6, the relevant marked vertices form two residue classes in a triangular lattice, not every lattice point. Write a primitive direction as v=(p,q). The first marked point is v if p+q is 0 or 1 modulo three, and 2v if it is 2. The source's explicit type rules then give weights sqrt(3)/2, 1/2 and 1 in the three cases, respectively. In the zero-residue class, parallel directions have one length and weight. In the other class the first length can double exactly when its weight doubles, so L/w remains 2|v|.

The generators (p,q)->(q,p) and (p,q)->(p-q,p) preserve the triangular norm p^2-pq+q^2 and send p+q to itself or its negative modulo three. This checks the full direction class. It is important that such a direction operation at a fixed base vertex need not preserve the honeycomb's missing residue class; the candidate correctly recomputes the first marked endpoint instead of declaring all primitive lattice points to be hexagon vertices.

## 7. Exact checks and verdict limits

All **14,630 submitted assertions** replay byte for byte. The independent standard-library checker passes **60,055 assertions**, including:

- actual corner-cycle and boundary-direction checks for n=3 through 24;
- 8,129 comparisons between cone-germ indices and the full parity-selected printed type definition, including boundary cases;
- the same number of reflected-label and reversed-intrinsic-index checks;
- direct-chord labels and canonical sine reflection;
- nonlinear antipodal angular-lift controls with arbitrary common cone-sheet offsets;
- direct first-marked-point searches in 464 primitive lattice directions, followed by all twelve triangular-lattice dihedral transformations.

The finite controls do not prove hyperelliptic uniqueness, Veech's theorems, or the all-n conclusion. The preceding geometric argument and credited theorems support those steps. No substantive gap was identified in the labelled ratio proof.

Publication should retain the source's parity convention, exact meaning of short and parallel, two-polygon even surface, three elementary exceptions, and classical-theorem access qualifications. The result concerns Conjecture 2.7 only. No historical-priority claim, proof of neighboring conjectures, or human-peer-review claim is supported by this audit.
