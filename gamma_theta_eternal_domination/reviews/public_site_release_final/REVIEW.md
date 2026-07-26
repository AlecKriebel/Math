# Final public-site release audit

## Verdict

**`ACCEPT_SITE_BYTES_CONDITIONAL_ONLY_ON_ATOMIC_TAG_PUSH`**

The accepted site bytes have no blocking structural, attribution, notation,
link, asset, or mathematical-scope defect. The sole publication condition is
atomic creation and push of
`gamma-theta-order12-frontier-v1.0.0` for these exact bytes.

This package was produced by the campaign's independent final-release
auditor. Before publication, `audit.py` emits the conditional verdict above.
After publication, it verifies every accepted site artifact directly from
the annotated tag and emits `ACCEPT_SITE_BYTES_TAG_BOUND`.

## Exact bindings

| Artifact | SHA-256 |
|---|---|
| `README.md` | `1a66969b4734dd2eaacfba02e5373f08282fc6d6b27bea52103382d43b1835e8` |
| `docs/index.html` | `6772d7de5014e91437111cfe40897413b8aa8874745093b28ba025c55bfa505b` |
| `docs/sitemap.xml` | `5bc452cf14985d31d1fbcc50ac71267d29091074420209678651b309eedd9158` |
| research page | `3f2e951e5d7ee69984fb27f2387bf64ecabdb3da2bf405f0d894706b6ff21459` |
| paper page | `a5d54c1f8bc997b81740c1bddb99a46468b2ccd4c696d31aae82a96e2d3a9a09` |
| public PDF | `b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2` |
| `paper.sha256` | `184df74e9e4d5dc3165ef807fde9f1fa35831b2c0aad325397fea1d40c74faeb` |
| cyclic-Bell paper page | `d870c1368678902cb1bdc19e4e6a89456cee4882fe6aafc1f425ab2ed18b6e36` |
| cyclic-Bell public PDF | `947b601903de18ea6ffbd8e49ba2bfe261c32342c4d1a71dd96ed9f283ec6c94` |
| campaign README | `5bb3053bc03b1d0abec557c15856ece982c9b526bfd70a41b59eca881d4501c2` |
| release notes | `fdb7043d86482aaf5cd05c495c7889b16e04621a9d9a892df3b7f1ec15a77779` |

All three paper/research JSON-LD documents and the XML sitemap parse
strictly. The integrated homepage reports eight current papers and contains
both the cyclic-Bell and gamma-theta cards. The 19-location sitemap contains
both publication URLs, and no merge-conflict marker remains. IDs are unique,
all local links, fragments, PDFs, and style assets resolve, and the decisive
page directories contain no symlink or unexpected file. Omitting
`og:image` is accepted and intentional because no generated social card
passed exact-text QA.

The pages consistently use the standard one-guard model: attacks are only at
unoccupied vertices and exactly one adjacent guard traverses one edge.
They define \(\theta\) as clique-cover number and distinguish it from Lovász
\(\vartheta\). Alec Kriebel attribution agrees across visible bylines,
metadata, JSON-LD, and citation text.

The scope matches the accepted ledger:

- C-050 is conditional on the published through-order-11 computation.
- C-053 excludes only the complement-\(C_{11}\) branch.
- C-054 supplies near-miss families, not counterexamples or a priority claim.
- C-056 is a bounded parameter-five reduction, not a slice exclusion.
- C-057 excludes only the complement-\(C_9\) template; \(C_5,C_7\) and the
  parameter-four and parameter-five slices remain live.

No page claims an unconditional through-order-12 theorem, a complete
order-13 exclusion, a lower bound of 14, or a universal resolution.
`order12_frontier` is the sole current campaign paper, while
`c035_order12_k3` is explicitly archival and superseded.

The deterministic checker passes before tag creation. If the tag is present
locally afterward, it additionally requires every bound integrated,
gamma-theta, and cyclic-Bell artifact to match its tagged bytes.
