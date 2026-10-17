# Corrections, superseded proposals, and version status

## 1. Dimension-one theorem: accept V2, not the original

The original 19,249-byte proof has SHA-256 `76e335e786c9a1f908bd671bd30110bfcb2cd991cc3352cccd9e1035207f5655`. It contains a real exceptional-case error: the empty-entry paragraph identifies D=N⁺ with N and invokes forward flow. It is not an accepted proof as written and is not included among this reader's current proof files.

The [corrected V2](proofs/ONE_DIMENSIONAL_ISOLATED_MOVABILITY_V2.md) is 19,573 bytes, SHA-256 `5a325bc382d9094bd50e13b8a17fbdf8151b31e56dc58e3e32af9355f8a0ca1c`. Exactly one paragraph changes. With empty entry E, every point remains in N for all backward time, so N=N⁻, whereas D=N⁺=K. Backward flow takes N into each target neighborhood for sufficiently large time, giving the required loop surjectivity without an entry-collar attachment.

The [authored correction patch](corrections/EMPTY_ENTRY_CORRECTION.patch) is 1,593 bytes, SHA-256 `91ad5980bd093fccf4d0466e2a45963712308d2d9d39b64543cb6d49b1ded9b4`. The independent audit verified that applying its one-paragraph replacement reproduces all of V2 exactly. The theorem's hypotheses and movability quantifiers are unchanged.

The [final acceptance](audits/DIMENSION_ONE_ACCEPTANCE.md) is 20,986 bytes, SHA-256 `24df75398dda97da9038ee94bf33495fb8eb1efd7d257002130e6fff58d3da0a`. Its verdict expressly accepts V2 and requires correction of the original. The full original is retained in the nonpublic preservation record. Neither the patch's removed text nor its hash should be read as acceptance of that original paragraph.

## 2. Satellite geometry and the later realization obstruction

The [satellite acceptance](audits/SATELLITE_ACCEPTANCE.md) records an already-applied inward-collar correction: the circles lie in the interiors of the relevant defining tori, so the proposed target sets really are open neighborhoods. It independently gives the explicit radius 7/8 construction. The current [satellite proof](proofs/SATELLITE_CIRCLE_AUDIT.md) uses interior satellite circles and the correct neighborhood argument.

Pass 1 proposed realizing this topological compactum as an isolated invariant set. It never established an actual flow realization. Pass 2's [finite-winding theorem](proofs/SATELLITE_ISOLATION_OBSTRUCTION.md) and [audit](audits/ISOLATION_OBSTRUCTION_ACCEPTANCE.md) rule out that specific isolated realization for every continuous full flow. Historical statements that it was “not constructed” must therefore not be mistaken for a still-open route for this same compactum.

The topological example addresses only the unqualified 2013 Hausdorff-circle sufficiency statement. An additional simultaneous-invariance interpretation was not refuted. That source limitation is explicit in the satellite audit and remains part of the conclusion.

## 3. Other accepted clarifications

- All possible B⊂R³ are finite dimensional. An early integrated report's suggestion that finite dimensionality was optional was corrected subsequently; the exact target in this reader is correct.
- “Free Ȟ¹ with no finite-rank assumption” alone did not establish an infinite-rank realization. The later stationary planar Hawaiian earring supplies one explicitly, and is movable.
- In the metric-threshold proof, “compact planar graphs” means graphs of continuous functions over planar compacta, not finite graph-theoretic objects or necessarily planar embedded subsets. The stationary singleton at the origin is the exception to the assertion about bounded nonstationary orbits lying in one shrinking copy's vertical hull.
- In the actual quotient argument, every neighborhood eventually contains the compact stopped-flow images. The images need not themselves be neighborhoods or ANRs. “Finite cohomology” in the abstract example means finitely generated integral groups Z and Z², not finite groups.
- Olędzki–Spież Corollary 3.5 is a pointed-shape realization statement, not a general embedding theorem. Bing's Theorem 8 supplies the needed actual solenoid embedding. The vertical-gap audit states the distinction and gives direct slab retractions.
- In the quadratic-wall example, smaller cores are movable by cap retraction but need not equal the stationary set. The coefficient of the quadratic contact is 1/98. The audit proves the stronger global no-boundary-segment assertion.
- The generic Hausdorff-continuity observation uses nonempty compact sets. The intersection identity also holds for empty cores; an empty limit under the common compact bound forces eventual emptiness. All cores in the final construction contain its nonempty stationary C.

These clarifications are supplied with their complete mathematical arguments in the corresponding independent reports; they do not broaden the accepted conclusions.

## 4. Editorial and audit identities

The dated authored proofs retain their original drafting-time “pending audit” sentences as historical text. Their completed status is given by [the index](PROOF_INDEX.md) and linked final audits. This never makes the superseded original dimension-one proof an accepted version.

All current proof files, the correction patch, and ten of the eleven audit files are byte-for-byte copies of their reviewed authored versions. The ambient-block acceptance differs only by removal of one local input-directory prefix; its basename, original input hash, mathematics, and citations are retained. [Artifact provenance](ARTIFACT_PROVENANCE.json) records both original and reader identities. The original ambient-audit hash in the dimension-one report intentionally refers to that original audited version, not to the editorially shortened reader copy.

The integrated operational reports, source bodies, extracts, and coordination records are not part of the public mathematical reader. A separate editorial record preserves the precise transformation and the full superseded original. Byte-integrity checks authenticate neither a source's claims nor the mathematical arguments; those require the actual proof and dependency review.
