# Independent original-source scope audit: PR218 / 30006020

Audit completed 2026-10-15 UTC. Frozen submitted author proof SHA256: `f1d43a7f4ae54e6c3ac8318cac8f2106b937d4657101bdd3a9b91523e0e5de4b`. Parent-supplied PR head: `dc457c741c779fbf90fbfdcdc73f750b3716f561` (not independently queried, and no Git/provider mutation performed).

## Outcome

**No ensemble or limit-order substitution is established by the title “principal quadratic” or “iterated.”** On the most definite contextual reading of the original Problem 2, those are the native settings. The candidate is an honest restricted result if someone chooses the broader all-strata interpretation; the original Problem 2 does not itself install that all-strata quantifier.

**Conditional scope adequacy:** If the candidate's Theorems A and B are mathematically valid, they answer the exact illustrative window and provide a coherent entire-multiset approximation for that native setting. This is not merely a mean for one arbitrarily selected example. Total variation for the full multiset is a meaningful all-scale distributional statement; Theorem B additionally states every intermediate scale and compact-window moments. This audit verifies the geometric and notation bridges relevant to that comparison, not every analytic step of Theorems A and B, and makes no overall mathematical acceptance or novelty determination.

**One real source-consistency caveat remains:** the original workshop summary's microscopic factor is 4g−4, whereas the final published simplex formula underlying the candidate has Gamma total 6g−6. The candidate openly notes and avoids relying on that workshop microscopic assertion. The discrepancy does not change the intermediate [1/√g,2/√g] target or the scale-invariant mesoscopic intensity. However, a promotion claiming literal recovery of every printed endpoint theorem would need to acknowledge or reconcile it. This audit does not silently declare the workshop line corrected.

## Independence and evidence discipline

[The source-scope freeze](SOURCE_SCOPE_FREEZE.md) was written before any candidate material was opened. It records the complete original contribution read, the exact formal target, alternative source interpretations, and acceptance criteria. The first candidate read was completed at 06:11:15 UTC, after the freeze at 06:10:20 UTC. File modification time and hashes are recorded in [the provenance file](SOURCE_READ_PROVENANCE.json).

I subsequently read exactly the requested submitted `CANDIDATE.md`, `FINAL_DISPOSITION.md`, `SOURCE_AUDIT.md`, `TARGET.json`, and the URL/hash `source_manifest.json`. The disposition's inherited acceptance label was encountered because the parent explicitly required reading that file. It is not evidence in this audit. No `independent_review`, parent/sibling conclusions, sibling audit folders, chat coordination, or outside individuals were accessed. No Git index/ref, provider, queue, candidate, paper, upload, or status mutation was performed.

The only OWR source paraphrase is in the freeze; that summary is below 200 words. The original mathematical comparisons below are auditor deductions. Full PDFs, extraction text, and rendered pages are under ignored `private/` and are excluded from the safe authored manifest.

## Exact scope comparison

| Dimension | Frozen source interpretation | Submitted claim | Audit finding |
|---|---|---|---|
| Random object | Isomorphism classes of square-tiled surfaces at a fixed stratum and square-count bound | Half-translation square-tiled surfaces in Q(1^{4g−4}), with at most N squares | Same native objects |
| Holonomy | The known theorem immediately controlling Problem 2 is quadratic principal | Quadratic principal, no other strata asserted | No Abelian substitution |
| Genus | Genus g of the base Riemann surface carrying the quadratic differential | Same g | No orientation-cover genus switch |
| Direction | A cylinder decomposition in a chosen coordinate direction; the preceding theorem treats the pair of horizontal/vertical marginals | Horizontal; identical vertical marginal | Sufficient for the displayed count question; no all-directions or simultaneous pair claim needed |
| Area | Cylinder area divided by total surface area; multiplicities retained | Same, each maximal cylinder counted once | Same normalized statistic |
| Sampling weights | Uniform fixed-bound classes; inverse automorphism weighting has the same limit | Explicitly either convention in the N→∞ limit | Same limiting law; not a claim of finite-N equality |
| Limits | N→∞ first at each fixed g, then g→∞ | Exactly that order | No interchange or missing diagonal theorem |
| Cylinder heights | No cutoff in the source's fixed-stratum sampling | m=∞ in DL | Correct unrestricted choice |
| Primitive objects | No primitive covering restriction | None | No primitive-torus-cover or height-one restriction |
| Particular window | [g^−1/2,2g^−1/2] in the normalized area | Poisson(log 2/2), mean and variance log 2/2, iterated limits | Exact same window; proof validity remains for the mathematical audit |
| Intermediate scales | The source asks for what lies between known end regimes | Every s_g→0 with g s_g→∞, for compact windows after dividing area by s_g | More than the one illustrative scale |
| Full spectrum | Unspecified rigorous mode; coherent full-law model is a defensible success criterion | Entire-multiset total variation approximation, plus the intermediate laws | Adequate on the native reading, conditional on Theorem A |
| Arbitrary strata | Mentioned in surrounding conjectures, not expressly universally quantified in Problem 2 | Explicitly excluded | Honest boundary; any all-strata claim would exceed what is proved |
| Diagonal N(g) | Separate Problem 3 | Explicitly excluded | Not part of this target |

