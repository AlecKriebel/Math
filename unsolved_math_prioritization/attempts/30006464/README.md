# Short coefficient detection: audited scoped partial

Problem **30006464 / OWR-14299577-017**, rank 831. **Unsolved, 5/5 approaches.** The original all-forms, all-levels positive-epsilon question remains open in this work. This AI-assisted report is unrefereed and makes no novelty or priority claim.

## Mandatory correction and accepted scope

**Read the unchanged [proof](author/PROOFS.md) together with the operative [d=0 correction](audit/GRAM_ZERO_DIMENSION.patch), its [exact before/after binding](audit/CORRECTION.json), and the [precision addendum](audit/PRECISION_ADDENDUM.md).** The least-Gram-eigenvalue language applies only when the cusp space has positive dimension. For dimension zero, the detection inequality is vacuous and the quadratic-form formulation remains meaningful. The actual patch is applied and replayed on a disposable copy; no changed derivative is published. Both frozen ZIPs and all extracted members remain byte-for-byte unchanged.

For every epsilon>0 and every integer N>=1, the accepted positive partial is

    H_N(c Delta(Nz)) <= H_1(Delta) max(1,8 log(2)/(3 epsilon))
                         S_{c Delta(Nz)}(4 N^(1+epsilon)).

Here H_N is the unnormalized Petersson integral and a_f(n) is the raw Fourier coefficient divided by n^((k-1)/2). The theorem covers the one-dimensional weight-12 family c Delta(Nz) at every level, including nonsquarefree levels. It does not cover arbitrary mixtures or every cusp form. The same family obstructs a fixed linear cutoff CN, which concerns epsilon=0 only and does not contradict the positive-epsilon question.

The finite-frame criterion and exponent-family horostrip equivalence isolate the exact remaining uniform lower bound. The cancellation model and geometric domain test reject particular shortcuts; neither is a counterexample to the original problem or to the cited exponent-2 theorem.

## Evidence and historical record

- [Five attempted approaches](author/APPROACHES.md)
- [Independent mathematical audit](audit/AUDIT.md)
- [Frozen audit results](audit/AUDIT_RESULTS.json)
- [Fresh full-byte source and corpus checks](SOURCE_CORPUS_CHECKS.json)
- [Archive identities and scope](PUBLICATION_METADATA.json)
- [Exact two-cell queue delta](QUEUE_DELTA.json)

The author has 790 exact finite controls and 18 corruption cases; the independent audit has 7,769 exact finite controls and 26 corruption cases. Each corruption case is rejected under normal and optimized Python. Finite controls supplement the written analysis; they are not formal proof certification. Earlier pending-review/no-publication statements are preserved as historical records.

## Operative publication verification

First obtain the wrapper and publication-manifest SHA-256 pins from the draft PR acceptance receipt and check the wrapper hash using a trusted local hash utility. Use an ordinary nonsymlinked directory and run:

    python3 -I -B verify_publication.py --expected-manifest EXPECTED_SHA256
    python3 -I -B -O verify_publication.py --expected-manifest EXPECTED_SHA256
    python3 -I -B test_publication.py --expected-manifest EXPECTED_SHA256 --full-relocation

The wrapper checks invocation ancestry, strict recursive regular-file inventory, the external manifest pin, all file hashes, both hard-pinned ZIPs, exact archive inventories and every extracted byte before launching any frozen executable. The frozen verifiers resolve their own pathname; use this wrapper as the entrypoint so symlinked invocations cannot silently select a different genuine tree. Checks run in isolated Python with bytecode writes disabled. Actual patch replay uses the system patch command in a temporary copy, checks the corrected proof hash, reseals only that copy, and runs normal/-O verifiers and the author mutation/relocation suite. No patch touches the freezes.

The wrapper's adversarial controls include symlinked roots, ancestors, entrypoints and files; malformed manifests; extra and missing entries; bytecode/import shadows; corrupted archives; and resealed scope/source/correction mutations. Hash anchors provide integrity, not an external signature, and are not protection against concurrent malicious filesystem changes.

## Public sources

- [Analytic Number Theory, OWR 51/2025, printed p.2756](https://ems.press/content/serial-article-files/52435?nt=1): original normalization and the separately announced squarefree Atkin-Lehner-eigenfunction result.
- [Assing--Li--Wang--Xia, arXiv:2503.05685v1, Section 3](https://arxiv.org/pdf/2503.05685v1): normalized Petersson norm and raw coefficients, equation (3.2), and the general exponent-2 Theorem 3.5. Multiplication by the level index yields the conventions here.
- [Stein, Modular Forms of Level 1](https://wstein.org/books/modform/modform/level_one.html): classical Hecke identities used in the partial theorem.

The immutable audit records primary-source inspection and the publicly displayed manuscript status at that time. No comprehensive latest-literature or first-resolution claim is made. This package contains authored mathematics, audits, code and public verification metadata only; no source PDFs, extracts, dataset contents or private coordination files are included.
