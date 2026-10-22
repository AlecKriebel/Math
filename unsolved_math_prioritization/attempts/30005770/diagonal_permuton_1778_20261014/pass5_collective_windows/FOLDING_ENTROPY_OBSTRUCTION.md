# Exponential fibres in a low-turnaround staircase folding map

Shared final PASS5, row1778 /30005770, 14 October2026. This is an obstruction to a concrete collective encoding, using actual canonical1324-avoiders. It is not a counterexample to their conjectured uniform weak limit, and it gives no upper or lower asymptotic estimate on the true finite-width gaps by itself.

## 1. The proposed map and the direction it would serve

The accepted PASS4 identity says that fixed-width unrestricted D-paths and canonical K-paths have the same exponential growth, by a constant-size guard. A possible collective comparison would fold an arbitrarily long path back and forth into W levels, merge the states at each level by skew sum, and retain the adjacent shuffle words. At a turnaround, duplicate the state so its two incident old edges can be stored separately. Reverse runs use inverse state patterns.

If this gave a recoverable encoding with small overhead and small fibres, it would lower-bound g_W by the full growth rate after accounting for the overhead. That would upper-bound delta_W=log(lambda/g_W). It would not provide the nonsummable lower gap required by the adaptive-window theorem. Such a comparison would nevertheless delimit the possible rate of that gap.

The theorem below shows that the natural fold loses an amount of information proportional to the original size, even when the total mass at turnaround cells is only O(n/W). Marking all turnaround points in the folded output does not recover that information. Even recording their complete coordinates in the source leaves exponentially large fibres for sufficiently large fixed width, as proved below by a counting argument.

## 2. Exact orientation under reversal

Let D(A,C) be the unrestricted vertical domino kernel, with upper A and lower S(C), where S=reverse-complement-inverse. Let A^{-1} denote inverse and let rc denote reverse-complement. Applying rc to the entire two-cell plot changes the upper state to

    rc(S(C))=C^{-1},

and the lower pattern to rc(A)=S(A^{-1}). It preserves1324 avoidance. Hence

    D(A,C)=D(C^{-1},A^{-1}).                                (1)

On a binary shuffle word, this map reverses the word and exchanges upper and lower. Write U and L for these two letters, and let bar(w) denote that operation. No symmetry D(A,C)=D(C,A) is assumed.

## 3. A family of genuine canonical paths

Fix integers W>=3 and R>=1. Let

    J={2,4,6,...} intersect {2,...,W-1},
    a=|J|=floor((W-1)/2),
    V=12,   V^*=12 skew-sum1=231,
    w=ULLU,   bar(w)=LUUL.

The source level walk consists of R consecutive excursions

    1,2,...,W-1,W,W-1,...,2,1,                              (2)

sharing the endpoint level1 between consecutive excursions. It has

    r=R(2W-2)+1

vertices. Every vertex normally carries the state V. Independently for each excursion and each j in J, choose a bit. Put the state V^* at the up-run occurrence of level j if the bit is1, and at its down-run occurrence if the bit is0. The other occurrence carries V. Endpoints and turnaround vertices always carry V.

There are exactly2^(Ra) different state sequences, all of total size

    n=2r+Ra=R(4W-4+a)+2.                                  (3)

Because active levels are nonadjacent, any source edge has at most one endpoint with an extra singleton. Give every source edge the word w, appending U if its upper normalized state is V^*, or appending L if its lower normalized state is V^*. With neither extra, use w alone.

Every such edge is a valid greedy K edge. The only increasing pair within either color is the first pair of its V block: any appended singleton lies after and below that pair. The two first pairs are interleaved ULLU, not the forbidden LULU. Therefore the domino avoids1324. Its highest lower point is the second L of the prefix, bracketed by the two upper points. This is the exact greedy witness. The normalized lower pattern is correct because S(V)=V and S(V^*)=V^*.

The accepted exact homogeneous kernel theorem reconstructs a unique1324-avoider from each path. Distinct bit vectors have distinct canonical state sequences, hence distinct permutations. This is an all-size canonical family, not merely a hypothetical mass profile.

## 4. Folding and all its collisions

Process one excursion. For each level j, concatenate by skew sum its up-run state and the inverse of its down-run state, in that order. The levelW turnaround has only one source vertex, so use both V and V^{-1}=V as separate copies. At level1 use the two endpoints of the excursion. At an endpoint shared by two excursions, each excursion gets a copy. Thus exactly2R-1 source turnaround vertices are duplicated, adding

    2(2R-1)=4R-2                                           (4)

points.

At each active level j the merged state is independent of the bit, because

    (V skew-sum1) skew-sum V^{-1}
        =V skew-sum1 skew-sum V
        =V skew-sum (V skew-sum1)^{-1}.                     (5)

Here inverse reverses the order of skew-sum components. At every inactive level the merged state is V skew-sum V.

