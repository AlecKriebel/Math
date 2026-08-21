# Global mathematical proof audit

**Audit date:** 2026-08-20  
**Scope of this note:** complete manuscript and supplement, with an adversarial check of the global proof chain, marginal/restoration/probe arguments, contextual triangle substitution, and the Omega and Theta full-dimensional overlaps.  This note does not treat a successful program exit as proof and does not duplicate the separate line-by-line atlas/code audit.

## Bottom line

I found **no theorem-level counterexample** in the arguments assigned to this audit.  Conditional on the bounded decorated-relation theorem (Theorem 6.3) having the exact machine meaning asserted, the mathematical implications from that theorem to Theorem 1.1 are coherent.  The Omega and Theta counterexample families also survive independent exact recomputation of their graph, equality, strict-interior, and rank claims.

There are nevertheless two concrete defects in ancillary archive certificates, one real proof-exposition gap in the contextual triangle step, and an unresolved archive-citation defect:

1. the purported clean-room marginal-submersion replay groups the wrong (rooted, unnormalized) edge signatures;
2. one advertised probe-coherence collision test is tautological;
3. the contextual triangle proof introduces the contraction map without writing the tensor-substitution/gauge identity that makes it well defined for a multi-terminal context;
4. the supplement and bibliography still contain a pending DOI placeholder.

Defects 1 and 2 do **not** falsify the theorem: the written marginal proof uses the correct equivalence relation, a corrected exhaustive recomputation verifies its finite instances, and stronger direct-anchor/compact-probe gates check the actual transports.  Defect 3 is a short but logically load-bearing exposition omission; the missing statement follows from ordinary multilinear tensor-network contraction once the boundary normalization is fixed.  I therefore recommend **MINOR REVISION**, not rejection or major revision, on the material audited here.

## Exact theorem scope and observation relations

The positive theorem is not about every rooted tree-child presentation.  Its objects are leaf-labelled, binary, level-2, already-simple mixed graphs obtained by exactly one `sd_0` root suppression of an LSA-valid rooted binary network (Definition 2.1, manuscript PDF pp. 3--4; `work/source/paper/main.tex:235-268`).  The class is the strong class \(\mathcal S_{\rm TC}\): the fixed mixed graph has an admissible rooting and **every** admissible rooting is tree-child (Lemma 2.2, PDF p. 4; `main.tex:280-340`).  Parameters are open JC Fourier edge multipliers and inheritance probabilities in \((0,1)\), with uniform root distribution (PDF p. 5; `main.tex:362-401`).

