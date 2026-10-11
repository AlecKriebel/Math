# PR110 independent geometric and global-family adversarial review

Result: **no required or optional mathematical correction found in the reviewed claim**. This is clearance for the geometric scope described below, not a novelty or publication certificate.

PR110 / upstream ID5100032 / invariant k603. Review completed 2026-10-06 UTC. Original effort recorded by the parent: 2/5; this review consumed zero new central proof-search turns. It independently verified an existing complete candidate, without extending an unfinished approach.

## Independence, materials, and target

I read the complete original `PROOF.md` (6990 bytes, SHA256 `8478d2a792944c5fb9e8a53324e0c6bce8eba317de29c31a6fcbd6ca0205709d`) and `source_record.json` (3926 bytes, SHA256 `488f04aa9db8b1bb428d3331b96773786cfbd3cfe225192f5182941edfbef1c5`). I did not read, import, execute, or use the author's verifiers, submitted independent review, or any current reviewer's report. The exact rational linear solves and tangent-normal orbit reconstruction in `independent_geometric_controls.py` are separate implementations.

I independently inspected the pinned primary PDFs supplied by the parent: Reznik-Garcia-Koiller arXiv:2004.12497v11 (3389610 bytes, SHA256 `c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da`) and the published 2021 paper (1836579 bytes, SHA256 `c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42`). Relevant text was extracted independently. I visually read arXiv pages7 and9, including Figure3 and Table7, and published PDF page9 / printed349, including Table7 and Section3.7. The source introduction and preliminaries specify an outer ellipse and confocal elliptical caustic. Section3.5 defines antipedal intersections; Section3.7 uses ordinary Euclidean distances from each focus; Table7 k603 is the ratio of the sums of those antipedal distances, with value1 for allN. Signed areas elsewhere in the paper do not change these distance definitions. The table is evidence for the literal target and its historical conjectural status, not evidence of current priority.

The source's informal word "rays" in Section3.5 does not specify a uniform choice of half-line. Figure3 shows the perpendicular supporting lines connecting neighboring antipedal vertices on their appropriate sides. I used the usual, and explicitly stated submitted, consecutive supporting-line intersection construction. Requiring a single common orientation of all perpendicular half-rays would generally fail even to define this antipedal polygon; that is not the illustrated construction. A cyclic reindexing of intersections has no effect on the sums.

Exact reviewed claim: for a>b>0 and 0<lambda<b^2, every closed nondegenerate billiard/Poncelet orbit between x^2/a^2+y^2/b^2=1 and the strictly nested confocal ellipse with squared axes a^2-lambda,b^2-lambda has equal sums of the ordinary focal distances to consecutive antipedal intersections. Simple, self-intersecting/star, reversed, and repeated orbits are included. There is no claim of a nondegenerate orbit for every integerN, no hyperbolic-caustic or degenerate two-bounce extension, and no individual-sum constancy claim.

## Independent normal-coordinate reconstruction

This supplies a checkable derivation without relying on the submitted midpoint-angle parametrization. Write c^2=a^2-b^2. Orient one billiard edge from A to B with the caustic to its left. Let n=(n_x,n_y) be the outward unit normal to its supporting line, so n dot X=rho with rho>0, and put

    H=a^2 n_x^2+b^2 n_y^2,
    v=(-n_y,n_x),
    rho^2=H-lambda.

The last equality is precisely tangency to the confocal ellipse. Solving the outer-ellipse quadratic on this line gives its chord midpoint and positive half-length:

    M=(a^2 rho n_x/H, b^2 rho n_y/H),
    L=ab sqrt(lambda)/H,
    A=M-Lv, B=M+Lv.

Both foci are strictly inside the caustic: a^2-lambda>c^2 follows from lambda<b^2. More directly, with h_sigma=rho-sigma c n_x,

    h_+ h_-=rho^2-c^2 n_x^2=b^2-lambda>0.

Since rho>0, both h_sigma are strictly positive. They are the ordinary perpendicular focal heights to the chord. Therefore

    det(A-f_sigma,B-f_sigma)=2L h_sigma>0.

The defining antipedal linear equations are nonsingular, and no antipedal intersection can equal its focus, since the equations require Q_relative dot (A-f_sigma)=|A-f_sigma|^2>0. Thus all distances are finite and strictly positive, even when an antipedal polygon itself crosses or has repeated vertices.

For an ellipse point with coordinate x, its focal distance is a-sigma c x/a>0, as follows by squaring and using the ellipse equation. If R_sigma is the product of the endpoint focal distances, the expressions for M,L give

    R_sigma=[a^2 h_sigma^2+b^2 lambda]/H.

For completeness, expand

    R_sigma=a^2-sigma c(x_A+x_B)+(c^2/a^2)x_A x_B,
    x_A+x_B=2a^2 rho n_x/H,
    x_A x_B=a^4 rho^2 n_x^2/H^2-a^2 b^2 lambda n_y^2/H^2.

Substituting rho^2=H-lambda and c^2=a^2-b^2 gives the stated identity. The antipedal linear solve, or the triangle area identity, yields the ordinary positive norm q_sigma=R_sigma/h_sigma. Hence

    q_sigma=[a^2 h_sigma+b^2 lambda/h_sigma]/H,
    q_+-q_-=(2c n_x/H)[-a^2+b^2 lambda/(b^2-lambda)].

The directed vertical chord displacement is 2L n_x. Consequently

    q_+-q_-=Gamma (y_B-y_A),
    Gamma=c/(ab sqrt(lambda))[-a^2+b^2 lambda/(b^2-lambda)].

All quantities needed to remove absolute values were proved positive before doing so. The calculation verifies the submitted coefficient, including its sign. Gamma can be negative, zero, or positive; its zero occurs at lambda=a^2 b^2/(a^2+b^2), where the two distances are equal separately on every edge.

