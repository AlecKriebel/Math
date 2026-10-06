# Symmetric lattice-polytope volume: audited partial results

Problem **30000638**, rank **814**, **OWR-1394-015**. Queue disposition: **unsolved, 5/5**. Independent gate: **ACCEPT_CORRECTED_PARTIAL**.

The general conjecture remains unresolved. For a full-dimensional origin-symmetric lattice n-polytope, with positive n, normalized volume V(P)=n! vol(P) and strictly interior lattice count I(P), the target is V(P) >= 2^(n-1)(I(P)+1).

## Accepted mathematics and exact limits

The [authored proof](corrected/PROOF.md) and [complete independent audit](audit/AUDIT_REPORT.md) establish these partial results without a novelty claim:

- Every 3D origin-symmetric lattice polytope with I<=5 satisfies the target. Hibi's inequalities apply because zero is interior; if the boundary count is six, the polytope is a crosspolytope; otherwise it is at least eight.
- A quotient-lattice proof certifies the known crosspolytope case, with at most two interior points per nonzero quotient coset and one in the zero coset. The result is credited to Bey–Henk–Wills.
- Cartesian products of certified factors satisfy the target strictly when both dimensions are positive.
- Free sums preserve satisfaction when one factor Q has exactly one interior lattice point. This does not require reflexivity. The dimensions are positive, and V(S)=V(P)V(Q), I(S)=I(P).

For precision, set Delta(P)=V(P)-2^(n-1)(I(P)+1), where P has dimension n and Q dimension m. The audit gives

    Delta(S)=V(Q)Delta(P)+2^(n-1)(I(P)+1)(V(Q)-2^m).

Thus the gap is exactly multiplied by V(Q) only when V(Q)=2^m. This qualification governs the informal gap-preservation sentence in the unchanged historical proof. No claim that every polytope has a suitable product/free-sum decomposition is made. The formal vector (1,11,11,7) is only an obstruction to the listed coefficient constraints, not a realizable-polytope counterexample. The asymptotic Henze bound does not give the exact conjectured constant.

## Operative correction and preserved history

Use **corrected/verify.py**. The original verifier's unqualified fail-closed claim is rejected: unmanifested bytecode can bypass recomputation, and rehashed source-status claims were not semantically guarded. The separate derivative rejects every extra entry including __pycache__, compiles and executes the exact verified source bytes rather than importing cached code, and requires exactly five source-claim keys with literal false values.

Only verify.py and its MANIFEST.json entry change. The [actual correction patch](audit/correction.patch) is applied to a fresh frozen author copy during the audit, then all resulting bytes are compared against the derivative and executed in normal and optimized Python. These were verification and metadata defects, not mathematical counterexamples.

The three ZIP archives and every extracted original/audit/corrected member retain their exact bytes. Historical false/pending audit and publication flags inside the author artifacts describe their preparation stage and are not rewritten. The corrected copy's unchanged README wording about importing the engine is historical; the operative verifier executes verified source bytes. The independent audit report supplies the later acceptance and corrections.

## Reproduce

Python 3.10+, the standard library, and the ordinary patch command are required. No network, datasets or source PDFs are needed.

    python verify_publication.py --replay
    python -O verify_publication.py --replay
    python test_publication_integrity.py

The publication verifier checks exact recursive file and directory inventories, hashes and byte counts, ZIP CRCs and members, extracted byte equality, all frozen manifests, and the two-file derivative scope before executing code. Replay runs the corrected verifier in normal and optimized modes and regenerates the independent audit results in an isolated relocated copy, comparing them to the frozen results. Each audit invocation covers 37 independent geometric checks, 72 original-regression checks and 52 extra adversarial probes; it applies and runs the actual patch in both modes. The intentional historical-cache demonstration executes only a harmless temporary marker in a disposable original fixture; no such cache is permitted in the operative derivative or publication inventory.

To check the narrow queue change with two locally supplied copies:

    python verify_publication.py --queue-base BASE_QUEUE.md --queue-updated BRANCH_QUEUE.md

Only this row's Status and Turns change; all other queue bytes, including Findings and the pre-existing header, are preserved.

## Source and publication scope

Public citations include [Bey–Henk–Wills](https://arxiv.org/abs/math/0606089), [Henk–Tagami](https://arxiv.org/abs/0710.2665), [Henze](https://arxiv.org/abs/1203.4075), and [OWR 56/2006, p.3386](https://doi.org/10.4171/owr/2006/56). The primary page was independently rendered from the hash-verified PDF; the web screenshot and problem-page access failures are disclosed in the audit. The bounded literature search found no authoritative complete resolution; that is not a proof of global absence.

This packet contains authored mathematics, code, audits, results, safe archives and public verification metadata. It excludes source PDFs, source text, page images and dataset contents. Finite checks support reproducibility; they are not exhaustive polytope enumeration or machine verification of the universal prose. Draft review only, with no novelty, peer-review or editorial-acceptance claim.
