# KP-1.65: audited local slicing diagnostic

**Problem 2724, rank 905. Status: unsolved / stalled partial. Attempts: 1/5.**

The accepted result is a bounded diagnostic, not a resolution of Kirby Problem 1.65. In the symplectization with contact form alpha = dz - y dx, the map

F(s,u) = (s,u,s,(s+1)u)

is an exact embedded local Lagrangian with primitive exp(s)u. Its height has no critical points, but every fixed-height slice has contact pullback du and is nowhere Legendrian. This disproves an automatic-slicing inference. The model has no compact cylindrical Legendrian ends and supplies no global counterexample or obstruction to an eventual Lagrangian isotopy.

## Accepted work and corrections

- [Corrected mathematical argument](corrected/MATHEMATICAL_AUDIT.md)
- [Corrected source comparison](corrected/SOURCE_AUDIT.md)
- [Exact acceptance](exact_acceptance/EXACT_ACCEPTANCE.md) and [bound artifact identities](exact_acceptance/EXACT_ACCEPTANCE.json)
- [Independent mathematical audit](independent_audit/audit/INDEPENDENT_AUDIT.md) and [primary-source scope review](independent_audit/audit/PRIMARY_SOURCE_REVIEW.md)
- [Actual correction patch](independent_audit/audit/CORRECTION.patch) and [recorded exact nine-file replay](independent_audit/audit/PATCH_REPLAY.json)
- [Single attempted route](corrected/ATTEMPT_LOG.md)
- [Publication metadata](PUBLICATION_METADATA.json), [replay results](PUBLICATION_REPLAY_RESULTS.json), and [publication manifest](PUBLICATION_MANIFEST.json)

The accepted corrected ZIP is 14001 bytes, SHA-256 1d578f1d9786c5dcf6ec51c81aef636bc68eae2f09f7a6ea7d3f7053f166ea43. The original author freeze is an immutable historical input, 13437 bytes, SHA-256 b497ff458b87d54ba733a05161b6c9e966356041308650180c7808e2662c83c6. Its original wording is superseded by the corrected derivative. Archives and corresponding external manifests are in [archives](archives/).

The correction explicitly retains Etnyre–Leverson's nonempty-end hypotheses, uses the Lagrangian concordances associated with Legendrian isotopies rather than arbitrary literal traces, paraphrases the target in the accepted exposition, and identifies Guadagni's displayed cap without asserting an isotopy-invariant obstruction. No mathematical attempt was added by the correction.

Global collaring, normalization into the permitted elementary pieces, and the required Lagrangian-isotopy conclusion remain unproved. No novelty claim, exhaustive literature-search claim, human peer review, or formal proof-assistant certification is made.

## Reproduce the checks

Run `python verify_publication.py` from this directory. Repeat with `python -O verify_publication.py` and `python -OO verify_publication.py`. The publication check verifies archive/member/manifest identities, exact extracted copies, status boundaries, and actual correction-patch application with deterministic regeneration of the internal manifest. It does not prove the global problem.

Run `python independent_audit/audit/verify_independent_audit.py --zip archives/LAGRANGIAN_ELEMENTARY_2724_CORRECTED_SAFE.zip --manifest archives/LAGRANGIAN_ELEMENTARY_2724_CORRECTED_EXTERNAL_MANIFEST.json` for the independent diagnostic audit. Repeat under -O and -OO. This includes the 135-check local diagnostic, relocated execution, direct false-premise tests, five semantic mutations, and artifact-integrity controls.

The optional `--catalog`, `--problems`, `--reports`, and `--source-directory` arguments allow privately supplied corpus and source-PDF pins to be checked. None of those external source files is distributed here. The included replay records identify when those checks were performed; a standalone run without those inputs explicitly reports them skipped.

The frozen author/audit files retain historical statements that publication and queue mutation had not occurred. They describe the freeze-time state. This publication changes only this problem's Status and Turns cells in the fresh base queue; all existing notes, chat links, and unrelated content remain byte-for-byte unchanged. The pull request is intended to remain draft, open, unmerged, with no auto-merge or release.
