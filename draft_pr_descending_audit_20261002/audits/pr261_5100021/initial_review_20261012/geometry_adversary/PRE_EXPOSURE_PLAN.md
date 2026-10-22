# Pre-exposure geometry audit plan

Timestamp: 2026-10-12 09:32:45 UTC. Audit completion estimate: 3%.

## Exposure declaration

Read only the root and program AGENTS.md instructions and the submitted packet's file-name inventory. No PROOF.md, author checker, receipt, prior review, author verdict, or source scope document has yet been read. The precise target below comes from the parent auditor's assignment.

## Target and assumptions

Fix a noncircular outer ellipse with semiaxes a>b>0 and one of its ORIGINAL foci F. Fix a strictly nested nondegenerate confocal elliptical caustic with semiaxes sqrt(a²-lambda), sqrt(b²-lambda), where 0<lambda<b². Consider primitive real billiard polygons with least period N divisible by 4, including admissible star winding. For each original side line form the foot of F. For each consecutive pair of original vertices form the intersection of their antipedal lines, each line passing through its original vertex and perpendicular to vertex minus F. Use ordered signed shoelace areas in orbit order. Hypothesis: the product of these two areas is independent of phase for fixed outer ellipse and caustic.

## Independent mechanism before proof exposure

1. Translate the ORIGINAL focus to the origin. Write each original vertex as P_i=r_i u_i, |u_i|=1; for the right focus, r_i=b²/(a+c cos(theta_i)), c²=a²-b². Derive both constructions solely by two-by-two linear algebra. With D_i=P_{i+1}-P_i and K_i=det(P_i,P_{i+1}), the pedal foot should be Q_i=K_i (D_iy,-D_ix)/|D_i|². The antipedal vertex should be A_i=((|P_i|²P_{i+1,y}-|P_{i+1}|²P_iy), (P_ix|P_{i+1}|²-P_{i+1,x}|P_i|²))/K_i. Independently prove these formulas and determine when their denominators can vanish.
2. Derive the reflection/tangency condition from the two quadratic ellipses, and formulate a direct geometric orbit generator. Avoid importing elliptic-function formulas or any submitted checker. Use tangent lines from a boundary point to the inner ellipse, intersect the outer ellipse, and choose oriented positive rotation branch.
3. Derive the period-4 caustic and family directly, then compute exact signed products at axial and generic phases. This provides a low-period algebra baseline independent of any general addition theorem.
4. Explore whether central symmetry for even billiards simplifies pedal/antipedal pairs. Check focal inversion, polarity, and angular identities as candidate mechanisms. Explicitly identify unsupported central claims rather than assuming closure implies needed symmetry.
5. Test primitive winding, both focus choices, finiteness, zero signed areas, cyclic shift, traversal reversal, scaling (expected degree four for an area product), degeneration as lambda approaches 0 or b², and near-parallel antipedal intersections.
6. Freeze independently derived formulas and computational output before exposing PROOF.md and source scope. Then inspect the complete proof and compare its stated hypotheses and all denominators with these independent results. Do not use the prior independent_review verdict as evidence.

## Success criteria

Either give a reproducible counterexample under the exact target assumptions, or verify the submitted general argument and its domain, clearly distinguishing independently proved low-period and geometric facts from deductions requiring its special-function lemmas. No statement of novelty follows from this geometry audit.

## Constraints

All writes stay in this geometry_adversary directory. No Git mutations, remote writes, external communications, PR changes, or new research-program proof attempts. Findings are reported internally to the parent auditor only.
