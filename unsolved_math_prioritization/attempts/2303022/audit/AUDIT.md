# Independent adversarial audit: Problem 2303022 / rank 572

Audit date: 4 October 2026 (UTC). Scope: the frozen local checkpoint, its analytical partial results, source scope, exact controls, and numerical disclaimers. This is an independent AI-assisted audit, not expert peer review or a proof of the sharp target.

## Verdict

**Frozen bundle: correction required. Corrected bundle: PASS as an unresolved, non-sharp research checkpoint.** The correction is confined to the connected-theorem convention in Section 3 and explicit hypotheses in Section 6. `corrections.patch` and `corrected-proof.md` supply the exact repaired text. Neither the frozen files nor any remote repository was changed.

All 27 exact controls replayed successfully, with output identical byte-for-byte to the frozen JSON. The optional finite-difference script also replayed byte-for-byte. These runs do not establish the analytical lemmas or certify a continuum PDE solution. The universal partial bound and the positive-escape construction survived independent analytical checking. The finite-component bound remains conditional on the published connected theorem, whose full proof was not independently retrieved or reverified.

The sharp supremum for arbitrary radial-covering closed obstacles remains unresolved in this attempt. No novelty, improvement over Hall-type literature, exhaustive current-status finding, or sharp extremizer is certified. The five recorded approaches do not collectively supply a missing sharp comparison theorem.

## 1. Identity, freeze, and scope

The supplied public manifest has SHA-256:

`b5ab673a48038729e817852896c54a8467857461d280acc703f8df7c2bcd2903`

All nine entries passed `sha256sum -c SHA256SUMS` before review. The frozen proof has SHA-256:

`b479cff5a77b7f6f316d6b49efb62cf59df4ff2d0c2893642cb79fbbb19fc053`

The original source PDF was independently inspected in text and in a rendered image of printed page 67. Its SHA-256 matches the dossier's `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`. The typography distinguishes the domain D from the unit disk. The obstacle is not being placed inside its own complementary open domain.

The target's outer-boundary requirement matters for candidate lower constructions. It does not invalidate a universal upper estimate proved for a larger class. The two-arc construction has a connected complementary domain reaching the entire outer annulus, so it satisfies the relevant requirement. The connector example's final Jordan barrier does not, and the proof correctly labels that set as a diagnostic example rather than a second admissible target competitor.

A domain containing 0 automatically gives positive clearance from its inner boundary near 0. The relative-closed formulation is a stated generalization, handled by compact exhaustion. For that formulation the intended Brownian convention is the pre-exit obstacle hit: Brownian motion is killed at the unit-circle exit, and escape is its complementary event. Making this convention explicit would improve Section 1's presentation; all substantive estimates concern this pre-exit event. This audit does not claim a separate counterexample to the intended convention.

## 2. Required correction: boundary contacts in the cited theorem

The frozen Section 3 asserted the connected theorem for a continuum K in the closed unit disk while using Section 1's notation

`h(K) = P_0(tau_K < tau_T)`.

Those conventions cannot simply be mixed. Take a nondegenerate closed arc K contained in T. Then no path can hit K strictly before its first hit on T, so the displayed h is zero, while the projected angular measure is positive. Thus the frozen statement, literally read under that definition, is false. This is a scope/definition defect, not a disproof of Marshall--Sundberg's theorem.

The exact patch uses only its interior-obstacle consequence: K is a compact continuum contained in U minus {0}. It explicitly distinguishes the source's boundary-harmonic-measure convention. It attributes sharpness to the source theorem rather than separately proving sharpness for this restricted class. Section 6 now states the same interior condition explicitly.

That repair is sufficient for every actual use of the cited inequality in the dossier. Each K_j in Section 6 is a compact subset of the interior obstacle E, hence lies strictly inside U and avoids 0. No boundary-contact theorem, limiting equality case, or assertion about infinitely many components is needed there. The universal Green-potential bound does not use the connected theorem at all.

## 3. Green-potential proof: independent checks

### Selector and measure

For compact K in the annulus 3/4 <= |w| < 1, its radial projection A is compact. The minimum radius on each fiber exists. If angles converge, a subsequence of the minimizing radii converges; closedness puts its limit in the limiting fiber. Hence the minimum-radius selector is lower semicontinuous, and therefore measurable. Its radius has a uniform upper bound R < 1. Consequently the measure obtained by weighting angular measure by 1/(-log r) is finite and supported on K.

The potential V is nonnegative. It is harmonic off K because the Green kernels and their local derivatives are uniformly controlled on compact sets away from K. Its value at 0 is exactly |A|. Uniform vanishing at T follows from compact support away from T, including the bounded density factor. The logarithmic singularity at a selected point does not create an angular atom.

### Kernel envelopes and constants

I independently checked the identity

