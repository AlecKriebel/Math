# Conditional page content — finite WARM graphs

This is an editorial candidate only, pending independent mathematical clearance and the parent publication gate. No page has been created or published by this scope task.

Suggested slug: `finite-warm-forest-whisker-bounds`

Suggested search title: `When reinforced graphs become forests | Alec Kriebel`

Suggested description: `A finite WARM graph preprint gives the sharp strict forest bound α > 4/3 and an equal-rate whisker bound α ≥ 17/4, with source files and limitations.`

Paper title: **A sharp forest bound and an improved whisker bound for finite WARM graphs**

Status: Unrefereed preprint · Version 1.0.0 · 21 October 2026. AI tools were extensively involved; internal AI review is not independent human peer review.

## In plain language

Imagine a finite network in which each vertex has its own clock. When a clock rings, one neighboring edge is reinforced. An edge that has been chosen often becomes more likely to be chosen again; the exponent α controls how strongly past choices are favored.

The paper studies the edges that continue to be reinforced forever. It shows that when α is greater than 4/3, those surviving edges almost surely contain no cycles, even when vertices fire at different rates. This strict threshold cannot be lowered: for 1 < α < 4/3, a triangle can keep all three edges with positive probability.

When all vertices fire at the same rate and α is at least 17/4, the surviving pieces have an even simpler shape. Each is a tree whose farthest vertices are at most three edges apart—a shape called a whisker. A whisker can still have many leaves; this is a bound on diameter, not on its number of vertices.

## What is interesting

A triangle already gives the obstruction for 1 < α < 4/3. The main cycle estimate shows that this small example sets the strict universal forest threshold even for much larger finite graphs with unequal rates, unequal edge weights and extra attached edges. The paper extends a known calculation for uniform bare cycles to arbitrary equilibrium weights and surrounding graph structure.

## Relation to earlier work

The question comes from Viktor Kleptsyn’s finite-graph improvement requests in [Oberwolfach Reports 12/2023](https://doi.org/10.4171/owr/2023/12). The paper uses established convergence and survival-support theorems of [Hirsch, Holmes and Kleptsyn](https://doi.org/10.1088/1361-6544/acc9a0), the uniform-cycle and triangle results of [van der Hofstad, Holmes, Kuznetsov and Ruszel](https://doi.org/10.1214/16-AAP1153), and the least-weight/champion arguments of [Holmes and Kleptsyn](https://doi.org/10.1063/1.4978683). The earlier stated whisker bound was 25; its displayed proof already yields a weaker improvement above 24. The contribution presented here is the stronger 17/4 bound together with the sharp strict forest bound, without a worldwide-firstness claim.

## Scope and limitations

The model uses finite simple undirected graphs, positive firing rates and fixed positive integer initial edge counts. The whisker conclusion requires equal rates. The paper does not settle what happens at α = 4/3 or establish the suggested sharp whisker conclusion throughout 4/3 < α < 17/4. It makes no infinite-graph, loop, noninteger-initialization or empirical biological claim.

## Paper and supporting files

- [Version-specific Zenodo record and DOI](https://doi.org/10.5281/zenodo.23592692)
- [Published paper PDF](https://zenodo.org/records/23592692/files/finite-warm-thresholds.pdf)
- [Source and verification archive](https://zenodo.org/records/23592692/files/finite-warm-thresholds-source-and-verification.zip)

The existing template may embed the authenticated PDF and retain a direct-download fallback. Use the complete original abstract in `abstract_original.txt`, preserving every qualification and the AI/unrefereed disclosure; do not substitute the summary above for the abstract.

## Collaboration

Researchers familiar with reinforced stochastic processes, stochastic approximation or dynamical systems are welcome to examine the arguments, identify corrections and discuss substantive further work or a journal submission. Any coauthorship would reflect a meaningful contribution and mutual agreement.

No new follow-up question or conjecture is proposed for this page. Existing unresolved endpoints belong in the limitations, without implying that a new route has been established.
