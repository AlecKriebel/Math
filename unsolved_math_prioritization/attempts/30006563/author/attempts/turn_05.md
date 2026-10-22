# Attempt 5 of 5: improve the seed and test an actual amplification rule

## Aim

The K_7 seed gives the fixed deficit 5. This last attempt searches for a larger deficit and tests whether the apparent two-vertices-per-new-color progression can be justified recursively, rather than extrapolated from small examples.

## An explicit three-color K_9

Let A and B be disjoint sets of three vertices, and let z,x,y be three further vertices. Use the actual colors 0,1,2, with the following rules:

| Edge location | Color |
|---|---:|
| Inside A | 1 |
| Inside B | 0 |
| A--B | 0 |
| A--z and B--z | 1 |
| A--x | 0 |
| B--x | 2 |
| A--y | 1 |
| B--y | 2 |
| zx | 1 |
| zy | 0 |
| xy | 2 |

The rules specify every edge of K_9. Deleting x,y gives the K_7 seed from Attempt 4.

Here is a complete triangle-type classification. In the first column, digits record the three edge colors with multiplicities, in increasing order.

| Type | Number of triangles | Intersection certificate |
|---|---:|---|
| 000 | 10 | Every triangle has at least two vertices of B |
| 001 | 12 | Every triangle has at least two vertices of A |
| 002 | 9 | Every triangle contains x |
| 011 | 18 | Every triangle contains z |
| 012 | 16 | Every triangle contains y |
| 022 | 6 | Every triangle has at least two vertices of B |
| 111 | 7 | Every triangle has at least two vertices of A |
| 112 | 3 | Every triangle contains both z and x |
| 122 | 0 | Absent |
| 222 | 3 | Every triangle contains both x and y |

This can be verified directly from the block rules by considering zero, one, two or three vertices in {z,x,y}. The counts sum to binom(9,3)=84. Each nonempty type family is intersecting: two two-subsets of the same three-element A or B intersect, and fixed-center types obviously intersect. Thus the coloring has no vertex-disjoint color-isomorphic triangles.

The fresh-private-star extension from Attempt 1 now proves

    g(n) <= n-6  for every n>=9.

Together with the certified two-color obstruction on eight vertices, this gives g(8)=g(9)=3. The K_9 upper bound and its all-n extension have the explicit hand proof above; the exact lower bounds for g(8),g(9) rely on the K_8 certificate.

## What the bounded search actually established

The script checks all 3^7 possible neighbor-color patterns for a new vertex of the specified K_7. There are 58 valid patterns. It reduces the first new vertex under the evident permutations of A and B, leaving 26 canonical first patterns. It finds the displayed K_9 after 27 candidate combinations; the resulting complete coloring is directly checked against all 840 unordered disjoint triangle pairs. These counts are reproducibility facts, not evidence for a general asymptotic claim.

## A concrete failed recursion, rather than an unsupported extrapolation

The data (n,q)=(5,1),(7,2),(9,3) tempt the conjecture that one can keep adding two vertices for one new color. Test the literal next-step rule: preserve the displayed K_9, add u,v with colors 0 and 1 respectively to A, color 3 from each of u,v to B, and color uv by 3. Allow all four colors independently on their edges to z,x,y.

There are only 4^3=64 possible rows for each new vertex. Exact checking leaves eight individually valid rows for u and three for v. All 24 pairs fail the disjoint-triangle condition. The included script test_pair_amplification.py tests precisely this finite ansatz, with no heuristic cutoff or numerical relaxation; it finishes in well under one second.

This negative result does not rule out other four-color K_11 constructions. It only rejects this proposed recursive rule. The broad uniform-blow-up obstruction from Attempt 3 is another reason a recursion cannot be assumed.

## Final mathematical verdict after five attempts

The full problem remains unresolved in this packet. The best unconditional all-n upper bound proved here is n-6 for n>=9; the strongest source-announced lower bound remains c*n^(1/2+epsilon) for unspecified positive constants. Neither g(n)=Theta(n) nor g(n)=n-O(1) has been proved or refuted. No priority claim is made for these elementary constructions or restricted-class results.

Substantive budget: 5/5. The attempts comprise proper-core deletion, intersecting-family concentration, homogeneous-cut/product analysis, two-color finite seed certification, and the K_9 construction plus failed amplification. Retrieval, source verification, exact-check packaging, and subsequent independent review are not extra proof-attempt turns.
