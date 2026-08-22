# Final adversarial audit of the K2P article and reader supplement

Date: 22 August 2026

Verdict: **mathematical and reproducibility pass; human metadata and immutable
release decisions remain**

## Executive result

No counterexample, theorem-level failure, finite-census discrepancy, unsafe
graph quotient, direction reversal, or replay/mutation failure was found. The
principal result remains unconditional `K2P-SAME` on the positive Fourier
domain, with the strict continuous-time transfer and the full-dimensional
`4n-3` weak-class sharpness family. `PC-PARTIAL` remains the correct stopping
point for proof compression: the exact restoration and probe ledgers remain
load-bearing.

The fresh review's mathematical and expository requests were checked rather
than applied mechanically. Each was valid in its narrow form and is now
closed:

- Huber, Englander, and the present directed-ported refinement are attributed
  at their correct graph-theoretic layers.
- The ordinary-triangle proof uses the analytic submersion theorem on the
  displayed rank-nine maps; the contextual step invokes the constant-rank
  theorem and composes explicit local sections.
- The exact symmetric and anisotropic Jacobian blocks are printed.
- The paired K2P marginal descriptor records the two switching signatures,
  serial products, invisible classes, identities, and only certified parent
  flips.
- The completion formula is explicitly identified as counting repair-tagged
  directed descriptors, including deterministic dummy roles on empty required
  segments.
- The 23 quadratic bodies, five high-degree bases, licensed transports,
  coordinate dictionaries, and three worked certificate paths are printed and
  independently replayed.
- The weak-sharpness edge-class and Jacobian-column orders are named and
  independently reconstructed from the primitive graphs.
- The generic complex/physical rank comparison and semialgebraic-dimension
  step are stated explicitly.
- The four directed theta placements and every minimum-repair family now have
  a self-contained exhaustive case analysis.
- The finite-topology premise now follows from the explicit tree-child bound
  (r\leq |\mathcal X|-1) and the resulting vertex bound
  (|V|\leq4|\mathcal X|-3).
- The compact compression table is an unconditional source dependency; a
  clean build with that file removed fails closed.
- The reconstruction procedure retains all locally unexcluded supports and
  selects the unique global triangle class by exact semialgebraic feasibility,
  rather than misusing rank certificates as pointwise tests.

## Exact validation

The frozen theorem authority is
`work/final_theorem_release/RELEASE_LOCK.json`, file SHA-256
`58e32bd29f7a039e3da4e47398e32ee8277ad46cf62271a7ed80bf41688b18fb`
and payload SHA-256
`3b7de4c60315a5820a2623de860f493d6b76a645b5c674ffda89f12fc31a5c90`.
It is promotion-ready with no blockers. Its transitive referee ledger contains
374 files and 434,698,345 bytes with content root
`7004e3e26bf359d0a11c07fd51cb1636859b30b07a97ca6c9cfd0dcd082dfc92`.

A detached clean checkout at commit `1e9ff6c6` passed the complete full replay:

| check | result |
|---|---|
| full theorem layers | 35/35 PASS |
| blockers | 0 |
| wall time | 5,172.89 s |
| verifier internal time | 5,172.248447 s |
| maximum resident set size | 1,960,001,536 bytes |
| peak memory footprint | 491,504,408 bytes |
| replay report SHA-256 | `7939b389880de80b7d8abd69022e0b69d2dc4188815854b294d3384fa24c9e18` |
| telemetry SHA-256 | `8779854633d9a52ba3d7bc9278ccbcc3918e51987bb4c30204c0adcd9771ce16` |

The seven-command old/new equivalence suite, all 11 compression mutations, all
18 printed-appendix mutations, and all 15 named-column mutations pass. The
probe-word replay covers 176 anchors, 29,964 one-port rows, 544,571 two-port
rows, and 67,741 exact transports. The restoration replay covers 997 parents,
2,540 physical roots, and 36,824 forest edges with no missing, duplicate,
cyclic, or unresolved records.

## Source and PDF freeze

| artifact | SHA-256 |
|---|---|
| article source | `480581cec37b9a90e5e96eb1528e6fca6a4bbfafaefd43d9d41357f8e67ac999` |
| bibliography | `14dbb4901d924b068c8cc2d050e73bae3cf996a72863a22ade90d6f8e6b4057c` |
| supplement source | `1989d763d51004f351e42279ccf82374d3c0afa2b4ea96bcfa3026075e6b3ce8` |
| certificate appendix source | `ef878c24ff3f6b28d70b6c3dbf90c6d1e7d3c85a2bece621c96f47c409ca0ffa` |
| article PDF | `204537cef40f155d1fd418c4b17cd7b8cd5e432773b0de037a829690f8ba77e1` |
| supplement PDF | `19865ffb832abf5757d5fb5d534e1888d22f3b11ea7ea035e451203359ca275a` |

The article and supplement are 26 and 24 pages, respectively. All 50 pages were rendered and
visually inspected. There are no clipped elements, overfull boxes, undefined
references or citations, fatal errors, or hyperref PDF-string warnings; all
fonts are embedded. The fail-closed missing-table build test also passes.

## Remaining hold

The only open items require the human author: corresponding email,
author-contribution approval, funding and competing-interests declarations,
paper/code/data licenses, immutable submission tag, and the decision whether
and when to create a GitHub/Zenodo DOI release. They are deliberately not
inferred. The mutable repository URL is already printed.

The deterministic referee archive is sealed by a machine manifest. Its archive
SHA-256 is recorded in a separate sidecar after construction, avoiding the
self-reference that would arise from embedding an archive's hash inside the
archive itself.

## Recommendation

Retain the main theorem, continuous-time corollary, reconstruction theorem,
and sharpness theorem unchanged. Do not reopen proof compression or the atlas.
After the human metadata and release choices are supplied, the package is
ready for preprint and journal circulation.
