# Public manuscript editing record

The current proof preserves every mathematical step of the independently audited manuscript. The contextual proof patch records its status update, the corrected FLO (4.5) locator (printed p.225), and the explicit equality between the kernel of unnormalized forward M and the image of reverse normalized N. No new mathematical proof approach was introduced.

The full independent audit and the separate narrow analytic audit retain all mathematical sections and their certification limits. Introductory workflow references and local input/receipt identifiers were removed. The latter audit still does not certify noninducedness; that part is certified by the full audit and all 15 Hall certificates. Historical diagnostic validation is retained as a narrative, with current public replay references.

The four checker adaptations remove file writes and input-path provenance and print the complete existing result, rather than a PASS-only summary. All mathematical operations are unchanged. The adaptation patches record those edits. A separate trusted isolated adapter enables the already-installed, version-checked SymPy 1.14.0 and mpmath 1.3.0 dependencies. No third-party package or source body is copied into this delivery.

The full superseded provisional proof is not included. Original inputs remain unchanged. No source PDFs, source text, dataset contents, private coordination records, or identifying metadata for excluded private files are included. Public scholarly PDF hashes and sizes are retained in the source metadata.

The analytic-checker I/O patch uses the neutral token PROOF_BYTES for the removed local-provenance expression; that editorial alias is documented here and is not executable checker code. The original-to-current exact diff remains outside the public packet. All mathematical lines are preserved.

The adapter records the exact captured inner stdout and stderr as verbatim UTF-8 JSON strings, with byte counts and SHA-256 values, beside the strictly interpreted result. Duplicate keys, nonfinite values, overflow, malformed JSON and trailing content are rejected. The verifier checks the entire raw adapter output and both inner streams against fixed references. Targeted controls reject whitespace-only changes and duplicate-key JSON that an ordinary decoder would map to the same object; these remain publication controls, not mathematical mutants.