## Global branch, reflection, winding, and boundaries

At a point of the outer ellipse there are exactly two tangent lines to the strictly convex inner ellipse. Among their inward-pointing directions, one keeps the caustic on the left and the other on the right. The billiard law for confocal conics continues along the other tangent line. Thus the incoming left-caustic direction continues to the inward left-caustic direction. This is also the single-branch Poncelet tangent map. The source itself states the bisecting-normal billiard property.

A hidden immediate retracing exception cannot occur in this scope. At P=(a cos t,b sin t), a chord on the outer normal has confocal tangency parameter

    lambda_normal=b^2 cos^2 t+a^2 sin^2 t >= b^2.

This follows by taking its unit line normal perpendicular to (cos t/a,sin t/b) and substituting into the preceding support equation. Therefore a tangent to a strictly elliptical caustic with lambda<b^2 cannot be a normal-incidence, branch-flipping retrace. A generic closed walk of tangent chords that backtracks is outside the billiard hypothesis.

Because the origin is strictly inside the caustic, it is strictly left of each left-oriented chord: det(A,B)>0. The lifted outer-ellipse parameter advance is therefore in (0,pi). This holds separately for every edge, irrespective of how many complete turns the orbit winds around the caustic. Star/self-intersected orbits need not have winding1. The normal-coordinate identity is local and does not use a simple-polygon area or a symmetry of low periods.

Summing the identity over any closed sequence on that branch gives Gamma times the sum of vertical displacements, which is exactly zero. Reversing the whole orbit preserves each ordinary focal antipedal distance; one can either reverse again for the left-oriented derivation or use the corresponding negative coefficient. Repeated traversal repeats all terms, including any repeated vertices, and preserves the ratio. There is no assumption that allN exist or thatN denotes a primitive period.

The endpoints lambda=0 and lambda=b^2 are excluded, for real geometric reasons: the former permits coalescing endpoints and coincident antipedal lines, while the latter degenerates the caustic to a focal segment and allows a chord through a focus, giving a singular antipedal system. The proof asserts neither continuity of each individual distance at those endpoints nor a ratio for undefined intersections. Hyperbolic caustics allow a focus on the opposite side of a support and would require a different absolute-value analysis. The stated circle limit has coincident foci, so equality is pointwise whenever the antipedal construction is defined.

## Independent controls and falsification attempts

Both normal and optimized Python runs passed **4037 explicit requirements**. Actual final child PIDs were1558 (normal) and2256 (optimized); both exited0 and were reaped. Complete argv, UTC start/end times, exit status, and complete small stdout/stderr bodies and hashes are in `process_receipts/controls_normal` and `process_receipts/controls_optimized`. The code uses explicit exceptions rather than assertions, so optimization does not remove its conditions.

The 21 exact rational chords use focal triples (a,b,c)=(5,3,4),(13,5,12),(17,8,15), with deliberately short, intermediate, and near-major-diameter chords, horizontal chords, and both coefficient signs. Each control directly solves the two rational antipedal line equations and checks the squared norm, positive focal products/heights, tangency, discriminant, and unsquared positive-norm coefficient. These computations do not import the submitted equation implementations.

For example, with axes5,3 and A=(5,0), B=(3,12/5), the caustic parameter is225/61 and the ordinary distances are

    q_+=13 sqrt(61)/30,
    q_-=37 sqrt(61)/30,
    q_+-q_-=-4 sqrt(61)/5.

With B=(-3,12/5), lambda=900/109 and the difference becomes +8 sqrt(109)/5. These verify that the proof is not silently assuming a coefficient sign or edgewise equality.

Nine small closed-cycle numerical controls independently reconstruct tangent points/lines from the inner ellipse and obtain the next outer-ellipse intersection. They check actual closure, each edge's common confocal tangency, ordinary antipedal norms, and the Euclidean reflection law at every vertex. The cases are an exact-coordinate four-bounce diamond and two different starts for each of (N,winding)=(3,1),(5,1),(5,2),(7,2). Each is also reversed and doubly traversed. The winding-2 cases are self-intersecting and would fail a hidden simple-polygon assumption. The near-degenerate five-point star has very large sums; its relative sum discrepancy is about1.6e-11, consistent with conditioning, while the exact identity supplies the proof. These finite-precision tests are controls, not rigorous certification of the root-found numerical caustic parameters.

The deliberate closed tangency backtrack A,B,A,B has focal-sum ratio **13/37**, not1. Its edge is exactly tangent to the fixed lambda=225/61 caustic, but it violates the billiard reflection/continuation law. It falsifies the stronger, unstated claim for arbitrary closed tangency walks, and confirms that global branch consistency is necessary. A further exact vertical-chord control gives lambda=16>b^2 and puts one focus across the supporting line; it exposes why a hyperbolic-caustic extension cannot reuse the positive-height step. Neither control is a counterexample to the submitted theorem.

## Findings, strongest claim, and remaining gaps

Required findings: **none**. Optional mathematical corrections: **none**.

The strongest verified mathematical result is the ordinary-distance equality, and hence positive ratio1, for every admissible closed nondegenerate single-branch billiard/Poncelet orbit in a strictly nested confocal ellipse pair. The local identity and cyclic cancellation cover all periods and windings without an unproved global constancy lemma. The primary source target matches that scope. No counterexample or unsupported geometric step was identified.

Current priority, novelty, later literature, and publication-package readiness remain outside this independent review. A separate priority audit is still required before any novelty claim. This review did not modify Git, native assessment data, services, the submitted source, other reviewer folders, or the primary PDFs. Copyrighted text extracts and page renders are private; their pins and exclusion list are recorded separately, and their bodies are excluded from the public review seal.
