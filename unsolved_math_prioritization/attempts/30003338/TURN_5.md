# Turn 5: a stronger Kempe constraint and an exact four-coordinate method barrier

2026-10-02. Fifth and final substantive author turn for 30003338. **Original target unresolved, 5/5.** The negative covariances below belong to explicitly constructed auxiliary probability laws, not to a proved graph-coloring marginal. They do not refute the source question. The turn identifies an additional universal graph constraint, rules out one tempting abstract law, and shows that the retained necessary conditions still do not imply four-coordinate association.

## 1. Universal domination under coarsening terminal colors

Let T be any subset of the observed side A of a finite bipartite graph. For a prescribed color pattern φ:T→{0,…,q−1}, let N(φ) count proper q-colorings extending it. This includes hidden A vertices outside T.

**Theorem.** If ψ is obtained from φ by merging color classes, then N(ψ)≥N(φ), after choosing representatives for the merged classes. Counts depend only on the partition of T into equal-color blocks, by global color symmetry.

It suffices to merge color d into color c. In an extension of φ, take every (c,d)-Kempe component containing a terminal prescribed color d, and swap c,d on all those components. A two-color component cannot contain both a color-c terminal and a color-d terminal: all its A vertices have the same color. Thus the operation preserves properness, fixes the other terminal prescriptions, and produces an extension of ψ.

This is an injection, not a claimed bijection. Given an image coloring and the original pattern φ, swap precisely those same two-color components containing the original color-d terminals. The induced two-color graph, and hence its components, did not change in the forward map. This uniquely recovers the original extension. Components in an image cannot contain terminals of both original types; other target colorings may lack a preimage. Iterating the injection proves the theorem. ∎

The mechanism is classical Kempe switching, stated explicitly to expose its scope and equality issue. No novelty claim is made.

## 2. Equality with the monochromatic prescription

Let φ_* prescribe one color at every terminal. Then

    N(φ)=N(φ_*)

if and only if φ is constant on the terminals within each connected component of G.

If φ is constant componentwise, independent color permutations on graph components give a bijection of the two extension sets. Conversely, suppose two terminals in one graph component have different φ-colors. Merge φ's color classes into two classes which still separate those terminals, obtaining χ. Section 1 gives N(φ)≤N(χ). Compare χ with the all-one-color prescription φ_*.

The coloring assigning color c to every A vertex and color d to every B vertex is an extension of φ_* (with the monochromatic color c). Its entire relevant graph component is a (c,d)-Kempe component containing both original χ-terminal types. It is therefore not in the image of the merging injection. Thus N(χ)<N(φ_*), proving strictness. This argument also applies when some φ extensions do not exist.

This is a constraint on genuine graph marginals beyond color symmetry and the one-coordinate regression inequalities of turn 2.

## 3. An exact abstract law with all the earlier regression properties

Use four observed positions 0,1,2,3 and three color labels. Encode a block of positions by its bit mask. For a color word c∈{0,1,2}⁴, let π(c) be its partition into equal-color blocks. Assign the following per-word integer weight h(π):

    π                         h
    (1,2,12)                 44
    (1,4,10)                 35
    (1,6,8)                  35
    (1,14)                   44
    (2,4,9)                  35
    (2,5,8)                  26
    (2,13)                   44
    (3,4,8)                  44
    (3,12)                   44
    (4,11)                   44
    (5,10)                   44
    (6,9)                    35
    (7,8)                    44
    (15)                     44

These are all fourteen partitions into at most three blocks. The sum over all 81 color words is 3,240. Dividing by this total defines a color-permutation-invariant law μ, with every word having positive probability and each zero indicator having marginal 1/3.

An exact exhaustive check of the 168 upward events E on four indicators proves

    Cov_μ(1_(c_i=0),1_E) ≥0

for each of the four coordinates i: all 672 inequalities hold. The table also obeys all 31 strict-refinement comparisons h(coarser)≥h(finer). These finite claims are fully certified with integer arithmetic in verify_turn5.py and TURN_5_ABSTRACT_CERTIFICATE.json; no numerical LP assumption enters the certificate.

Nevertheless, for F={c_0=c_1=0} and G={c_2=c_3=0},

    P_μ(F)=P_μ(G)=11/90,    P_μ(F∩G)=11/810,
    Cov_μ(1_F,1_G)=−11/8100.                                (1)

Thus singleton regression, color symmetry, full support and non-strict partition-coarsening dominance do not imply four-coordinate association. By turn 4, this law still has associated marginals on every three coordinates.

## 4. Why this first law cannot be a graph witness

