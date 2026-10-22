# Published scope and correction history

Checkpoint: 2026-10-03 20:18 UTC. Disposition: already_solved. Substantive investigation count: 1/5. Estimated completion of verifying the requested minimum and constructing an attaining map: 100%, relative to the explicitly named classical theorem inputs. Independent verification of all full-class equality cases is outside the completed scope.

The original minimum-area theorem is credited to Aharonov, Shapiro and Solynin (1999), DOI [10.1007/BF02791132](https://doi.org/10.1007/BF02791132), and its 2006 restatement. No novelty or priority is claimed.

The current [proof](PROOF.md) establishes the minimum and explicit attaining maps using the ordinary conformal-radius replacement comparison. The typically-real bound concerns Dirichlet energy, which equals ordinary image area for univalent maps. Full-class uniqueness for 1/2 < abs(a2) < 2 remains attributed to the published theorem and is not independently established here.

## Complete audit history

1. [Original audit: not passed](audit/ORIGINAL_AUDIT_NOT_PASSED.md). Attribution, the extremal, and the typically-real calculation passed, but a discrepancy between the 2001 OCR biangle inequality and the cited 1993 printed source blocked the full-class comparison.
2. [Narrow repair audit: pass](audit/REPAIR_AUDIT_PASS.md). The replacement was checked using authoritative ordinary-symmetrization page images, slit topology and inclusions, conformal-radius normalization and monotonicity, the coefficient limit, and radial exhaustion.

Both complete reports are retained verbatim. The old biangle-source discrepancy remains unresolved and unused. The unqualified original proof is superseded and is not included as a current proof. The reports refer to preserved research-stage integrity controls and an exact old/new diff; those inputs were reviewed before publication but are not part of this distribution. Source PDFs, page images and source transcripts are likewise not redistributed.

The [source gate](SOURCE_GATE.md) states which original texts, transcriptions and page images were inspected, and which classical theorems remain external inputs. The original 1999 proof remains unread; the 2001 and 2006 accessible texts were OCR. The ordinary conformal-radius theorem's exact authoritative displays were inspected as images.

## Reproduction

Run `python verify_exact.py` with SymPy 1.14.0. Its 16 exact checks should reproduce [verification.json](verification.json). They check the algebra and Taylor directions, not the geometric or analytic theorem inputs. `MANIFEST.sha256` binds the seven revised mathematical files; `PACKAGE_SHA256SUMS` additionally binds this scope note and the complete audit reports.
