# Independent review: Erickson exact graph colorings, source 3031 / alias 3114

Review completed: 2026-10-03 UTC.

## Disposition

**SCOPED PASS for the mathematical partial results and the additive strict-checker supplement. The original conjecture remains UNSOLVED, with the original five-turn author budget EXHAUSTED (5/5). No novelty certificate is issued.**

The frozen checker has one reproducible input-validation defect. It checks the integer type of lower-triangle edge entries, while its palette routine reads upper-triangle entries. Python considers an integer equal to an equal-valued float or Boolean, so the symmetry test does not close that gap. An additive corrected checker and regression suite are supplied. The frozen originals were not edited. All actual frozen certificate edge labels are integers; the defect changes none of their results and invalidates none of the five mathematical proofs.

**Mandatory usage condition:** use `rooted_verify_strict.py`, or apply `rooted_verify_validation.patch`, whenever advertising strict integer-label validation. Do not describe the frozen checker alone as satisfying that promise. Both off-diagonal entries are now type/range checked; diagonal entries remain deliberately ignored under the documented model convention.

This is an uninvolved audit. The reviewer did not participate in the author's finite-model worker, did not consult that worker's separate scratch packet, and performed no sixth author construction search. Work was limited to source verification, adversarial proof review, reproduction, independent controls, and a narrowly scoped validation repair. No remote writes, PRs, publication, or queue updates were performed.

## 1. Frozen identity and reproducibility

The reviewed packet manifest has SHA-256:

`f4e747a9eebc3fcfbad9b607539d31ebae5fe7174226575064dfee94af00fcfd`

All 39 listed files matched their byte counts and SHA-256 values before review. The strongest construction, `TURN_2.md`, matched:

`22794a8f325bb9a3ca68b6af964160e856c778eb9d3978749a2c27222c31db99`

The entire author replay ran successfully in a separate copy. Every manifest-listed file in that copy was byte-identical to the frozen original afterward, including regenerated certificates and output JSON. The original packet and manifest were rechecked at completion.

Reproduced author checks:

- 12 positive rooted examples, 3 validation/negative controls, and 315 fixed-seed bounded-versus-full comparisons.
- Repeated K5 blocks, including every one of the 65,536 subsets of the 16-vertex (112,43) core.
- All subsets of the four gap-six gadgets and the author's p=10 through 10,000 representation checks.
- All 7,936 subsets of the gap-12 local gadgets and all seven semigroup certificates.
- The deficit-16 padding examples, weighted over all 2^22 and 2^24 subsets.
- All 131,072 subsets of the failed 17-vertex extension.

`author_replay.log` records the successful replay. The shell lacked `/usr/bin/time`; the initial timing wrapper failed before any replay work. Retrying with the shell's built-in `time` completed normally. This was an environment-only issue.

## 2. Exact target, primary sources, credit, and provenance

