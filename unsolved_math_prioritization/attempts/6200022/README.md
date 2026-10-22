# Delzant diagonal convex cores: credited prior negative resolution

**6200022 / AMR-061-0022, rank 809: already_solved, 1/5 substantive routes.** The independent AI mathematical audit accepts the frozen disposition and both scoped geometric arguments without correction. No novelty, conventional human peer review, or formal proof certification is claimed.

## Attribution and precise scope

The universal existence assertion in Thomas Delzant's Problem 22 in [Kapovich's survey](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf), printed page 7, is false. **Credit the published prior resolution to Subhadip Dey and Beibei Liu**, [Rigidity of convex co-compact diagonal actions](https://ems.press/journals/ggd/articles/14298926), Groups, Geometry, and Dynamics, online July 4, 2025, [DOI 10.4171/GGD/908](https://doi.org/10.4171/GGD/908). The author and auditor inspected the [public version-1 preprint](https://arxiv.org/abs/2408.03462v1), including Question 1.1, Theorem 1.2 and Corollary 1.5. The publisher record was checked; the subscription journal PDF was not inspected. The general rigidity theorem is credited, not independently certified in full here.

The illustrative weighted F(a,b) tree construction is also credited to **Guilbault and Mooney**, [Cell-Like Equivalences and Boundaries of CAT(0) Groups](https://arxiv.org/abs/1011.1298v1), Examples 2.2 and 2.4. The authored elementary midpoint proof excludes **every nonempty invariant convex subset with compact quotient**, including candidates unrelated to the chosen orbit's convex hull. No presentation-priority claim is made.

A separate conditional proposition assumes proper CAT(0) geometric factor actions and a nonempty, closed, invariant, cocompact convex subset C of their product. The restricted projections induce equivariant **homeomorphisms** of visual boundaries. The argument uses their affine-geodesic property and uniformly positive projected ray speeds; it does not assume arbitrary CAT(0) quasi-isometries extend to boundaries. Neighboring Problem 21, concerning broader cell-like boundary equivalence without a convex core, is not settled.

Read [the authored proof](author/RESULT.md), [the complete independent audit](audit/AUDIT.md), and [the governing current verdict](VERDICT.json). The one-route early stop records discovery of a verified prior resolution. The remaining four routes are unspent.

## Reproduce and authenticate

Requires Python 3.10+ standard library. Run from any working directory:

    python3 /path/to/6200022/verify_package.py
    python3 -O /path/to/6200022/verify_package.py
    python3 /path/to/6200022/run_package_controls.py

For an external publication-manifest pin and the exact queue delta:

    python3 verify_package.py --expected-manifest SHA256 --queue-base /path/to/base-QUEUE.md --queue-updated /path/to/branch-QUEUE.md

The wrapper checks the exact recursive file and directory inventory, duplicate JSON keys, regular-file and symlink/ancestor-link safety, immutable archive and inner manifest pins, every ZIP member byte, current disposition, and both arithmetic replays. The controls repeat normal/optimized and relocated runs, the audit's complete mutation suite for both frozen packages, and hostile publication mutations. The 77,142 author and 27,534 independent finite exact checks supplement the written infinite geometric arguments; they are not formal verification of them.

The unchanged author ZIP is 16,021 bytes, SHA-256 2ed1cf89f1d8e3ea19184fa5bd14b840a2e12183b0ab4c1f0b690c9eea4f1e62. The unchanged audit ZIP is 16,755 bytes, SHA-256 8921a5898f44d36b27fee9fff5d11df195da4ebd11be86d50b5778fbab367c5a. Every extracted file matches its ZIP. Authenticate the publication manifest with the retained receipt or remote Git commit. Unsigned hashes cannot prevent replacement of every trusted binding and verifier.

Historical author statements that audit was pending and audit statements that publication had not occurred remain intact. The separate accepted audit and this wrapper record the later disposition. Only this target queue row's Status, Turns and qualified Findings change. Every other queue byte, including its preexisting header, is preserved. No global queue regeneration is included.

Only authored mathematical analysis, code/results, public verification metadata and the two safe ZIPs are distributed. Third-party PDFs, copied text/images, corpora, private sources, personal data and coordination are excluded. This is a draft review package; no merge, release, new DOI or outreach is part of it.
