# Five-turn partial outcome: complex ordinary conics

**Original problem 30003084 remains unsolved after 5/5 substantive author turns. Independent review is pending.**

The exact source asks whether every finite set in the complex projective plane not contained in a conic has a conic uniquely determined by exactly five of its points and containing no others. Singular and reducible conics count. The existing real theorem and finite-field counterexamples do not decide this complex question.

## Retained partial theorems

1. Every such complex point set of at most ten points has an ordinary conic. Quadratic interpolation and Gale duality reduce the claim to explicit low-rank circuit geometry, including zero and proportional Gale columns. The rank-four classification and its two exclusions are proved in TURN_3.
2. Every finite nonconic set contained in any complex projective cubic has an ordinary conic. The smooth irreducible case uses elliptic divisor theory, complement reflections and abstract characters. Singular irreducible cases have explicit normalization parameters. Every reducible case, including component intersection points, is treated in TURN_5.
3. A line-rich set has an ordinary conic whenever a line contains l points and the remaining r satisfy l>=max(4,r-1). This is proved by excluding at most one second line-intersection for each additional outside point.
4. The full three-line Fermat family with 3n points, n>=3, has at least 3n times binomial(n,2) distinct ordinary reducible conics. Four exact Hesse/Fermat configurations also have explicit ordinary conics, so none is a counterexample.

These are scoped research candidates and credited classical-method consequences, not a priority claim or a full resolution of the source question.

## What remains open in this attempt

A hypothetical counterexample must have at least eleven points, be contained in no cubic, and place at most floor((n-2)/2) points on any line. No proof or counterexample is provided for all configurations satisfying those necessary conditions. The low-rank Gale classification is not silently extended to arbitrary rank, and residual reflection laws require the particular cubic geometry.

## Five substantive turns and checks

- Turn 1: exact Hesse/Fermat counterexample tests and the general Fermat-family lower bound; 29,835 five-subsets in the four fixed configurations
- Turn 2: interpolation/Gale proof for at most nine points
- Turn 3: complete rank-four circuit argument extending the bound to ten points; 1,018 finite exact algebra, graph and Gale controls
- Turn 4: irreducible-cubic theorem, including singular cases; 610 finite/symbolic controls
- Turn 5: all reducible cubic supports and the large-line criterion; 873 finite/symbolic controls and six explicit rational witnesses

The counts describe finite computational receipts; none replaces the universal proofs or the requested independent audit. Source retrieval, an intervening independent review of another problem, and packaging were not counted as author turns.

Run the three verification scripts with Python and SymPy; they write JSON to stdout. `explore_configurations.py` uses only the standard library and exact Q(omega) arithmetic. Its first two configurations reproduce `turn1_small_configurations.jsonl`, and arguments `fermat18 hesse21` reproduce `turn1_larger_fixed_configurations.jsonl`. No downloaded source executable is needed. Complete source PDFs and text are excluded from the public packet.

`TARGET.json` is the original source-gate queue snapshot, not the final research status. Current metadata and this result supersede its queued/zero-turn fields. The final reviewed outcome should update only this problem's queue row to unsolved 5/5 after the separate publication gate.