The live [2013 problem page](https://www.openproblemgarden.org/op/graphs_of_exact_colorings) and [Erickson's 2010 author-posted version](https://openproblemgarden.org/op/exact_colorings_of_graphs) agree: for finite integers c≥m≥1, P(c,m) concerns every surjective c-coloring of the edges of a countably infinite complete graph and the existence of an infinite induced complete subgraph using exactly m colors. The proposed classification is m=1, m=2, or m=c. To prove it, all c>m≥3 must be covered; a family of counterexamples is not a full resolution.

The pinned dataset extracts for 3031 and 3114 are identical to their records in the full cached dataset. Their statements are byte-identical and share SHA-256 `0af7f39efdbc59158e1eab5d5ee5dbd24500be6053bd5a17c323f07dbd3300b2`. There is no keyed research-results entry for either OPG code. The full cached source files, not the much smaller adjacent extracts, were hashed independently and match the [repository manifest](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/manifest.json), blob `55589bae6bad2d3e2f696e08645330ff1219b709`, dataset revision `37e53eabe540fb458758e198be61634bd02ee008`:

- problems.json: 68,931,837 bytes; `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`
- research_results.json: 80,334,822 bytes; `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`

A fresh read of [QUEUE.md](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md), blob `d60e9b1df63bebb7b49af7bbb6c6ed64c83681d0`, still has 3031 at rank 425, queued 0/5, and no 3114 row. That is the remote state, not this local attempt's completed author budget. The old queue blob recorded in SOURCE_GATE is a historical snapshot, not a claim that the current entire queue hash is unchanged. Keep alias 3114 reserved; do not fabricate a separate queue record. This audit did not rerun every historical PR/commit/branch search in the author's gate, so their scoped negative-history search remains a recorded author procedure rather than a fresh global absence certificate.

The full local Stacey–Weidl author preprint, dated 1996-06-13, was inspected, especially pages 2–3 and 16. Its published form is [JCTB 75 (1999), 1–18](https://doi.org/10.1006/jctb.1998.1855). Theorem 2 supplies p≢q modulo 6, p=0, or q=0 coverage. Page 16 additionally records p=q; q∈{1,2,3,k−2,k−3,k−4,k−5}; and n−p<k−q. Theorem 3 gives sufficiently large c for each fixed m≥3. Page 3 already states finite vertex-and-edge-colored core equivalence. The packet correctly credits that reduction and does not present it as newly discovered. Page 16 states the extra boundary examples without proofs, so TURN_2's boundary completion is explicitly literature-dependent.

[Narayanan's author manuscript](https://sites.math.rutgers.edu/~narayanan/pdf/m_col.pdf) confirms the spectrum-size context and Erickson formulation. It is not a solution of the entire classification. The packet does not relabel its results as new.

The newest relevant primary source located in this targeted check is [Ranđelović, arXiv:2512.04233v1](https://arxiv.org/abs/2512.04233v1), submitted 2025-12-03. The live arXiv record still lists only v1 and no journal reference. [Theorem 4](https://arxiv.org/html/2512.04233v1) states failure of P(c,m) for all sufficiently large m and every c>m. Combined with fixed-m sufficiently-large-c coverage, this leaves finitely many pairs. Targeted title/author/conjecture searches found no later full resolution. This is a current-source check, not proof of global literature completeness. The 1994 Erickson article was not retrieved; the original-author problem page and later primary papers corroborate its attribution.

The warning about the 2025 preprint is accurate: §4 literally defines successive Y_i with a shared edge, while referring to four-vertex X_i supports. This is an apparent local transcription/construction inconsistency. It is not a refutation of the main theorem and is not used in this packet's proofs. Likewise, the explicit exp(10^83) bound occurs within Theorem 3's proof and must not be advertised as an independently verified global cutoff for Theorem 4. No full independent proof audit of that paper is claimed here.

**Source masking/novelty finding:** the packet retains known-source credit, identifies imported literature triage as third-party material, distinguishes new local arguments from cited coverage, and repeatedly disclaims novelty. The (112,43) example lies outside the specifically listed elementary Stacey–Weidl baseline: (n,p,k,q)=(16,10,10,4), with n−p=k−q=6 and no listed boundary condition. That does not establish its novelty against all literature. The same limitation applies to the gap-six family.

## 3. Finite rooted models: universal proof review

### Exact spectrum and complete core bound

A finite core V, spoke labels a(v), and core-edge labels b(uv), with monochromatic infinite tail color 0, has exactly the infinite palette family

P(S)={0}∪{a(v):v∈S}∪{b(uv):u,v∈S}, for S⊆V.

Every infinite subset has an infinite tail intersection because V is finite. Conversely S together with the tail realizes every listed palette. Thus the finite formula exactly characterizes all infinite subsets, with no missing subset-size case.

The 2(c−1) core bound is valid. In an arbitrary counterexample, first choose an infinite monochromatic set. For each other color retain endpoints of one edge of that color, using at most 2(c−1) vertices. Remove these vertices from the monochromatic set, then successively thin it to make each retained vertex's spokes constant. All c colors survive, and avoidance is inherited. The reverse construction is immediate. Arbitrary spoke labels must remain available for a complete search.

The target-verification bound 2(m−1) is also valid. Any m-color palette can be witnessed by one spoke or edge for each nonzero color; their endpoints occupy at most 2(m−1) vertices. The resulting subpalette contains all m colors and no additional ones. The m=1 empty-core case is correctly handled.

### Essential colors and crossing cores

A nonzero color essential at two vertices can occur only on their connecting edge; it is essential at no third vertex. Hence Σ_v |L(v)|≤2(p−1), with each |L(v)|≤n. For an inclusion-minimal set with p>m in an m-avoiding model, deletion leaves at most m−1, so d=p−m+1≤|L(v)|. This yields d≤n≤⌊2(p−1)/d⌋≤m.

For n≥d+1, counting gives p−1≥d(d+1)/2. If n=d, all n removed slots at every vertex must have distinct nonzero essential labels; spokes are private and each core edge has its own private color, so the same bound follows. Substitution gives binom(d,2)≤m−2. The stated quadratic bound and equality examples are correct.

When n=m, equality forces d=2, p=m+1, zero spokes, and precisely one occurrence of each nonzero color on an edge. Every vertex has colored degree two, so those edges form disjoint simple rainbow cycles. Conversely any nonempty deletion removes at least two of these colored edges. The diagonal cycle examples are valid and the order bound is attained by these vertex-minimal models. This does not say every pair has no smaller alternative model.

These are universal mathematical arguments, not inferences from the finite tests.

## 4. TURN_1: K5 deficit blocks

The proper K5 coloring has induced deficits 0,0,0,0,1,5 at orders 0 through 5. Its losses from full deficit 5 are {0,4,5}. With disjoint palettes and globally unique nongadget edges, deficits add over blocks. A sum of such losses cannot be 6.

For nonempty core order t, palette size is 2+binom(t,2)−D(S). The conditions b≥2, k≥max(7,5b−4), n≥max(k+1,5b) are sufficient:

- For t<k, the largest possible palette is 2+binom(k−1,2); m exceeds it by k+5−5b≥1.
- For t=k, m would require D=5b−6, equivalent to impossible loss 6.
- For t>k, the smallest bound is 2+binom(k+1,2)−5b; it exceeds m by k−6≥1.
- Empty core gives one color; m≥3 in the stated range.

The c>m claim follows from the same final inequality and n≥k+1. Independently reconstructed (112,43) palettes agree with the frozen complete spectrum on all 65,536 subsets. **PASS.**

## 5. TURN_2: full normalized p−q=6 family

The four raw edge-list certificates independently yield exactly these loss sets:

| Deficit | Core order | Losses |
|---:|---:|---|
| 3 | 4 | 0,3 |
| 5 | 5 | 0,4,5 |
| 9 | 6 | 0,4,5,8,9 |
| 11 | 7 | 0,4,5,8,9,10,11 |

The properness and every subset were checked. The written proofs also stand independently: in the order-six construction, deleting two vertices leaves every original three-edge matching represented before splitting; further splitting cannot lower the number of colors. The order-seven construction has the listed four singleton-color edges, with every vertex incident to one and vertex 1 incident to two. Deleting one vertex gives loss 4 or 5; deleting at least two gives loss at least 8. Deficit is monotone under vertex inclusion, since adding r edges adds at most r distinct colors.

The five bases 10=5+5, 11=11, 12=3+9, 13=3+5+5, 14=5+9 cover every residue modulo 5; adding deficit-5 gadgets covers every p≥10. Their vertex total is ≤p+1, preserved by adding five vertices for each added deficit 5. At most one deficit-3 gadget occurs.

For an arbitrary subset, total loss 6 is impossible: a lone loss is never 6; two positive losses can reach 6 only as 3+3, which is forbidden by the single deficit-3 gadget; all other combinations exceed 6. This covers **every subset of every assembly**, not merely the tested p range.

Normalize c=binom(n,2)+2−p and m=binom(k,2)+2−q with 0≤p≤n−2, 0≤q≤k−2. For p≥10, p−q=6, k≥7:

- There is room because gadget order≤p+1≤n−1.
- At t<k, m−[2+binom(k−1,2)]=k−1−q≥1.
- At t=k, equality requires deficit q, hence loss 6, impossible.
- At t>k, [2+binom(k+1,2)−p]−m=k−6≥1.
- Empty core yields one color. Surjectivity follows from the disjoint palettes and fresh spoke/tail colors.

If c>m, n>k: n≤k would make c−m≤−6. Thus no hidden feasibility problem arises. The omitted p<10 cases have q∈{0,1,2,3}; the only possible p≥10, k<7 case is p=10, q=4, k=6. These are exactly the credited Stacey–Weidl boundary cases. Consequently the full normalized difference-six statement is correct **with those cited boundary results**. It is not a result for all p≡q modulo 6. **PASS.**

The explicit failure of repeating the same gadgets at loss 12 is also valid: three K5 blocks can each lose 4.

## 6. TURN_3: larger fixed-gap semigroups

For d=6r≥12 and d/2+2≤t≤d, the stated modular factorizations are proper, with t−1 colors for even t and t colors for odd t. Each color class is a matching with at least three edges. Deleting one vertex removes no color, so the loss is t−1, strictly between d/2 and d. Deleting two removes no color either, so loss is 2t−3>d. Further deletion cannot increase deficit. Hence every nonzero loss exceeds d/2, and no single gadget has loss d; no union can have loss d.

Each allowed gadget has order at most weight w(t). Therefore an expression p=Σw(t) fits within p≤n−2 vertices. The full-spectrum size split is valid under all the stated conditions, particularly k>d: below k there are too few colors, at k the necessary loss d is absent, above k the palette bound exceeds m by k−d>0. The proof must retain k>d.

The gcd-one proof is valid for every allowed d: the interval contains consecutive orders 2s,2s+1,2s+2,2s+3. The first two weights have gcd s−1 and the last two have gcd s, so all four have gcd one. A finite positive generating set of gcd one yields all sufficiently large p, by reachable residues modulo the minimum generator. This proves only a fixed-d eventual family, not uniform coverage of all smaller p or all k.

The exact conductors were independently recovered with ordinary coin dynamic programming, not Dijkstra:

| d | Conductor |
|---:|---:|
| 12 | 122 |
| 18 | 258 |
| 24 | 458 |
| 30 | 641 |
| 36 | 964 |
| 42 | 1258 |
| 48 | 1698 |

Every supplied residue minimum and nonnegative representation agrees. For each conductor C, C−1 is unreachable, and C through C+a−1 are reachable, where a is the minimum generator; adding a proves the complete infinite tail. **PASS.** The p=16, q=4, d=12 noncoverage is correctly retained.

## 7. TURN_4: deficit-16 gadget and failed compact padding

The order-eight raw certificate has 28 edges, 12 colors, deficit 16, and induced deficit set {0,1,2,3,5,6,7,10,11,16}. In particular 4 and 14 are absent.

The proof's split-color counting is correct. For ≤5 vertices at least the seven original matching classes survive before splitting, giving deficit≤3. At order six, the two deleted vertices either hit different color-zero matching edges, allowing at most one color-zero split increment, or one matching edge, allowing at most two. In the second case one of the two distinguished color-one edges is removed because together they meet all four color-zero matching pairs. Hence at most three total increments survive and the deficit is at least 5. At order seven the losses are 5 or 6, giving deficit 11 or 10. Full deficit is 16.

For n=22, c=217, m=43, only t=10 or 11 could hit the target, requiring deficits 4 or 14. Smaller orders have at most 38 colors and orders at least 12 have at least 52. Therefore the example is globally 43-avoiding. The weighted count covers all 4,194,304 subsets.

For n=24, c=262, m=64, the claimed counterexample **fails**, as the packet states. All eight gadget vertices and any five of the sixteen fillers give 64 colors. Independent counting finds exactly binom(16,5)=4,368 target subsets among 16,777,216 subsets. The universal support obstruction is correct: if all deficit p is supported on h vertices, every t≥h can retain that deficit by choosing its entire support and padding. Thus support h≤13 necessarily fails here at t=13. This establishes a limitation of that architecture only. It does not prove P(262,64), nor does it claim the pair is unresolved in all literature. **PASS, with the failed construction preserved as a failure.**

## 8. TURN_5: arbitrary palette extension and sumset obstruction

For the exact (112,43) model, the new vertex has fresh spoke color 112 and background-zero cross edges. A subset omitting it has an old palette; a subset containing it has exactly one additional color. Thus the full spectrum is F∪(F+1), and the stronger multiplicity identity N_new(j)=N_old(j)+N_old(j−1) holds. Independent full enumeration confirms the identity. Since 42 belongs to F, the extended (113,43) model is not a counterexample.

For two rooted modules with disjoint nonzero palettes and zero cross edges, palettes intersect exactly in {0}, so their glued spectrum is {a+b−1:a∈F(A),b∈F(B)}. Every nontrivial module has a 2-color subset: choose a vertex with a nonzero spoke, or, if there are none, endpoints of a nonzero edge. Consequently any nontrivial such extension introduces m whenever m−1∈F(A). The obstruction is universal within the specified gluing architecture; interacting colors and different cross-edge schemes are outside it. **PASS, with the failed extension preserved as a failure.**

## 9. Independent implementation controls

`independent_controls.py` uses no author algorithms for positive verification. It computes palette unions by a subset-zeta transform from spoke/edge occurrence supports, rather than the author's candidate enumerator or incremental added-vertex algorithm. It independently checks:

- All 14 rooted certificates, including the intended failed extension; spectra and complete palette counts agree.
- All four raw edge-list gadgets, their properness, and their full deficit/loss tables.
- 123 exact weighted assembled spectra (p=10,…,50, three normalized boundary/interior choices each), including every subset multiplicity by convolution. These finite controls supplement, rather than replace, the universal TURN_2 proof.
- Both padding examples with complete multiplicities.
- All seven semigroup certificates via a different algorithm, and the 7,936 local d=12 subsets.
- Every surjective rooted assignment with n≤3 and c≤5, plus 400 differently seeded random models of orders 4 through 8: 6,555 models, 1,505 eligible minimal crossing cores, and 6 equality/tight cores. All target-witness size, essential-color, crossing-size, sharp-jump, and cycle-structure assertions hold.

The only author module imported by this independent test file is used at the end to demonstrate its validation defect. `independent_results.json` and `independent_controls.log` retain the exact outcomes.

### Validation repair

A concrete accepted malformed input is c=4, m=3, spokes=[1,2], edges=[[0,3.0],[3,0]]. Its numeric palette still corresponds to the same valid mathematical coloring, but it violates the documented integer-only representation. An equal-valued Boolean bypass is also reproduced. This is a schema-validation defect, not a false counterexample.

`rooted_verify_strict.py` checks both entries of each off-diagonal pair. `test_strict_validation.py` rejects 19 malformed edge-label cases, compares all 14 supplied valid-input outputs against the frozen checker, and verifies exit statuses 0 for the positive certificate, 1 for the intentional target-containing certificate, and 2 for malformed input. All passed. The original files and certificates remain unmodified.

## 10. Limits and required downstream handling

1. Preserve original-target status as exhausted/unsolved 5/5, full_resolution=false.
2. Retain the exact scope of each theorem, especially normalizations, fresh/disjoint palettes, k≥7 or k>d, and the literature dependence of gap-six boundary cases.
3. Retain both failed routes and their witnesses. Never report (262,64) or the simple (113,43) extension as avoiding its target.
4. Supply the strict checker or validation patch alongside any distributed verifier; preserve the frozen checker as provenance, not as an unqualified validation guarantee.
5. Do not infer novelty from this audit, the source baseline comparison, or targeted search misses. No global novelty audit or independent recertification of the 2025 asymptotic paper was completed.
6. Do not silently synchronize the remote queue, invent an alias row, or publish. This review authorized and performed no such external changes.

Within those conditions, no remaining mathematical repair is required for the partial theorem packet.
