# Turn 5: nine-label closure and a barrier to a global palette reduction

The fifth and final substantive author turn leaves the original all-n, all-d, arbitrary-list floor conjecture unresolved. No further author search is undertaken after this freeze.

## 1. Extended all-length theorem

**Computer-assisted theorem.** Every path P_n, of any length n>=1, admits a (2,2)-labeling from arbitrary six-element integer lists whose union has at most nine distinct labels.

The rank-expansion argument from turn 3 reduces this to the consecutive palette {1,...,9}. There are 84 possible six-element lists. The exact reachable-pair closure has

- 7,056 initial relations, one for each ordered pair of input lists
- 4,087,257 relations in the completed closed set
- 343,329,588 input transitions, exactly 84 per closed state
- No empty relation

The C++ breadth-first run completes its queue; its maximum shortest prefix length among these states is 43. This number is a property of the finite state graph, not a bound on the path lengths covered. Closure under every possible next list proves all lengths by the induction in turn 3.

The authoritative portable replay `verify_turn5.py` computes the complete closure in Python using exact arbitrary-precision integers and the standard library. It has no state cap or sampling. To avoid recomputing the same small Boolean tests, it precomputes for each previous terminal label b and each possible row S of preceding labels the contribution

    Q_b(S)={(b,c): |b−c|>=2 and S contains some a with |a−c|>=2}.

The unrestricted successor is the union of these contributions over all rows b; restricting its rows c to the next input list gives the exact successor relation. This is algebraically the same recurrence as before, not an approximation. The sorted state set is serialized into 11 little-endian bytes per 81-bit relation and hashed. A separately written C++ packed-state implementation agrees with the complete state count, transition count and full state-set digest. Its exploratory cap is not reached in this completed run; the Python proof replay imposes no cap.

For n>=6, six is the original source's proposed value for d=2. The explicit five-list P6 obstruction from turn 3 extends to every longer path, so six is also necessary within the at-most-nine-label family. The unrestricted d=2 question is still not proved: any counterexample in that regime would have to use at least ten distinct labels.

## 2. Why a single global recoding cannot always reduce to nine labels

A possible shortcut would try to replace every label of an arbitrary instance by a label in a fixed nine-element palette, preserving six distinct options in every list, before applying the closure theorem. The following feasible instance rules out such a blanket argument.

On P10, let

    L_i={i,i+1,...,i+5} modulo 10, interpreted as labels 1,...,10,

for i=1,...,10. Each list has six elements. Every pair of distinct labels occurs together in at least one list: their shorter cyclic separation is at most five, so a cyclic interval of six labels contains both.

Let g be any single global map on these ten labels that preserves six distinct values in the image of every list. If g(a)=g(b) for distinct a,b, choose a list containing both. Its image then has at most five elements, a contradiction. Thus g is injective and cannot take values in a nine-element palette. This argument does not assume order preservation; it excludes every global recoding with that cardinality-preserving requirement.

The instance is nevertheless (2,2)-labelable. The JSON receipt supplies an explicit labeling checked against every list and all distance-one/two conditions. At n=10,d=2 the conjectured size is six, as used here. Hence this is a barrier to the proposed reduction, not a counterexample to the original conjecture. It does not rule out vertex-dependent transformations, a different proof technique, or a more sophisticated reduction that does not preserve six distinct images per list.

The exact gap compression of turn 1 still holds, but its label bound grows with n and k; it cannot supply a uniform nine-label bound.

## 3. A parameter-scaling warning

The same finite-state exploration at d=3 finds an impossible eight-list assignment on P13 using only nine labels. Its thirteen lists and exact reachable-pair layers are included in TURN_5_CHECKS.json and checked independently by a set-based recurrence. The source predicts nine, not eight, at these parameters:

    floor(9(1−1/13))+1=9.

This is another one-below-target obstruction consistent with the known lower bound. It prevents treating the d=2 six-list result as an unqualified result for other separations. No shortest-instance or optimal-palette claim is required or made.

## 4. Final gap and conclusion

The two bounded-palette closures prove genuinely unbounded path-length statements, but they do not bound the union in arbitrary list assignments. The sparse/common-label and variable-anchor theorems give all-size families with unrestricted palettes, but the 42-vertex certificate from turn 4 shows that the optimized deficit method is incomplete. The source's original floor conjecture for arbitrary natural-number lists is therefore still unresolved after five genuine turns.

The catalog's ceiling statement has a separate elementary transcription counterexample; it must not be promoted to a solution of the corrected source conjecture. The recommended final status after independent review is unsolved, 5/5, with the exact source normalization and all scoped partial results retained. No novelty or priority claim is made.

## Replay

    python verify_turn5.py > /tmp/pathlabel-turn5.json
    cmp TURN_5_CHECKS.json /tmp/pathlabel-turn5.json

This standard-library replay can use several hundred megabytes and take longer than the earlier checkers. The optional independent C++ cross-check requires a compiler supporting C++17 and unsigned 128-bit integers, such as GCC:

    g++ -O3 -std=c++17 crosscheck_turn5.cpp -o /tmp/pathlabel-cross5
    /tmp/pathlabel-cross5 9 6 2 8000000 /tmp/pathlabel-states9.bin
    sha256sum /tmp/pathlabel-states9.bin

Compare the CLOSED line to TURN_5_CPP_M9.txt and the binary state-set hash to the Python receipt. A CAPPED result would be inconclusive, not successful verification. The archived run completed at 4,087,257 states, below the stated cap. The generated binary contains mathematical state data and need not be published or retained.
