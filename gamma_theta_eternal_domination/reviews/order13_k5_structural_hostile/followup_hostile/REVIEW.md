# Hostile review: order-13, parameter-five follow-up

## Verdict

**ACCEPT_CONDITIONAL_STRUCTURAL_FOLLOWUP**

No mathematical flaw was found in Theorems 1, 4, 6, 8, or 10; Corollaries
2, 3, and 5; Proposition 7; Lemma 9; the finite counts; or the coverage
argument.

This acceptance is deliberately narrower than a campaign claim.  Every
result is conditional on the accepted lower-order frontier C-050 and the
accepted C-048/C-051 reductions.  The note neither executes the proposed
kernel-and-mask enumeration nor excludes the \((n,k)=(13,5)\) slice.

Reviewed target:

- `math/working/order13_k5_followup/RESULT.md`
- 18,805 bytes
- SHA-256
  `14d44f8b69acdec27783559794f6096c77c9c3f63cc2e219d59728eaf1e4a88b`

The target was not edited during this review.

## 1. Projection hierarchy

Theorem 1 has exactly the hypotheses needed by C-051.  A nonempty
independent set \(S\) with \(1\leq |S|\leq4<5\) gives
\(P_S=G-N[S]\), which is nonempty, well-covered, and has
\[
\gamma(P_S)=\alpha(P_S)=\gamma^\infty(P_S)=5-|S|.
\]
Because C-050 makes a hypothetical order-13 counterexample minimum-order,
the minimum-counterexample corollary of C-051 gives
\(\theta(P_S)=5-|S|\).  This use is not circular: \(P_S\) is a proper graph
of smaller order, and no order-13 conclusion is assumed.

For Corollary 2, \(\{v\}\cup T\) is independent whenever \(T\) is
independent in \(Q=G-N[v]\), and its size is at most four.  Direct deletion
gives
\[
G-N[\{v\}\cup T]=Q-N_Q[T].
\]

For Corollary 3, the identities
\[
G-N[a]=G[\{b\}\cup(Q-A)],\qquad
G-N[b]=G[\{a\}\cup(Q-B)]
\]
are exact.  Every \(T\) in the displayed residual is anticomplete to the
corresponding anchor, so the applications to
\(\{a\}\cup T\), \(\{b\}\cup T\), and
\(\{a,b\}\cup T\) satisfy the independence and \(t<5\) hypotheses.  The
mask-dependent formula (2.5) correctly retains \(b\) exactly when
\(q\notin B\).

## 2. Clique insertion

Theorem 4 is an exact equivalence.

If a four-clique part of \(Q\) lies in \(A\), it can absorb \(a\), and
\(\{v,b\}\) is the fifth clique; the \(B\) case is symmetric.

Conversely, in any clique partition of \(G\) with at most five parts, the
part containing \(v\) is exactly one of
\(\{v\},\{v,a\},\{v,b\}\).  Restricting the other parts to \(Q\) must
produce exactly four nonempty clique parts because \(\theta(Q)=4\).  In the
\(\{v,a\}\) case the part containing \(b\) must therefore have a nonempty
\(Q\)-intersection contained in \(B\), and symmetrically.  In the singleton
\(\{v\}\) case both \(a\) and \(b\) occupy different parts with nonempty
\(Q\)-intersections, giving both insertions.  Since six cliques always
suffice, failure of every insertion is equivalent to \(\theta(G)=6\).

The hostile replay checked the equivalence independently on all relevant
four-vertex kernels and a deterministic suite over all 65 labeled
five-vertex kernels with clique-cover number four: 16,896 attachment cases.

## 3. The 707 domination characterization

Every dominating set meets \(\{a,b,v\}\), because \(v\) has no neighbor in
\(Q\).  Writing a set uniquely as \(C\cup X\), the three displayed
conditions are respectively domination of \(Q\), \(a\), and \(b\);
\(C\ne\varnothing\) is exactly domination of \(v\).  Thus the
characterization is iff, not merely a filter.

