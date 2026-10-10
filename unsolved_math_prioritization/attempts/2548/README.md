# KOU-21.39: scoped partial results

UnsolvedMath **2548**, rank **767**. **Unsolved, 5/5 approaches.**

The original question asks whether a locally finite, characteristically simple group with finitely many element-orbits under its full automorphism group can fail to be residually finite. This package does not construct such a group or prove that none exists.

## Retained results

- Countable reflection preserves all target hypotheses and does not increase the orbit count, conditional on an ambient example already existing.
- Necessary conditions include finite exponent, perfectness, centerlessness, no nontrivial finite images, and finite commutator width.
- Pointed Cantor A5 functions give a characteristically simple, locally finite eight-orbit control, but are residually finite.
- The dense McLain construction has no finite images, but unbounded element orders prevent finite orbit count.
- An infinite extraspecial odd-p group has three orbits, but a proper characteristic center equal to its finite residual.
- A finite class-two amalgam obstruction and a conditional pseudofinite p-group exclusion rule out specific shortcuts only.

Read [the result](author/RESULT.md), [complete proofs](author/PROOFS.md), [five approaches](author/RESEARCH_LOG.md), [limitations](author/LIMITATIONS.md), and the [full independent audit](audit/AUDIT_REPORT.md). The audit gives a scoped PASS with [no mandatory correction](audit/CORRECTIONS.md). No novelty, human peer review, or formal proof-assistant certification is claimed.

## Frozen history and publication boundary

All ten author files and eight audit files are preserved byte-for-byte. Historical pending-review and no-remote-write fields describe those frozen stages. Current publication acceptance is recorded separately in [BINDING.json](BINDING.json); no historical field was rewritten.

The two ZIPs were newly created at publication from these frozen directories. Each contains exactly its corresponding directory's files with identical bytes, including its original manifest. No preexisting archive provenance is implied. Public source and dataset hashes, byte counts, inspection history, and manuscript-status metadata remain in their authored records. Source PDFs, source extractions/images, raw corpora, and private coordination are excluded.

The publication changes only this problem's Status and Turns cells in QUEUE.md. All other queue bytes, including the existing header, remain unchanged. This scoped draft does not regenerate the separate queue database or history files.

## Portable verification

Python 3.10 or newer; standard library only. From this directory run:

    python3 -I -B verify_publication.py
    python3 -I -B verify_publication.py --replay

The wrapper rejects optimized execution. Replay runs unoptimized, isolated subprocesses in a temporary relocated copy. It reproduces the author's 116,329 checks byte-for-byte and independently repeats 2,138,862 audit assertions, comparing all non-source results with the retained full audit output. The full historical 2,138,878-assertion output adds 16 optional source/corpus metadata checks; these are not claimed as freshly replayed from the portable package.

Every publication file, both original manifests, both archive inventories and contents are checked before and after replay. These finite controls support the scoped constructions; they do not settle the infinite-group existence question.
