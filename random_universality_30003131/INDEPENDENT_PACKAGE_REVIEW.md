# Independent package review

Review date: 2026-10-21 UTC. Target: problem ID 30003131, source key
OWR-14604-008, the quadratic-length random-permutation universality question.

## Verdict

**PASS for the reviewed mathematical acceptance record, theorem scope, checker
hardening, and public-content boundary.** Two precision issues identified during
this review were corrected and the corrections were inspected: empty value
bands in the coupling explanation, and rejection of a symlinked manifest.
Neither changes the accepted quadratic-order conclusion.

This report was authored before final manifest generation. It does not certify
its own eventual hash or claim that a not-yet-generated final manifest was
verified. Final inventory, digest, and verifier runs are recorded separately.

## Mathematical review

The complete main proof in Chen and Wang's Theorem 1.1 and Section 3 was checked
against the independent reconstruction, as was the invoked proof of He and
Kwan's Lemma 2.2. The probability estimate and deterministic implication are
valid for simultaneous containment of every target permutation, not merely a
fixed target or an asymptotically large fraction of targets.

- The greedy scan queries a fresh column at each step. Padding after completion
  yields the stated binomial distribution without changing failure.
- Independence is assigned to fixed, disjoint support rectangles, not adaptive
  traces. A union bound over deterministic candidate independent subsets handles
  their eventual selection from the observed bad tests.
- The short-tuple good event is independent of the target permutation. The
  strip-counting contradiction therefore supplies all-pattern universality
  without an unaccounted-for factorial union bound.
- Empty value bands need not correspond to nonempty intervals of rank rows.
  The corrected audit uses the needed direct implication: an occupied cell has
  an actual point witness, and ordered column blocks and distinct ordered value
  bands lift any embedded permutation to the rank permutation. Empty bands are
  unused by such an embedding. Deleting them also makes the contraction
  description precise. The fair-bit stochastic domination argument is unchanged.
- The explicit conservative choice c=1/2352 for log(k)>=32 is consistent with
  the analytic estimates. Even the base exponential inequality can be justified
  without floating-point arithmetic: e^32 > 32^13/13! > 117600*32^3, since
  36893488147419103232 > 23995929266749440000. Monotonicity of e^x/x^3 for x>3
  propagates that bound.

The relative order of the first 32k^2 entries of a uniform permutation of length
1000k^2 is uniform, so the accepted theorem implies the original weaker
sufficiency question. The package correctly leaves the sharp coefficient 1/4
and the stronger conjectured failure exponent unresolved. It does not require
acceptance of the optional improved-constant sketch. The result is asymptotic;
no all-finite-k assertion is made. Mathematical acceptance, author attribution,
and absence of established journal acceptance are kept distinct.

## Executable checks and integrity boundary

Independent normal and optimized runs of check_audit.py exited successfully,
with outputs byte-identical to one another and to CHECK_RESULTS.json: 382 bytes,
SHA-256 4e6b3bf19af4cc11d91a8cc9fe8eb5ecef5b4f9b94e337e95c2f8233a3e9a3d6.
The 2036 support sets and the binomial-tail range 1 through 200 agree with the
reported finite tests.

All four original assert predicates were replaced by explicit RuntimeError
checks, preserving enforcement under python -O. The checker no longer rewrites
its frozen result. Its floating-point tail and base calculations are finite
sanity checks, not a formal or infinite proof certificate; the analytic review
is the source of mathematical acceptance.

The manifest verifier was inspected for inventory equality, duplicate or unsafe
names, regular-file and symlink checks, byte lengths, SHA-256 values, subprocess
failure handling, stderr rejection, and exact output comparison in both modes.
It now checks MANIFEST.json itself for regular-file/non-symlink status before
reading it. An external manifest digest remains necessary to detect coordinated
replacement of manifest and contents; the README states this limitation.

## Sanitation and evidence limits

The reviewed package contains authored explanations and code, public
bibliographic metadata, public-artifact fingerprints, and dataset identity/match
metadata. No copied scholarly PDF, extracted source text, dataset record,
private coordination material, private filesystem path, or personal data was
found. Source-artifact names in metadata are identifiers, not included files.

The local Chen-Wang and He-Kwan source PDFs were independently rehashed during
this review; their byte counts and digests match the corresponding metadata.
Other retrieval timestamps, original-page inspection history, and corpus match
results are the source gate's recorded evidence, not new retrievals or corpus
searches performed by this reviewer. The package correctly distinguishes
fresh hashing of existing corpora from fresh upstream downloads.

Primary mathematical sources:

- Chen and Wang: https://arxiv.org/pdf/2610.13530v1
- He and Kwan: https://arxiv.org/pdf/1911.12878v2
- Original problem report: https://ems.press/journals/owr/articles/14604

No queue or repository state was changed by this review.