## Primary bridge checks

### DL final edition: short source register

Delecroix–Liu, *Length partition of random multicurves on large genus hyperbolic surfaces*, JEMS 27 (2025), 5093–5131; [publisher PDF](https://ems.press/content/serial-article-files/51451?nt=1), DOI [10.4171/JEMS/1469](https://doi.org/10.4171/JEMS/1469). Pages 5096–5097 define the surface model and Theorem 1.4. Pages 5102–5107 define F, Y, Z, the weighted graph mixture, and its law. Pages 5116–5118 give the uniform coefficients and positive monomial expansion. The surface law uses normalized horizontal-cylinder areas and a bound m on maximum height. The weighted multicurve component length includes its multiplicity. This register is below 200 words; the algebra below is independently checked from those formulas.

For m=∞, there is no height restriction. A multicurve component is one isotopy class carrying an integer weight, rather than one new component per unit of weight. On the surface side the associated object is a single maximal cylinder, with that weight encoding the number of horizontal square bands. Thus “counted once” in the candidate is the correct statistic; counting each square band as another cylinder would not be.

The final DL conventions fix the potential automorphism issue: F itself does not include the graph automorphism factor, while the mixture divides by it. A one-vertex k-loop graph has 2^k k! automorphisms. In the positive monomial expansion, the exponents are 2j_i−1 and Σj_i=3g−3. Dividing the monomial simplex integral by its factorial denominator gives a factor 1/(2j_i); the sum over unbounded heights gives ζ(2j_i). Therefore the candidate's assembly weights ζ(2j)/(2j) are the weights produced by this bridge, not an unexplained change to an Abelian assembly.

The conditional monomial density is proportional to ∏x_i^{2j_i−1} on Σx_i=1. Its Dirichlet parameters are 2j_i, with total 2Σj_i=6g−6. The simplex measure is ordinary coordinate measure on the hyperplane; no extra Euclidean √k factor belongs in this calculation. The rendered equations, not only extracted text, were checked.

### DGZZ final edition: short source register

Delecroix–Goujard–Zograf–Zorich, *Large genus asymptotic geometry of random square-tiled surfaces and of random multicurves*, Inventiones 230 (2022), 123–224; [author-hosted final publisher PDF](https://webusers.imj-prg.fr/~anton.zorich/Papers/Large_Genus_Asymptotic_Geometry_2022_Inventiones_published.pdf), DOI [10.1007/s00222-022-01123-y](https://doi.org/10.1007/s00222-022-01123-y). PDF pages 7–10 define the no-simple-pole holomorphic surface ensemble, its fixed-genus sampling, and the cylinder-count correspondence. Pages 23–28 give the square size, strata, principal-stratum counting, and graph-volume construction. Theorem 1.12 on PDF page 15 concerns the same count law; Theorem 5.2 on page 83 gives uniform low-cylinder-number estimates. This register is below 200 words; comparisons below are auditor deductions.

DL's Q_g(Z) includes all holomorphic quadratic square-tiled surfaces. The OWR theorem and candidate specify the principal stratum. This difference is harmless only after the fixed-g square-count limit, and that is exactly the order being used. The principal stratum is the open dense top-dimensional stratum. At fixed g there are finitely many singularity partitions, and nonprincipal strata have smaller complex dimension. Their lattice-count orders are lower, hence they have vanishing probability in the total holomorphic lattice count. DGZZ explicitly states the negligible nonprincipal contribution on PDF page 24. The displayed sentence prints lowercase n→∞ in that clause, although its surrounding formula and paragraph concern the square-count limit N→∞; I do not reinterpret it as a theorem about a growing number of poles.

Zero labeling does not introduce a new area distribution: at fixed g the number of principal simple zeros is fixed. Automorphism-weighted labeling multiplies each class by the same factorial; the workshop's equality of limiting weighted/unweighted laws deals with the difference for uniform classes. Nothing here establishes uniformity in growing g before taking N→∞.

DGZZ takes 1/2-by-1/2 squares, while DL and the report use unit squares. Scaling every surface by 2 identifies their combinatorial tilings, multiplies every area by 4 and every height by 2, and leaves every ratio area(cylinder)/area(surface) unchanged. Constant rescaling of a cutoff also leaves an N→∞ limiting law unchanged. The unrestricted m=∞ selection makes the height-unit difference immaterial. This cannot account for a difference between factors 4g−4 and 6g−6 after normalizing by total area.

## Boundary and adversarial interpretations

1. **Does “quadratic” mean the square of an Abelian differential?** No. In Q(1^{4g−4}) every zero has odd order; a global square of a holomorphic Abelian differential has only even-order zeros. The principal quadratic stratum is therefore not the Abelian sampling ensemble.

2. **Could g mean the genus upstairs?** No such change appears in either correspondence. As a check, the orientation double cover of a principal quadratic surface branches at its 4g−4 simple zeros and has genus 4g−3 by Riemann–Hurwitz. Using that genus as g would be a different parametrization. The candidate consistently uses the base genus.

3. **Could “full spectrum” require every stratum?** This is a possible broader research ambition, not an explicit quantifier in Problem 2. It must be recorded as an interpretation rather than used to replace the contextual ν_{2,(1^{4g−4})} with an unannounced universal statement. The native principal-quadratic answer can be promoted only under its displayed scope.

4. **Could “full” mean only the sample window?** The word “example” makes that too narrow as a sole claim of completeness. Here Theorem A provides an explicit full random multiset law up to total variation, and Theorem B handles every intermediate rate. Their combination is a reasonable interpretation of full-spectrum description. It does not promise uniform relative errors for events whose probabilities vanish, nor all unbounded statistics at arbitrary microscopic scales. Total variation controls absolute probabilities of arbitrary measurable observations, even observations depending on g. Moment convergence requires additional arguments; the candidate does provide separate ones for intermediate compact windows.

5. **Does weak fixed-g convergence justify the moving-g count?** For each individual g, the endpoints are fixed numbers during N→∞. The exact mixture has simplex densities when there are at least two cylinders, and its one-cylinder atom is at area 1. For g≥5 both requested endpoints are below 1 and have zero boundary mass. The count is bounded by 3g−3 at that fixed g. Consequently the fixed-g count probabilities and moments pass to ν_g before g is changed. No quantitative finite-N rate or interchange is hidden in that inference. The g=4 upper endpoint equals 1, but that isolated finite genus does not affect the large-genus theorem.

6. **Does the source demand horizontal/vertical joint independence at large genus?** The preexisting fixed-genus theorem gives a product limit. A single-direction count answers the stated example. The candidate disclaims a new pair assertion, so it does not lose an expressly requested new conclusion. It also does not claim all slopes at once.

7. **Could area normalization absorb the microscopic discrepancy?** No. Both descriptions require the area multiset to sum to 1. Scaling square units cancels in those ratios; using cover area inconsistently would break that convention. The problem's [1/√g,2/√g] endpoints are fixed exactly as written in the candidate.

## Checkable microscopic compatibility calculation

This calculation is an endpoint falsification check on the claimed *model*, not a new attempt to solve the research problem or a replacement target.

Write n=3g−3, a_j=ζ(2j)/(2j). In the candidate's ideal model, a part of fixed size j has asymptotic expected multiplicity a_j, and its unnormalized Gamma mark has density e^{−y} y^{2j−1}/(2j−1)!. The resulting small-mark intensity is

    f(y) = Σ_{j≥1} a_j e^{−y} y^{2j−1}/(2j−1)!
         = e^{−y}/y · Σ_{j≥1} ζ(2j)y^{2j}/(2j)!.

The total Gamma parameter is 2n=6g−6, so (6g−6) times normalized model area has that natural intensity. At the workshop's printed scale x=(4g−4)area=(2/3)y, the same model instead has transformed intensity

    (3/2) f(3x/2)
      = e^{−3x/2}/x · Σ_{j≥1} ζ(2j)(3x/2)^{2j}/(2j)!.

These are not equal: as x→0, f(x)~ζ(2)x/2 while (3/2)f(3x/2)~(9/4)ζ(2)x/2. No area-unit convention fixes this factor because the inputs are already normalized ratios. The conditional Dirichlet total parameter alone is not a full proof of a microscopic point-process limit; the intensity calculation additionally uses the model's fixed-part factorial formula. The usual exponential Gamma tails justify truncating the fixed compact mark interval before letting j grow. This establishes the model's normalization incompatibility, not an externally sourced correction to the workshop statement.

The discrepancy is immaterial to a ratio-window limit governed by dx/(2x), which is invariant under a fixed positive dilation. It is material to an unqualified assertion that the entire-multiset model recovers the literal microscopic formula printed in the report. The candidate explicitly does not make that endpoint claim. I found no basis in the inspected originals to force the displayed mesoscopic question into a different ensemble just to reconcile this factor.

## Strongest verified result and exact remaining gap

Strongest source-scope result: the candidate's ensemble, normalized area statistic, one-cylinder-per-maximal-component convention, unrestricted heights, base genus, and iterated limit agree with the definite native setting of the original Problem 2. The all-holomorphic quadratic correspondence can be restricted to the principal stratum at fixed genus, without a hidden uniform-in-genus inference. Neither all Abelian/quadratic strata nor the diagonal N(g) problem is an explicit missing quantifier in that native setting.

Exact remaining gaps: (a) this scope audit does not independently certify every proof estimate needed for the candidate's total-variation or mesoscopic/moment theorems; (b) the microscopic factor discrepancy remains unresolved as a source-consistency matter and must not be concealed by calling 4g−4 and 6g−6 identical conventions; (c) an all-strata generalization, finite-N uniformity/diagonal limit, rare-event relative errors, and arbitrary microscopic moments would require distinct additional claims and proofs; (d) novelty/priority work was deliberately deferred as instructed.

The appropriate use of this report is therefore: reject a scope objection based only on the candidate's “iterated principal-quadratic” title; retain its explicit restrictions; and carry the stated endpoint caveat into any later full-source consistency or promotion decision.
