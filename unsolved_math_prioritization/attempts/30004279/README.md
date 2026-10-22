# Audited partial results: bicommutant categories of conformal nets

Problem 30004279 / OWR-17292-002, queue rank 719. Current disposition: **unsolved, 5/5 substantive approaches**. No pair of nonisomorphic nets with a proven equivalence of their full soliton tensor categories is constructed. No novelty, prior resolution, exhaustive literature coverage, or global openness is certified.

## Retained mathematical results

- Tensor equivalence of full soliton categories forces braided equivalence of their centers, hence of the representation categories in the stated finite-index setting. The converse is unavailable.
- For a nontrivial holomorphic net H, T(H) and Hilb have equivalent centers but are not equivalent as complex-linear *-categories: the absorbing soliton has a type III endomorphism algebra, while every nonzero Hilbert space has a minimal endomorphism projection.
- Holomorphic central-charge-8 tensor powers supply pairwise nonisomorphic covariant nets with equal representation categories and centers. Equivalence of their full soliton categories remains unproved.
- The fusion-category Morita theorem applies only after the missing full-soliton-to-fusion-commutant identifications have been established. It cannot be applied to T(A) as a finite fusion category.
- A normal factor isomorphism yields a sufficient spatial strategy only if transport of both bimodule actions preserves the four-interval normal-extension predicate for every separable bimodule, in both directions. The audit expands the Connes-fusion comparison, naturality, and coherence. No such map for a candidate pair is constructed.
- Proper solitons give uncountably many simple classes in the nontrivial diffeomorphism-covariant setting. Finite DHR data and matching geometric labels or fusion rules do not determine the full category or its coherent tensor structure.

The scope is nontrivial, irreducible, diffeomorphism-covariant, finite-index nets in the strong-additive split setting, with separable Hilbert spaces and complex-linear *-equivalences with unitary tensor constraints. The audit explains why full *-equivalences between the relevant W*-categories are normal using endomorphism order isomorphisms and linking corners; it does not assert normality of arbitrary functors.

## Proof, audit, and historical snapshots

1. [Author proof](safe_packet_v1/PROOFS.md): five routes, retained deductions, external inputs, and residual gaps.
2. [Independent audit](independent_audit_v1/AUDIT.md): accepted bounded unsuccessful research, including expanded operator actions and Connes-fusion coherence.
3. [Audit binding](independent_audit_v1/BINDING.json): exact reviewed inputs and public source-verification metadata.
4. [Current status](PUBLICATION_STATUS.json): disposition and limits.

All 16 original author/audit files are preserved byte-for-byte. Pending-review or no-publication fields in the frozen author packet describe its historical creation state. The later completed audit and current status supersede those fields without rewriting history. The audit's refusal to certify scholarly publication readiness remains in force; this is a draft research record, not a reviewed solution or preprint release.

## Portable offline verification

Python 3.8 or newer, standard library only. From this directory:

    python3 -B verify_publication.py
    python3 -O -B verify_publication.py
    PYTHONOPTIMIZE=2 python3 -B verify_publication.py

The wrapper checks exact inventories, file sizes, SHA-256 digests, hard-pinned original manifests and audit, and the audit's input binding. Both frozen outputs must replay byte-for-byte: 47 author assertions and 113 independent controls, including three actual mathematical mutations. These finite checks supplement the written operator-algebra arguments; they cannot prove source theorems, normal extension, or an equivalence of soliton categories.

Every child process runs with optimization explicitly set to zero and without forwarded -O flags. A real assert-false subprocess must fail with the expected AssertionError. The wrapper's own checks use explicit exceptions and stay active under optimization. Paths are relative to the script and no source download or network access is required. The outer manifest excludes itself; authenticate its SHA-256 against the PR or an independently trusted receipt.

## Source limits and repository scope

Eight primary-source PDFs were privately retrieved and inspected at specified sections, then independently hashed and re-extracted. The exact target site was inaccessible and uninspected; raw imported statements and AI reports were unavailable and uninspected. The Oxford 2026 thesis PDF remains uninspected, and its abstract does not settle the target. The HPT journal DOI refresh failed in the independent audit; the theorem-scope conclusion relies on the inspected preprint. Public titles, URLs, source hashes, byte counts, and inspection history are retained with these limits.

Only authored proof/audit/code and public verification metadata are included. Source PDFs, extracts, images, raw records, raw connector responses, and private coordination are excluded. The queue edit changes only this problem's Status and Turns. Its Findings, Chat, and DOI cells, every other row, and the pre-existing embedded header are preserved. No queue regeneration, merge, release, DOI creation, or outreach is part of this draft.
