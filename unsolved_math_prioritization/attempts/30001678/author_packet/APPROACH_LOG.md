# Five-approach log

The literature/source gate preceded the mathematical investigation on 2026-10-05 UTC. No complete resolution was verified. The following are five different mathematical approaches, not five downloads or five numerical trials. All retained claims have full proofs in PROOF.md. They are classical arguments or elementary deductions, without a priority claim.

## 1. Separate classes by orbit closures

Attempt: encode an orbit using the countable basic open sets that meet it, and pull the code back through the given reduction.

Retained result: Proposition 1 constructs the classifier for continuous Polish-group actions with closed orbits, including compact-group actions. This handles arbitrary Borel pullbacks into that restricted class.

Failed extension: finite bit flips have distinct dense orbits, so all closure codes coincide. The action is continuous and its orbit relation E0 is Borel. The missing hypothesis is genuine orbit separation, not continuity of the reduction.

## 2. Build coordinatewise antichains

Attempt: thin each source factor independently until its equivalence relation is equality, then combine all coordinate codes.

Retained result: Lemmas 2.1–2.2 prove countable-section meagerness and an explicit perfect antichain fusion. Proposition 2 handles the native coordinatewise product of countable Borel relations, including products of countable discrete group actions.

Failed extension: the original reduction need not respect coordinates. The duplication map has an image containing no full perfect product, and suitable target products have empty preimage. Arbitrary Borel pullback cannot be replaced by coordinatewise thinning without a new theorem. This is consistent with, and weaker than, the broader published countable-structure result.

## 3. Put a small product inside one orbit

Attempt: choose coordinate diameters small enough that every difference is allowed by the acting sequence group.

Retained result: Proposition 3 proves the full-box criterion. Corollary 3.1 supplies it for native weighted l^p translations and c_0 translations, below any starting perfect product.

Failed extension: Q^omega translations admit no perfect product within a single orbit, although Route 2 gives a smooth equality restriction. The box method cannot equate a one-class conclusion with smoothness. The finite-support subgroup also fails the box criterion, but its E1 relation is excluded by the original orbit-reducibility assumption.

## 4. Test finite-tail limits and arbitrary perfect restrictions

Attempt: take the limit of closed, continuously classifiable tail relations; alternatively use a perfect set in the full sequence space.

Retained result: Lemma 4.1 proves E0 nonsmooth by the Baire zero-one argument. Proposition 4 embeds E0 into E1 on every perfect product. The diagonal is a perfect set with a smooth E1 restriction but contains no full perfect product. The explicit increasing union F_N is nonsmooth even though every F_N is closed and smooth.

Outcome: both proposed shortcuts fail. Kechris–Louveau Theorem 4.2, read in the original published paper, prevents using E1 itself as an admissible counterexample. The infinite obstruction cannot be established by finite coordinate enumeration.

## 5. Force the graph to become closed on a rectangle

Attempt: organize a full countable-coordinate fusion rather than allowing coordinate splitting to collapse, and use compact-class distance codes.

Retained result: Lemmas 5.1–5.3 prove comeager rectangular fusion, continuous reading of a Borel map on a product, and smoothness of a closed compact equivalence relation. Proposition 5 shows the desired existential smoothness conclusion is equivalent to existence of a Cantor product on which the equivalence graph is closed.

Exact unresolved obligation: obtain such a closed graph from arbitrary Borel reducibility to a Polish-group orbit relation. Continuous reading applies to an existing classifier but does not construct it; applying it only to the given orbit reduction leaves the target relation nonclosed. Neither the closed-orbit proof nor the coordinatewise or box constructions cover the general interaction between coordinates.

## Stopping status

Five routes completed. No unrestricted proof and no counterexample satisfying all source hypotheses. Recommended research disposition is `unsolved`, five substantive approaches used. This counts the attempt's mathematical routes, not literature age or previous repository attempts. The source URL access limitation remains explicit and should be preserved in any later release.
