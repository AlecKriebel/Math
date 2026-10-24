# Fresh adversarial audit: metrizable reduction and thin-branch model

UTC checkpoint: 2026-10-24T23:22Z. Assigned verification completion: **100%**. Complete21.122 resolution: **not achieved**; the author's frozen discovery estimate is5%, highly uncertain. Reviewer: `/root/p21124_retraction_adversary`, not an author of the note.

**PASS for the frozen supporting deductions and non-word countermodel.** Audited proof SHA256: `a7dafdf2d8cd189c64c7924c29104cf6b80e391199a075e4d1367951dcbd8661`. The frozen checker and submitted certificate also match the author's checkpoint. No full-problem answer, novelty claim, or publication approval follows.

## Exact target and quotient construction

The source contract correctly fixes a finite ordinary group word w and its value **set** `G_w`, for an arbitrary profinite G. The target is `|G_w|<2^aleph0` implying that this set is finite. Closed verbal-subgroup conclusions, arbitrary continuous-map conclusions, finite generation, and CH are not assumptions.

Suppose the value set X is infinite and smaller than continuum. Choose distinct values x_i for i≥0. For every pair i<j there is an open normal U_ij separating their images in a finite quotient, because a profinite group has a separating basis of open normal subgroups. Enumerating this countable family and taking successive finite intersections gives descending open normal N_n with closed normal intersection N.

The countable basis claim requires justification beyond the formal existence of countably many subgroups. It is correct here in either of two ways:

- `G/N` embeds continuously into the countable product of finite groups `G/N_n`. The map is injective because its kernel is N; a continuous injection from compact to Hausdorff is a homeomorphism onto its image. Thus the quotient is compact metrizable and second countable.
- Alternatively, if an open subset O of G contains N but no N_n, the descending compact sets `N_n\O` are all nonempty and have nonempty intersection, contradicting `N⊆O`. Hence the neighborhoods `N_n/N` are cofinal at the identity of `G/N`. Their finite sets of cosets give a countable full basis.

All selected x_i remain distinct modulo N. The quotient q maps X **onto** `(G/N)_w`, because any finite tuple in the quotient lifts coordinate by coordinate to G and word evaluation commutes with q. Its word image is therefore infinite and has cardinal at most|X|<continuum. It is compact as a continuous image of the compact finite power of the quotient.

## Perfect-set and cardinality step without CH

For an uncountable compact metric space K, take a countable basis and remove the union C of basis opens whose intersections with K are countable. The union C is countable. The closed set `P=K\C` is nonempty and uncountable. If p were isolated in P, an open neighborhood of p would meet K only in p and a subset of C, making p belong to one of the removed basis opens. Thus P has no isolated point. Binary splitting within P into disjoint relatively open sets with nested shrinking closures produces an injective map from Cantor space into P. Compact metric spaces also have cardinal at most continuum, by their countable basis. Hence every uncountable compact metric space has cardinal exactly continuum.

The quotient word image above must consequently be countably infinite. This proves the stated equivalence: a small infinite word image anywhere yields a countably infinite word image in a countably based quotient; such a quotient is itself a counterexample to the original question. No CH or assertion that every cardinal below continuum is countable has been used. There is no justified restriction to topologically finitely generated groups.

The earlier frozen source contract's warning against merely discarding other small cardinals needs a scope addendum after this deduction: the countable reduction is now **proved**, rather than assumed. Root agreed to preserve the historical contract and add that clarification separately. This is a cross-file interpretation point, not a defect in the audited note.

## Exact inverse limit, including the tuple issue

For a surjective inverse sequence of finite groups Q_n, the maps on the finite word images Y_n are surjective: lift a tuple realizing a value in Q_n to Q_(n+1). This does **not** assert that every selected tuple realizing a fixed lower value lifts to a tuple realizing an arbitrarily selected higher value.

For a coherent value sequence y_n, let K_n consist of tuples in `G^d`, G=limQ_n, whose word value projects to y_n. Projection `G→Q_n` is onto for a surjective inverse sequence, so K_n is nonempty. It is closed, and coherence makes these sets nested. Compactness of `G^d` gives a tuple in their intersection. This is a fully justified simultaneous lift and proves `G_w=limY_n` as actual subsets of G.

The fresh secondary reviewer supplies a boundary control: for squares under C4→C2, the coherent values can be0 at both stages, while the particular lower witness1∈C2 cannot lift to an upper witness for0∈C4. Thus solution-fiber surjectivity is not available. The proof correctly uses nested compact fibers instead.

If|Y_n|≤M for every n, M+1 distinct limit values would be pairwise separated at finitely many levels, hence at one common deeper level, contradicting the bound. Conversely every Y_n is a projection of the limit, so a finite limit uniformly bounds their sizes. Equivalently, the nondecreasing integer cardinalities eventually stabilize exactly when the limit is finite. Empty/identity words and finite groups cause no exception.

