# Mathematical acceptance: PR 256 / k307

Checkpoint 2026-10-13 03:34:03 UTC. Status: PASS for the exact domain-qualified theorem, with the explicit four-period converse in candidate_repair_01/PROOF.md. Mathematical audit completion 100%; overall review/package estimate 40%. Priority review is ongoing; this is not publication clearance.

The authenticated original PR head is 9445a90b57f76493bd901edc544b09dec393e20f. The original proof has SHA256 d072c6ecf0f398753382603bbd00b4a950e50881d1fd3aa70526fc8889c12584 (12332 bytes); the revised proof has SHA256 db195a16fdc3d4e28969f04a2740f78912533d8ddab292a13913822c5ebd7820 (12727 bytes). Submitted originals remain unchanged.

## Accepted claim and boundaries

For a>b>0 and a strict confocal elliptic caustic 0<lambda<b² supporting a poristic billiard family of least even period N>=4, the signed area centroid of the ordered perpendicular feet from any fixed real M onto the outer tangent lines is given by formula (2), independently of phase whenever its signed area is nonzero. Formula (1) gives the entire zero-area locus: none when d>=0, precisely the fixed circle |M|²=-2F/d when d<0. Simple winding-one even families have d>=0. Least period four is equivalent to d=0, and its centroid is M/3. Primitive stars, signed self intersections, reversal, and repetitions of even least-period orbits retain the stated conclusions. Padded odd least periods, hyperbolic or degenerate caustics, and circular billiards are outside this claim.

The source's definition is the signed first-moment quotient, not the arithmetic vertex mean or the centroid of an unsigned polygon union. Both primary Table 4 pages and the centroid definition were read directly. The exact 8/3 orbit has exceptional radius squared 123539/20736, and a point on that circle has nonzero raw first moment, so its undefined quotient is genuine.

## Complete proof audit

Root independently read the entire original proof, the supplied three verification sources, both new derivations and their checkable sources. The commuting finite circle group is cyclic and its unique involution gives antipodal pairing. Strict origin-inside-caustic geometry gives positive successive normal sine and positive S(0), including stars. Chord tangency gives the bilinear support identity; both F±ed factors are strictly positive. The squared support compatibility and division-free unit-circle telescope give T_Z=2v S_Z. The origin-area telescope and antipodal projection averages then give the full quadratic area and all cubic moment coefficients. Both Laurent and direct real Cartesian edge reductions have explicit endpoint potentials which telescope in trajectory order, without a simplicity assumption. Signed translation and division by 6S give exactly the stated centroid. The final expression removes the intermediate division by d; d=0 is proved directly using a rectangle.

The only requested exposition repair was N=4⇒d=0. The inserted paragraph adds the two consecutive support identities whose right sides negate under n2=-n0 and whose left sides both equal d h0 h1. Positive support numbers force d=0. Root and both independent reviewers directly verified this paragraph. No remaining mathematical gap or unresolved falsifier was found within the stated assumptions.

## Reproduction and independent evidence

Root's author replay passed all 63 exact assertions and its numerical controls; the two floating maxima differ from the original by about 2.6e-15, honestly retained in the reproduction summary. The supplied independent exact replay (4355 checks) and separate 85-digit replay (6108 diagnostics) reproduced byte for byte.

The new algebraic adversary derived the entire all-period Laurent calculation independently and passed 68 exact assertions, unrestricted symbolic-M star polynomials, and 141 independently tangent-generated families / 564 phases / 2520 pedal cases. The new geometric adversary independently constructed physical reflected trajectories, proved the all-real Cartesian coefficient reductions, and passed 21 families at 110 digits, periods up to 200 and aspect ratios up to 10^6. Root also normally reproduced the finalized real Cartesian symbolic certificate (exit 0, PASS), including its quotient-assembly assertions. Finite diagnostics corroborate the written deductions; they are not the all-period proof.

Initial numerical generator failures near degenerate caustics and the spurious N4 circle caused by sign noise are retained with their reproducing sources and successful precision/domain repairs. Neither produced a surviving mathematical counterexample. The algebraic reviewer explicitly records that the original first-run full scripts were not retained and labels the minimal reproducer as reconstructed.

AI tools were used extensively for this audit. These are independent AI reviews, not external human peer review or proof-assistant formalization. No absolute novelty conclusion, preprint, DOI, tracker row, or PR merge is accepted at this checkpoint. Program counts remain 37 completed, 14 preprints, 14 native merges, 0 pending tracker rows.
