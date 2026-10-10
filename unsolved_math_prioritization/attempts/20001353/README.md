# Known maximal-subgroup examples in Thompson's group T

Problem **20001353 / AIM-DYNAMICAL_SYSTEMS-0011**, queue rank 512. **Known examples supplied: already_solved, 1/5**, scoped to the finite dyadic-set construction below. The recovered source request is open-ended; this does **not** classify all maximal subgroups or close the broader programme.

For every nonempty finite dyadic set A of cardinality k, its **setwise** stabilizer in classical T is maximal proper, has countably infinite index, and is isomorphic to F wr C_k. Different k give nonisomorphic subgroups. The full elementary proof passes a fresh independent audit, **PASS_SCOPED_KNOWN_EXAMPLES**, with no blocking mathematical finding.

## Essential attribution and access limits

The same theorem was already announced by Alper Ferudun in September 2026. **No novelty or priority is claimed.** The [EulerSolve landing page](https://eulersolve.org/papers/aim-dynamical-systems-0011/) was verified, but the earlier full PDF and verification report were inaccessible and were **not audited**. The proof here is a complete independent reconstruction.

The exact original request, “Find new maximal subgroups of infinite index in Thompson groups,” is recovered from a **pinned extraction**. The live original AIMPL page and catalogue page were unavailable. The official workshop report confirms context but does not reproduce this question. No fresh primary verification of the original sentence is claimed.

## Read the result and review

- [Complete self-contained proof](public/PROOF.md)
- [Source, prior work, and novelty gate](public/SOURCE_GATE.md)
- [Substantive attempt and early-stop rationale](public/RESEARCH_LOG.md)
- [Full independent mathematical/source audit](audit/AUDIT_REPORT.md)
- [Audit manifest](audit/AUDIT_MANIFEST.json)
- [Frozen author manifest](public/FROZEN_AUTHOR_MANIFEST.json)
- [Publication integrity manifest](PUBLICATION_MANIFEST.json)

All seven frozen author files and all six audit files are preserved byte-for-byte. Statements in the frozen author README that review is pending describe the pre-audit snapshot; the full audit and this entrypoint record the subsequent PASS.

## Reproduce the bounded checks

With Python 3's standard library, from this directory:

    python public/check_exact.py
    python audit/audit_controls.py

The author checks reproduce 59,629 exact assertions. The independent controls reproduce 41,290 assertions, including six negative controls. Both outputs replay byte-for-byte. These finite diagnostics supplement the universal written proof; they are not an exhaustive computation in the infinite group.

AI tools were used extensively for research, proof preparation, independent auditing, and verification. This is unrefereed work, without external human peer review or formal proof-assistant certification. Source PDFs, full-source text, corpus records, and private context are excluded. No merge, release, DOI creation, or external outreach is requested.
