# Post-seal mathematical addendum

Timestamp: 2026-10-12T15:10:28.518453+00:00. Checkpoint completion estimate: 97% of the scientific implication audit. The immutable first files are preserved unchanged; this addendum makes the source normalization and a v1 notation issue explicit.

## Rate normalization, exactly as the source SDE uses it

The first assessment's q_v and displayed lambda-a neighborhood functions are the physical generator intensities. Section 3.2 of v1 gives Poisson intensity `Leb^2 tensor varsigma`, with a probability measure varsigma on jump marks. Fix X={0,1,2}, J={1,2}, varsigma(1)=varsigma(2)=1/2. To implement physical transition rates lambda_a times the number of type-a neighbors, use SOURCE acceptance functions

`r_a(G,v,t,x) = 2 lambda_a 1{x_v(t-)=0} sum_{u in N_v(G)} 1{x_u(t-)=a}`.

Integration over mark a multiplies this by varsigma(a)=1/2, recovering q_v exactly. Set `C_l,T=1+2 lambda_max*l`. This is positive and componentwise nondecreasing, and bounds the acceptance functions on EVERY simple graph, every history and every environmental mark. Choosing an unnormalized lambda_a acceptance rate with mark mass 1/2 would produce physical rate lambda_a/2; that is a real bookkeeping error, although doubling both rates would not change the qualitative existence argument. The exact original rates are recovered here. The first assessment anticipated a corresponding intensity normalization in words; its displayed formula should be read as generator intensities, with this explicit adjustment when implementing the source SDE.

## Literal v1 offspring notation and a direct proof on the actual tree

The actual rendered v1 page 22 Definition 5.14 puts index k+1 on the left of the size-biased offspring equation, while its surrounding prose describes offspring. There is also a root-generation notation ambiguity in the conditioned offspring statement. Read literally, that index would shift the intended offspring law and is not the actual CM offspring law. I do not suppress the issue or pretend the literal symbol alone identifies the tree.

The actual CM limit is specified independently: root degree D, and non-root offspring Y=D*-1 with

`P(Y=k)=(k+1)P(D=k+1)/mu`, `nu=E[Y]=E[D(D-1)]/mu<infinity`.

The core conclusion of Corollary 5.16 is nevertheless available from its own underlying Proposition 5.15 mechanism, as follows. Fix any finite horizon T and any positive nondecreasing closure-rate bound family C_l,T. Let gamma=varsigma(J)<infinity (gamma=1 for our chosen probability mark measure). In the source's potential-jump site percolation, a vertex with offspring y and a parent has closed neighborhood size y+2 and is active independently, conditional on the tree, with probability

`p_Delta(y)=1-exp(-gamma C_(y+2),T Delta)`.

In a non-root descendant tree, retain all even generations and retain an odd-generation vertex only if active. This half-percolation dominates the true active percolation. The expected number of grandchildren surviving from an even-generation vertex with Y-distributed children is

`m_Delta = nu E[Y p_Delta(Y)]`.

Since Y is finite almost surely, p_Delta(Y)->0 as Delta->0; since Y p_Delta(Y)<=Y and E[Y]<infinity, dominated convergence gives m_Delta->0. Choose a deterministic Delta>0 with m_Delta<1. Then expected even-generation population at generation 2r of the half-percolated descendant tree is m_Delta^r. Its probability of being infinite is at most the probability of having a vertex in every such generation, hence zero by Markov's inequality and m_Delta^r->0.

This calculation uses the FULL-tree closure size y+2 even at the root of a descendant subtree. It therefore explicitly avoids a parent-removal error. Equivalently one could apply Proposition 5.15 with the shifted bound family C'_l,T=C_(l+1),T to dominate the full-tree percolation on a descendant tree. The same deterministic Delta works for all descendant trees having the same Y offspring law. Countability of the Ulam--Harris vertex labels gives simultaneously finite descendant active components almost surely.

At the actual root, whose child count is D instead of Y, keep the root and every even generation. The expected surviving first grandchildren count is `mu E[Y p_Delta(Y)]<infinity`. At generation 2r for r>=1 the expectation is this quantity times m_Delta^(r-1), again tending to zero. Alternatively attach the root to its a.s. finite number D of descendant trees. Every active component avoiding the root has a minimal-generation vertex and is contained in its finite descendant active component; the root component joins only finitely many finite components. Thus ALL components of the source percolation are finite almost surely. This verifies finite dissociability of the exact CM tree and all relevant rate families, without relying on the printed UGW index.

