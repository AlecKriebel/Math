# Smooth embedded limits of complete intersections: partial results

Problem 20000814 (AIM-ARITHMETIC_GEOMETRY-0060), rank 759. **Unsolved, 5/5.**

The full characteristic-zero AIM Problem 13 remains unresolved by this packet. Reconstructed classical arguments prove the affirmative answer for every type CI(a,b) with a <= 3 and for type (4,4), without a novelty claim. Read the [report](author/REPORT.md), [proofs](author/PROOFS.md), and [independent audit](independent_audit/AUDIT.md). The audit passes precisely these partial results; it does not certify a complete resolution, global priority, human peer review, or formal proof-assistant verification.

A non-CI smooth special fiber would require an integral minimal containing surface of degree 3 <= c < a, a nonreduced lci auxiliary zero curve of degree (a-c)(b-c) > 1, and the mandatory fixed-factor equations through degree b. These necessary conditions neither exclude nor construct a remaining example, and an actual embedded smoothing to CI(a,b) is still required. A negative arithmetic genus is not a contradiction for a nonreduced auxiliary curve.

Two important precision points: the Serre bundle is constructed absolutely on the special P3; no relative bundle construction or specialization of splitting is claimed. The degree-one exclusion uses purity furnished by the lci zero-section construction.

The original author and independent-audit files and ZIP archives are preserved byte-for-byte. The author's pending-review wording and both packets' no-remote-write statements describe their historical freezes. The independent audit supplies the subsequent scoped acceptance. The full Ellia–Hartshorne 1999 chapter was not obtained or inspected; its citation is bibliographic, with no assertion about uninspected content or priority.

## Reproduce

Requires Python 3 and SymPy 1.14.0. From any working directory, run `python3 PATH/verify_publication.py` or `python3 -O PATH/verify_publication.py`. The read-only verifier checks the exact allowlist, frozen pins, manifests, both archive memberships, the declared scope, author replay, and the independent portable replay. The audit internally relocates the author program and checks ordinary and optimized execution.

PORTABLE_AUDIT_RESULTS.json is the publication-stage replay without optional corpus/PDF inputs. The frozen audit's verification_results.json instead records its historical full-input run, including private-local rehashing of public-source files. Those source files are deliberately not bundled. Finite arithmetic and metadata check counts are regression controls, not proofs of the geometric theorems. Runtime version fields in the portable replay must match the recorded environment for byte-exact equality.

Only the target queue row's Status and Turns change: unsolved, 5/5. Its Findings, Chat, DOI, historical embedded header and every other byte remain unchanged. No merge or release is included.