`g(s,r exp(i phi)) = (1/2) log(1 + (1-s^2)(1-r^2)/|s-r exp(i phi)|^2)`.

For s <= 1/2, r >= 3/4 gives distance at least 1/4. Using log(1+x) <= x and -log r >= 1-r gives a kernel bound of 16, and thus V <= 32 pi.

For s > 1/2, set a=1-s, t=1-r, and c=3/(2 pi^2). The exact denominator is `(a-t)^2 + 4sr sin^2(phi/2)`, which is at least `(a-t)^2+c phi^2` for |phi| <= pi. The numerator is at most 4at. Each of the three stated envelopes has the correct direction:

- t <= a/2: `(a-t)^2 >= a^2/4`;
- t >= 2a: `(t-a)^2 >= a^2`;
- a/2 < t < 2a: `1/(2t) <= 1/a` and `4at <= 8a^2`.

Summing the envelopes is legitimate even though their regimes differ with angle. Their whole-real-line integrals are respectively `4 pi/sqrt(c)`, `2 pi/sqrt(c)`, and `4 sqrt(2) pi/sqrt(c)`. The logarithmic integral is finite; its value follows by differentiation with respect to the positive scale parameter, with the zero-scale limit justified by scaling. The rational bound `4510/147 < 32` correctly closes the comparison with 32 pi. The singular value at phi=0 lies on an angular null set and does not invalidate the integral bound.

### Stopping, irregular points, and exhaustion

One can localize in the origin component of U minus K and stop on a smooth exhaustion. The bounded nonnegative harmonic martingale has a limit, with expectation preserved by bounded convergence. At exits on T that limit is zero; on hits of K it is at most 32 pi. Continuity of V at every irregular boundary point is not required for this inequality. Thus `|A| <= 32 pi h(K)` is justified.

For relatively closed E, each `K_m=E intersect {|z|<=1-1/m}` is compact and away from 0. Its angular projections increase to the entire circle. Continuity from below of angular measure and monotonicity of pre-exit hitting probabilities suffice. One does not need to assert continuity of harmonic measure at every boundary point, nor to prove equality between a limit of hitting probabilities and h(E). The result is the stated nonsharp `h(E)>=1/16` and escape bound `q(E)<=15/16`.

## 4. Full power pullback: branch point and coverage

The proof pulls back the whole compact set under z -> z^n. It does not independently shift each point radially. The inverse image K' is compact inside U, avoids 0, and for large n lies in |z| >= 3/4.

The branch point at the starting point is not an obstruction. By Itô's formula, the two real coordinates of `B_t^n` are continuous local martingales with common quadratic-variation clock

`A_t = integral_0^t n^2 |B_s|^(2n-2) ds`

and zero cross variation. Almost surely this clock is strictly increasing on nontrivial time intervals, despite its zero instantaneous derivative at t=0 when n>1. Before disk exit it is finite. The analytic image with this clock is planar Brownian motion. The image is inside U exactly while the original path is inside U. Hits of K correspond exactly to hits of K', proving equality of the pre-exit hitting probabilities. This reasoning handles noninjectivity and does not rely on an unsupported assertion that arbitrary radial relocation preserves harmonic measure.

The full n-fold angular inverse image preserves normalized Lebesgue measure: split the angular integral into n equal sectors and substitute the multiplied angle. Thus the projected angular measures agree. The pullback argument validly transfers the near-boundary bound to every compact interior K.

## 5. Topology and positive escape

A compact one-point-per-ray selector maps continuously and bijectively to the circle, so the inverse is continuous. Its radius is positive and bounded below 1. This is an embedded radial Jordan curve surrounding 0; any path to T must cross it. The compactness hypothesis is genuinely doing work. The proof does not misuse the measurable selector from the potential construction as a closed replacement obstacle.

For the two semicircles, the three-piece path has the claimed obstacle clearance 1/8 and outer-circle clearance at least 1/4. The middle semicircle stays at radial distance 1/8 from each obstacle circle; the two vertical pieces lie in the complementary half-planes relevant to the arcs. These checks include the arc endpoints. Open balls of radius 1/8 remain in the domain even where equality of clearance occurs.

The six plus nineteen plus six subdivision gives 31 links, each of length <=1/16. Harnack's disk factor is `(R-d)/(R+d) >= 1/3`. The annular comparison at 3i/4 gives `log(3/2)/log 2 > 1/2`. Harnack may be applied first to the nonnegative harmonic escape function; positivity at the terminal point then propagates, so the reasoning does not assume the desired positivity circularly. This proves `q(E)>1/(2*3^31)`.

Adding the two stated real connectors makes a Jordan curve encircling 0. Escape falls to zero. Obstacle monotonicity has the stated direction, so connectedification cannot prove the desired universal upper escape bound by applying an upper bound to the enlarged obstacle.

