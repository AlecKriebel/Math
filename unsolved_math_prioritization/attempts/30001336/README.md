# Rooted-tree expansion: independently audited partial results

**Problem 30001336 / OWR-4084-010, rank 825: unsolved, 5/5 substantive approaches.**

The [independent audit](audit/AUDIT_REPORT.md) accepts the retained scoped partials and requires no mathematical correction. It does not accept a solution of the original problem. The exact target is the continuous-index planar two-point expansion of the four-dimensional self-dual model, with its stated subtraction prescription and restricted joint-prefactor/rooted-integral coefficient class.

## Accepted scope

- The exact source coefficient recursion includes the quotient by G(0,a), both origin counterterms, the N subtraction, and the final nonlinear term. Construction is conditional on coefficientwise integrals and limits existing.
- Actual first-order source kernels and the published second-order coefficient are reconstructed. Low-order endpoint cancellation is justified.
- Every source-kernel rooted tree lies in the regular-at-zero harmonic-polylogarithm algebra with multiple-zeta coefficients.
- At every tree size, the divided difference of one tree is the tree formed by adding a leaf at its root plus a convergent MZV period. The all-size star family has the explicit factorial-zeta period.
- Forest leading-word matrices have exact full rational rank through weight 9, independently checked using two additional primes.

Read [model and recurrence](author/MODEL_AND_RECURRENCE.md), [rooted-kernel proofs](author/ROOTED_KERNEL_PARTIALS.md), and [five approaches and gaps](author/APPROACHES_AND_GAPS.md) together with the audit.

## Limits

The finite ranks prove only weights 1 through 9. No all-weight reverse-containment theorem is established. Single-tree divided-difference closure does not establish arbitrary mixed-rational forest closure. Low-order endpoint convergence does not prove all-order source integrability. The divergent L control a²+b² is a counterexample to an overly broad operator-domain claim, not an actual perturbative-coefficient counterexample.

The modern four-dimensional exact solution is credited; its auxiliary hypergeometric solution and two-point reconstruction do not automatically establish the specified restricted polynomial reduction. The earlier two-dimensional Lambert-W solution is distinct. The literature assessment is bounded by the inspected sources. No novelty, priority, exhaustive literature, human peer-review, or formal-proof certification claim is made.

## Preserved artifacts

The two ZIPs in [archives](archives/) and their extracted [author](author/) and [audit](audit/) members are unchanged. No correction patch is required. Any historical freeze-stage review or retrieval statements remain historical snapshots; the current acceptance is the scoped verdict above. PUBLICATION_METADATA.json records the pinned archive and manifest hashes. No source PDFs, copied source extracts, corpus contents, private sources, private personal data, or private coordination material are distributed.

## Replay

Python 3.10+, SymPy and mpmath are required. The tested versions are pinned in requirements.txt; dependency installations are outside the packet's integrity boundary. Author replay checks 177 exact identities and 27 numerical diagnostics; independent replay checks 62 exact identities and 26 numerical diagnostics. Numerical quadratures are reproducible diagnostics, not certified enclosures or all-size proofs.

Inspect the verifier and retain a trusted SHA-256 of PUBLICATION_MANIFEST.json independently. First verify its bytes against that trusted digest, then run from this directory:

    python -I -B verify_publication.py TRUSTED_MANIFEST_SHA256
    python -I -B verify_publication.py TRUSTED_MANIFEST_SHA256 --full
    python -I -O -B verify_publication.py TRUSTED_MANIFEST_SHA256 --full

The full replay verifies both strict inventories and exact ZIP/member equivalence before execution, and compares author/independent outputs with their frozen expected JSON. It runs the six mathematical mutation controls and eight inventory controls in normal and optimized Python through audit/replay_author.py. Mathematical mutations are deliberately reviewed changes; injected bytecode is rejected before execution. Relocate the entire directory for a relocation replay. The optional full-corpus verifier in audit/ takes separately supplied corpus paths; those corpora must remain outside this directory.

PUBLICATION_TEST_RESULTS.json records publication tests. Manifest hashes bind bytes and inventory; they cannot authenticate a coordinated replacement without the independently retained digest. Draft publication does not merge, release, create a DOI, or contact outside people.
