# Small unrestricted powerset-cover thresholds

## Model and conclusions

For a positive integer n, H_u(n) is the smallest integer h in {0,...,n} for which a map f:P([n])->[n] has f(P(Y))=[n] for every h-element Y. Both the empty set and Y itself belong to P(Y). Colors are encoded 0,...,n-1 in the files, an immaterial relabeling of [n]. This is the unrestricted model: no condition f(A) outside A is imposed. These certificates do not establish values for an exterior-coloring variant.

The exact values proved here, for n=1,...,11, are

    n:       1 2 3 4 5 6 7 8 9 10 11
    H_u(n):  0 1 2 3 3 3 4 4 4  4  4

If the definition insists on positive h, replace only H_u(1)=0 by H_u(1)=1. No exact value at n=12 is claimed by this packet.

## Elementary lower bounds

Every P(Y) has 2^h elements, so 2^h>=n is necessary. At n=2^h with h>=2, equality is impossible: each P(Y) would have to receive all n colors injectively. Every pair of distinct singletons lies in some h-set Y, and every singleton lies in such a Y together with the empty set. Therefore the n singletons and the empty set would need n+1 distinct colors. This gives H_u(n)>=ceil(log_2(n+1)) for n>=3. The exception n=2,h=1 is real: assign the empty set one color and both singletons the other color.

These arguments give all required lower bounds in the displayed table except the strengthened H_u(7)>=4. For n=1,2,3,4 the matching upper bounds are immediate: use f(A)=|A| when h=n-1, with arbitrary values on larger subsets; for n=1,h=0 use the constant map.

## Solver-independent lower certificate at n=7,h=3

The following reduction is exact.

1. Relabel f(empty)=0. Every other set assigned color 0 may be recolored arbitrarily with colors 1,...,6, without losing any required color. Thus nonempty sets may be assumed to use only these six colors.
2. A triple Y has six proper nonempty subsets: three singleton vertices and three two-element edges. Their colors must contain at least five of the six colors, since the color of Y can add at most one. Conversely this condition suffices: give Y any missing color, or any color if none is missing.
3. No singleton color occurs three times, because on those three vertices the six proper nonempty subsets could show at most four colors.
4. Some singleton color repeats, since there are seven vertices and six colors. If vertices a,b have the same color, then on every triple {a,b,c}, the other four proper nonempty subsets must all have distinct colors different from that repeated color. In particular, the edge {a,b} has a color different from the color of every singleton, including every c outside the pair. Hence at least one of the six colors is absent from all singletons.
5. The singleton multiplicity partition must therefore be either 2+2+1+1+1 or 2+2+2+1. Relabel vertices and colors to obtain respectively [1,1,2,2,3,4,5] and [1,1,2,2,3,3,4]. In the latter case, the unused colors 5 and 6 are symmetric, so the first repeated pair's edge may be fixed to color 5.

The standard-library script certify_n7_h3.py enumerates the possible colors of the 21 edges in both reduced cases. Each of the 35 triangle constraints retains exactly the edge-color triples whose union with its fixed vertex colors has at least five colors. It enforces generalized arc consistency, then branches exhaustively on every remaining value of a smallest-domain edge. A branch is rejected only when an explicit triangle relation has no compatible tuple. It uses no optimizer, SAT library, floating-point reasoning, or randomized step.

Both cases are unsatisfiable. The first needs 22 search calls (12 failed leaves, maximum depth 3); the second needs 24 calls (13 failed leaves, maximum depth 5). The saved statistics are in COMMAND_LOG.json. This is an independently rerunnable finite exhaustive proof, not merely an optimization solver's infeasibility claim.

## Positive witnesses and verification

Positive witnesses specify every subset of size at most h by its binary bitmask. Bit i represents ground-set element i+1. Subsets larger than h may be colored arbitrarily, for example color 0, and do not affect verification.

- milp_n5_h3.json and milp_n6_h3.json certify the nontrivial h=3 upper bounds.
- milp_n7_h4.json, milp_n8_h4.json and milp_n9_h4.json certify h=4 for n=7,8,9.
- local_n10_h4.json and local_n11_h4.json certify h=4 for n=10,11.

Run:

    python verify_witnesses.py
    python certify_n7_h3.py

The verifier uses only the Python standard library. It checks the domains, confirms that exactly all subsets of size at most h are present, and explicitly enumerates every h-set Y and every subset A of Y, checking that their color set is {0,...,n-1}. replay output in COMMAND_LOG.json records witness file sizes, SHA-256 hashes and the number of checked h-sets.

