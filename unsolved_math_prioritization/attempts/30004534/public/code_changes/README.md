# Checker packaging changes

The accepted PROOF.md and AUDIT.md and both historical result files are unchanged. The two checker scripts have only these explicit changes:

- Add argparse and an optional --output path. The default writes nothing. An explicitly requested output uses exclusive creation and never overwrites an existing file.
- Serialize the recomputed result exactly as before and compare its UTF-8 bytes with the included historical result before reporting success.
- In verify_independent.py, replace all nine Python assert statements with explicit require calls evaluating the identical condition and raising RuntimeError on failure. Validation therefore remains active under -O and -OO.

There are no mathematical algorithm, test-range, formula, expected-value, or optimization changes. Each .patch file is the exact unified diff from its original checker to the portable checker. PROVENANCE.json records both versions' SHA-256 hashes and byte counts. The original text can be reconstructed by reversing its diff.

Packaging verification compares the AST of every mathematical helper and the complete main-function computation through construction of the result. For the independent checker it first maps each original assert to its documented require call, preserving the condition's AST. The comparison deliberately excludes only the newly added CLI prefix and replaced output suffix. This is a finite source-equivalence check for these files, not a general program-equivalence theorem.
