# Green potential covering public safe version 2

Problem ID 2303023; rank 677; Hayman-Lingham Problem 3.23.
Disposition: already_solved, 1/5. Audit classification: already_solved1.

The cited [Hayman-Lingham Update 3.23](https://arxiv.org/pdf/1809.07200v2), printed p.67, records the prior affirmative answer. The cited manuscript is a draft dated 21 September 2018. This derivative retains the conditional deduction and complete lower examples. It makes no novelty or sharp-coefficient-27 claim.

For every normalized nonnegative Green potential or positive harmonic function on the unit disk, the strict superlevel set at t has a countable disk cover of total radius at most 1 for 0<=t<=28 and 27/(t-1) for t>28. The deduction also covers nonnegative superharmonic functions with u(0)=1, including infinite values away from the origin.

The explicit external premise is the whole-disk theorem attributed to Govorov in Eiderman, Theorem 4.2 and following A=9 paragraph, printed p.1315. For subharmonic v with v(0)>0 and 0<M=sup v<infinity, every P>1 admits a countable disk family of radius sum at most 1/P, outside which v>=-9PM. [Official publication record](https://www.mathnet.ru/eng/im166).

Every universal budget for either original class is at least 1/(t+1). Thus inverse-linear decay is the best possible order, while the best upper coefficient remains undetermined.

## Reading guide

1. [Authored deduction](author/PROOF.md).
2. [Complete exposition and lower examples](audit/DEDUCTION_AND_LOWER_BOUNDS.md).
3. [Current mathematical audit](audit/FULL_AUDIT.md) and [machine-readable verdict](audit/AUDIT_RESULT.json).
4. [Public citations and limits](author/SOURCE_AUDIT.md), [disposition](audit/CORRECTIONS_AND_DISPOSITION.md), and [version changes](PUBLIC_SAFE_CHANGES.md).

This version contains no source-retrieval evidence and performs no fresh source inspection. Eiderman's covering theorem remains an external premise; Govorov's original proof is not independently verified. No independent corpus-byte or exact-record verification is claimed. The review is an internal mathematical audit, not peer review or formal verification.

## Externally pinned portable replay

Requires Python 3 and SymPy. Before executing code, hash PUBLICATION_MANIFEST.json and verify every listed file, including the verifier and both archives, against the independently supplied version-2 acceptance and external pins. A matching manifest stored beside a changed program is not an independent trust anchor.

Then, from any working directory, run:

    python /path/to/package/verify_publication.py --expected-manifest-sha256 SHA256_FROM_EXTERNAL_PINS --negative-controls

The wrapper checks the externally pinned manifest, exact inventory, archive identities, archive-to-folder byte equality, author and audit manifests, and audit input bindings before running either checker. It reruns the 16,452 arithmetic assertions and 3,340 independent assertions, including seven mathematical error controls. It also tests altered, missing, extra, linked and misbound files, a rewritten manifest, and invalid ZIP inventories and members. No network or source cache is required. Dependencies are reported separately from mathematical report comparisons.

The external acceptance binds this whole package through its manifest. Its own hash is supplied in the external pins; neither file purports to hash itself. Public-safe author and audit archives are under archives/. No earlier archive is embedded. No remote change was performed by this derivative task.
