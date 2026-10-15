# Pre-exposure independent test and source plan

Saved 2026-10-12T09:33:53.063230+00:00. No submitted proof, author script, old review, or old review script has been read. Intake manifest and directory listing only have been read. Audit fixed head: 7b7fcd63d5ea83df3a4c29853c4ba34b93d16f07.

## Exact hypothesis and success criteria

The target is Table 5 invariant k_{403,b}: for an original elliptic billiard of primitive period N divisible by 4 and a strict, nondegenerate inner confocal elliptical caustic, the product of the signed areas of the ORIGINAL pedal polygon and ORIGINAL antipedal polygon with respect to either ORIGINAL focus is invariant as the initial point moves through the Poncelet family. The original pedal means Euclidean perpendicular feet of the focus to the supporting lines of the original sides. The original antipedal means intersections of consecutive vertex lines through each original vertex perpendicular to its vector from the original focus. Primitive star orbits, negative/signed areas, and zero products must be included. Source verification must compare the complete primary statement with all these restrictions, and identify omitted circle/hyperbolic/degenerate regimes without silently replacing a bundled target.

## Independent approach family

1. Build physical billiard trajectories directly in Cartesian coordinates: select the outgoing direction at an outer boundary point by solving tangency to a strict confocal caustic, intersect the ray with the outer ellipse using the quadratic equation, and reflect at the Euclidean normal. Do not import Jacobi helper functions or proof equations.
2. Detect primitive period and winding from the ray-traced trajectory; find desired closure parameters by a real closure/rotation-number root equation. Validate outer boundary, confocal tangency discriminants, reflection residual, closure, central symmetry, and primitive status independently. Exercise convex and star families at nonaxis seeds for N=4,8,12,16 and higher periods, with caustics approaching circular and flattened limits.
3. Compute feet and consecutive antipedal intersections directly; apply shoelace signed areas, measure both factors and product over phases and both foci. Intentionally measure incorrect inverted constructions if needed to diagnose source ambiguity.
4. Derive a low-period symbolic check from the axis-aligned four-bounce diamond, imposing reflection and caustic conditions, and compare the physical feet/intersections with source target. Assess whether this can check the full one-parameter quadrilateral family, not merely one symmetric phase.
5. Obtain full primary PDFs and source URL metadata, extract the complete definitions, Table 5, and surrounding regime limitations. Visually inspect relevant pages under the PDF skill. Current literature checks use primary sources, with novel/solved status treated separately from mathematical validity.
6. Only after this independent construction is recorded, statically inspect author and previous reviewer scripts and proof-derived computational coverage. Replay scripts in separate writable copies within this owned folder, preserving original submitted bodies. Record interpreter versions, package versions, command logs, hashes and output differences. Report actual coverage and excluded cases, not raw claimed count.

## Falsification and remaining gaps

Any phase-dependent physical product beyond precision/reflection error is a counterexample. Numerical constancy alone is partial evidence. Independence fails if orbit closure or areas are merely repeated proof/Jacobi-helper algebra. No prior reviewer verdict is independent evidence. This agent will not mutate any remote provider or primary .git, and will write only in this folder.

Initial completion estimate: 5% toward this source/reproduction audit.
