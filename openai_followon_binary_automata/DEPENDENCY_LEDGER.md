# Dependency ledger

Pin: openai/math adc7f1241b42e322a6451854ab7e4b4c146bf78a. Source clone read-only. Hash manifest and independent audit receipts pending.

| ID | Precise dependency | Assumptions / use | Validation basis | Status / gap |
|---|---|---|---|---|
| D1 | OWL_h 2DFA bound 2^floor((h−2)/31)≤4(s+2)², h≥2 | All relation letters, finite-run conventions; apply binary-target pullback | Original manuscript, actual Automata.Main.main_theorem and model inspected; independent audit underway | Not yet certified; central rank-loss and semantic representation audit pending |
| D2 | Product-emptiness 2NFA bound 2^floor((h−2)/127)≤2(s+1), h≥2 | Complement within Σ_h*; pullback must recognize emptiness exactly | Original manuscript, actual TwoWayAutomata.Main theorem and Source inspected | Not yet certified; transport/nesting/amplification audit pending |
| R1 | Fixed h² adjacency encoding | Explicit source and target compilers; all binary words defined | Independent derivation underway; prior machinery in Kapoutsis 2013 | Uniform proof/counts and exhaustive boundary probes pending |
| F1 | Lean proof checking and semantic correspondence | Only if invoked as validation of D1/D2 | Real proof files have no directly found sorry/axiom; comparator templates excluded | Pinned-copy builds and #print axioms pending; file existence is not verification |
| P1 | Priority / previous binary results | Accurate scope and no duplicate novelty claim | Independent primary-literature search underway | Exact statements/citation chain/public dates pending |
