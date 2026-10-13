# Accepted mathematical dependencies and immutable first edition

The second edition depends on the following exact authored mathematical baseline. The files under first_edition are byte-preserved copies of all eight public first-edition files. Their relative links remain within that preserved directory. No first-edition file has been edited or superseded in place. The [published first edition](https://github.com/AlecKriebel/Math/blob/a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09/unsolved_math_prioritization/attempts/30002861/README.md) is pinned to immutable commit a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09; it was published in [PR 1328](https://github.com/AlecKriebel/Math/pull/1328). The preserved local copies have the same exact eight accepted file identities as that publication.

## Mathematical dependencies

1. [QUARTIC_REDUCTION.md](first_edition/QUARTIC_REDUCTION.md) supplies the full Bernstein parameterization, boundary-fan elimination, singular-row treatment, exact Rm=Hj equivalence, weighted active-component criterion, and local moment identities.
2. [CONVEX_SUPPORT.md](first_edition/CONVEX_SUPPORT.md) supplies the zero-ray geometry, convex induced-support theorem, support boundary structure, and at-least-three nonsingular degree-four vertices.
3. [QUARTIC_AUDIT.md](first_edition/QUARTIC_AUDIT.md) independently accepts both results. Its mathematical proof and conclusions are the baseline accepted by the second-pass audits. The first public edition removed implementation and preservation descriptions from one final reproducibility paragraph; the mathematical acceptance was unchanged.
4. [SOURCES.md](first_edition/SOURCES.md) and [SOURCE_METADATA.json](first_edition/SOURCE_METADATA.json) identify the public problem sources and the exact dated inspection limits. Those source inspections are inherited, not newly performed by this edition.

The [cubic proof](first_edition/CUBIC_PROOF.md) and [cubic audit](first_edition/CUBIC_AUDIT.md) retain the negative cubic answer credited to Qiu. They are included for the bundled row's complete context, but none of the new quartic proofs relies on Qiu's source coordinates or on the cubic rank computation.

## Exact first-edition file identities

The following SHA-256 identities and byte counts refer only to the public authored files listed here. They identify the immutable mathematical dependency versions. They are not mathematical proofs.

- [CONVEX_SUPPORT.md](first_edition/CONVEX_SUPPORT.md) ([immutable published copy](https://github.com/AlecKriebel/Math/blob/a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09/unsolved_math_prioritization/attempts/30002861/CONVEX_SUPPORT.md)): 16244 bytes; SHA-256 88383775684929d4f1845d4ef5905ee402a70045faa5558a22d02e3784bdd091
- [CUBIC_AUDIT.md](first_edition/CUBIC_AUDIT.md) ([immutable published copy](https://github.com/AlecKriebel/Math/blob/a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09/unsolved_math_prioritization/attempts/30002861/CUBIC_AUDIT.md)): 18253 bytes; SHA-256 e6b6d9fdf72e20ee70afa9816ec6fdcc5e92740e88ec5a8887b7ac050d7795eb
- [CUBIC_PROOF.md](first_edition/CUBIC_PROOF.md) ([immutable published copy](https://github.com/AlecKriebel/Math/blob/a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09/unsolved_math_prioritization/attempts/30002861/CUBIC_PROOF.md)): 12032 bytes; SHA-256 9bdebb3c39e4f43be1616b41ac282f93a7032bc6672da3d70d713217a892885b
- [QUARTIC_AUDIT.md](first_edition/QUARTIC_AUDIT.md) ([immutable published copy](https://github.com/AlecKriebel/Math/blob/a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09/unsolved_math_prioritization/attempts/30002861/QUARTIC_AUDIT.md)): 21735 bytes; SHA-256 5aa96b1cd66fe68030fe506044a95592208994b02f6edef2ef9b2176b0d80f06
- [QUARTIC_REDUCTION.md](first_edition/QUARTIC_REDUCTION.md) ([immutable published copy](https://github.com/AlecKriebel/Math/blob/a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09/unsolved_math_prioritization/attempts/30002861/QUARTIC_REDUCTION.md)): 13001 bytes; SHA-256 f6fa7b93c9b24f2d8020aa92f341394e2fff8417b82f883c33863b1ff6dc191b
- [README.md](first_edition/README.md) ([immutable published copy](https://github.com/AlecKriebel/Math/blob/a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09/unsolved_math_prioritization/attempts/30002861/README.md)): 5278 bytes; SHA-256 b03b0ad4c45a0edc890ed1e4a002c847b3efbbc8380fd4e1dce908dfbe31bdce
- [SOURCES.md](first_edition/SOURCES.md) ([immutable published copy](https://github.com/AlecKriebel/Math/blob/a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09/unsolved_math_prioritization/attempts/30002861/SOURCES.md)): 8194 bytes; SHA-256 04d4934f5f4df071bf8ebeb78feb154e9b86f517b2ca07bb190d629dcee3682c
- [SOURCE_METADATA.json](first_edition/SOURCE_METADATA.json) ([immutable published copy](https://github.com/AlecKriebel/Math/blob/a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09/unsolved_math_prioritization/attempts/30002861/SOURCE_METADATA.json)): 7662 bytes; SHA-256 06193363645629264e7256ef68e3440ea9ff070e1b8d088c38cf1cb6271b26d9

## Second edition dependency graph

The theory proof uses baseline items 1–3 and is reviewed by [THEORY_AUDIT.md](THEORY_AUDIT.md). The construction proof uses the same baseline; its five-corner theorem and symmetric-family exclusion are proved in full, and its finite example is specified in [SECOND_PASS_CERTIFICATE.json](SECOND_PASS_CERTIFICATE.json). [CONSTRUCTION_AUDIT.md](CONSTRUCTION_AUDIT.md) reviews that entire branch. [REPRODUCTION.md](REPRODUCTION.md) and [FINITE_WITNESSES.json](FINITE_WITNESSES.json) make the finite arithmetic independently auditable.

The baseline's local-jet qualification remains valid as a first-pass criterion. The second-pass theorem proves it automatic, using a degree-four vertex guaranteed by the baseline. The new argument does not assume the unresolved cycle-balance existence question. The known dimension formula is recovered from the accepted reduction and new nonvanishing proof; no uninspected historical proof is imported as a mathematical premise.
