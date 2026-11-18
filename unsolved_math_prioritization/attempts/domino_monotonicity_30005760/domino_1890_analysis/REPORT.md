# Literal horizontal domino inversion monotonicity: partial investigation

Status: UNRESOLVED. This report does not prove or disprove the full conjecture. It contains five substantive approaches, an exact finite basis, a low-inversion injection, a stable-range bijection, exhaustive finite checks, and obstructions to two natural injection strategies. No novelty claim is made.

## Scope and source convention

For n,k≥0, let D(n,k) consist of permutations π of length n with k inversions, globally avoiding1324, for which some position cut c∈{0,…,n} has π[1:c] avoiding132 and π[c+1:n] avoiding231. Count permutations, not cuts. Empty cells are allowed.

The original printed p.285 of Oberwolfach Report6/2024 (https://doi.org/10.4171/OWR/2024/6) visibly has one horizontal row [Av(132)|Av(231)]. Thus the literal grid is a split by positions, not values. The previous page fixes inversion count while increasing length. The structural source https://arxiv.org/abs/1711.10325 instead defines a gridded vertical domino with top213/bottom132; transposing yields213, not231. Its formulas cannot simply be used here. This report addresses the literal horizontal ungridded interpretation, not any silently corrected intended problem.

## Approach1: canonical cut obstruction and complete finite basis

Use 1-based positions. Let E be the minimum last position among132 occurrences, or n+1 if none. Let S be the maximum first position among231 occurrences, or0 if none. A cut c is valid exactly when S≤c<E. Consequently the grid condition is E>S. This tests existence and does not multiply by E−S.

If E≤S, take a132 occurrence ending atE and a231 occurrence starting atS. Their position sets are disjoint, or share only E=S. Thus every nonmember has a witness of length≤6. Shared-point witnesses standardize to exactly14352,15342,24351,25341. The disjoint witnesses are the20 interleavings listed in basis_certificate.json. Each witness contains one of1324,15342,25341,365241,465231; the certificate gives explicit positions. Conversely each of those five patterns violates the defining global/grid conditions, and avoidance conditions are hereditary. Therefore, rigorously,

D=Av(1324,15342,25341,365241,465231).

The four witness orders of size5 and20 of size6 exhaust possibilities because within each triple the relative order is prescribed. The certificate is a short finite proof, not an extrapolation from enumerating to some arbitrary length. Minimality follows by checking all one-entry deletions, also covered by verify.py.

Outcome: exact reformulation and efficient membership test, not a monotonicity theorem by itself.

## Approach2: direct exhaustive inversion distributions

Generate each member of length n+1 uniquely by inserting its maximum into a member of length n, retain exactly those satisfying the direct original definition. This is complete because D is hereditary and deletion of the maximum is unique. enumerate.py uses the E,S criterion plus a direct1324 test; it does not use the derived finite basis to generate the data. Inversion counts are explicit pair counts. counts_extended.json stores every coefficient and totals. The verified scope and last length are recorded in VALIDATION.json; no assertion beyond that finite range is made.

Small totals at lengths0 through10 are1,1,2,6,23,101,476,2324,11549,57933,292246. For example the length5 distribution is[1,2,5,10,16,19,19,15,9,4,1]. All checked adjacent-length coefficient differences are nonnegative; absent coefficients are zero. These computations are evidence only, not a proof for all n,k.

## Approach3: endpoint and all insertion-only strategies fail

Appending the new largest entry preserves inversion count but creates1324 whenever the input contains132. Prepending the new smallest entry similarly creates1324 when the input contains213, and can also destroy the grid condition:4231∈D becomes15342∉D despite still avoiding1324.

The permutation2413∈D has three inversions, is sum-indecomposable, and contains both132 and213. Appending5 gives24135 with1324 at positions1,2,4,5. Prepending1 gives13524 with1324 at positions1,2,4,5. Any insertion adding no inversions must be an isolated direct-sum singleton: all earlier entries are smaller and all later entries larger. For an indecomposable input, the only possible positions are the two ends. Hence2413 has no inversion-preserving one-point insertion intoD at all.

Outcome: this rules out every injection that only inserts a point while keeping the old permutation as an unchanged pattern, not arbitrary nonlocal injections or the counting conjecture.

## Approach4: stable-range bijection on sum components

Every permutation has a unique factorization into nonempty sum-indecomposable components. For decomposable π∈D, define T(π) by inserting a singleton component immediately after its first component. This adds no inversions and is injective: remove the second component, which is a singleton.

Proof T preserves1324 avoidance. An occurrence involving the new isolated singleton cannot use it as either middle point of1324, which form an inversion. If it is the smallest/first point, replace it by any point in the first component, all of which precede and are smaller than the later entries. This gives an old1324. If it is the largest/final point, the first component would contain132, and any old point of a later component already extends that to1324. Both are impossible.

Proof T preserves the horizontal grid condition. No231 occurrence can involve an isolated singleton, because231 is sum-indecomposable. An old132/231 obstruction cannot be created. In a new132 occurrence involving the singleton, that point can only be its smallest/first entry; replace it with any point of the first component. The endpoint of that132 is unchanged, as is any later231 start, producing an old obstruction. This is impossible. The E>S criterion therefore still holds.

If a sum-indecomposable permutation has length m, it has at least m−1 inversions. One proof sorts it by exactly inv(π) adjacent swaps: every position boundary must be crossed at least once, otherwise its initial prefix-value set would already be{1,…,i}, a sum cut. For a permutation with c components, summing gives inv(π)≥n−c.

Consequently, if n≥k+2, every member of D(n,k) is decomposable, so T is defined on all ofD(n,k). Moreover every member ofD(n+1,k) has at least3 components. Every interior component of a1324-avoider must be a singleton: an inversion inside it, together with a point of an earlier and later component, gives1324; a nontrivial increasing component is not indecomposable. Thus deleting the second component from any target gives a member ofD(n,k) by heredity, remains decomposable, and invertsT.

Therefore |D(n,k)|=|D(n+1,k)| for all n≥k+2. In particular the requested inequality holds in this stable range. This alone does not settle n≤k+1; Approach5 strengthens the proven range to k≤n.

## Approach5: testing the publicly posted almost-decomposable injection

The source https://arxiv.org/abs/2604.01143v1 (Section6, Theorem6.3) describes the Linusson–Verkama map f. It extends singleton insertion by deleting a boundary point, inserting the middle singleton in the resulting decomposable permutation, and reinserting the boundary point with specified priority and position/value adjustment. transfer.py implements those four explicit cases F1,F2′,F3′,F4′.

The map does not preserve our entire class. Take π=4723516 (length7,11 inversions). Its valid horizontal cut is c=4. Deleting its first point, smallest point, or last point does not make it decomposable. Deleting its largest point7 gives423516=42351⊕1. The source's F4′ inserts a singleton between these components, then inserts new largest8 one position later than the old largest. The result is f(π)=42835167, still with11 inversions and globally avoiding1324, but containing25341 at positions2,3,4,5,6. Its earliest132 endpoint and latest231 start are both4, so no grid cut exists.

The obstruction extends into the source's half-monotone range. For every n≥7, let π_n=(4,n,2,3,5,1,6,7,…,n−1). Its cut c=4 is valid. Deleting n leaves42351 followed by an increasing tail, which avoids132. Therefore every132 of π_n uses n as its middle/largest value and cannot extend to1324; n itself cannot be the final entry of1324 since only one point precedes it. Thus π_n∈D, with inv(π_n)=6+(n−2)=n+4.

Removing the first, smallest, or last point leaves an indecomposable permutation: after the first position its largest value already occurs, and the first value is not1. Removing n gives42351⊕id_(n−6), so F4′ applies. Its output is(4,2,n+1,3,5,1,6,7,…,n), containing25341 at positions2,3,4,5,6. For n≥11, n+4≤2n−7. In particular n=11,k=15 is an explicit failure within the cited half-monotone range, not merely outside it.

Outcome: this infinite family blocks an unqualified restriction of the cited map, including its half-monotone range. It does NOT disprove the counting inequality. Incompatibility of one forbidden pattern alone would not establish failure for the intersection; these explicit inputs inD and outputs outsideD do.

### A positive restricted-range theorem from the same injection

The supplementary independent_structure.md proves |D(n,k)|≤|D(n+1,k)| whenever k≤n, using exactly Theorems6.1 and6.3 of the cited source, not a claim of global D-compatibility. For an indecomposable input, f's image has at most two sum components: otherwise deleting its second singleton would produce a decomposable source with the same image, violating the global injectivity theorem. At length n+1 with k≤n inversions, the image's inversion graph therefore has cycle rank k−(n+1)+r≤1. Since4231 has cycle rank2, the image avoids4231. The direct inclusion Av(1324,4231)⊆D, proved in the supplement, establishes membership.

For n≥7, k≤n implies k≤2n−7, so the source guarantees that all inputs are in the map's domain. Cases n≤6 are checked exhaustively over every permutation through length7 by independent_smallcase_check.py. For decomposable inputs the earlier singleton injection preserves D. All branches are restrictions of the same source injection, so there are no cross-branch collisions. The supplement supplies the full graph lemmas, structural argument, source dependencies, and finite small-case rows. Thus the remaining unrestricted range is k>n, not k≥n.

## Limitations and next step

Five approaches have been completed, not five proofs of the conjecture. The finite-basis characterization, k≤n theorem, stable-range bijection, and map obstructions stand separately. Numerical monotonicity is bounded. The literal231/source-intent ambiguity remains explicitly scoped. The strongest unfinished direction is whether a modified almost-decomposable injection preserves all five avoidance conditions in a larger inversion range. No full-conjecture acceptance, global open-status certification, or publication authorization is inferred from these partial results.