For an output edge j->j+1, concatenate its up-run edge word with the reverse-complemented down-run edge word. If neither endpoint is active, the result is w bar(w). If its unique active endpoint has output color X in {U,L}, the up-run word is w X^epsilon, and the transformed down-run word is X^(1-epsilon) bar(w). Their concatenation is always

    w X bar(w),                                            (6)

independent of epsilon. The opposite source orientation on the down run is exactly what makes the new color X agree in the two factors. Nonadjacency of active levels is essential: with two independently active adjacent levels, the two middle colors need not commute.

Concatenate the resulting state blocks and edge-word blocks across all R excursions. The folded state at level j is R skew copies of V skew-sum V, with one singleton inserted between the two V blocks of each copy when j is active. The folded words likewise consist of R copies of(6) or w bar(w). Therefore every one of the2^(Ra) source permutations has exactly the same folded labeled path.

This output is an unrestricted valid D-path. Within any color, an increasing pair stays inside one V block, since all blocks are in skew order and singleton blocks have no increasing pair. The edge words separate different excursion blocks and the two reflected domino pieces, except for the intervening single-color singleton, which belongs to no increasing pair. Thus an interlocked pair of increasing pairs would already occur in w or bar(w), neither of which contains LULU. All edge shuffles consequently avoid1324. Equivalently this follows directly from the two legitimate domino pieces and the absence of any new ascending pair across their skew-sum blocks.

Applying the accepted symmetric guard to every output state and edge makes it a canonical W-cell path and adds2W points. Since that guard is injective, it neither removes nor separates any of the collisions. The common canonical output has size

    N=n+(4R-2)+2W=R(4W+a)+2W.                              (7)

All turnaround copies, their complete patterns, their locations in the folded output and the output boundaries between excursions can be marked identically for every source choice. These are output markings; their original source coordinates need not agree across choices. The collision remains for those output records: the lost bits tell whether an internal trailing singleton came from the up or down occurrence.

## 5. Quantitative information loss

The maximum fibre of this concrete fold, even with the listed folded-output turnaround data retained, is at least

    2^(Ra),
    (1/n)log(fibre) >= [Ra log2]/[R(4W-4+a)+2].             (8)

For each fixed W let R tend to infinity. The duplication overhead relative to n tends to

    4/(4W-4+a),                                            (9)

which tends to zero as W grows. In contrast, the lower fibre-entropy rate tends, as W then grows, to

    log2/9>0.                                             (10)

Thus small turnaround mass does not imply small entropy loss under this map.

One can also retain complete original coordinates of every source turnaround point, including the two endpoints. There are2R+1 source cells at levels1 or W and hence

    m=4R+2

such marked points. Distinct marked cells are at least two cell indices apart because W>=3. The accepted staircase geometry puts them in skew order, and each has pattern12. Their induced pattern is therefore the fixed pattern(12) skew-summed2R+1 times. Specifying their original positions and their original values determines every coordinate pair, because this induced pattern is fixed. There are at most binom(n,m)^2 such records. Their source cell indices in the level walk are already determined by W and R.

Partition the2^(Ra) sources by these records. Some fibre of the fold together with this full source-coordinate record has cardinality at least

    2^(Ra)/binom(n,4R+2)^2.                                (11)

This is a pigeonhole bound, not a claim that the source records are identical for all bit choices. Writing h(t)=-t log t-(1-t)log(1-t), and first letting R tend to infinity with W fixed, its logarithmic rate per original point is at least

    [a log2]/[4W-4+a]-2h(4/[4W-4+a]).                       (12)

As W tends to infinity this lower bound tends to log2/9. It is therefore positive for all sufficiently large fixed W. Recording all original turnaround coordinates still does not make this fold injective or make its worst-case fibre entropy tend to zero with width. Any repair has to encode additional interior information, or exploit a different transformation with a proven recovery rule.

The argument does not say that every possible folding map must have these fibres. In particular, a new encoding might retain and compress interior information in a different way. Nor does it show that the constructed family has nonvanishing probability among uniform1324-avoiders. It only invalidates the specified low-turnaround recovery shortcut.

## 6. Scope and exact inputs

The construction uses accepted inputs only: the exact homogeneous K-path reconstruction, the unrestricted D orientation, and the symmetric D-to-K guard. The source family and its collisions are explicitly proved above. The accompanying finite checker is a regression of the state and word indexing, not the all-size proof.

- pass2_staircase_bias/EXACT_GREEDY_TRANSFER.md, SHA-256 dfbab3a20d05861a7c4aba868b89a225f2ac5db201a467358f015f6efabe2b03.
- pass3_kernel_feasibility/SQUARED_KERNEL_GAP_IMPOSSIBLE.md, SHA-25699e3262041ff09e1ce308fbc5a13704d286602e0eb5af7d814d99915848c314f.
- pass4_window_gaps/FIXED_WIDTH_CALIBRATION.md, SHA-256 f831a975f8757858a6ad2a875d135011068047f49154ec426c66e262e5e3705c.

The original staircase characterization is credited to Bevan, Brignall, Elvey Price and Pantone, Proposition1: https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf . No source theorem is asserted to prove these new folding claims.
