# Rejected diagnostic: three-vertex extensions of the fixed mixed cap

Date: 2026-07-26 (PDT)

## Status

**REJECTED-DIAGNOSTIC.** No order-13 exclusion, fixed-template exclusion,
or central campaign claim is accepted from this calculation.

## Independently reproduced fixed-cap facts

Start with `HDzruf]` on

\[
(a,b,c,x_0,x_1,x_2,x_3,w,y)=(0,1,2,3,4,5,6,7,8)
\]

and add \(z=9\), nonadjacent in \(G\) to \(x_0,x_3,y\) and adjacent to
\(a,b,c,x_1,x_2,w\).  The resulting ten-vertex graph has graph6 string

```text
IDzruf]zO
```

Delete the six direct-swap triples

\[
023,\ 013,\ 024,\ 125,\ 126,\ 016
\]

from the dominating triples and apply the literal one-guard greatest-fixed-
point deletion algorithm.  An independent implementation obtains deletion
round sizes

\[
100\longrightarrow82\longrightarrow75.
\]

The fixed graph has exactly the following nine dominating pairs:

\[
04,\ 06,\ 13,\ 15,\ 34,\ 39,\ 56,\ 69,\ 89.
\]

These are useful replay facts about this one ten-vertex graph only.

## The predicate discrepancy

The proposed extension diagnostic represented each of three new vertices
by its set of nonneighbors among the ten fixed vertices.  Such a type must
contain no independent base triple if the final graph is to have
\(\alpha\leq3\).  It must also contain no family state that is known to be
present, because that state would fail to dominate the new vertex.

There are two materially different state predicates:

1. Requiring domination by **all 75 states of the greatest safe family**
   leaves 130 types.  This is too strong for the intended arbitrary
   specified-family argument: a family realizing the mixed pattern need
   not contain every state in the greatest family of the fixed cap.
2. Requiring only the states explicitly forced by the proved mixed-path,
   \(W/Y\), and end-ridge arguments leaves 354 types.  The explicit set
   used in this replay consists of \(S\), the six positive direct swaps,
   the two Hall-tight end states, the two \(W\)-swap states, \(T_w\), the
   \(Y\) co-state, the three end-ridge states, the forced \(c\)-swap at
   \(z\), and \(\{x_0,x_3,z\}\).

The provisional count of 239 admissible types lies between these two
counts, but no mathematically specified admissibility predicate producing
239 was recoverable.  Consequently the associated provisional counts
of 192 unordered three-type covers and 1,536 graphs are unreproducible
and superseded.  Continuing to test those graphs would not establish a
well-defined mathematical universe.

## Conclusion

Only the ten-vertex fixed-cap replay above is retained.  The extension
enumeration is rejected at its coverage-definition gate.  In particular,
there is no accepted statement about all extensions of this cap, no
accepted order-13 result, and no evidence from this rejected diagnostic
that can be used as an exclusion theorem.
