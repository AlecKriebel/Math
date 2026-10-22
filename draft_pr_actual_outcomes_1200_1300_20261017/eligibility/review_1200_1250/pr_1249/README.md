# Forest correlation: exact reductions, known families, and shortcut obstructions

Problem 3309 / OPG-1757. Status: **PARTIAL**. The general distinct-edge conjecture is unresolved by this work; no novelty is claimed.

This is an AI-assisted, unrefereed authored-prose edition with an internal AI mathematical audit. It has no external human peer review or formal proof-assistant certification. It is not a computational reproduction package: the complete mathematical arguments and essential formula witnesses are included, while programs, raw expanded certificates, source documents, and datasets are not distributed. Historical checks and source inspection are described as historical evidence, not as newly executed checks or blanket acceptance of external source proofs.

## Exact target

For a finite simple graph, choose uniformly among all acyclic edge subsets, including the empty subset and isolated vertices. For distinct edges e,f, ask whether P(e,f in F) ≤ P(e in F)P(f in F). This is pairwise negative correlation. The original display's missing distinctness is repaired from Grimmett–Winkler's primary formulation; self-pairs, rooted forests, spanning trees, fixed-component forests, and full negative association are different questions.

## What is established

- U ⇔ B ⇔ W: the universal uniform-simple, uniform-simple-bipartite, and positive-weighted-loopless-multigraph versions are equivalent. The proof explicitly counts path-gadget fibers, transfers covariance of individual marked microscopic edges, and passes to arbitrary positive activities by continuity.
- Exact weighted K4 identities prove the property on K4. Series, parallel, disjoint/one-vertex products, precisely defined terminal edge gluing, and minors preserve it. All pair positions and boundary cases are addressed.
- Triangle non-real-stability, the K4 negative Rayleigh coefficient, and the rooted-star projection mismatch invalidate three stronger shortcuts, not the conjecture.

These are self-contained derivations of reductions and established family results. Uniform-to-weighted equivalence, the Semple–Welsh K4-extension family, and Cocks/Wagner closure receive prior credit in the complete proof and audit. Source text is not needed to follow those derivations.

## Read the edition

- [PROOF.md](PROOF.md): complete mathematical proof, exact hypotheses, essential witnesses, prior attributions, and residual.
- [AUDIT.md](AUDIT.md): complete independent internal mathematical audit and bounded historical check coverage.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json): bounded acceptance, exclusions, and document bindings.
- [SOURCES.json](SOURCES.json): public titles, URLs, hashes/sizes, historical inspection scope, manuscript caveats, and corpus authentication metadata.
- [VERIFICATION.json](VERIFICATION.json): authenticated inventory identities and historical check receipt metadata.
- [MANIFEST.json](MANIFEST.json): exact eight-file inventory, with the other seven files' byte counts and SHA-256 hashes; its own hash is supplied separately.

Corpus 30006450 / OWR-14299575-001 shares the first all-one-vector pairwise question; its broader interpolation-class question is untouched. Neither record is a solved problem here, and the overlap provides no duplicate solved count. The source is Oberwolfach Report 47/2025, distinct from the corpus's 2026 display year.

## Evidence limits

The historical independent checks used exact symbolic/rational arithmetic and five finite gadgets in Python normal, -O, and -OO modes. They do not exhaust all graphs or replace the complete general counting/continuity proofs. Editorial preparation authenticated bytes and checked packaging without rerunning mathematical programs or inspecting new scholarly sources. No external paper is blanket-accepted; recent manuscript claims and date anomalies remain explicitly qualified. Hashes identify bytes, not truth, novelty, copyright permission, or external certification.

The exact remaining task is Δ_G(e,f) ≥ 0 for every finite loopless graph, positive activity vector, and distinct edge pair, equivalently the original uniform-simple or simple-bipartite conjecture.
