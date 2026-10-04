# Primary-source and target gate

## Identity and initial duplication check

- Numeric ID: 30001391; source code: OWR-4137-007.
- Catalogue title: Degree Bounds for Degenerate Herman Rings.
- Initial live queue rank: 616; row status queued; 0/5 turns.
- Initial live state has no target entry. The target attempt directory and README return 404. Searches of all PR states by the numeric ID and by Herman/rings returned no matches.
- The catalogue page was attempted directly; the web tool could not open it and a private HTTP retrieval returned 403. The exact row was therefore recovered from the supplied immutable corpus, whose SHA-256 is recorded in SOURCE_MANIFEST.json, and checked against the primary report. The inaccessible page is not described as read.
- The supplied research-results dictionary has no OWR-4137-007 entry. The separate related AMR reports were read as prior triage, not as proof certificates.

## Primary report

The source is *Mini-Workshop: The Escaping Set in Transcendental Dynamics*, Oberwolfach Report 54/2009, DOI 10.4171/OWR/2009/54, printed page 2958, Problem 2(2), attributed to W. Bergweiler. The workshop dates are December 6-12, 2009. The TIB-hosted PDF was downloaded privately, text-extracted, and the printed page visually inspected.

Problem 2's surrounding definition has all these features: analytic Jordan curve; periodic under f; an iterate acts as an orientation-preserving homeomorphism with irrational rotation number; exclusion from the closure of a Herman ring. Circles are allowed. The short question then asks for a degree-based count. It does not specify whether the count is of component curves or of cycles.

The paragraph does not explicitly exclude Siegel-disk level curves or require Julia-set membership. Immediately preceding Problem 1 explicitly explains the usual level curves in both Siegel disks and Herman rings and asks for other examples. This context strongly supports the intended exclusion of known rotation-domain curves. LITERAL_SCOPE_COUNTEREXAMPLE.md demonstrates the consequence of ignoring that context and is not used to mark the intended target solved.

## Later definitions and essential scope changes

Eremenko's *Analytic invariant curves for rational functions*, dated November 22, 2025, defines a degenerate Herman ring by Julia-set membership, exclusion of circles and rotation-domain boundaries, and conjugacy of f on the curve to an irrational rotation. Its Question 2 asks about finiteness and a degree bound. This is a useful current primary open-question witness, but its printed invariant-curve convention is not identical to the original periodic-curve formulation.

Yang's 2024 paper uses the noncircular Julia-set definition and proves the existence of smooth cubic examples. Smooth means C-infinity, not analytic. The paper explicitly leaves the analytic existence problem beyond its method. Lim's 2025 paper constructs bounded-type Herman quasicircles in a specified degree d0+d_infinity-1 family; its arbitrary combinatorics describe one curve's critical data, not an unbounded number of curves for a fixed map.

Three distinctions must survive any queue update:
1. Analytic curves in the 2009 report versus general Jordan/smooth/quasicircle versions in later work.
2. Individually invariant curves versus periodic component curves versus periodic cycles.
3. The literal omitted exclusion versus the intended Julia/rotation-domain exclusion.

## Exact result boundaries

PARTIAL_PROOF.md A addresses individually invariant curves under the explicit modern Julia-set and boundary exclusions. It is not asserted to settle the source's unrestricted periodic target. Part B addresses only spherical circles; part C only curves or cycles meeting Crit(f). The fixed-iterate corollary depends on L through d^L-1. The source's degree-only periodic bound remains unproved here.

The 2025 note's literal invariant wording is close to Part A, so the restricted argument may be useful for that separate formulation. However, the possibility of an implicit periodic/cycle convention, the need for independent audit, and unestablished novelty prevent any promotion of the full original target. No inference of current openness rests only on a search failure.

## Related targets

- 30001390 / OWR-4137-006: analytic noncircular existence. Yang's smooth construction does not settle it.
- 3700007 / AMR-036-0007: analytic existence under later exclusions.
- 3700008 / AMR-036-0008: later counting/finiteness formulation; check invariant versus periodic convention before reusing Part A.

These are related formulations and shared obstructions, not separate discoveries. No related queue row was changed.
