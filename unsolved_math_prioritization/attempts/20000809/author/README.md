# Smooth Borel points and rational Hilbert components

Problem 20000809 / AIM-ARITHMETIC_GEOMETRY-0055, rank 758.

**Disposition: unresolved in the general projective interpretation. Five substantive approach families examined.** No general proof or qualifying nonrational counterexample is claimed. The original 2010 question asks whether a component containing a smooth Borel-fixed Hilbert point must be rational. The catalog's tangent-weight title describes an earlier partial report, not the original target.

## What this packet establishes

1. **A complete classical positive answer for finite-length subschemes.** In any affine dimension, every finite-colength monomial ideal is smoothable. If its point is smooth on the entire Hilbert scheme, its unique component is the rational smoothable component. The same conclusion holds for saturated Borel ideals of constant Hilbert polynomial in projective space. This uses classical distraction and an explicit interpolation chart; it is not a new theorem.
2. **A concrete failure of the prior report's proposed universal half-space hypothesis.** For every integer m >= 3, the saturated strongly stable ideal
   
   J_m = (x^2, x y^m, y^(m+1)) in k[x,y,z]
   
   is a smooth point of Hilb^(2m+1)(P^2), but its full diagonal-torus tangent representation contains both characters (-1,2,-1) and (1,-2,1). No diagonal one-parameter subgroup makes this point a source or sink. Its component is nevertheless rational.
3. **A necessary tangent-space correction.** At J_3, the actual projective Hilbert tangent space has dimension 14, whereas Hom_S(J_3,S/J_3)_0 has dimension 12. Use sheaf Hom, an affine neighbourhood of the support, or a sufficiently high truncation. The unqualified untruncated formula in the earlier report misses genuine tangent directions and can falsely pass a half-space test.
4. **Earlier relevant literature omitted from that report.** Bertone--Cioffi--Roggero's 2017 double-generic-initial theorem provides another sufficient rationality condition. It does not identify an arbitrary smooth Borel point with the double-generic point. The example here cannot be that point for the general seven-point component, by its quadratic Hilbert function.

The m=3 ideal and the entire odd-length family already occur in Cioffi--Lella--Marinari--Roggero, arXiv:1003.2951v1, Example 3.15(1) and Proposition 3.16; the example is credited there to Conca--Sidman (2005). The displayed weight calculation is an elementary consequence, not a priority or novelty claim. The valid BB/Gordan criterion is also standard and was already in the supplied prior report.

## Read and reproduce

- `PROOFS.md`: complete arguments for the claims above, with exact hypotheses and the general gap.
- `RESEARCH_REPORT.md`: source interpretation, prior-attempt corrections, five approaches, and bounded literature review.
- `sources.json`: public bibliographic and retrieval metadata, including actual downloaded PDF hashes and inspection scope.
- `provenance.json`: independently recomputed dataset hashes and target-record fingerprints; no dataset contents.
- `verify.py`: Python 3.10+ standard-library exact arithmetic controls.
- `verification.json`: deterministic control output (116 assertions, including five rejected false alternatives).
- `MANIFEST.json`: byte counts and SHA-256 hashes of the frozen authored files.
- `verify_packet.py`: integrity checks plus byte-for-byte control replay.

Run `python3 -B verify.py` from this folder, or invoke the script by an absolute path. It uses no current directory assumptions, network access, or third-party files. Compare its stdout byte-for-byte with `verification.json`, or run `python3 -B verify_packet.py` to check both integrity and replay. The controls supplement mathematical proofs; they do not certify the general question.

No primary PDFs, extracted source text, screenshots, dataset records, or private coordination material are included. This is an authored research/audit packet, not human peer review. Independent review is required before any publication; this author freeze itself makes no publication claim.
