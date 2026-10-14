# Exact source and prior-attempt gate: k404

Checked 2026-10-01. Target 5100022 / AMR-050-0022, rank 275.

## Exact formula and objects

Both Reznik–Garcia–Koiller editions agree: arXiv:2004.12497v11 (29 October 2020), Table 5 p. 7, and *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal 7 (2021), Table 5 p. 348, DOI 10.1007/s40598-021-00174-y. The row k404 is

    A_M^* / A_M,    N = 2 modulo 4,    M=f1 or f2.

The denominator is the signed area of the feet from the fixed focus M onto successive side lines of the original billiard orbit. The numerator is the signed area of the antipedal polygon of that same original orbit: its side through P_i is perpendicular to P_i−M, and its vertices are consecutive intersections of those lines. Neither object uses the outer tangent polygon or the inner caustic polygon. The fixed focus is a focus of the original billiard ellipse, also shared by its confocal caustic.

Source §2 specifies a>b>0 and a confocal elliptical caustic. Equation (1) uses signed shoelace area. Section 3.5 explicitly allows self-intersecting antipedals. Primitive periodic orbits, including star winding classes with strict nondegenerate elliptical caustic, are the intended period convention; repetitions must be considered through their underlying primitive period, rather than assigning a different parity to the same orbit.

Both table renderings have been visually checked. They retain a question mark in the proof column. The §3.5 prose reuses A_m for the antipedal area without its star, while the table and neighboring pedal definitions disambiguate A_m^*. The target row is stable across these editions, despite numbering and formula changes elsewhere in the papers.

## Domain obligations

Every focal pedal foot is finite. For focal antipedal consecutive intersections, dependence of the two normal vectors would mean a caustic tangent chord passes through a focus; the focus lies strictly inside the elliptical caustic, so this cannot happen. Thus the real intersections are finite under the stated strict hypotheses.

The signed denominator must still be checked. Finite vertices or convexity of the original orbit do not by themselves prove nonzero derived area for stars. Any invariant quotient must be stated on its actual nonzero denominator locus, with a separate decision about whether a cross-multiplied identity or an extension remains meaningful. A zero numerator is allowed. Hyperbolic/degenerate caustics and a circular billiard are outside the exact source assumptions.

## Known results and related campaign work

Stachel's canonical Jacobi parametrization in *On the motion of billiards in ellipses*, European Journal of Mathematics 8 (2022), 1602–1622, Theorem 4.3 and equation (4.9), provides an applicable exact parametrization for the strict elliptic-caustic family. Its repository filename mentions a different journal, so the full PDF header and theorem, rather than that filename, identify the source.

The campaign's k204 / 5100013 proves the original pedal trace and ratio for the same period parity and arbitrary M. Its exact frozen proof is a possible credited input, not an independent new result of this target. Prior k203,a / PR203 and k203,b / PR204 underlie that trace method. Related antipedal PRs 110, 140, 223, 224, 227, and 228 concern other quantities or equality/centroid assertions; none claims the k404 target. The symmetry proof for equality of the two focal antipedal areas does not imply their ratio to a pedal area.

A targeted current search for k404 and focal antipedal/pedal area-ratio proofs did not identify a full general-period proof. This search is not a proof of current historical openness. The source's companion low-period literature and the bicentric/focus-inversion literature must be distinguished from a general k404 resolution. No novelty is claimed at the gate.

## Prior-Alec/campaign gate

Exact numeric, AMR code and k404 PR searches return no result; the broader antipedal search returned only the distinct targets above. The target branch does not exist. Main commit histories for both established attempt-directory layouts are empty; the local all-ref target-path log is empty, and no related-target group contains this ID. The queue was queued 0/5.

The imported research report does exist and records a prior literature triage. It is upstream source material, not a prior Alec campaign attempt. Its negative literature conclusions are not adopted without verification.

## Source access and publication limits

Complete arXiv and published source PDFs/text and table images are held as local reading copies. Only mathematical work, code, provenance and checks will enter the public checkpoint. Complete imported records/reports and source PDFs/text/images are excluded. This source gate consumes no substantive author turn.
