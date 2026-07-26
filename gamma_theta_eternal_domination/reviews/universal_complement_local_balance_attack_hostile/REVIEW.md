# Hostile review: universal complement/local-balance attack

## Verdict

**ACCEPT.**

I found no false statement labeled `PROVED`, no one-guard model error, no
reversal between \(G\) and \(\overline G\), and no circular claim of a
resolution.  The note is a valid proof-lane result with the scope it states:
it proves several structural lemmas and identifies an exact list-coloring
endpoint, but it does not prove or disprove the gamma--theta conjecture and
does not raise the finite counterexample frontier.

This verdict is bound to:

| artifact | SHA-256 |
|---|---|
| working note | `ed88c3ace73acc061bab41e8d7ab9a7a74ede1d739ef9c3aae9ed05b38aa0772` |
| evidence log | `7fbbb0cd2cf91086461d0a10f0779e143a07b06bd749e1534ed48a9fa94d875b` |
| diagnostic probe | `327424e37242aafd7da0cf0e06774fcb0ecf25d5fa7669d7837cbb8f478209df` |

Any later change to those files requires rebinding this verdict.

## Proof audit

The accepted inputs were used with their exact hypotheses:

- C-051 is applied only to nonempty cliques of \(H\), equivalently
  independent sets of \(G\), inside a minimum counterexample.
- C-048 is used only to rule out a simplicial vertex of the minimum
  counterexample.
- The maximum-independent-state forcing lemma is applied only when the
  independent state has the same cardinality as the eternal family.
- The greatest-family assertion uses the accepted greatest fixed point:
  every eternal \(k\)-family, including a clique-partition product family,
  is contained in \(\mathcal K_\ast\).

The individual arguments survive hostile audit.

1. **Lemma 1.** A \((k-1)\)-set fails to dominate \(G\), so an undominated
   vertex is a common open \(H\)-neighbor. Extension proves the statement
   for smaller sets. Together with \(\omega(H)=k\), this makes every
   maximal \(H\)-clique a \(k\)-clique.
2. **Complement dictionary.** For a clique \(A\) of \(H\),
   \(G-N_G[A]\) has vertex set \(N_H(A)\), and its complement is exactly
   \(H[N_H(A)]\). Thus C-051 gives both
   \(\chi=\omega=k-|A|\) in the asserted direction. Also
   \(V(H)-N_H(v)=N_G[v]\), so the nonsimplicial translation is correct.
3. **Lemma 2.** In two facets sharing a ridge, only the departing vertex is
   adjacent in \(G\) to the entering vertex. The attack is unoccupied, one
   guard moves along one edge, and the unique successor is the other
   forced maximum-independent state.
4. **Proposition 3.** The Graph6 and edge data for `FCpbO` agree. The
   stated three clique parts give a product eternal three-family. The
   complement has exactly the six listed triangles, no \(K_4\), thirteen
   edges, and connected flag complex with
   \[
   \dim H_1=13-7+1-6=1.
   \]
   Hence the equality example and its nonsimple-connectivity conclusion
   are both proved.
5. **Lemma 4.** Two nonadjacent vertices in one closed private block would
   extend \(S-\{u\}\) to an independent \((k+1)\)-set. The blocks are
   therefore disjoint cliques.
6. **Lemma 5.** The Hall restoration argument has the correct online
   quantifiers. Attacking an independent outside set moves distinct guards
   from \(S\). Starting afresh from the resulting family state and
   reattacking all but one missing \(S\)-vertex forces outside guards back.
   The last outside guard must answer the final missing vertex, proving the
   required original response-list membership. This works separately for
   every omitted guard and yields Hall's inequality for every subset.
7. **Theorem 6.** A response color certifies adjacency to its entire
   private clique, while a proper color class in \(H[X]\) is a clique in
   \(G[X]\). The resulting \(k\) sets are a genuine clique partition.
8. **Proposition 7.** The forward implication is Theorem 6. Conversely, a
   \(k\)-clique partition meets \(S\) once per part; replacing the guard in
   a part by any other vertex of that part is a state of the product
   strategy, hence of \(\mathcal K_\ast\). This proves the claimed
   response-list equivalence.
9. **Lemma 8.** Both attacks are unoccupied and each response moves exactly
   one adjacent guard. In the second branch, membership of
   \(S-\{v\}+\{x\}\) in the family makes it dominating; since no vertex of
   \(S-\{v\}\) is adjacent to \(v\), domination forces \(xv\in E(G)\).
   Thus the claimed alternative response color really is in the list.
10. **Corollaries 9 and 10.** The singleton consequence follows directly
    from Lemma 8. The minimal uncolorable induced list instance is
    connected, has \(d_Y(x)\ge |L(x)|\), cannot have one or two vertices,
    and has the stated leaf behavior. Its clique-wise Hall condition is
    exactly Lemma 5 because a clique of \(H[X]\) is independent in \(G\).

## Refuted mechanisms and scope

The two labeled-loop examples are correct. On \(C_7\), all seven displayed
transitions are legal one-edge moves between maximum independent triples
and return with a nontrivial label permutation, while
\((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4)\). On \(C_4\), all
six two-subsets dominate and form an eternal family, and the displayed loop
exchanges the physical guard labels despite full equality.

The transport discussion now correctly says that path independence only
addresses one ridge-connected facet component and that a global coloring
would additionally require compatibility across components and
lower-dimensional overlaps.

Proposition 7 is an equivalence with the desired conclusion, but the note
uses it only to identify the remaining obstruction. It explicitly stops
rather than treating “prove the list instance colorable” as an independent
resolution. There is therefore no circular proof or overclaim.

## Independent finite evidence

The clean-room `audit.py` imports none of the campaign graph or transition
code. It independently verified the two loops, all data for `FCpbO`, its
five parameters, and its mod-two homology. It also streamed all 1,099
labelled graphs through order five and checked:

- 375 equality graphs;
- 1,373 maximum independent reference states;
- 6,605 independent-outside-set Hall obligations;
- 312 collision-transfer obligations; and
- the greatest-family response-list equivalence at every reference state.

All checks passed. These finite checks are falsification evidence, not
proofs of the universal statements; the proofs above carry the claims.

During review, four precision defects were corrected before this acceptance:
the collision proof made its forced \(xv\)-edge explicit, facet transport
was restricted to the compatibility it actually supplies, the response
list wording stopped suggesting a false converse about family membership,
and the evidence log was rebound to the final note and probe hashes.
