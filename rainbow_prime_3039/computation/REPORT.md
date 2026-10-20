# Exact bounded computations and an interval-transfer obstruction

## Outcome and limits

No balanced rainbow-free coloring exists for primes 5, 7, 11, 13, 17, 19, 23, 29, according to exhaustive C++ search. Independent pure-Python enumeration confirms 5, 7, 11, 13, 17. Prime 31 reached its 20-second bound and is **unknown**, not UNSAT. These are reproducible computational outcomes, not machine-checkable SAT refutation certificates; no asymptotic conclusion follows. The exact search intentionally stops at this modest range.

`results.jsonl` records the balanced runs. `search.cpp` is self-contained C++17. Compile with `g++ -O3 -std=c++17 search.cpp -o search`, then run `./search p seconds`. Optional third argument changes the problem to all four sizes at least that argument, with implied upper bound p minus three times the lower bound; those exploratory results are separate in `relaxed_results.jsonl` and must not be represented as balanced witnesses. Every timeout remains UNKNOWN.

## Search correctness

Every ordered modular progression a,a+d,a+2d,a+3d for d nonzero is included. Sorting and deduplicating its four vertices preserves the forbidden-rainbow condition. For primes at least 5 all vertices are distinct. A coloring is balanced exactly when every class size lies between floor(p/4) and ceil(p/4).

The only spatial symmetry reduction is fixing colors at 0 and 1 to distinct named colors 0 and 1. Any balanced coloring has distinct-colored points u and v. The affine change x -> u+(v-u)x is invertible over the prime field, preserves all APs, and moves these points to domain coordinates 0 and 1. Permuting color names establishes the normalization. No class-size ordering or additional affine assumption is imposed.

Domains are four-bit masks. If three points of an edge have fixed distinct colors, the fourth cannot have the missing color. Class-size propagation removes a color after its upper bound is filled, or forces all remaining possible positions when their number equals its lower bound. All such inferences are necessary. Branching tries every remaining color of a chosen vertex. A fully fixed feasible leaf is a witness. Exhaustion without timeout proves absence subject to implementation correctness.

The independent Python check enumerates colorings in restricted-growth order (first color 0; each new color is the next integer), which removes only color permutation symmetry. It uses neither affine normalization nor domain propagation. It checks each edge when its last coordinate is assigned. Its separate witness validator directly checks every ordered (a,d).

## Exact obstruction to transferring the interval examples

Source for the four explicit words: Jana–Das, *A Note On Rainbow 4-Term Arithmetic Progression*, arXiv:2502.01086v1, Section 2, https://arxiv.org/html/2502.01086v1 . This use does not endorse the paper's other arguments or terminology.

Let U=ABCC and V=DDAB. For m>=1 the source's words of odd lengths are U^m V^m D (8m+1); U^m V^m DBA (8m+3); CC U^m V^m DBA (8m+5); and U^(m+1) V^m DBA (8m+7). Coordinates below are 1,...,n, with n representing zero modulo n.

**Proposition.** Each of these four balanced words has a modular rainbow 4-AP for every m>=1, regardless of primality.

**Proof.** For n=8m+1, use (n,1,2,3), with step 1 and colors D,A,B,C. For n=8m+3 use (n-2,n,2,4), with step 2 and colors D,A,B,C. For n=8m+5 use (n-2,n-1,n,1), with step 1 and colors D,B,A,C. For n=8m+7 use (n-2,n,2,4), with step 2 and colors D,A,B,C. Each asserted color follows directly from the initial or final block. Consecutive differences equal the stated nonzero step modulo n. All four points are distinct since n>=9. This proves the proposition.

Thus these interval constructions fail to transfer to **every** odd prime covered by their formulas, not merely to selected numerical examples. The obstruction occurs right across the seam with step at most 2. An affine image or color permutation cannot remove it. This is an obstruction to this specific construction, not a theorem that all balanced prime colorings have rainbow APs.

`interval_transfer.py` checks the formulas and balance for 1<=m<=100 (400 tests). The proof above, not the finite tests, establishes all m.
