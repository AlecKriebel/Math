# Independent review: spherical Plateau networks and volume labels

**Verdict: PASS_SCOPED_INSTABILITY_WITH_SOURCE_HOLD.** The two configurations and their negative constrained second variations are correct for the stated two-label volume constraint. No mandatory mathematical correction was found. Recommend **unsolved, 1/5**, retaining the original-question interpretation hold.

Reviewed on 30 September 2026 by a separate GPT-6 Astra agent at xhigh effort. This is an independent AI review, not human peer review or a novelty certification. The reviewed PARTIAL.md has SHA-256
**1a692897015355a3797c6aba435e10c5434b0e6a5f69e49e64ef3bf9b04dbda5**.

## Source scope and verdict limits

The indexed primary text of [Sullivan–Morgan, Problem 3](https://citeseerx.ist.psu.edu/document?doi=13ac2665ff2736dd27fc8780991a091b9698d8f5&repid=rep1&type=pdf) asks: “Is any such cluster necessarily stable in the sense of having non-negative second variation?” Its antecedent concerns spherical pieces obeying Plateau's rules. I independently retrieved the indexed introduction and Problems 2–3. The surrounding text prescribes enclosed volumes and allows disconnected regions in Problem 2. Direct retrieval of the full original PDF failed; this review does not claim to have visually inspected it or resolved its unstated conventions.

The exact mathematical statement proved in the package is narrower and unambiguous: two disjoint physical satellites share one constrained volume, and their interface pieces need not share a single supporting sphere for each labeled pair. It is an instability theorem for that explicitly defined class. It is not a certified resolution of the intended historical question under separately preserved physical-bubble volumes or a globally spherical pair-interface requirement.

The current [Milman survey](https://arxiv.org/abs/2510.07078v2), Section 9(3), still presents Kusner's question; I read and visually inspected that item. Its arXiv metadata identifies the July 2026 revision and ICM proceedings reference. I did not independently compare the proceedings PDF.

## Geometry, regularity, and stationarity

At the planar base, the upper satellite is the unit-ball cap centered at $e$ above $z=1/2$, the lower one is its reflection, and the central cell is the unit-ball band. Their interiors are disjoint. The two circular interfaces have positive radius $\sqrt3/2$ and are separated; the intervening spherical band connects the entire interface network. The only singularities are ordinary triple circles.

At the fully spherical base, the upper satellite is the intersection of the balls of radii $1/2$ and $1$ centered at $(\sqrt3/2)e$ and $\sqrt3e$. Its reflected copy lies strictly below the equatorial plane. Each satellite is convex and connected. In the central cell, a vertical segment toward $z=0$ stays outside the removed north and south balls. Every such point therefore connects to the equatorial disk, proving connectedness. All interfaces lie on finite-radius spheres, with triple circles at $z=\pm\sqrt3/2$ and radius $1/2$.

At either base, the three oriented unit normals obey
\[
n_{AB}+n_{BO}-n_{AO}=0.
\]
Rotation in the normal plane to a triple circle gives the corresponding conormal balance, so the sheets meet at $120^\circ$. Curvatures, with the submitted normal convention, are the pressure differences: $(p_A,p_B)=(2,2)$ at the planar base and $(4,2)$ at the fully spherical base. Interface first variations and triple-circle boundary terms therefore give
\[
\delta\mathcal A=p_A\delta|A|+p_B\delta|B|
\]
for every smooth compactly supported ambient field. This establishes stationarity for the merged labels. No minimization claim is needed.

The nearby geometric family also has the stated mean curvatures and angle balance. Its internal equation
\[
(1-r)|x|^2-2d(r)z+1=0,\qquad d(r)^2=1+r^2-r,
\]
has unit normal $((1-r)x-d(r)e)/r$ and curvature $2/r-2$. At $r=1$ the selected sheet passes smoothly through its planar graph limit; at $r=1/2$ it is a regular spherical cap. Thus the cap formulas describe a nonsingular local family, with no collision of the two junction circles.

I checked the signed cap-volume term, the total-area accounting, both derivative tables, and the first-variation identity along that family. Independent horizontal-slice integrals reproduce the initial volumes. In particular, at $r=1/2$ the satellite cross-sectional area switches at $z=\sqrt3/2$ between the internal unit sphere and the external radius-$1/2$ sphere; integrating these two pieces yields $3\pi/4-3\sqrt3\pi/8$, as submitted.

## The deformation is an ambient field

The polynomial field
\[
Z(x)=zx-\frac{1+|x|^2}{2}e
\]
has zero normal component on the central unit sphere. At the planar base, it gives the required outer-cap speed $(1+z)/2$ and the required internal graph speed. At the fully spherical base, $(4/\sqrt3)Z$ gives outer normal speed $1$ and internal normal speed $|x|^2$. These are identities on the whole sheets, including their common circle, rather than independently assigned sheet displacements.

The upper sheets are compact and lie in a positive halfspace bounded away from zero. A smooth compact cutoff can consequently equal one near their closures and be supported in $z>1/4$. The reflected negative field admits a disjoint lower cutoff. Their sum is smooth throughout space and retains zero central-sphere normal speed, even where the cutoffs vary. It is a legitimate compactly supported ambient vector field. Reflection and the opposite sign make the two satellite volume derivatives cancel; their exchanges with the central cell cancel as well.

## Independent direct second-variation calculation

The [Milman–Xu paper](https://arxiv.org/abs/2504.11185v1), Section 1.2, gives the standard Jacobi form for a stationary regular partition and explains its dependence only on the physical normal field. I read the setup and visually checked equations (1.1)–(1.3). Applying that form supplies an independent verification which does not depend on the submitted second derivatives of cap-volume formulas.

In Euclidean space let $L=\Delta_\Sigma+|\mathrm{II}|^2$. The contribution of a sheet is
\[
-\int_\Sigma fLf+
\int_{\partial\Sigma}(\partial_\eta f-\overline{\mathrm{II}}f)f,
\]
where $\eta$ is its outward conormal and the junction coefficient is the signed curvature combination from the cited formula.

**Fully spherical case.** On the upper exterior hemisphere, $f=1$, the radius is $1/2$, and $Lf=8$. On the internal unit-sphere cap, use $u=z-\sqrt3\in[-1,-\sqrt3/2]$. Then
\[
f=4+2\sqrt3u,\qquad
\Delta_\Sigma f=-2(f-4),\qquad Lf=8.
\]
The outer junction coefficient is $(1-1)/\sqrt3=0$, matching its zero conormal derivative. On the internal cap, $f=1$ at the junction, $\partial_\eta f=\sqrt3$, and the coefficient is $(2+1)/\sqrt3=\sqrt3$. Both boundary terms vanish. The central normal field is identically zero.

The satellite's first-order volume flux is therefore
\[
v=\frac{\pi}{2}
 +2\pi\int_{-1}^{-\sqrt3/2}(4+2\sqrt3u)\,du
 =\frac{17-9\sqrt3}{2}\pi>0.
\]
The upper sheets contribute $-8v$. Reflection and reversal of the lower normal field give the same quadratic contribution. Consequently
\[
Q=-16v=(72\sqrt3-136)\pi<0.
\]
The sign follows, without rounding, from $243<289$.

**Planar case.** On the outer unit sphere write $u=z-1\in[-1/2,1]$. Its normal speed is $1+u/2$ and $Lf=2$. On the internal disk, with radial coordinate $\rho$, the speed is $\rho^2/2+3/8$ and again $Lf=2$. The respective fluxes are $27\pi/8$ and $27\pi/64$, whose sum is $243\pi/64$.

At the outer boundary the conormal derivative is $-\sqrt3/4$, equal to the coefficient $-1/\sqrt3$ times the boundary speed $3/4$. At the disk boundary the conormal derivative is $\sqrt3/2$, equal to $(2/\sqrt3)(3/4)$. The boundary terms again vanish. Doubling the upper contribution gives
\[
Q=-4(243\pi/64)=-243\pi/16.
\]

As another consistency check, stationarity of the three-physical-cell family gives, after differentiating its first variation along $r_\pm=r_0\pm t$,
\[
Q=-\frac{4}{r_0^2}V'(r_0),
\]
which agrees with both independent flux computations and both submitted Hessians.

## Exact volume preservation and the excluded stronger claims

The first-order exchange changes the individual satellite volumes by the nonzero values $v,-v$. It preserves their sum and the central-cell volume. Fields supported on separate regular outer patches of $A$ and $B$ have independent two-label volume derivatives. Apply the implicit function theorem to their flows composed with the exchange flow. Since the initial volume derivative is zero, the correction parameters have zero first derivative and start at order $t^2$.

Stationarity then cancels the correction's second-order area contribution against the pressure-weighted second-order volume change. The resulting exactly volume-preserving curve has area second derivative equal to the negative $Q$ computed above. Thus the result is not an artifact of using only linearized constraints.

If the satellite volumes are separately fixed, this particular direction is inadmissible. Moreover, merging the satellites puts distinct supporting spheres into the same labeled interfaces. A single sphere cannot contain both open outer patches, and likewise cannot contain both internal patches. The example therefore fails a global pair-interface sphericity requirement. The report makes no claim about stability after imposing those stronger constraints.

The paper's definition permits disconnected cells, but its positive theorem has further spherical-Voronoi and Möbius-flat hypotheses. Its Remark 1.4 and Corollary 1.7 retain the admissible-range condition $f=L_Vu$. The submitted elementary observation that constant-potential Laplacians on separate closed components have zero integral on each component is correct. It identifies a range issue; it does not contradict that theorem or certify its full analytic proof.

## Reproducibility

All **270** submitted exact assertions replay successfully, reproducing the receipt byte for byte. The independently written verifier passes **363** exact assertions. It starts from normal-flux integrals and the direct Jacobi operator, checks the signed junction terms, uses horizontal slices for the initial volumes, and separately tests exact points on the spherical pieces and triple circle.

Finite controls supplement the analytic argument; they do not settle historical source intent. The original target remains **unsolved, 1/5** in this package. The immutable reviewed snapshot and both verifiers are included in the eight-file publication list in review_summary.json. No author mathematical file was changed. Rendered source pages, auxiliary stdout files, and source PDFs are excluded from that list.
