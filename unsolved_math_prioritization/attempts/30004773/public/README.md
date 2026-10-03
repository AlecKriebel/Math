# Character degrees of graph-defined exponent-p groups: partial results

**Disposition: unsolved.** This is an AI-assisted, unrefereed research packet for catalogue problem 30004773 / OWR-8415341-012. It does not claim a complete resolution or historical novelty.

The primary question is Tobias Rossmann's problem on pp. 2081–2082 of [Oberwolfach Report 38/2021](https://ems.press/journals/owr/articles/8415341): for a fixed finite simple graph, describe how the counts of degree-p^i ordinary irreducible characters of its class-at-most-two exponent-p group depend on the odd prime p. The 2022 paper [Enumerating conjugacy classes of graphical groups over finite fields](https://doi.org/10.1112/blms.12665), §1.6, Question 1.10, states the related prime-power version and its known alternating-matrix reduction. The solved conjugacy-class enumeration problem is different from the character-degree question.

## Established here

- A complete explicit character construction gives ch(Gamma,i;q)=q^(n-2i) N_i(Gamma;q), with N_i counting graph-supported alternating matrices of rank 2i.
- For every graph, a finite vertex-subset formula computes N_1 as an integer polynomial, thus computing the number of degree-q characters.
- For forests, every N_i is given by a polynomial sum over edge subsets with matching number i.
- If the graph has maximum matching size at most three, two moments and the rank-two formula recover every N_i as an integer polynomial. This includes all graphs on at most seven vertices and some arbitrarily large graphs.
- The bipartite reduction and Schur-complement identity explain precisely where the attempted extension to arbitrary higher-rank graphs stalls.

The first reduction and the class-count polynomial are standard and are credited in the source gate. The other partial formulas are proved in full; their historical priority has not been established.

## Files and verification

Read the five numbered TURN files in order. SOURCE_GATE.md records the exact target, source distinctions, and bounded prior-work checks; ATTEMPT_LOG.md records the five analytic approaches and remaining gaps.

Run with Python 3 and its standard library only:

    python3 verify.py --check
    python3 verify_bundle.py

The first command reproduces the exact finite receipt: 83,201 alternating matrices across 157 graph/field cases, 80,312 representation-phase checks, 16,354 rectangular-to-alternating rank checks, and 486 Schur-complement checks. The 5,400 forest-weighting checks and 156 polynomial-recovery checks are subsets of those controls, not independent extra enumerations. The finite checks support implementation and boundary-case reliability; the written proofs establish the unrestricted partial theorems.

The SHA-256 manifest covers the public packet, excluding the manifest itself. No downloaded source PDF, source text corpus, or private research material is distributed. The packet remains subject to independent review.
