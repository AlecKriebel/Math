# Littlewood small-value counting: scoped partials, 30003114

**Unsolved, 5/5 approaches. No full resolution or novelty claim.**

This preserves the eight-file author freeze and ten-file independent audit, together with both original ZIP archives. The audit accepts all five scoped partial arguments and requires no correction. The governing target concerns ternary coefficients, including zero, positive degree, and absolute value at each fixed reduced rational in [9/10,19/20]. One exponential constant must work independently of the denominator; only the positive prefactor may depend on the rational.

## Retained mathematics

- Exact rational evaluation injection and lattice counting prove the complete bounded-denominator case: for q<=Q, C=log Q and prefactor 1 leave only zero below the strict threshold.
- Lacunary conditioning gives a uniform count with exponent (21/22)log 3, substantially larger than the required 1/100.
- A collision lower bound forces C>=log 2-1/100 in any positive resolution. This does not exclude larger constants.
- Jensen, Blaschke products and Harnack give explicit analytic root localization. They do not count the different polynomials with nearby roots.
- Superincreasing products remain at least exp(-380) on the interval; origin shifts cost the factor (9/10)^d. This controls only the stated structured family.

Read [the complete proofs](safe_release/PROOF.md) and [the independent audit](audit_release/AUDIT.md) for hypotheses, quantifiers and exact gaps. The exact dataset already repairs missing modulus bars in printed sources; a literal-typography example is not a counterexample to the intended question. Finite enumeration, source inspection and literature checks have the limits recorded in those files. No global-openness certificate is claimed.

## Freeze identities

- Author archive: 16,914 bytes; SHA-256 443d5dc030e08c32e7a758c0eb1f5ab63eb8673f0a4dfd13930f2a60f568f228
- Author manifest: SHA-256 913457490b8f076c4a5035e6bcb32016a69dfe1a6c97a56ad396fc16882e23cf
- Audit archive: 27,071 bytes; SHA-256 09e9cffe79b52aadad8aaa263998b0326018abef8d01781fd41ae1774ce8a294
- Audit manifest: SHA-256 bfe47987a59ac1e9ec5f32527411a6ede96495ae42ebb647a6576a1a4c991cba

Historical pending-audit and no-remote-write labels inside the untouched freezes describe their creation checkpoints. The completed audit and this wrapper give the later disposition. Public source metadata is preserved; source PDFs, extracts, rendered pages, raw datasets, private sources and coordination are absent.

## Portable replay

From any working directory, run Python 3.9+ without optimization:

    python3 /path/to/30003114/verify_publication.py --expected-manifest <SHA256_FROM_PR> --queue /path/to/unsolved_math_prioritization/QUEUE.md

Use the independent publication-manifest pin recorded in the PR, rather than deriving a trust anchor from a mutable checkout. The wrapper verifies exact inventories, all hashes and sizes, both archive-to-directory identities and the optional queue bytes. It then replays the author with assertions enabled, byte-compares the saved result, replays the independent exact controls including temporary-copy corruption controls, and byte-compares that result. It also requires the deliberately false author assertion to fail.

The author script alone is assertion-based and must never be counted under optimization. The publication wrapper and independent verifier deliberately reject -O/-OO; those failures are negative execution controls, never positive mathematical verification. The standalone independent verifier can also run directly as described in its [README](audit_release/README.md).

## Queue scope

Exactly one row changes: rank 730 / 30003114, Status queued to unsolved and Turns 0/5 to 5/5. Findings, Chat, DOI and every other byte are preserved. PUBLICATION.json records hashes computed from the actual queue blob. Legacy SHA/size text embedded at its start is unchanged content, not the actual metadata.