The count by \(|C|=1,2,3\) is
\[
528+168+11=707.
\]
The hostile checker compared all 707 formulas with direct domination on
eight synthetic ten-vertex attachment graphs.

The assumptions \(\alpha(Q)=4\) and \(\alpha(R)=3\) correctly give
\(\alpha(G)=5\) by splitting an independent set according to its
intersection with \(\{a,b,v\}\).  A maximum independent set
\(\{v\}\cup I\) dominates \(G\), so \(\gamma(G)\leq5\); hence absence of a
dominating set among the 707 cases is exactly \(\gamma(G)=5\).

## 4. Degree and nonsimplicial translation

From \(\alpha(Q-N_Q[q])=3\), the residual has at least three vertices, so
\(d_Q(q)\leq6\).  Equation (4.7) is the exact degree formula for a kernel
vertex.

The four nonsimplicial cases are exact:

- for \(q\in R\), \(N_G[q]=N_Q[q]\);
- for \(q\in A-B\), \(N_G[q]=N_Q[q]\cup\{a\}\), which is a clique iff
  \(Q[N_Q[q]]\) is a clique and \(N_Q[q]\subseteq A\);
- the \(B-A\) case is symmetric; and
- for \(q\in A\cap B\), the nonadjacent neighbors \(a,b\) prevent
  simpliciality.

The replay exhausted all 65,536 combinations of a labeled four-vertex
kernel, two masks, and a kernel vertex.  Given Corollary 5's nonempty masks,
\(a,b,v\) are automatically nonsimplicial, so no terminal-vertex condition
is missing.  Since \(|R|\geq3\), at least three vertices are nonsimplicial
in \(Q\), excluding cluster-graph kernels.

The final target now states explicitly that \(v,a,b\) are automatically
nonsimplicial.  Its added sentence uses Corollary 5's
\(|A|,|B|\geq1\): \(a\)'s closed neighborhood contains the nonadjacent
vertices \(v\) and any member of \(A\), and symmetrically for \(b\), while
\(v\)'s two neighbors \(a,b\) are nonadjacent.  The hostile checker reverses
this sentence in memory and recovers the former 18,551-byte target at its
exact former hash, proving this was the only final-byte change.

## 5. Forced states and the one-guard model

Theorem 8 uses only independent five-states, which the accepted forcing
lemma places in every eternal five-family.

For \(D=\{v\}\cup I\), an unoccupied attack at \(a\) has exactly the
responders \(v\) and \(I\cap A\):

- \(v\to a\) leaves \(\{a\}\cup I\), which dominates \(b\) iff
  \(I\cap B\ne\varnothing\);
- \(x\to a\), for \(x\in I\cap A\), leaves
  \(\{v,a\}\cup(I-\{x\})\), whose domination of \(Q\) is exactly
  \(A\cup N_Q[I-\{x\}]=Q\).

The \(b\)-attack is symmetric.  For
\(\{a,b\}\cup J\), an unoccupied attack at \(v\) can be answered only by
\(a\) or \(b\), producing exactly the two equalities in (5.3).  These are
necessary first-response tests only, exactly as labeled.

The hostile replay compared the formulas with direct one-edge successor
domination on 216 maximum-\(Q\) state/attack pairs and four maximum-\(R\)
states.  Every attack was unoccupied, and each tested response moved one
adjacent guard only.

## 6. Five-vertex residual and six-mask theorem

Lemma 9's classification is correct.  A five-vertex graph with
\(\theta=4\) has an edge.  Any two distinct edges, whether incident or
disjoint, give an explicit dominating three-set, contradicting
\(\gamma=4\).  Hence exactly one edge exists.  Conversely every labeled
one-edge graph has \((\gamma,\alpha,\theta)=(4,4,4)\).  Independent
exhaustion of all \(2^{10}=1,024\) labeled five-vertex graphs found exactly
the ten labeled one-edge graphs.

