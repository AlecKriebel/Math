# Order-13 parameter-three manuscript package

This directory contains the standalone manuscript proving the finite
statement

> No graph on 13 vertices satisfies
> `gamma(G) = gamma_infinity(G) = 3 < theta(G)`.

It does not exclude common parameters four or five at order 13 and does not
resolve the universal gamma--theta conjecture.

## Frozen artifact manifest

| Artifact | SHA-256 |
|---|---|
| `main.tex` | `56afff0796fb602589d38714793e42b6864a5454d71d8da51b559daa3daea8f2` |
| `main.pdf` | `6768cecf0d46672f7d56cbda2715b49ef18470e5d60b3c7912fc9999843ae5a4` |
| `references.bib` | `79600fcc86edce90e6cedf1eb1ee07ff3544ac7e0eb62bef4d9904fa59f0615b` |
| `main.bbl` | `e48bb8852ac967e5c698a59007f83e7225acabdbf10981a8bf1e0b713d9750a6` |
| `main.blg` | `36a26a35030c17e6a29ed5fa683a298f907726cf9a3af844f8f4d3b56dd6020e` |
| `main.log` | `3508e221fb28b95ea51ea641a700399b11ee6d4b7759cd8ba75e51994dac0bc8` |

The public copy at
`docs/papers/gamma-theta-order-13-k3/paper.pdf` is byte-identical to
`main.pdf`. The complete publication QA record is `qa.json`.

## Deterministic build

From this directory:

```text
SOURCE_DATE_EPOCH=1785231600 \
  tectonic --keep-logs --keep-intermediates main.tex
```

The public edition identifies Alec Kriebel as author and discloses heavy
assistance from ChatGPT 5.6 Sol. Two final builds were byte-identical, and
all ten rendered pages were inspected.

## Reproduction

From the campaign directory:

```text
python3 -I -B -W error repro/c097/replay.py
```

The wrapper reconstructs and replays the decisive no-full certificates. The
full-response certificate has its own independent checker:

```text
python3 -I -B -W error reviews/order13_full_target_hostile/checker.py
```

The exact manuscript, certificates, controls, theorem scope, attribution,
disclosure, and rendering were accepted by the independent hostile audit in
`reviews/order13_k3_release_audit_fast/`. The frozen public release is tagged
`gamma-theta-order13-k3-v1.0.0`.
