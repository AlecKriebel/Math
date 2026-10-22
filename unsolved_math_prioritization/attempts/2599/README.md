# Kourovka 21.90: scoped partial results

UnsolvedMath **2599**, rank **770**. **Unsolved, 5/5 approaches completed.**

The primary problem asks for a Q-polynomial distance-regular graph of diameter three whose exact-distance-two and exact-distance-three graphs are strongly regular. The source does not explicitly require these distance graphs to be connected. The connected/nondegenerate interpretation studied here is inferred from the literature; it is not verified authorial intent.

## Results and remaining gap

- Crown graphs, including the six-cycle, satisfy the permissive convention allowing disconnected strongly regular graphs with μ=0. This exception is known in the 2019 literature and is not a new solution claim.
- Authored proofs recover the necessary parameter reduction and Q-polynomial equation, exclude primitive parameters with t≤3 or c=1, and provide five exact rational triple-intersection nonexistence certificates.
- A necessary-parameter sieve for 2≤t≤30 checks 959 triples: 159 pass the basic sieve and 154 remain after the five certificates. Survivors are neither constructed graphs nor claims that each array remains open in the literature.
- The connected/nondegenerate interpretation remains unresolved. There is no general construction, global nonexistence theorem or novelty claim.

## Controlling version and complete history

Start with [accepted v2](author_v2/README.md), [proofs](author_v2/PROOFS.md), [five-approach log](author_v2/RESEARCH_LOG.md), and [limitations](author_v2/LIMITATIONS.md).

The [original independent audit](audit_original/AUDIT_REPORT.md) passed the mathematics but required five wording replacements and one clarification sentence. Its historical correction-required verdict and the [exact correction list](audit_original/REQUIRED_CORRECTIONS.json) remain unchanged. The [v2 patch](author_v2/V1_TO_V2.patch) and [version provenance](author_v2/VERSION_PROVENANCE.json) record the entire revision. The later [delta acceptance](delta_acceptance/DELTA_ACCEPTANCE.md) accepts the exact pinned v2; no required corrections remain. This later acceptance governs the current payload.

All 48 frozen files and all four original ZIP archives are preserved byte-for-byte. Historical audit-pending and no-remote-write statements describe the frozen stages, not this publication. The original author payload remains in [author_original](author_original/) for provenance; its superseded intent wording must not be treated as the controlling account.

The independent audit records 155,035 standard-library checks, including adversarial controls, plus 46 supplementary symbolic identities. It is computational-assistant review, not human peer review or a proof-assistant formalization. Source inspections and retrieval limitations are retained in [source verification](author_v2/SOURCE_VERIFICATION.json) and [source audit](audit_original/SOURCE_AUDIT.json); external literature proofs were not comprehensively audited.

## Portable verification

Python 3 and SymPy 1.14.0 are used for full replay. From this directory:

    python3 -B verify_publication.py --replay --selftest
    python3 -O -B verify_publication.py --replay --selftest

Without --replay, verification needs only the standard library. The wrapper checks strict file/directory inventory, every hash and byte count, archive members, the four frozen manifests, version/scope binding, and archive-to-directory equality. Replay runs all author and independent mathematical programs plus the exact editorial-delta verifier in disposable copies, with assertions enabled even if the wrapper runs under -O. Generated files must reproduce exactly; the source payload is never modified.

Only authored proofs/code/certificates/results/audits and public verification metadata are added. Source PDFs, extracts, page images, raw dataset contents and private coordination material are excluded. QUEUE.md changes only this target's Status and Turns cells; every other byte, including the existing stale header and links, is preserved. No merge, release, DOI or outside contact is included.
