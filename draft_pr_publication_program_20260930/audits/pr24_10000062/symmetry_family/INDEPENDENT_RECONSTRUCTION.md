# Independent reconstruction sealed before reviewer/scripts

Time UTC: 2026-10-01T20:38:18.982304+00:00
Exact original head: 6b702110d1bd4b9220e2033fa5eed030911ce8c6.
Candidate SHA256: 3df33716dab169f07c9ff24434023d2945fc8121e03519f91a0a3fdb1ea30f84.
Read before this seal: original candidate, input record, source citations, original PDF full body and page 7 visual, Frettloh-Garber published PDF contextual definitions, Section 2.3 and Appendix A.1.2. No old reviewer report or scripts or sibling/root findings read.

## Full source success criterion
For either X=Euclidean plane or X=hyperbolic plane, consider an ordinary triangulation with all triangle diameters <=r and every vertex-centered ambient metric radius-r ball congruent by an ambient isometry respecting the restricted triangulation. Original Question 5.7 asks whether periodicity follows; it provides no definition. A source-level verdict must retain this ambiguity, ambient alternatives, and whole-ball quantifiers. A Euclidean counterexample to cocompact full ambient symmetry refutes the implication under that convention; it does not decide a convention of existence of one translation, and does not supply a hyperbolic example. No stronger novelty claim is inferred.

## Scoped submitted theorem to verify
Every bi-infinite delta_j in {1/2,3/2} gives the explicit short/tall strip triangulation with maximum diameter sqrt(10) and mutually ambient-congruent closed sqrt(10) vertex balls, with all restricted cells including boundary traces. The concrete submitted sequence has delta_0=1/2 and delta_j=3/2 for j!=0. Its full symmetry group must be noncocompact; translation subgroup must equal 2Z x {0}.

## Reconstruction and attack plan
1. Partition: triangles in each strip form alternating faces with period 2; rows glue face-to-face, locally finite and nondegenerate. Short squared lengths are {5/4,13/4,4}, tall {4,10,10}; areas 1,3.
2. Root lower row at origin. Rows have y=-4,-3,0,1,4 with phases -1-delta_-1,-1,0,delta_0,delta_0+1. Radius sqrt(10)<4 excludes more layers. Cap below -3 contains only one base triangle; outgoing edges at x=+-1 have dot product >=3/2 with downward vector, hence cannot enter disk; other endpoints have |x|>=3 and whole edges |x|>=3/2,|y|>=3. Boundary traces require separate incidence accounting. Reflection switches delta chirality; upper-root halfturn reverses strip order and leaves central chirality. Verify these maps globally as family maps, not claimed symmetries of each concrete member.
3. Intrinsic edge-length recognition must establish all length-2 edges horizontal, with no accidental equal cross-edge lengths. Then every global isometry has linear part diag(s,t), s,t in {+-1}. Rows and unique 1/3 spacings constrain b_y=4m for t=+1 and b_y=4m+1 for t=-1. Set epsilon_j=2(delta_j-1). Sequence constraints are epsilon_(j+m)=s*epsilon_j for t=+1, and epsilon_(m-j)=-s*epsilon_j for t=-1. Row-phase compatibility modulo 2 also needs proof.
4. Concrete sequence has one negative epsilon at index 0, positive at every other integer, including all negative indices. Shift invariance forces m=0. Shift-complement and reversal-complement invariance impossible by cardinality of negative symbols. Reversal invariance forces m=0. This predicts exact full group: translations (x,y)->(x+2n,y) and halfturns (x,y)->(-x+1/2+2n,1-y). No orientation reversing isometry, including glide reflection. Full group has index 2 over translations and cannot cover unbounded heights from compact set (heights become y or 1-y).
5. All empirical finite tests must be subordinate to universal reduction. Independently test exact strip geometry and affine group maps, periodic sequence controls, complemented/reversed sequences, translated defect locations, altered triangle metric, cap radius enlargement, deleted/changed faces, negative-index recurrence. Reproduce historical scripts only after this seal and compare saved receipt content, not timestamps.

## Completion and scope
Audit progress estimate: 20%. Discovery/source-resolution estimate remains the submitted scoped partial 1/5; validation adds 0 proof-attempt turns. No canonical/shared candidate or Git/PR/publication mutation authorized.
