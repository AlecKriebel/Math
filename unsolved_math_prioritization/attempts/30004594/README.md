# Contact-process threshold separation: audited partial results

Problem 30004594 / OWR-4990373-008, rank 780. **UNSOLVED, 5/5 substantive approaches; budget exhausted.** The original nearest-neighbor lattice question is not settled. Best-guess completion toward its full proof remains the author's 0% estimate, not a probability of correctness.

## Retained scope

The unchanged author packet supplies a credited Bernoulli upper comparison and one-dimensional boundary case, exact stationary moment identities, an explicit vanishing-density percolating field outside the contact-process family, a finite-radius graphical criterion and a narrowly scoped obstruction to that criterion, an embedding obstruction, and a 511-state exact dual-exit calculation.

The no-go theorem uses **total infection rate lambda >= 1**, with recovery rate one. If b is the per-neighbor arrow rate, b=lambda/(2d), so the same range is b >= 1/(2d). It concerns only the specified singleton dual-exit / independent color-class / path-union-bound certificate. It does not prove actual spatial percolation or impossibility of every renormalization method. The essential gap is unchanged: no rate strictly above survival is certified spatially nonpercolating for the actual nearest-neighbor process on every Z^d, d>=2.

## Independent review and preserved freezes

`audit/FULL_AUDIT.md` and `audit/CORRECTIONS.md` record PASS_RETAINED_PARTIALS_FULL_AUDIT with no mandatory mathematical correction. Historical author statements that review is pending remain unchanged. The later independent audit supplies the current reviewed disposition; no file inside either freeze was edited. No novelty, formal proof-assistant verification, human peer review, proposer acceptance or full-resolution claim is made.

`author/` contains the exact ten-file author freeze; `audit/` contains the exact twelve-file independent-audit freeze. `frozen_archives/` holds canonical base64 encodings of their original ZIP bytes. The verifier decodes and checks every archive member, CRC, size and hash against the preserved directories.

## Provenance qualifications

The descriptor review hash was independently recalculated using the repository importer's empty-object convention for an absent prior report. Publication-time complete cached corpus and catalog bytes were additionally bound to fresh immutable-main metadata; see `SOURCE_BINDING.json`.

All six stored source PDFs match their frozen metadata. The independent audit's five fresh core-PDF downloads match byte-for-byte. The supplementary Chalmers PDF has retrieval-dependent timestamp bytes, so the fresh PDF hashes differ. Its entire extracted text matches only after omission of the sole changed download-timestamp line. Do not describe all live PDF hashes as matching. See `audit/source_retrieval_audit.json`. No source PDFs, extracts, images, raw corpora, raw API responses or private coordination records are distributed.

## Reproduce without external inputs

Python 3.10+, standard library only. From any working directory:

    python /path/to/packet/verify_publication.py
    python /path/to/packet/test_publication_integrity.py

The read-only verifier checks exact recursive inventory, publication hashes, both frozen manifests and archives, then reproduces the author's 72,940 controls and the independent audit's 875,433 controls byte-for-byte. The independent count includes 343,400 Bareiss exact-division assertions. Assertions remain enabled. The executable rejects optimized Python mode. These finite exact controls support the written partial proofs; they are not an infinite-volume threshold-separation certificate or a measure of proof reliability.

For optional historical provenance replay, run `audit/audit_provenance.py --help` and supply its separately obtained full inputs. The portable verification command reports this external-input stage NOT_RUN_EXTERNAL_INPUTS_REQUIRED; it does not silently treat missing inputs as a pass. Its frozen prior result is evidence of the earlier audit, not a new replay.

## Repository scope

This single draft PR changes only this target row's Status from queued to unsolved and Turns from 0/5 to 5/5 in QUEUE.md. Findings, Chat, DOI, the stale embedded header and every other byte are preserved. Historical catalogs, assessments, queue state and other targets remain untouched. No merge, release, DOI creation or outreach is part of this publication. No hosted-CI pass is claimed.
