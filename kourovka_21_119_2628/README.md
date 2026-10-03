# Unbounded finiteness lengths of virtual algebraic fibers

KOU-21.119, catalogue ID 2628. Research notes, 3 October 2026.

## Verdict

**Unresolved after five substantive proof-attempt turns.** No group satisfying the entire question and no universal impossibility theorem has been obtained. These AI-assisted notes are unrefereed. Independent adversarial review is pending. No historical novelty or full-solution claim is made.

The problem asks for one group G with finite-index subgroups G_n and maps G_n→Z whose kernels are F_n but not F_{n+1}, for every n. F_n means a classifying space with finite n-skeleton. A separate ambient group for each n, an arbitrary subgroup of one group, or only homological FP_n finiteness does not suffice.

## Proved scope

- Turn 1: G must be F_∞; the maps may be surjective with nested normal finite-index domains. The virtual fiber spectrum is a commensurability invariant. Virtual first Betti number at most one is excluded.
- Turn 2: a product of M nonabelian finite-rank free groups has exactly the finite virtual fiber lengths 0,…,M−1. Explicit cyclic-cover homology cycles certify the negative finiteness bounds. The positive construction is credited to Bieri–Stallings and Bestvina–Brady.
- Turn 3: no group of finite virtual cohomological dimension can satisfy the question.
- Turn 4: the finite virtual fiber spectrum of Thompson F is exactly {0,1}, as a consequence of the established Bieri–Geoghegan–Kochloukova invariants and an explicit character-extension argument.
- Turn 5: kernels of virtual integral characters preserve oligomorphicity. The tested wreath-product construction cannot produce the desired finiteness threshold by a first failure of finite tuple-orbit counts.

## Exact remaining gap

An example would need an F_∞ group outside finite virtual cohomological dimension with genuinely unbounded finiteness lengths of virtual character kernels. In the tested wreath-product route, tuple-stabilizer kernel finiteness, characters nonzero on the lamps, and other finite-index subgroup forms remain unanalyzed. Neither finite-dimensional character spheres nor the presence of arbitrary subgroups of all finite finiteness lengths settles the question.

## Checkable artifacts

The five turn files contain the arguments. Run `python verify_chain_certificates.py` to reproduce `verification.json`. The script checks Laurent-polynomial cellular identities and finite illustrative cases only; it does not prove the cited theorems, classify infinite groups by computation, or resolve the original question. The source gate and research log document provenance and limitations. `MANIFEST.json` binds this version, excluding itself.
