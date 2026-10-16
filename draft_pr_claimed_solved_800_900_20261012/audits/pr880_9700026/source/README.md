# Literal city-ODE collapse conjecture: negative answer

Problem 9700026 / AMR-096-0026, rank 934. Draft research package, 6 October 2026.

## Exact accepted conclusion

The literal alpha > 1 collapse alternative in the 2007 fixed-site city ODE Conjecture 32(a) is false. For any finite number of at least two distinct interior sites and every positive initial probability vector, beta > 2 alpha gives uniform persistence. The asymmetric alpha=2, beta=8 three-city witness has every coordinate between 1/4096 and 2047/2048 for every t >= 0. This refutes the literal catalog conjunction, rather than merely identifying a heuristic concern or exceptional equilibrium.

The beta < 2 alpha collapse restriction, critical beta = 2 alpha case, convergence and uniqueness or initial-value independence of limiting equilibria, and stochastic models with new cities remain unresolved by this work. There is no claim of novelty, human peer review, or formal proof-assistant certification. The 2012 parameter-restricted stochastic paper is not refuted.

## Reading order

- [Author proof](author/PROOF.md) and [source distinction](author/SOURCE_AUDIT.md)
- [Independent audit A](audit_a/AUDIT_REPORT.md) and [exact acceptance](audit_a/ACCEPTANCE.json)
- [Independent review B](review_b/REVIEW_B.md) and [exact acceptance](review_b/ACCEPTANCE_B.json)
- [Publication scope and queue provenance](PUBLICATION_SCOPE.json)

Both mathematical/source reviews accept the same unchanged author bytes without repair. Each separately supplies a local-Lipschitz/trajectory-uniqueness supplement; equilibrium uniqueness remains open here. Historical pending-review labels inside the author freeze are preserved, with the later acceptance judgments kept separate.

## Reproducibility

The package includes both exact ZIP freezes, their external manifests, their expanded members, and the five unchanged review-B files. PUBLICATION_MANIFEST.json binds every other public member, including the wrapper. Its SHA-256 is published outside this directory in the draft PR description and the final verification receipt. Use that external value, not an untrusted replacement manifest's own claim.

Run from any directory with Python's standard library:

    python -I -B verify_publication.py --manifest-sha256 EXTERNALLY_PINNED_SHA256
    python -I -B -O verify_publication.py --manifest-sha256 EXTERNALLY_PINNED_SHA256

To also verify the separately held complete inputs:

    python -I -B verify_publication.py --manifest-sha256 EXTERNALLY_PINNED_SHA256 --corpus CORPUS_DIRECTORY --sources PDF_DIRECTORY

The corpus directory must contain catalog.json, problems.json, and research_results.json; the PDF directory must contain cities-notes.pdf and cities-2012.pdf matching the audit's public pins. A source-free run explicitly reports external inputs as NOT_RUN. Hashes and exact finite tests establish artifact identity, constants and algebra, not the analytic theorem or source interpretation.

Source documents and corpus contents are excluded from this package. Only authored mathematics, authored verification code, public citations and verification metadata are distributed. The repository QUEUE.md change is limited to this problem's Status, Turns and Findings cells, with all other bytes retained, including its historical sha:size prefix.

## Public sources

- [Aldous, 25 April 2007 technical notes, section 6.4 and Conjecture 32](https://www.stat.berkeley.edu/~aldous/Research/OP/cities-notes.pdf)
- [Aldous and Huang, A Spatial Model of City Growth and Formation, 2012](https://arxiv.org/abs/1209.5120v1)

Draft review stage only; no merge, release, DOI or third-party outreach is part of this package.
