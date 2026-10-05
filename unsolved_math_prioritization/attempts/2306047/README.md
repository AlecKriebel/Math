# Function Theory 6.47: audited partial results

Target 2306047 / AMR-022-6047, rank 685. Disposition: **unsolved, 5/5 approaches exhausted**. This package does not solve the sharp coefficient problem and makes no novelty claim.

For normalized holomorphic functions on the open unit disk whose functions and first derivatives are both injective, the strongest unconditional audited result is the strict nonsharp bound `A_2 < (2+sqrt(13))/3`. The package also proves coefficient attainment, the correctly normalized derivative coefficient transfer, and two counterexamples to attempted proof strategies. These counterexamples do not settle the full source question.

The limit `2 exp(2 Catalan/pi)` is established for the explicitly defined analytic candidate. Its membership in the admissible class still depends on the inspected Hayman–Lingham report; the original Barnard–Suffridge proof was not inspected. Entire analyticity of the symmetrization example does not mean entire-plane injectivity: the injectivity statements are on the disk. No sharp maximum, optimality, exhaustive literature status, or proof that the problem remains globally open is certified.

## Read the evidence

- [Authored partial proofs](author/PROOF_PARTIALS.md)
- [Five approaches and exact remaining gaps](author/APPROACH_LOG.md)
- [Full independent adversarial audit](audit/INDEPENDENT_AUDIT.md)
- [Authored source metadata](author/SOURCE_VERIFICATION.json)
- [Independent source-check limitations](audit/AUDIT_SOURCE_METADATA.json)

The original eight author files and all five audit files are preserved byte-for-byte. Historical statements such as “audit pending” and “no remote writes” in the author freeze describe its earlier creation stage. The later audit certifies the partial-work disposition with no mandatory mathematical corrections. This publication does not rewrite those historical records.

## Reproduce

From this directory, run `python verify_publication.py --replay --selftest`. Python 3.10+ and SymPy 1.14.0 are required for exact stored-output replay. The integrity-only command `python verify_publication.py` uses the standard library. It verifies the strict inventory and immutable nested bindings.

Replay runs the frozen scripts from a temporary copy because they write result files beside themselves. It compares the generated files byte-for-byte with the frozen results: 48 author controls and 55 independent audit checks. `--selftest` checks rejection of corruption, unsafe paths, duplicate metadata, missing/extra files, empty directories, symlinks, changed dispositions, and altered proof limits. Finite controls support the written analytic proofs; they are not a formal proof certificate for global injectivity, compactness, sharpness, or candidate membership.

## Publication scope

Only authored mathematics, code, audit results, and public verification metadata are included. No downloaded PDF, source text, source images, dataset records, private source material, or private coordination files are included. Dataset corpus hashes remain reported historical metadata; no fresh full-corpus match is claimed.

The queue edit changes only this row's Status from `queued` to `unsolved` and Turns from `0/5` to `5/5`, retaining every other byte, including its existing header and links. The queue generator and other ledger files are untouched. No merge, release, DOI, or external outreach is part of this draft.
