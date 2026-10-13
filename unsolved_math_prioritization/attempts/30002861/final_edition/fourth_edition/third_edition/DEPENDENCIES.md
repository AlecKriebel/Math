# Exact accepted dependencies for the third edition

The entire [second edition](second_edition/README.md) is retained without any byte change, including its eight first-edition files and their relative links. [Its content manifest](second_edition/CONTENT_MANIFEST.json) identifies its mathematical documents. The third edition's [content manifest](CONTENT_MANIFEST.json) identifies every retained dependency and new public file. File identities establish which mathematical text is meant; they do not prove its claims.

The first edition has an immutable [published revision](https://github.com/AlecKriebel/Math/blob/a4813752fdfb8d12cd04cb29237b9f9a7bc6aa09/unsolved_math_prioritization/attempts/30002861/README.md), associated with [PR 1328](https://github.com/AlecKriebel/Math/pull/1328). No second-edition published revision is asserted here. The retained accepted local mathematical edition supplies its exact dependencies independently of publication status.

## First edition mathematical baseline

- [QUARTIC_REDUCTION.md](second_edition/first_edition/QUARTIC_REDUCTION.md) gives the Bernstein parameterization, boundary fan elimination, singular-row treatment, exact Rm=Hj equivalence, active-component criterion, and moment identities.
- [CONVEX_SUPPORT.md](second_edition/first_edition/CONVEX_SUPPORT.md) gives zero-ray geometry, induced convex support, strict/straight boundary degree constraints, and the existence of at least three original nonsingular degree-four interior vertices in a closed component.
- [QUARTIC_AUDIT.md](second_edition/first_edition/QUARTIC_AUDIT.md) independently accepts those conclusions. The third-pass component proofs use its original-mesh degree-four statement and full-star consequence; they do not replace it by a degree condition in an arbitrary subcomplex.
- [CUBIC_PROOF.md](second_edition/first_edition/CUBIC_PROOF.md) and [CUBIC_AUDIT.md](second_edition/first_edition/CUBIC_AUDIT.md) retain the credited negative cubic answer. The new quartic proofs do not depend on its source coordinates.
- [SOURCES.md](second_edition/first_edition/SOURCES.md) and [SOURCE_METADATA.json](second_edition/first_edition/SOURCE_METADATA.json) retain exact dated source-inspection limits.

## Second edition mathematical baseline

- [SECOND_PASS_THEORY.md](second_edition/SECOND_PASS_THEORY.md), accepted by [THEORY_AUDIT.md](second_edition/THEORY_AUDIT.md), supplies automatic pure-gradient nonvanishing, the exact obstruction criterion, face-normalized weights, homogeneous signed-Ceva balance including infinity, and the one-way compact-quadratic construction. An arbitrary compact quadratic is not a converse to that construction.
- [SECOND_PASS_CONSTRUCTIONS.md](second_edition/SECOND_PASS_CONSTRUCTIONS.md), accepted by [CONSTRUCTION_AUDIT.md](second_edition/CONSTRUCTION_AUDIT.md), supplies actual exterior attachments and the strict five-corner lower bound. Its full eighteen-vertex face list is the full topology treated in the new pencil-collapse corollary.
- [SECOND_PASS_CERTIFICATE.json](second_edition/SECOND_PASS_CERTIFICATE.json), [FINITE_WITNESSES.json](second_edition/FINITE_WITNESSES.json), and [FINITE_AUDIT_CERTIFICATE.json](second_edition/FINITE_AUDIT_CERTIFICATE.json) specify and independently verify the authored sign-balanced but magnitude-unbalanced disk. The disk remains an interpolatory example, not a quartic counterexample. Its particular coordinates are unnecessary for the new nonsymmetric theorem.
- [REPRODUCTION.md](second_edition/REPRODUCTION.md) fixes the earlier rational matrix and full Bernstein conventions. No row-scaling convention or old certificate is silently changed by this edition.

## New dependency graph and historical scope

The [twelve-vertex proof](THIRD_PASS_CEVA_OBSTRUCTION.md) uses the reduction, convex support, face normalization, and actual exterior attachments. Its [audit](INDEPENDENT_RING_ACCEPTANCE.md) independently verifies those uses and the complete eighteen-vertex component argument.

The [nested-ring proof](THIRD_PASS_NESTED_RING_EXTENSION.md) uses that pencil-collapse lemma and boundary positivity, then proves a new local propagation lemma and finite induction. Its [audit](INDEPENDENT_NESTED_RING_ACCEPTANCE.md) retains the distinction between a complete closed core and a proper component in a larger full mesh.

The [corrected cofactor proof](COFACTOR_NORMAL_FORM.md) uses the specified quartic cofactor normalization and necessary compact-spline construction; its examples and normal form are derived explicitly. Its [audit](INDEPENDENT_COFACTOR_ACCEPTANCE.md) accepts only the corrected incident-segment formulation. [CORRECTION_NOTE.md](CORRECTION_NOTE.md) states the correction without treating the old literal wording as true.

The earlier files' pass counts, then-current remaining questions, and bounded source review are historical text. This third edition adds results but does not reinterpret old accepted scope, claim a new lifetime count, or promote a partial result into a solution of the whole row.