For \(|A|=6\), \(S_a\) has vertices \(\{b\}\cup(Q-A)\).  Its edges are
exactly \(Q[Q-A]\) plus the \(b\)-edges to \(B-A\).  The one-edge
classification therefore gives exactly the two alternatives in Lemma 9.

For two six-masks, \(|R|\geq3\) gives
\[
|A\cap B|=|R|+2.
\]
Thus either \(A=B\), with \(|R|=4\), or each set difference is a singleton
and \(|R|=3\).  In the unequal case write
\(B-A=\{x\}\), \(A-B=\{y\}\).  Lemma 9 makes both
\(R\cup\{x\}\) and \(R\cup\{y\}\) independent.  Therefore
\(D=\{v\}\cup R\cup\{x\}\) is an independent five-state forced into every
eternal family.

The attack at the unoccupied vertex \(b\) has exactly two occupied
neighbors:

- \(v\to b\) leaves \(a\) undominated because
  \((R\cup\{x\})\cap A=\varnothing\);
- \(x\to b\) leaves \(y\) undominated because \(y\notin B\) and
  \(R\cup\{y\}\) is independent.

This is a valid one-guard contradiction.  The replay checked all 5,040
ordered unequal six-mask pairs with direct responder and successor
simulation.  It also recovered 210 equal pairs, which remain live.

## 7. Counts and coverage

There are
\[
\sum_{j=1}^{6}\binom{10}{j}=847
\]
individual nonempty masks.  Direct enumeration gives 465,157 ordered pairs
with \(|A\cup B|\leq7\); 847 are fixed by swapping.  Burnside's lemma
therefore gives
\[
\frac{465157+847}{2}=233002
\]
unordered raw pairs.  The follow-up author's audit and the hostile replay
agree on every count.

The coverage proof is valid as a design:

1. a hypothetical counterexample has a degree-two root \(v\);
2. deleting \(N[v]\) reconstructs a unique rooted triple
   \((Q,\{A,B\})\);
3. fixing one independent four-set in \(Q\) is safe by relabeling, not an
   assertion of orbit uniqueness;
4. completed-graph canonicalization retains an unlabeled representative;
5. the diagonal \(\operatorname{Aut}(Q)\) action and the swap
   \(a\leftrightarrow b\) cover every rooted mask orbit; and
6. final Graph6 canonicalization removes duplicates caused by another
   eligible root.

Every proposed filter is necessary for a counterexample, and final exact
evaluators cannot remove one incorrectly.  Any future implementation of
partial canonical pruning still needs its own soundness audit.  The note
correctly requires a complete orbit manifest, coverage audit, and proof
artifacts before a finite exclusion can be claimed.

## 8. Claim boundary, circularity, and reproducibility

No all-guards transition is used.  Attacks in Theorems 8 and 10 are at
unoccupied vertices; exactly one occupied adjacent guard moves to the
attack; failure of every resulting state to dominate is sufficient to
contradict family closure.

No theorem assumes \(\theta(G)=5\), the target conclusion, or the existence
of a lifted eternal family.  Clique-cover equality for projected graphs
comes only from the accepted smaller-order frontier.  The coverage proof
does not claim that the proposed enumeration has been run.

The author's existing replay matches its checked-in evidence byte-for-byte:

```sh
cmp \
  <(python3 -B -W error math/working/order13_k5_followup/audit.py) \
  math/working/order13_k5_followup/evidence.json
```

The independent hostile replay is:

```sh
python3 -B -W error \
  reviews/order13_k5_structural_hostile/followup_hostile/audit.py
```

Expected verdict:

```text
ACCEPT_CONDITIONAL_STRUCTURAL_FOLLOWUP
```

The hostile replay is a finite audit of the proofs' local identities and
counts.  It is not a broad ten-vertex enumeration, an eternal-family search,
or a slice certificate.
