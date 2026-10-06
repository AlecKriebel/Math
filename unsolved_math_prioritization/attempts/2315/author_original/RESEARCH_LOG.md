# Five approach log

This is an authored mathematical outcome log, not private working notes. All five approaches occurred on 2026-10-06 UTC. Source triage and the inherited-work gate are prerequisites, not additional approaches.

## Approach 1

Question: Can improper adjacent color repetitions be removed at negligible density cost?

Result: Yes. Encode the endpoints of monochromatic wedges as the third edge class of a tripartite auxiliary graph. Every such edge has one triangle because its endpoints have exactly one common neighbor. Triangle removal deletes o(n^2) auxiliary edges; a specified map transfers these to at most as many original edges and destroys every monochromatic adjacent pair. Exact extremal and balanced-bipartite consequences are proved.

Gap: Proper rainbow-C4 colorings can still have the unknown extremal behavior.

## Approach 2

Question: Does properness make the associated triple system (7,4)-free so an existing hypergraph theorem can finish the problem?

Result: The standard forward implication is proved, but the converse is false. A four-edge path colored a,b,a,b supplies four linear triples on seven vertices while remaining properly colored and C4-free.

Gap: One needs new control over permitted alternating paths, or a direct density theorem. No (7,4) theorem is assumed or claimed proved.

## Approach 3

Question: Can an additive affine label on two cyclic vertex classes produce positive density with a linear palette?

Result: No within the stated unit-coefficient family. A dense grid contains a nondegenerate square by multidimensional Szemeredi, and its off-diagonal edges receive identical labels.

Gap: Non-affine and other algebraic coloring systems are not addressed.

## Approach 4

Question: Can a finite example be amplified by complete uniform blowup or unrestricted isolated-vertex padding?

Result: Complete blowup is obstructed because K_{t,t} requires t^2 distinct colors. Isolated-vertex padding preserves validity but divides density by the square of the size expansion.

Gap: Neither observation excludes modified constructions or supplies bounded-ratio sizes. An arbitrarily sparse subsequence of sizes does not meet the all-size target merely by padding.

## Approach 5

Question: Does counting common neighbors already force vanishing edge density under a palette of n colors?

Result: Every K_{2,d} uses 2d colors. A double count and Cauchy-Schwarz give the explicit quadratic-root upper bound in PROOFS.md, with limiting coefficient 1/(2 sqrt(2)) for n colors.

Gap and stop: The coefficient stays positive. All five approaches have explicit remaining gaps; the original question is unsolved by this attempt. No sixth mathematical approach was pursued.
