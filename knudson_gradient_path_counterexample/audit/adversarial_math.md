# Independent adversarial mathematical audit

Audit timestamp: 2026-09-23 03:28:56 UTC. Mathematical verification completion estimate: **100% for the counterexample to the published Conjecture 2**. This estimate does not cover historical priority, catalogue status, or publication preparation.

## Verdict and exact scope

**PASS.** The seven-simplex example refutes Knudson's Conjecture 2 as published in his contribution to Oberwolfach Report 29/2008. Its nonincident persistence pair `(b, ac)` has zero gradient paths in the specified, fixed vector field. No mathematical gap was identified. This is a negative resolution of that universal statement, not a claim about every possible sequential-cancellation reformulation.

The catalogue identifier OWR-2040-002 is supplied by the user. Its live page could not be independently read during this audit; the verdict rests directly on the original mathematical source. Priority is a separate question.

## Source and hypothesis check

Read the complete contribution, printed pp. 1628–1630, including the material before and after Conjecture 2: Kevin P. Knudson, *Persistent homology and discrete Morse theory*, in *Computational Algebraic Topology*, Oberwolfach Report 29/2008, [report DOI](https://doi.org/10.4171/OWR/2008/29), [primary PDF](https://ems.press/content/serial-article-files/46173).

The setup requires a finite simplicial complex, a filtration adding one simplex at a time, and coefficients in F2. Its face notation means codimension one. The persistence pairing uses the youngest available positive simplex after previous pair eliminations. The field `V_P` retains precisely the incident pairs. Conjecture 2 predicts one gradient path for each remaining persistence pair, in this same field. It has no positive-dimension, closed-manifold, geometric-filtration, or connected-intermediate-stage hypothesis. The subsequent cancellation discussion explains a consequence; it does not replace `V_P` by an iteratively modified field. The following conjecture concerns a different construction and adds no assumption here.

## Independent derivation

Use the filtration

`a, b, c, d, cd, bd, ac`.

All edge endpoints are already present when their edge enters. There are no other nonempty simplices. The final complex is the interval with vertex sequence `a-c-d-b`.

An independent component argument obtains the pairing without relying on the submitted program. The edge `cd` merges the components born at `c` and `d`, killing the younger birth `d`. The edge `bd` joins the component whose surviving oldest vertex is `c` to the older component born at `b`, killing `c`. The edge `ac` then joins the surviving component born at `b` to the oldest component born at `a`, killing `b`. Thus

`P = {(d, cd), (c, bd), (b, ac)}`.

Only the first pair is incident. Hence `V_P = {(d, cd)}`. The complete directed incidence graph is

`ac -> a`, `ac -> c`, `bd -> b`, `bd -> d`, `d -> cd`, `cd -> c`.

No arrow leaves `a`, `b`, or `c`. In particular the reachable set from `ac` is exactly `{ac, a, c}`, which excludes `b`. This proves nonexistence of a gradient path, independently of any question about path uniqueness. The graph is acyclic by direct inspection, so the field is a valid discrete gradient.

The submitted verifier was read. Its ordinary F2 reduction, independent elder-rule computation, matching construction, topological sorting, and path enumeration implement the claimed checks correctly for this input. A separately written inline computation using signed boundaries and exact rational arithmetic gave reduced columns `d-c`, `c-b`, `b-a`, the same three pairs, and the same reachable set. Its checks passed. Since all eliminated pivot coefficients are units with value 1 or -1, this signed calculation also establishes the same example over any field; that extension is optional and unnecessary to refute the F2 conjecture.

## Attempts to invalidate the example

- **Unallowed filtration:** every face precedes its coface, no simultaneous insertion or tied birth is used, and relabeling the indices from 1–7 to 0–6 changes nothing.
- **Wrong homology convention:** ordinary H0 leaves `a` essential and yields the pairs above. Even reduced H0 gives the same finite pairs, so an essential-class convention cannot rescue the conjecture.
- **Invalid field or noncritical endpoints:** `b` and `ac` are both absent from the only matching pair and therefore are critical. The matching has no repeated simplex and its directed incidence graph has no cycle.
- **Path-definition ambiguity:** the report's abbreviated displayed V-path definition omits the usual restriction against immediately returning through the same matched incidence. Its later reversed-Hasse convention disambiguates the intended gradient notion. The zero-path conclusion is even stronger: after either initial descent from `ac`, no matched upward step exists under either reading.
- **Confusing persistence reduction with geometric paths:** eliminating a pivot at `c` using the reduced column of `bd` is legitimate algebra. It cannot create the missing incidence `c < bd` in the original complex.
- **Sequential cancellation:** the other nonincident pair has the unique path `bd -> d -> cd -> c`. Reversing it changes the matching to `{(d, bd), (c, cd)}` and then creates `ac -> c -> cd -> d -> bd -> b`. This supports the candidate's explanation and does not supply a path in the original field.
- **Overstated conclusion:** the audit establishes failure of the published universal statement, including its existence assertion. It establishes no historical novelty, no resolution of Conjecture 3, and no general theorem about successive cancellations. A minimality claim is not needed and was not used.

## Remaining gap

None in the mathematical counterexample or its applicability to the published Conjecture 2. Historical priority and the present status of the user-supplied catalogue entry require separate evidence. External communications were neither prepared nor initiated.