The directed relation \(N\preceq_{\rm JC}N'\) means that a relatively open neighborhood in a regular **source** image stratum is contained in the target open stochastic image; the target may have larger dimension.  The symmetric relation \(\bowtie_{\rm JC}\) means a common regular germ of full local dimension on both sides (Definition 2.4, PDF p. 6; `main.tex:403-418`).  Theorem 1.1 says that either relation occurs exactly when the labelled reduced bridge trees agree and each corresponding nontrivial blob is label-isomorphic or differs only by an ordinary-triangle redirection (PDF pp. 2--3; `main.tex:180-195`).  Corollary 1.2 is a generic statement outside a topology-dependent proper algebraic subset, not everywhere identifiability (`main.tex:197-202`).

The sharpness results concern the larger weak-but-not-strong class.  Omega is triangle-free of common dimension \(2n+1\) (Theorem 1.3, PDF p. 3; `main.tex:204-215`); Theta is triangle-containing of common dimension \(2n\) (Theorem 9.3, PDF pp. 25--27; `main.tex:1690-1802`).  Neither family is asserted to be an ambiguity inside the strong class.

## Dependency graph reconstructed from the manuscript

1. Definition 2.1 and Lemma 2.2 fix the mixed-graph convention and characterize strong tree-childness by the no-omnian condition.
2. Lemmas 3.1--3.2 and Proposition 3.3 exhaust the cycle/four-theta primitive cores; Proposition 3.4 supplies uniqueness of an ordinary triangle in a strong blob.
3. Lemmas 4.1--4.2 plus exact Lemma 4.4 prove pointwise cut recovery in Theorem 4.3, hence the labelled decorated bridge tree in Corollary 4.5.
4. Theorem 5.1 identifies the complete positive incidence-scaling bridge fibre; Lemmas 5.3--5.4 and Proposition 5.5 turn global containment into projective local containment without cross-blob compensation.
5. Lemma 6.2, the support/completion grammar, and finite Theorem 6.3 feed fixed-full restoration; Lemma 6.4 reconstructs arbitrary port words and proves the necessity direction of local Theorem 6.1.
6. Lemma 6.5 supplies the ordinary-triangle local converse, Lemma 6.6 performs simultaneous physical gluing, and Theorem 6.1 plus Corollary 4.5/Proposition 5.5 yields Theorem 1.1.
7. The semialgebraic/Zariski argument at `main.tex:1440-1489` yields Corollary 1.2.
8. Exact graph-to-Fourier equalities, stochastic-interior checks, and rank bounds prove the Omega and Theta sharpness theorems.

This matches the archive's stated boundary: `PROOF_BOUNDARY.md:3-6` assigns marginal submersion, restoration, probes, contextual gluing, and the global implication to the human proof, while `PROOF_BOUNDARY.md:8-18` limits the finite computation to the bounded directed-relation assertion.  The crosswalk points Theorem 6.3 to the row-bound evidence map and independent gates (`THEOREM_CERTIFICATE_CROSSWALK.md:7-12`), and the regeneration map identifies the primitive-to-final pipelines (`REGENERATION_MAP.md:9-21`).

## Audit of restoration, marginal submersion, and probes

### Marginal open image (Lemma 6.2)

The **written mathematical argument is valid**.  After setting omitted Fourier characters to zero, a physical edge contributes only its complete vector of zero-sum JC exponents across all displayed switchings.  A descendant mask and its complement give the same XOR on a zero-sum assignment, so the equivalence relation must first normalize every mask modulo complement.  An all-zero normalized row is invisible and is discarded.  For each remaining edge class \(C\), the descriptor coordinate is
\[
y_C=\prod_{e\in C}x_e.
\]
Its differential has a positive coefficient in every class variable on the open cube.  Distinct classes are disjoint partitions of the physical edges, so these differential rows have disjoint supports and full row rank.  The inheritance block is an identity or parent-flip block.  Hence the descriptor map is onto (for example, take every \(x_e=y_C^{1/|C|}\)) and submersive.  The subsequent intersection of nonempty Zariski-open rank/smoothness loci and the constant-rank open-map argument are legitimate (`main.tex:1088-1137`, manuscript PDF pp. 15--16).

The archive replay advertised for this claim does **not implement that equivalence relation**.  `reviews/root_probe/verify_parameter_submersion.py:157-162` groups the raw rooted descendant-mask rows.  Lines 163--170 normalize only a diagnostic collection of *switching columns*, after the raw row classes have already been fixed.  Lines 170--185 retain full-mask tensor-invisible classes and report the raw class count as descriptor dimension.  Lines 246--312 then certify row rank for this wrong descriptor.

I independently recomputed every completion generated by that program from `primary/certificates/core_universe.json`, for source sizes 3, 4, 5, and 6.  There are exactly **42,908** completions.  For each physical edge and each displayed switching I regenerated its descendant mask, replaced each mask \(m\) by \(\min(m,F\mathbin{\mathsf{xor}}m)\) for the selected-port full mask \(F\), discarded the all-zero normalized row, and only then partitioned equal rows.  Results:

- the raw and corrected class counts differ in **42,908/42,908** completions (at minimum, the raw program retains a full-mask class that becomes zero);
- the raw census has at most 19 edge classes, whereas the corrected census has at most 17;
- with up to two inheritance coordinates, the corrected target descriptor dimension is at most 19;
- the corrected product classes are disjoint in every completion;
- the largest corrected product class has size 5 (212 completions attain it; the size histogram is 23,710 of size 2, 16,184 of size 3, 2,802 of size 4, and 212 of size 5).

The first discrepancy is the cycle completion with three outgoing ports, incoming retained, sink mask 0, and word counts \((0,3)\).  The archive raw rows are
\((1,1),(2,2),(4,4),(8,8),(12,12),(14,14)\), six classes.  Correct complement normalization and invisible-row deletion give
\((1,1),(2,2),(3,3),(4,4),(7,7)\), five classes, with physical class sizes \(1,1,1,2,3\).  This example is also visible in the frozen certificate's `redundant_parameter_example`.

This correction verifies, rather than undermines, Lemma 6.2: after normalization, every finite instance has exactly the disjoint positive product blocks used in the manuscript's proof.  Arbitrarily long subdivisions merely enlarge one or more such blocks and the same product-map calculation applies.  The primary hard-cover code does use complement normalization (`primary/hard_cover_compiler.py:141-164`), and the separately represented exact descriptor code explicitly normalizes before classing and discards invisible rows (`reviews/final_hard_cover_cleanroom/jc_exact.py:105-130,168-204`).

### Fixed-full restoration

The restoration direction is logically correct (`main.tex:1277-1305`, manuscript PDF pp. 18--19).  It fixes the full relation first, replaces every target dummy by its actual physical label, and takes each prefix as a direct marginal of that one assumed containment.  Lemma 6.2 supplies a relatively open selected germ at every prefix.  Therefore an exact separating certificate at any prefix contradicts the assumed full containment; the actual path must terminate at an isomorphic/ordinary-triangle anchor.  This does not make the invalid converse inference “a small marginal containment implies a larger one.”

The relevant archive data structure is appropriately a fixed-full forest, and the asserted regeneration path is explicit in `REGENERATION_MAP.md:17-20`.  `ATLAS_SUMMARY.md:29-34` says the authoritative record binds direction, graphs, disposition, base evidence, restoration transport, and closure evidence; the CSV is only a projection (`ATLAS_SUMMARY.md:36-39`).

### Coherent probes (Lemma 6.4)

The human combinatorial argument is sound once the unique anchor transport and the finite parent restrictions have been certified (`main.tex:1307-1331`, manuscript PDF p. 19).  A one-port probe locates the port's anchored interval; a two-port probe gives the relative order of ports in the same interval.  Pairwise order restrictions coming from actual finite words determine one total word.  If a probe subdivides the only ordinary-triangle edge, the triangle disappears and fixes literal orientation; otherwise Proposition 3.4 ensures that every surviving ambiguity is the same unique ordinary triangle.  The bound is eight support ports plus two probes.

However, the collision statistic in `reviews/root_probe/verify_probe_coherence.py` is **tautological**.  Lines 293--306 form the two one-port codes and the two-port code.  Line 308 places `codes[2]` inside the grouping key, line 309 sets `full_code = codes[2]`, and line 310 inserts that same value into the keyed set.  Consequently the collision test at lines 324--335 cannot possibly find two full codes under one key; lines 325--328 acknowledge that this two-port probe is already the full two-extra-label graph.  Thus this file is not independent evidence of assembly coherence.

The weakness is mitigated by stronger load-bearing gates: `REGENERATION_MAP.md:18-20` identifies the direct-anchor compiler/verifier and the 269,730 compact path-bound relations, while `THEOREM_CERTIFICATE_CROSSWALK.md:9-10` binds them to each atlas row.  Their actual semantic checks reconstruct parent restrictions and ordered transports, rather than relying on the tautological grouping.  The misleading ancillary certificate should nonetheless be repaired or its claim narrowed.

## Contextual triangle gluing and physical gluing

The strict three-sunlet calculation is valid: independent regeneration verifies equality of all 64 Fourier coordinates at the rational point, strict physical parameters, rank four for every orientation, and the four-dimensional normalized ambient bound.  Thus each orientation covers a common open neighborhood in the three-boundary tensor space (Lemma 6.5, `main.tex:1338-1359`, manuscript PDF p. 19).

The extension to an arbitrary unchanged context has a **load-bearing exposition gap** at `main.tex:1361-1379` (PDF pp. 19--20).  The proof simply introduces
\(\Phi:U\times\mathcal C\to\mathcal P\) as “the common contraction map.”  It does not explicitly establish that the chosen normalized/projective three-boundary tensor, including its three incidence gauges and port ordering, is a sufficient statistic for the context when two terminals reconnect inside one theta blob.  That equality is not supplied by the archive: `PROOF_BOUNDARY.md:3-6` explicitly assigns contextual triangle gluing to the human proof.

This is repairable without a new computational theorem.  The manuscript should state the standard substitution identity: after summing over the triangle's internal states, its contribution is a three-boundary tensor \(Q_{abc}\); every external context contributes a tensor \(C_{abc,\gamma}\), and the global coordinates are the finite multilinear contraction
\[
\Phi(Q,C)_\gamma=\sum_{a,b,c}Q_{abc}C_{abc,\gamma}.
\]
Equality of the boundary tensors therefore persists under arbitrary reconnection of the three named terminals.  The text must also say how the normalized incidence factors are assigned to \(Q\) or absorbed into the positive context chart, so that \(\Phi\) is literally the same map for all orientations rather than only projectively equal.  Once this identity/gauge convention is stated, the generic-rank and common-section argument at lines 1370--1377 is correct.  I classify this as an **exposition/proof-completeness gap, not a theorem-level error**, because multilinearity supplies the missing implication directly and no contrary context was found.

Lemma 6.6's subsequent simultaneous physical gluing is correct (`main.tex:1387-1421`, PDF p. 20): on compactly contained local neighborhoods all incidence scales and reciprocals are bounded; choosing each common effective bridge scale \(z_e\) sufficiently small makes \(x_e^{(k)}=z_e/(a_{u,e}^{(k)}a_{v,e}^{(k)})\) lie in \((0,1)\) on both sides.  Incidence scales cancel in the bridge product, choices are edgewise on a tree, and the product-chart extraction supplies the full-rank image.  This also excludes cross-blob compensation in the converse direction when combined with Proposition 5.5.

## Omega audit

The combinatorial claims in Proposition 9.1 (`main.tex:1570-1589`, manuscript PDF p. 23) were independently regenerated from the primitive graphs: each reduction is simple, binary, triangle-free and level two; the one blob has cycle lengths \(4,4,6\); all seven admissible rootings were enumerated; exactly two are tree-child; and the other five contain the asserted omnian witness.  The label-distance invariant distinguishes the two mixed graphs, and the absence of a triangle excludes triangle redirection.

For Proposition 9.2 (`main.tex:1591-1646`, PDF pp. 23--24), a separately implemented complete audit verified all zero-sum Fourier identities under the rational correspondence, all 256 Fourier/pattern coordinates at the strict point, and every open-cube inequality.  Independent symbolic differentiation gave core Jacobian rank 6 and reproduced the displayed nonzero minor
\(-723/8589934592\).  All fourteen Euler identities were checked; one pendant direction lies in the core span, so the full rank is at most \(6+4-1=9\).  The exact source and target rank-nine minors give the lower bound.  The rational correspondence is strict on a neighborhood and has common rank 9, so its image is relatively open in both nine-dimensional images.  Identical cherry substitution then adds exactly two dimensions per taxon, giving \(2n+1\).

I found no stochastic-interior, regularity, or dimension gap in Omega.

## Theta audit

The graph/root audit confirms Proposition 9.4 (`main.tex:1718-1732`, manuscript PDF p. 25): both displayed rootings are tree-child, the alternate rooting has an omnian, the fixed reductions are weak but not strong and level two, and the leaf-1 triangle/nontriangle adjacency invariant excludes both isomorphism and ordinary-triangle redirection.

The independently replayed sharpness verifier regenerated equality of all 256 Fourier/pattern coordinates over \(\mathbb Q(\beta)\), proved the isolating interval and every strict parameter inequality, and reproduced rank 8 on both sides.  Algebraically, on \(BE\ne0\), five of the six displayed equations reconstruct \(J,K,M,N,O\) from \(A,\ldots,H,L\), and the remaining equation \(L^2=BEH\) is irreducible; its \(H\)-derivative is \(-BE\ne0\).  Thus the localized common locus is a smooth irreducible eight-fold.  Rank eight of the projection to \((A,\ldots,H)\) for both physical maps puts both images on the same positive branch \(L=\sqrt{BEH}\), hence both contain a common relatively open eight-dimensional neighborhood (`main.tex:1736-1791`, PDF pp. 26--27).  Cherry substitution yields dimension \(2n\) and preserves the graph obstruction (`main.tex:1793-1802`).

I found no stochastic-interior, branch, irreducibility, or rank gap in Theta.

## Active falsification results

- **Class membership/conventions:** No contradiction found.  The no-omnian test is applied to all admissible rootings of the fixed mixed graph, not merely to the displayed rooting.  Omega and Theta are correctly outside the positive class.
- **Atlas exhaustiveness:** The mathematical reduction to cycle/four-theta cores, strong repairs, completion grammar, both incoming modes, and relative port permutations is coherent.  The complete record counts are checksums, not premises (`ATLAS_SUMMARY.md:3-4`).  Final acceptance still depends on the separate archive/code audit confirming the asserted one-record-per-relation regeneration.
- **One-sided containment closure:** Restoration always marginalizes a fixed assumed full relation; it never promotes a smaller relation upward.  No invalid closure reversal found.
- **Stochastic interior/regularity:** All audited witnesses are strictly inside \((0,1)\), and the relevant exact minors are nonzero.  The physical gluing step shrinks to a uniform positive interval.
- **Genericity:** For fixed \(n\), the topology set is finite; irreducibility of each complex model closure, semialgebraic dimension, and the constant-rank stratification justify the proper exceptional set at `main.tex:1440-1489` (PDF pp. 20--22).  The proof correctly includes only witness pullbacks known to be nonzero on the intended stratum.
- **Nontriangle ambiguity in the strong class:** None was found.  Omega and Theta exploit a failure of strong tree-childness, and the bounded local theorem is the sole remaining finite dependency excluding a strong-class nontriangle relation.

## Concrete defect classification

| Severity/type | Exact location | Defect | Mathematical effect |
|---|---|---|---|
| **Reproducibility defect** | Lemma 6.2, manuscript PDF pp. 15--16, `main.tex:1091-1108`; archive `reviews/root_probe/verify_parameter_submersion.py:157-185,246-312` | Replay classes raw rooted-mask rows instead of zero-sum complement-normalized rows and retains invisible full-mask classes. | Its reported descriptor dimension/rank is not the lemma's descriptor.  Corrected 42,908-case recomputation passes the actual product-block claim, so no theorem counterexample. |
| **Reproducibility defect / misleading test** | Lemma 6.4, PDF p. 19, `main.tex:1307-1331`; archive `reviews/root_probe/verify_probe_coherence.py:293-335` | The grouped key already contains the alleged `full_code`, making zero collisions tautological. | This certificate supplies no coherence evidence.  Direct-anchor and compact semantic gates provide the relevant nontrivial parent/transport checks. |
| **Exposition/proof-completeness gap** | Lemma 6.5, PDF pp. 19--20, `main.tex:1361-1379`; `PROOF_BOUNDARY.md:3-6` | The common contextual contraction map and incidence-gauge compatibility are asserted without the explicit multi-boundary substitution identity. | Central but short repair: state multilinear boundary-tensor contraction and gauge absorption.  No counterexample; no new finite certificate required. |
| **Reproducibility/citation defect** | Supplement PDF p. 6, `work/source/supplement/supplement.tex:381-385`; `work/source/paper/references.bib:164-174` | `ZENODO_DOI_PENDING` remains and the bibliography says “Zenodo DOI pending.” | A supplied sidecar hash authenticates only the supplied object/envelope relationship; the public immutable archive cited by the paper is not yet identifiable.  Replace before submission. |

## Strongest verified result and exact remaining gap

The strongest result established by this audit is: **assuming the exact bounded classification in Theorem 6.3, the human structural, marginal, restoration, probe, local-to-global, semialgebraic genericity, Omega, and Theta arguments support the stated theorems; no nontriangle strong-class ambiguity or invalid one-sided closure was found.**  The marginal claim remains true under the correct normalization despite the faulty ancillary replay, and the two sharpness families have exact strict full-dimensional overlaps.

The exact remaining dependency is not a missing mathematical construction in these sections; it is independent confirmation that the regenerated bounded atlas truly contains each decorated directed relation exactly once with graph-derived evidence and correct transports.  That is the subject of the separate archive/code audit.  Before publication, the contextual contraction identity should be written explicitly, the two misleading ancillary certificates repaired or narrowed, and the DOI placeholder replaced.
