# Independent review of the Crofton partial and its measure convention

**Verdict: PASS_SCOPED_PARTIAL_AFTER_CONVENTION_CORRECTION.** The explicit planar formula is valid on the domain-local line space. The five-point certificate excludes positive hyperplane Crofton measures for curve length on every simplex of dimension at least three. The intended general higher-dimensional ellipsoid characterization remains unresolved. Recommend **unsolved, 2/5**, preserving both source qualifications.

Reviewed on 30 September 2026 by a separate GPT-6 Astra agent at xhigh effort. This is an independent AI review, not human peer review or a novelty certification.

- Originally submitted PARTIAL_RESULT.md: **1801312e32b0e6fd08766e1b5fa73b811df2a5e8464c7943b8dce9a37f996d7a**
- Corrected and fully reviewed PARTIAL_RESULT.md: **afb765a94ecbc7432a9f90ec8f448c33da602fa078e9c605aaebf813f45d319a**

The correction was requested during this review and made by the author. Both snapshots and the exact content diff are retained. No outstanding mandatory correction remains.

## Exact source scope

I read Schneider's [OWR 04/2010 contribution](https://ems.press/content/serial-article-files/46262?nt=1), printed pp. 150–153, and visually checked its final page. For curve length the integrating flats have codimension one. They are lines only in dimension two. The target asks for a positive measure; the earlier allowance for signed measures does not remove this restriction. It is an existence question, with no uniqueness requirement.

The final ellipsoid-only statement omits a dimension restriction. The immediately preceding hypersurface result includes dimension two, where hypersurface area is length. Its contextual discussion of degrees below the hypersurface degree suggests the intended higher-dimensional target, but that inference must remain explicit. The candidate correctly does not turn the planar exception or a simplex-only obstruction into a general higher-dimensional resolution.

I also read the first three pages of Schneider's [polytopal Hilbert geometry paper](https://home.mathematik.uni-freiburg.de/rschnei/Polytopal.Hilbert.pdf) and visually checked its measure definition. The full-logarithm cross-ratio normalization is correct. The paper's positive line measure represents hypersurface area, which is not curve length in higher dimensions.

## Mandatory convention correction, now resolved

The original submitted paragraph claimed agreement with the cited paper's Crofton convention after proving only finiteness over compact subsets of the open triangle. This was insufficient: manuscript p. 3 explicitly describes local finiteness on the entire affine line space. The proposed level-line measure has infinite mass near a boundary-side line in that larger space.

The corrected text defines $H(D)$ to be the open space of lines meeting the open triangle and claims the Radon property there only. This is valid. Each family $p_i=e^tp_j$ is a continuous proper map from $\mathbb R$ to $H(D)$: as $t\to\pm\infty$, its limiting line is a boundary-side line, outside $H(D)$. A compact subset of $H(D)$ consequently has compact parameter preimage, and the pushforward of Lebesgue measure is Radon. The finite sum retains that property.

Equivalently for this construction, lines meeting a fixed compact $K\subset D$ have parameter values among the bounded values of $\log(p_i/p_j)$ on $K$. Conversely, every compact collection of lines in $H(D)$ is covered by finitely many neighborhoods of lines meeting small closed balls inside $D$. This explains the domain-local finiteness statement without confusing the two ambient spaces.

The newly added global obstruction is also correct. The set of affine hyperplanes meeting a fixed compact convex body is compact in the usual unoriented hyperplane parameter space. A globally locally finite positive measure has finite mass there. For each fixed segment, hyperplanes containing the entire segment have zero measure if the finite intersection-count formula holds. The remaining hyperplanes meet the segment at most once. Thus that finite mass would bound the Hilbert length of every segment in the body. But the distance from a fixed interior point along a chord tends to infinity on approaching its boundary endpoint. Global local finiteness is therefore incompatible with positive hyperplane representations of the complete bounded-domain Hilbert metric, including the ellipsoid case.

This establishes a necessary convention distinction. It does not identify the historical author's intended repair. The current artifact explicitly keeps that source qualification and no longer claims a globally Radon planar example.

## Simplex metric and positive planar representation

The direct cross-ratio calculation is correct. For $r_i=q_i/p_i$, the weighted average $\sum p_ir_i=1$ gives $\min r_i<1<\max r_i$ when $p\ne q$. The first boundary hits along $p+t(q-p)$ occur at
\[
A=-\frac1{\max r_i-1},\qquad
B=\frac1{1-\min r_i}.
\]
The cross ratio $B(1-A)/((B-1)(-A))$ is $\max r_i/\min r_i$. This yields the displayed logarithmic variation metric and, by differentiation, the tangent norm
\[
F(p,v)=\max_i(v_i/p_i)-\min_i(v_i/p_i).
\]

