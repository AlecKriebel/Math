# Kähler-package Koszulness: scoped partial results

Problem 30005418 / OWR-12697689-014, rank 797.

**General target UNSOLVED; five of five approach families used. Independent audit PASS for the stated partial results and exact controls. No mathematical correction was required.**

Read `author/PROOF.md`, `independent_audit/AUDIT.md`, and `independent_audit/CORRECTIONS.md` together. The target asks whether a quadratic standard-graded real algebra with the full Kähler package is Koszul. The packet fixes a common real Lefschetz element, multiplication pairing, orientation, primitive spaces and signs. A full-package point yields a sufficiently small mixed cone for that fixed algebra. This is not an assertion on an arbitrary preassigned geometric cone or an arbitrary-field positivity theorem.

## Accepted scope

- A square-zero linear subspace of dimension at least two prevents degree-one HR.
- The credited quadratic Gorenstein idealization with Hilbert vector (1,8,8,1) is hard Lefschetz and non-Koszul; an exact rational off-diagonal bar-homology certificate proves non-Koszulness. It fails HR at every possible element and is not a target counterexample.
- The full assertion holds in socle degree at most two. An infinite explicit tensor family is Koszul and satisfies the full mixed package on its stated real cone. Uniform Gröbner and Lorentz-cone proofs establish these claims; finite samples are verification controls only.
- The cubic apolar control satisfies HR but is nonquadratic and is explicitly excluded from the target.

No construction simultaneously establishes quadraticity, full HR and non-Koszulness, and no argument covers all remaining socle degrees. The five-family limit is preserved. Known constructions and criteria retain their credit. No novelty, first-priority, universal resolution, formal verification or external human peer review is claimed.

## Immutable historical packets

`author/` and `independent_audit/` reproduce the exact contents of the original ZIP files in `archives/`. The author's audit-pending wording and the frozen no-remote-write statements describe their historical freeze stages. The later scoped PASS is supplied by the separate audit and this publication wrapper; the original files are unchanged.

## Portable replay

Use Python 3 with SymPy 1.14.0 installed. The author's checker uses only the standard library; the independent checker uses SymPy for exact characteristic-zero arithmetic.

    python3 -B /path/to/30005418/verify_publication.py --expected-manifest-sha256 PIN

PIN is the external SHA-256 of `PUBLICATION_MANIFEST.json` recorded in the draft PR. The wrapper verifies a closed recursive inventory, both exact ZIP hashes and all expanded members, and the externally bound author/audit manifests. It launches arithmetic in normal Python with assertions enabled, even when the outer wrapper is invoked with `-O` or `PYTHONOPTIMIZE` is set. A child assertion sentinel is checked before replay. The unchanged audit deliberately rejects direct `python -O` execution.

    python3 -B /path/to/30005418/test_publication_integrity.py --expected-manifest-sha256 PIN

Source PDFs, extracted text, images and all three complete source corpora/catalogs are excluded. Portable replay reports optional source-input rehashing as NOT_RUN_MISSING_OPTIONAL_SOURCE_INPUTS. Stored source results and inspection history are historical evidence; replay does not perform fresh source inspection or establish exhaustive literature coverage. To rehash separately obtained inputs, use the optional source scripts documented in the frozen READMEs.

Only authored mathematical proof/audit discussion, verification code, exact results, safe immutable archives and public verification metadata are distributed. The queue patch changes this row's Status and Turns only, preserving all other queue bytes, including the existing stale header. No merge, release, DOI or external outreach is part of this checkpoint.
