# Acceptance report

Problem 30001812 / OWR-5158-013. 9 October 2026 UTC.

## Disposition

**Accepted partial theorem with the supplied presentation and diagnostic corrections.**

The original universal equality is **unresolved after 5/5 approaches**. The independent audit adds zero research turns. No strict counterexample was found by the frozen work; this audit does not launch a sixth search.

The accepted partial comparison is

    ||alpha||_1 <= G_X(alpha) <= (v_8/v_3) ||alpha||_1

for every topological space and real third-homology class. The exact integral stabilization, rational-to-real passage, suspension example, finite coloured pseudomanifold witness equivalence, and dual bounded-cocycle criterion are also accepted within the scopes stated in INDEPENDENT_AUDIT.md.

## Required corrections

Apply CORRECTIONS.patch to the three named files in a publication/staging copy of the frozen authored directory:

- Qualify connected-manifold rational realization by path connectedness; split arbitrary targets into the finitely many relevant path components.
- Attribute the symmetrization homotopy over R as in the source, and use the formula's preservation of rational chains. A rational homotopy is not needed.
- Make the finite support, Delta-pseudomanifold convention and component reasoning explicit; retain other cited theorems' actual hypotheses.
- Replace removable assertions in the original finite diagnostic with explicit exceptions. Its optimized-mode PASS was insufficient evidence.

The patch was actually applied to an independent staging copy, and all three resulting files matched the prepared corrected copies byte for byte. Original frozen files remain unchanged. No theorem constant or accepted proposition needs weakening.

## Verification

- All seven frozen authored sizes and SHA-256 values match before and after.
- All seven supplied scholarly PDF hashes/sizes match their recorded public metadata.
- Independent checker: normal, -O and -OO all pass; 80 exact chain cases per mode.
- Eleven actual algorithm/input mutations per mode: 33 correctly rejected.
- Actual frozen-input corruption: rejected in all three modes.
- Original false-assertion mutation: fails normally, incorrectly passes -O/-OO, reproducing the defect.
- Patched false-count mutation: fails in every mode.
- Actual non-root uid 1000 read-only runs: all three pass, including copied frozen inputs; six actual file-write attempts are denied with errno 13. The read-only copy and original frozen inputs remain unchanged.

These finite diagnostics are not a theorem prover. Mathematical acceptance rests on the complete proof audit and the primary-source interfaces. Source bytes prove byte identity only. No novelty, optimality, literature-exhaustion, equality, or strict-witness claim is accepted.

## Packet boundary

The authored directory contains only newly authored audit material, correction patches to authored material, executable diagnostics, and public verification metadata. It includes no source PDFs, extracted third-party source text, dataset contents, private sources, or private coordination records. This audit itself made no publication or queue changes.
