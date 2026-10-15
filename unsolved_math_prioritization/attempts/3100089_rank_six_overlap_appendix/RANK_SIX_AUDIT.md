# Independent acceptance audit: arbitrary-ambient rank-six pressing connectivity

## Verdict and frozen version

**ACCEPTED, with no mathematical correction required.** The accepted theorem is: for every finite successfully pressable symmetric binary matrix of rank six, with any number of labelled coordinates, the successful-word graph at LCS at least two is connected and has diameter at most six. At rank six this is the original LCS at least rank minus four bound. Combined with the accepted lower-rank result, the bound holds in ranks at most six.

This verdict concerns the complete [rank-six proof](RANK_SIX_CONNECTIVITY.md) and its fully checked positive finite lemma. The distributed prose is identified in [MANIFEST.json](MANIFEST.json). The underlying positive witness collection is not distributed here; its exact coverage and verification contract are preserved in this audit and the [finite verification contract](FINITE_VERIFICATION_CONTRACT.md).

This is a computer-assisted proof after a rigorous finite-dimensional reduction, rather than an extrapolation from bounded ambient size. No claim of general-rank connectivity, universal one-vector component preservation, or novelty is accepted.

## Mathematical dependencies and source identity

The complete accepted [full-state and trajectory-fiber lemmas](../3100089_positive_connectivity_appendix/STRUCTURAL_LEMMAS.md) and [five-section terminal-coordinate and signature theorem](../3100089_short_neighbor_terminal_appendix/TERMINAL_COORDINATE_THEOREM.md) were read, and their exact identities were independently checked. The [complete terminal-coordinate audit](../3100089_short_neighbor_terminal_appendix/TERMINAL_COORDINATE_AUDIT.md) supplies its independent acceptance.

The terminal-coordinate result imports only pressability existence from Bixby, Flint, and Miklós, *Proving the pressing game conjecture on linear graphs*, Involve 9(1), 2016, pp. 41–56, Theorem 4 on printed p. 47. This audit rechecked the locally retained publisher PDF's 886,918-byte identity and SHA-256 `ba3882a3bdd2688c411630a42cfa78348f0c4d8b0043124e5a0ea7b030e2b3ba`, and read the extracted theorem and its surrounding qualification. The previous accepted audit supplied the independent retrieval and visual inspection. The existence theorem applies to arbitrary black-and-white graphs with a black vertex in each component; deleting isolated white vertices yields the required formulation. No external connectivity theorem is used.

Primary source: https://msp.org/involve/2016/9-1/involve-v9-n1-p03-s.pdf

No source PDF, copied source text, or source image is included in this audit packet. No no-isolated-word theorem, short-neighbor theorem, negative-search screen, basis-exchange claim, or withdrawn proof is a dependency.

## Review of the symbolic arbitrary-ambient reduction

### Full rank, quotient, and normalization

Every legal press lowers the full rank by exactly one. The six quotient vectors selected by a successful word therefore form a basis. Gram–Schmidt along that word produces an orthonormal trajectory basis; each selected coordinate has its own coefficient one and all later coefficients zero. Thus the selected-vector matrix is unit lower triangular, with exactly fifteen freely chosen bits. All 32,768 roots are relevant, and no nonsingular coordinate change is being mistaken for a permissible change of original labels.

The root code stores lower-triangle entries row by row: (1,0), (2,0), (2,1), through (5,4), with diagonal bits fixed at one. Coefficient position zero is the least significant bit. Consequently the three exceptional strings 011111, 101111, and 100011 are exactly masks 62, 61, and 49. The initial word's recovered profile was checked against its mask in every pair.

### Quantifiers in the positive bridge

For any two full successful words S and T, the target label a is specifically the first actual label of T. It is therefore initially black and admits a full successful continuation. These are the hypotheses needed by the accepted terminal/signature theorem. If its profile along S is nonexceptional, Section 5 of that theorem gives an at-most-four-edge bridge in the full ambient matrix. The use here is the positive bridge theorem, not the converse of a necessary condition.

For exceptional profiles, the certificate covers every root and all three vectors, even when the seven-label restriction has no successful a-first word. Thus the finite lemma never discards a case on the basis of an unsuccessful restricted first press. Its old-only profile branch may legitimately invoke a later bridge using other original ambient labels; existence of that bridge is provided by the accepted full-ambient theorem, not by an unproved projection assertion.

### Lifting restricted successful words

Restriction to selected actual labels commutes exactly with every press at one of those labels. Hence every pivot legal in the selected principal Gram matrix is legal in the full matrix. Six such legal presses lower full rank six to zero. This clears the entire ambient matrix, including every omitted row and column. It does not merely clear a principal restriction or produce an abstract congruent state.

The coefficient profile of a also lifts correctly. At each pivot it is the a-coordinate entry of the current pivot column. Those entries are determined by the initial inner products and the same rank-one updates. They agree between the seven-vector model and the full quotient realization, including when the extra formal coordinate duplicates an old vector.

### Duplicate vectors, labels, and zero coordinates

The six old vectors are a basis, so their actual labels and quotient vectors are distinct. Every profile-type path uses only those six labels at every step. This applies equally when a is an omitted label with a duplicate vector or is itself one of the old actual labels. The model's extra coordinate is then used only to recover its profile, never as an additional pressed label.

