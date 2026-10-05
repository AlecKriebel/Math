# Prior-resolution verification: matroidal amoeba dimension

Problem 30005479 / OWR-12697711-015; queue rank 652.

**Disposition: already_solved; 1/5 substantive turns.** The full affirmative
argument is attributed to Alper Ferudun, *The Amoeba Dimension of an Arbitrary
Loopless Matroid*, released 30 September 2026 as an expressly **unrefereed,
AI-assisted preprint**: <https://eulersolve.org/papers/owr-12697711-015/>.
This package claims no new theorem or priority, and its AI-assisted checks are
not human peer review or journal acceptance.

The equality is verified for every finite loopless matroid, with the minimum
taken over real or rational subspaces. An optimal partition supplies a rational
minimizer. The neighboring arbitrary-fan algorithm question remains outside scope.

- `author/`: all 12 frozen authored files, preserved byte-for-byte.
- `audit/`: all nine portable independent audit files, preserved byte-for-byte.
- `audit/AUDIT.md`: complete independent proof, hypothesis challenges, source
  limitations, and the nonoptimal-partition pitfall.
- `RELEASE_VERIFICATION.json`: publication-stage checks and bound inputs.
- `RELEASE_MANIFEST.json`, `verify_release.py`: strict inventory and byte checks.

The earlier author-stage request for a fresh audit is historical: the complete
independent audit now passes without required mathematical corrections.
The live UnsolvedMath catalogue remains unverified. The prior PDF's preserved
bytes were checked, but no independent match to the DOI archive is asserted.
Bernstein's nonempty-subset notation issue and the false equality for an
arbitrary nonoptimal partition are explained in the audit and do not undermine
the verified target or require changes to the frozen author packet.

## Portable verification

Requires Python 3.10+ and only its standard library. From any directory:

```sh
python3 path/to/30005479/verify_release.py
python3 path/to/30005479/verify_release.py --replay
```

The second command runs the author and independent verifiers and compares their
outputs byte-for-byte with the frozen regression results. It deliberately runs
mathematical verifiers with assertions enabled, even if this release wrapper is
invoked using `python3 -O`. Both positive and negative integrity tests were run
for the wrapper with and without optimization. Extra files, directories,
symlinks, missing payloads and changed bytes are rejected.

Finite checks supplement the universal proof; they do not establish arbitrary
matroid or subspace quantifiers. No third-party PDF, extracted source text,
rendered source page, corpus content, or private coordination file is included.
