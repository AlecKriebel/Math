# Turn 3: all-length six-list theorem for palettes of at most eight labels

This is a computer-assisted restricted-family result. It does not settle the original unrestricted-palette floor conjecture.

## 1. The theorem

**Theorem.** For every n>=1, every assignment of six-element integer lists to the vertices of P_n whose union contains at most eight distinct labels admits a (2,2)-labeling.

For n>=6, the source's conjectured cardinality is floor(6(1−1/n))+1=6. Thus this proves the conjectured upper bound for all path lengths in that range, subject to the explicit palette-union restriction. Moreover five lists do not always suffice already on P6, even over a seven-label palette; the explicit obstruction below extends to every longer path.

The all-length step is a finite-state closure proof, not an enumeration of paths up to a maximum length. The remaining restriction is the number of distinct labels in the union, not the size of n.

## 2. Reduction to the consecutive eight-label palette

Let the distinct actual integer labels be a_1<...<a_M with M<=8. Replace each a_j by its rank j. For i<j,

    a_j−a_i >= j−i.

Consequently a valid rank labeling with separations at least 2 expands to a valid original labeling. A six-element list retains six distinct ranks, and all rank lists are subsets of {1,...,8}. This direction suffices: rank compression can destroy a previously feasible labeling, so no converse is claimed. The exact two-way gap compression from turn 1 is a different statement.

It therefore suffices to consider all six-element subsets of a fixed consecutive palette of size eight.

## 3. Finite-state closure

Use the exact reachable-pair semantics proved in turn 1. A state is a relation R on the ordered palette: (a,b) belongs to R if these can be the last two labels of a valid prefix. There are at most 2^64 relations for eight labels; this crude finiteness bound suffices for the construction.

For every ordered pair of six-element lists A,B, initialize

    R(A,B)={(a,b): a in A, b in B, |a−b|>=2}.

For a state R and any next six-element list C, the successor is

    T_C(R)={(b,c): c in C, |b−c|>=2,
               and some a has (a,b) in R and |a−c|>=2}.

The complete next-list alphabet has binomial(8,6)=28 members. Start with every initial state and repeatedly add every successor for all 28 lists until no new state appears. `verify_turn3.py` performs this closure with exact integer bitsets. It uses no randomness, state cap, heuristic, floating-point arithmetic or external solver. Each relation is stored as eight rows, row b containing the possible preceding a labels. The successor first computes all possible next rows c, then masks to the chosen C. That optimization is exactly the displayed transition.

The exhaustive run produces:

- 784 initial states
- 227,952 states in the completed closed set
- 6,382,656 checked transitions, exactly 28 per closed state
- No empty state

The script processes every state it adds and asserts that every successor is nonempty. It also computes a SHA-256 digest of the entire sorted state set, using the byte format specified in its JSON receipt. Separate smaller-palette runs and an independently written C++ implementation agree with the recorded closure cardinalities and transition counts. The portable authoritative replay is the standard-library Python script.

**Why this proves every length.** Every two-vertex prefix has one of the initialized states. If a prefix state is in the closed set, the next list is one of the 28 possible inputs and its exact successor is in the closed set. By induction every prefix of any length has a state in this set. Since none is empty, every such prefix admits a labeling. The one-vertex case is immediate. This is a finite computer-assisted proof for a fixed palette, with an unbounded path length.

## 4. Sharp five-list obstruction in the restricted family

For P6, d=2, take these five-element lists in path order:

    L1 = {1,2,5,6,7}
    L2 = {2,3,4,5,6}
    L3 = {1,2,3,5,6}
    L4 = {2,3,4,5,6}
    L5 = {1,2,3,5,6}
    L6 = {2,3,4,5,6}.

The exact reachable-pair recurrence reaches the empty relation at the sixth vertex. All intermediate relations are included in TURN_3_CHECKS.json and recomputed from the lists. This is a verifiable explicit obstruction, not a counterexample to the original conjecture: it is one below the proposed list size six. The original source already states a matching general lower bound, so this certificate is consistent with credited prior knowledge and carries no novelty claim.

For a longer path retain these first six lists and give later vertices, for example, L6. Every full labeling would restrict to an impossible first six-vertex labeling. Therefore within the family of palettes of size at most eight, six is necessary and sufficient for every n>=6.

## 5. A failed stronger invariant and limits

A possible hand-proof strategy would maintain at least four terminal labels b for which the set of possible preceding labels has diameter at least 3. Such a row cannot be killed by any single forbidden interval of length three. The complete state run disproves this proposed invariant: it reaches a nonempty state with only one such row. The JSON receipt includes an explicit input sequence reaching it and recomputes the row count with a separate set-based recurrence. This does not contradict six-list feasibility, but prevents relying on that stronger invariant without modification.

A separate exploratory nine-label computation was capped before closure, so it gives no all-length nine-label theorem. No restriction on an arbitrary instance's union to eight labels has been proved. The finite-alphabet bound from turn 1 grows with n and k; it cannot remove this gap. After three genuine turns, the unrestricted original remains unresolved.

## Replay

    python verify_turn3.py > /tmp/pathlabel-turn3.json
    cmp TURN_3_CHECKS.json /tmp/pathlabel-turn3.json

Only Python 3 standard library is required. The calculation can take several seconds depending on hardware. The listed closure size is a completed finite proof obligation for the restricted palette theorem, whereas the original unrestricted conjecture remains a separate question.
