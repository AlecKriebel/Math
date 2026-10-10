# Rooted-tree two-point expansion: scoped partial research

Problem 30001336 / OWR-4084-010, rank 825.

**Outcome: unresolved. Five bounded substantive approaches are documented.**
There is no all-orders proof of the source's restricted polynomial assertion and no counterexample to it. This packet is not an acceptance report for a solution and makes no novelty or priority claim.

The exact target is the continuous-index planar connected two-point function of the **four-dimensional self-dual** Grosse–Wulkenhaar model, with mass and wavefunction Taylor subtraction at zero. It is not the two-dimensional Lambert-W model.

Retained results:

1. An exact coefficient recursion for the source's renormalized equation, including the quotient and all subtraction terms. Its existence statement is conditional on the stated coefficientwise integrals and limits existing.
2. Explicit evaluation of the first-order integral operators and independent reconstruction of the published second-order coefficient.
3. A proof that every source-kernel rooted-tree integral belongs to the harmonic-polylogarithm algebra with multiple-zeta coefficients.
4. A proof that the divided-difference operator sends each single such tree to the tree obtained by adding a leaf at its root, plus a multiple-zeta period. The star-tree family has an explicit formula at every size.
5. Exact finite-field full-rank certificates for the leading-word spans of tree forests through weight 9. These establish only those nine finite-dimensional statements, not an all-weight theorem.
6. An explicit demonstration that the proposed whole polynomial ring, even restricted by the origin renormalization conditions, is not a domain on which every source operator exists. Actual perturbative coefficients need an additional endpoint-cancellation invariant.

Read MODEL_AND_RECURRENCE.md, ROOTED_KERNEL_PARTIALS.md and APPROACHES_AND_GAPS.md. Public bibliography and source identities are in SOURCES.json. No PDFs, extracted source text, complete imported problem records, credentials or private coordination material are included.

## Replay

Requires Python 3.10+, SymPy and mpmath. Tested with SymPy 1.14.0 and mpmath 1.3.0. These are exact algebra and high-precision numerical diagnostics; the written proofs are separate.

First inspect the code and independently verify MANIFEST.json against a trusted manifest hash. Then run:

    python -B verify_packet.py
    python -B verify_math.py
    python -O -B verify_math.py

The integrity verifier rejects unexpected files, directories, symlinks and other nonregular entries. It does not execute the mathematical verifier. Relocation needs only this directory. Comparison with expected_results.json occurs in the mathematical verifier. No network access or file writes occur during replay.

The author's freeze receipt is external to this directory. An independently obtained trusted manifest hash is necessary: a manifest cannot authenticate itself against coordinated replacement.

## Adversarial-check refinement

During author validation, changing the zero-letter transformation sign was not detected by finite rank alone. Direct signed-word and independent numerical K-on-Li₂ controls were added. The final checker rejects this mutation in normal and optimized mode. This illustrates why full finite ranks alone do not validate the underlying transformation.
