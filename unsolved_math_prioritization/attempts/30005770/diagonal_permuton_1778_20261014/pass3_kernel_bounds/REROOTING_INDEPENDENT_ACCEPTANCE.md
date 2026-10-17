# Independent acceptance of the one-point rerooting bound

Reviewed 14 October 2026 during shared PASS3. This is a complementary mathematical review of a document authored in the concentration-audit lane; it is not a human peer-review claim.

## Reviewed artifact

`pass3_concentration_audit/REROOTING_ONE_POINT_BOUND.md`

- SHA-256: 41336ca4027b4c0c40928e3df4df0e70ec107043d78f64f799d404017c8870b5
- Bytes: 10256

**Disposition: accepted in its stated partial scope. No correction requested.**

## Checks

1. The first-entry increasing inflation stays in Av(213). Its reflected operation is adjacent increasing inflation of the lower maximum. An old incoming edge lifts injectively, with the existing upper greedy witness intact. A new two-color 1324 cannot select both globally adjacent lower twins.

2. The direct bridge uses the Av(132) maximum split L,max,R with all L values greater than every R value. Placing the first block in a selected upper ascent gap and the second after all uppers prevents any alternating increasing pair of each color. Thus the bridge is genuinely greedy, not merely an unrestricted shuffle.

3. The rotated chain has size n+1. When the marked cell was terminal, it is inflated and has size a+1; otherwise the first cell retains size a. This is handled by the first-cell threshold at least a. The removed incoming edge is correctly stored rather than discarded. All surviving old edge multiplicities are retained by the exact path encoding.

4. An output and proposed bridge index determine the original state order, marked index, deflation location, and every retained edge. The only remaining data are the cut binary shuffle. Its count is at most binom(a+b,b), with no need to assume K symmetric. For the absolute predecessor cap, a+b<=n and b<=p_0<=n/2 justify both binomial comparisons. The same fibre bound counts marked objects, so it bounds the unmarked existence event as well.

5. The finite-class normalization is explicit. Deleting the minimum proves a_(n+1)<= (n+1)a_n without a ratio asymptotic. The first-cell threshold divided by n+1 tends to epsilon; applying each fixed theta<epsilon and then increasing theta to epsilon gives the asserted exponent. The polynomial factors vanish on the logarithmic scale.

6. For the relative bound, the absolute frontier estimate B_N(a)<=C_eta lambda^N exp(-eta a) is uniform in both parameters. This supplies the uniformity needed to sum all at most n^2 pairs (a,b). The binomial entropy is a*f(b/a), and f is increasing. If f(c)<eta<gamma, every summand is bounded by the same exponential in the minimum allowed a. Dividing by a_n leaves lambda^n/a_n=exp(o(n)); it is not treated as bounded. Finally eta may increase to gamma after taking limsup.

7. The conclusion controls arbitrary-index large upward jumps, not all macroscopic cells. The graded-profile obstruction and the distinction between a sufficient largest-cell condition and a necessary condition are both stated correctly. There is no claimed proof of the anti-diagonal or universal limit.

The geometry reviewer independently checked the local maps. The present acceptance also checks the global reconstruction and probability normalization. Finite diagnostics are supplementary and cannot replace these all-size arguments.
