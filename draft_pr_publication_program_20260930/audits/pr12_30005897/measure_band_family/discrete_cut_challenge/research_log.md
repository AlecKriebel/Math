# Independent discrete-cut challenge

## Scope

Independently test the stated band-splitting claim for positive bi-infinite scalar weights. This audit does not consult the PR12 proof, earlier reviews, or parent notes. No external outreach or Git operations are authorized for this subtask.

## 2026-10-01 05:35:37 UTC — Initial checkpoint

**Completion estimate: 15%.** Converted the claimed operator decay into a scalar requirement: a fiber cut must make `rho[j-k]/rho[j]` decay on the lower band and `rho[j+k]/rho[j]` decay on the upper band. Forward invariance for the backward shift requires lower, rather than upper, fiber support. The `d=1` condition propagates a rightward drop indefinitely once it begins. The central adversarial issue for `d>1` is whether residue cuts can disagree by an unbounded distance despite uniformly bounded neighboring ratios.

An attempted independent counterexample-search delegation was unavailable because the team already uses every agent slot. This audit continues independently.

## 2026-10-01 05:38:20 UTC — Residue-cut mechanism established

**Completion estimate: 75%.** In logarithmic weights, each residue increment sequence has an initial growth region, at most one intermediate edge, and a final decay region. Comparing residues at the actual coordinate positions `r+dk` and `s+dk` gives `|v_r(k)-v_s(k)| <= |r-s| log Q`. Sustained opposite slopes force this difference to grow by at least `2(-log eta)` per edge, proving a uniform bound on finite cut disagreement and excluding incompatible infinite cuts. This mechanism answers the central attempted counterexample.

## 2026-10-01 05:41:56 UTC — Complete scalar proof and reproducible checks

**Completion estimate: 100% of the assigned scalar-proposition audit.** The independent derivation constructs `K(w)=d t_0(w)` with both infinite conventions and proves its measurability by countable nongrowth-edge events. Explicit uniform exponential constants are given. The scalar norm identity verifies both invariant support bands, including `p=1`. The exact-log validation script passed 481,475 scalar decay inequalities across 405 families, covering differing cuts, intermediate edges, large translations, `d=1,...,8`, and full/zero-band extremes.

No counterexample or mathematical gap was found under the exact stated assumptions. The hypotheses must include one neighbor-ratio bound uniform in both coordinate and fiber, and the conclusion must permit zero bands. A counterexample without that global bound is recorded. The audit does not validate the relation between these scalar assumptions and any wider measure-theoretic setup or source theorem.

The parent is independently checking a materially different finite-support-band route. This audit maintained source independence through completion. No Git operation or external communication occurred.
