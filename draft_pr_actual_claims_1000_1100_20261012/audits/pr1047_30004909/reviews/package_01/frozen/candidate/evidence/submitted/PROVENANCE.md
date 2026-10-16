# Provenance of the proof-only edition

## Original source and mathematical scope

László Végh's contribution, *Open problem: Approximating submodular functions by matroid rank functions*, appears in *Combinatorial Optimization*, Oberwolfach Report 53/2021, printed p. 2946 (PDF page 54). The complete contribution was visually inspected in the mathematical/source audit; the next titled contribution immediately follows. It displays r(S)/alpha <= f(S) <= alpha r(S), requires normalized nonnegative monotone submodular f, and uses one matroid on the same ground set. It does not display weights, an expanded ground set or a scalar multiplier of the rank. Its sentence names the rank f while its formula uses r; the manuscript consistently uses r.

The corpus transcription omitted the lower denominator alpha. REPORT.md restores the source formula and disproves that weaker comparison itself. The word “constant” is interpreted dimension-independently; the source does not separately write a universal quantifier over V. The precise claim and all quantifiers are stated explicitly in the manuscript.

The manuscript gives complete elementary proofs for square-root cardinality and a rational-valued cardinality family, using a basis/full-set rank comparison. Uniform matroids attain the exact square-root-family optimum. The related Goemans–Harvey–Iwata–Mirrokni paper concerns oracle learning with a different output class, so its lower bounds are not treated as this argument or as an answer to the same question.

## Preservation and editorial selection

REPORT.md is preserved byte-for-byte. SOURCE_AUDIT.md retains all mathematical checks, original-source observations, literature-search limits and the accepted disposition. The only prose edit removes the private repository/corpus-history and deduplication passage, adds an explicit edition-selection notice, and retains the one-approach, 1/5 accounting. This is a narrowly edited audit, not a byte-identical copy. No mathematical or source-audit argument is shortened.

ARTIFACT_MANIFEST.json is a selected inventory for this edition, not the original computational inventory. It binds the actual REPORT.md, SOURCE_AUDIT.md and STATUS.json members while omitting script/output/private-history identities. STATUS.json is edition-level scope metadata and does not reproduce private deduplication history. SOURCE_PROVENANCE.json contains only public bibliographic, raw PDF identity, retrieval/inspection and bounded-search metadata. README.md, ACCEPTANCE.md and this document explain the edition. MANIFEST.json enumerates every edition member and hashes every member except itself, avoiding a circular self-hash.

The original publisher PDF's raw byte count and SHA-256 were independently rechecked against the inspected copy during preparation and match the audit. This verifies the identity of a public source copy; it neither extends the original source inspection nor certifies its mathematical statements. No source document is distributed.

## Proof-only boundary

The edition contains no executable code, computational fixtures, standalone checker output, execution logs, copied third-party PDFs, extracted source text, source renderings, dataset contents, private sources, private storage paths, private coordination, or hashes of those excluded materials. Raw public PDF identities are allowed bibliographic metadata. Every proof step remains in the written manuscript, and its universal claims do not depend on finite computational tests.

Exactly nine files are added under this problem's attempt directory. No QUEUE.md or unrelated file is changed. The additive patch and byte-identity checks establish packaging integrity only. The bounded literature search did not locate an exact prior presentation of this elementary obstruction, but it does not establish novelty, priority or exhaustive present literature status. The mathematical/source reviews are AI-assisted research audits, not external human peer review or formal proof certification.
