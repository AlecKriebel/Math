# Coxeter boundaries of rational dimension one: audited partial results

**Problem 6200010 / AMR-061-0010, rank 807: unsolved, 5/5 approaches.** Independent audit: **PASS_SCOPED_PARTIALS_ORIGINAL_UNRESOLVED**. There is no accepted general construction, nonexistence theorem, novelty claim, human peer review or formal proof-assistant certification.

The exact target is a finitely generated Coxeter group whose CAT(0) Davis visual boundary has covering dimension n >= 3 and rational cohomological dimension one, ultimately for arbitrary/unbounded n. Hyperbolicity is not required. Known dimension-two examples do not settle this target. The current live catalogue page was inaccessible; source and corpus identity are documented rather than claiming its current rendered status was verified.

## Accepted scope

- For a finite Coxeter nerve, the maximum reduced cohomology degree over all induced subcomplexes equals the maximum over full complements of simplices. This gives the coefficient-specific regularity reformulation.
- For a three-dimensional nerve with every vertex link a closed connected triangulated surface, rational boundary dimension is at least two. In the all-RP2-link case, b2 = V/2 - 1 + b1 > 0.
- In higher dimensions, compatible PL manifold vertex-link triangulations force the stated link-sphere obstruction. Merely topological manifold links are not substituted for the compatible PL hypothesis.
- Ordinary barycentric flagification of dimension >= 3 introduces an induced rational sphere obstruction. This excludes that method and its iterations, not all flag triangulations of a space.
- New-vertex cone attachments cannot eliminate an obstruction while the old nerve remains induced. Modifying old-only simplices falls outside the theorem.
- The cited CKV quotient/thickening iteration increases rational virtual dimension, so each positive iteration from the indicated seed leaves rational boundary dimension one.

Read [the proofs and five approach outcomes](author/RESULT.md), [the complete independent audit](audit/AUDIT.md), and [the current scoped verdict](VERDICT.json). The exact finite model has 64 vertices, cubical cells (64,192,240,80), triangulated f-vector (64,512,960,480), rational Betti vector (1,0,31,0), and mod-two vector (1,0,32,1). It is a topological control, not a claimed solution or claimed flag nerve. The 32,400 author and 5,055 independent checks supplement the general mathematical arguments and imported theorems; their counts are not coverage of infinite families.

## Correction to related work

The related [PR390](https://github.com/AlecKriebel/Math/pull/390) for problem 6200004 warned too broadly that arbitrary vertex deletion changes the invariant. Individual puncture profiles change, but their maximum nonvanishing cohomology degree agrees with the simplex-deletion maximum. Proposition 1 and the audit give the proof; the independent four-cycle control distinguishes the profiles while preserving their common maximum. The older packet and PR are not edited. Its concrete simplex-deletion calculations and closed-manifold exclusions are unaffected. Hyperbolicity-specific restrictions from that earlier question are not imposed here.

## Operative integrity correction and reproduction

The immutable original author verifier ignores unexpected nested files named MANIFEST.json. No such unexpected file is in its reviewed freeze. The audit closes that omission with exact relative paths, and the publication wrapper checks the complete file and directory inventory, symlinks including ancestor components, both archive/manifest pins, ZIP member bytes, unchanged duplicate author bindings and the scoped disposition.

Use the strict wrapper as the publication entry point, from any working directory:

    python3 /path/to/6200010/verify_package.py
    python3 -O /path/to/6200010/verify_package.py
    python3 /path/to/6200010/run_package_controls.py

Each wrapper execution invokes audit/verify_audit.py, which strictly checks the audit payload and replays both the author and independent calculations. The controls exercise normal/optimized and relocated clean runs, the original audit's 30 hostile mutations, additional publication mutations, and a reproducible demonstration of the historical author-only omission. Rejection checks remain effective under Python -O.

For external manifest trust and exact queue verification:

    python3 verify_package.py --expected-manifest SHA256 --queue-base /path/to/base-QUEUE.md --queue-updated /path/to/branch-QUEUE.md

The publication manifest excludes only itself; authenticate it with the remote Git commit or retained receipt. Hash checks are not signatures or protection against replacing every trusted binding and verifier.

Both author/audit directories and both ZIPs are unchanged. Historical pending-review and no-publication wording is retained as history; this wrapper and the independent scoped verdict supply the current disposition. The author ZIP SHA-256 is a2fc0e27b9bd81dca28450f20cdbbda139b2e50933126bd6b9db577662cc0dcf. The audit ZIP SHA-256 is d1f99fa9ec76e240ecb80f365c9f98a820402e5345723e34842c6a4285d6b491. The respective manifest hashes are b8f24c4403ad0c93be653da10572689ecb683741e4e387b97996ebb05a717609 and c6015afbde76381d7f7eb2d27f00bf6a0afff22d4d163aa3d2be9c5810e312ec.

Only this target queue row's Status and Turns change to unsolved and 5/5. Every other queue byte, including the preexisting header, is preserved. No global state/history/ranking regeneration or new proof-search turn is included. Source PDFs, copied extracts, raw corpora, private sources and coordination are excluded. Draft review only; no merge, release, DOI or outreach.
