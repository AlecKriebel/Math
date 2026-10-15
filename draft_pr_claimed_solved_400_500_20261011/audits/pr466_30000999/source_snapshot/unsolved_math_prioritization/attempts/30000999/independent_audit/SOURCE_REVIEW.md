# Source and duplicate review

Problem 30000999 / OWR-2042-008. Independent read-only check, 3 October 2026.

## Primary source

[Official report](https://ems.press/content/serial-article-files/46174),
[DOI](https://doi.org/10.4171/OWR/2008/31).

The mathematical source identification and exact scope pass; the concise
findings are in Section 2 of `AUDIT.md`. Printed p. 1763 was checked visually,
in addition to extraction. No PDF, page image, or complete source extraction
has been copied into these audit deliverables.

## Classical attribution

[Quellmalz, Analysis and Mathematical Physics 10, 38 (2020)](https://link.springer.com/article/10.1007/s13324-020-00383-2)
was read at its normalized-transform definition, nullspace discussion, and
Sobolev range statement. Its bibliography and attribution reinforce that
the parity obstruction and smoothing spectrum are classical. The exact
same-order Wasserstein counterexample theorem is proved in the audited
package itself; no claim that Quellmalz already states that exact theorem is
made.

## Independent repository duplicate check

Read-only GitHub connector searches were scoped to `AlecKriebel/Math`:

- PR query `30000999`, all states, at most 30 results: none.
- PR query `OWR-2042-008`, all states, at most 30 results: none.
- Default-branch code query `30000999`, at most 20 results: none.
- PR query `Radon`, all states, at most 30 results: four results, none identical.
- PR query `Wasserstein`, all states, at most 30 results: one result, unrelated.

Returned Radon-adjacent work concerned [domain-local Crofton measures](https://github.com/AlecKriebel/Math/pull/120),
[signed-measure Cramer–Wold extensions](https://github.com/AlecKriebel/Math/pull/231),
[planar capacity](https://github.com/AlecKriebel/Math/pull/423), and
[geodesic currents](https://github.com/AlecKriebel/Math/pull/38).
The Wasserstein match concerned [Markov-generator contraction methods](https://github.com/AlecKriebel/Math/pull/273).
The returned titles and descriptions do not concern the target equator
operator and its reverse Wasserstein estimate. This is not a proof that no
same-problem work exists in unindexed files, remote branches, or elsewhere.

## Bounded public literature search

Searches used the exact Stephens contribution title; the Quellmalz title;
`Funk Wasserstein inverse inequality`; `Geodesic Radon Wasserstein inverse`;
`Funk Radon Wasserstein stability`; and `30000999 Radon`.

They confirmed primary sources and found adjacent spherical sliced-transport
literature. Those constructions can use different, injective transforms and
must not be conflated with the normalized equator operator here. I found no
exact same-theorem prior publication in this bounded pass. This says only
what this search located; it supplies no positive claim of novelty, priority,
or exhaustive clearance. The classical nature of Theorem 1 is already clear
from the operator's odd kernel, independent of any search result.

## Disposition

**PASS for source fidelity and appropriately limited attribution.** Keep
the author's no-novelty disclaimers. The audit has made no external writes,
contacts, queue edits, or publication actions.
