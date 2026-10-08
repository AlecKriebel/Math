# Credited prior result: planar convex integer IKEA

Target: 1900002 / AMR-018-0002, rank 1016. Disposition: `already_solved`, **0/5 proof turns, for planar convex lattice polygons only**.

**The original 2017 question does not explicitly require convexity. This packet accepts only the planar convex interpretation; it does not resolve an unrestricted nonconvex reading.**

Credit: James Dolan and Oleg Karpenkov, *Lattice angles of lattice polygons*, JTNB 37(3) (2025), 873–896, [Theorem 3.3 and §5.1](https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.1345/). The result is an existential integer-witness classification. No novelty, nonconvex or higher-dimensional classification, adjacent cosine-rule solution, or total decision algorithm from bounded curvature search is claimed.

The mathematical review and acceptance are in `accepted/public/`. The audit supplies a zero-aware crossing argument and a rational-to-integer convex construction while explicitly importing credited sail lemmas. This is an AI-assisted authored audit, not formal verification or conventional human peer review. Finite arithmetic controls do not prove the universal classification.

## Preserved evidence

All 35 accepted public files are copied byte-for-byte from the reviewed allowlist. `accepted/PUBLIC_AUDIT.zip` is the original sealed 32-member archive. Its manifest contains 31 payload files; the final archive receipt and delivery pins are separately bound. Original v1 and the literal private correction patches are intentionally absent because they contain copied source text. No private source bytes, dataset contents, or private coordination files are published.

The inspected 2023-preprint correction file identified three supporting notation/terminology slips, with no change to the main criterion. Some journal supporting notation also needs the clarification documented in the audit. The source assessment is qualified and dated; it is not a guarantee that no further correction exists. Saved full-input receipts describe historical checks, not fresh source retrieval during this publication replay.

## Reproduce from a trusted Python

First check `BOOTSTRAP.py` against the SHA-256 delivered independently in the PR description. A hash stored only in the same untrusted folder is not an independent trust anchor. The bootstrap pins the verifier and manifest before running package code. Then, from this directory:

```sh
python -I -S -B BOOTSTRAP.py
python -I -S -B -O BOOTSTRAP.py
python -I -S -B -OO BOOTSTRAP.py
python -I -S -B TEST_MUTATIONS.py
```

Run as a non-root user. Full replay uses fresh authenticated copies, freezes them to 0444/0555, and actually attempts append/create operations on every file/directory. It checks unchanged bytes and modes. This is permission-enforced read-only testing, not an immutable mount. The verifier runs the corrected producer controls, independent arithmetic controls, and the accepted relocated read-only replay. The publication tests additionally reject per-file mutations, missing members, unsafe object types, malformed/duplicate/nonfinite JSON, exact-type mistakes, forged claims, and hostile code/import attempts. Schema tests exercise semantic validators directly as well as the external hash boundary.

Optional current local private-input checks:

```sh
python -I -S -B BOOTSTRAP.py --problems /local/problems.json --reports /local/research_results.json --sources /local/source-pdfs
```

Both corpora must be supplied together. Inputs are checked against accepted identities before replay. No network is used. If absent, current source/corpus/record checks explicitly report `NOT_RUN`; historical receipts do not turn them into passes. Fresh retrieval and fresh source inspection always report `NOT_RUN`. GitHub CI is reported separately from these local checks.

`--integrity-only` checks the exact tree, nested manifests, archive membership, byte identities, and scope without running arithmetic controls. It cannot be combined with private-input options.
