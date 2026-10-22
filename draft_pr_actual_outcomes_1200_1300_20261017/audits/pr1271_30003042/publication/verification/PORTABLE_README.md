# Verification archive for the n=8 gamma-filtration counterexample

The manuscript gives the original-target negative conclusion as a credited consequence of published results. The main proof uses Karpenko's later analytic index bound and the pointwise transfer and filtration theorem in his original paper. The additional exact computations verify earlier published ingredients; no firstness, current-openness, new Spin-index theorem or new class-valuation theorem is claimed.

Use Python 3.9 or later and its standard library. Unpack the archive into a new directory. Run `python3 verify.py` with all three required options: `--expected-manifest-sha256`, `--expected-context-sha256` and `--expected-snapshot-sha256`. Obtain their values from the outside build/review receipt in the repository, identified by the published artifact hash. Merely copying those values from the same untrusted archive does not supply an independent trust anchor. The checker has no network dependency and works on temporary copies of executable diagnostics.

The four automatically replayed programs are:

- `reviews/source_only_math/CHECK_MOD2.py`: the finite polynomial step in the later analytic proof. It writes its output only in the checker's temporary directory.
- `reviews/candidate_adversary/COMPUTATION.py`: independently constructed exact localization and integer Pieri witnesses for the sufficient index bound.
- `reviews/chow_computation/check_chow.py`: integral lower-divisibility identities and a complementary intersection pairing, proving the known class valuation 22.
- `reviews/finite_computation_adversary/check_independent.py`: a subsequent independent root-monomial/Vandermonde extraction and root-system localization challenge.

Each runs in normal, `-O` and `-OO` modes and must agree with its explicitly retained result. They do not run the original source-author Maple program. Finite computations do not replace the written proof or reprove its standard Clifford, Chow, filtration, transfer, and Gysin/localization dependencies. Exact generic index 8 is a cited result; the package's rational-cycle witness alone supplies an upper bound dividing 8. A zero-cycle degree is not a closed-point or field-extension degree.

`original_submitted/` and `current_edition/` preserve the same original eight files. Their October 11 statements about access and computations remain historical. The current manuscript and current mathematical/priority adjudications describe the later audit and computations. Missing older editorial input bodies and omitted historical execution bodies are not replay-certified. The Appendix A prose discrepancy is explicitly recorded: eight doubled factors give the correct normalization 2^8, rather than the printed prose's 2^3.

Nested authored manifests are selected by the current context's explicit relative schemas. Other paths inside source or input receipts are locators, not archive membership. Raw third-party PDFs, extracted text, search-provider output, images, caches and scratch are omitted. Hashing a source identifies bytes; it does not broaden the recorded reading scope. Initial families were sealed before the disclosed reverse cross-reviews; later exposure and tooling-only feedback are documented.

The archive includes the manuscript source, actual compile and all-page layout receipts, source-reading receipts, mathematical and priority evidence, scoped checker results, and sealed workflow source copies. Fresh complete-package reviews and eventual publication/integration receipts are retained separately in the repository to avoid self-referential archive hashes. The manuscript's outside PDF hash is bound in the current context; the PDF is the other deposited file.

AI tools were used extensively in solving, verification, literature review, drafting and internal adversarial review. This is an unrefereed preprint with no external human peer review, journal acceptance or formal proof-assistant certification claimed.
