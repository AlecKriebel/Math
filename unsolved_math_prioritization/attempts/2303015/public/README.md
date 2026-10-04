# Function Theory 3.15 partial-results packet

**Full problem unresolved. Proposed status: unsolved; approaches: 5/5.**

- RESULTS.md: complete proofs of the stated partials and exact remaining gap.
- APPROACHES.md: the five substantive approaches and stopping verdict.
- SOURCES.md and provenance.json: primary statement, literature limits,
  immutable source hashes, and live duplication checks.
- verify.py and verification.json: reproducible exact controls and their scope.
- SHA256SUMS: file manifest, excluding itself.

Run `python3 verify.py` and `sha256sum -c SHA256SUMS` from this directory.
Python 3.10+ with its standard library is sufficient. The controls do not
certify the continuum proofs or resolve the optimal-curve problem.

The strongest general bound proved here is a strictly positive, uniform gap
below the boundary harmonic interpolant when its value at the curve's marked
point is positive and the two marked points differ. The proof works for every
admissible curve, not merely smooth or radial ones. Exact answers are supplied
for all feasible cases where that harmonic value is nonpositive, for the
coincident-point case, and for the radial subclass.

No novelty or full-resolution claim is made. Boundary limits and regularity
conventions are stated in RESULTS.md; weakening them is outside this packet.
