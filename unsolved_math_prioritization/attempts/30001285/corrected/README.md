# Comparison maps for central simple algebras

Problem 30001285 / OWR-3481-002, queue rank 972.

**Status: unsolved. Five substantive author approaches completed.** This is a source-free authored partial-results packet awaiting independent mathematical review. It does not claim a new general comparison theorem, a new counterexample to the full source-level request, or historical priority.

## Main outcome

A known Platonov–Suslin–Wouters example rules out recovering the r=1 geometric invariant by ordinary quotient projection from an unquotiented homomorphism. Kahn's exponent-two theorem identifies the different r=2 geometric invariant with c_A. These statements concern different coefficient arrows and are consistent. Neither computes the comparison with the étale Bloch–Lichtenbaum spectral-sequence map beta.

## Files

- STATEMENT.md fixes the source scope, hypotheses, maps and targets.
- COEFFICIENTS.md fixes the integral, finite and Q/Z presentations and separates projection, reduction and multiplication.
- RESULTS.md states the actual partial conclusions and the remaining gaps.
- TURN_1_LIFTING.md through TURN_5_SK2_SUSPENSION.md record the five mathematical approaches, including their failed or conditional steps.
- LITERATURE.md and SOURCES.json identify public sources and precisely what was inspected. Source PDF bytes, extracted text and corpus contents are excluded.
- CORPUS_METADATA.json records only supplied-corpus hashes, sizes and match counts.
- checks.py and CHECK_RESULTS.json provide 114,419 exact finite controls. They are not a verification of the imported motivic theorems.
- MANIFEST.json and verify_manifest.py identify this frozen file inventory. The manifest hash must be obtained separately; self-consistency alone does not authenticate it.

## Essential limits

The generic beta-minus-sigma class is unevaluated. The common product/sign normalization needed to apply approach 5 to those two specific families remains unverified. The source report supplies an SL_1-based SK_1 construction; this packet does not invent an analogous third SK_2 construction. The Q_5 example is only an SK_1 example and cannot be moved into the SK_2 argument with its algebraically closed-subfield hypothesis.

For review, pay particular attention to the use of the quotient cycle module and its bounded-torsion submodule in the generic-evaluation reduction, and to the imported index-annihilation statement for SK_2. These are credited theorem inputs, not conclusions of the finite checks.

Run the controls with Python 3: `python3 -I -S -B checks.py`. Verify the frozen inventory with `python3 -I -S -B verify_manifest.py --expected-manifest-sha256 THE_EXTERNALLY_SUPPLIED_HASH`. The verifier resolves files relative to its own directory and rejects additional files, symlinks and changed bytes.

AI tools were used extensively. This work is unrefereed, has not undergone human peer review, and is not a proof-assistant formalization. This author freeze does not publish source documents, push a repository, create a PR, merge, submit a paper, or perform external outreach.