Every first-label-type entry explicitly requires its candidate vector to differ from all six old vectors. Therefore its actual target label is also distinct from all six old labels. Relabelling all seven formal labels is injective, preserves all checked common subsequences, and introduces no repeated original letter. The certificate has 3,072 duplicate-vector inputs; all 3,072 use profile witnesses. Ambient zero coordinates cannot occur in a successful word and are covered by full rank exhaustion.

### Diameter accounting

A nonexceptional starting profile costs at most four edges. A profile certificate costs at most two edges and is followed by the accepted at-most-four-edge bridge, giving at most six. A first-label certificate costs at most two edges by the formal finite lemma and is followed by at most two edges connecting a-first words. In the supplied certificate every first-label path actually has one edge, so those cases cost at most three. Fixed-first-label connectivity follows from shared-letter diameter two on rank-five suffixes, with the common first label supplying the second common letter.

Identity steps in the imported constructions may be omitted. Every certificate step checked here is nonidentity. All paths remain in the complete successful-word graph of the original matrix. The global diameter bound is therefore sound.

## Independent complete positive verification

The independent verifier was written before reading or importing either the author's builder or verifier. It reconstructs roots itself, represents complete matrices by row-bit tuples, and applies the literal update M plus (M e_v)(M e_v) transpose. Profiles are recorded from successive pivot-column entries at label 6. A separate ordinary dynamic-programming recurrence calculates LCS. There is no trusted search, determinant recurrence, trajectory enumeration, or absence conclusion.

In each of normal Python, `-O`, and `-OO` modes, it verified:

- Exactly 32,768 distinct roots, with precisely masks 62, 61, and 49 once each: 98,304 input pairs.
- Every seven-label initial Gram matrix has independently computed binary rank six.
- 98,304 initial successful-word replays, each recovering the specified candidate profile.
- 98,306 noninitial successful-word replays; every word has six distinct in-range labels, every pivot is diagonal one, and the entire seven-by-seven terminal matrix is zero.
- All 98,306 nonidentity edges have LCS at least two: 986 with LCS two, 10,006 with LCS three, 32,727 with LCS four, and 54,587 with LCS five.
- 96,308 profile entries have nonexceptional odd-norm endpoint profiles and old-only paths. Of these, 96,306 have one edge and two have two edges.
- 1,996 first-label entries have one edge, start their terminal word with label 6, and satisfy the required vector-distinction check.
- Every path has one or two edges. The two two-edge inputs are root 15,845/mask 62 and root 31,602/mask 62.

All three complete outputs are byte-for-byte identical. Explicit exceptions, rather than removable assertions, enforce every check.

### Independent ambient stress test

Each of the 98,306 noninitial certificate words was additionally replayed on one full 66-coordinate Gram matrix containing every one of the 64 vectors in F2^6, an extra zero-vector coordinate, and an extra copy of a nonzero coordinate. Formal labels were mapped to their actual vector representatives. Every one of these full 66-by-66 matrices cleared after six legal presses in each optimization mode.

This test includes all possible quotient vector types, omitted coordinates, duplicated vectors, and radical-zero coordinates simultaneously. It supplements the symbolic lifting proof; the arbitrary-ambient theorem does not depend on extrapolating this fixed-size test.

## Negative controls

Nineteen independently constructed mutation controls were rejected for their intended reasons, with byte-identical outputs in normal, `-O`, and `-OO` modes:

1. An otherwise valid old-label edge with LCS one.
2. A profile endpoint whose signature remains exceptional.
3. An identity step.
4. A repeated pivot label.
5. A five-letter word.
6. An out-of-range pivot label.
7. A Boolean masquerading as an integer label.
8. A diagonal-zero pivot.
9. A claimed a-first endpoint beginning with an old label.
10. A three-edge path, exceeding the certified bound.
11. An extra label used on a purported old-only profile path.
12. A six-pivot word leaving a nonzero full ambient residual.
13. A candidate mask outside the three exceptional vectors.
14. A valid a-first word with a duplicated old vector, violating the certificate's stronger distinct-label contract.
15. Incomplete root coverage.
16. A duplicate root record.
17. Duplicate exceptional-mask coverage.
18. A root code outside its domain.
19. A Boolean masquerading as an integer root code.

Control 14 uses root 17,409, mask 49, and successful word (6,1,2,3,4,0). It passes legality and LCS but is correctly rejected by the explicit vector-distinction guard. This confirms that the duplicate-vector guard is independently effective, rather than incidentally protected by failure of another condition.

Separate integrity controls reject altered manuscript bytes, altered certificate bytes, missing artifacts, and a self-rehashed changed verification inventory against its independently fixed identity. These checks bind the verifier, complete results, controls, reviewed inputs, report, and source metadata.

## Reproducibility and publication scope

Complete positive replay with the universal 66-coordinate lifting test, and the negative controls, were run in normal Python and both optimization modes; the resulting mathematical outputs were compared. Separate integrity verification checked the independently fixed inventory identity and every recorded artifact’s size and digest.

This prose edition preserves the full symbolic proof, audit, exact finite coverage, and verification conditions. It does not include executable programs, raw witness or state collections, or coordination material, and is not a self-contained executable reproduction bundle. Independent readers cannot reproduce every positive replay from the distributed prose alone. The positive finite lemma remains a computer-assisted part of the proof, rather than a new symbolic derivation of those 98,304 cases. Copied third-party source material is excluded.

The accepted result remains rank-six connectivity and its diameter-six bound. Rank seven and above at LCS at least rank minus four remain outside this theorem.
