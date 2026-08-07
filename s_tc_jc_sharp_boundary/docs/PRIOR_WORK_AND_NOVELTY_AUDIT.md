# Prior-work and novelty audit

## Frozen scope

The revised headline theorem concerns all binary standard semi-directed
`S_TC` level-2 networks under the open four-state Jukes--Cantor model, modulo
ordinary triangle redirection. The phrase "all" is always qualified by
`S_TC`, level 2, the standard semi-directed convention, and JC. Complete
stochastic-image equality under triangle redirection is not claimed.

The structural reconstruction returns one canonical topology modulo `T` and,
optionally, the complete structural `T`-equivalence class. It does not claim
that a fixed input distribution belongs to the stochastic image of every
redirected orientation; that is a separate pointwise semialgebraic membership
problem.

## Closest work

| Reference | Prior class/model/result | Precise increment here |
|---|---|---|
| Holtgrefe, Huber, van Iersel, Jones, and Moulton, *Theory in Biosciences* 145 (2026), article 4 | General characterizations of weakly and strongly tree-child semi-directed and multi-semi-directed networks (Theorem 5 and Corollary 3). | A direct binary-level-2 structural theorem: `W_TC` automatically excludes blobs with two triangles. The narrow audit did not locate this exact lemma in the cited paper. |
| Ardiyansyah, arXiv:2104.12479 (2021) | Fourier-invariant distinguishability results for simple and semisimple level-2 network varieties, including four-leaf cases, under standard group-based substitution constraints. | Direct historical context for level-2 variety comparison. The paper does not supply a global open-stochastic, one-sided-containment classification for all binary standard `S_TC` level-2 networks. |
| Englander, Frohn, Gross, Holtgrefe, van Iersel, Jones, and Sullivant, bioRxiv 2025.04.18.649493 | Generic JC identifiability for triangle-free strongly tree-child level-2 semi-directed networks (Theorem 3.2 in the manuscript version consulted). | Extends from triangle-free networks to every binary standard `S_TC` level-2 topology and identifies exactly the residual ordinary triangle-redirection quotient. |
| Englander et al., same preprint | The JC trinet polynomial `F_abc=r_ab r_ac r_bc-u_abc^2`, introduced to distinguish a three-leaf tree from strict level-1/2 trinets (Proposition 2.26 in the April 2025 version). | The polynomial itself is not new. Its new use is on labels restored by a rigid core-3 support, which separates all residual seven-port completions. |
| Brits, Holtgrefe, van Iersel, and Martin, arXiv:2607.12919v2 | Full level-1 identifiability modulo triangle redirection; level-`k` trinet inequality. | Treats interacting level-2 theta blobs under JC and proves the full `S_TC` classification is still modulo only ordinary triangle redirection. |
| Currie et al., arXiv:2606.26673 | Complete semialgebraic geometry of the three labelled three-leaf JC triangle models, with full-dimensional intersections and differences. | Explains why the local quotient is formulated using a common regular germ rather than equality of complete stochastic images; the present theorem globalizes the quotient within the level-2 `S_TC` class. |
| Cox, Gross, and Martin, *Bulletin of Mathematical Biology* 87 (2025), 132 | Geometry and dimension of group-based models on 3-sunlets. | Supplies triangle-model context; it is not used as a proof of the level-2 result. |

## Version and numbering note

The cited level-2 preprint changed between its April and December 2025
versions. The manuscript identifies the trinet inequality as "Proposition
2.26 in the April 2025 version" and records the latest version consulted in
the bibliography. The level-1 theorem and level-`k` lemma are cited to the
version explicitly named in the bibliography.

## Incremental contribution

The paper contributes five linked results:

1. every binary standard semi-directed `W_TC` level-2 topology automatically
   has at most one triangle per blob;
2. a pointwise cut-split theorem and directed local-to-global containment
   theorem for all binary standard `S_TC` level-2 networks;
3. an exhaustive cycle/four-theta local classification, including one-sided
   containment, lifted from bounded rigid supports to arbitrary port words;
4. closure of the residual 192 seven-outgoing-port core-3 cases by applying the
   established trinet inequality to newly restored support labels; and
5. a sharpness theorem showing that `W_TC \ S_TC` contains an all-leaf-number
   non-triangle ambiguity.

The paper does not address level greater than two, richer substitution models,
a positive classification of the full weakly tree-child class, equality of
complete open stochastic images under triangle redirection, or the
input-specific problem of deciding which redirected orientations contain one
fixed distribution.