## 6. Finite components and rectangle

The finite-component event proof uses unrestricted Brownian motion up to disk exit rather than killing the motion on the first different component. Therefore the union event is exactly the obstacle-hit event, and the pointwise inequality `sum 1_Aj <= k 1_union` is valid even with overlaps. The projection cover supplies `sum |p(K_j)| >= 2 pi`. Under the corrected compact-interior connected premise this yields `h(E)>=C_conn/k`.

No step makes an infinite-component inference. Angular disjointness does not imply hitting-event disjointness. For the two separated arcs, after a hit on the first arc the ordinary Brownian path has positive probability to hit the second before T; the relevant hitting function is strictly positive on the connected complement of the second arc. The strong Markov argument thus supports the claimed positive overlap.

The rectangle separation-of-variables formula has the correct aspect ratio, signs, and side convention. The positive term magnitudes at the center strictly decrease, so the four-term even partial sum is a lower bound and adding the fifth term is an upper bound. Machin's identity and positive exponential Taylor-tail bounds are used in their correct directions. The bracket encloses the short-side probability, not its complement, and cannot by itself identify the arbitrary-obstacle supremum.

## 7. Replays and their limitations

Environment independently checked: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0. Commands executed from the frozen scripts, with outputs directed only into this separate audit directory:

- `python3 .../public/controls/verify.py`: PASS, 27 controls; byte-identical replay.
- `python3 .../public/controls/explore_two_arcs.py`: completed; byte-identical replay.

The exact controls verify encoded arithmetic and selected finite event patterns. Some are elementary consistency checks or deliberate mutant rejections. They do not mechanically check the selector lemma, analytic time change, martingale argument, literature theorem, or sharpness.

The finite-difference code uses the stated logarithmic cylinder, periodic angular grid, slit-node Dirichlet data, and reflecting truncated inner boundary. The three approximate values are 0.0036338605876081054, 0.00421646315226311, and 0.0045144475626956145. Empty and full-circle controls behave as recorded. The code does not include a continuum endpoint-error certificate, an infinite-cylinder truncation estimate, a justified one-sided convergence assertion, or a global optimization. Identical numerical replay adds reproducibility, not those missing theorems.

## 8. Independent source checks and access limits

- [Hayman--Lingham, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200), printed p. 67: statement/update rechecked, including notation in the rendered page. Its update describes a connected special case; it does not certify a full arbitrary-closed-set answer.
- [Marshall--Sundberg author abstract](https://library.slmath.org/preprints/files/1995/1995-098/1995-098abs.html): confirms a continuum hypothesis, the numerical constant, and the rectangle interpretation. This is a theorem-statement source, not an independently checked full proof.
- [Marshall's selected-publications retrospective](https://sites.math.washington.edu/~marshall/myreviews/select.pdf): explicitly restricts the Fuchs result to connected sets.
- [Betsakos primary preprint, indexed excerpt](https://citeseerx.ist.psu.edu/document?doi=b279c6c7daf32cfcb269c82e93749b6ed9d87d9e&repid=rep1&type=pdf): the primary-document excerpt rechecked for Problem 1, concerning two curves. Direct PDF retrieval failed. This audit does not promote that excerpt to full-paper verification.
- [Markowsky, analytic-image Brownian motion](https://www.acadsci.fi/mathematica/Vol43/Markowsky.html): a supplementary primary source explicitly describes the extension to noninjective analytic maps; the pullback audit above also supplies the concrete time-change reasoning needed here.

The catalogue page remained inaccessible. The 1989 DOI request and the old linked 1996 PostScript/DVI routes did not yield a full usable proof. This audit therefore retains, rather than erases, the frozen source limitations. Bounded fresh searches on Fuchs, radial projection, Hall's lemma, two curves, and the target identifier did not establish a later unrestricted resolution. That negative search result is not an exhaustive literature theorem.

Only original audit text, the correction, replay outputs, and hash metadata are included here. The source-page research image is kept separately and is not part of the public audit deliverable. No source PDF or catalogue corpus is redistributed.

## 9. Gate and reproducibility contract

Use the corrected proof only with the otherwise unchanged frozen public files. `corrected-public-SHA256SUMS` binds that exact corrected public bundle. `audit_results.json` records the input and output hashes, defect, repair, replay results, and scope limitations. `SHA256SUMS` binds this complete audit deliverable, excluding itself.

`verify_audit.py` checks all these byte identities and applies the supplied patch in a temporary directory to verify that it produces the corrected proof. It does not edit the frozen package. Publication may describe this as an audited unresolved checkpoint with the stated partial bounds, conditional finite-component result, and explicitly noncertified numerical experiment. It must not describe the full target as solved, the sharp constant as found, or the inaccessible literature proofs as independently checked.
