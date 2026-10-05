# Binary wreath shortest laws: audited partial results

Problem 1200005 (AMR-011-0005), rank 755. **Unsolved, 5/5. No complete candidate, general resolution, or novelty claim.**

The target is the minimum length of a nonempty reduced coefficient-free law in the automorphism group of the full finite rooted binary tree of depth n. Length counts every generator or inverse letter, expanding powers. All finite variable ranks are allowed in the full target.

The [unchanged author packet](author/README.md) gives proofs and exact finite certificates. The [independent adversarial audit](independent_audit/AUDIT.md) passes only these scoped partial claims, with no mandatory correction. This AI-assisted, unrefereed research documentation is not external human peer review or formal proof-assistant verification.

## Results and essential limits

- The general bounds are n < L_n <= 2^n. The constructive linear lower bound is credited to Bradford.
- The exact all-rank values are L_1=2, L_2=4 and L_3=8.
- The depth-four computation establishes only L_(4,2)=16 for words in two variables. It does not establish L_4=16 over arbitrary rank. A shorter balanced depth-four candidate can use as many as seven variables.
- Exponent, exponent-sum obstruction, parity, monotonicity, central half-powers and an exact recursive section criterion are proved. A literal universal half-length-section claim has a commutator obstruction. The central-power commutator has length 2^n+2 and does not improve the power law.
- Bradford indexes W_0=C2, hence W_n has n+1 factors. Here W_0 is trivial and W_n has n factors. Replacing the source index by n-1 gives the stated n < L_n.
- Qualitative lawlessness, infinite-group lawlessness growth and the later Hausdorff-dimension result do not settle this finite minimum. Finite computations provide no general asymptotic determination. No exhaustive current-worldwide-open-status or historical-priority certification is claimed.

The ten author files and original 21,562-byte ZIP, and the eight audit files, are byte-for-byte preserved. The author's pending-audit wording and both freezes' no-remote-write statements are historical snapshots. This wrapper records the subsequent independent scoped PASS and publication.

## Reproduce offline

Run `python3 verify_publication.py` here or invoke it by absolute path from any working directory. Python 3.10 or later and its standard library suffice. The wrapper checks the exact file and directory allowlists, pinned original files, archive membership, both original manifests and interpretation scope. It then replays the audit and author controls without network access. The audit produces 13,590 independent exact counterevaluations, checks the author certificates and performs the additional finite controls documented in its report.

`python3 -O verify_publication.py` is also supported: the wrapper's checks use explicit exceptions and force an ordinary child process with assertions enabled. Direct `python3 -O author/verify.py` or optimized `independent_audit/replay_audit.py` must reject execution; such rejection is a negative control, never a successful scientific replay. Do not run the frozen assertion-based author controls directly with optimization enabled.

Only the target row's Status and Turns change in QUEUE.md. The existing embedded header, all other rows, and the target Findings, Chat and DOI remain byte-identical. Source PDFs, source extracts, raw datasets and private coordination are excluded. No merge, release or outside outreach is part of this draft.
