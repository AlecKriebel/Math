# Source-first reconstruction (pinned before candidate inspection)

Timestamp: 2026-10-06T04:07:30.287958+00:00

## Literal target

The complete Volker Kaibel contribution begins on printed page 3014 and continues on printed page 3015 of Oberwolfach Report 50/2018. I independently extracted and rendered PDF pages 46-47. Problem 2 is separate from Problem 1. Its input is a directed graph D=(V,A), a root r in V, and a vector c^v in R^A for every v other than r. Its objective is to choose an arborescence T subset A minimizing sum over v other than r of c^v(P^v), where P^v subset T is the r-to-v path. The path requirement for every nonroot vertex makes the feasible object a spanning out-arborescence rooted at r. The source attaches motivation through Wong's extended formulation; verifying that motivation is not needed to prove NP-hardness of the explicitly stated combinatorial problem.

I interpret c^v(P^v) as sum_{a in P^v} c^v_a. Thus an arc shared by two destination paths can be charged twice, using two different coefficients. This is not a single scalar-weight arborescence objective. A hardness proof may use a subclass of the allowed real costs. A classical decision complexity statement must explicitly supply finite encodings, such as binary rational coefficients and a binary rational threshold. The all-real optimization wording itself is not a finite-input decision language without a representation model.

## Initial falsification criteria

A valid reduction must provide a polynomial-size finite instance and demonstrate equivalence for all feasible arborescences, not just a hand-picked family. Root reachability and exactly one parent per nonroot vertex must force global variable consistency. Every selected root-to-clause path must be accounted for at every destination, including auxiliary variable vertices. The exact objective must be derived without assuming that the tree is already a canonical assignment tree. Need boundary cases for empty clauses, tautologies, repeated literals, no clauses, no variables, duplicate or unused variables, and the preprocessing needed to keep the target feasible and preserve any indegree or layering promise. Need proof of size using dense destination-by-arc encoding, exact rational bit complexity in NP, and a bounded-numeric reduction to justify strong NP-hardness. A {1,2} modification is only safe if added unit costs sum to the same constant on every feasible tree.

## Independent source NP-completeness basis

I independently rendered PDF pages 10-11 (printed 94-95) of Karp's original contribution. Printed page 94's main theorem says all the listed problems are complete. Printed page 95's item 11 is satisfiability with at most three literals per clause, from positive and negated variables. This provides the intended finite Boolean reduction source; it does not need an exact-three-distinct-literals convention. Empty clauses, if admitted by at-most-three syntax, are immediately unsatisfiable and must be handled separately or excluded by a satisfiability-preserving preprocessing rule with a valid fixed no-instance.

## Status

Candidate PROOF.md, original review, and other current families have not been read. Completion estimate: 15% for this verification audit, not for the mathematical discovery.