For three real entries, half the sum of the three pairwise absolute differences equals their range. Apply this identity first to endpoint logarithmic ratios and then to $v_i/p_i$. Each level of $h_{ij}=\log(p_i/p_j)$ is an affine line. Along any segment, the underlying ratio is fractional-linear with positive denominator; it is monotone or constant. Except at finitely many parameter levels of zero Lebesgue measure, the intersection count is exactly the indicator of the interval between its endpoint $h_{ij}$ values.

Consequently the half-sum of the three pushed-forward Lebesgue measures gives every segment's Hilbert distance. It is positive and Radon on $H(D)$ as above. The triangle is a nonellipsoid, so this is a genuine planar certificate under that precise convention.

For a rectifiable set, use its Euclidean approximate unit tangent $\tau$. The integrand is
\[
F(p,\tau)=\tfrac12\sum_{i<j}|d h_{ij}(p)\tau|.
\]
Each $h_{ij}$ is Lipschitz on a compact interior exhaustion. The standard one-dimensional coarea formula on rectifiable sets gives the desired counting formula on each such piece; a nested exhaustion and monotone convergence handle noncompact or infinite-length sets. The imported coarea theorem has the right hypotheses and multiplicity. For a parametrized curve with repeated traversal, both sides must count that traversal; the candidate expressly separates this from set cardinality. Holmes–Thompson one-dimensional volume agrees with this norm length, also for the stated continuous generalized Finsler metric.

## Hypermetric obstruction: signs and null incidences

For a positive hyperplane measure representing finite interior segment lengths, all hyperplanes through a fixed interior point have measure zero. Choose centered segments shrinking to that point. Their lengths tend to zero by local continuity of the Finsler norm, while every hyperplane through the point contributes at least one to each count. Positivity bounds the measure of that hyperplane set by each shrinking length.

For finitely many prescribed points, almost every hyperplane therefore avoids all of them. Its intersection with a pairwise segment is one precisely when the endpoints lie in opposite open halfspaces. For integer weights with total one, a cut with side weight $s$ contributes
\[
\sum_{i<j}b_ib_j\,\mathbf1_{\text{separated}}=s(1-s)\le0,
\]
because $s$ is an integer. The finite signed sum is integrable since every individual pair distance is finite. Integration against a positive measure preserves the inequality. No analogous conclusion follows from a signed measure. Endpoint or segment-containing hyperplanes cannot supply a hidden positive contribution because their relevant incidence sets are null.

## Five rational points in every dimension at least three

The five exponent vectors use three varying coordinates and at least one further coordinate fixed at zero. That fourth coordinate is essential: it keeps the all-zero vector and $(1,1,1,0,\ldots)$ distinct after projective normalization. The submitted restriction $n\ge3$ guarantees it.

Normalize their coordinatewise powers of two to obtain five distinct rational interior points. Logarithms of the normalizing constants cancel from the maximum-minus-minimum distance. Among the three middle points, all distances are $2\log2$. Every other off-diagonal distance is $\log2$.

With weights $(-1,1,1,1,-1)$, the total weight is one. The three middle-middle pairs contribute $6\log2$, the pair of negative-weight points contributes $\log2$, and their six pairs with middle points contribute $-6\log2$. The sum is therefore
\[
\log2>0.
\]
This violates the necessary cut inequality and excludes every positive hyperplane Crofton measure representing all segment lengths on these higher-dimensional simplices, including any domain-local Radon measure. The argument does not require global local finiteness.

There are ten pairwise distances and every product of the selected weights has absolute value one. The claimed perturbation margin follows from the triangle inequality: errors of magnitude less than $\varepsilon$ in each distance change the certificate by less than $10\varepsilon$. This is a metric statement conditional on actual distance control, not a general assertion about perturbed domains.

## Verification and remaining target

The corrected artifact's unchanged author checker passes **92,660** assertions and reproduces its updated receipt byte for byte. Its receipt changed only because the reviewed artifact hash changed. My independently written standard-library checker passes **1,401** exact assertions: it tests multiple integer cut weights, computes boundary hits directly along affine chords, verifies rational cross-ratio products in several dimensions and bases, and checks planar incidences and the tangent identity. The analytic statements about measures and coarea are reviewed above, not inferred from those controls.

The positive planar representation is now precisely qualified. The higher-dimensional simplex obstruction is rigorous but does not classify all nonellipsoids. No argument is supplied that every nonellipsoid contains an isometric simplex or the five-point metric. Thus the intended general target remains **unsolved, 2/5**. No novelty or human peer-review claim is warranted.

The ten publication files, including the original snapshot, corrected snapshot, exact diff and reproducible checks, are listed in review_summary.json. Source PDFs, rendered pages and redundant stdout captures are not publication files.
