# Setwise asymptotic stationarity and coupling criteria

Problem ID 9900006 (AMR-098-0006), Thorisson Problem 3.2. Research and audit date: 2026-10-20. Intended repository directory: `setwise_stationarity_9900006`.

**Disposition: partial mathematical results; named problem UNSOLVED, 5/5 attempts.** This status does not deny the positive theorem: Attempt 3 proves a necessary-and-sufficient random-time coupling characterization of full-path setwise convergence on arbitrary measurable spaces. It preserves one original process and uses auxiliary stationary-law copies, with a separate construction for each deterministic subsequence. Whether this is the intended or novel resolution of Thorisson's named problem has not been established.

The source does not explicitly impose a single-pair requirement. We neither add that requirement to its wording nor claim that the present auxiliary-copy format has been accepted as its intended answer. No literature-priority or peer-review claim is made.

## Main result

Let θ be a measurable map on any measurable space, let μ be a probability, and let ν be θ-invariant. Then θ^n_*μ converges setwise to ν if and only if, for every strictly increasing sequence of nonnegative integers n_k, there is a common probability space with:

- one X with law μ;
- finitely supported random indices K_j≥j, whose entire sequence is independent of X;
- comparison variables Y_j with law ν;
- measurable success events H_j with P(H_j^c)≤2^{-j}, on which θ^{n_{K_j}}X=Y_j pointwise.

Thus exact equality holds eventually on a measurable event of probability one. The Y_j need not be independent or shifts of one stationary process. The construction may depend on the deterministic subsequence, but not on a measurable test event. The proof uses classical weak-L1 convexification and a common-part construction realized with independent uniforms and residual samples. It needs neither a measurable diagonal nor a disintegration theorem.

## Contents and reading order

1. [SCOPE.md](SCOPE.md): precise target, accepted conclusions, quantifiers, dependencies, and unresolved interpretation.
2. [ATTEMPT_3.md](ATTEMPT_3.md): the general auxiliary-copy random-time equivalence, including its explicit success-event construction.
3. [ATTEMPT_1.md](ATTEMPT_1.md): an explicit full-path setwise/non-TV Bernoulli-orbit example and an aligned coupling for that example. The counterexample answers neighboring Problem 3.1, not Problem 3.2 by substitution.
4. [ATTEMPT_2.md](ATTEMPT_2.md): a mixing rank-one obstruction to necessity of one fixed aligned-pair condition, extending the argument to arbitrary bistochastic couplings.
5. [ATTEMPT_4.md](ATTEMPT_4.md): fixed-target and fixed-pair quantifier obstructions.
6. [ATTEMPT_5.md](ATTEMPT_5.md): why this random-time criterion cannot drop universal subsequences or impose uniformly bounded sampling supports.
7. [COUPLING_CRITERIA.md](COUPLING_CRITERIA.md): a separate freely recoupled-sequence theorem under separability of a control-measure algebra.
8. [AUDIT.md](AUDIT.md) and [AUDIT_EXTENSIONS.md](AUDIT_EXTENSIONS.md): mathematical audit reports and resolved publication clarifications. These are authored mathematical checks, not certification of novelty or independent journal peer review.
9. [SOURCES.md](SOURCES.md): public references, source-inspection scope, imported theorem limits, and metadata for the original source PDF.
10. [MANIFEST.json](MANIFEST.json): SHA-256 and byte counts of every other package file; it excludes itself.

## Verification and publication boundaries

The substantive results are analytic proofs, not finite computations or machine-checked certificates. No computational verifier is needed or claimed for the general measurable-space statements. The manifest verifies file identity only, not mathematical truth.

The publication text incorporates the audit clarifications: nonnegative time indices; an explicit pointwise success-flag construction; sampling independent of the entire pair when the fixed-pair error is represented as a convex average; and the corrected statement that SC can hold while TV convergence fails, without an unsupported reverse implication.

This package contains authored proofs, audits, scope analysis, public citations, and verification metadata. It contains no source PDFs, reproduced scholarly papers, dataset contents, or private coordination material. Its preparation does not itself establish remote publication or change any repository status.
