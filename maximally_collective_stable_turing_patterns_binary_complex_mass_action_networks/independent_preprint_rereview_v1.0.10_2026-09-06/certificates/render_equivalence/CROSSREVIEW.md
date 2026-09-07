# Adversarial peer review of the conflicting coefficient-fields finding

Review timestamp: 2026-09-07 03:54 UTC. Bounded cross-review completion: 100%.

Verdict: confirmed. This is a semantic disagreement between two consumers of
one certificate row, not unused metadata. It affects rejection of malformed
inputs and synchronization of future generated tables. The actual shipped
coefficients remain correct, and the previous 50 rendering repairs remain
fully valid.

The witness adds `coefficient_in_U_ascending: ["1"]` to the spatial row with
powers `[6,1,0]`, preserving its correct `coefficient_in_A_ascending` value
`["8281/24300"]`. Both fields are recognized by the existing generator, which
gives the U field precedence whenever it is present (`generate_tables.py`,
lines 69–72). The direct mode reader consumes only the A field for this spatial
section (`frontier_verify_mode_certificates.py`, lines 229–235), as does the
exposition identity reader (`frontier_verify_exposition_identities.py`, lines
447–460).

Independent reruns confirmed that both reader functions accept this mutant.
The real generator was invoked independently and reproduces the saved mutant
table, where `8281/24300` becomes `1`. The independent exact TeX parser rejects
that table against the correct A-field coefficients at powers `(6,1,0)`.

An independent derivation using the real and imaginary parts of the displayed
F and G factors confirms that the generated polynomial minus the actual
modulus polynomial is exactly

\[
\frac{16019}{24300}x^6z.
\]

It separately confirms that the shipped A-field coefficients equal the actual
modulus polynomial exactly. The issue therefore introduces a false displayed
identity in the mutant even though all displayed coefficients are positive;
it does not falsify the true certificate or a headline theorem.

The saved full-symbolic and manuscript-audit logs report successful checks on
the mutant and regenerated source. The supplied PDF-gate result records a
successful scratch supplement rebuild and PDF semantic audit. I inspected
those artifacts, rather than rerunning the full suite or the TeX build. Source
inspection explains the containment failure: the printed-modulus freshness
check calls the same field-selecting generator
(`frontier_verify_exposition_identities.py`, lines 593–609), so freshness
against its output cannot distinguish this inconsistent interpretation.
The layout audit measures row counts, spacing, and required phrases; it is
not an independent polynomial identity check of the printed coefficients.

There is an important existing containment boundary: the unchanged release
manifest hashes detect both the mutated JSON and the changed table. The
independent script confirms that the two shipped files match those manifest
entries and both mutants differ. This finding does not demonstrate an
undetected modification of the immutable release or a hash bypass. It
demonstrates that regenerating the table from this input can preserve the
reported mathematical verification success while printing the wrong
coefficient.

A narrow repair is to require the section's designated coefficient field and
reject a conflicting recognized field in each row; generators should select
the coefficient parameter from the section contract rather than field
presence. A mutation regression should exercise both direct verification and
table generation with mixed recognized A/U fields. Arbitrary unused metadata
need not be rejected merely for being extra.

`crosscheck_conflicting_fields.py` and `CROSSREVIEW_RESULT.json` record the
independent execution and exact discrepancy. The script requires the project
Python environment with SymPy and performs no full replay, PDF build, source
edit, or release mutation.
