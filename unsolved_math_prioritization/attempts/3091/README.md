# Generalised empty hexagons: public mathematical derivative

**3091 / OPG-59923 · rank 1058 · exhausted, 5/5 · full target unresolved.**

The [complete mathematical report](packet/author/REPORT.md) and
[independent audit, public derivative](packet/audit/AUDIT.md) accept six elementary
partial results and explain the remaining obstruction in each of five attempted
routes. No mathematical correction was needed. The all-ell conjecture and ell=4
remain unresolved, and no novelty is asserted.

- Boundary blockers can be removed from an interior-empty strictly convex polygon.
- Perturbation yields a weak interior-empty six-set with a corner-loss obstruction.
- Deletion to general position gives the sufficient bound n >= 31d+30.
- Grid parity gives the conditional lower bound max(30, (ell-1)^2+1).
- Boundary-only sets satisfy a sufficient threshold 5(ell-2)+1.
- An occupied one-edge region of an empty pentagon produces an empty hexagon.

H=30, the bounded-collinearity pentagon theorem and the 29-point example remain
literature dependencies. No SAT replay, Lean build or independent witness
validation is claimed. See the [source audit](packet/author/SOURCE_AUDIT.md).

## Public-only scope and verification

This is a fresh public derivative, not a copy or integrity replay of an original
private packet. Original private research history, full-packet manifests/archive
identities and receipts covering excluded files are omitted. The
[derivation record](evidence/PUBLIC_DERIVATION.json) identifies only retained public
mathematics/code and permitted public metadata. The proof report, native geometry,
point fixtures and independent oracle are unchanged; the audit's proof-by-proof
review is preserved with its inventory/replay claims explicitly narrowed.

[Replay instructions](packet/README.md), [publication acceptance](ACCEPTANCE.md),
and the [complete delivery manifest](DELIVERY_MANIFEST.json) describe fresh public
manifests and the fixed external bootstrap. [Matrix evidence](evidence/MATRIX.json)
indexes the complete [normal](evidence/normal.stdout.json), [-O](evidence/O.stdout.json)
and [-OO](evidence/OO.stdout.json) native geometry/oracle outputs and semantic controls.
No original whole-packet integrity pass is claimed.

[Boundary controls](evidence/BOUNDARY_CONTROLS.json) cover fixed-bootstrap tampering,
strict JSON and hostile imports. [Optional-input controls](evidence/OPTIONAL_INPUT_CONTROLS.json)
reject missing/corrupt/symlinked inputs and correctly return NOT_RUN when absent.
[Public-input rehashes](evidence/CURRENT_PUBLIC_INPUT_REHASH.json) separately match
nine retained public sources and both public dataset files, without claiming a
renewed source inspection, download or record join.

No source documents, dataset bodies, private sources or coordination material,
or excluded private-file identifying metadata is included. The only queue edits
are this target's Status, Turns and Findings. No merge, release, DOI or outreach.

## Authenticate the entire delivery

Use DELIVERY_BOOTSTRAP.py, authenticated against the external SHA-256 in the PR
body. It binds all target files, including acceptance and evidence, and requires
the exact queue file. From this target directory:

    python3 -I -S -B DELIVERY_BOOTSTRAP.py . --queue ../../QUEUE.md --integrity-only

For full readonly replay, follow packet/README.md but invoke this delivery
entrypoint with --queue and omit --integrity-only. Full output comparison requires
Python 3.12.14. Every complete native/oracle/semantic result is compared against
pinned expected outputs, with no normalization. [Output-comparison controls](evidence/OUTPUT_COMPARISON_CONTROLS.json) test exact rejection of changed outputs.

The complete delivery manifest excludes only itself and its externally trusted
bootstrap. Every other delivered target file is bound. Final checks of this outer
anchor are recorded separately from the delivered files to avoid hash cycles.
