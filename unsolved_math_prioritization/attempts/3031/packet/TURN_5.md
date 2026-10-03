# Author turn 5: arbitrary-palette extension attempt and final gap

2026-10-03 UTC. Outcome: exhausted,5/5; original conjecture unsolved. Best-guess full-target completion:10% (subjective).

## Attempted extension
The finite crossing-core bound suggests beginning with a small m-avoiding palette and adding missing colors until the required c is reached. I tested the simplest module extension on the exact (112,43) certificate: add a vertex with new spoke color 112 and background-color 0 edges to every old core vertex. This produces113 colors.

The new infinite spectrum is F∪(F+1), where F is the old spectrum. The old witness has 42 in F, so the extension necessarily introduces43. `extension_failure.py` independently checks the original65536 subsets using the general rooted verifier, then all 131072 extended subsets. It records an explicit 43-color witness. The extension is rejected, not reported as a113-color counterexample.

## General obstruction to disjoint palette padding
Take rooted models A,B with common background0, otherwise disjoint color palettes, and give every cross-core edge color 0. Their glued infinite spectrum is
F(A glue B)={a+b−1:a in F(A),b in F(B)}.
This follows directly because the palette is the union of the two selected palettes and their only common color is0. Every nontrivial rooted module B realizes exactly 2 colors: if it has a nonzero spoke, select that vertex; otherwise select the endpoints of any nonzero edge. Thus if m−1 belongs to F(A), any such nontrivial module introduces m.

This rules out the attempted route of obtaining arbitrary c by palette-disjoint neutral extensions of the useful112-color example, and more generally of any model whose spectrum contains m−1. It does not rule out interacting palettes, nonzero cross colors, or independently designed exact-c models.

## Final strongest result and precise unresolved obligation
The packet proves explicit finite models and bounded certificate checks; a full construction for the normalized p−q=6 subfamily; larger-gap proper-clique semigroup families; and two exact architecture obstructions. None settles the complete source claim for every c>m≥3. In particular the compact-gadget route does not resolve(262,64); this is a gap in this packet, not a claim that all literature leaves that pair open.

A full result still needs either (a) an m-avoiding surjective c-coloring for every remaining pair, with a verified exhaustive reduction if relying on the 2025 asymptotic theorem, or(b) a proof of P(c,m) for one pair c>m≥3 that refutes the conjecture. No such final step was obtained within five substantive author turns.

No additional proof-search turn is authorized by this budget. The local packet is frozen for uninvolved adversarial review of its partial results, scope, provenance and tests. Original-target status must remain exhausted/unsolved, even if all partial theorems pass review. Source alias3114 receives no separate attempt. No remote write, PR, merge, release or publication has occurred.
