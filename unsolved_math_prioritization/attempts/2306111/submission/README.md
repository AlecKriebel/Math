# Problem 2306111: Janowski convex coefficient neighbourhoods

**Status: unsolved; 5/5 substantive approach turns used.**

No complete proof or counterexample to Hayman–Lingham Problem 6.111 was found. No claim is made that the problem remains open in all current literature: a directly relevant 2020 paper could be inspected only at metadata/abstract level.

The strongest proved results are:

1. The proposed radius is the sharp uniform radius for **univalence** for every -1<=B<A<=1.
2. The original starlikeness assertion is equivalent to an explicit 2 by 2 singular-value inequality. Any failure has a **single quadratic coefficient perturbation** witness.
3. The recorded positive theorem guarantees starlikeness at least on |z|<(2+sqrt(3))/(4|B|) in the missing parameter region.

`FULL_PROOF.md` contains complete arguments for these partial results and the exact residual statement. `APPROACH_LOG.md` and `turns.jsonl` record five distinct routes. `SOURCE_GATE.md` and `SOURCE_MANIFEST.json` distinguish primary authority, prior triage, current metadata, and retrieval limitations.

Reproduce the lightweight algebraic/numerical controls with:

    python3 verify.py
    python3 verify_manifest.py

Optional finite atomic-measure search (requires NumPy and SciPy):

    OPENBLAS_NUM_THREADS=1 python3 finite_search.py

The preliminary four-seed variable-parameter search is also preserved as exploratory_search.py and EXPLORATORY_SEARCH_RESULTS.txt; replay it with OPENBLAS_NUM_THREADS=1 python3 exploratory_search.py. Both search scripts require NumPy and SciPy.

The searches are bounded and non-exhaustive. Neither a passing control suite nor a matching manifest proves the target.

Author: Alec Kriebel, https://orcid.org/0009-0001-9320-500X.
