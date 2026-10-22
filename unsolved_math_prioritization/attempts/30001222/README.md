# Quantum complete intersection rigidity: audited partial results

Target: rank 668, ID 30001222, OWR-3400-006. Publication checkpoint: 4 October 2026.

**Disposition: unsolved, 5/5 substantive approaches completed.** The complete frozen author packet and separate adversarial AI audit are preserved. No full resolution, counterexample satisfying every hypothesis, novelty certificate, or human peer-review claim is made.

Read [RELEASE_CLARIFICATIONS.md](RELEASE_CLARIFICATIONS.md) together with the unchanged [proof and partial results](packet/PROOF_AND_PARTIALS.md), [five-approach log](packet/APPROACH_LOG.md), and complete [independent audit](audit/AUDIT_REPORT.md). Historical statements in the frozen author packet that the audit is pending describe its pre-audit state; the audit and this wrapper record the later publication gate.

## Strongest conclusions and exact gaps

- Center reconstruction settles the commutative case. The split-local rank congruence is necessary and does not imply rank-one equivalence bimodules.
- A **k-linear derived equivalence** between finite-dimensional local k-algebras gives a k-algebra isomorphism. No derived lift from the target stable equivalence is provided.
- The 36-dimensional F11 pair is nonisomorphic, with matching ordinary centers, radical layers, and HH1 dimensions. Its stable equivalence of Morita type is **UNDETERMINED**: neither established nor excluded here.
- The characteristic-three 9-dimensional deformation pair is **EXCLUDED** from stable equivalence of Morita type by HH1 dimensions 8 and 7.
- The precise Benson–Kessar–Linckelmann bound retains parameter order **e ≥ 2** dividing p−1, odd characteristic p, the specified p-power truncation family, and a split local symmetric partner. The target's commutative e=1 case is covered separately by center reconstruction.
- Ordinary-center isomorphism remains an independent hypothesis. Stable-center invariance is not ordinary-center invariance. Matching invariants do not construct an equivalence.

The general noncommutative reconstruction or lifting step remains open in this investigation. Completion estimate: the five-approach record and its independent audit are 100% complete; no meaningful numerical percentage toward a proof of the general target is claimed.

## Reproduce offline

Python 3.8+ and its standard library suffice. From this directory:

    python -B verify_release.py

This verifies every release file, both exact archives and their extracted members, both inner manifests, the audit input binding, and byte-identical reruns of the author's 204,097 exact assertions and the structurally independent word-rewriting/full-cocycle calculation. These are computational checks, not counts of independent mathematical proofs. For a quick inventory-only check:

    python -B verify_release.py --integrity-only

The original independent checker obtains derivations from every basis-pair cocycle equation and also checks the Higman/projective-center dimensions and symbolic characteristic-three cube identities. No equivalence bimodules are produced.

## Frozen inputs and safe scope

- Author archive: `rank668-30001222-authored-packet.zip`, 23,282 bytes, 10 files, SHA-256 `4fc5af73089e545434dbb7020c197edb070066208122ad03237879da58bb01fa`.
- Audit archive: `rank668-30001222-independent-audit.zip`, 17,826 bytes, 10 files, SHA-256 `2fff6f35083905fbbbaa50f8f599cd61bc91b63e7acef1bfbf28114c6b45cc64`.

All 20 extracted files retain their exact frozen bytes. The release includes authored analysis, code, results, and public scholarly/provenance metadata. Source PDFs, extracted source text, dataset contents, and private coordination files are excluded. Dataset provenance remains the author's recorded evidence; the audit did not repeat dataset-wide searches. Bounded source and duplicate searches do not certify novelty or global open status.

The queue change is limited to this target's Status and Turns cells. All other queue bytes, including its existing header and links, are preserved. No queue regeneration, merge, GitHub release, DOI, or outside outreach is part of this publication.