## The first-nonzero map is a valid obstruction to the broad mechanism

Use additive coordinates on A=∏_(i≥1)F2. At a nonzero point with first1 at k, its prefix through k gives a clopen cylinder on which f is constantly e_k. At0, forcing the first m input coordinates to0 forces the first m output coordinates to0. These are continuity proofs at every point.

The image is precisely `{0,e1,e2,...}`. Each e_i is isolated by its ith coordinate; e_i→0, and every neighborhood of0 contains all sufficiently late e_i. Its first Cantor–Bendixson derivative is{0} and its second is empty. It is a countably infinite compact convergent sequence space. The local constancy locus contains A\{0}, a dense open set because0 is not isolated in A. Conjugation is trivial, so every image point has singleton conjugacy class and conjugacy equivariance holds.

For every integer m, multiplication by m on A is the identity for odd m and zero for even m, including negative integers. Therefore `f(ma)=mf(a)` in all cases. This is an extra property of this model; the note does not claim that arbitrary noncommuting word maps commute with powering all inputs.

At level n the image has n+1 points. Under truncation every nonzero image point has exactly one lift, while0 has the two lifts0 and e_(n+1). A coherent infinite path either stays0 forever or first becomes e_k at level k and thereafter has a uniquely determined nonzero tail. These are all paths. Thus unbounded finite image sizes coexist with a countable inverse limit. The claim that arbitrary surjective finite-set systems must have continuum limits is genuinely refuted.

This is **not a word map**. On an elementary abelian group, an ordinary word evaluates as the sum of its arguments multiplied by exponent sums modulo2. In one variable it is either0 or the identity. Here `f(e1+e2)=e1` while `f(e1)+f(e2)=e1+e2`, so additivity already fails. A further independent diagnostic is failure of naturality under the coordinate swap1↔2: that swap fixes e1+e2 but does not fix f(e1+e2). No implication about genuine fixed word maps is inferred from this non-word example.

## Scattered-image and isolated-value consequences

A countable compact metric space is scattered: a subset without isolated points would have a nonempty perfect compact closure and therefore continuum cardinality. Its isolated points are dense; apply scatteredness to any nonempty relatively open subset. In an infinite compact metric space there are infinitely many such points, and a sequence of distinct isolated points has a convergent subsequence whose limit is another, nonisolated point.

For an isolated x∈G_w, choose a group-open neighborhood O with `O∩G_w={x}`, then an open normal U with xU⊆O. This gives the exact unique-lift statement `G_w∩xU={x}`, and the converse is immediate. The finite quotient **may depend on x**. The note is not claiming one finite quotient isolates infinitely many distinct values at once.

Small word image also implies that every value has finite conjugacy class. The class of a value stays inside the word image. An infinite conjugacy class is the homogeneous profinite quotient by its closed centralizer, and the associated orbit map is nowhere locally constant unless that centralizer is open. Detomi–Klopsch–Shumyatsky's result then supplies continuum many values; in the open-centralizer case the class is finite. There is no claim that the closed subgroup generated by these finite-conjugacy values consists entirely of finite-conjugacy elements.

## Independent artifacts and primary checks

The independent tuple-coordinate implementation in `independent_check.py` uses a direct first1 scan, not the author's low-bit formula. It checks n=0,...,12, including the trivial boundary. It verifies exact input fiber counts: size1 over0 and size `2^(n−i)` over e_i (one-based i). It checks286,685 integer-power cases, prefix compatibility, the single splitting output fiber, nonadditivity, and failure of coordinate-swap naturality. Independent tree enumeration through level25 gives n+1 coherent prefixes. A separate final section executes the author's checker read-only and reproduces every non-timestamp certificate field.

The fresh secondary audit independently verifies the quotient and inverse-limit proof and the solution-fiber boundary. Its artifacts and receipt are in `secondary/`.

Fresh primary reads confirm the cited source boundaries: [DKS1907.01344v2, Proposition2.1 and Lemma2.2](https://arxiv.org/html/1907.01344v2#S2) concern nowhere local constancy and conjugacy classes; [Shumyatsky2401.15707v2, Theorem1.1](https://arxiv.org/html/2401.15707v2#S1) concludes finiteness of the iterated verbal subgroup; [de las Heras–Zozaya2502.07427v1, Theorem1.1](https://arxiv.org/html/2502.07427v1#S1) assumes a dense equationally Noetherian subgroup. Applying the first proposition to every nonempty clopen source region gives dense local constancy, not global local constancy. None of these citations supplies the missing arbitrary-word branching mechanism.

No substantive objection remains in the audited scope. The precise open step is unchanged: rule out thin splitting for genuine fixed group-word maps, or construct a genuine word/group system realizing it. Neither has been done here.