The table gives equal probabilities to the all-zero word and to the particular word (1,0,0,0). Were it induced by uniform proper colorings on terminals in one bipartition class, Section 2 would imply that terminal 0 lies in a different graph component from each of terminals 1,2,3. Its color would then be independent of the other terminal colors, forcing P(F)=1/9, contrary to 11/90.

This also rules out realizing μ's zero-indicator marginal through some different color-symmetric law: the probability of the word (1,0,0,0) is forced to be half the exact-zero-set probability μ(S={1,2,3}), by symmetry between the two nonzero colors. The displayed zero-set weights have μ(S={1,2,3})=2μ(S={0,1,2,3}), so the same monochromatic equality and contradiction follow.

Consequently (1) is provably not a source counterexample. The equality characterization is essential; an arbitrary color-symmetric four-tuple cannot simply be called a graph-coloring marginal.

## 5. A strict full-support abstract obstruction remains

Let σ be the genuine color-word marginal on the four leaves A of the star K_(4,1). Its per-word weight is (3−|π|)/48: the center can use exactly the colors absent among its leaves. It obeys singleton regression by the universal Kempe theorem. Define

    ν=(99/100)μ+(1/100)σ.

Both laws have coordinate marginals 1/3, so each singleton-regression inequality is linear in this mixture. Therefore ν satisfies all 672 inequalities. It is color symmetric and has full support because μ does. Its per-word integer weight with denominator 648,000 is

    H(π)=198h(π)+135(3−|π|).                                (2)

Every proper coarsening strictly increases H: its h term cannot decrease and its block-count term strictly increases. Hence all 31 coarsening comparisons are strict, and the particular equality obstruction in Section 4 no longer applies.

But direct exact calculation gives

    P_ν(F)=P_ν(G)=46/375,
    P_ν(F∩G)=499/36000,
    Cov_ν(1_F,1_G)=−593/500000.                              (3)

All claims, including strictness and positivity of all 81 word weights, are checked by an independent-from-the-LP rational verifier. This proves that even strict coarsening dominance, full color symmetry, full support, all singleton-regression inequalities and all three-coordinate association conclusions are insufficient as abstract hypotheses for the four-coordinate source test.

It does **not** prove that ν is realizable by any graph. No such graph has been constructed here, and no general realization theorem is asserted. A proof of the source conjecture must use additional graph-specific structure; a counterexample based on ν would need a rigorous graph realization or approximation preserving a negative covariance.

## 6. Directed graph search, with exact signs and limited scope

The discovery LPs were numerical guides only. Their rationalized outputs were checked exactly before use, and the final table (2) is certified directly without SciPy or any solver. The optional LP script remains for provenance; the mathematical claims rest on the integer table and full finite inequality verification.

A separate bounded graph search tried to approximate the strict abstract partition law using graphs with four marked A terminals, two through four hidden A vertices, q=3, and 2–20 B-neighborhood factors. Neighborhoods containing more than two marked terminals were excluded because such a factor would forbid some three-color terminal words, whereas the target abstract law has full support. This is a heuristic choice of search family, not a proved restriction on all possible counterexamples.

The floating-point distance only steers proposals. Every graph evaluation counts all colorings through the exact marginal formula, and every tested covariance sign uses 128-bit integers. Across 12,030 graph evaluations, no source counterexample was found. The closest recorded graph has A size six and neighborhood masks (20,24,34,33), giving exact counts

    (Z, Z_F, Z_G, Z_(F∩G))=(2304,288,288,36),

so its covariance numerator is zero, not negative. The finite search does not prove that ν is unrealizable, nor that all source graphs are associated. Its distance diagnostic is not part of any proof.

## 7. Exact controls and final outcome

The standalone verifier certifies both abstract laws from their integer word weights, every singleton-regression inequality, all strict coarsening comparisons, and the exact moments in (1) and (3). It also checks the actual merging injection and its inverse on all relevant dreidel extensions, and checks the monochromatic equality characterization on connected and disconnected examples. All 18,422 exact assertions pass. These are author controls, not independent review.

Run python verify_turn5.py to regenerate TURN_5_CHECKS.json and TURN_5_ABSTRACT_CERTIFICATE.json. The optional bounded search can be rerun by compiling turn5_signature_search.cpp. Its exact count conclusions remain separate from its floating proposal heuristic.

**Final original disposition: unresolved after 5/5 substantive turns.** No full association proof and no unconditioned proper-coloring counterexample have been obtained. The four-vertex conjunction problem from the primary source remains unproved here. The retained universal partials and graph-class theorems are listed in FINAL_RESULT.md. No sixth author search is part of this attempt; independent review may verify or require corrections, not continue the unfinished search under a different label.
