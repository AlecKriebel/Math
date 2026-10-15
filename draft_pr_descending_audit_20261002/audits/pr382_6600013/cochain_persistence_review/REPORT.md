# PR382 independent cochain and persistence audit

**Verdict: PASS_SCOPED for the assigned cochain/persistence family. No mandatory mathematical repair found. The original problem remains unsolved, 5/5.** This verdict certifies neither novelty, a solution of the original problem, nor merge readiness. Audit completion: 100%; progress to a proof or counterexample of the arbitrary source implication: 0% in this audit.

## Frozen inputs and independence

Reviewed PR head `421c6aa90eace49c8659f9a96e83c24fe1b5b901`. The 58 paths in `../snapshot_manifest.json`, SHA-256 `f5217fe6c213057956ff0c11c059b82d00f12b83e5b5375623eb2c3b0df9dec9`, matched both the manifest and `git show` bytes at that head, with no mismatch. The shared checkout was on main at `a5dfd64903e7abe6c8af9a078e19a7a490f0494c` when this family began; conclusions use the frozen PR input, not that current checkout.

Read SOURCE_NORMALIZATION and SOURCE_MANIFEST first, then fetched and read the original [Problem2.5.1](https://arxiv.org/pdf/1604.06280) and Julien's [Theorem5.10, Proposition5.13, Lemma5.14 and Proposition5.16](https://arxiv.org/pdf/0804.0145). The first reconstruction was sealed before opening candidate TURN proofs/code or any old technical review. PR metadata, including its scoped result summary, had been printed; this limited exposure is disclosed in INITIAL_RECONSTRUCTION. After independently reconstructing all five candidate proofs and inspecting all author libraries/checkers, CANDIDATE_RECONSTRUCTION was sealed before reading the old technical review. No sibling/root technical report was read.

## Claim and exact remaining gap

The target concerns all degrees of rational Cech cohomology of the translational hull of an aperiodic repetitive d-dimensional tiling with complexity O(n^d). It does not concern integral finite generation or merely large ranks of finite complexes. Julien's dimension-one mechanism is credited: connected Rauzy graph rank is p(n+1)-p(n)+1; a linear complexity bound forces a uniformly bounded rank on arbitrarily late stages; the rational direct limit is then finite dimensional. The published/arXiv numbering discrepancy is explicitly retained.

The packet's actual results give product and finite-cover subclasses, a finite-rank example with growing raw approximants, and a failed nonexpansive profinite candidate. Its exact unresolved gap is a uniform bound on persistent images for arbitrary source-admissible low-complexity hulls, or an admissible example with infinitely many persistent independent rational classes. This audit adds no sixth author search.

## Persistence quantifiers and direction

For finite-dimensional V_i, the increasing kernels of maps V_i to V_j stabilize for each fixed i. Their union is the kernel of V_i to the direct limit. Thus the canonical image has dimension inf_(j>=i) rank A_(j,i); increasing canonical images exhaust the limit, yielding

    dim colim V_i = sup_i inf_(j>=i) rank A_(j,i).

The bound M is therefore equivalent to `for every i, there exists j >= i with rank A_(j,i) <= M`. No uniform delay is needed. Arbitrarily late starting stages with some later endpoints also suffice, by moving representatives of any M+1 prospective independent limit classes beyond their common starting stage. Bounding one fixed source image, or finitely many source images, is insufficient. The formula includes infinite dimension.

A finite limit need not have a uniform stabilization delay: add a permanent rational class and one class at each time i which dies at i squared. Every source stage stabilizes eventually, but its latest transient may persist until a quadratic endpoint. The candidate correctly avoids deducing a universal two-scale estimate from its finite scans. Large raw dimensions can also be entirely transient, as in zero bonding maps on Q^i.

The crop map goes from fine to coarse chains; its transpose goes from coarse to fine cochains. The image formula `rank[B_target,F Z_source] - rank(B_target)` is valid because the map preserves cocycles and coboundaries. The candidate verifies those identities before using the formula. Symmetric cropping is tested only for equal-parity scales, so the windows are genuinely nested centered rectangles. Either parity gives a cofinal inverse system. Degree-one horizontal and vertical cells have different rectangle shapes, avoiding accidental label identification.

## Actual sheared construction and admissibility

The candidate uses z(i,j)=(t_(i+j),t_(i+j+1),y_j), with t Thue-Morse and y Sturmian. The two-symbol Thue-Morse block is invertibly recoded. Translation (a,b) acts as independent shifts (a+b,b), a unimodular change of integer coordinates. Minimality of each factor therefore gives minimality of the product action and repetitivity of the unit-square tiling. A period would imply b=0 from Sturmian aperiodicity, and then a=0 from Thue-Morse aperiodicity. The finite alphabet gives translational FLC. These agree with the definitions independently read in [Julien2017, Sections2.1 and2.3](https://www.numdam.org/item/10.5802/aif.3091.pdf).

An n-column, m-row rectangle recovers a Thue-Morse word of length n+m and a Sturmian word of length m. Every pair occurs by the independent coordinates. Consequently P(n,m)=p_TM(n+m)(m+1) and P(n,n)<=8n(n+1). The real extension of the integer shear identifies its suspension topologically with the product suspension, so the limiting rational rank is finite.

The signed mixed difference gives chi=(m+2)(s(n+m+1)-s(n+m))+s(n+m). Thue-Morse alignment and complete language recurrences yield chi=2n+6 for n=2^(a-1), and chi=-2n for n=3*2^(a-2), a>=2. Connected two-dimensional approximants then force beta2>=2n+5 and beta1>=2n+1 on those respective subsequences. This is an obstruction to a raw approximant-rank argument and cannot imply infinite hull cohomology.

The rectangular inverse-limit identification requires two-sided growing windows. The stated centered windows satisfy this: compatible interior faces retain the two fractional coordinates and reconstruct all symbols; edge and vertex identifications encode integer boundary crossings. Compactness supplies the homeomorphism after this reconstruction. No unilateral truncation is used to represent the full hull.

## Collared Thue-Morse survival

All ten shared-pair adjacencies of the six triple edges coincide with the complete legal four-letter language. The substitution-induced vertex and edge maps respect cellular boundaries. A double letter determines substitution parity; the forbidden alternating length-five words ensure every sufficiently long word supplies such a marker. Taking limits of substituted words gives existence, and parity gives uniqueness of each desubstitution hierarchy.

A substituted collared triple determines the central block and both neighbor blocks of length 2^n; hence neighborhoods of growing radius are determined even at a graph vertex. This is the required border information. Finite graph paths can include longer illegal concatenations; the growing substituted collars, rather than graph adjacency alone, eliminate them in the inverse limit. The candidate's argument contains this distinction.

Independent homology calculations assembled the stationary collar chain map from substituted strings without importing the asserted J basis. Its H1 image ranks at the first and second powers both equal 2. Equality of those ranks forces the stationary stable image to remain rank 2 at all later powers. Rational duality gives the same cohomological rank. Kunneth with the Sturmian factor therefore gives the limiting Betti numbers (1,4,4), total rank 9. Integral invertibility of the eigenvalue 2 is not asserted.

## Independent exact controls

The standalone independent_controls.py imports no candidate libraries. It generates a complete Thue-Morse language from a single substitution prefix containing every allowed adjacent pair, and generates Sturmian languages using exact quadratic sign/floor comparisons. It independently builds the rectangular integer chain complexes and crop maps. Primitive sparse integer row elimination computes exact rational ranks by fraction-free row operations and gcd normalization.

Rather than reuse the candidate's cocycle-basis formula, it computes the image on homology using the block matrix with source cycle constraints D, chain map F, and target boundaries B:

    image rank = rank([[D,0],[F,B]]) - rank(D) - rank(B).

This equals the cohomology pullback rank over Q. The resulting image ranks are:

| Source | Endpoint | H1 image | H2 image |
| --- | --- | --- | --- |
| 1 | 3 | 4 | 4 |
| 2 | 4 | 4 | 6 |
| 2 | 6 | 4 | 4 |
| 1 | 5 | 4 | 4 |
| 3 | 5 | 5 | 6 |
| 4 | 6 | 5 | 6 |

The first three reproduce every published persistence endpoint. The last two show that endpoint ranks above the limiting rank occur even at these later stages. Exact composition checks for 1->3->5 and 2->4->6 prove that the six-to-four degree-two drop really kills two dimensions from the source-2 image. It is not a comparison of unrelated complexes.

For scales 1 through 6, independently computed Betti numbers are (1,5,12), (1,5,14), (1,13,6), (1,5,18), (1,7,10), (1,19,6). All boundaries square to zero and the complexes are connected. The independent control passes 72 exact checks. A separate comparison, performed only after the independent construction was sealed, passes 761 checks: complete TM languages through length257, Sturmian languages through length80, every scale1..6 boundary matrix, six cropping maps, and 400 random rational rank controls including dependent rows. Cross-library agreement supports implementation consistency; the written all-scale proofs carry the infinite conclusions.

## Complete replay, source receipts and repairs

All five author scripts were copied to a private replay directory and run to completion. Their complete stdout files match the frozen TURN_CHECKS bytes; every stderr is empty. Aggregate REPLAY_ALL passes 5,367 assertions and 173 historical/final bindings. The script hashes, stdout hashes, timestamps and return codes are in the JSON receipts. Source-free replay correctly reports zero primary PDF checks.

Fresh downloads of the two original arXiv PDFs and Julien2017 match all frozen SHA values. The fresh Cambridge PDF differs from its historical hash: it has 485764 bytes and SHA `6546bc723d194a8bf788b6b37de96a6af939571679cbf92af07b813877a1ecfa`, with a footer showing the current download timestamp. The historical expected file has 485567 bytes and SHA `098e4c40604d18e2fea293d0a57711cd62b567f601971cd778d2428f54d365b5`. This is a source byte-reproducibility limitation, not a mathematical discrepancy established by this review. No four-source exact replay is claimed. The raw downloaded papers and private replay tree are ignored from publication.

Mandatory mathematical repairs: none within the assigned scope. Retain the frozen explicit all-scale quantifiers, centered/parity crop convention, rational coefficient distinction, admissible sheared construction, and README's existing PF/unit-roof clarification. The reviewed finite computations support the scoped results; they cannot promote the original arbitrary implication to solved.
