# PR201 / problem5100014 — independent direct-geometry audit

Date: 2026-10-16 UTC. Original submitted proof read only after independent freezes; no sibling-family mathematical report was read. The original submitted independent review was read after the freeze as part of candidate comparison. No external-person contact or outreach occurred.

## Verdict and strongest verified result

**No counterexample or internal mathematical defect found within the submitted theorem's exact scope: primitive period N=2 mod4, noncircular ellipse, strictly nested nondegenerate confocal elliptical caustic, arbitrary fixed real M, signed shoelace area.** The candidate's distinct all-period argument is internally coherent conditional on its credited flag-curve and published AA' theorem inputs. This family did not independently read those external credited papers and does not certify their scope; the primary-source family should do so.

The strongest independently reconstructed all-period statements are (i) the exact arbitrary-M radial quadratic identity (6) in DIRECT_DERIVATION.md for every primitive even elliptical-caustic orbit, (ii) central symmetry from the elementary conic invariant measure, and (iii) the full product theorem on the circular boundary for every admissible period/winding/repetition. The direct geometric route reduces the full noncircular target to two scalar products but does not prove their invariance. Its precise gap is recorded rather than promoted as a second full proof.

Two exact counterexamples show why confocality and least-period conventions must be preserved. Neither contradicts the submitted primitive confocal theorem.

## Primary contract

RGK arXiv:2004.12497v11 Section2 assumes a>b>0 and explicitly defines all polygon areas as signed cross-product sums. Section3.4 and Table4 k303,a concern feet from arbitrary M to the outer polygon's sides, i.e. the tangent lines to the boundary ellipse at the billiard vertices. They do not concern feet to the original orbit chords. Table4 gives N=2 mod4 and all M. The source's word 'N-periodic' must be understood as least period, or else the repeated-triangle counterexample below applies. The candidate explicitly states primitive period, so this is an exposed convention rather than an omitted candidate assumption.

## Independent obstruction: listed N without least period

Take E:x²/15+y²/7=1 and lambda=105/16. The inner confocal squared axes are135/16 and7/16, strictly positive. Two primitive3 billiard orbits in this same pair are

H: (sqrt15,0), (−3sqrt15/4,7/4), (−3sqrt15/4,−7/4);
V: (0,sqrt7), (−15/4,−sqrt7/4), (15/4,−sqrt7/4).

For fixed M=(1,0), direct exact tangent intersections and projections give

H: A'=49sqrt15/3; B_M=5/4+235sqrt15/64;
V: A'=25sqrt7; B_M=329sqrt7/64.

Traverse each triangle twice and label its list N=6. Both signed areas double, so the products are respectively

57575/16+245sqrt15/3,     57575/16.

They differ. `exact_geometry_controls.py` verifies the boundary equations, confocal chord tangencies, reflection via equal signed Joachimsthal values, all finite tangent determinants, and area scaling. It uses exact SymPy expressions and explicit exceptions surviving Python optimization. Therefore allowing nonprimitive listed N=2 mod4 without qualification is false.

A repeated traversal of a primitive n=2 mod4 orbit an odd number r of times remains valid, with product scaled by r². The problematic alternative when listed N=2 mod4 is an even repetition of an odd primitive orbit; the example proves no unrestricted extension.

## Independent obstruction: strict nesting without confocality

Take E:x²/4+y²=1 and the homothetic inner ellipse x²/3+y²/(3/4)=1. The affine-regular hexagons

p_i=(2cos(t+i*pi/3),sin(t+i*pi/3))

are primitive6 Poncelet polygons between the same pair. For M=O, the exact products at t=0 and t=pi/6 are5760/169 and1440/49, respectively. All chord tangencies to the homothetic ellipse are verified symbolically. This disproves a weakening to arbitrary concentric nested Poncelet ellipses; those affine polygons are not being asserted to satisfy Euclidean billiard reflection. The candidate retains confocality.

## Candidate comparison after freeze

The candidate's projection formula agrees exactly with the independently derived Euclidean one. The published-input-dependent all-period mechanism was examined for local and global consistency:

- Central inversion preserves each oriented real flag circle, commutes with T, and generates a finite group with it. Averaging a circle metric makes the group rotations, whose nontrivial order2 element is unique. Thus I=T^(N/2); the independent invariant-measure proof corroborates this conclusion and its star coverage.
- The two boundary points at infinity each have two unramified flag lifts. Their lifts pair under I. The proposed set S on the quotient therefore has at most2 points. Adjacent infinite vertices are correctly excluded by the line-at-infinity and tangent-line dual tests. The original area has at most simple poles.
- A left-caustic real oriented chord has positive det(P_i,P_(i+1)), including stars, so A>0. Orientation reversal negates A and B_M while fixing M. The nonconstancy argument is valid, forcing2 distinct quotient poles and dim L(D)=2.
- The foot projection is bounded at infinity because 1/a²−1/b² is nonzero. The four finite isotropic-normal contacts are simple and precisely the common-tangent contacts of the confocal conics. Their displayed C residual is nonzero for lambda>0, hence no unnoticed projection branch.
- For odd m, the congruence2k=1−m modulo2m transports a common-tangent flag to an infinite boundary flag. The possible singular-foot indices0,1,m,m+1 are exhaustive, using sigma-fixed flags and their T-images. Since m>=3, only the paired adjacent singularities can generate a nominal double pole. Their residue vectors lie in the same normal direction, so each leading determinant vanishes for every M, including special zero residues.
- The quotient is unramified for a finite nontrivial translation group; the asserted pole orders descend unchanged. B_M in span{1,A}, followed by orientation reversal, yields B_M=c_M A with no additive constant. The credited AA' invariant then yields the desired product. No division by B_M appears.

No direct-geometry inconsistency was found in these steps. In particular the four-index cancellation has no m=1 problem because primitive period2 cannot have a strictly interior nondegenerate elliptical caustic. This audit is a reconstruction of the finite geometric/local checks, not an independent verification of the external algebraic-geometry inputs or a deep novelty audit.

## Boundaries, signs, and reproducibility

Stars use orbit order and signed areas. The circle formula includes them; direct noncircular numerical diagnostics include primitive10 winding3 and primitive14 windings3,5. Negative quadratic pedal coefficients occur in stars, making zero signed pedal area a real possibility; no division should be introduced.

Circles a=b are outside the submitted a>b hypothesis but satisfy the independent closed formula. At lambda=0, the caustic equals the boundary and collision chords collapse. At lambda=b², the caustic becomes the focal segment and the positive invariant density can become singular. Hyperbolic caustics lambda>b² do not satisfy the nested-ellipse target and require a separate phase-space analysis. At a diameter2-cycle, opposite tangents are parallel and the outer polygon is undefined. None of these boundaries is licensed by the submitted proof or by a continuity slogan.

The two programs are authored here. They use existing software only; SymPy is imported from the sibling runtime dependency directory without reading any authored sibling mathematics. Standard-library numerical diagnostics are regression evidence, not numerical proof. Exact outputs and numerical outputs are identical in normal and−O runs. A transient accidental float promotion in the first exact-control draft was corrected by sympifying all inputs before the final runs; final outputs contain no SymPy Float and exact comparisons were repeated.

Independent route status: **partial / blocked for full noncircular invariant**, because reduction (7) still contains the central difficulty. Reopen it only for a materially new conic identity or geometric mechanism. Mathematical audit workflow is complete for this family; no mandatory correction to the original candidate within its explicit scope is identified. Publication must preserve primitive period and all exact assumptions and must rely on independently checked credited inputs. No novelty assertion is certified.
