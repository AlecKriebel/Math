# Independent geometric reconstruction before historical audit

Checkpoint: 2026-10-21 23:51:12 UTC. Estimated geometry-audit completion: 75%.

This document was written after reading the complete immutable candidate PROOF.md and the fresh primary source interfaces, but before reading its historical AUDIT.md or acceptance files. Candidate head: c29139d2c2a98f1a0284d0dc794c88f51c680a0c. Candidate proof SHA-256: c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658.

## Exact claim tested

For each fixed m >= 2, every positive prescribed area S, positive gap target L, and positive radius r can be realized by a connected closed smooth hypersurface H in B(0,r) in R^(m+1), with |H|=S and first positive intrinsic eigenvalue greater than L. Taking r=1/2, S=q, L=q(q+m-1) should yield a connected smooth domain between H and the unit sphere, with exactly two boundary components and a uniform positive volume lower bound.

## Reconstruction

1. CDE Theorem 1.4 provides unbounded normalized first positive eigenvalue on embedded closed connected hypersurfaces; in dimension two topology varies, while for m >= 3 the chosen abstract manifold can be S^m. Choose an induced smooth metric g0 with lambda_+(g0) Vol(g0)^(2/m) > 2 L S^(2/m). Rescale intrinsically to Vol(g)=S; then lambda_+(g)>2L.
2. Choose any smooth hypersurface embedding e of the selected abstract manifold. Its positive scalar multiple is strictly short for g and has image inside B(0,r/8). Compactness makes both requirements simultaneous.
3. The inspected DLS Theorem 1.2 explicitly permits N=n+1, arbitrary C0 closeness, and an embedded conclusion when the starting short map is embedded. It supplies a C1 isometric embedding f with image in B(0,r/4).
4. Componentwise smoothing on the compact source produces smooth maps f_j converging in C1. Compact C1 embeddings are open in the C1 topology: local derivative bounds preserve local injectivity, and a positive separation bound for source pairs outside a fixed diagonal neighborhood preserves global injectivity. Thus f_j are embeddings eventually.
5. The induced smooth metrics converge uniformly to g. If c^-1 g <= h <= c g, then volume densities compare by c^(+/-m/2), Dirichlet energies by c^(+/-(1+m/2)), and Rayleigh quotients by c^(+/-(m+1)). The full min-max characterization avoids a changing mean-zero constraint and controls every fixed numbered eigenvalue. Volume and the first positive eigenvalue therefore converge.
6. Rescaling f_j by (S/Vol(h_j))^(1/m) makes area exactly S. The scale tends to one, so the gap stays above L and the image stays inside B(0,r). There is no uniform-in-q regularity assertion.
7. The selected H is orientable: CDE's dimension-two construction is orientable, and for m >= 3 it may be chosen diffeomorphic to S^m. The smooth general hypersurface separation theorem gives exactly two complementary components, each with boundary H. No Schoenflies theorem is used, and the bounded component is not asserted to be a ball.
8. If a=max_H |x|<1/2, every point of norm greater than a is in the unbounded component E, by a radial path to infinity. Thus the bounded component U and its closure stay within B(0,1/2). The open set Omega=B(0,1) intersect E equals B(0,1) minus closure(U). Every point connects within it to the outer annulus, by following an E-path to infinity until its first crossing of radius 3/4. Therefore Omega is connected, its boundary is the disjoint union H and S^m, and its volume is at least omega_(m+1)(1-2^(-(m+1))).

## Falsification attempts and status

- Codimension-one result might only give immersion: rejected by the explicit embedding clause in inspected DLS Theorem 1.2.
- Tiny containment might not survive smoothing or exact-area correction: rejected by the strict radial margins and scaling tending to one.
- Smooth final metric might be unavailable because the Nash-Kuiper output is C1: rejected by C1 smooth approximation plus quantitative metric comparison.
- Large normalized gap on fixed-topology surfaces might be impossible: true for m=2, but that route is not used; genus is allowed to vary. Fixed S^m is used only when m>=3.
- Smooth Schoenflies in ambient dimension four might be required: rejected; only two complementary components and common smooth boundary are needed.
- Complicated cavity topology might disconnect the exterior inside the unit ball: rejected by the path-to-annulus argument; no simple connectivity is required.
- Reversing the cavity's boundary normal could alter its spectrum: rejected; the intrinsic scalar Laplace-Beltrami operator depends on the induced metric, not normal orientation.

No mathematical defect has been found in the geometric part. The main unresolved audit work is a final explicit topology-source cross-check, comparison with the historical audit, boundary-case accounting, and artifact sealing. No current publication, global novelty, or external acceptance conclusion is made.

## Fresh source interface inspection

The actual freshly retrieved PDFs have the same hashes as their historical metadata, but those historical claims were not used as proof. Visually inspected: CDE PDF pages 6,14,15; DLS PDF page 4; complete OWR talk on PDF pages 22-24, printed 2034-2036; CEG PDF pages 1,2,14. The original question invokes Theorem 3, which covers bounded smooth Euclidean domains with no connected-boundary condition. CEG Example 3.1 explicitly uses a two-component boundary and the corresponding two zero modes, although that example is not a Euclidean counterexample.

Hirsch's book has not been independently retrieved. The smoothing argument above does not require a new theorem beyond elementary smooth approximation and compact embedding stability. The underlying Colbois-Dodziuk and arithmetic-surface theorems are accepted established inputs through CDE; they are not reproved. An attempted web retrieval of McGrath's smooth separation note returned HTTP 403; Hatcher's author-hosted Alexander-duality statement is accessible as an independent topological interface.

SOURCE_METADATA.json's historical reviewed_proof_sha256 is 0123ee87...ac9, whereas the immutable proof read here hashes to c4608dbf...f658. This is an evidence-binding discrepancy; it does not by itself falsify the present proof.
