# Function Theory 2.42: credited resolution and reconstructed example

This is a **new recovery freeze**, prepared on 2026-10-05 for problem 2302042
(AMR-022-2042, queue rank 675). It is not a byte-for-byte restoration of an
earlier packet. A fresh independent audit is required before publication.

## Result and attribution

The positive-ratio example is due to A. A. Gol'dberg and A. E. Eremenko,
*On asymptotic curves of entire functions of finite order*, Math. USSR-Sbornik
37(4) (1980), 509-533, Section 3, pp. 531-532. The reconstruction in PROOF.md
gives, for every integer n >= 2, an entire function with 2n distinct finite
asymptotic values and ratio 1/(2n) on each of 2n rays. Any desired finite
number l >= 2 of values can be selected by taking 2n >= l. No claim is made
that the function has exactly an arbitrary prescribed odd number of values.

Hayman and Lingham's 2018 draft, Update 2.42, attributes a complete answer
to Barsegyan and reports sum(b_k) <= 1 for entire functions, and <= 2 for
meromorphic functions. The entire-function bound rules out simultaneous
b_k = 1 when l >= 2. **Barsegyan's original proof was not inspected.** This
part is an attributed literature-status correction, not a newly verified
proof of that inequality. A bibliographic venue discrepancy remains.

Recommended disposition: already_solved, with the preceding source limitation
displayed. No novelty claim, journal-readiness claim, or inherited audit PASS
is made. The positive example is prior work and is included for transparent
verification.

## Contents and replay

- PROOF.md: exact scope and reconstructed positive example
- CLAIMS.json: machine-readable scope, formulas, and explicit limitations
- SOURCE_VERIFICATION.json: inspected sources, hashes, locations, and limits
- verify_exact.py: standard-library algebraic and scope checks
- CHECKS.json: deterministic output from the exact checks
- verify_manifest.py and MANIFEST.json: strict safe-file inventory

Run `python3 verify_exact.py` and `python3 verify_manifest.py` in this folder.
The same checks should also pass with `python3 -O`. They check encoded
identities and publication scope. They are not a formalization of the
complex-analysis proof and do not verify the uninspected Barsegyan theorem.

No source PDFs, extracted source text, raw dataset, or private coordination
files are included. Full upstream problem/report corpus byte verification was
not repeated during this recovery. Recorded dataset statement/review hashes
are catalog metadata, not fresh matches against original record bytes.

Provisional, AI-assisted research reconstruction prepared for Alec Kriebel.
Qualified expert review remains necessary.
