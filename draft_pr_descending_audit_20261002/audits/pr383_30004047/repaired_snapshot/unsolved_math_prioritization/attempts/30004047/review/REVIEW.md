# Full independent review: mono-constrained two-step density

PASS for the scoped results. Both original assertions remain unresolved after five substantive author turns. This review is not a novelty certification or a claim of external peer review.

## Binding and source

Reviewed all five proofs, the source scope, final result, frozen manifests and full exact replay. Author manifest SHA-256: 7a3a86cd82d0057438b599e4e1b6d4d5a5f4196cdf7fd9bc583467af1a7373de. Final WIP: 5bff26446951d935a58199e99a4742a949565a43. No frozen author changes are required.

Visually checked printed pages 46–47 of the original OWR contribution, including both the universal definition and the exact strict/weak asymmetric hypothesis. Checked the published paper's mono-constrained results and Theorem 6.6. The source uses distinct reached vertices, not path multiplicity. Only the A-to-B and B-to-C degree conditions are present. The neighboring biconstrained psi problem is separate. Its known results cannot supply missing reverse degree hypotheses here. The 2022 paper's approximately 0.352202 diagonal threshold does not settle the one-third threshold. Credited finite LP duality and the weighted framework are legitimate dependencies.

## Turn 1

The fixed-template optimization correctly places the maximum over C outside the averaging over first-part types. Last-part weights enforce admissibility but do not average that maximum. Finite LP duality gives the stated certificate, and rational optimal data admit finite blow-ups. This is not a minimax assertion over all templates.

The complete-uniform family is evaluated exactly by a union-size bound and the all-h-subsets attainment graph. The count uses ceil(x binomial(n,r)), including the boundary cases r=1 and k=1. A below-1/k value forces x no larger than the displayed binomial ratio. For r>=2, the separate inequalities kx<1/k and y<1/k exclude the weak condition kx+y>=1, including k=2. For r=1, integer kh<n is what supplies the needed strict-threshold obstruction. No template reduction is claimed.

The 396-vertex graph has the stated degrees and reach 9/11. The missing-two-label first vertex defeats every two-vertex integral cover. This refutes only that stronger covering mechanism, not the original half-reach statement.

## Turn 2

The rank bound counts positive-weight types, not total A weight. Every middle vertex has a positive C-neighbor, so its whole A-neighborhood has weight below half under the contradictory hypothesis. Counting incidences without alpha validly bounds nx by two. The graph on occurring pairs, its independence inequality, and the pairwise incompatible-type disjointness all follow directly from the two forward degree conditions.

For four A-types, no disjoint pair of edges can occur. The star/triangle classification and triangle-plus-singleton charge are complete, including isolated vertices. For five types, the fractional-cover dual half-integrality proof is valid: every fractional tight component must contain an odd cycle, since a bipartite component admits a two-sided perturbation. Equality at total cover 5/2 forces a fractional perfect matching with no singleton weight. Independent incidence columns imply that its nontrivial support components are odd cycles. On five vertices this gives exactly the two listed alternatives. Incompatible unions are complements of a occurring edge or singleton as claimed. The endpoint examples keep strictness visible and are not original counterexamples.

## Turns 3 and 4

The integer r=floor((n-1)/k) is exactly the largest possible reached-set size under strict below-n/k reach. Each occurring r-type owns a disjoint C class of weight at least y. If k such classes existed, any type contained in none would have available C weight less than y; otherwise their union would cover n vertices with at most kr<n. This proves the type bound rather than assuming it.

The U charge covers every maximal type and every smaller type. The denominator inequalities use |U|<=tr and positive denominators correctly. The r=0 and r=1 cases are separately contradictory. Thus the symmetric result through 4k and the reduction of 4k+2 through 5k follow with their stated strict endpoints. The nine-vertex relaxation is explicitly nonrealizable: summing all ten triple degree requirements gives y<=2/7.

At n=4k+1 the count forces exactly k-1 four-types. Residual C weight is less than 2y, forcing intersection of every two residual neighborhoods in C. Their A unions consequently have size at most four. The triple-family classification is complete: either a common pair or a common four-set. Every charge in the common-pair and four-set cases is feasible for all occurring types, not just for triples. In the exceptional disjoint U,D,w case, a pair containing w must meet every residual triple in its other point; the singleton or empty common intersection accounts for all such pairs. The revised charges then have total greater than k+1. This proves the claimed 5k bound, while leaving unbounded A and the full asymmetric wedge unresolved.

## Turn 5

Pairwise disjoint maximal A-neighborhoods partition A, and every nonempty type is assigned to exactly one block. Empty middle types may be discarded from this accounting. Hence mx<=1. A below-1/k graph forces m>=k+1 and y<1/k by a separate reachability average. For m>=k+2 the displayed inequality contradicts kx+y>=1, including the equality endpoint at k=2. With m=k+1, any two maximal blocks have combined weight greater than 1/k because their complementary k-1 blocks are all strictly lighter than 1/k. The representative C-neighborhoods are disjoint, giving the final contradiction. The argument does not wrongly assume C reaches only whole blocks.

Deleting middle mass epsilon lowers x to (x-epsilon)/(1-epsilon), while preserving y. Both normalized threshold inequalities are algebraically identical to the stated strict and weak epsilon bounds; positivity and the denominator conditions are retained. No small-deletion claim is asserted for arbitrary graphs.

The local uncrossing example was independently reconstructed from the actual finite incidence graph. After deleting the two middle labels, each C vertex still reaches exactly 45 first vertices. Adding the union type raises this to 51 or 55, depending on its label. It therefore cannot even receive one C edge without raising the old maximum. This disproves the specified local nonincreasing operation with other edges fixed, and says nothing about arbitrary global rearrangements.

## Checks and final scope

Full author replay passed 12,967,236 assertions, 27 historical bindings, 67 total file bindings and two primary PDF checks. Separate standard-library controls passed 30,053 assertions, with no author imports: compatible triple-family classification, exact uniform-family endpoint inequalities, reconstruction of the 396-vertex uncrossing graph, and rational deletion equivalences. Finite controls do not replace the universal analytic proofs or establish an upper bound on general counterexample size.

Approved disposition: original unsolved, five of five. The remaining obstruction is arbitrary large overlapping higher-rank middle-to-A neighborhoods. No general laminarization, support reduction, full threshold theorem or original counterexample has been supplied. No sixth search turn is included. Publication should preserve the frozen author and review whitelists, add a current-status wrapper, and change only the target queue status/turn cells.
