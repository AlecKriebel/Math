# Corrected-release audit supplement

Problem **30006276 / OWR-14299284-004**.

**Verdict: accepted corrected release. The mathematical target remains unsolved.**

This supplement binds acceptance to the release SHA256SUMS digest:

    6e530df04a9bf69747646de41c6dfb3b7410576a2388843b6b754895a17339c6

The earlier audit and all frozen originals remain unchanged. This is a
correction-closure review, not a new literature search or a certificate of
the full multiplicativity conjecture.

## Correction closure

- **C1 closed.** Section 4 explicitly limits the annihilator and square-zero
  calculation to g>=2 and treats g=1 separately with I=0 and lambda_0=1.
  The formerly missing qualifier is now present before the lemma.
- **C2 closed.** Section 3.1 explicitly checks Deligne Proposition 8.2.7's
  hypotheses for the boundary normalization, obtains cohomological
  vanishing on the full boundary, and then uses the compact-support lift.
  The level cover, trace and division by its degree are stated.
- **C3 closed.** Section 5 specifies a Torelli-compatible compactification
  and the interpretation of extended pullbacks. It no longer implicitly
  requires every arbitrary smooth compactification to carry the extension.

No required correction from the original audit remains outstanding for
these exact release bytes. The preserved original audit's qualified verdict
is historical; this supplement records closure without altering it. The
release's frozen “binding pending” fields likewise record its preparation
state and are resolved by this external, hash-bound acceptance.

## Verification

A read-only binding verifier passes **485 assertions**. It checks:

- All 27 release checksum entries and the exact 28-file recursive inventory,
  including SHA256SUMS itself; no symlinks or unlisted files
- Byte-for-byte preservation of the complete original author and audit trees
- Correction-ledger hashes, file sizes and the release manifest
- Exact recomputation of CORRECTION_DIFF.patch from the five changed files
- The three amendments and unchanged remaining mathematical sections
- Preservation of every pre-existing RESULT.json field, including the exact
  target, unsolved status, remaining gaps, and absence of novelty/full-solution
  claims
- Both checker programs and their fixtures, followed by fresh successful
  execution from the corrected release

The fresh outputs are byte-identical to the preserved fixtures:

- Author: 5,250 assertions and 215,267 partition cases
- Independent audit: 2,736 assertions and 1,295,920 partition cases

The independent mathematical checker intentionally remains bound to the
preserved original author packet. The separate binding verifier checks the
corrected proof, ledger and entire release. Neither replay computes the
five geometric Torelli self-intersection integrals.

## Scope and preservation

The geometric left-hand sides remain unevaluated. No new claim of a genuine
A_g counterexample, general product vanishing, or characteristic-p
restriction-image theorem has been introduced. The fixed-fibre and abstract
ring controls retain their restricted logical roles.

The release contains only original exposition, code, result fixtures,
correction records and hash metadata. It contains no source PDFs or full
texts, imported catalogue corpus, private coordination records, or linked
private directories. Its complete inventory is recorded in
BINDING_CHECKS.json. The release inventory and hashes are identical before
and after this review. No remote write or release edit was performed.

## Reproduction

From the campaign directory, with Python and SymPy 1.14.0 available:

    python3 release-binding-audit/verify_binding.py > /tmp/release-binding.json
    diff -u release-binding-audit/BINDING_CHECKS.json /tmp/release-binding.json
    cd release-binding-audit && sha256sum -c SHA256SUMS

The acceptance applies only to the exact release digest above; a subsequent
release mutation requires a new binding check.
