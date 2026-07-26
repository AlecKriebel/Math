# Public release: certified order-12 frontier

The current campaign paper is publicly released:

> Alec Kriebel, *A Certified Order-Twelve Extension of the
> gamma--theta Frontier in One-Guard Eternal Domination*, 17 pages,
> 26 July 2026.

- Active workstream:
  <https://aleckriebel.github.io/Math/research/gamma-theta-conjecture/>
- Paper page:
  <https://aleckriebel.github.io/Math/papers/gamma-theta-order-12-frontier/>
- PDF:
  <https://aleckriebel.github.io/Math/papers/gamma-theta-order-12-frontier/paper.pdf>
- Tagged reproducibility release:
  <https://github.com/AlecKriebel/Math/releases/tag/gamma-theta-order12-frontier-v1.0.0>

## Exact result boundary

Assume MacGillivray, Mynhardt, and Virgile's published exhaustive result that
there is no counterexample through order 11. Then every counterexample to the
standard one-guard-moves gamma--theta conjecture has at least 13 vertices.

This is a certificate-backed finite frontier, not a universal proof, a
counterexample, a lower bound of 14, or a campaign-only re-enumeration through
order 11. The universal conjecture remains open.

## Release binding

- release commit:
  `16dd2a7803d21fda02fa28e26561d652b7f3b595`
- annotated tag: `gamma-theta-order12-frontier-v1.0.0`
- PDF SHA-256:
  `b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2`
- GitHub Pages build: `1116371323`, status `built`, exact release commit
- public acceptance record:
  `results/order12_frontier_public_release_acceptance.json`

The homepage, workstream page, paper page, PDF, checksum sidecar, sitemap, and
release PDF were downloaded over HTTPS and compared byte-for-byte with the
accepted local artifacts. Both post-tag audit scripts verify the accepted
bytes directly from the annotated tag.

## Reproduction

From this campaign directory:

```text
python3 -I -B repro/c050/replay.py --full
```

Expected terminal verdict:

```text
VERIFIED_ORDER12_FRONTIER_BINDINGS_AND_EXACT_LRAT
```

The replay invokes no SAT solver. The earlier
`paper/c035_order12_k3/` draft is archival and superseded; it is not a second
current publication.
