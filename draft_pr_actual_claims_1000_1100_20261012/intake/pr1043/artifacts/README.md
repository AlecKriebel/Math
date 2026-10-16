# Continuous PL extension: accepted approach-1 partial results

**The original problem remains UNRESOLVED after approach 1 (1/5).** This proof-only edition preserves the full authored mathematical arguments and complete independent mathematical audit. It supplies neither a continuous extension selector for all boundary embeddings nor a counterexample to such a selector. It makes no novelty or comprehensive current-literature-status claim.

Problem 30004524 / OWR1703876-018 asks whether every injective finite piecewise-linear map of a fixed triangle boundary into the plane can be assigned an injective finite piecewise-linear extension to the whole triangle, continuously in the boundary map. The prescribed parameterization matters, and input and output subdivisions may vary without a complexity bound.

## Topology and exact gap

The report uses the **uniform topology**, equivalently compact-open topology on these compact source domains. This is an explicit interpretation: the short primary statements do not specify mapping-space topologies. A fixed triangulation, a bounded-complexity stratum or a direct-limit topology is not substituted.

The exact missing statement is a continuous PL-valued extension section on some **full uniform neighborhood** of the standard triangle boundary inclusion. Such a neighborhood must contain arbitrarily many boundary bends, steep small features and arbitrary finite subdivisions. The report proves that this local statement would imply a global selector, but does not prove or disprove the local statement.

## Reading order

- [APPROACH1.md](APPROACH1.md): the full mathematical report, with an edition notice and edited auxiliary inventory section.
- [AUDIT.md](AUDIT.md): the full mathematical audit and accepted stopping point, with omitted-evidence history clearly labeled.
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md): complete authored analysis of the five primary sources and the topological/PL distinctions.
- [ACCEPTANCE.json](ACCEPTANCE.json) and [STATUS.json](STATUS.json): accepted scope, unresolved gap and review limits.
- [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json): sanitized historical public-source metadata and PDF match records.
- [PROVENANCE.md](PROVENANCE.md): precise editorial and publication boundary.
- [MANIFEST.json](MANIFEST.json): exact membership and byte identities of this edition.

## Accepted mathematics

The preserved proofs establish:

1. Each extension fiber is a contractible group of finite PL disk homeomorphisms fixing the boundary, using explicit Alexander rescaling.
2. Fiberwise interpolation is jointly continuous even as the common image changes.
3. Locally defined sections globalize by a locally finite weighted construction that uses finitely many PL operations at each input. Zero weights and support boundaries are handled without assuming local compactness.
4. Global section existence is equivalent to section existence near the triangle inclusion, by fixed ambient PL Schoenflies transport and the preceding gluing.
5. The convex-image subspace has a 1-Lipschitz finite-PL extension selector.
6. Every continuous radial-cone apex rule fails on an appropriate shrinking hairpin family near the inclusion. This obstructs that construction class, not unrestricted PL extension selectors.
7. Any exact selector requires unbounded triangulation complexity on every full uniform neighborhood. This necessary complexity condition is compatible with uniform continuity and is not a nonexistence theorem.

The source audit additionally checks Yagasaki's genuinely PL-valued local extensions for maps into a fixed ambient boundary. That fixed-boundary result does not settle the freely moving plane-curve problem. The checked topological extension, homotopy-density, local-contractibility and conformal-parametrization results do not supply the missing exact-trace PL-valued operator as stated.

## Evidence and publication boundary

The explicit hairpin coordinates, determinant and collision proof were already written in the authored report and are retained unchanged. Historical supplementary checks remain labeled as such: four original fixture rows, 194 unshifted cases and 150 translated-apex cases were accepted by the original audit. Their programs, fixtures and standalone outputs are not included and were not rerun during packaging. The written analytical arguments, rather than finite samples, prove the universal partial conclusions. No excluded program or fixture has been transcribed into new prose, and this edition does not supply executable reproduction of the historical checks.

The report, audit and source-audit notices identify the inventory-only edits. They are not byte-for-byte reproductions of every original administrative or reproduction paragraph; all mathematical proofs, source reasoning and substantive limitations are preserved. Public raw-PDF hashes and sizes are retained without local paths. Copied source documents, extracted source text, datasets, private sources, private personal data and private coordination material are excluded.

The primary problem appears in [OWR 30/2020, Problem 14, printed p. 1523](https://ems.press/content/serial-article-files/46867) and [Rote's 2020 public problem list, p. 4](https://page.mi.fu-berlin.de/rote/Kram/Problems-Discrete-Geometry-2020.pdf). Source checks record the original inspection scope and date; packaging is not a fresh literature review.

The acceptance is independent AI-assisted mathematical auditing, not human peer review, journal acceptance or formal proof-assistant verification. This addition changes no queue file or turn count and adds no substantive proof-search approach.