This is precisely the elementary percolation mechanism of the already existing Proposition 5.15/Corollary 5.16 proof. It requires E[D^2]<infinity and no third moment. The whole implication is consequently supplied by the v1 general hydrodynamic theorem plus its own stated proof mechanism, with the notation qualification above. If one insists on treating v1 Definition 5.14 literally without using its surrounding prose or Proposition 5.15, the bare statement “our tree equals its literally indexed UGW(D)” is unjustified; the direct argument is the repair.

## Published-version comparison

I safely acquired the actual published body from the NSF Public Access Repository at https://par.nsf.gov/servlets/purl/10582270. Its title page identifies Electronic Journal of Probability 29 (2024), article 185, 1--63, DOI 10.1214/24-EJP1243. PDF SHA-256 is `2169be74748f44f4028478cfa3f160700b6c5f5abf9f59a63e6f64366ee79e9b` (1,011,506 bytes). I also acquired actual arXiv v3 dated 29 July 2024, SHA-256 `4c61999efd80f56ff4470e40308b19d6c35a9d8173954f7eb6f5084a750ed8cb` (963,071 bytes). They are distinct files and are not silently identified as the same edition.

The published Definition 2.4 uses the correctly shifted offspring law at argument k, as displayed above. Published Theorem 4.11 and Corollary 4.12 give the corresponding local-in-probability trajectory convergence and hydrodynamic empirical limit. Published Corollary 5.16 retains finite dissociability for finite-second-moment UGW laws. Its graph convention remains simple and Assumption 1 remains uniform over every graph, history and mark. The published Example 2.6's discussion of multiplicity marks does not itself waive that all-mark rate bound for unbounded multiplicity-dependent rates. The defect-vertex sandwich remains the rigorous bridge for the exact original multigraph dynamics.

The arXiv v3 numbering is different again: Theorem 4.11/Corollary 4.12 and Corollary 5.15; published finite dissociability is Corollary 5.16. Reading coverage and exact source acquisition identities are in the post-seal ledger. No claim is made that every page or every revision change was inspected. The early v1 general theorem already suffices; the later body confirms the needed mechanism and clarifies notation.

## Adversarial checks and limitations

The monotone order is the declared infection order `2<0<1`, not the integers' usual numeric order. Each type's graphical arrow map is monotone for all pairs of source/target states in this order, independently of the two positive rates. The physical exponential-edge model and the Poisson-arrow model need only have the same finite-state generator; their edge clocks are not claimed to be pathwise identical on every cyclic graph.

Forcing all defect vertices permanently to a color ensures every discarded parallel edge has both endpoints already occupied by that color. Any edge leaving the defect set has multiplicity one. Thus simple-skeleton generator equality is exact for the bounding processes even when rates differ, even if a defect vertex is a seed or the competing singleton, and even for loops or isolated skeleton vertices. It is not obtained merely from small defect density; that density alone could be insufficient if rare defects caused fast propagation. The source theorem applied to the bounding processes supplies the needed control of those effects.

To determine defect marks at a radius-r boundary, reveal all half-edges incident to the boundary vertex, with all newly revealed partner vertices and their degrees included in the exposure budget. A half-edge-count budget that omitted those partners would be unsafe. In the fixed-radius limit that enlarged exposure is finite almost surely, and every repeated vertex/collision contributes to the vanishing cutoff error. This is enough for empirical marked convergence in probability, rather than just annealed convergence.

The source trajectory limit is evaluated only at FIXED deterministic finite T_j after proving no deterministic-time root jump. Only then is n taken sufficiently large for that fixed j, and only then is j allowed to advance by the deterministic diagonal. There is no source assertion of a uniform logarithmic-time approximation being used.

The retained exact finite diagnostic script checks all 72 comparable two-coordinate arrow updates, 21,240 generator-coordinate comparisons on 759 multigraphs with up to three vertices and multiplicities at most two, and exact rational jump-mark normalization. Ordinary and optimized Python pass. Both reject an intentionally incorrect normalization with an explicit ValueError. These finite diagnostics check algebraic implementation and failure behavior only; the mathematical proof above and in the first assessment establishes the all-graph comparisons, and the imported hydrodynamic theorem establishes the stochastic limit. No finite computation is offered as a proof of a stochastic theorem.

No mathematical obstruction to the requested implication remains identified. The practical limitation is nonquantitative schedules: the reduction gives existence, not optimal growth rates, efficient computability, prescribed polynomial budgets, or a fixed-number-of-hubs conclusion.
