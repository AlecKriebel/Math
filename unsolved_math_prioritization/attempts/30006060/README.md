# Positive three-braid concordance: audited partial results

**Problem 30006060 / OWR-14298592-014, rank 804: unsolved, 5/5 approaches.** This package makes no full-solution, novelty, or priority claim. The general smooth-concordance question remains open in this investigation.

For the closures of sigma1^3 sigma2^3 sigma1^6 sigma2^6 and sigma1^3 sigma2^5 sigma1^3 sigma2^7, the independent agent audit accepts these scoped results:

- The same Alexander polynomial, determinant 243, and genus eight.
- Equality of the entire Levine–Tristram signature and nullity functions on S1 minus {1}, including singular parameters. The proof uses tree-gauge equivalence and exact equality of adjacency characteristic polynomials, not sampled signatures. The value at one is only a convention for the chosen matrices.
- Different double-branched-cover homology groups, Z/9 + Z/27 and Z/3 + Z/81, proving non-isotopy only. The difference linking form has an explicit 243-element metabolizer equal to its orthogonal complement.
- Equal tau=8, Rasmussen s=16, and Upsilon(1)=-7. Full Upsilon functions and full knot Floer complexes are not established.
- An embedded connected oriented six-saddle genus-three cobordism. Baker's theorem excludes ribbonness of the difference knot and homotopy-ribbon concordance in either direction, but does not imply smooth nonsliceness.

See [the current verdict](VERDICT.json), [authored proof](author/PROOF.md), [complete independent audit](audit/AUDIT.md), and [source and identity review](audit/SOURCE_REVIEW.md). Neither smooth concordance nor non-concordance is established; no topological locally flat or algebraic concordance verdict is asserted. Bounded source/duplicate searches do not establish historical openness or originality.

## Required verifier correction

The operative author checker is the top-level [verify.py](verify.py), byte-identical to [audit/corrections/verify.py](audit/corrections/verify.py). The only correction is [the exact explicit-exception patch](audit/VERIFY_HARDENING.patch). The immutable original [author/verify.py](author/verify.py) is preserved for provenance and is not the operative checker: Python -O removes its assert statement. The audit controls retain the exact false-determinant demonstration, including the original optimized false positive, and prove the hardened derivative rejects it in both modes. This is a verifier-integrity fix, not a mathematical v2.

## Replay

Python 3.10 or later and the standard library suffice. From this directory run:

    python3 verify_package.py
    python3 -O verify_package.py
    python3 run_package_controls.py

The package runner works from any current directory. It checks the exact file inventory, lengths and hashes, both ZIPs and every archive member, both frozen manifests, the exact hardening relationship, the original clean replay, the operative hardened replay in both modes, the independent verifier in both modes, and all 20 independent subprocess controls. The independent verifier has 163 explicit checks; the hardened author checker reports 432 checks. Package controls add relocated normal/optimized runs and deliberate inventory/hash/archive/manifest corruption rejection.

## Preserved history and publication scope

The author and audit directories and both ZIP archives are unchanged. Historical “audit pending” or “publication not performed” statements describe their respective freezes; the later audit and this publication wrapper supply the current assessment. The package manifest excludes itself and is bound externally by the Git commit and publication receipt. Do not regenerate it after unreviewed edits and treat that alone as verification.

Only the target queue row's Status and Turns become unsolved and 5/5. Every other queue byte, including its preexisting stale header, is preserved. The package does not synchronize or regenerate other queue state, rankings, or history. This checkpoint adds no proof-search attempt.

Included material is authored mathematical prose, code, audits, computed results, public verification metadata, and the two unchanged safe ZIPs. Copied source documents, extracts, raw datasets, private sources and private coordination are excluded. This is an independent agent audit, not human peer review. Draft PR only; no merge, release, DOI, or external outreach.
