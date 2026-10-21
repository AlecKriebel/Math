# Independent package acceptance audit

Date: 2026-10-21 UTC. Decision: PASS for publication as accepted partial results, subject to the final complete manifest verification recorded in the external freeze receipt. This audit does not change the problem's UNSOLVED status.

## Mathematics and editorial changes

The original independent mathematical audit remains valid. The package proof reports were compared against the audited versions. The arithmetic-gap report is unchanged. Changes in the projective-equivalence report mark its accepted status, specify projective algebraic sets need not be irreducible, and explicitly link the complete rational Veronese inverse proof. Changes to the original audit clarify that its execution covered the original checker and remove irrelevant operational narration. None changes a mathematical argument.

FIVE_AVENUES.md was independently reviewed as a final editorial synthesis rather than a verbatim historical log. It accurately replaces the provisional absence of a converse reduction and arithmetic gap with the final accepted results. It retains the limitations of the failed lattice and rank approaches and does not include unaudited low-dimensional algorithms or unrelated optimization lemmas.

README.md, FIVE_AVENUES.md, the proof reports, and the audits consistently limit the result to effective finite oracle equivalence for arbitrary finite rational fans, not a polynomial-time bound, unconditional terminating algorithm, or undecidability theorem. The explicit arithmetic example is nonpure. No extension to pure, balanced, matroid-realizable, or irreducible-tropical inputs is established. Source-gate discussion distinguishes the adjacent linear-space and matroid questions and labels the later matroid manuscript unrefereed and not proof-audited here.

## Checker hardening and independent executions

AST comparison established that all ten original assert predicates occur, in the same order and with identical expression trees, as the first ten explicit check calls. Every original mathematical assignment has an identical AST in the hardened checker. The checker contains no Python assert statements. Its check function raises RuntimeError explicitly, so optimization does not remove the guards. Added checks validate graph consistency and the cone formulas and inequalities, not a new mathematical claim.

The supplied control harness was independently executed successfully. In each of normal and optimized Python, the positive exact checks and full manifest validation passed. Four negative controls changed actual mathematical inputs: the graph coefficient, a real witness coefficient, the arrow matrix, and an H-cone generator coefficient. Each failed an explicit mathematical guard without relying on a manifest mismatch. Five further controls changed file bytes, removed a file, added an unexpected file, falsified a digest, and falsified a byte count. Each failed manifest validation. Thus all 18 supplied negative executions rejected correctly.

Review found and corrected an inventory edge case: only the root manifest itself should be excluded, rather than every file with the same basename. The corrected checker was additionally tested against an unexpected nested MANIFEST.json under both normal and optimized Python; both rejected it through the inventory check. These two additional tests are separate from the 18 supplied controls. Python bytecode caches remain intentionally excluded as documented.

Finite computations verify the displayed matrices and data, not the exclusion of every rational threshold witness. The universal proofs establish the rational lower bound, real/rational gap, anchor reduction, and rational-point equivalence. The manifest is an integrity inventory, not a signature or independent guarantee of authenticity.

## Sanitization and provenance

The package was checked for unexpected file types, symlinks, local absolute paths, private coordination references, and private conversation links. No such content was found. Only authored mathematical reports, executable checks, public bibliographic/retrieval metadata, and integrity metadata are included. No source PDFs, extracted source text, dataset contents, page images, or private coordination files are included.

The five public source metadata entries were independently checked against the previously retrieved source bytes: every recorded size and SHA-256 matched. This verifies prior retrieval provenance and is not a claim that those sources were freshly downloaded during packaging. Dataset metadata describes existing corpus hashing rather than a fresh download. The Reineke construction was inspected as described in the mathematical audit; no unrecorded PDF hash is claimed for it.

## Freeze condition

After adding this audit, regenerate MANIFEST.json to include every package file other than the root manifest itself and documented bytecode caches. Then rerun positive normal/optimized executions and the control harness. Record the resulting manifest SHA-256 and exact file inventory in the external receipt. No hash is embedded here because doing so would create a self-referential hash dependency. Any later substantive change requires renewed review and a new freeze receipt.
