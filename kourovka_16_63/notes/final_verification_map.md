# Final verification map

The earlier construction checkpoint is preserved as a historical candidate-stage note. `progress.json` and the final report supersede its unfinished list.

| Obligation | Proof / evidence |
|---|---|
| Exact question and archival distinction | Literature ledger; notebook pp.102,255 inspected |
| Explicit group, not library identifier | Report Definitions2.1 and5.1; full finite Lie table in JSON; canonical BCH rule |
| Consistency of integral Lie bracket | Integer Jacobi proof and both implementations, 4495 triples in each basis |
| Full finite-field automorphisms | Report Proposition3.2, including radical complement argument, PGL2 and swap component |
| No hidden semisimple / finite automorphisms after lattice choice | Report Proposition4.1, explicit weight contradictions |
| Every finite automorphism, not only those lifting exactly | Report Lemma5.2, approximate-relator errors and ambient Lie-word integrality |
| Derivation-to-automorphism correspondence without precision loss | Report Section6, explicit matrix/tensor lattice bounds and convergent integral series |
| Full automorphism cardinality | Report Proposition6.3 plus complete Smith kernel count |
| Exact Smith invariants and no hidden high-valuation invariants | Python modulo p^12, replay modulo p^6; independent C++ modulo p^6; 931 nonzero pivots plus 30 inner derivations bound the rational rank |
| Exact group order and BCH consistency | 31 coordinate normal forms modulo p^1689, class bound846<p1009, finite Lazard equivalence |
| Full group rather than Lie-only answer | Lazard equality of FULL automorphism groups, actual finite hypotheses checked in primary paper |
| Corrupted-certificate rejection | Executed nonzero-exit test with first pivot valuation changed0 to5 |
| Reproducible delivery | `python3 scripts/resume.py`, executed successfully; `--full` for Python regeneration |

No external reviewer or formal proof assistant is part of the evidence. The group has not been enumerated or stored as a Cayley table. Those are verification boundaries, not missing steps in the stated mathematical argument.
