# EP252 audit disposition

## Mathematical assessment

PASS within the stated mathematical and static-source inspection scope: the
complete reconstruction in MATHEMATICAL_AUDIT.md finds no mathematical gap in
Tokengrinder's prior argument for every integer k >= 0. The actual target is
the ordinary divisor-power factorial series, with convergence checked and
with the vanishing zero summand in the formal indexing explicitly reconciled.
The degree-zero argument is separate; the progression mean applies only for
k >= 1. The proof is unconditional and uses ordinary CRT progressions.

This assessment is an AI-assisted mathematical audit, not a new proof claim,
priority claim, human referee report, or journal acceptance. This authored
audit edition is unrefereed. The complete seven-step substantive reconstruction
is preserved, with editorial framing and historical-evidence labels only.
No mathematical correction is proposed.

## Formal assessment: HOLD_FORMAL_REPRODUCIBILITY

FORMAL REPRODUCIBILITY HOLD remains explicit and uncleared. No independent
Lean build was run. No complete transitive compiler/dependency/kernel closure
was independently established. No independent final-theorem axiom report or
fresh Lean-kernel replay was obtained. The author's build and axiom reports
remain attributed reports. Static source inspection, hash agreement and finite
Python tests do not substitute for those missing checks.

The project/toolchain pins are Lean 4.33.1 and official mathlib revision
0df444a360eaa60ab8c11dca51a86af692955474. The project manifest's eight inherited
package revisions match mathlib's manifest at that revision. This does not
verify compiler binaries, every transitive source, generated artifacts, or
imported oleans. The unrelated Generalizations library is excluded.

The missing advertised SHA256SUMS file is a documentation/reproducibility
defect. It does not supply a mathematical counterexample.

## Evidence needed to clear the formal hold

Obtain the exact pinned official toolchain and dependency revisions in an
isolated environment; inspect build hooks before execution. Rebuild the main
source from those bytes without inherited project artifacts and with trust
zero, then compile the six statement-audit results against the rebuilt module.
Preserve complete output, versions, source/artifact hashes, and the final
theorem's transitive axiom report. The author's advertised allowed axioms are
propext, Classical.choice and Quot.sound; this audit has not independently
obtained that report. A leanchecker replay uses Lean's own kernel and must not
be described as a second kernel implementation.

No such execution or installation occurred during edition preparation. The
historical finite checks remain bounded corroboration; the general mathematical
argument is the written reconstruction. This publication supplies authored
analysis and public metadata, not an executable reproduction package.
