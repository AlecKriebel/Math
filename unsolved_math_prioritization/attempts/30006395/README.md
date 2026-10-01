# 30006395 / OWR-14299518-013

**In progress after substantive author turn 3 of 5. Original detection transition unresolved.** No final PR or queue promotion. No novelty claim.

The exact target is an unknown uniform labelled Cayley tree planted in G(n,c/n), with fixed mean degree c. The source separates a revealed-template O(log n) bound from an unknown-tree O(log² n) bound; the latter is not a proved sharp lower endpoint. `SOURCE_GATE.md` preserves the historical source-only checkpoint.

`TURN_1.md` proves an exact forest-overlap second moment for the unknown-shape mixture. It gives the complete square-root strong-detection scale for fixed c>e, and a lower bound at c=e: indistinguishability for k=o(n^(4/9)). The latter is not an established critical threshold. An exact finite checker validates the enumeration with 312,359 assertions and 972,471 ordered tree pairs.

`TURN_2.md` gives an actual hairy-path detector for k/log²n tending to infinity when g(c)=(c+1)log(1+1/c)−1−log c>0. This includes c=4/3, with unique criterion root c_h between 4/3 and 7/5. Exact path-prefix conditioning is checked on 18,248 trees. Together with monotonicity and Turn 1, the true polylog-detection boundary lies between c_h and e; it is not identified.

`TURN_3.md` identifies the exact two-parameter critical second-moment limit near c=e and proves that n^(4/9) is the sharp scale for L² convergence to 1 at c=e. This is an L² threshold, not a total-variation or detection threshold. A nontrivial finite moment does not itself prove weak detection.

The original gap remains: a matching detection theory in the intervening mean-degree regime, the true transition location/form, and a sharp unknown-tree low-c scale. Divergent second moments do not prove detection; mixture bounds do not automatically apply to revealed templates.

The per-turn manifests bind immutable mathematical/source inputs. Global log/ledger/README may evolve in later turns. Full independent review is required before a final partial or claimed-full result is published.
