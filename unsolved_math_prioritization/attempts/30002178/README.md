# 30002178: audited partial results for roots-of-unity lower bounds

**Unsolved; five of five approaches used.** This draft records independently
audited restricted deductions, not a proof or counterexample to the full target.
For each fixed number m of summands, a conductor-uniform polynomial lower bound
for every nonzero sum remains unproved, beginning with unrestricted m=5.

The retained results include elementary bounds for m<=4, paired-norm and prime
energy bounds, factored chord-product estimates, an exact prime counting
reformulation, and a Taylor estimate with an explicit exponent-spread threshold.
No averaged, exceptional-set, or existentially selected-prime result is promoted
to an individual bound for every prescribed common conductor. Finite enumeration
is corroboration only. Passing from a non-strict bound with a leading constant
to the strict eventual target requires exponent slack as explained in the proof.

## Package

- `author/` contains the 13 original author-freeze members, byte for byte.
- `audit/` contains the 14 independent-audit members, byte for byte.
- The two original ZIPs are preserved exactly and contain only those safe files.
- `PUBLICATION_STATUS.json` gives the current audited disposition.
- `PUBLICATION_MANIFEST.json` binds all other package files by SHA-256 and size.
- `verify_publication.py` checks both external archive anchors, exact extraction,
  manifests, disposition, and optionally replays all mathematical checks.
- `test_publication_integrity.py` mutates disposable copies and checks rejection.

The original author README and status predate the independent audit, so their
historical `pending` audit and `remote_writes: false` fields are preserved.
The audit's no-write fields likewise describe its original audit stage. Consult
the publication status and independent audit for the later disposition.

## Reproduce

Python 3 and SymPy 1.14.0 reproduce the author result bytes; the independent
checker uses only the Python standard library. Obtain the external publication
manifest SHA-256 from the draft PR description, then run from this directory:

    python verify_publication.py . EXPECTED_PUBLICATION_MANIFEST_SHA256 --replay
    python -O verify_publication.py . EXPECTED_PUBLICATION_MANIFEST_SHA256 --replay
    python test_publication_integrity.py
    python -O test_publication_integrity.py

The verifier uses disposable directories and writes no outputs into the package.
It is independent of the checkout location and current working directory.
The expected archive anchors are also embedded in the verifier and recorded in
the publication status; recomputing a hash of an untrusted replacement is not
an identity check.

Author checks: 67,380 over 46,803 normalized multisets, with 21 counting cases,
12 Taylor cases and eight semantic controls. Independent checks: 161,595 over
the same finite range, with 17 semantic/quantifier controls. Separate author,
audit and publication integrity tests check actual corruptions. These are local
verification results; zero GitHub CI checks does not mean CI passed.

## Source and publication scope

The primary OWR Conjecture 7 was directly inspected; the numeric problem website,
raw dataset row and prior AI reports remain uninspected. Public hashes in the
source metadata are scoped declarations or verified scholarly-PDF fingerprints
as explicitly identified there. No raw-record equality is claimed. No novelty,
complete prior resolution or global-openness claim is made.

This package contains authored proofs, audit, code, finite results and public
verification metadata. It excludes source PDFs, source extracts, rendered pages,
raw records, and private coordination material. The queue update changes only
this problem's Status to `unsolved` and Turns to `5/5`; every other byte is
preserved. This is a draft PR checkpoint, not a release or DOI publication.
