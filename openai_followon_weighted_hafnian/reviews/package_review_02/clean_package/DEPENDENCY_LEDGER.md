# Dependency ledger

| Dependency | Exact required statement | Citation / validation | Status / limitation |
|---|---|---|---|
| Unweighted FPRAS | All finite simple graphs; nonnegative rational estimate, relative error epsilon, failure delta<1/2, every-tape bit polynomial in input, epsilon inverse and log delta inverse; zero on infeasible; empty count one | OpenAI Theorem1.1, pin adc7f1241b42e322a6451854ab7e4b4c146bf78a; full manuscript audit UPSTREAM_PROOF_AUDIT; real Lean thm_main source semantics FORMAL_SCOPE_AUDIT | Mathematical source audit passed; kernel build and actual axiom closure not reproduced |
| Exact support feasibility/witness | Deterministic polynomial algorithm finds maximum matching in general graphs; perfect iff size equals half order | Edmonds, Paths, trees, and flowers, CJM17(1965),449–467, doi10.4153/CJM-1965-045-4 | Established external theorem; only finite reference helpers implemented locally |
| Integer gadget and gluing | Signature(W,1,0,0), O(log W) simple graph, fiber product and parity | GADGET_PROOF; exact code and separate reconstruction | Verified proof plus finite checks; old weight-removal mechanism, Horner variant |
| Rational scaling | Product denominators D, integer weights W; #PM(H)=D^m haf(A), O(L²) graph, polynomial arithmetic lengths | GADGET_PROOF and manuscript Theorem2 | Verified; no numeric expansion |
| Count-to-sample | <=s² calls; adaptive next-step TV budgets yield <5eta/6; exact zero branches, feasible fallback, fixed dyadic draw | SAMPLING_PROOF; classical JVV framework; code exact-law integration | Self-contained quantitative proof; uses base FPRAS and Edmonds |
| TV pushforward | Finite deterministic map contracts TV; uniform fiber mass gives weighted distribution | Elementary triangle inequality and gadget fibers | Proved |
| Priority comparison | Exact binary rational equivalence already public; restricted hafnian algorithms distinct | McQuillan2013 §7.2 Lemmas25–27; Dell2010 §3; RSZ2016; Barvinok2017; Yi2026; PRIORITY_AUDIT | Audited primary theorem statements; no proof of absence of an identical exposition |
