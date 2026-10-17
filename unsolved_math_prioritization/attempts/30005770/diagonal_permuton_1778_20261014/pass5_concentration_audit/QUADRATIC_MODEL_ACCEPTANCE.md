# Independent analytic acceptance: the monotone staircase comparison model

Final shared PASS5, 14 October 2026.

Reviewed: `pass5_collective_windows/QUADRATIC_STAIRCASE_BARRIER.md`, SHA-256 `e7eafa29aa64acc8be095e8177da1dd987724c859c555d932b47cbdfa0580b10`.

**Accepted as a comparison-model theorem.** It does not give the actual 1324 window gaps.

For fixed cell sizes, decreasing cells have unique internal patterns. Each adjacent row or column order contributes its binary-shuffle factor, and the monotone staircase reconstruction gives the displayed product. Allowing empty cells is essential for this gridded count. A fixed ungridded permutation has at most(n+1)^(K-1) placements of the dividing lines, so fixed-K exponential growth is unchanged upon forgetting its gridding.

The upper entropy bound follows by summing over at most(n+1)^K size vectors. At the stated positive maximizing vector, rounding to integer counts and Stirling's formula give a matching lower bound with O_K(log n) error. K is fixed throughout this step; those errors are not discarded uniformly in an increasing K.

With theta=pi/(K+2), the sine recurrence gives the two neighboring-sum identities exactly, including both endpoints. Differentiating the sum of edge entropies gives log[(x_(j-1)+x_j)(x_j+x_(j+1))/x_j^2], with the zero endpoint contribution interpreted continuously. Every coordinate derivative at the proposed positive vector equals log(4cos^2 theta). Concavity gives a global maximum; degree-one homogeneity then identifies its value. The K=1 case gives growth one, as it should. Thus h_K=4cos^2(pi/(K+2)) is exact under the stated width convention.

Every decreasing-staircase permutation avoids 123, because a three-point increasing chain could neither use two points of one cell nor use three pairwise adjacent distinct cells. The cited monotone staircase gridding supplies the converse. The growth of the full union is also consistent directly with the exact h_K approaching four and the Catalan upper bound for Av(123); no uniform-in-K multiplicity estimate is required for the fixed-width calculation.

The true model gap relative to growth four is -2log cos(pi/(K+2)). Taylor expansion gives pi^2/(K+2)^2+O(K^(-4)), hence a summable sequence of positive gaps. This is a concrete failure of any inference that path-shaped staircase geometry and positive boundary shuffle counts alone force a harmonic lower gap. It neither proves summability of the actual 1324 gaps nor rejects the conditional adaptive theorem; it also makes no probabilistic nonconvergence claim.

The complementary structural review covers the gridded model and source-based staircase correspondence. The entropy maximization and fixed-K limit above are independently checked here.
