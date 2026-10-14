# PASS5 supplemental structural acceptance

14 October2026. The seven-note main audit and receipt remain frozen. Both supplements are accepted at the exact pins below, with their explicit limited scopes.

## 1. Near-empty pairs with escaping canonical cell indices

Reviewed `pass5_pair_rectangles/NEAR_EMPTY_PAIR_OBSTRUCTION.md`, SHA-256
`5b226d59b9d751ff1923c1957187c523d5425e2f1f224432c0ddf918e121da0c`.

**Accepted in full.** This is a deterministic insufficiency result, not a uniform-probability statement.

The simple direct-sum example is valid. Within each increasing block the open rectangles are chain segments; cross rectangles contain only the earlier points of the upper endpoint's increasing block. Thus every rectangle is increasing and1324 is avoided. A cross rectangle is empty exactly at a block's first entry, giving k^3 cross covers; internal consecutive entries give k(k-1) further covers.

For the canonical reinforcement, D_a=12 skew-sum J_(a-2) is fixed by S, has exactly one ascent pair, and avoids213. The state A_k=1 direct-sum Q_k also avoids213: its first minimum cannot be in a213 occurrence, while a skew sum of increasing blocks has none. Its internal covers are the k edges from the first minimum to the first entry of each block and the k(k-1) consecutive block pairs, totaling k^2.

The ordinary and first special edges use the accepted ascent bridge with the correct maximum positions. The second special word U L^(k^2) U^(k^2) is also genuine: all lower points are consecutive, so no lower-upper-lower-upper1324 is possible. The other color distributions are excluded by the two cell classes. The highest lower point lies after the first upper and before a larger second upper, so greediness holds. Exact path reconstruction therefore supplies the stated canonical states, not merely a possible staircase gridding.

For a word U L^b U^(a-1), the first upper is before either endpoint of every cross increasing pair and cannot lie in its open rectangle. Empty cross rectangles correspond precisely to a lower endpoint with no later larger lower point and an upper endpoint with no earlier smaller point in the upper suffix. Other cells cannot enter by rectangle locality. Consequently the first special edge has k^2-1 empty pairs and k^4-1 total pairs; the second has k(k^2-1) empty pairs and k^4 total pairs. On an ordinary edge only the first two lower points precede the upper suffix. The first lower point has the second lower in every such rectangle, while the second lower gives an empty rectangle because the upper suffix is decreasing. Its counts a-1 and2(a-1) are exact.

There are4s D states. Summing the ordinary source sizes gives3k^2-4s-4 after subtracting one per ordinary edge. Adding internal and special-edge counts gives exactly

    Z_0=k^3+5k^2-k-5,
    Inc=2k^4+(k^3+13k^2)/2-4s-9,
    n=5k^2-3.

An increasing chain can meet at most two adjacent cells. Thus LIS<=k+3 and every open increasing-pair interior has at most k+1 points. Fixed initial and terminal numbers of cells have bounded mass, while central mass is macroscopic. The three threshold assertions are consequently sound: exactly empty counts vanish after n^2 normalization, but counts up to the sublinear threshold k+1 and then up to any fixed positive mass threshold retain limiting density2/25. Small LIS and few exactly empty rectangles do not imply few near-empty pairs.

Independent full reconstruction, greedy peeling, and inspection of every increasing-pair rectangle passed for k=2,4,8. The tuples (n,Inc,Z_0) were (17,49,21), (77,631,135), and (317,8843,819). Observed LIS values were4,6,10 and maximum interiors2,4,8, within the proved conservative bounds. The checker uses explicit errors rather than removable assertions and gives identical normal, -O and -OO JSON output. These finite checks do not replace the preceding all-size reasoning.

## 2. Monotone staircase comparison and quadratic true gaps

Reviewed `pass5_collective_windows/QUADRATIC_STAIRCASE_BARRIER.md`, SHA-256
`e7eafa29aa64acc8be095e8177da1dd987724c859c555d932b47cbdfa0580b10`.

**Accepted in full as a comparison model only.** It supplies no rate estimate on actual1324 finite-width gaps.

For the descending staircase with decreasing cells, each neighboring binary word fixes the only free relative order in its shared row or column. Row words specify value order; column words specify position order. Incident edges constrain different coordinates of their shared cell, and its prescribed decreasing pattern matches those orders. Thus arbitrary neighboring words are simultaneously realizable and uniquely determine a gridded permutation. Empty cells are allowed. This verifies the exact product-binomial count without imposing canonical greediness that the model does not require.

Each increasing chain meets at most two adjacent cells and at most one point from each, so every resulting permutation avoids123. For the converse I directly inspected the primary Albert--Brignall--Ruskuc--Vatter manuscript, Section2, PDF page4. It states and constructs increasing-cell staircase griddings for every321-avoider. Complement changes its up/right staircase to down/right with the opposite first direction; composing with anti-diagonal reflection gives exactly the present first down, then right convention. Equivalently the combined coordinate map is (x,y)->(y,1-x). It maps321 to123 and increasing cells to decreasing cells. Therefore the union of the model is Av(123), with Catalan growth four.

The first K-cell support has K-1 total internal horizontal and vertical grid lines. Choosing their gaps among n+1 possible gaps bounds the number of labeled griddings of a fixed permutation by (n+1)^(K-1), including empty rows or columns. Thus fixed-K gridded and ungridded growth coincide. This is a polynomial bound for fixed K; no uniform-in-growing-K conclusion is inferred.

The displayed sine vector is positive and normalized. The sine recurrence gives the two adjacent sums exactly, including the boundary values x_0=x_(K+1)=0. Each entropy derivative equals log(rho_K^2). At an endpoint the artificial E(0,x) term has zero derivative, so the formula is correct; K=1 gives growth one. Concavity establishes global maximality, and homogeneity supplies the attained value. Integer rounding at fixed K changes the exponent by only O_K(log n). Hence h_K=4cos^2(pi/(K+2)) is exact, and its relative gap is pi^2/(K+2)^2+O(K^-4), a summable sequence.

I also directly inspected Bevan's primary manuscript, Theorem3.6, which states the general squared spectral-radius formula. The note does not need an unproved specialization of that theorem, since its own exact entropy derivation fixes the width convention. The primary sources checked were:

- Albert, Brignall, Ruskuc and Vatter, *Rationality For Subclasses of321-Avoiding Permutations*, Section2, PDF p4: https://www.rbrignall.org.uk/papers/av321.pdf
- Bevan, *Growth rates of permutation grid classes, tours on graphs, and the spectral radius*, Theorem3.6: https://oro.open.ac.uk/38963/1/GrowthRatesRevision3.pdf

The source-supported claims above are confined to the staircase existence, Catalan enumeration, and general grid-class theorem. The supplemental note's exact calculation supplies its own claimed example. A summable gap in this different model does not show that actual1324 gaps are summable, nor does failure of a sufficient criterion imply a failed permuton limit.

## Final scope

The main seven-note acceptance plus this two-note supplement constitute the final structural review for PASS5. No additional mathematical variant is requested or needed. The uniform1324 and universal fixed-alpha limits remain unresolved. The surviving missing estimates concern actual completion-weighted mass, including all near-empty thresholds and unbounded-width state profiles.
